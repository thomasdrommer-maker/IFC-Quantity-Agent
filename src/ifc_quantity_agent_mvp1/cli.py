from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .collector import collect
from .regression import build_report, evaluate_rules, read_json, write_json_report, write_junit_report


def _parser() -> argparse.ArgumentParser:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="IFC Quantity Agent MVP-1 Regression")
    parser.add_argument("--ifc", required=True, help="Pfad zur IFC-Referenzdatei")
    parser.add_argument("--baseline", default=str(root / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json"))
    parser.add_argument("--rules", default=str(root / "rules" / "mvp1_rules_v0.1.json"))
    parser.add_argument("--output-dir", default=str(root / "reports"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        baseline = read_json(args.baseline)
        catalog = read_json(args.rules)
        actual = collect(args.ifc)
    except Exception as exc:
        print(f"FEHLER: Eingaben oder IFC konnten nicht geladen werden: {exc}", file=sys.stderr)
        return 2

    results = evaluate_rules(actual, baseline, catalog)
    report = build_report(args.ifc, args.baseline, catalog, actual, results)
    output_dir = Path(args.output_dir)
    write_json_report(report, output_dir / "mvp1_regression_report.json")
    write_junit_report(results, output_dir / "mvp1_regression_junit.xml")

    summary = report["summary"]
    print(
        f"MVP-1 Regression: {summary['passed']}/{summary['total']} bestanden, "
        f"{summary['failed']} fehlgeschlagen, {summary['error']} Fehler"
    )
    for result in results:
        print(f"[{result.status.upper():6}] {result.rule_id} – {result.title}")
    return 0 if summary["passed_all"] else 1

