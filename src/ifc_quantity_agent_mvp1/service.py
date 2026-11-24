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
        "title": "IfcBuildingElementProxy fachlich prÃ¼fen",
        "severity": "warning",
    },
    "uncontained_elements": {
        "source_rule_id": "IQA-M1-SPAT-003",
        "title": "Element ohne rÃ¤umliche Zuordnung",
        "severity": "warning",
    },
    "opening_elements_without_void_relation": {
        "source_rule_id": "IQA-M1-OPEN-001",
        "title": "Ã–ffnung ohne IfcRelVoidsElement-Beziehung",
        "severity": "warning",
    },
    "slab_sockel_stuetze_with_lv_einzelfundament": {
        "source_rule_id": "IQA-M1-REVIEW-001",
        "title": "IfcSlab Sockel_StÃ¼tze mit LV-Ident Einzelfundament prÃ¼fen",
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
            "api_version": "1.2.0",
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
        missing_net_volume: bool | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> dict[str, Any]:
        rows = list(self._get(analysis_id)["objects"].values())
        filtered = [
            row for row in rows
            if (ifc_class is None or row["ifc_class"] == ifc_class)
            and (lv_ident is None or row["lv_ident"] == lv_ident)
            and (missing_lv_ident is None or (not row["lv_ident"]) == missing_lv_ident)
            and (has_findings is None or (row["finding_count"] > 0) == has_findings)
            and (missing_net_volume is None or (row["quantities"]["net_volume"]["value"] is None) == missing_net_volume)
        ]
        summaries = [{
            **{
                key: row[key]
                for key in (
                    "global_id", "step_id", "ifc_class", "name", "object_type", "tag",
                    "has_representation", "lv_ident", "materials", "review_flags", "finding_count",
                )
            },
            "gross_701": row["quantities"]["gross_volume_701"]["value"],
            "custom_qto": row["quantities"]["custom_gross_volume"]["value"],
            "net_volume": row["quantities"]["net_volume"]["value"],
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


    QUANTITY_SOURCES = (
        ("gross_701", "gross_volume_701"),
        ("custom_qto", "custom_gross_volume"),
        ("net_volume", "net_volume"),
    )

    def quantity_summary(self, analysis_id: str, *, group_by: str = "lv_ident", material: str | None = None) -> dict[str, Any]:
        """Aggregate volumes per group. Sources stay separate; missing values are counted, never replaced."""
        if group_by not in ("lv_ident", "ifc_class"):
            raise ValueError(f"Unbekannte Gruppierung: {group_by}")
        rows = list(self._get(analysis_id)["objects_by_step"].values())
        if material is not None:
            rows = [row for row in rows if material in (row.get("materials") or [])]

        def new_bucket() -> dict[str, Any]:
            bucket: dict[str, Any] = {"object_count": 0, "finding_count": 0, "materials": {}, "step_ids": []}
            for source, _ in self.QUANTITY_SOURCES:
                bucket[source] = {"sum": 0.0, "objects_with_value": 0, "objects_missing": 0}
            return bucket

        buckets: dict[str, dict[str, Any]] = {}
        totals = new_bucket()
        unit = "m3"
        for row in rows:
            key = (row.get("lv_ident") or None) if group_by == "lv_ident" else row.get("ifc_class")
            key = key or ""
            for bucket in (buckets.setdefault(key, new_bucket()), totals):
                bucket["object_count"] += 1
                bucket["finding_count"] += row.get("finding_count", 0)
                for name in row.get("materials") or ["(ohne Material)"]:
                    bucket["materials"][name] = bucket["materials"].get(name, 0) + 1
                for source, quantity_key in self.QUANTITY_SOURCES:
                    value = row["quantities"][quantity_key]["value"]
                    if value is None:
                        bucket[source]["objects_missing"] += 1
                    else:
                        bucket[source]["sum"] += value
                        bucket[source]["objects_with_value"] += 1
            buckets[key]["step_ids"].append(row["step_id"])

        source_paths = {
            "gross_701": "BASF_General.701_Bruttovolumen",
            "custom_qto": "QTO.QTO.01_Bruttovolumen_m3",
            "net_volume": "Qto_*BaseQuantities.NetVolume",
        }

        def finish(bucket: dict[str, Any]) -> dict[str, Any]:
            out = {k: v for k, v in bucket.items() if k not in {s for s, _ in self.QUANTITY_SOURCES}}
            out["materials"] = [{"name": n, "objects": c} for n, c in sorted(bucket["materials"].items())]
            for source, _ in self.QUANTITY_SOURCES:
                entry = dict(bucket[source])
                entry["sum"] = entry["sum"] if entry["objects_with_value"] else None
                entry["source_path"] = source_paths[source]
                out[source] = entry
            return out

        groups = []
        for key in sorted(buckets, key=lambda k: (k == "", k)):
            item = finish(buckets[key])
            item["key"] = key or None
            item["label"] = key or ("ohne LV-Ident" if group_by == "lv_ident" else "ohne IFC-Klasse")
            item["unassigned"] = key == ""
            groups.append(item)
        total = finish(totals)
        warnings = []
        for source, text in (("net_volume", "Netto-Volumen"), ("gross_701", "Bruttovolumen 701"), ("custom_qto", "QTO-Bruttovolumen")):
            if total[source]["objects_missing"]:
                warnings.append({"code": f"{source}_missing", "message": f"{total[source]['objects_missing']} Objekte ohne {text}", "objects": total[source]["objects_missing"]})
        unassigned = next((g for g in groups if g["unassigned"]), None)
        if unassigned and group_by == "lv_ident":
            warnings.append({"code": "lv_ident_missing", "message": f"{unassigned['object_count']} Objekte ohne LV-Ident", "objects": unassigned["object_count"]})
        reconciliation = {
            source: abs(sum(g[source]["sum"] or 0.0 for g in groups) - (total[source]["sum"] or 0.0)) < 1e-9
            and sum(g[source]["objects_with_value"] for g in groups) == total[source]["objects_with_value"]
            for source, _ in self.QUANTITY_SOURCES
        }
        reconciliation["object_count"] = sum(g["object_count"] for g in groups) == total["object_count"]
        total.pop("step_ids", None)
        return {
            "analysis_id": analysis_id,
            "group_by": group_by,
            "unit": unit,
            "material_filter": material,
            "basis": {"rule_package": self.catalog["package_version"], "baseline_version": self.baseline.get("document_version")},
            "groups": groups,
            "totals": total,
            "reconciliation": reconciliation,
            "warnings": warnings,
        }

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
