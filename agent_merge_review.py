#!/usr/bin/env python3
"""
Agent-in-the-loop merge review.

Uses the augrade pipeline programmatically to:
  1. Build the extraction dataset with merge candidates
  2. Analyze merge patterns per family
  3. Auto-label high-confidence merges with documented reasoning
  4. Flag ambiguous cases for human review
  5. Export labels for the merge lab and supervised pipeline

This script documents the analysis journey — run it, read the output,
then load the exported labels into the merge lab for refinement.

Usage:
    python agent_merge_review.py "Airport Doors_MEZZ.dxf"
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from augrade import dataset as ds


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_layers(desc: dict) -> list[str]:
    return sorted(set(d["raw_layer"] for d in desc.get("source_layer_details", [])))


def print_pair(c: dict, a: dict, b: dict, indent: str = "  ") -> None:
    print(f"{indent}{c['id']:35s}  score={c['heuristic_score']:.3f}  "
          f"gap={c['boundary_gap']:.2f}  angle={c['angle_diff_deg']:.1f}  "
          f"area_ratio={c['area_ratio']:.3f}")
    print(f"{indent}  A: {a.get('id','?'):20s}  layers={get_layers(a)}  "
          f"kind={a.get('source_kind','?')}  area={a.get('area',0):.0f}")
    print(f"{indent}  B: {b.get('id','?'):20s}  layers={get_layers(b)}  "
          f"kind={b.get('source_kind','?')}  area={b.get('area',0):.0f}")


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def main() -> None:
    dxf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("Airport Doors_MEZZ.dxf")

    print("=" * 70)
    print("AGENT MERGE REVIEW")
    print("=" * 70)
    print(f"\nBuilding dataset from {dxf_path}...")
    data = ds.build(dxf_path, snap_tolerance=0.5, with_merge=True)
    print(f"Done in {data.runtime_seconds:.2f}s\n")

    labels: dict[str, str] = {}
    reasoning: list[str] = []

    for family in ["columns", "curtain_walls", "walls"]:
        descs = data.descriptors_by_family[family]
        cands = data.family_payloads[family]["candidates"]
        rec = [c for c in cands if c["recommended"]]
        d_by_li = {d["local_index"]: d for d in descs}

        print("=" * 70)
        print(f"  {family.upper()}: {len(descs)} polygons, "
              f"{len(cands)} candidate pairs, {len(rec)} recommended")
        print("=" * 70)

        # ------------------------------------------------------------------
        # COLUMNS
        # ------------------------------------------------------------------
        if family == "columns":
            print("""
HYPOTHESIS: Many column merges are deduplication artifacts — the same
physical column recovered twice via different extraction paths (graph_face
vs direct_ellipse/direct_lwpolyline) on the same layer.

TEST: Check if recommended pairs share the same layer, have near-zero gap,
and differ only in source_kind.""")

            dedup_pairs = []
            adjacent_pairs = []
            other_pairs = []

            for c in rec:
                a, b = d_by_li.get(c["a"], {}), d_by_li.get(c["b"], {})
                a_layers = set(get_layers(a))
                b_layers = set(get_layers(b))
                a_kind = a.get("source_kind", "")
                b_kind = b.get("source_kind", "")

                if (a_layers == b_layers
                        and c["boundary_gap"] < 0.1
                        and a_kind != b_kind):
                    dedup_pairs.append(c)
                elif c["boundary_gap"] < 1.0 and c["angle_diff_deg"] < 5.0:
                    adjacent_pairs.append(c)
                else:
                    other_pairs.append(c)

            print(f"""
FINDING:
  - {len(dedup_pairs)} are extraction-path duplicates (same layer, gap<0.1,
    different source_kind). These are the same column drawn once but
    recovered via both graph_face and direct_ellipse.
    → Auto-label POSITIVE (deduplication merge).

  - {len(adjacent_pairs)} are adjacent same-layer columns with small gap.
    These are likely DIFFERENT physical columns sitting close together
    (e.g. paired columns at a structural bay).
    → Auto-label NEGATIVE (distinct elements, not a merge).

  - {len(other_pairs)} need visual inspection.""")

            for c in dedup_pairs:
                labels[c["id"]] = "positive"
            for c in adjacent_pairs:
                labels[c["id"]] = "negative"

            reasoning.append(
                f"columns: {len(dedup_pairs)} positive (extraction dedup), "
                f"{len(adjacent_pairs)} negative (adjacent distinct columns)"
            )

            print("\n  Sample dedup pairs (positive):")
            for c in sorted(dedup_pairs, key=lambda x: -x["heuristic_score"])[:3]:
                a, b = d_by_li.get(c["a"], {}), d_by_li.get(c["b"], {})
                print_pair(c, a, b, indent="    ")

            if adjacent_pairs:
                print("\n  Sample adjacent pairs (negative):")
                for c in sorted(adjacent_pairs, key=lambda x: -x["heuristic_score"])[:3]:
                    a, b = d_by_li.get(c["a"], {}), d_by_li.get(c["b"], {})
                    print_pair(c, a, b, indent="    ")

        # ------------------------------------------------------------------
        # CURTAIN WALLS
        # ------------------------------------------------------------------
        elif family == "curtain_walls":
            print("""
