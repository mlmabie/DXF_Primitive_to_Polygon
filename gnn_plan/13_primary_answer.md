# Primary Answer: Training A GNN Over DXF/DWG Vector Soup

Last revised: 2026-05-12 (PDT), after the external review and the post-pivot conversation that this document now consolidates.

## The one-sentence answer

**Train a small heterogeneous GNN as a calibrated ranker over deterministically-formed supervector candidates, with HATCH companion layers as the self-supervised correctness signal, validators kept outside the learned stack, and one frozen encoder reused across many small task heads that a frontier model can call as tools.**

The rest of this document is the decomposition of that sentence into mechanisms, contracts, and falsifiers.

## Why be extra — by-the-book is insufficient

The standard CAD/graph-ML pipeline (get labels → pick an architecture → train → report on a held-out split → ship) fails on this problem for four concrete reasons:

1. **Layer-name labels do not exist for the real distribution.** Cross-firm and cross-drafter naming is unreliable. This repo already shows it: `A-GLAZING MULLION` (LINE-only) and `A-GLAZING-MULLION` (LWPOLYLINE-only) are the same physical mullions at ~97% spatial overlap. Any model that uses layer names as supervision learns punctuation, not architecture.
2. **The supervised task masks the harder problem.** "Classify this primitive as wall" assumes there is such a thing as the wall primitive. Walls are *carriers* — sometimes hatch boundaries, sometimes outline lines, sometimes 2-line offsets, sometimes fills on a separate layer. The two-stage merge decomposition in this repo (29/29 curtain-wall merges programmatic from provenance alone, 1/28 wall merges) is direct evidence the per-primitive label is the wrong unit.
3. **The benchmark metric does not match the production cost function.** Per-primitive accuracy ignores false merges that destroy drafter work. The source-entity coverage proxy this repo already ships "misses *shape* correctness by construction" — HATCH-IoU catches it; the standard metric does not.
4. **The input distribution is authored, not natural.** ML papers assume IID. CAD is authored procedurally with house-style conventions and decade-long version drift. There is no "more data" fix — the representation must be stable under *authored* rewrites (collinear split, carrier swap, snap jitter, schema remap, hatch ↔ outline). That is a different ask than augmentation.

## Why the on-topic papers are not prescriptive

CAD-GNN literature (FloorplanCAD, BIM-graph papers, raster-then-graph hybrids) has three structural problems:

1. **Papers ship models, not systems.** A model that wins on FloorplanCAD does not carry the validator boundary, the rewrite-stability tests, the workflow-exhaust loop, or the rule compiler. Adopting the model imports a benchmark frame that does not match a production constraint.
2. **Benchmarks strip out the structural difficulty.** Hand-labeled entity-level ground truth filters out the hardest production cases — multi-carrier walls, schema drift across firms, hatch-vs-outline ambiguity, T-junctions that change meaning.
3. **Entity-level random splits leak drafter style.** A model that memorizes "this drafter uses LINE-only mullions" appears to generalize within a drawing but breaks across firms.

The most useful adjacent literature is *not* the on-topic CAD papers. It is molecular GNNs (atom-bond analogy), matryoshka representations (one model, many surfaces), conformal prediction (calibrated bands), DEQ-GNNs (fixed-point iteration), and verifier environments (validators as reward rubrics). None of those are about CAD; all are load-bearing here. *That* is where the "extra" comes from: necessary composition, not deliberation.

## The supervision signal — HATCH-IoU as hidden ground truth

The bet is that the data already contains a self-supervised correctness signal nobody is using:

> For walls and columns, fill-vs-outline pairs like `A-EXTERNAL WALL` / `A-EXTERNAL WALL HATCH` describe the same physical element with two independent carrier types. A graph-recovered polygon's IoU against the `* HATCH` boundary on the companion layer is a self-supervised correctness signal that captures *shape* correctness — which the source-entity coverage proxy misses by construction.

The take-home solver already produces this signal via the snap × joint grid search ranked by HATCH-IoU + coverage (`scripts/grid_search.py`). The Pareto-front result is recorded in `reference/process/topology_coupling_experiment.md`. This is the one bet with empirical evidence in this repo today.

