from pathlib import Path
import sys
import unittest
import warnings

warnings.filterwarnings("ignore", message="Using `httpx` with `starlette.testclient` is deprecated.*")
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ifc_quantity_agent_mvp1.api import create_app
from ifc_quantity_agent_mvp1.service import AnalysisService


class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service = AnalysisService(
            ROOT / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json",
            ROOT / "rules" / "mvp1_rules_v0.1.json",
        )
        cls.client = TestClient(create_app(service))

    def test_health_and_openapi_contract(self):
        health = self.client.get("/api/v1/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["rule_package"]["rule_count"], 32)
        schema = self.client.get("/openapi.json")
        self.assertEqual(schema.status_code, 200)
        paths = schema.json()["paths"]
        self.assertIn("/api/v1/analyses", paths)
        self.assertIn("/api/v1/analyses/{analysis_id}/overview", paths)
        self.assertIn("/api/v1/analyses/{analysis_id}/rule-results", paths)
        self.assertIn("/api/v1/analyses/{analysis_id}/findings", paths)
        self.assertIn("/api/v1/analyses/{analysis_id}/objects/{global_id}", paths)

    def test_ui_shell_is_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("IFC Quantity Agent", response.text)
        asset = self.client.get("/assets/app.js")
        self.assertEqual(asset.status_code, 200)
        self.assertIn("iqa:select-objects", asset.text)

    def test_invalid_file_extension_is_rejected(self):
        response = self.client.post(
            "/api/v1/analyses",
            files={"file": ("not-ifc.txt", b"not an IFC", "text/plain")},
        )
        self.assertEqual(response.status_code, 415)

    def test_unknown_analysis_returns_404(self):
        response = self.client.get("/api/v1/analyses/does-not-exist/overview")
        self.assertEqual(response.status_code, 404)


class ApiReferenceModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reference = Path("/workspace/scratch/5ab184777645/upload/Z445_799_ECA_BM_801_3D.ifc")
        if not reference.exists():
            raise unittest.SkipTest("Z445-Referenzmodell ist nicht verfügbar")
        service = AnalysisService(
            ROOT / "baseline" / "IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json",
            ROOT / "rules" / "mvp1_rules_v0.1.json",
        )
        cls.client = TestClient(create_app(service))
        with reference.open("rb") as handle:
            response = cls.client.post(
                "/api/v1/analyses",
                files={"file": (reference.name, handle, "application/x-step")},
            )
        if response.status_code != 201:
            raise AssertionError(response.text)
        cls.created = response.json()
        cls.analysis_id = cls.created["analysis_id"]

    def test_analysis_created_contract(self):
        self.assertEqual(self.created["status"], "completed")
        self.assertEqual(self.created["summary"]["passed"], 32)
        self.assertTrue(self.created["summary"]["passed_all"])
        self.assertNotIn("ifc_path", self.created)

    def test_project_overview(self):
        response = self.client.get(f"/api/v1/analyses/{self.analysis_id}/overview")
        self.assertEqual(response.status_code, 200)
        overview = response.json()
        self.assertEqual(overview["counts"]["ifc_elements"], 202)
        self.assertEqual(overview["lv_ident"]["missing_or_empty"], 121)
        self.assertEqual(overview["model"]["model_type"]["value"], "ECA")
        self.assertNotIn("ifc_path", overview)

    def test_rule_result_filter(self):
        response = self.client.get(
            f"/api/v1/analyses/{self.analysis_id}/rule-results",
            params={"status": "passed"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 32)

    def test_findings_are_object_traceable(self):
        response = self.client.get(
            f"/api/v1/analyses/{self.analysis_id}/findings",
            params={"finding_type": "einzelfundament_without_gross_volume"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["total"], 3)
        self.assertTrue(all(item["global_id"] for item in payload["items"]))
        self.assertTrue(all(item["source_rule_id"] == "IQA-M1-QTY-006" for item in payload["items"]))

    def test_object_list_and_drilldown(self):
        response = self.client.get(
            f"/api/v1/analyses/{self.analysis_id}/objects",
            params={"missing_lv_ident": "true", "limit": 200},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["total"], 121)
        global_id = payload["items"][0]["global_id"]
        detail = self.client.get(f"/api/v1/analyses/{self.analysis_id}/objects/{global_id}")
        self.assertEqual(detail.status_code, 200)
        object_data = detail.json()["object"]
        self.assertEqual(object_data["global_id"], global_id)
        self.assertIn("property_sets", object_data)
        self.assertIn("quantities", object_data)
        self.assertIn("findings", object_data)


if __name__ == "__main__":
    unittest.main()

