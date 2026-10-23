from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any

import ifcopenshell
from ifcopenshell.util.element import get_material, get_psets
from ifcopenshell.util.unit import get_project_unit


def _present(value: Any) -> bool:
    return value is not None and (not isinstance(value, str) or bool(value.strip()))


def _property(psets: dict[str, dict[str, Any]], pset: str, prop: str) -> Any:
    return psets.get(pset, {}).get(prop)


def _find_property(psets: dict[str, dict[str, Any]], prop: str) -> Any:
    for values in psets.values():
        if prop in values:
            return values[prop]
    return None


def _find_base_quantity(psets: dict[str, dict[str, Any]], prop: str) -> Any:
    """Return a native IFC base quantity, never a same-named custom PSet value."""
    for set_name, values in psets.items():
        if set_name.startswith("Qto_") and set_name.endswith("BaseQuantities") and prop in values:
            return values[prop]
    return None


def _find_base_quantity_with_source(
    psets: dict[str, dict[str, Any]], prop: str
) -> tuple[Any, str | None]:
    for set_name, values in psets.items():
        if set_name.startswith("Qto_") and set_name.endswith("BaseQuantities") and prop in values:
            return values[prop], f"{set_name}.{prop}"
    return None, None


def _float(value: Any) -> float | None:
    if not _present(value):
        return None
    if isinstance(value, str):
        value = value.replace(" ", "").replace(",", ".")
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _material_names(material: Any) -> list[str]:
    if material is None:
        return []
    if material.is_a("IfcMaterial"):
        return [material.Name] if _present(material.Name) else []
    names: list[str] = []
    for attr in ("Materials", "MaterialLayers", "MaterialProfiles", "MaterialConstituents"):
        for item in getattr(material, attr, None) or []:
            names.extend(_material_names(getattr(item, "Material", item)))
    return names


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if hasattr(value, "is_a") and hasattr(value, "id"):
        return {"ifc_class": value.is_a(), "step_id": value.id()}
    return str(value)


def _object_reference(element: Any) -> dict[str, Any]:
    return {
        "global_id": getattr(element, "GlobalId", None),
        "ifc_class": element.is_a(),
        "name": getattr(element, "Name", None),
    }


def _evidence(element: Any, **extra: Any) -> dict[str, Any]:
    row = {
        "global_id": getattr(element, "GlobalId", None),
        "ifc_class": element.is_a(),
        "name": getattr(element, "Name", None),
    }
    row.update(extra)
    return row


def _unit_name(model: Any, unit_type: str) -> str | None:
    unit = get_project_unit(model, unit_type)
    if unit is None:
        return None
    name = str(getattr(unit, "Name", "")).upper()
    prefix = str(getattr(unit, "Prefix", "") or "").upper()
    if unit_type == "LENGTHUNIT" and prefix == "MILLI" and name == "METRE":
        return "millimetre"
    return {
        "SQUARE_METRE": "square_metre",
        "CUBIC_METRE": "cubic_metre",
        "METRE": "metre",
    }.get(name, name.lower() or None)


def _header_metadata(model: Any) -> dict[str, Any]:
    header = model.header.file_name
    description = tuple(model.header.file_description.description or ())
    view_definition = None
    for item in description:
        if "ViewDefinition" in item:
            view_definition = item.split("[", 1)[-1].rstrip("]")
    exporter = str(header.preprocessor_version or "")
    exporter = exporter.replace("IFC-manager", "IFC Manager").replace(" (", " ").replace(")", "")
    authoring = str(header.originating_system or "")
    if authoring.startswith("SketchUp ") and " (" in authoring:
        authoring = authoring.split(" (", 1)[0]
    return {
        "schema": model.schema,
        "view_definition": view_definition,
        "authoring_application": authoring,
        "exporter": exporter,
        "export_timestamp": header.time_stamp,
    }


