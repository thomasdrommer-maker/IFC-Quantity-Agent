from __future__ import annotations

import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Literal

from fastapi import FastAPI, File, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from .service import AnalysisNotFound, AnalysisService, ObjectNotFound


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class HealthResponse(ApiModel):
    status: Literal["ok"]
    service: str
    api_version: str
    rule_package: dict[str, Any]


class AnalysisCreatedResponse(ApiModel):
    analysis_id: str
    status: Literal["completed"]
    created_at_utc: str
    file_name: str
    model_sha256: str
    summary: dict[str, Any]
    links: dict[str, str]


class RulePackageResponse(ApiModel):
    package_id: str
    package_version: str
    title: str
    status: str
    valid_from: str
    basis: str
    baseline_version: str
    model_types: list[str]
    id_convention: str
    rules: list[dict[str, Any]]


class OverviewResponse(ApiModel):
    analysis_id: str
    status: Literal["completed"]
    created_at_utc: str
    file_name: str
    summary: dict[str, Any]
    model: dict[str, Any]
    units: dict[str, Any]
    counts: dict[str, Any]
    spatial: dict[str, Any]
    ifc_class_counts: dict[str, int]
    property_set_coverage: dict[str, int]
    lv_ident: dict[str, Any]
    key_field_coverage: dict[str, Any]
    material_assignments: dict[str, int]
    assemblies: dict[str, Any]
    openings: dict[str, Any]
    quantities: dict[str, Any]


class CollectionResponse(ApiModel):
    analysis_id: str
    total: int
    items: list[dict[str, Any]]
    offset: int | None = None
    limit: int | None = None


class ObjectDetailResponse(ApiModel):
    analysis_id: str
    object: dict[str, Any]


def default_service() -> AnalysisService:
    package_root = Path(__file__).resolve().parents[2]
    return AnalysisService(
        package_root / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json",
        package_root / "rules" / "mvp1_rules_v0.1.json",
    )


def create_app(service: AnalysisService | None = None) -> FastAPI:
    analysis_service = service or default_service()
    app = FastAPI(
        title="IFC Quantity Agent MVP-1 API",
        version="1.0.0",
        description=(
            "Plattformneutrale REST-API für IFC-Inventur, reproduzierbare "
            "MVP-1-Regelergebnisse, Prüfbericht und Objekt-Drilldown."
        ),
        contact={"name": "IFC Quantity Agent"},
        license_info={"name": "Internal project artifact"},
    )
    app.state.analysis_service = analysis_service
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in os.getenv("IQA_CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",") if origin.strip()],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Accept"],
    )

    @app.get("/api/v1/health", response_model=HealthResponse, tags=["System"])
    def health() -> dict[str, Any]:
        return analysis_service.health()

    @app.get("/api/v1/rule-packages/current", response_model=RulePackageResponse, tags=["Rules"])
    def current_rule_package() -> dict[str, Any]:
        return analysis_service.rule_package()

    @app.post(
        "/api/v1/analyses",
        response_model=AnalysisCreatedResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Analyses"],
        summary="IFC-Datei hochladen und synchron analysieren",
    )
    async def create_analysis(file: UploadFile = File(..., description="IFC-SPF-Datei (*.ifc)")) -> dict[str, Any]:
        file_name = Path(file.filename or "model.ifc").name
        if Path(file_name).suffix.lower() != ".ifc":
            raise HTTPException(status_code=415, detail="Nur IFC-Dateien mit der Endung .ifc werden akzeptiert.")
        max_bytes = int(os.getenv("IQA_MAX_UPLOAD_BYTES", str(100 * 1024 * 1024)))
        size = 0
        temp_path: Path | None = None
        try:
            with NamedTemporaryFile(prefix="iqa_", suffix=".ifc", delete=False) as handle:
                temp_path = Path(handle.name)
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > max_bytes:
                        raise HTTPException(status_code=413, detail=f"IFC-Datei überschreitet das Limit von {max_bytes} Byte.")
                    handle.write(chunk)
            try:
                return analysis_service.run_analysis(temp_path, display_name=file_name)
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(status_code=422, detail=f"IFC-Datei konnte nicht analysiert werden: {exc}") from exc
        finally:
            await file.close()
            if temp_path and temp_path.exists():
                temp_path.unlink()

    @app.get("/api/v1/analyses/{analysis_id}/overview", response_model=OverviewResponse, tags=["Project overview"])
    def overview(analysis_id: str) -> dict[str, Any]:
        try:
            return analysis_service.overview(analysis_id)
        except AnalysisNotFound:
            raise HTTPException(status_code=404, detail="Analyse nicht gefunden.")

    @app.get("/api/v1/analyses/{analysis_id}/rule-results", response_model=CollectionResponse, tags=["Audit"])
    def rule_results(
        analysis_id: str,
        status_filter: Literal["passed", "failed", "error"] | None = Query(None, alias="status"),
        category: str | None = None,
        severity: str | None = None,
        rule_id: str | None = None,
        include_evidence: bool = False,
    ) -> dict[str, Any]:
        try:
            return analysis_service.rule_results(
                analysis_id,
                status=status_filter,
                category=category,
                severity=severity,
                rule_id=rule_id,
                include_evidence=include_evidence,
            )
        except AnalysisNotFound:
            raise HTTPException(status_code=404, detail="Analyse nicht gefunden.")

    @app.get("/api/v1/analyses/{analysis_id}/findings", response_model=CollectionResponse, tags=["Audit"])
    def findings(
        analysis_id: str,
        finding_type: str | None = None,
        severity: str | None = None,
        status_filter: str | None = Query(None, alias="status"),
        global_id: str | None = None,
        offset: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
    ) -> dict[str, Any]:
        try:
            return analysis_service.findings(
                analysis_id,
                finding_type=finding_type,
                severity=severity,
                status=status_filter,
                global_id=global_id,
                offset=offset,
                limit=limit,
            )
        except AnalysisNotFound:
            raise HTTPException(status_code=404, detail="Analyse nicht gefunden.")

    @app.get("/api/v1/analyses/{analysis_id}/objects", response_model=CollectionResponse, tags=["Objects"])
    def objects(
        analysis_id: str,
        ifc_class: str | None = None,
        lv_ident: str | None = None,
        missing_lv_ident: bool | None = None,
        has_findings: bool | None = None,
        offset: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
    ) -> dict[str, Any]:
        try:
            return analysis_service.objects(
                analysis_id,
                ifc_class=ifc_class,
                lv_ident=lv_ident,
                missing_lv_ident=missing_lv_ident,
                has_findings=has_findings,
                offset=offset,
                limit=limit,
            )
        except AnalysisNotFound:
            raise HTTPException(status_code=404, detail="Analyse nicht gefunden.")

    @app.get("/api/v1/analyses/{analysis_id}/objects/{global_id}", response_model=ObjectDetailResponse, tags=["Objects"])
    def object_detail(analysis_id: str, global_id: str) -> dict[str, Any]:
        try:
            return analysis_service.object_detail(analysis_id, global_id)
        except AnalysisNotFound:
            raise HTTPException(status_code=404, detail="Analyse nicht gefunden.")
        except ObjectNotFound:
            raise HTTPException(status_code=404, detail="Objekt nicht gefunden.")

    return app


app = create_app()

