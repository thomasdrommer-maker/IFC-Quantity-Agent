from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ifc_quantity_agent_mvp1.regression import evaluate_rules


class BaselineAndRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads((ROOT / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "rules" / "mvp1_rules_v0.1.json").read_text(encoding="utf-8"))

    def test_class_counts_equal_element_count(self):
        self.assertEqual(sum(self.baseline["ifc_class_counts"].values()), self.baseline["counts"]["ifc_elements"])

    def test_lv_counts_are_complete(self):
        lv = self.baseline["lv_ident"]
        self.assertEqual(sum(lv["values"].values()), lv["populated"])
        self.assertEqual(lv["populated"] + lv["missing_or_empty"], self.baseline["counts"]["ifc_elements"])

    def test_rule_ids_are_unique_and_stable_shape(self):
        ids = [rule["id"] for rule in self.catalog["rules"]]
        self.assertEqual(len(ids), len(set(ids)))
        for rule_id in ids:
            self.assertRegex(rule_id, r"^IQA-M1-[A-Z]+-[0-9]{3}$")

    def test_baseline_self_comparison_passes(self):
        results = evaluate_rules(self.baseline, self.baseline, self.catalog)
        self.assertTrue(all(result.status == "passed" for result in results))

    def test_changed_value_is_detected(self):
        changed = json.loads(json.dumps(self.baseline))
        changed["counts"]["ifc_elements"] = 201
        results = evaluate_rules(changed, self.baseline, self.catalog)
        result = next(item for item in results if item.rule_id == "IQA-M1-ELEM-002")
        self.assertEqual(result.status, "failed")


if __name__ == "__main__":
    unittest.main()

