"""Shared geometry helpers used by the dataset layer, HTML renderers, and REPL.

All polygon inputs are sequences of (x, y) tuples with the closing vertex repeated
(the same convention used by tokenize_dxf.PolygonRecord.vertices). The
``entity_to_dxf_snippet`` helper accepts a tokenize_dxf.Entity.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple

import tokenize_dxf as td


Point = Tuple[float, float]


def distance(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def polygon_perimeter(points: Sequence[Point]) -> float:
    return sum(distance(points[idx], points[idx + 1]) for idx in range(len(points) - 1))


def polygon_centroid(points: Sequence[Point]) -> Point:
    area = td.polygon_area(points)
    if abs(area) < 1e-9:
        xs = [x for x, _ in points[:-1]]
        ys = [y for _, y in points[:-1]]
        return (sum(xs) / len(xs), sum(ys) / len(ys))
    cx = 0.0
    cy = 0.0
    for idx in range(len(points) - 1):
        x1, y1 = points[idx]
        x2, y2 = points[idx + 1]
        cross = x1 * y2 - x2 * y1
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    factor = 1.0 / (6.0 * area)
    return cx * factor, cy * factor


def dominant_orientation(points: Sequence[Point]) -> float:
    sum_x = 0.0
    sum_y = 0.0
    for idx in range(len(points) - 1):
        x1, y1 = points[idx]
        x2, y2 = points[idx + 1]
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length <= 1e-9:
            continue
        theta = math.atan2(dy, dx)
        sum_x += length * math.cos(2 * theta)
        sum_y += length * math.sin(2 * theta)
    if abs(sum_x) < 1e-9 and abs(sum_y) < 1e-9:
        return 0.0
    return 0.5 * math.atan2(sum_y, sum_x)


def angle_diff_degrees(theta_a: float, theta_b: float) -> float:
    diff = abs(theta_a - theta_b) % math.pi
    diff = min(diff, math.pi - diff)
    return math.degrees(diff)


def averaged_orientation(theta_a: float, theta_b: float) -> float:
    sum_x = math.cos(2 * theta_a) + math.cos(2 * theta_b)
    sum_y = math.sin(2 * theta_a) + math.sin(2 * theta_b)
    if abs(sum_x) < 1e-9 and abs(sum_y) < 1e-9:
        return theta_a
    return 0.5 * math.atan2(sum_y, sum_x)


def projection_interval(points: Sequence[Point], theta: float) -> Tuple[float, float]:
    ux = math.cos(theta)
    uy = math.sin(theta)
    projected = [x * ux + y * uy for x, y in points[:-1]]
    return min(projected), max(projected)


def interval_overlap_ratio(interval_a: Tuple[float, float], interval_b: Tuple[float, float]) -> float:
    overlap = min(interval_a[1], interval_b[1]) - max(interval_a[0], interval_b[0])
    denom = min(interval_a[1] - interval_a[0], interval_b[1] - interval_b[0])
    if denom <= 1e-9:
        return 0.0
    return max(0.0, overlap) / denom


def interval_gap(interval_a: Tuple[float, float], interval_b: Tuple[float, float]) -> float:
    if interval_a[1] < interval_b[0]:
        return interval_b[0] - interval_a[1]
    if interval_b[1] < interval_a[0]:
        return interval_a[0] - interval_b[1]
    return 0.0


def bbox_gap(
    bbox_a: Tuple[float, float, float, float],
    bbox_b: Tuple[float, float, float, float],
) -> float:
    dx = max(0.0, max(bbox_a[0] - bbox_b[2], bbox_b[0] - bbox_a[2]))
    dy = max(0.0, max(bbox_a[1] - bbox_b[3], bbox_b[1] - bbox_a[3]))
    return math.hypot(dx, dy)


def bbox_iou(
    bbox_a: Tuple[float, float, float, float],
    bbox_b: Tuple[float, float, float, float],
) -> float:
    x1 = max(bbox_a[0], bbox_b[0])
    y1 = max(bbox_a[1], bbox_b[1])
    x2 = min(bbox_a[2], bbox_b[2])
    y2 = min(bbox_a[3], bbox_b[3])
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    area_a = max(0.0, bbox_a[2] - bbox_a[0]) * max(0.0, bbox_a[3] - bbox_a[1])
    area_b = max(0.0, bbox_b[2] - bbox_b[0]) * max(0.0, bbox_b[3] - bbox_b[1])
    union = area_a + area_b - inter
    return inter / union if union > 1e-9 else 0.0


def point_segment_distance(point: Point, a: Point, b: Point) -> float:
    ax, ay = a
    bx, by = b
    px, py = point
    dx = bx - ax
    dy = by - ay
    length_sq = dx * dx + dy * dy
    if length_sq <= 1e-12:
        return distance(point, a)
    t = ((px - ax) * dx + (py - ay) * dy) / length_sq
    t = max(0.0, min(1.0, t))
    nearest = (ax + t * dx, ay + t * dy)
    return distance(point, nearest)


def segment_distance(a1: Point, a2: Point, b1: Point, b2: Point) -> float:
    if td.segments_intersect(a1, a2, b1, b2):
        return 0.0
    return min(
        point_segment_distance(a1, b1, b2),
        point_segment_distance(a2, b1, b2),
        point_segment_distance(b1, a1, a2),
        point_segment_distance(b2, a1, a2),
    )


def ring_boundary_gap(ring_a: Sequence[Point], ring_b: Sequence[Point]) -> float:
    best = float("inf")
    for idx in range(len(ring_a) - 1):
        a1 = ring_a[idx]
        a2 = ring_a[idx + 1]
        for jdx in range(len(ring_b) - 1):
            b1 = ring_b[jdx]
            b2 = ring_b[jdx + 1]
            best = min(best, segment_distance(a1, a2, b1, b2))
            if best <= 1e-9:
                return 0.0
    return best


def equivalent_radius(area: float) -> float:
    return math.sqrt(max(area, 0.0) / math.pi) if area > 0.0 else 1.0


def layer_jaccard(layers_a: Sequence[str], layers_b: Sequence[str]) -> float:
    set_a = set(layers_a)
    set_b = set(layers_b)
    union = set_a | set_b
    return len(set_a & set_b) / len(union) if union else 0.0


def entity_to_dxf_snippet(entity: td.Entity, max_lines: int = 40) -> str:
    """Render a tokenize_dxf.Entity into a short DXF code snippet string.

    Callers that need byte-identical output to the prior build_dashboard
    (``max_lines=44``) or build_merge_lab (``max_lines=38``) defaults should
    pass ``max_lines`` explicitly.
    """
    lines = ["0", entity.type]
    if entity.type == "POLYLINE":
        for code, raw in entity.tags:
            lines.extend([str(code), raw])
        for x, y, bulge in entity.points:
            lines.extend(["0", "VERTEX", "10", f"{x}", "20", f"{y}"])
            if abs(bulge) > 1e-9:
                lines.extend(["42", f"{bulge}"])
        lines.extend(["0", "SEQEND"])
    else:
        for code, raw in entity.tags:
            lines.extend([str(code), raw])
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["...", "..."]
    return "\n".join(lines)
