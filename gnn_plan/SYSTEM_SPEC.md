# System Spec

This is the concrete buildable system this plan targets, expressed as
contracts, modules, and the smallest first slice. It is the operational
counterpart to [`01_problem_framing.md`](01_problem_framing.md) and
[`02_graph_representations.md`](02_graph_representations.md). Read those
first for *why*; this file states *what*.

## Goal

Turn unsorted DWG/DXF primitive soup into:

1. a typed heterogeneous graph with stable ids,
2. calibrated relation scores over candidate object pairs,
3. typed residual-edit proposals with validator-residual readouts,

while preserving exact vector geometry and provenance.

The system is a research substrate, not a finished product. The success bar
for the first slice is: ingest 4–5 annotated examples, produce one graph per
example, beat a non-GNN baseline on at least one relation that needs
neighborhood context, and land structured edit proposals with calibrated
review bands.

## Module Stack

```
┌────────────────────────────────────────────────────────┐
│ 8. Validator loop          (deterministic, external)   │
├────────────────────────────────────────────────────────┤
│ 7. Structured readout      (typed edit proposals)      │
├────────────────────────────────────────────────────────┤
│ 6. GNN consistency layer   (only after 4-5 are stable) │
├────────────────────────────────────────────────────────┤
│ 5. Prototype/memory head   (low-label regime)          │
├────────────────────────────────────────────────────────┤
│ 4. Pair-relation scorer    (sparse baseline + cal.)    │
├────────────────────────────────────────────────────────┤
│ 3. Graph construction      (typed nodes + edges)       │
├────────────────────────────────────────────────────────┤
│ 2. Object formation        (primitives -> supervectors)│ <- current solver
├────────────────────────────────────────────────────────┤
│ 1. Geometric perception    (parser, snap, closure)     │ <- current solver
└────────────────────────────────────────────────────────┘
```

Layers 1–2 already exist in `tokenize_dxf.py` + `augrade/`. Layers 3–8 are
this plan. The GNN sits at layer 6, not layer 1.

## Data Contracts

All artifacts are versioned by `graph_manifest.json`. Every record carries a
stable id and a provenance pointer.

### `primitives.parquet`

| field | type | notes |
|---|---|---|
| `prim_id` | string | stable hash of canonical entity payload |
| `kind` | enum | `LINE`, `LWPOLYLINE`, `ARC`, `CIRCLE`, `HATCH`, `INSERT`, ... |
| `coords` | json | exact CAD coordinates, no rounding for storage |
| `length`, `area`, `bbox`, `orientation` | numeric | derived |
| `closure_flag` | bool | true if intrinsically closed |
| `source_layer` | string | original layer name (provenance only) |
| `source_kind` | enum | `direct`, `direct_hatch`, `graph_face`, ... |
| `evidence` | json | `{file_path, dxf_handle, conversion_chain}` |

Layer name is stored but never used as a model input in layer-blind
experiments. It is evaluation metadata.

### `supervectors.parquet`

| field | type | notes |
|---|---|---|
| `sv_id` | string | stable hash |
| `composition` | array<prim_id> | child primitives |
| `kind` | enum | `chain`, `closed_loop`, `hatch_boundary`, `panel_cell`, `symbol_group`, `wall_face`, `door_swing`, ... |
| `geometry` | json | canonical polyline, polygon, or compact shape descriptor |
| `local_frame` | json | origin + axis for symmetry handling |
| `features` | json | length, area, perimeter, curvature, aspect ratio, repeated-spacing stats, local density |
| `evidence` | json | links back to primitives |

### `faces.parquet`

| field | type | notes |
|---|---|---|
| `face_id` | string | stable hash |
| `boundary` | array<sv_id> | ordered |
| `area`, `perimeter`, `compactness` | numeric |  |
| `containment` | json | parent and child face ids |
| `holes` | array<face_id> | inner faces if any |

### `edges.parquet`

Pair-feature table over `(left_id, right_id)` where each id may be a
primitive, supervector, or face. Used for both the non-GNN baseline and as
edge features for the GNN.

| field | type | notes |
|---|---|---|
| `edge_id` | string | hash of `(left_id, right_id, relation)` |
| `relation` | enum | typed edges from §02_graph_representations.md |
| `features` | json | gap, intersection type, angle delta, axial overlap, lateral offset, bbox IoU, containment ratio, area ratio, continuation score, crossing penalty, shared boundary length, route cost |
| `family_left`, `family_right` | enum | family inference output (not layer name) |
| `score` | float | filled by scorer |
| `cp_lower`, `cp_upper` | float | conformal review band |
| `decision` | enum | `auto_merge`, `reject`, `review` |

