from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from threading import RLock
from typing import Any
from uuid import uuid4

from .collector import collect
from .regression import evaluate_rules, read_json


FINDING_DEFINITIONS = {
    "building_element_proxies": {
        "source_rule_id": "IQA-M1-REVIEW-001",
        "title": "IfcBuildingElementProxy fachlich prüfen",
        "severity": "warning",
    },
    "uncontained_elements": {
        "source_rule_id": "IQA-M1-SPAT-003",
        "title": "Element ohne räumliche Zuordnung",
        "severity": "warning",
    },
    "opening_elements_without_void_relation": {
        "source_rule_id": "IQA-M1-OPEN-001",
        "title": "Öffnung ohne IfcRelVoidsElement-Beziehung",
        "severity": "warning",
    },
    "slab_sockel_stuetze_with_lv_einzelfundament": {
        "source_rule_id": "IQA-M1-REVIEW-001",
        "title": "IfcSlab Sockel_Stütze mit LV-Ident Einzelfundament prüfen",
        "severity": "warning",
    },
    "einzelfundament_without_gross_volume": {
        "source_rule_id": "IQA-M1-QTY-006",
        "title": "Einzelfundament ohne Bruttovolumen",
        "severity": "error",
    },
    "elements_without_baunummer": {
        "source_rule_id": "IQA-M1-FIELD-002",
        "title": "Baunummer fehlt",
        "severity": "warning",
    },
    "elements_without_bruttogewicht": {
        "source_rule_id": "IQA-M1-FIELD-002",
        "title": "Bruttogewicht fehlt",
        "severity": "info",
    },
}


class AnalysisNotFound(KeyError):
    pass


class ObjectNotFound(KeyError):
    pass