Training procedure: at SSL time, strip companion `* HATCH` primitives from the input graph for the slices where the model predicts a supervector boundary. Score predicted polygons by IoU against the held-out HATCH. Without that step the model just retrieves the HATCH from its input — the held-out-channel discipline below is the safeguard.

## Supervector formation — how we get the candidates

Supervectors are **deterministic** candidate groupings of primitives. The learned layers (M4+) do not invent them; they score, merge, split, and route. The principle is **over-generate then score**: recall at the candidate stage is the formation rules' job; precision is the model's job.

Each candidate carries provenance and exact-geometry pointers:

```python
supervector = {
    id:                 stable across runs,
    kind:               wall_candidate | column_candidate | curtain_wall_candidate | ...,
    member_primitives:  [primitive_id, ...],
    source_layers:      [layer_name, ...],          # provenance only, never a feature
    geometry_proxy:     {bbox, area, perimeter, ...},
    geom_id:            reference into the exact-coord geom pack,
    formation_rule:     HATCH_BOUNDARY | PARALLEL_OFFSET | FACE_WALK | ...,
    confidence_prior:   rule-based scalar,
    overlaps:           [other_supervector_id, ...]
}
```

Formation rules per family:

**Walls.** Closed LWPOLYLINE with high aspect → wall candidate. Elongated HATCH boundary → wall candidate (strongest rule when present). Companion-layer pair (`A-EXTERNAL WALL` ↔ `A-EXTERNAL WALL HATCH` within IoU threshold) → wall candidate with the pair edge pre-tagged. Parallel-offset pair (two parallel lines at consistent offset within a thickness band) → wall-mass candidate. Bounded faces in the snapped endpoint graph with high aspect → wall-region candidate (the existing solver's main path).

**Columns.** Closed polygon with low-aspect bbox + small area → column candidate. Compact HATCH region → column candidate. CIRCLE or short closed polyline in column-size band → column candidate. `S-COLUMN` / `S-COLUMN HATCH` companion pair → column candidate.

**Curtain walls.** Repeated narrow rectangles with consistent spacing (mullion + panel pattern) → curtain-wall candidate. Long thin closed polyline with internal parallel divisions → curtain-wall candidate. Cross-layer pool of `A-GLAZING MULLION` / `A-GLAZING-MULLION` variants → mullion supervector.

**Doors / windows / fixtures.** Named INSERT before explosion → named symbol supervector. Arc + flanking lines at a wall break → door-swing candidate. Two short parallel lines bridging a wall gap → window candidate.

**Faces / rooms / regions.** Bounded faces in the wall-supervector graph → room candidate. HATCH boundary on a room-fill layer → room candidate. Containment relationships across face candidates produce nested face supervectors.

**Symbols (repeated motifs).** Clusters of primitives sharing a canonical shape descriptor (turning function, normalized point cloud) → `same_symbol_family` supervector. Named INSERTs sharing a block name → named-symbol-family supervector.

**Annotations.** TEXT / MTEXT / DIMENSION / LEADER entities → annotation supervectors directly, with `points_to` candidate edges to spatial neighbors.

Three properties matter: candidates **overlap** (same primitive can belong to multiple supervectors — the NMM cover-system analogy: Numerical Manifold Method's dual mathematical/physical cover, see [`_prep/TALK_TRACK.md`](_prep/TALK_TRACK.md)), candidates carry **provenance** (formation rule, member primitives, source layers, all auditable), and IDs are **stable** (re-running formation on the same input produces the same IDs so the per-node cache can invalidate locally on edits).

## The tensor

One drawing is a heterogeneous graph **plus a parallel geometry pack**. The graph is what the GNN sees; the geometry pack is what validators and shape-correctness signals see. They are never the same tensor, and gradients never flow through the geometry pack.

```
graph = {
  nodes: {
    primitive:   (N_p, D_p)   D_p ≈ 24    # features only, no (x, y)
    supervector: (N_s, D_s)   D_s ≈ 32
    face:        (N_f, D_f)   D_f ≈ 16
    annotation:  (N_a, D_a)   D_a ≈ 16
  },
  edges: {                                # 13–15 typed relations
    (primitive,   near,              primitive):  (2, E), edge_attr (E, D_e ≈ 4)
    (primitive,   touches,           primitive):  ...
    (primitive,   parallel_offset,   primitive):  ...
    (primitive,   continuation,      primitive):  ...
    (primitive,   companion_hatch,   primitive):  ...
    (supervector, bounds,            face):       ...
    (primitive,   inside,            face):       ...
    (annotation,  points_to,         primitive | supervector | face):  ...
    (annotation,  labels,            primitive | supervector | face):  ...
    (supervector, same_symbol_family, supervector): ...
    (supervector, duplicate_footprint, supervector): ...
    (supervector, conflicts_with,    supervector): ...
    (insert,      parent_of,         primitive):  ...
  },
  geom_ids: (N_p,)                        # int32 pointers into geom_pack
}

geom_pack = {
  geom_id -> {
    kind: enum,
    coords: float64 array,                # exact, never normalized
    bulges: float64 array,                # for polylines
    vertices: float64 array,              # for hatches
    bbox: float64[4],
    handle: str,                          # DXF handle, stable
  }
}
```

PyG `HeteroData` works directly — one `x` tensor per node type, one `edge_index` plus optional `edge_attr` per relation. The geometry pack is a sibling object addressed by `geom_id` (dict or columnar Arrow table).

### Node features

**Primitive** (`D_p ≈ 24`): one-hot kind (LINE / ARC / LWPOLYLINE / CIRCLE / HATCH / TEXT / DIMENSION / INSERT) → 8; `log_length`, `log_bbox_diag`, `bbox_aspect`, `curvature_proxy`, `segment_count`, `has_bulge` → 6; carrier-style buckets (dash class, weight bucket, color bucket) → 4 (provenance only, masked at train time); structural flags (`is_companion_hatch`, `exploded_from_insert`, `closed`) → 3; learned positional invariants (snap-graph degree, T-junction multiplicity, parallel-offset partner count) → 3.

**Supervector** (`D_s ≈ 32`): primitive composition counts per kind (bucketed) → 8; pooled geometry stats (`log_area`, `log_perimeter`, `closure_quality`, `winding_sense`, `T_junction_count`, `aspect`) → 6; topology (cycle indicator, boundary continuity, junction count, hole count) → 4; provenance (bag-of-layers low-dim embedding, `direct_hatch_flag`, `direct_polyline_flag`) → 6; carrier mixture (entropy across primitive kinds) → 2; reserved → 6.

**Face** (`D_f ≈ 16`): area, perimeter, aspect, compactness, log of each, cardinality buckets, enclosed-primitive counts.

**Annotation** (`D_a ≈ 16`): kind, text-class bucket, character-count bucket, font-size bucket, anchor type, geometric flags.

What is **not** in node features: absolute coordinates, layer name strings, drafter-correlated continuous values.

### Edge features

Edge attributes are small (`D_e ∈ {2, 4, 6}`) and pairwise — invariant under global translation, rotation, and reflection by construction:

- `near` / `touches`: gap distance, log distance, gap angle, tolerance bucket.
- `parallel_offset`: offset distance, parallelism score, length ratio.
- `continuation`: direction cosine, gap, chain position.
- `companion_hatch`: IoU against companion, boundary length ratio.
- `points_to` / `labels`: leader length, anchor angle, text-height ratio.
- `bounds`: coverage fraction of boundary.
- `inside`: containment margin.

Absolute world coordinates never enter the message-passing tensor through any path.

## Geometry fidelity while warping relational space

Two coordinate systems exist and they do not mix:

1. **Latent relational space** — node embeddings live here. Evolve through message passing, support InfoNCE contrast over rewrite orbits, used for retrieval/classification/ranking. Gradients flow freely.
2. **Euclidean geometry space** — exact float64 coordinates from the DXF parse. Used by validators (closure, winding, containment, clearance) and by the HATCH-IoU computation. Gradients **never** flow here.

The bridge is `geom_id`. When the model proposes "supervector S25 is a wall," it does not propose new coordinates — it points to existing primitive geom_ids and asserts a grouping. The validator pulls exact coordinates from the geom pack and checks. If the model proposes an edit, the edit is a typed action over geom_ids ("merge geom_id 142 and 187 by extending endpoints"), not a coordinate regression. The post-edit geometry is then re-parsed by the deterministic engine.

Trivial Euclidean symmetries (translation, rotation, reflection) are not learned — they are designed away by using only pairwise features. The authored rewrites that matter (collinear split, carrier swap, snap jitter, schema remap, hatch ↔ outline) are **categorical equivalences**, not group actions; those are what the invariance loss `L_inv = E‖f(x) − f(g(x))‖²` is trying to collapse.

## Derived-feature discipline — no leakage, no lookahead

The classic engineered-feature trap is computing a feature that quietly encodes the label. Four rules:

1. **Causal lineage rule.** Every feature carries a provenance manifest: `f_i: depends_on={raw_fields...}, derived_at=preprocess_step_k, label_free=True`. A feature is admissible only if it can be computed from raw geometry alone with no access to labels, held-out HATCH boundaries (when those are the SSL target), or validator outputs computed using labels.
2. **Train/inference symmetry.** Anything the engine cannot compute at inference time on a brand new drawing cannot be a training feature. Snap-graph degree: fine. Neighborhood wall density from gold labels: forbidden.
3. **Drawing-level splits.** Random entity splits leak drafter style. Splits are by drawing or project; across firms where possible. Reported metrics on entity splits are diagnostics, not headline results.
4. **Held-out-channel discipline for SSL.** When HATCH-IoU is the supervision target, the companion `* HATCH` layer is stripped from the input graph for the prediction slice. The annotation-to-object work needs the same: when predicting which primitive an annotation refers to, the annotation's authoring proximity should be masked.

A `features_manifest.json` per drawing records every feature's lineage, and the training harness asserts every feature in the tensor has an entry with `label_free=True`.

## Core self-supervised tasks

1. **Held-out HATCH-boundary prediction.** Strip companion `* HATCH` primitives; predict the boundary; score IoU against the held-out HATCH. The headline signal.
2. **Rewrite-invariance contrast.** Apply one of the five authored rewrites; minimize `‖f(x) − f(g(x))‖²` for safe rewrites; push apart across different drawings (InfoNCE). The same loss flags which rewrites are unsafe — those become "family-conditioned" labels.
3. **Masked relation prediction.** Mask ~15% of typed edges; predict type from neighborhood. Dense, cheap, pretrains relation embeddings.
4. **Companion-layer existence.** Binary classifier: does a `* HATCH` companion exist somewhere in the drawing for this element family? Sharpens the bridge from local to global.
5. **Closure consistency.** Discriminate real closed faces (from the solver) from random cycles. Calibrates boundary-formation.

## Core supervised tasks

1. **Pair-relation scoring** (the load-bearing supervised baseline). For each typed relation (`should_merge_into_same_supervector`, `parallel_offset`, `T_junction`, `collinear_split`, `hatch_outline_pair`), train a calibrated head on (primitive, primitive) pairs with binary cross-entropy. Programmatic labels from the deterministic solver where confident; conformal calibration on a drawing-level holdout produces auto-accept / route / reject bands. Multi-label binary, not softmax — relations are not mutually exclusive.
2. **Primitive class classification.** ~11–13 way over wall / column / curtain_wall / door / window / fixture / plumbing / shell / room / symbol / dimension / annotation / grid / unknown. Programmatic labels from the deterministic solver where confident; expert labels routed through the review loop for the rest.
3. **Supervector class classification.** Same taxonomy at the composed-unit level. Often the more useful prediction because it pools rewrite variants.
4. **Annotation-to-object correspondence.** Given an annotation and a small candidate-target set (within geometric range), predict the referent. The Paper 1 contribution.
5. **Closure-repair action classification.** Given a near-closed cycle with a small gap, predict which deterministic repair action (extend, snap, bridge, ignore) the validator would accept. Labels from validator decisions on perturbed inputs — fully programmatic.

Deployment order: (1) pair-relation scoring ships first; (2) HATCH-IoU SSL pretrains the encoder before any supervised label; (3) supervector classification piggybacks on the pretrained encoder; (4) annotation-to-object follows once the supervector layer is calibrated; (5) closure-repair becomes the bridge to Phase 5 typed-edit actions.

## From core model to subagent

The frontier-model-callable surface is a four-stage pipeline:

1. **Train the core encoder.** Heterogeneous GNN, R ≈ 3 rounds. Pretrained via SSL on HATCH-IoU + rewrite-invariance contrast + masked-relation. Output: per-node embedding (~256d). **Frozen after Phase 4.** One-time investment.
2. **Specialize with small heads.** Freeze the encoder; attach task-specific heads (linear, small MLP, or BT density-ratio for the kalomaze ranker: freeze a large backbone and train one Bradley-Terry linear head for edit acceptance, see [`_prep/TALK_TRACK.md`](_prep/TALK_TRACK.md)). Each is a few thousand to a few million parameters and trains in minutes on commodity hardware. Most labels are programmatic.
3. **Calibrate.** Conformal prediction on a drawing-level holdout. Output is not a probability; it is a **band**: `{accept | route_to_expert | reject}` with a formal coverage guarantee. The risk band is the published contract.
4. **Package as a tool.** JSON input/output schema, idempotent, documented `does_not_do` contract, versioned HTTP/RPC. This is the surface Opus or GPT-5.5 actually calls.

### What we maintain — tool-callable vs background

| Concern | Tool-callable subagent (LLM calls it) | Background application model |
|---|---|---|
| Caller | Frontier LLM during reasoning | Pipeline code on a trigger |
| Input shape | Small JSON, schema-validated | Bulk Arrow / tensor |
| Output shape | Small JSON, calibration band as first-class field | Bulk Arrow / tensor, scores |
| Latency | < 100 ms preferred | Batched, throughput-optimized |
| Calibration | **Mandatory** — LLM uses the band to decide next action | Nice to have |
| Error semantics | Errors must be LLM-readable | Retry / log / queue |
| Versioning | Strict semantic; breaking changes are major bumps | Internal versioning sufficient |
| `does_not_do` contract | **Mandatory** | Implicit |
| Test suite | Tripwire (input → expected output) cases gate every retrain | Validation metric per batch |
| Frontier-LLM integration tests | Yes — verify tool still works when called by next LLM version | N/A |
| Idempotency | **Mandatory** for safe LLM retries | Often not enforced |

The headline: tool-callable subagents cost more to maintain because the consumer reasons over the contract, not just consumes a score. The `does_not_do` list is the most undervalued artifact — without it the LLM will try to use the wall-classifier on a curtain wall and produce confidently wrong answers. The same encoder serves both modes; the tool surface is just a wrapped, calibrated, schema-validated head with a clean API.

## What the GNN should own — and own falsifiably

The GNN earns its place only when, on a drawing-level holdout, it improves at least one context-heavy relation or annotation-to-object task **over the sparse pair-relation baseline at the same calibrated review band**. If sparse wins, ship sparse.

What it should own:
- supervector and primitive classification when local composition is ambiguous,
- annotation-to-object correspondence (tags, dimensions, leaders, room names),
- relation recovery where geometry alone is underdetermined,
- uncertainty surfacing for the annotation queue.

What it should not own:
- exact geometry validity,
- closure / winding truth,
- code/compliance truth,
- whole-scene generation,
- any auto-apply decision that validators cannot bound.

Closure, containment, clearance stay outside the learned stack as deterministic validators that decide what may auto-apply.

## The bet / extrapolation / unknown ladder

Pragmatist epistemics. Each claim goes on a rung; each rung is treated differently in conversation, in the deck, and in the experiment plan.

### High-confidence (shown in this repo today)
- HATCH companion layers as hidden ground truth; HATCH-IoU as a self-supervised correctness signal.
- Programmatic-vs-contextual merge decomposition (29/29 curtain-wall programmatic; 1/28 wall programmatic).
- Cross-layer pooling on canonical-layer-equivalent variants (~97% spatial overlap evidence on the GLAZING MULLION case).
- Snap = 0.5 + T-junction coupling on the Pareto front (grid_search CSV + Pareto SVG).
- "Pool for geometry, tag for provenance" as a defensible engineering principle.

### Medium-confidence (extrapolations that follow)
- Authored-rewrite-invariance as an auxiliary training loss. The five rewrites are real; the `L_inv` collapse is the unverified part.
- Sparse pair-relation baselines beat GNNs on most slices; GNNs earn their keep only on context-heavy residuals.
- Calibrated conformal review bands at M4 enable auto-accept / reject / route.
- Drawing-level splits change rankings vs random entity splits.

### Speculative (named but flagged as bets, not commitments)
- Matryoshka embeddings buy real product knobs (cache vs routing vs offline).
- SAE bridge gives explainability that compiles back into engine rules.
- Verifier environments + hosted RL improve search-space coverage in Phase 5.
- Objective-loop autonomy reaches the "expert reviews summary" mode within a year.

The discipline is: lead with rung 1, label rung 2 honestly, isolate rung 3 behind its own gates. The composition itself is the contribution.

## Robust exemplar partition

The system separates cases safe to learn from as truth from cases that should remain uncertain. Four lanes:

| Lane | Meaning | Action |
|---|---|---|
| Gold | expert-confirmed, validator-consistent, rewrite-stable | train / eval / rule mining |
| Silver | strong weak supervision, stable across checks, no contradiction | train with lower weight |
| Amber | plausible but ambiguous or under-scoped | review / active learning |
| Red | conversion error, contradiction, invalid geometry, or out-of-distribution | do not train as truth; fix pipeline or quarantine |

A robust exemplar is not merely a high-confidence model prediction. It should pass several evidence tests: stable id and provenance, exact geometry preserved, label aligned with deterministic geometry or metadata, validator-consistent relation, label survives rewrite perturbations, agreement across at least one independent signal (annotation, weak label, text/tag semantics, rendered view, expert review, or validator residual), low or explainable disagreement with sparse baseline, accepted by expert or repeatedly confirmed by workflow outcomes.

A non-robust case carries one or more of: uncertain DWG conversion fidelity, missing handles/text/colors/blocks, label depending strongly on layer conventions, multiple plausible targets, weak or contradictory annotation, rewrite perturbation changes prediction, sparse-baseline / GNN disagreement without validator support, low conformal confidence, no expert/workflow confirmation. These cases are not discarded — they are high-value review and active learning material.

## Evaluation

Drawing-level splits, never entity splits. Random entity splits leak drafter style and repeated symbols.

Headline metrics:
- supervector macro-F1
- relation macro-F1 by relation type
- annotation-to-object accuracy
- conformal coverage at the published risk band
- review-load reduction at fixed precision
- rewrite stability (score variance under authored rewrites)
- validator residual reduction
- HATCH-IoU on a held-out slice (self-supervised correctness)

A change ships only if it improves at least one of these without regressing the others by more than a stated tolerance.

## Gaps to close

After the pivot, the load-bearing gaps are:

1. **Annotation semantics.** Distinguish architectural labels, schedule tags, dimensions, ordinary CAD text, and reviewer markup.
2. **Gold labels at supervector and annotation-to-object levels** for the first ~20 drawings.
3. **Rewrite benchmark.** Authored equivalence transforms with a metric for whether labels survive.
4. **Calibration set.** Held-out drawings for conformal / review-band calibration.
5. **Validator inventory.** Enumerate which residuals are exact today and which are future policy.

## Final form

> Train the GNN as a small, calibrated, frozen-encoder ranker over deterministically-formed supervector candidates. Pretrain on HATCH-IoU and rewrite invariance. Specialize with small heads per task, calibrate via conformal prediction, expose each head as a tool with a `does_not_do` contract. Keep validators deterministic and outside the learned stack. Partition examples into gold / silver / amber / red. The system composition is the contribution: it lets future architecture wins compound without pretending any single architecture choice is already proven.