def collect(ifc_path: str | Path, model_file_name: str | None = None) -> dict[str, Any]:
    path = Path(ifc_path).resolve()
    logical_file_name = Path(model_file_name).name if model_file_name else path.name
    model = ifcopenshell.open(str(path))
    elements = list(model.by_type("IfcElement"))
    products = list(model.by_type("IfcProduct"))
    roots = list(model.by_type("IfcRoot"))
    psets_by_id = {e.id(): get_psets(e, psets_only=False) for e in elements}

    void_relations = list(model.by_type("IfcRelVoidsElement"))
    voided_opening_ids = {rel.RelatedOpeningElement.id() for rel in void_relations}
    assembly_relations = [
        rel for rel in model.by_type("IfcRelAggregates")
        if rel.RelatingObject.is_a("IfcElementAssembly")
    ]
    assembly_parents: dict[int, list[Any]] = defaultdict(list)
    assembly_children: dict[int, list[Any]] = defaultdict(list)
    for relation in assembly_relations:
        parent = relation.RelatingObject
        for child in relation.RelatedObjects:
            assembly_parents[child.id()].append(parent)
            assembly_children[parent.id()].append(child)

    global_ids = [r.GlobalId for r in roots if _present(getattr(r, "GlobalId", None))]
    duplicate_global_ids = sum(count - 1 for count in Counter(global_ids).values() if count > 1)
    containment_counts = [len(getattr(e, "ContainedInStructure", ()) or ()) for e in elements]

    class_counts = Counter(e.is_a() for e in elements)
    pset_coverage = Counter()
    for psets in psets_by_id.values():
        pset_coverage.update(psets.keys())

    lv_values = Counter()
    materials = Counter()
    bim_core_values = Counter()
    plan_status = Counter()
    field_present = Counter()
    evidence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    object_records: list[dict[str, Any]] = []

    gross_net_pairs: list[tuple[float, float]] = []
    gross_custom_matches = True
    lv_groups: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "objects": 0,
        "gross_701_objects": 0,
        "gross_701_sum_m3": 0.0,
        "net_volume_objects": 0,
        "net_volume_sum_m3": 0.0,
    })

    for element in elements:
        psets = psets_by_id[element.id()]
        basf = psets.get("BASF_General", {})
        bim_core = psets.get("BIM_Core", {})
        lv_ident = basf.get("540_LV_Ident")
        gross = _float(basf.get("701_Bruttovolumen"))
        custom_gross = _float(psets.get("QTO", {}).get("QTO.01_Bruttovolumen_m3"))
        raw_net, net_source = _find_base_quantity_with_source(psets, "NetVolume")
        net = _float(raw_net)

        if _present(lv_ident):
            lv_ident = str(lv_ident)
            lv_values[lv_ident] += 1
            group = lv_groups[lv_ident]
            group["objects"] += 1
            if gross is not None:
                group["gross_701_objects"] += 1
                group["gross_701_sum_m3"] += gross
            if net is not None:
                group["net_volume_objects"] += 1
                group["net_volume_sum_m3"] += net
        if gross is not None and net is not None:
            gross_net_pairs.append((gross, net))
        if gross is not None and custom_gross is not None and abs(gross - custom_gross) > 1e-9:
            gross_custom_matches = False

        material_names = _material_names(get_material(element, should_skip_usage=True))
        for name in material_names:
            materials[name] += 1
        if _present(bim_core.get("IfcClass")):
            bim_core_values[str(bim_core["IfcClass"])] += 1
        if _present(basf.get("504_Planungsstand")):
            plan_status[str(basf["504_Planungsstand"])] += 1

        field_map = {
            "BASF_General.701_Bruttovolumen": gross,
            "BASF_General.604_Bruttogewicht": basf.get("604_Bruttogewicht"),
            "BASF_General.550_Baunummer": basf.get("550_Baunummer"),
            "BIM_Core.IfcClass": bim_core.get("IfcClass"),
            "native.Name": getattr(element, "Name", None),
            "native.Description": getattr(element, "Description", None),
            "native.ObjectType": getattr(element, "ObjectType", None),
            "native.Tag": getattr(element, "Tag", None),
        }
        for key, value in field_map.items():
            if _present(value):
                field_present[key] += 1

        review_flags: list[str] = []
        if element.is_a("IfcBuildingElementProxy"):
            evidence["building_element_proxies"].append(_evidence(element))
            review_flags.append("building_element_proxy")
        if not getattr(element, "ContainedInStructure", ()):
            evidence["uncontained_elements"].append(_evidence(element))
            review_flags.append("without_spatial_containment")
        if element.is_a("IfcSlab") and getattr(element, "Name", None) == "Sockel_Stütze" and lv_ident == "Einzelfundament":
            evidence["slab_sockel_stuetze_with_lv_einzelfundament"].append(_evidence(element, lv_ident=lv_ident))
            review_flags.append("slab_sockel_stuetze_with_lv_einzelfundament")
        if lv_ident == "Einzelfundament" and gross is None:
            evidence["einzelfundament_without_gross_volume"].append(_evidence(element, lv_ident=lv_ident))
            review_flags.append("einzelfundament_without_gross_volume")
        if not _present(basf.get("550_Baunummer")):
            evidence["elements_without_baunummer"].append(_evidence(element))
            review_flags.append("without_baunummer")
        if not _present(basf.get("604_Bruttogewicht")):
            evidence["elements_without_bruttogewicht"].append(_evidence(element))
            review_flags.append("without_bruttogewicht")
        if element.is_a("IfcOpeningElement") and element.id() not in voided_opening_ids:
            review_flags.append("opening_without_void_relation")

        containment = [
            _object_reference(relation.RelatingStructure)
            for relation in (getattr(element, "ContainedInStructure", ()) or ())
        ]
        object_records.append({
            "global_id": getattr(element, "GlobalId", None),
            "step_id": element.id(),
            "ifc_class": element.is_a(),
            "name": getattr(element, "Name", None),
            "description": getattr(element, "Description", None),
            "object_type": getattr(element, "ObjectType", None),
            "tag": getattr(element, "Tag", None),
            "predefined_type": getattr(element, "PredefinedType", None),
            "has_representation": bool(getattr(element, "Representation", None)),
            "spatial_containment": containment,
            "assembly_parents": [_object_reference(item) for item in assembly_parents[element.id()]],
            "assembly_children": [_object_reference(item) for item in assembly_children[element.id()]],
            "materials": material_names,
            "lv_ident": str(lv_ident) if _present(lv_ident) else None,
            "quantities": {
                "gross_volume_701": {
                    "value": gross,
                    "unit": "m3" if gross is not None else None,
                    "source": "BASF_General.701_Bruttovolumen" if gross is not None else None,
                },
                "custom_gross_volume": {
                    "value": custom_gross,
                    "unit": "m3" if custom_gross is not None else None,
                    "source": "QTO.QTO.01_Bruttovolumen_m3" if custom_gross is not None else None,
                },
                "net_volume": {
                    "value": net,
                    "unit": "m3" if net is not None else None,
                    "source": net_source,
                },
            },
            "property_sets": _json_safe(psets),
            "review_flags": review_flags,
        })

    openings = list(model.by_type("IfcOpeningElement"))
    for opening in openings:
        if opening.id() not in voided_opening_ids:
            evidence["opening_elements_without_void_relation"].append(_evidence(opening))

    assemblies = list(model.by_type("IfcElementAssembly"))

    spatial = {}
    for ifc_class in ("IfcSite", "IfcBuilding", "IfcBuildingStorey", "IfcSpace"):
        objects = list(model.by_type(ifc_class))
        spatial[ifc_class] = {
            "count": len(objects),
            "names": [o.Name for o in objects if _present(getattr(o, "Name", None))],
        }

    key_field_coverage: dict[str, Any] = {}
    for key in (
        "BASF_General.701_Bruttovolumen",
        "BASF_General.604_Bruttogewicht",
        "BASF_General.550_Baunummer",
        "BIM_Core.IfcClass",
        "native.Name",
        "native.Description",
        "native.ObjectType",
        "native.Tag",
    ):
        present = field_present[key]
        key_field_coverage[key] = {"present": present, "missing_or_empty": len(elements) - present}
    key_field_coverage["BASF_General.504_Planungsstand"] = {
        "values": dict(plan_status),
        "missing_or_empty": len(elements) - sum(plan_status.values()),
    }

    quantity_groups = {}
    for key, value in lv_groups.items():
        quantity_groups[key] = {
            "objects": value["objects"],
            "gross_701_objects": value["gross_701_objects"],
            "gross_701_sum_m3": value["gross_701_sum_m3"],
            "net_volume_objects": value["net_volume_objects"],
            "net_volume_sum_m3": value["net_volume_sum_m3"],
        }

    header = _header_metadata(model)
    file_name_upper = logical_file_name.upper()
    model_type = "ECA" if "_ECA_" in file_name_upper else None
    actual = {
        "model": {
            "file_name": logical_file_name,
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "size_bytes": path.stat().st_size,
            **header,
            "model_type": {
                "value": model_type,
                "source": "file_name" if model_type else None,
                "confidence": "medium" if model_type else "none",
                "property_corroboration": False,
            },
        },
        "units": {
            "length": _unit_name(model, "LENGTHUNIT"),
            "area": _unit_name(model, "AREAUNIT"),
            "volume": _unit_name(model, "VOLUMEUNIT"),
        },
        "counts": {
            "step_entities": len(list(model)),
            "ifc_products": len(products),
            "ifc_elements": len(elements),
            "elements_with_representation": sum(bool(getattr(e, "Representation", None)) for e in elements),
            "elements_without_representation": sum(not bool(getattr(e, "Representation", None)) for e in elements),
            "ifc_roots_with_global_id": len(global_ids),
            "duplicate_global_ids": duplicate_global_ids,
            "elements_with_one_spatial_containment": sum(count == 1 for count in containment_counts),
            "elements_without_spatial_containment": sum(count == 0 for count in containment_counts),
        },
        "spatial": spatial,
        "ifc_class_counts": dict(class_counts),
        "property_set_coverage": dict(pset_coverage),
        "lv_ident": {
            "property": "BASF_General.540_LV_Ident",
            "populated": sum(lv_values.values()),
            "missing_or_empty": len(elements) - sum(lv_values.values()),
            "values": dict(lv_values),
        },
        "key_field_coverage": key_field_coverage,
        "bim_core_ifc_class_values": dict(bim_core_values),
        "material_assignments": dict(materials),
        "assemblies": {
            "count": len(assemblies),
            "with_representation": sum(bool(getattr(a, "Representation", None)) for a in assemblies),
            "parent_relationships": len(assembly_relations),
            "referenced_children": sum(len(rel.RelatedObjects) for rel in assembly_relations),
        },
        "openings": {
            "IfcOpeningElement": len(openings),
            "IfcRelVoidsElement": len(void_relations),
            "names": dict(Counter(o.Name for o in openings if _present(getattr(o, "Name", None)))),
        },
        "quantities": {
            "objects_with_gross_701_and_net_volume": len(gross_net_pairs),
            "gross_701_sum_m3": sum(pair[0] for pair in gross_net_pairs),
            "net_volume_sum_m3": sum(pair[1] for pair in gross_net_pairs),
            "gross_minus_net_m3": sum(pair[0] - pair[1] for pair in gross_net_pairs),
            "gross_701_matches_custom_qto_where_both_present": gross_custom_matches,
            "lv_groups": quantity_groups,
        },
        "expected_review_findings": {key: len(rows) for key, rows in evidence.items()},
        "finding_evidence": dict(evidence),
        "objects": object_records,
    }
    return actual

