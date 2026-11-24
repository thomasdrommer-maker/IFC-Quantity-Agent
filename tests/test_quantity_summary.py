from pathlib import Path
import json
import os
import sys
import unittest
import warnings

warnings.filterwarnings("ignore", message="Using `httpx` with `starlette.testclient` is deprecated.*")
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ifc_quantity_agent_mvp1.api import create_app
from ifc_quantity_agent_mvp1.service import AnalysisService

BASELINE_V02 = ROOT / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.2.json"
BASELINE_V03 = ROOT / "baseline" / "IFC_Quantity_Agent_MVP1_Mengenuebersicht_Sollwerte_Z445_ECA_v0.3.json"
RULES = ROOT / "rules" / "mvp1_rules_v0.2.json"


def row(step, ifc_class, lv, gross, net, material="Stahlbeton"):
    def q(value):
        return {"value": value, "unit": "m3" if value is not None else None, "source": None}
    return {
        "step_id": step, "global_id": f"G{step}", "ifc_class": ifc_class, "lv_ident": lv,
        "materials": [material] if material else [], "finding_count": 0,
        "quantities": {"gross_volume_701": q(gross), "custom_gross_volume": q(gross), "net_volume": q(net)},
    }


class QuantitySummarySyntheticTests(unittest.TestCase):
    def setUp(self):
        self.service = AnalysisService(BASELINE_V02, RULES)
        rows = [
            row(1, "IfcWall", "Stb_Wand", 10.0, 9.5),
            row(2, "IfcWall", "Stb_Wand", 5.0, None),
            row(3, "IfcFooting", "Stb_Fundament", 2.0, None),
            row(4, "IfcSlab", "", 1.0, 1.0, material=None),
            row(5, "IfcSlab", None, None, None),
        ]
        self.service._analyses["a"] = {"objects_by_step": {r["step_id"]: r for r in rows}}

    def test_missing_net_is_counted_not_replaced(self):
        result = self.service.quantity_summary("a", group_by="lv_ident")
        wall = next(g for g in result["groups"] if g["key"] == "Stb_Wand")
        self.assertEqual(wall["net_volume"]["sum"], 9.5)
        self.assertEqual(wall["net_volume"]["objects_missing"], 1)
        self.assertEqual(wall["gross_701"]["sum"], 15.0)
        footing = next(g for g in result["groups"] if g["key"] == "Stb_Fundament")
        self.assertIsNone(footing["net_volume"]["sum"])

    def test_unassigned_row_and_reconciliation(self):
        result = self.service.quantity_summary("a", group_by="lv_ident")
        unassigned = [g for g in result["groups"] if g["unassigned"]]
        self.assertEqual(len(unassigned), 1)
        self.assertEqual(unassigned[0]["object_count"], 2)
        self.assertTrue(all(result["reconciliation"].values()))
        self.assertEqual(result["totals"]["object_count"], 5)
        self.assertEqual(result["totals"]["gross_701"]["objects_missing"], 1)

    def test_class_grouping_same_totals(self):
        by_lv = self.service.quantity_summary("a", group_by="lv_ident")["totals"]
        by_class = self.service.quantity_summary("a", group_by="ifc_class")["totals"]
        for source in ("gross_701", "custom_qto", "net_volume"):
            self.assertEqual(by_lv[source], by_class[source])

    def test_material_filter_and_invalid_group(self):
        result = self.service.quantity_summary("a", group_by="ifc_class", material="Stahlbeton")
        self.assertEqual(result["totals"]["object_count"], 4)
        with self.assertRaises(ValueError):
            self.service.quantity_summary("a", group_by="material")


class QuantitySummaryReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env_path = os.environ.get("IFC_MVP1_REFERENCE_MODEL")
        if not env_path or not Path(env_path).exists():
            raise unittest.SkipTest("IFC_MVP1_REFERENCE_MODEL ist nicht gesetzt oder nicht verfügbar")
        cls.client = TestClient(create_app(AnalysisService(BASELINE_V02, RULES)))
        with Path(env_path).open("rb") as handle:
            created = cls.client.post("/api/v1/analyses", files={"file": ("ref.ifc", handle, "application/x-step")}).json()
        cls.analysis_id = created["analysis_id"]
        cls.expected = json.loads(BASELINE_V03.read_text(encoding="utf-8"))

    def _get(self, group_by):
        response = self.client.get(f"/api/v1/analyses/{self.analysis_id}/quantity-summary", params={"group_by": group_by})
        self.assertEqual(response.status_code, 200)
        return response.json()

    def _compare(self, result, expected_groups):
        by_label = {g["label"] if not g["unassigned"] else "(ohne LV-Ident)": g for g in result["groups"]}
        self.assertEqual(set(by_label), set(expected_groups))
        for key, exp in expected_groups.items():
            group = by_label[key]
            self.assertEqual(group["object_count"], exp["objects"], key)
            self.assertAlmostEqual(group["gross_701"]["sum"], exp["gross_701_m3"], places=9, msg=key)
            self.assertAlmostEqual(group["custom_qto"]["sum"], exp["custom_qto_m3"], places=9, msg=key)
            self.assertEqual(group["net_volume"]["objects_with_value"], exp["net_volume_objects"], key)
            if exp["net_volume_m3"] is None:
                self.assertIsNone(group["net_volume"]["sum"], key)
            else:
                self.assertAlmostEqual(group["net_volume"]["sum"], exp["net_volume_m3"], places=9, msg=key)

    def test_by_lv_ident_matches_baseline_v03(self):
        result = self._get("lv_ident")
        self._compare(result, self.expected["by_lv_ident"])
        self.assertTrue(all(result["reconciliation"].values()))

    def test_by_ifc_class_matches_baseline_v03(self):
        self._compare(self._get("ifc_class"), self.expected["by_ifc_class"])

    def test_totals_and_drilldown(self):
        totals = self._get("lv_ident")["totals"]
        exp = self.expected["totals"]
        self.assertAlmostEqual(totals["gross_701"]["sum"], exp["gross_701_m3"], places=9)
        self.assertAlmostEqual(totals["net_volume"]["sum"], exp["net_volume_m3"], places=9)
        self.assertEqual(totals["net_volume"]["objects_missing"], exp["net_volume_missing_objects"])
        base = f"/api/v1/analyses/{self.analysis_id}/objects"
        self.assertEqual(self.client.get(base, params={"missing_net_volume": True}).json()["total"], 9)
        self.assertEqual(self.client.get(base, params={"missing_lv_ident": True}).json()["total"], 2)
        footing = self.client.get(base, params={"ifc_class": "IfcFooting"}).json()["items"]
        self.assertTrue(all(item["net_volume"] is None and item["gross_701"] is not None for item in footing))


if __name__ == "__main__":
    unittest.main()
