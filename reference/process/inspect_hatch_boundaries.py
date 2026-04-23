#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Sequence, Tuple


TARGET_HATCH_LAYERS = {
    "A-EXTERNAL WALL HATCH",
    "A-MEZZANINE WALL FULL HATCH",
    "A-WALL 1 HATCH",
    "A-WALL 2 HATCH",
}

PATH_FLAG_BITS = {
    1: "external",
    2: "polyline",
    4: "derived",
    8: "textbox",
    16: "outermost",
    32: "texture",
}

EDGE_TYPE_NAMES = {
    1: "line",
    2: "circular_arc",
    3: "elliptic_arc",
    4: "spline",
}


Pair = Tuple[int, str]


def read_dxf_pairs(path: Path) -> Iterator[Pair]:
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        while True:
            code = handle.readline()
            if not code:
                break
            value = handle.readline()
            if not value:
                break
            yield int(code.strip() or 0), value.rstrip("\r\n")


def iter_raw_entities(path: Path) -> Iterator[Tuple[str, List[Pair]]]:
    in_entities = False
    current_type: Optional[str] = None
    current_tags: List[Pair] = []

    for code, raw in read_dxf_pairs(path):
        if not in_entities:
            if code == 2 and raw == "ENTITIES":
                in_entities = True
            continue

        if code == 0 and raw == "ENDSEC":
            if current_type is not None:
                yield current_type, current_tags
            break

        if code == 0:
            if current_type is not None:
                yield current_type, current_tags
            current_type = raw
            current_tags = []
            continue

        if current_type is not None:
            current_tags.append((code, raw))


def entity_layer(tags: Sequence[Pair]) -> str:
    for code, raw in tags:
        if code == 8:
            return raw
    return ""


def decode_path_flags(flags: int) -> List[str]:
    labels = [name for bit, name in PATH_FLAG_BITS.items() if flags & bit]
    return labels or ["default"]


def parse_hatch_paths(tags: Sequence[Pair]) -> List[Dict[str, object]]:
    paths: List[Dict[str, object]] = []
    path_index = 0
    while path_index < len(tags):
        code, raw = tags[path_index]
        if code != 92:
            path_index += 1
            continue

        flags = int(raw)
        path: Dict[str, object] = {
            "flags": flags,
            "labels": decode_path_flags(flags),
            "polyline": bool(flags & 2),
            "edge_types": [],
            "vertices": 0,
            "edges": 0,
        }
        path_index += 1

        if flags & 2:
            vertex_count = 0
            while path_index < len(tags):
                code, raw = tags[path_index]
                if code == 93:
                    vertex_count = int(raw)
                    path_index += 1
                    break
                if code in {92, 75, 76, 98}:
                    break
                path_index += 1
            seen_vertices = 0
            while path_index < len(tags) and seen_vertices < vertex_count:
                code, raw = tags[path_index]
                if code == 10:
                    seen_vertices += 1
                path_index += 1
            path["vertices"] = vertex_count
            paths.append(path)
            continue

        edge_count = 0
        while path_index < len(tags):
            code, raw = tags[path_index]
            if code == 93:
                edge_count = int(raw)
                path_index += 1
                break
            if code in {92, 75, 76, 98}:
                break
            path_index += 1

        edge_types: List[int] = []
        while path_index < len(tags) and len(edge_types) < edge_count:
            code, raw = tags[path_index]
            if code == 72:
                edge_types.append(int(raw))
            path_index += 1
        path["edges"] = edge_count
        path["edge_types"] = edge_types
        paths.append(path)

    return paths


def format_pairs(tags: Sequence[Pair]) -> str:
    return "\n".join(f"{code:>3}\n{raw}" for code, raw in tags)