class AnalysisService:
    """Application service shared by API, future UI adapters and tests."""

    def __init__(self, baseline_path: str | Path, rules_path: str | Path):
        self.baseline_path = Path(baseline_path).resolve()
        self.rules_path = Path(rules_path).resolve()
        self.baseline = read_json(self.baseline_path)
        self.catalog = read_json(self.rules_path)
        self._analyses: dict[str, dict[str, Any]] = {}
        self._lock = RLock()

    def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "ifc-quantity-agent-mvp1-api",
            "api_version": "1.1.0",
            "rule_package": {
                "id": self.catalog["package_id"],
                "version": self.catalog["package_version"],
                "rule_count": len(self.catalog["rules"]),
            },
        }

    def rule_package(self) -> dict[str, Any]:
        return self.catalog

    def run_analysis(self, ifc_path: str | Path, display_name: str | None = None) -> dict[str, Any]:
        actual = collect(ifc_path, model_file_name=display_name)
        results = evaluate_rules(actual, self.baseline, self.catalog)
        result_rows = [asdict(result) for result in results]
        summary = {
            "total": len(results),
            "passed": sum(item.status == "passed" for item in results),
            "failed": sum(item.status == "failed" for item in results),
            "error": sum(item.status == "error" for item in results),
        }
        summary["passed_all"] = summary["failed"] == 0 and summary["error"] == 0

        analysis_id = str(uuid4())
        file_name = display_name or actual["model"]["file_name"]
        findings = self._build_findings(analysis_id, actual["finding_evidence"])
        objects = {row["global_id"]: row for row in actual["objects"] if row.get("global_id")}
        finding_ids_by_object: dict[str, list[str]] = {}
        for finding in findings:
            finding_ids_by_object.setdefault(finding["global_id"], []).append(finding["finding_id"])
        for global_id, row in objects.items():
            row["finding_ids"] = finding_ids_by_object.get(global_id, [])
            row["finding_count"] = len(row["finding_ids"])

        record = {
            "analysis_id": analysis_id,
            "status": "completed",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "file_name": file_name,
            "summary": summary,
            "model": actual["model"],
            "units": actual["units"],
            "counts": actual["counts"],
            "spatial": actual["spatial"],
            "ifc_class_counts": actual["ifc_class_counts"],
            "property_set_coverage": actual["property_set_coverage"],
            "lv_ident": actual["lv_ident"],
            "key_field_coverage": actual["key_field_coverage"],
            "material_assignments": actual["material_assignments"],
            "assemblies": actual["assemblies"],
            "openings": actual["openings"],
            "quantities": actual["quantities"],
            "rule_results": result_rows,
            "findings": findings,
            "objects": objects,
            "objects_by_step": {row["step_id"]: row for row in actual["objects"]},
            "structure": actual["model_structure"],
        }
        with self._lock:
            self._analyses[analysis_id] = record
        return self.analysis_created(record)

    @staticmethod
    def _build_findings(analysis_id: str, evidence: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        for finding_type, rows in evidence.items():
            definition = FINDING_DEFINITIONS.get(finding_type)
            if not definition:
                continue
            for row in rows:
                global_id = row.get("global_id")
                digest = sha256(f"{analysis_id}|{finding_type}|{global_id}".encode("utf-8")).hexdigest()[:16]
                findings.append({
                    "finding_id": f"f-{digest}",
                    "finding_type": finding_type,
                    "source_rule_id": definition["source_rule_id"],
                    "title": definition["title"],
                    "severity": definition["severity"],
                    "status": "open",
                    "global_id": global_id,
                    "ifc_class": row.get("ifc_class"),
                    "name": row.get("name"),
                    "evidence": row,
                })
        return findings

    @staticmethod
    def analysis_created(record: dict[str, Any]) -> dict[str, Any]:
        analysis_id = record["analysis_id"]
        return {
            "analysis_id": analysis_id,
            "status": record["status"],
            "created_at_utc": record["created_at_utc"],
            "file_name": record["file_name"],
            "model_sha256": record["model"]["sha256"],
            "summary": record["summary"],
            "links": {
                "overview": f"/api/v1/analyses/{analysis_id}/overview",
                "rule_results": f"/api/v1/analyses/{analysis_id}/rule-results",
                "findings": f"/api/v1/analyses/{analysis_id}/findings",
                "objects": f"/api/v1/analyses/{analysis_id}/objects",
                "structure": f"/api/v1/analyses/{analysis_id}/structure",
            },
        }

    def _get(self, analysis_id: str) -> dict[str, Any]:
        with self._lock:
            try:
                return self._analyses[analysis_id]
            except KeyError as exc:
                raise AnalysisNotFound(analysis_id) from exc

    def overview(self, analysis_id: str) -> dict[str, Any]:
        record = self._get(analysis_id)
        return {
            key: record[key]
            for key in (
                "analysis_id", "status", "created_at_utc", "file_name", "summary",
                "model", "units", "counts", "spatial", "ifc_class_counts",
                "property_set_coverage", "lv_ident", "key_field_coverage",
                "material_assignments", "assemblies", "openings", "quantities",
            )
        }

    def rule_results(
        self,
        analysis_id: str,
        *,
        status: str | None = None,
        category: str | None = None,
        severity: str | None = None,
        rule_id: str | None = None,
        include_evidence: bool = False,
    ) -> dict[str, Any]:
        rows = self._get(analysis_id)["rule_results"]
        filtered = [
            row for row in rows
            if (status is None or row["status"] == status)
            and (category is None or row["category"] == category)
            and (severity is None or row["severity"] == severity)
            and (rule_id is None or row["rule_id"] == rule_id)
        ]
        if not include_evidence:
            filtered = [{key: value for key, value in row.items() if key != "evidence"} for row in filtered]
        return {"analysis_id": analysis_id, "total": len(filtered), "items": filtered}

    def findings(
        self,
        analysis_id: str,
        *,
        finding_type: str | None = None,
        severity: str | None = None,
        status: str | None = None,
        global_id: str | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> dict[str, Any]:
        rows = self._get(analysis_id)["findings"]
        filtered = [
            row for row in rows
            if (finding_type is None or row["finding_type"] == finding_type)
            and (severity is None or row["severity"] == severity)
            and (status is None or row["status"] == status)
            and (global_id is None or row["global_id"] == global_id)
        ]
        return {"analysis_id": analysis_id, "total": len(filtered), "offset": offset, "limit": limit, "items": filtered[offset:offset + limit]}

    def objects(
        self,
        analysis_id: str,
        *,
        ifc_class: str | None = None,
        lv_ident: str | None = None,
        missing_lv_ident: bool | None = None,
        has_findings: bool | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> dict[str, Any]:
        rows = list(self._get(analysis_id)["objects"].values())
        filtered = [
            row for row in rows
            if (ifc_class is None or row["ifc_class"] == ifc_class)
            and (lv_ident is None or row["lv_ident"] == lv_ident)
            and (missing_lv_ident is None or (row["lv_ident"] is None) == missing_lv_ident)
            and (has_findings is None or (row["finding_count"] > 0) == has_findings)
        ]
        summaries = [{
            key: row[key]
            for key in (
                "global_id", "step_id", "ifc_class", "name", "object_type", "tag",
                "has_representation", "lv_ident", "materials", "review_flags", "finding_count",
            )
        } for row in filtered[offset:offset + limit]]
        return {"analysis_id": analysis_id, "total": len(filtered), "offset": offset, "limit": limit, "items": summaries}

    def object_detail(self, analysis_id: str, global_id: str) -> dict[str, Any]:
        record = self._get(analysis_id)
        try:
            row = dict(record["objects"][global_id])
        except KeyError as exc:
            raise ObjectNotFound(global_id) from exc
        row["findings"] = [item for item in record["findings"] if item["global_id"] == global_id]
        return {"analysis_id": analysis_id, "object": row}


    def structure(self, analysis_id: str) -> dict[str, Any]:
        return {"analysis_id": analysis_id, **self._get(analysis_id)["structure"]}

    def object_detail_by_step(self, analysis_id: str, step_id: int) -> dict[str, Any]:
        record = self._get(analysis_id)
        try:
            row = dict(record["objects_by_step"][step_id])
        except KeyError as exc:
            raise ObjectNotFound(step_id) from exc
        gid = row.get("global_id")
        unique = gid and sum(o.get("global_id") == gid for o in record["objects_by_step"].values()) == 1
        row["findings"] = [f for f in record["findings"] if unique and f["global_id"] == gid]
        row["finding_identity_ambiguous"] = not bool(unique)
        return {"analysis_id": analysis_id, "object": row}
