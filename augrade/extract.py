"""Thin facade over tokenize_dxf that collects the extraction result.

This exists so dataset.py and callers do not need to know the exact ordering
of iter_entities -> direct + graph polygons -> dedupe.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import tokenize_dxf as td


SnapTolerance = Union[float, dict]


@dataclass
class ExtractionResult:
    input_path: Path
    snap_tolerance: SnapTolerance
    entities: List[td.Entity]
    polygons: List[td.PolygonRecord]
    graph_segments: List[td.Segment]
    runtime_seconds: float

    @property
    def scalar_snap_tolerance(self) -> float:
        """Single scalar for dashboards/filenames/merge-lab display."""
        return td.snap_tolerance_for_report(self.snap_tolerance)


def run_extraction(input_path: Path, snap_tolerance: SnapTolerance) -> ExtractionResult:
    start = time.time()
    entities = list(td.iter_entities(input_path))
    direct_polygons = td.extract_direct_polygons(entities)
    graph_segments = [
        segment for entity in entities for segment in td.entity_to_segments(entity)
    ]
    graph_polygons = td.extract_faces_from_segments(
        graph_segments, tolerance=snap_tolerance
    )
    polygons = td.dedupe_polygons(direct_polygons + graph_polygons)
    return ExtractionResult(
        input_path=input_path,
        snap_tolerance=snap_tolerance,
        entities=entities,
        polygons=polygons,
        graph_segments=graph_segments,
        runtime_seconds=time.time() - start,
    )
