#!/usr/bin/env python3
"""
Emit a cleaned DXF file from extraction results.

Reads the original DXF and the tokenization JSON output, then writes a new DXF with:

  1. Original primitives preserved on their raw layers (dimmed via color override)
  2. Extracted polygons as closed LWPOLYLINEs on new EXTRACTED-{FAMILY} layers
  3. Polygon IDs as MTEXT labels at polygon centroids on ID-{FAMILY} layers
  4. Healed layer names applied (unicode normalization, etc.)
  5. Non-target layers frozen (visible but locked)

The output DXF is a reviewable artifact: open in any CAD viewer to visually
verify extraction quality, inspect polygon IDs, and compare against raw geometry.

Usage:
    python emit_dxf.py <original.dxf> <tokenization_output.json> [--output cleaned.dxf]
                       [--normalization normalization.json] [--no-labels] [--no-raw]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

try:
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
except ImportError:
    print("ezdxf required: uv pip install ezdxf", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Family styling
# ---------------------------------------------------------------------------

# DXF ACI color indices
FAMILY_COLORS: Dict[str, int] = {
    "walls":         5,    # blue
    "columns":       1,    # red
    "curtain_walls": 3,    # green
}

# Dimmed color for original primitives on target layers
RAW_TARGET_COLOR = 8       # dark gray
RAW_NONTARGET_COLOR = 253  # light gray

from tokenize_dxf import FAMILY_LAYER_MAP as FAMILY_LAYERS

ALL_TARGET_LAYERS = {l for layers in FAMILY_LAYERS.values() for l in layers}


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def polygon_centroid(vertices: List[Dict[str, float]]) -> Tuple[float, float]:
    """Compute centroid of a polygon from its vertex list.

    Note: operates on List[Dict] with x_coord/y_coord keys (the JSON output
    format) rather than Sequence[Point] tuples used by geometry.polygon_centroid.
    The format difference is intentional — this module works directly with the
    serialized extraction JSON, not the internal PolygonRecord representation.
    """
    n = len(vertices)
    if n == 0:
        return (0.0, 0.0)
    cx = sum(v["x_coord"] for v in vertices) / n
    cy = sum(v["y_coord"] for v in vertices) / n
    return (cx, cy)


def polygon_area_from_verts(vertices: List[Dict[str, float]]) -> float:
    """Shoelace formula for area."""
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i]["x_coord"] * vertices[j]["y_coord"]
        area -= vertices[j]["x_coord"] * vertices[i]["y_coord"]
    return abs(area) / 2.0


def label_height_for_polygon(vertices: List[Dict[str, float]]) -> float:
    """Pick a readable text height proportional to polygon size."""
    if not vertices:
        return 5.0
    xs = [v["x_coord"] for v in vertices]
    ys = [v["y_coord"] for v in vertices]
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    # Text height ~5% of polygon span, clamped
    return max(1.0, min(span * 0.05, 20.0))


# ---------------------------------------------------------------------------
# Core: write cleaned DXF
# ---------------------------------------------------------------------------

def write_cleaned_dxf(
    original_path: Path,
    extraction_json: dict,
    output_path: Path,
    normalization: Optional[dict] = None,
    include_labels: bool = True,
    include_raw: bool = True,
) -> dict:
    """
    Write a cleaned DXF file with extraction overlay.

    Returns a summary dict with counts and layer info.
    """
    doc = ezdxf.readfile(str(original_path))
    msp = doc.modelspace()

    # --- Apply layer healing from normalization ---
    layer_map: Dict[str, str] = {}
    if normalization and "layer_map" in normalization:
        layer_map = normalization["layer_map"]
        # Rename healed layers in the DXF layer table
        for raw_name, healed_name in layer_map.items():
            if raw_name != healed_name and raw_name in doc.layers:
                try:
                    layer_obj = doc.layers.get(raw_name)
                    # ezdxf doesn't support direct rename, so reassign entities
                    for entity in msp:
                        if entity.dxf.layer == raw_name:
                            entity.dxf.layer = healed_name
                    # Create healed layer if it doesn't exist, copy properties
                    if healed_name not in doc.layers:
                        doc.layers.new(healed_name, dxfattribs={
                            "color": layer_obj.color,
                        })
                except Exception:
                    pass  # best-effort healing

    # --- Set up extraction overlay layers ---
    for family, color in FAMILY_COLORS.items():
        layer_name = f"EXTRACTED-{family.upper()}"
        if layer_name not in doc.layers:
            doc.layers.new(layer_name, dxfattribs={"color": color})

        if include_labels:
            label_layer = f"ID-{family.upper()}"
            if label_layer not in doc.layers:
                doc.layers.new(label_layer, dxfattribs={"color": color})

    # --- Dim original primitives and freeze non-target layers ---
    frozen_layers: set = set()
    if include_raw:
        for entity in msp:
            layer = entity.dxf.layer
            if layer in ALL_TARGET_LAYERS:
                entity.dxf.color = RAW_TARGET_COLOR
            else:
                entity.dxf.color = RAW_NONTARGET_COLOR
                frozen_layers.add(layer)

        # Lock non-target layers (visible but not editable)
        for layer_name in frozen_layers:
            try:
                layer_obj = doc.layers.get(layer_name)
                if layer_obj is not None:
                    layer_obj.lock()
            except Exception:
                pass
    else:
        # Remove all existing entities, keep only extracted
        for entity in list(msp):
            msp.delete_entity(entity)

    # --- Write extracted polygons ---
    summary = {"walls": 0, "columns": 0, "curtain_walls": 0, "labels": 0}

    for family_key in ["walls", "columns", "curtain_walls"]:
        layer_name = f"EXTRACTED-{family_key.upper()}"
        label_layer = f"ID-{family_key.upper()}"
        color = FAMILY_COLORS[family_key]

        polygons = extraction_json.get(family_key, [])
        for poly in polygons:
            vertices = poly.get("vertices", [])
            if len(vertices) < 3:
                continue

            poly_id = poly.get("id", "")
            source_layers = poly.get("source_layers", [])

            # Write closed LWPOLYLINE
            points = [(v["x_coord"], v["y_coord"]) for v in vertices]
            lwpoly = msp.add_lwpolyline(
                points,
                dxfattribs={
                    "layer": layer_name,
                    "color": color,
                },
                close=True,
            )

            # Attach extended data: polygon ID and source layers
            # Using XDATA for CAD-readable metadata
            appid = "AUGRADE_EXTRACT"
            if appid not in doc.appids:
                doc.appids.new(appid)
            lwpoly.set_xdata(appid, [
                (1000, poly_id),
                (1000, "|".join(source_layers)),
            ])

            summary[family_key] += 1

            # Write label at centroid
            if include_labels and poly_id:
                cx, cy = polygon_centroid(vertices)
                height = label_height_for_polygon(vertices)
                msp.add_mtext(
                    poly_id,
                    dxfattribs={
                        "layer": label_layer,
                        "color": color,
                        "char_height": height,
                        "insert": (cx, cy),
                    },
                )
                summary["labels"] += 1

    # --- Save ---
    doc.saveas(str(output_path))

    summary["output_path"] = str(output_path)
    summary["layers_added"] = [
        f"EXTRACTED-{f.upper()}" for f in FAMILY_COLORS
    ] + ([f"ID-{f.upper()}" for f in FAMILY_COLORS] if include_labels else [])

    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Emit a cleaned DXF file with extracted polygon overlay."
    )
    parser.add_argument("original_dxf", type=Path, help="Path to original DXF file")
    parser.add_argument("extraction_json", type=Path, help="Path to tokenization_output.json")
    parser.add_argument("--output", type=Path, default=None, help="Output DXF path (default: <input>_cleaned.dxf)")
    parser.add_argument("--normalization", type=Path, default=None, help="Path to normalization.json for layer healing")
    parser.add_argument("--no-labels", action="store_true", help="Skip polygon ID labels")
    parser.add_argument("--no-raw", action="store_true", help="Omit original primitives (extraction only)")
    args = parser.parse_args()

    # Defaults
    if args.output is None:
        stem = args.original_dxf.stem
        args.output = args.original_dxf.parent / f"{stem}_cleaned.dxf"

    # Load extraction results
    with open(args.extraction_json) as f:
        extraction = json.load(f)

    # Load normalization if provided
    normalization = None
    if args.normalization and args.normalization.exists():
        with open(args.normalization) as f:
            normalization = json.load(f)

    summary = write_cleaned_dxf(
        original_path=args.original_dxf,
        extraction_json=extraction,
        output_path=args.output,
        normalization=normalization,
        include_labels=not args.no_labels,
        include_raw=not args.no_raw,
    )

    print(f"Cleaned DXF written to {summary['output_path']}")
    print(f"  Walls:         {summary['walls']}")
    print(f"  Columns:       {summary['columns']}")
    print(f"  Curtain walls: {summary['curtain_walls']}")
    print(f"  Labels:        {summary['labels']}")
    print(f"  Layers added:  {', '.join(summary['layers_added'])}")


if __name__ == "__main__":
    main()
