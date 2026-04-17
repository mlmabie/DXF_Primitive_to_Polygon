"""Unified compute layer: ``AnalysisDataset`` and its builder.

Both HTML views (dashboard, merge lab), the DXF emitter, and the REPL consume
this single dataset. The builder is composable: gallery and merge-candidate
construction are opt-in so cheap paths (e.g. ``emit dxf``) skip them.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import tokenize_dxf as td

from . import merge as merge_mod
from .extract import ExtractionResult, run_extraction
from .provenance import build_provenance_index


FAMILIES = ("walls", "columns", "curtain_walls")


@dataclass
class AnalysisDataset:
    """Single source of truth for downstream renderers and the REPL."""

    input_path: Path
    snap_tolerance: float
    runtime_seconds: float

    entities: List[td.Entity]
    polygons: List[td.PolygonRecord]
    polygons_by_family: Dict[str, List[td.PolygonRecord]]
    entity_by_id: Dict[str, td.Entity]
    graph_segments: list

    provenance: Dict[str, object]
    summary: Dict[str, object]

    descriptors_by_family: Optional[Dict[str, List[Dict[str, object]]]] = None
    family_payloads: Optional[Dict[str, Dict[str, object]]] = None
    gallery: Optional[List[Dict[str, object]]] = field(default=None)


def _group_polygons_by_family(polygons):
    grouped: Dict[str, List[td.PolygonRecord]] = defaultdict(list)
    for polygon in polygons:
        grouped[polygon.family].append(polygon)
    for family in FAMILIES:
        grouped.setdefault(family, [])
    return dict(grouped)


def build(
    input_dxf: Path,
    snap_tolerance: float,
    *,
    with_merge: bool = False,
    extraction: Optional[ExtractionResult] = None,
) -> AnalysisDataset:
    """Build an AnalysisDataset from a DXF path.

    Set ``with_merge=True`` to populate per-family merge candidate payloads
    (needed by the merge lab renderer and the REPL). Gallery construction is
    renderer-specific and lives in the dashboard renderer; we keep the dataset
    agnostic to that.

    Pass a pre-computed ``extraction`` to avoid re-parsing the DXF file.
    """
    start = time.time()
    if extraction is None:
        extraction = run_extraction(input_dxf, snap_tolerance)
    entities = extraction.entities
    polygons = extraction.polygons
    provenance = build_provenance_index(entities)
    summary = td.build_analysis_summary(
        entities=entities,
        polygons=polygons,
        runtime_seconds=time.time() - start,
        snap_stats=td.compute_snap_stats(
            entities, wall_tolerances=[0.1, 0.25, 0.5, 1.0]
        ),
    )
    runtime_seconds = time.time() - start

    entity_by_id = {entity.entity_id: entity for entity in entities if entity.family}
    grouped = _group_polygons_by_family(polygons)

    dataset = AnalysisDataset(
        input_path=input_dxf,
        snap_tolerance=snap_tolerance,
        runtime_seconds=runtime_seconds,
        entities=entities,
        polygons=polygons,
        polygons_by_family=grouped,
        entity_by_id=entity_by_id,
        graph_segments=extraction.graph_segments,
        provenance=provenance,
        summary=summary,
    )

    if with_merge:
        populate_merge_candidates(dataset)

    return dataset


def populate_merge_candidates(dataset: AnalysisDataset) -> None:
    """Fill in per-family descriptors + merge candidates in place."""
    family_payloads: Dict[str, Dict[str, object]] = {}
    descriptors_by_family: Dict[str, List[Dict[str, object]]] = {}
    for family in FAMILIES:
        payload = merge_mod.generate_family_data(
            family,
            dataset.polygons_by_family[family],
            dataset.entity_by_id,
            dataset.provenance,
        )
        family_payloads[family] = payload
        descriptors_by_family[family] = payload["polygons"]
    dataset.family_payloads = family_payloads
    dataset.descriptors_by_family = descriptors_by_family


def merge_lab_payload(dataset: AnalysisDataset) -> Dict[str, object]:
    """Return the JSON blob embedded in merge_lab.html."""
    if dataset.family_payloads is None:
        populate_merge_candidates(dataset)
    assert dataset.family_payloads is not None
    return {
        "meta": {
            "dataset_id": f"{dataset.input_path.name}|snap={dataset.snap_tolerance}",
            "input_file": dataset.input_path.name,
            "snap_tolerance": dataset.snap_tolerance,
            "generated_runtime_seconds": round(dataset.runtime_seconds, 3),
            "family_colors": td.FAMILY_COLORS,
            "provenance": {
                "family_summaries": dataset.provenance["family_summaries"],
                "variant_group_count": len(dataset.provenance["variant_groups"]),
                "multi_variant_group_count": sum(
                    1
                    for payload in dataset.provenance["variant_groups"]
                    if len(payload["raw_layers"]) > 1
                ),
            },
            "summary_counts": {
                family: {
                    "polygons": dataset.family_payloads[family]["stats"]["polygon_count"],
                    "candidates": dataset.family_payloads[family]["stats"]["candidate_count"],
                    "recommended": dataset.family_payloads[family]["stats"]["recommended_count"],
                }
                for family in FAMILIES
            },
        },
        "families": dataset.family_payloads,
    }
