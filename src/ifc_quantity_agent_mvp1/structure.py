"""IFC relationship inventory. Node identity uses STEP ids, not potentially duplicate GlobalIds."""
from collections import Counter


def collect_structure(model, elements, object_records):
    entities = {e.id(): e for e in elements}
    spatial_class = 'IfcSpatialStructureElement' if model.schema.startswith('IFC2X3') else 'IfcSpatialElement'
    for entity in model.by_type('IfcProject') + model.by_type(spatial_class):
        entities[entity.id()] = entity
    relations = []
    for relation_type in ('IfcRelAggregates', 'IfcRelNests', 'IfcRelContainedInSpatialStructure'):
        for relation in model.by_type(relation_type):
            parent = relation.RelatingStructure if relation_type == 'IfcRelContainedInSpatialStructure' else relation.RelatingObject
            children = relation.RelatedElements if relation_type == 'IfcRelContainedInSpatialStructure' else relation.RelatedObjects
            # Retain intermediate real IFC objects too (e.g. IfcGroup/other decompositions).
            entities[parent.id()] = parent
            for child in children:
                entities[child.id()] = child
                relations.append({'parent': str(parent.id()), 'child': str(child.id()),
                                  'relation_type': relation_type, 'relation_step_id': relation.id()})
    records = {o['step_id']: o for o in object_records}
    nodes = []
    for step_id, entity in sorted(entities.items()):
        record = records.get(step_id, {})
        nodes.append({'node_id': str(step_id), 'step_id': step_id,
                      'global_id': getattr(entity, 'GlobalId', None), 'ifc_class': entity.is_a(),
                      'name': getattr(entity, 'Name', None), 'is_element': entity.is_a('IfcElement'),
                      'is_assembly': entity.is_a('IfcElementAssembly'),
                      'is_spatial': entity.is_a(spatial_class) or entity.is_a('IfcProject'),
                      'lv_ident': record.get('lv_ident'), 'materials': record.get('materials', [])})
    incoming = {e['child'] for e in relations}
    roots = [n['node_id'] for n in nodes if n['node_id'] not in incoming]
    children = {}
    for edge in relations:
        children.setdefault(edge['parent'], []).append(edge['child'])
    seen = set()
    def visit(start):
        stack = [start]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(children.get(current, []))
    for root in roots:
        visit(root)
    # Components without a root (invalid cyclic relations) remain inspectable.
    cycle_roots = []
    for node in nodes:
        if node['node_id'] not in seen:
            cycle_roots.append(node['node_id'])
            visit(node['node_id'])
    ids = Counter(n['global_id'] for n in nodes if n['global_id'])
    contained = {e['child'] for e in relations if e['relation_type'] == 'IfcRelContainedInSpatialStructure'}
    return {'nodes': nodes, 'edges': relations, 'roots': roots, 'cycle_roots': cycle_roots,
            'uncontained_elements': [n['node_id'] for n in nodes if n['is_element'] and n['node_id'] not in contained],
            'summary': {'elements': len(elements), 'assemblies': sum(e.is_a('IfcElementAssembly') for e in elements),
                        'nodes': len(nodes), 'relations': len(relations),
                        'missing_global_ids': sum(not n['global_id'] for n in nodes),
                        'duplicate_global_ids': sum(c - 1 for c in ids.values() if c > 1)}}
