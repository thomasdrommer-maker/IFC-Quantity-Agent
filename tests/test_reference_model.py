from pathlib import Path
import json
import os
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ifc_quantity_agent_mvp1.collector import collect
from ifc_quantity_agent_mvp1.regression import evaluate_rules


class ReferenceModelRegressionTest(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("IFC_MVP1_REFERENCE_MODEL"), "IFC_MVP1_REFERENCE_MODEL ist nicht gesetzt")
    def test_z445_reference_model(self):
        model = Path(os.environ["IFC_MVP1_REFERENCE_MODEL"])
        baseline = json.loads((ROOT / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "rules" / "mvp1_rules_v0.1.json").read_text(encoding="utf-8"))
        results = evaluate_rules(collect(model), baseline, catalog)
        failures = [f"{r.rule_id}: {r.message} expected={r.expected!r} actual={r.actual!r}" for r in results if r.status != "passed"]
        self.assertFalse(failures, "\n".join(failures))


if __name__ == "__main__":
    unittest.main()

