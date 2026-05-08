# GNN Primitive Classification Prompt

## Objective

Build a narrow, high-quality graph-learning pipeline for classifying raw
DWG/DXF vector primitives and composed supervectors into representative
architectural elements, while preserving exact vector detail and producing
signals that improve the deterministic modeling engine.

The model is not the whole CAD/BIM system. It is a focused product inside a
larger loop: classify, expose uncertainty, surface useful edge cases, and help
discover rules or forms that improve coverage and consistency.

## Starting Assumptions

- Input may be DWG or DXF.
- Treat all primitives as if they are on one effective layer.
- Do not rely on layer names, groups, or authored object metadata.
- Geometry arrives as an unsorted soup of vectors: lines, arcs, polylines,
  circles, hatches, blocks once exploded, and similar CAD carriers.
- Preserve the original level of vector detail and coordinate accuracy.
- Rasterization may be used for auxiliary context or baselines, but vector
  geometry remains the source of truth.

## Priority 1: GNN Classification

Explore graph methods that classify primitives and supervectors into
representative architectural elements:

- wall
- door
- window
- column
- fixture
- plumbing
- shell element
- room/region boundary
- symbol
- dimension
- annotation/text
- grid
- unknown/noise

The graph should represent primitives, supervectors, faces/regions, and typed
relations such as endpoint proximity, intersection, containment, overlap,
parallel offset, collinearity, closure, repeated spacing, and adjacency.

The immediate question:

> Does graph context improve classification beyond local geometry features and
> raster/convolutional baselines?

## Rule And Form Discovery

The best model output is not only a class label. It should help identify why
the deterministic engine misses coverage or creates inconsistent results.

Useful discoveries include:

- hatch-vs-outline equivalence
- wall continuity patterns
- merge/split/extend candidates
- repeated symbol decomposition forms
- carrier-choice or decomposition-style failure modes
- snap-tolerance or closure failure regimes
- rule candidates that should be promoted into the deterministic engine

The GNN/embedding layer should act as a microscope for the modeling engine:
find recurring structured intent, expose uncertainty, and suggest where expert
annotation or rule updates will matter most.

## Data And Annotation Loop

This domain is not a natural, balanced distribution. Authored CAD/BIM artifacts
are procedural, stylistic, and full of rare edge cases.

Prioritize:

- calibrated uncertainty
- high-recall retrieval of weird or predictive cases
- embedding/prototype memory for recurring failure families
- expert annotation queues that genuinely change rules, labels, or models
- active learning focused on coverage and consistency failures

The loop should be:

```text
engine output
-> graph/features/embeddings
-> classification + uncertainty
-> retrieve similar failures
-> route high-value cases to annotation
-> update model and deterministic rules
-> verify coverage/consistency improvement
```

## Priority 2: Predictive Modeling And Editing

This is secondary until classification and relation structure are stable.

Two later flavors:

1. **System inference inside an architectural shell**
   Infer plausible systems, especially plumbing, from rooms, walls, fixtures,
   shafts, chases, access constraints, and similar graph context.

2. **Edit cascade prediction**
   Given an action such as move, resize, delete, split, merge, reroute, or add,
   predict conflicts, dependencies, and affected elements.

## Non-Goals For Now

- not a full end-to-end BIM generator
- not raster-first floorplan understanding
- not replacing deterministic geometry or validation
- not broad RL/search yet
- not a giant black-box model before the annotation loop is strong

## Success Criteria

A useful first version should:

- ingest DWG/DXF-derived vector primitives
- build a graph over primitives, supervectors, and candidate faces/regions
- preserve exact geometry and provenance
- compare sparse/vector baselines, raster/convolutional baselines, and GNNs
- classify representative elements
- identify low-confidence or high-value annotation cases
- expose interpretable embedding/rule signals
- measurably improve coverage or consistency of the modeling engine

## Short Version

Build small GNN products that classify vector geometry and help discover the
rules, forms, and edge cases needed to make the modeling engine more complete,
consistent, and annotation-efficient.