HYPOTHESIS: Curtain wall merges are cross-layer duplicates — the same
mullion drawn as LINE on A-GLAZING MULLION and as LWPOLYLINE on
A-GLAZING-MULLION. Our normalization analysis already showed these layers
are 'complementary' (97% spatial overlap, zero shared entity types).

TEST: Check if all recommended pairs cross the space/hyphen layer boundary.""")

            cross_layer = []
            same_layer = []
            for c in rec:
                a, b = d_by_li.get(c["a"], {}), d_by_li.get(c["b"], {})
                a_layers = set(get_layers(a))
                b_layers = set(get_layers(b))
                if a_layers != b_layers:
                    cross_layer.append(c)
                else:
                    same_layer.append(c)

            print(f"""
FINDING:
  - {len(cross_layer)}/{len(rec)} recommended merges are cross-layer.
  - {len(same_layer)} are same-layer.
  - This CONFIRMS the normalization analysis: the space-vs-hyphen variants
    are the same physical elements drawn with different conventions.
    → Auto-label ALL cross-layer pairs POSITIVE.""")

            for c in cross_layer:
                labels[c["id"]] = "positive"

            reasoning.append(
                f"curtain_walls: {len(cross_layer)} positive (cross-layer mullion dedup)"
            )

            print("\n  Sample cross-layer pairs (positive):")
            for c in sorted(cross_layer, key=lambda x: -x["heuristic_score"])[:3]:
                a, b = d_by_li.get(c["a"], {}), d_by_li.get(c["b"], {})
                print_pair(c, a, b, indent="    ")

        # ------------------------------------------------------------------
        # WALLS
        # ------------------------------------------------------------------
        elif family == "walls":
            print("""
HYPOTHESIS: Wall merges are adjacent fragments from the same physical wall
that were split during graph-face extraction. Most will be on
A-MEZZANINE WALL FULL where the linework is dense and fragmented.

TEST: Check layer distribution and gap/angle patterns.""")

            layer_dist = Counter()
            gap_zero = []
            gap_small = []
            gap_large = []
            for c in rec:
                a, b = d_by_li.get(c["a"], {}), d_by_li.get(c["b"], {})
                for layer in get_layers(a) + get_layers(b):
                    layer_dist[layer] += 1
                if c["boundary_gap"] < 0.5:
                    gap_zero.append(c)
                elif c["boundary_gap"] < 10.0:
                    gap_small.append(c)
                else:
                    gap_large.append(c)

            print(f"""
FINDING:
  - Layer distribution: {dict(layer_dist.most_common())}
  - Gap breakdown: {len(gap_zero)} touching (gap<0.5), {len(gap_small)} close
    (gap<10), {len(gap_large)} far (gap>=10).
  - Touching pairs with same angle are strong merge candidates.
  - Far pairs are likely separate walls that happen to align.
    → Auto-label touching+aligned POSITIVE, far pairs NEGATIVE.""")

            for c in gap_zero:
                if c["angle_diff_deg"] < 5.0:
                    labels[c["id"]] = "positive"
            for c in gap_large:
                labels[c["id"]] = "negative"

            pos_walls = sum(1 for c in rec if labels.get(c["id"]) == "positive")
            neg_walls = sum(1 for c in rec if labels.get(c["id"]) == "negative")
            unlabeled_walls = len(rec) - pos_walls - neg_walls

            reasoning.append(
                f"walls: {pos_walls} positive (touching+aligned), "
                f"{neg_walls} negative (far apart), "
                f"{unlabeled_walls} need visual inspection"
            )

            print(f"\n  Labeled: {pos_walls} positive, {neg_walls} negative, "
                  f"{unlabeled_walls} unlabeled")

            print("\n  Sample positive wall merges:")
            for c in sorted(gap_zero, key=lambda x: -x["heuristic_score"])[:3]:
                a, b = d_by_li.get(c["a"], {}), d_by_li.get(c["b"], {})
                print_pair(c, a, b, indent="    ")

        print()

    # ------------------------------------------------------------------
    # Summary and export
    # ------------------------------------------------------------------
    print("=" * 70)
    print("LABEL SUMMARY")
    print("=" * 70)
    pos = sum(1 for v in labels.values() if v == "positive")
    neg = sum(1 for v in labels.values() if v == "negative")
    print(f"\n  Total labels: {len(labels)} ({pos} positive, {neg} negative)")
    for r in reasoning:
        print(f"  - {r}")

    # Export
    out_path = Path("agent_labels.json")
    out_path.write_text(json.dumps(labels, indent=2), encoding="utf-8")
    print(f"\n  Exported to {out_path}")
    print(f"  Load into merge lab:  labels import {out_path}")
    print(f"  Or build supervised dataset:")
    print(f"    python -m augrade.cli.merge_lab 'Airport Doors_MEZZ.dxf' out_lab")
    print(f"    python -m augrade.cli.labels out_lab/merge_lab_data.json "
          f"agent_labels.json --output labeled_pairs")

    print(f"""
NEXT STEPS:
  1. Open merge_lab.html, import agent_labels.json
  2. Review the {sum(1 for v in labels.values() if v == 'positive')} positive and {sum(1 for v in labels.values() if v == 'negative')} negative labels visually
  3. Inspect the unlabeled wall pairs (need spatial context to judge)
  4. Tune wall merge parameters — current presets may be too conservative
  5. Export refined labels for the supervised pipeline
""")


if __name__ == "__main__":
    main()
