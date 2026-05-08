#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
import tokenize_dxf as td  # noqa: E402


FAMILIES = ["walls", "columns", "curtain_walls"]
ENTITY_TYPES = [
    "LINE",
    "LWPOLYLINE",
    "HATCH",
    "ELLIPSE",
    "ARC",
    "CIRCLE",
    "INSERT",
    "POLYLINE",
    "3DFACE",
    "POINT",
    "OTHER",
]


@dataclass
class Node:
    entity_id: str
    entity_type: str
    family: str
    centroid: Tuple[float, float]
    endpoints: List[Tuple[float, float]]
    features: List[float]


def _path_length(path: Sequence[td.Point]) -> float:
    return sum(td.distance(path[i], path[i + 1]) for i in range(len(path) - 1))


def _orientation_feature(paths: Sequence[Sequence[td.Point]]) -> Tuple[float, float]:
    best = None
    best_len = 0.0
    for path in paths:
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            length = td.distance(a, b)
            if length > best_len:
                best = (a, b)
                best_len = length
    if best is None or best_len <= 1e-9:
        return 0.0, 1.0
    (x1, y1), (x2, y2) = best
    angle = math.atan2(y2 - y1, x2 - x1)
    return math.sin(angle), math.cos(angle)


def _node_from_entity(entity: td.Entity) -> Node | None:
    if entity.family not in FAMILIES:
        return None

    paths = td.entity_to_draw_paths(entity)
    points = [point for path in paths for point in path]
    if not points and entity.start and entity.end:
        points = [entity.start, entity.end]
        paths = [points]
    if not points:
        return None

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x
    height = max_y - min_y
    bbox_area = max(width * height, 1e-9)
    length = sum(_path_length(path) for path in paths)
    area = sum(abs(td.polygon_area(path)) for path in paths if len(path) >= 4)
    aspect = max(width, height) / max(min(width, height), 1e-9)
    point_count = sum(len(path) for path in paths)
    segment_count = sum(max(0, len(path) - 1) for path in paths)
    compactness = min(area / bbox_area, 1.0)
    sin_o, cos_o = _orientation_feature(paths)

    type_name = entity.type if entity.type in ENTITY_TYPES else "OTHER"
    type_features = [1.0 if type_name == item else 0.0 for item in ENTITY_TYPES]
    endpoints = []
    for path in paths:
        if path:
            endpoints.append(path[0])
            endpoints.append(path[-1])

    features = type_features + [
        1.0 if entity.closed else 0.0,
        math.log1p(length),
        math.log1p(area),
        math.log1p(width),
        math.log1p(height),
        math.log1p(aspect),
        math.log1p(point_count),
        math.log1p(segment_count),
        compactness,
        sin_o,
        cos_o,
        math.log1p(entity.radius or 0.0),
    ]

    return Node(
        entity_id=entity.entity_id,
        entity_type=entity.type,
        family=entity.family,
        centroid=((min_x + max_x) / 2.0, (min_y + max_y) / 2.0),
        endpoints=endpoints,
        features=features,
    )


def load_nodes(path: Path, sample_per_family: int, seed: int) -> List[Node]:
    grouped: Dict[str, List[Node]] = defaultdict(list)
    for entity in td.iter_entities(path):
        node = _node_from_entity(entity)
        if node is not None:
            grouped[node.family].append(node)

    rng = random.Random(seed)
    nodes: List[Node] = []
    for family in FAMILIES:
        family_nodes = grouped[family]
        rng.shuffle(family_nodes)
        nodes.extend(family_nodes[:sample_per_family])
    rng.shuffle(nodes)
    return nodes


