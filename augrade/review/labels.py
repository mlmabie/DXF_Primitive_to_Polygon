#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


VALID_LABELS = {"positive", "negative"}


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_labels(payload: Dict[str, object]) -> Dict[str, str]:
    if isinstance(payload, dict) and "labels" in payload and isinstance(payload["labels"], dict):
        raw = payload["labels"]
    else:
        raw = payload
    labels: Dict[str, str] = {}
    for candidate_id, label in raw.items():
        if label in VALID_LABELS:
            labels[str(candidate_id)] = str(label)
    return labels


def iter_rows(merge_data: Dict[str, object], labels: Dict[str, str], include_unlabeled: bool) -> Iterable[Dict[str, object]]:
    families = merge_data["families"]
    for family, payload in families.items():
        polygons = {polygon["local_index"]: polygon for polygon in payload["polygons"]}
        for candidate in payload["candidates"]:
            candidate_id = candidate["id"]
            label = labels.get(candidate_id)
            if label is None and not include_unlabeled:
                continue
            polygon_a = polygons[candidate["a"]]
            polygon_b = polygons[candidate["b"]]
            row = {
                "candidate_id": candidate_id,
                "family": family,
                "label": label or "",
                "polygon_a_id": polygon_a["id"],
                "polygon_b_id": polygon_b["id"],
                "polygon_a_source_kind": polygon_a["source_kind"],
                "polygon_b_source_kind": polygon_b["source_kind"],
                "polygon_a_layers": "|".join(polygon_a["source_layers"]),
                "polygon_b_layers": "|".join(polygon_b["source_layers"]),
                "polygon_a_area": polygon_a["area"],
                "polygon_b_area": polygon_b["area"],
                "polygon_a_thickness": polygon_a["thickness"],
                "polygon_b_thickness": polygon_b["thickness"],
                "polygon_a_aspect_ratio": polygon_a["aspect_ratio"],
                "polygon_b_aspect_ratio": polygon_b["aspect_ratio"],
                "bbox_gap": candidate["bbox_gap"],
                "boundary_gap": candidate["boundary_gap"],
                "center_gap": candidate["center_gap"],
                "angle_diff_deg": candidate["angle_diff_deg"],
                "thickness_rel_diff": candidate["thickness_rel_diff"],
                "area_ratio": candidate["area_ratio"],
                "span_ratio": candidate["span_ratio"],
                "gap_major_norm": candidate["gap_major_norm"],
                "gap_minor_norm": candidate["gap_minor_norm"],
                "overlap_major_ratio": candidate["overlap_major_ratio"],
                "overlap_minor_ratio": candidate["overlap_minor_ratio"],
                "bbox_iou": candidate["bbox_iou"],
                "layer_jaccard": candidate["layer_jaccard"],
                "same_source_kind": candidate["same_source_kind"],
                "scale_ref": candidate["scale_ref"],
                "heuristic_score": candidate["heuristic_score"],
                "hard_pass": candidate["hard_pass"],
                "recommended": candidate["recommended"],
            }
            yield row


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a labeled merge-candidate dataset from merge_lab_data and an exported label file.")
    parser.add_argument("merge_lab_data", type=Path, help="Path to merge_lab_data.json")
    parser.add_argument("labels_json", type=Path, help="Path to exported merge-lab labels JSON")
    parser.add_argument("output_dir", type=Path, help="Directory for labeled dataset outputs")
    parser.add_argument("--include-unlabeled", action="store_true", help="Include unlabeled candidates with empty label fields")
    args = parser.parse_args()

    merge_data = load_json(args.merge_lab_data)
    label_payload = load_json(args.labels_json)
    labels = normalize_labels(label_payload)

    rows = list(iter_rows(merge_data, labels, include_unlabeled=args.include_unlabeled))
    counts = {
        "total_rows": len(rows),
        "positive": sum(1 for row in rows if row["label"] == "positive"),
        "negative": sum(1 for row in rows if row["label"] == "negative"),
        "unlabeled": sum(1 for row in rows if not row["label"]),
    }

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    dataset = {
        "meta": {
            "merge_lab_data": str(args.merge_lab_data),
            "labels_json": str(args.labels_json),
            "include_unlabeled": args.include_unlabeled,
            "counts": counts,
        },
        "rows": rows,
    }

    (output_dir / "labeled_merge_pairs.json").write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    write_csv(output_dir / "labeled_merge_pairs.csv", rows)
    (output_dir / "labeled_merge_pairs_summary.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
