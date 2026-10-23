from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element, SubElement, ElementTree


def read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_path(data: dict[str, Any], path: str) -> Any:
    value: Any = data
    for part in path.split("."):
        value = value[part]
    return value


def _values_equal(expected: Any, actual: Any, tolerance: float) -> bool:
    if isinstance(expected, bool) or isinstance(actual, bool):
        return expected is actual
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return abs(float(expected) - float(actual)) <= tolerance
    return expected == actual


def _subset_equal(expected: Any, actual: Any, tolerance: float) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _subset_equal(value, actual[key], tolerance)
            for key, value in expected.items()
        )
    if isinstance(expected, list):
        return isinstance(actual, list) and len(expected) == len(actual) and all(
            _subset_equal(e, a, tolerance) for e, a in zip(expected, actual)
        )
    return _values_equal(expected, actual, tolerance)


@dataclass
class RuleResult:
    rule_id: str
    rule_version: str
    title: str
    category: str
    severity: str
    status: str
    expected_path: str
    actual_path: str
    expected: Any = None
    actual: Any = None
    message: str = ""
    evidence: Any = None


def evaluate_rules(
    actual: dict[str, Any],
    baseline: dict[str, Any],
    catalog: dict[str, Any],
) -> list[RuleResult]:
    results: list[RuleResult] = []
    for rule in catalog["rules"]:
        try:
            expected = resolve_path(baseline, rule["expected_path"])
            observed = resolve_path(actual, rule["actual_path"])
            tolerance = float(rule.get("tolerance", 0.0))
            comparator = rule.get("comparator", "equals")
            if comparator == "equals":
                passed = _values_equal(expected, observed, tolerance)
            elif comparator == "subset_equal":
                passed = _subset_equal(expected, observed, tolerance)
            else:
                raise ValueError(f"Unbekannter Comparator: {comparator}")
            evidence = None
            if rule.get("evidence_path"):
                try:
                    evidence = resolve_path(actual, rule["evidence_path"])
                except KeyError:
                    evidence = None
            results.append(RuleResult(
                rule_id=rule["id"],
                rule_version=rule["version"],
                title=rule["title"],
                category=rule["category"],
                severity=rule["severity"],
                status="passed" if passed else "failed",
                expected_path=rule["expected_path"],
                actual_path=rule["actual_path"],
                expected=expected,
                actual=observed,
                message="Sollwert erreicht" if passed else "Soll-/Ist-Abweichung",
                evidence=evidence,
            ))
        except Exception as exc:
            results.append(RuleResult(
                rule_id=rule.get("id", "UNKNOWN"),
                rule_version=rule.get("version", "0"),
                title=rule.get("title", "Unbekannte Regel"),
                category=rule.get("category", "unknown"),
                severity=rule.get("severity", "error"),
                status="error",
                expected_path=rule.get("expected_path", ""),
                actual_path=rule.get("actual_path", ""),
                message=f"Regel konnte nicht ausgewertet werden: {exc}",
            ))
    return results


def build_report(
    ifc_path: str | Path,
    baseline_path: str | Path,
    catalog: dict[str, Any],
    actual: dict[str, Any],
    results: list[RuleResult],
) -> dict[str, Any]:
    counts = {
        status: sum(result.status == status for result in results)
        for status in ("passed", "failed", "error")
    }
    return {
        "report_schema": "iqa.mvp1.regression-report/1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "ifc_path": str(Path(ifc_path).resolve()),
        "baseline_path": str(Path(baseline_path).resolve()),
        "rule_package": {
            "id": catalog["package_id"],
            "version": catalog["package_version"],
        },
        "summary": {"total": len(results), **counts, "passed_all": counts["failed"] == 0 and counts["error"] == 0},
        "model_identity": actual["model"],
        "results": [asdict(result) for result in results],
    }


def write_json_report(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_junit_report(results: list[RuleResult], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    failures = sum(r.status == "failed" for r in results)
    errors = sum(r.status == "error" for r in results)
    suite = Element("testsuite", {
        "name": "IFC Quantity Agent MVP-1 Regression",
        "tests": str(len(results)),
        "failures": str(failures),
        "errors": str(errors),
    })
    for result in results:
        case = SubElement(suite, "testcase", {
            "classname": result.category,
            "name": f"{result.rule_id} {result.title}",
        })
        if result.status == "failed":
            node = SubElement(case, "failure", {"message": result.message})
            node.text = json.dumps({"expected": result.expected, "actual": result.actual}, ensure_ascii=False)
        elif result.status == "error":
            node = SubElement(case, "error", {"message": result.message})
            node.text = result.message
    ElementTree(suite).write(target, encoding="utf-8", xml_declaration=True)