def build_edges(nodes: Sequence[Node], k: int, snap_tolerance: float) -> np.ndarray:
    edges = set()
    centroids = np.array([node.centroid for node in nodes], dtype=np.float64)
    min_xy = centroids.min(axis=0)
    max_xy = centroids.max(axis=0)
    span = np.maximum(max_xy - min_xy, 1e-9)
    cell = span / 48.0
    bins: Dict[Tuple[int, int], List[int]] = defaultdict(list)
    for i, point in enumerate(centroids):
        key = tuple(np.floor((point - min_xy) / cell).astype(int))
        bins[key].append(i)

    for i, point in enumerate(centroids):
        bx, by = tuple(np.floor((point - min_xy) / cell).astype(int))
        candidates: List[int] = []
        radius = 1
        while len(candidates) < k * 4 and radius <= 4:
            candidates.clear()
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    candidates.extend(bins.get((bx + dx, by + dy), []))
            radius += 1
        candidates = [j for j in candidates if j != i]
        if candidates:
            nearest = sorted(candidates, key=lambda j: float(np.sum((centroids[i] - centroids[j]) ** 2)))[:k]
            for j in nearest:
                edges.add((i, j))
                edges.add((j, i))

    endpoint_bins: Dict[Tuple[int, int], List[int]] = defaultdict(list)
    for i, node in enumerate(nodes):
        for x, y in node.endpoints:
            key = (round(x / snap_tolerance), round(y / snap_tolerance))
            endpoint_bins[key].append(i)
    for owners in endpoint_bins.values():
        unique = sorted(set(owners))
        if 1 < len(unique) <= 16:
            for a in unique:
                for b in unique:
                    if a != b:
                        edges.add((a, b))

    if not edges:
        return np.empty((2, 0), dtype=np.int64)
    return np.array(sorted(edges), dtype=np.int64).T