### `annotations.parquet`

Maps incoming labels onto graph ids. See
[`05_annotation_intake.md`](05_annotation_intake.md) for the source schema.

| field | type | notes |
|---|---|---|
| `label_id` | string | from annotation file |
| `unit` | enum | `primitive`, `supervector`, `face`, `component`, `relation`, `edit_event`, `workflow_trace` |
| `target_ids` | array<string> | ids in graph |
| `class` | string | label |
| `confidence` | enum | `high`, `medium`, `speculative` |
| `notes` | text | reviewer comments |

### `graph_manifest.json`

| field | type | notes |
|---|---|---|
| `example_id` | string | one per drawing |
| `created_at` | iso8601 |  |
| `solver_version` | string | tokenize_dxf hash |
| `extractor_version` | string | augrade hash |
| `rewrite_seed` | int | for invariance experiments |
| `tables` | object | hashes of every parquet/json file above |
| `eval_split` | string | `train`, `val`, `test`, `holdout` |

## Module Contracts

### M1. Graph Export

`augrade.graph_export.build_graph(dxf_path, out_dir, manifest_extras)`

Output: `primitives.parquet`, `supervectors.parquet`, `faces.parquet`,
`edges.parquet`, `graph_manifest.json`.

Rules:

- layer-blind: `source_layer` is provenance only.
- exact coordinates preserved in `coords`.
- supervector and face composition is deterministic; same input ->
  byte-identical output (modulo timestamp).
- emits a small SVG overlay for each example for human review.

### M2. Annotation Alignment

`augrade.annotation_align.align(annotations_path, manifest_path)`

Output: `annotations.parquet` keyed by graph ids, plus a residuals report for
any annotations that did not align cleanly.

Rules:

- never silently drop unmappable labels; record them in residuals.
- preserve `confidence` and free-text `notes` verbatim.
- support primitive, supervector, component, relation, edit-event, and
  workflow-trace label units.

### M3. Pair-Feature Baseline

`augrade.pair_score.fit(edges_path, annotations_path, model="logistic"|"gbdt"|"heuristic")`
`augrade.pair_score.predict(edges_path, model_path)`

Output: scores written back to `edges.parquet` plus a calibration plot.

Rules:

- this is the GNN's competitor. It must be present and beaten before the GNN
  ships.
- include conformal calibration so each edge gets `cp_lower`, `cp_upper`,
  and a `decision` band.

### M3.5 Scope Resolver

`augrade.scope.resolve(query, graph_manifest, policy)`

Input: objective, edit proposal, validator residual, annotation, or user
selection.

Output: minimal sufficient subgraph, validators to run, dirty cache keys,
retrieval queries, risk band, and scope certificate.

A scoped subgraph is sufficient when the downstream scorer, validator, or edit
policy returns the same decision/residual/proposal as the full graph within
risk tolerance. It is minimal enough when it preserves that result while
reducing compute, context, and review burden.

Rules:

- start with deterministic dependency closure over objects, relations, faces,
  annotations, schedules, validators, and spatial neighborhoods.
- every scoped call should carry a certificate that says what was included,
  what was excluded, which validators apply, and what evidence would force
  expansion.
- trained scope resolvers can ship only after they beat the deterministic
  baseline on decision fidelity at lower context/compute cost.

### M4. Rewrite Invariance Test

`augrade.rewrites.generate(manifest, kinds=["collinear_split", "carrier_swap", "snap_jitter", "schema_remap", "hatch_to_outline"])`
`augrade.rewrites.score(model, original_manifest, rewritten_manifest)`

Output: stability metrics per relation type, plus a small report listing
relations whose score changes more than a threshold under semantically
equivalent rewrites.

Rules:

- rewrites must be advertised as authored equivalences, not Lie-group
  symmetries.
- failures here are signals that the scorer is over-fit to provenance, not
  a Euclidean equivariance bug.

### M5. Small GNN

`augrade.gnn.fit(graph_dir, model="graphsage"|"gatv2"|"pna"|"hetero", config_path)`
`augrade.gnn.predict(graph_dir, model_path)`

Output: per-node and per-edge predictions, attention weights, and per-relation
delta vs M3 baseline.

