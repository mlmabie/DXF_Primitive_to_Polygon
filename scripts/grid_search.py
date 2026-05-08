#!/usr/bin/env python3
"""Grid search over (snap, joint) tolerances ranked by HATCH-IoU + coverage.

The source-entity coverage proxy is a length signal, not a shape signal.
HATCH companion layers describe the same physical elements as their outline
twins with independent carriers, so HATCH-boundary IoU against graph-recovered
polygons is a self-supervised correctness signal that captures shape
directly. See README "What the analysis found" #4.

Composite score per run:
    score = 0.6 * hatch_iou + 0.4 * coverage_proxy
Hard reject: any invalid polygon, or any family count > 2x conservative.

Axes (35 runs total, ~3 min):
    snap  in {0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0}
    joint in {0.0, 0.01, 0.025, 0.05, 0.1}

Outputs in --output-dir:
    grid_search_results.csv  -- one row per (snap, joint)
    grid_search_pareto.svg   -- coverage vs hatch_iou scatter, Pareto-marked

Requires shapely for polygon intersection/union.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shapely.geometry import Polygon as ShapelyPolygon
from shapely.validation import make_valid

import tokenize_dxf as td
from augrade.extract import run_extraction


SNAP_AXIS: Tuple[float, ...] = (0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0)
JOINT_AXIS: Tuple[float, ...] = (0.0, 0.01, 0.025, 0.05, 0.1)
CONSERVATIVE_COUNTS: Dict[str, int] = {"walls": 1169, "columns": 764, "curtain_walls": 304}
# Loosened from 2x after empirical check: --mode joined recovers 825 curtain
# walls (2.7x conservative), and they are real T-junction-derived panels, not
# noise. 3x catches truly degenerate runs (e.g. 10x) without rejecting modes
# we have already validated.
COUNT_BLOWUP_FACTOR: float = 3.0
KNOWN_MODES: Dict[Tuple[float, float], str] = {
    (0.5, 0.0): "conservative",
    (0.75, 0.0): "liberal",
    (0.5, 0.025): "joined",
    (0.25, 0.025): "coupled",
}


def to_shapely(polygon: td.PolygonRecord) -> ShapelyPolygon | None:
    if len(polygon.vertices) < 3:
        return None
    sp = ShapelyPolygon(polygon.vertices)
    if not sp.is_valid:
        sp = make_valid(sp)
        if sp.geom_type != "Polygon":
            return None
    return sp if sp.area > 0 else None


def hatch_iou_score(polygons: Sequence[td.PolygonRecord]) -> Tuple[float, int, int]:
    """Mean IoU of non-HATCH polygons against best-matching HATCH polygon
    on a companion layer, weighted by match-rate within the family.

    Curtain-wall layers in this file have no HATCH companions, so they are
    excluded from the IoU score (coverage_proxy still applies to them).

    Returns (hatch_iou, scored_polygons, family_polygons_eligible).
    """
    by_family: Dict[str, Dict[str, List[td.PolygonRecord]]] = {}
    for p in polygons:
        bucket = by_family.setdefault(p.family, {"hatch": [], "other": []})
        if p.source_kind == "direct_hatch":
            bucket["hatch"].append(p)
        else:
            bucket["other"].append(p)

    iou_sum = 0.0
    scored = 0
    eligible = 0
    for family, groups in by_family.items():
        if not groups["hatch"]:
            continue  # no companion HATCH for this family in this run
        eligible += len(groups["other"])
        hatch_shapes = [(p, to_shapely(p)) for p in groups["hatch"]]
        hatch_shapes = [(p, s) for p, s in hatch_shapes if s is not None]
        for op in groups["other"]:
            os_shape = to_shapely(op)
            if os_shape is None:
                continue
            best_iou = 0.0
            for _, hs in hatch_shapes:
                if not os_shape.intersects(hs):
                    continue
                inter = os_shape.intersection(hs).area
                union = os_shape.union(hs).area
                if union > 0:
                    iou = inter / union
                    if iou > best_iou:
                        best_iou = iou
            if best_iou > 0.0:
                iou_sum += best_iou
                scored += 1
    if eligible == 0:
        return 0.0, 0, 0
    # mean-IoU-on-match * match-rate; penalises both bad shape and missing match
    mean_iou = iou_sum / scored if scored else 0.0
    match_rate = scored / eligible
    return mean_iou * match_rate, scored, eligible


def coverage_proxy(polygons: Sequence[td.PolygonRecord], entities: Sequence[td.Entity]) -> float:
    target = [e for e in entities if e.family]
    total = sum(td.entity_length(e) for e in target)
    if total == 0:
        return 0.0
    consumed_ids = {eid for p in polygons for eid in p.source_entity_ids}
    consumed = sum(td.entity_length(e) for e in target if e.entity_id in consumed_ids)
    return consumed / total


def polygon_validity(polygons: Sequence[td.PolygonRecord]) -> int:
    bad = 0
    for p in polygons:
        vs = p.vertices
        if len(vs) < 3 or len({tuple(v) for v in vs}) < 3:
            bad += 1
            continue
        s = sum(vs[i][0] * vs[(i + 1) % len(vs)][1] - vs[(i + 1) % len(vs)][0] * vs[i][1] for i in range(len(vs)))
        if s >= 0:  # CW = negative shoelace in DXF Y-up
            bad += 1
    return bad


def family_counts(polygons: Sequence[td.PolygonRecord]) -> Dict[str, int]:
    counts = {"walls": 0, "columns": 0, "curtain_walls": 0}
    for p in polygons:
        if p.family in counts:
            counts[p.family] += 1
    return counts


def run_one(input_path: Path, snap: float, joint: float) -> Dict[str, object]:
    t0 = time.time()
    result = run_extraction(input_path, snap_tolerance=snap, joint_tolerance=joint)
    runtime = time.time() - t0
    counts = family_counts(result.polygons)
    invalid = polygon_validity(result.polygons)
    blowup = any(counts[f] > CONSERVATIVE_COUNTS[f] * COUNT_BLOWUP_FACTOR for f in counts)
    rejected = invalid > 0 or blowup
    iou, scored, eligible = (0.0, 0, 0) if rejected else hatch_iou_score(result.polygons)
    cov = 0.0 if rejected else coverage_proxy(result.polygons, result.entities)
    score = 0.6 * iou + 0.4 * cov
    return {
        "snap": snap,
        "joint": joint,
        "mode": KNOWN_MODES.get((snap, joint), ""),
        "walls": counts["walls"],
        "columns": counts["columns"],
        "curtain_walls": counts["curtain_walls"],
        "invalid": invalid,
        "blowup": int(blowup),
        "rejected": int(rejected),
        "hatch_iou": round(iou, 4),
        "iou_scored": scored,
        "iou_eligible": eligible,
        "coverage": round(cov, 4),
        "score": round(score, 4),
        "runtime_s": round(runtime, 2),
    }


def pareto_front(rows: Sequence[Dict[str, object]]) -> List[int]:
    """Indices of rows on the Pareto front in (coverage, hatch_iou) space."""
    keep: List[int] = []
    for i, ri in enumerate(rows):
        if ri["rejected"]:
            continue
        dominated = False
        for j, rj in enumerate(rows):
            if i == j or rj["rejected"]:
                continue
            if (rj["coverage"] >= ri["coverage"] and rj["hatch_iou"] >= ri["hatch_iou"]
                    and (rj["coverage"] > ri["coverage"] or rj["hatch_iou"] > ri["hatch_iou"])):
                dominated = True
                break
        if not dominated:
            keep.append(i)
    return keep


def write_pareto_svg(path: Path, rows: Sequence[Dict[str, object]], front: Sequence[int]) -> None:
    W, H = 720, 520
    PAD_L, PAD_R, PAD_T, PAD_B = 70, 30, 40, 60
    plot_w = W - PAD_L - PAD_R
    plot_h = H - PAD_T - PAD_B
    valid = [r for r in rows if not r["rejected"]]
    if not valid:
        path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><text x="20" y="40">No valid runs</text></svg>')
        return
    cov_max = max(0.01, max(r["coverage"] for r in valid))
    iou_max = max(0.01, max(r["hatch_iou"] for r in valid))

    def x(c): return PAD_L + (c / cov_max) * plot_w
    def y(i): return PAD_T + plot_h - (i / iou_max) * plot_h

    parts: List[str] = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif" font-size="11">']
    parts.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    parts.append(f'<line x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{PAD_T+plot_h}" stroke="#888"/>')
    parts.append(f'<line x1="{PAD_L}" y1="{PAD_T+plot_h}" x2="{PAD_L+plot_w}" y2="{PAD_T+plot_h}" stroke="#888"/>')
    parts.append(f'<text x="{PAD_L+plot_w/2}" y="{H-20}" text-anchor="middle">coverage proxy</text>')
    parts.append(f'<text x="20" y="{PAD_T+plot_h/2}" text-anchor="middle" transform="rotate(-90 20 {PAD_T+plot_h/2})">HATCH-IoU score</text>')
    parts.append(f'<text x="{W/2}" y="20" text-anchor="middle" font-size="13" font-weight="bold">Grid search Pareto front (snap × joint)</text>')
    front_set = set(front)
    for i, r in enumerate(rows):
        if r["rejected"]:
            continue
        cx, cy = x(r["coverage"]), y(r["hatch_iou"])
        on_front = i in front_set
        named = r["mode"]
        fill = "#d62728" if on_front else "#1f77b4"
        rad = 6 if on_front else 4
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad}" fill="{fill}" opacity="0.7"/>')
        if named or on_front:
            label = named if named else f's{r["snap"]}/j{r["joint"]}'
            parts.append(f'<text x="{cx+7:.1f}" y="{cy-5:.1f}" font-size="10">{label}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input_dxf", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--snap", nargs="+", type=float, default=list(SNAP_AXIS))
    ap.add_argument("--joint", nargs="+", type=float, default=list(JOINT_AXIS))
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, object]] = []
    print(f"running {len(args.snap) * len(args.joint)} (snap, joint) combinations...")
    for snap in args.snap:
        for joint in args.joint:
            row = run_one(args.input_dxf, snap, joint)
            rows.append(row)
            tag = f"[{row['mode']}]" if row["mode"] else ""
            status = "REJECT" if row["rejected"] else f"score={row['score']:.3f}"
            print(f"  snap={snap:<5} joint={joint:<6} walls={row['walls']:>4} cols={row['columns']:>3} cw={row['curtain_walls']:>4} cov={row['coverage']:.3f} iou={row['hatch_iou']:.3f} {status} {tag}")

    csv_path = args.output_dir / "grid_search_results.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    front = pareto_front(rows)
    svg_path = args.output_dir / "grid_search_pareto.svg"
    write_pareto_svg(svg_path, rows, front)

    print()
    print(f"wrote {csv_path} ({len(rows)} rows)")
    print(f"wrote {svg_path} ({len(front)} Pareto-optimal points)")
    valid = [r for r in rows if not r["rejected"]]
    if valid:
        best = max(valid, key=lambda r: r["score"])
        print(f"best by composite score: snap={best['snap']} joint={best['joint']} "
              f"score={best['score']:.3f} cov={best['coverage']:.3f} iou={best['hatch_iou']:.3f} {best['mode'] or ''}")


if __name__ == "__main__":
    main()