def normalized_edges(n: int, edge_index: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    loops = np.vstack([np.arange(n), np.arange(n)])
    edges = np.concatenate([edge_index, loops], axis=1) if edge_index.size else loops
    degree = np.bincount(edges[1], minlength=n).astype(np.float64)
    weight = 1.0 / np.sqrt(np.maximum(degree[edges[0]] * degree[edges[1]], 1e-12))
    return edges, weight


def propagate(x: np.ndarray, edges: np.ndarray, weight: np.ndarray) -> np.ndarray:
    out = np.zeros_like(x)
    np.add.at(out, edges[1], x[edges[0]] * weight[:, None])
    return out


def stratified_split(labels: np.ndarray, train_frac: float, seed: int) -> Tuple[np.ndarray, np.ndarray]:
    rng = random.Random(seed)
    train, test = [], []
    for label in sorted(set(labels.tolist())):
        idx = [i for i, y in enumerate(labels) if y == label]
        rng.shuffle(idx)
        cut = max(1, int(len(idx) * train_frac))
        train.extend(idx[:cut])
        test.extend(idx[cut:])
    return np.array(sorted(train)), np.array(sorted(test))


def accuracy(logits: np.ndarray, labels: np.ndarray, idx: np.ndarray) -> float:
    pred = logits[idx].argmax(axis=1)
    return float(np.mean(pred == labels[idx])) if len(idx) else 0.0


def train_model(
    x: np.ndarray,
    labels: np.ndarray,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
    edge_index: np.ndarray,
    hidden: int,
    epochs: int,
    lr: float,
    seed: int,
) -> Tuple[Dict[str, float], np.ndarray]:
    rng = np.random.default_rng(seed)
    n, in_dim = x.shape
    classes = int(labels.max()) + 1
    edges, weight = normalized_edges(n, edge_index)
    ax = propagate(x, edges, weight)
    w0 = rng.normal(0.0, math.sqrt(2.0 / in_dim), size=(in_dim, hidden))
    b0 = np.zeros(hidden)
    w1 = rng.normal(0.0, math.sqrt(2.0 / hidden), size=(hidden, classes))
    b1 = np.zeros(classes)
    y_onehot = np.eye(classes)[labels]

    for _ in range(epochs):
        h_pre = ax @ w0 + b0
        h = np.maximum(h_pre, 0.0)
        ah = propagate(h, edges, weight)
        logits = ah @ w1 + b1
        shifted = logits[train_idx] - logits[train_idx].max(axis=1, keepdims=True)
        probs_train = np.exp(shifted)
        probs_train /= probs_train.sum(axis=1, keepdims=True)

        dlogits = np.zeros_like(logits)
        dlogits[train_idx] = (probs_train - y_onehot[train_idx]) / len(train_idx)
        dw1 = ah.T @ dlogits
        db1 = dlogits.sum(axis=0)
        dah = dlogits @ w1.T
        dh = propagate(dah, edges[[1, 0]], weight)
        dh_pre = dh * (h_pre > 0.0)
        dw0 = ax.T @ dh_pre
        db0 = dh_pre.sum(axis=0)
        w0 -= lr * dw0
        b0 -= lr * db0
        w1 -= lr * dw1
        b1 -= lr * db1

    logits = propagate(np.maximum(ax @ w0 + b0, 0.0), edges, weight) @ w1 + b1
    return {"train_acc": accuracy(logits, labels, train_idx), "test_acc": accuracy(logits, labels, test_idx)}, logits


def confusion(logits: np.ndarray, labels: np.ndarray, idx: np.ndarray, classes: int) -> List[List[int]]:
    pred = logits[idx].argmax(axis=1)
    matrix = np.zeros((classes, classes), dtype=int)
    for truth, guess in zip(labels[idx], pred):
        matrix[int(truth), int(guess)] += 1
    return matrix.tolist()


def main() -> None:
    parser = argparse.ArgumentParser(description="Layer-hidden primitive graph classifier MVP.")
    parser.add_argument("--dxf", type=Path, default=REPO_ROOT / "Airport Doors_MEZZ.dxf")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "gnn_plan/experiments/runs/primitive_graph_classifier")
    parser.add_argument("--sample-per-family", type=int, default=1200)
    parser.add_argument("--knn", type=int, default=8)
    parser.add_argument("--snap-tolerance", type=float, default=0.5)
    parser.add_argument("--hidden", type=int, default=48)
    parser.add_argument("--epochs", type=int, default=180)
    parser.add_argument("--lr", type=float, default=0.04)
    parser.add_argument("--train-frac", type=float, default=0.7)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    start = time.time()
    nodes = load_nodes(args.dxf, args.sample_per_family, args.seed)
    if not nodes:
        raise SystemExit("no family-labeled primitive nodes found")

    x = np.array([node.features for node in nodes], dtype=np.float64)
    label_map = {family: i for i, family in enumerate(FAMILIES)}
    labels = np.array([label_map[node.family] for node in nodes], dtype=np.int64)
    train_idx, test_idx = stratified_split(labels, args.train_frac, args.seed)
    mean = x[train_idx].mean(axis=0)
    std = np.maximum(x[train_idx].std(axis=0), 1e-6)
    x = (x - mean) / std

    edge_index = build_edges(nodes, args.knn, args.snap_tolerance)
    identity_edges = np.empty((2, 0), dtype=np.int64)
    baseline, baseline_logits = train_model(
        x, labels, train_idx, test_idx, identity_edges, args.hidden, args.epochs, args.lr, args.seed
    )
    graph, graph_logits = train_model(
        x, labels, train_idx, test_idx, edge_index, args.hidden, args.epochs, args.lr, args.seed
    )

    args.out.mkdir(parents=True, exist_ok=True)
    result = {
        "dxf": str(args.dxf),
        "seed": args.seed,
        "node_count": len(nodes),
        "edge_count": int(edge_index.shape[1]),
        "train_count": int(len(train_idx)),
        "test_count": int(len(test_idx)),
        "family_counts": Counter(node.family for node in nodes),
        "entity_type_counts": Counter(node.entity_type for node in nodes),
        "feature_names": ENTITY_TYPES
        + [
            "closed",
            "log_length",
            "log_area",
            "log_width",
            "log_height",
            "log_aspect",
            "log_point_count",
            "log_segment_count",
            "compactness",
            "orientation_sin",
            "orientation_cos",
            "log_radius",
        ],
        "families": FAMILIES,
        "feature_only_mlp": baseline,
        "primitive_graph_gcn": graph,
        "graph_confusion_test": confusion(graph_logits, labels, test_idx, len(FAMILIES)),
        "runtime_seconds": round(time.time() - start, 3),
        "note": "Labels come from source layers; raw layer names are excluded from model features.",
    }
    (args.out / "metrics.json").write_text(json.dumps(result, indent=2, default=dict), encoding="utf-8")
    print(json.dumps(result, indent=2, default=dict))


if __name__ == "__main__":
    main()