Rules:

- ships only when M3 + M4 are stable.
- must report where the GNN improves over the baseline by relation type, not
  only on average.
- must reuse the same calibration head as M3.
- the encoder is pretrained via SSL on held-out HATCH-boundary prediction
  (the headline supervision signal — see [`13_primary_answer.md`](13_primary_answer.md))
  plus rewrite-invariance contrast and masked-relation prediction, before any
  supervised label is shown.
- the encoder is frozen after Phase 4. Per-task heads are small (linear or
  shallow MLP) and trained on programmatic labels first.

### M6. Structured Readout

`augrade.readout.propose_edits(graph_dir, model_path, action_grammar)`

Output: typed residual-edit proposals
`{action, target_ids, expected_impacts, conflicts, validator_delta_before,
validator_delta_after, evidence_links}`.

Action grammar: `move`, `resize`, `attach`, `split`, `merge`, `reroute`,
`delete`, `repair`, `reassign` (see §03_predictive_editing.md).

Rules:

- proposals are validator-facing. They must include a residual readout that
  the validator layer (M7) can verify.
- alternatives are ranked, not collapsed.

### M7. Validator Loop

External and deterministic. Not part of the model.

Inputs: a proposed graph state. Outputs: hard-validity flags, residuals to
threshold, and the evidence pointers behind any failure.

Initial validators:

- closure / winding / planarity
- duplicate-footprint catch
- minimum clearance for known typed relations
- containment consistency

Hooks for future: code/compliance, structural, MEP clearance, fire-rating,
accessibility. These belong outside the learned stack.

## Eval Contract

A change ships only if it improves at least one of these without regressing
the others by more than a stated tolerance:

- HATCH-IoU on a held-out slice (self-supervised shape correctness — the
  load-bearing post-pivot metric)
- relation classification accuracy by type (not only macro F1)
- review-band efficiency: fraction of cases that auto-merge or reject without
  reviewer touch, at fixed precision
- rewrite stability: score variance across the rewrite generators in M4
- residual-edit acceptance: fraction of M6 proposals that the validator
  accepts on the first round
- compute envelope: graph construction, feature generation, scorer
  forward-pass profiled separately

Splits are by drawing or project, never by entity. Random entity splits leak
drafter style and overstate generalization.

## First Slice: Phase 0 Through Phase 2

Ship in this order before adding the GNN:

1. **Phase 0 — Graph Export.** M1 + an example bundle for one airport-doors
   subset. Confirms exact geometry survives the export, supervector and face
   ids are deterministic, and the SVG overlays match the manifest.

2. **Phase 1 — Annotation Alignment.** M2 over the first 4–5 annotated
   examples. Confirms the schema in §05_annotation_intake.md works in
   practice, and produces residuals for any unmappable labels.

3. **Phase 2 — Non-GNN Baseline.** M3 over the typed relations covered in
   §02_graph_representations.md. Produces calibrated scores and a review
   band. This is the bar the GNN has to clear.

Phases 3–5 (rewrite invariance, small GNN, raster context ablation) come
after Phase 2 has a clean baseline and at least one relation that the
baseline gets wrong because it ignores neighborhood context. Phase 5
(predictive editing / M6 + M7) ships once relation scoring is calibrated and
typed actions are stable.

## What Is Out Of Scope For The First Slice

- end-to-end BIM generation
- raster-first floorplan understanding
- learning to replace deterministic geometry, closure, or winding
- broad RL/search over graph edits
- a giant pretrained encoder before a sparse baseline exists
- arbitrary HATCH on non-scoped layers, INSERT explosion, full SPLINE
  handling, exact bulge for all polyline curvature, second-pass merge for
  fragmented wall runs, explicit glazing-grid recovery (these are direct
  solver extensions, not learned components)

## Open Questions To Decide Before Phase 0 Ships

- Are the 4–5 annotated examples primitive-level, supervector-level, or
  mixed? This affects the M2 alignment rules.
- Which workflow exhaust signals are accessible from the source environment:
  edits, rejections, validator residuals, comments, time-to-fix? At least
  one of these should be enumerable for Phase 1.
- What is the target deployment envelope: interactive CPU loop, batch GPU
  review, or both? This determines whether M3/M5 share the same runtime path
  or split.
- Which validators are first-class for the initial scope? Closure and
  containment are already deterministic in the solver; clearance and
  duplicate-footprint catch should be promoted into M7 explicitly.
