from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Sequence, Tuple

import tokenize_dxf as td


BBox = Tuple[float, float, float, float]


def healed_layer_name(layer: str) -> str:
    chars = []
    for ch in layer:
        chars.append("-" if ord(ch) > 127 else ch)
    return "".join(chars)


def canonical_layer_name(layer: str) -> str:
    healed = healed_layer_name(layer)
    return re.sub(r"[-\s]+", " ", healed.upper()).strip()


def bbox_union(a: Optional[BBox], b: Optional[BBox]) -> Optional[BBox]:
    if a is None:
        return b
    if b is None:
        return a
    return (
        min(a[0], b[0]),
        min(a[1], b[1]),
        max(a[2], b[2]),
        max(a[3], b[3]),
    )


def bbox_overlap_pct(a: Optional[BBox], b: Optional[BBox]) -> float:
    if a is None or b is None:
        return 0.0
    ix_min = max(a[0], b[0])
    iy_min = max(a[1], b[1])
    ix_max = min(a[2], b[2])
    iy_max = min(a[3], b[3])
    if ix_max <= ix_min or iy_max <= iy_min:
        return 0.0
    intersection = (ix_max - ix_min) * (iy_max - iy_min)
    area_a = max((a[2] - a[0]) * (a[3] - a[1]), 1e-9)
    area_b = max((b[2] - b[0]) * (b[3] - b[1]), 1e-9)
    return intersection / min(area_a, area_b)


def bbox_to_list(bbox: Optional[BBox]) -> Optional[List[float]]:
    if bbox is None:
        return None
    return [round(value, 4) for value in bbox]


def sort_counter(counter: Counter) -> Dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def classify_variant_relationship(a: Dict[str, object], b: Dict[str, object]) -> Tuple[str, str]:
    overlap = bbox_overlap_pct(a["bbox"], b["bbox"])
    types_a = set(a.get("entity_types", a.get("entity_types_counter", {})))
    types_b = set(b.get("entity_types", b.get("entity_types_counter", {})))
    shared = sorted(types_a & types_b)
    if overlap < 0.1 and not shared:
        return (
            "disjoint_zones",
            f"Disjoint spatial zones ({overlap:.0%} overlap) with different entity-type profiles.",
        )
    if overlap > 0.3 and not shared:
        return (
            "complementary",
            f"Same broad region ({overlap:.0%} overlap) but complementary entity types.",
        )
    if overlap > 0.5 and shared:
        return (
            "overlapping",
            f"Significant overlap ({overlap:.0%}) with shared types {shared}.",
        )
    return (
        "related",
        f"Canonical variants with {overlap:.0%} overlap and shared types {shared}.",
    )