def write_summary(input_path: Path, output_path: Path, sample_count: int) -> None:
    hatch_entities: List[Tuple[str, List[Pair], List[Dict[str, object]]]] = []
    for entity_type, tags in iter_raw_entities(input_path):
        if entity_type != "HATCH":
            continue
        layer = entity_layer(tags)
        if layer not in TARGET_HATCH_LAYERS:
            continue
        hatch_entities.append((layer, tags, parse_hatch_paths(tags)))

    layer_counts = Counter(layer for layer, _, _ in hatch_entities)
    path_count_distribution = Counter(len(paths) for _, _, paths in hatch_entities)
    flag_distribution = Counter()
    edge_type_distribution = Counter()
    polyline_vertex_distribution = Counter()
    edge_count_distribution = Counter()

    for _, _, paths in hatch_entities:
        for path in paths:
            flag_distribution[path["flags"]] += 1
            for edge_type in path["edge_types"]:
                edge_type_distribution[edge_type] += 1
            vertices = int(path["vertices"])
            edges = int(path["edges"])
            if vertices:
                polyline_vertex_distribution[vertices] += 1
            if edges:
                edge_count_distribution[edges] += 1

    nested = [
        (layer, index + 1, [path["flags"] for path in paths])
        for index, (layer, _, paths) in enumerate(hatch_entities)
        if len(paths) > 1
    ]

    lines = [
        "# HATCH Boundary Inspection",
        "",
        f"Input: `{input_path}`",
        "",
        "## Companion Layer Counts",
        "",
        f"- Total HATCH entities on companion layers: `{len(hatch_entities)}`",
    ]
    for layer, count in sorted(layer_counts.items()):
        lines.append(f"- `{layer}`: `{count}`")

    lines.extend(
        [
            "",
            "## Boundary Path Shape",
            "",
            f"- Boundary path count distribution: `{dict(sorted(path_count_distribution.items()))}`",
            "- Path flag distribution:",
        ]
    )
    for flags, count in sorted(flag_distribution.items()):
        labels = ", ".join(decode_path_flags(flags))
        lines.append(f"  - `{flags}` ({labels}): `{count}` paths")

    lines.append("- Polyline vertex count distribution:")
    for vertices, count in sorted(polyline_vertex_distribution.items()):
        lines.append(f"  - `{vertices}` vertices: `{count}` paths")
    if not polyline_vertex_distribution:
        lines.append("  - none")

    lines.append("- Edge path edge count distribution:")
    for edges, count in sorted(edge_count_distribution.items()):
        lines.append(f"  - `{edges}` edges: `{count}` paths")
    if not edge_count_distribution:
        lines.append("  - none")

    lines.append("- Edge type codes inside edge paths:")
    for edge_type, count in sorted(edge_type_distribution.items()):
        label = EDGE_TYPE_NAMES.get(edge_type, "unknown")
        lines.append(f"  - `{edge_type}` ({label}): `{count}`")
    if not edge_type_distribution:
        lines.append("  - none")

    lines.extend(["", "## Nested Paths / Holes", ""])
    if nested:
        lines.append(f"- HATCH entities with more than one boundary path: `{len(nested)}`")
        for layer, ordinal, flags in nested[:20]:
            labels = ["+".join(decode_path_flags(flag)) for flag in flags]
            lines.append(f"  - `{layer}` entity #{ordinal}: flags `{flags}` ({'; '.join(labels)})")
        if len(nested) > 20:
            lines.append(f"  - ... {len(nested) - 20} more")
    else:
        lines.append("- No multi-path HATCH entities found on the companion layers.")

    lines.extend(["", "## Verbatim Samples", ""])
    for sample_index, (layer, tags, paths) in enumerate(hatch_entities[:sample_count], start=1):
        lines.append(f"### Sample {sample_index}: `{layer}`")
        lines.append("")
        lines.append(f"- Parsed paths: `{paths}`")
        lines.append("")
        lines.append("```dxf")
        lines.append("  0")
        lines.append("HATCH")
        lines.append(format_pairs(tags))
        lines.append("```")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect HATCH boundary paths on known wall companion layers.")
    parser.add_argument("input_dxf", type=Path)
    parser.add_argument(
        "output_md",
        type=Path,
        nargs="?",
        default=Path("reference/process/hatch_boundary_inspection.md"),
    )
    parser.add_argument("--samples", type=int, default=3)
    args = parser.parse_args()
    write_summary(args.input_dxf, args.output_md, args.samples)
    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
