from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import ifcopenshell
from ifcopenshell.guid import new
from fastapi.testclient import TestClient
from ifc_quantity_agent_mvp1.api import create_app
from ifc_quantity_agent_mvp1.service import AnalysisService
from ifc_quantity_agent_mvp1.collector import collect


def fixture(schema='IFC4'):
    model = ifcopenshell.file(schema=schema)
    def entity(cls, name):
        return model.create_entity(cls, GlobalId=new(), Name=name)
    project = entity('IfcProject', 'Projekt')
    site = entity('IfcSite', 'Standort')
    building = entity('IfcBuilding', 'Bauwerk')
    storey = entity('IfcBuildingStorey', 'Ebene')
    assembly = entity('IfcElementAssembly', 'Baugruppe')
    beam = entity('IfcBeam', 'Unterzug')
    orphan = entity('IfcBeam', 'Ohne Zuordnung')
    duplicate = entity('IfcBeam', 'Gleiche GlobalId')
    duplicate.GlobalId = beam.GlobalId
    missing = entity('IfcBeam', 'GlobalId fehlt')
    missing.GlobalId = ''
    for parent, child in [(project, site), (site, building), (building, storey), (assembly, beam)]:
        model.create_entity('IfcRelAggregates', GlobalId=new(), RelatingObject=parent, RelatedObjects=[child])
    model.create_entity('IfcRelContainedInSpatialStructure', GlobalId=new(), RelatingStructure=storey, RelatedElements=[assembly, duplicate, missing])
    return model, beam, orphan, missing, assembly


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.model, self.beam, self.orphan, self.missing, self.assembly = fixture()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test_ECA_model.ifc'
        self.model.write(str(self.path))

    def test_inventory_and_native_relationships(self):
        actual = collect(self.path)
        tree = actual['model_structure']
        self.assertEqual(actual['counts']['ifc_elements'], 5)
        self.assertEqual(tree['summary']['elements'], 5)
        self.assertEqual(tree['summary']['assemblies'], 1)
        self.assertEqual(tree['summary']['duplicate_global_ids'], 1)
        self.assertEqual(tree['summary']['missing_global_ids'], 1)
        self.assertEqual(len(tree['nodes']), len({n['node_id'] for n in tree['nodes']}))
        self.assertIn(str(self.orphan.id()), tree['roots'])
        self.assertIn(str(self.beam.id()), tree['uncontained_elements'])
        edge = next(e for e in tree['edges'] if e['child'] == str(self.beam.id()))
        self.assertEqual(edge['parent'], str(self.assembly.id()))
        self.assertEqual(edge['relation_type'], 'IfcRelAggregates')
        self.assertTrue(edge['relation_step_id'])

    def test_cyclic_component_remains_visible(self):
        a = self.model.create_entity('IfcElementAssembly', GlobalId=new(), Name='A')
        b = self.model.create_entity('IfcElementAssembly', GlobalId=new(), Name='B')
        for parent, child in [(a,b),(b,a)]:
            self.model.create_entity('IfcRelAggregates', GlobalId=new(), RelatingObject=parent, RelatedObjects=[child])
        self.model.write(str(self.path))
        tree = collect(self.path)['model_structure']
        self.assertTrue(tree['cycle_roots'])
        self.assertIn(str(a.id()), {n['node_id'] for n in tree['nodes']})

    def test_upload_structure_and_step_drilldown(self):
        service = AnalysisService(ROOT/'baseline/IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json', ROOT/'rules/mvp1_rules_v0.1.json')
        client = TestClient(create_app(service))
        response = client.post('/api/v1/analyses', files={'file':('test_ECA_model.ifc',self.path.read_bytes(),'application/x-step')})
        self.assertEqual(response.status_code,201,response.text)
        base='/api/v1/analyses/'+response.json()['analysis_id']
        result=client.get(base+'/structure')
        self.assertEqual(result.status_code,200)
        self.assertEqual(result.json()['summary']['elements'],5)
        for entity in [self.beam,self.missing]:
            detail=client.get(base+'/objects/by-step/'+str(entity.id()))
            self.assertEqual(detail.status_code,200,detail.text)
            self.assertEqual(detail.json()['object']['step_id'],entity.id())
            self.assertTrue(detail.json()['object']['finding_identity_ambiguous'])
        self.assertEqual(client.get(base+'/objects/by-step/999999').status_code,404)
        self.assertEqual(client.get('/api/v1/analyses/unknown/structure').status_code,404)

    def test_ifc43_relationship_inventory(self):
        model, beam, orphan, missing, assembly = fixture('IFC4X3_ADD2')
        model.write(str(self.path))
        self.assertEqual(collect(self.path)['model_structure']['summary']['elements'], 5)

    def test_nests_and_multiple_parents_are_preserved(self):
        self.model.create_entity('IfcRelNests', GlobalId=new(), RelatingObject=self.assembly, RelatedObjects=[self.orphan])
        self.model.create_entity('IfcRelAggregates', GlobalId=new(), RelatingObject=self.orphan, RelatedObjects=[self.beam])
        self.model.write(str(self.path))
        edges=collect(self.path)['model_structure']['edges']
        self.assertTrue(any(e['relation_type']=='IfcRelNests' for e in edges))
        self.assertEqual(sum(e['child']==str(self.beam.id()) for e in edges),2)