def build_provenance_index(entities: Sequence[td.Entity]) -> Dict[str, object]:
    target_entities = [entity for entity in entities if entity.family]

    entity_details: Dict[str, Dict[str, object]] = {}
    layer_summaries: Dict[str, Dict[str, object]] = {}
    groups: Dict[Tuple[str, str], List[str]] = defaultdict(list)

    for entity in target_entities:
        bbox = td.entity_extent(entity)
        healed = healed_layer_name(entity.layer)
        canonical = canonical_layer_name(entity.layer)

        entity_details[entity.entity_id] = {
            "entity_id": entity.entity_id,
            "raw_layer": entity.layer,
            "healed_layer": healed,
            "canonical_layer": canonical,
            "family": entity.family,
            "entity_type": entity.type,
            "bbox": bbox_to_list(bbox),
        }

        summary = layer_summaries.setdefault(
            entity.layer,
            {
                "raw_layer": entity.layer,
                "healed_layer": healed,
                "canonical_layer": canonical,
                "family": entity.family,
                "entity_count": 0,
                "entity_types_counter": Counter(),
                "bbox": None,
                "entity_ids": [],
                "group_id": None,
                "group_kind": "single",
            },
        )
        summary["entity_count"] += 1
        summary["entity_types_counter"][entity.type] += 1
        summary["bbox"] = bbox_union(summary["bbox"], bbox)
        if len(summary["entity_ids"]) < 8:
            summary["entity_ids"].append(entity.entity_id)

    for raw_layer, summary in layer_summaries.items():
        groups[(summary["family"], summary["canonical_layer"])].append(raw_layer)

    variant_groups: List[Dict[str, object]] = []
    variant_groups_by_id: Dict[str, Dict[str, object]] = {}

    for family, canonical in sorted(groups):
        raw_layers = sorted(groups[(family, canonical)])
        group_id = f"{family}:{canonical.lower().replace(' ', '_')}"
        relationships = []
        overall_bbox = None
        group_type_counter = Counter()
        for raw_layer in raw_layers:
            summary = layer_summaries[raw_layer]
            summary["group_id"] = group_id
            overall_bbox = bbox_union(overall_bbox, summary["bbox"])
            group_type_counter.update(summary["entity_types_counter"])

        if len(raw_layers) == 1:
            group_kind = "single"
            note = "Single raw layer for this canonical name."
        else:
            relationship_labels = []
            for idx in range(len(raw_layers)):
                for jdx in range(idx + 1, len(raw_layers)):
                    a = layer_summaries[raw_layers[idx]]
                    b = layer_summaries[raw_layers[jdx]]
                    relationship, evidence = classify_variant_relationship(a, b)
                    relationships.append(
                        {
                            "layers": [raw_layers[idx], raw_layers[jdx]],
                            "relationship": relationship,
                            "overlap_pct": round(bbox_overlap_pct(a["bbox"], b["bbox"]), 4),
                            "shared_entity_types": sorted(set(a["entity_types_counter"]) & set(b["entity_types_counter"])),
                            "evidence": evidence,
                        }
                    )
                    relationship_labels.append(relationship)
            if "complementary" in relationship_labels:
                group_kind = "complementary"
            elif "disjoint_zones" in relationship_labels:
                group_kind = "disjoint_zones"
            elif "overlapping" in relationship_labels:
                group_kind = "overlapping"
            else:
                group_kind = "related"
            note = "; ".join(rel["evidence"] for rel in relationships[:3])

        for raw_layer in raw_layers:
            layer_summaries[raw_layer]["group_kind"] = group_kind

        record = {
            "group_id": group_id,
            "family": family,
            "canonical_layer": canonical,
            "raw_layers": raw_layers,
            "group_kind": group_kind,
            "entity_count": sum(layer_summaries[layer]["entity_count"] for layer in raw_layers),
            "entity_types": sort_counter(group_type_counter),
            "bbox": bbox_to_list(overall_bbox),
            "note": note,
            "relationships": relationships,
        }
        variant_groups.append(record)
        variant_groups_by_id[group_id] = record

    family_summaries: Dict[str, Dict[str, int]] = {}
    for family in td.FAMILY_LAYER_MAP:
        family_layers = [summary for summary in layer_summaries.values() if summary["family"] == family]
        family_groups = [group for group in variant_groups if group["family"] == family]
        family_summaries[family] = {
            "raw_layer_count": len(family_layers),
            "variant_group_count": len(family_groups),
            "multi_variant_group_count": sum(1 for group in family_groups if len(group["raw_layers"]) > 1),
            "target_entity_count": sum(summary["entity_count"] for summary in family_layers),
        }

    serializable_layers = {}
    for raw_layer, summary in layer_summaries.items():
        serializable_layers[raw_layer] = {
            "raw_layer": summary["raw_layer"],
            "healed_layer": summary["healed_layer"],
            "canonical_layer": summary["canonical_layer"],
            "family": summary["family"],
            "entity_count": summary["entity_count"],
            "entity_types": sort_counter(summary["entity_types_counter"]),
            "bbox": bbox_to_list(summary["bbox"]),
            "group_id": summary["group_id"],
            "group_kind": summary["group_kind"],
            "entity_ids": list(summary["entity_ids"]),
        }

    return {
        "entity_details": entity_details,
        "layer_summaries": serializable_layers,
        "variant_groups": variant_groups,
        "variant_groups_by_id": variant_groups_by_id,
        "family_summaries": family_summaries,
    }
