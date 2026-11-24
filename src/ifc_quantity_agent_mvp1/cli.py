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
    parser.add_argument("--baseline", default=str(root / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.2.json"),
                        help="Standard: Referenz v0.2; für das ursprüngliche Modell die v0.1-Baseline angeben")
    parser.add_argument("--rules", default=str(root / "rules" / "mvp1_rules_v0.2.json"),
                        help="Standard: Regelpaket v0.2; für das ursprüngliche Modell mvp1_rules_v0.1.json angeben")
    parser.add_argument("--output-dir", default=str(root / "reports"))
    parser.add_argument("--quantity-summary", choices=["lv_ident", "ifc_class"],
                        help="Mengenübersicht (m³) nach LV-Ident oder IFC-Klasse ausgeben, aus demselben Service wie die API")
    return parser


def _fmt(entry: dict) -> str:
    total = entry["objects_with_value"] + entry["objects_missing"]
    if entry["sum"] is None:
        return f"fehlt (0 von {total})"
    suffix = f" ({entry['objects_with_value']} von {total})" if entry["objects_missing"] else ""
    return f"{entry['sum']:.2f}{suffix}"


def _print_quantity_summary(args) -> int:
    from .service import AnalysisService

    try:
        service = AnalysisService(args.baseline, args.rules)
        analysis_id = service.run_analysis(args.ifc)["analysis_id"]
        summary = service.quantity_summary(analysis_id, group_by=args.quantity_summary)
    except Exception as exc:
        print(f"FEHLER: Mengenübersicht nicht möglich: {exc}", file=sys.stderr)
        return 2
    print(f"Mengenübersicht nach {args.quantity_summary} ({summary['unit']}); Brutto 701 | QTO-Brutto | Netto")
    for group in summary["groups"] + [{**summary["totals"], "label": "Gesamt"}]:
        print(f"{group['label']:32} {group['object_count']:4} Obj.  {_fmt(group['gross_701'])} | {_fmt(group['custom_qto'])} | {_fmt(group['net_volume'])}")
    for warning in summary["warnings"]:
        print(f"HINWEIS: {warning['message']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.quantity_summary:
        return _print_quantity_summary(args)
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

