# Talk Track

Live-conversation reference. Source for follow-up calls. Detailed material is
in [`13_primary_answer.md`](13_primary_answer.md), [`SYSTEM_SPEC.md`](SYSTEM_SPEC.md),
[`17_dxf_tokenization.md`](17_dxf_tokenization.md), and [`REVIEW_AND_PIVOT.md`](REVIEW_AND_PIVOT.md).

## One-sentence frame

A small heterogeneous GNN as a calibrated ranker over deterministically-formed
supervector candidates, with HATCH companion layers as the self-supervised
correctness signal, validators kept outside the learned stack, and one frozen
encoder reused across many small task heads that a frontier model can call as
tools.

## Three claims to defend live

1. **Geometry stays deterministic.** Closure, winding, family scoping,
   provenance, validators. The take-home solver is the smallest concrete
   instance: stdlib pipeline producing **1169 walls / 764 columns / 304
   curtain-walls** under `pool for geometry, tag for provenance`.

2. **The supervision signal already exists in the data.** HATCH companion
   layers are hidden ground truth. A graph-recovered polygon's IoU against the
   `* HATCH` boundary on the companion layer catches shape correctness that the
   coverage proxy misses by construction. Shown already in `scripts/grid_search.py`
   ranked by HATCH-IoU + coverage.

3. **Real work is residual repair, not whole-scene generation.** The
   first-class actions are typed edits over object/relation state with
   validator residuals readable before and after. Workflow exhaust (edits,
   rejections, repairs, validator failures, time-to-fix) is more valuable than
   static class labels.

## Why we are "extra" — back-pocket

If pushed: standard CAD/graph-ML fails here for four reasons. (1) Layer labels
are unreliable across firms; the repo shows `A-GLAZING MULLION` ≡
`A-GLAZING-MULLION` at ~97% overlap. (2) Per-primitive class is the wrong unit
— walls are carriers, not entities; the 29/29 vs 1/28 merge decomposition in
the repo is the evidence. (3) Coverage-style benchmarks miss shape correctness
by construction; HATCH-IoU catches it. (4) The distribution is authored, not
natural; the right invariance is over authored rewrites (collinear split,
carrier swap, snap jitter, schema remap, hatch ↔ outline), not over data
augmentation.

The on-topic CAD-GNN literature ships models, not systems; benchmarks strip
the structural difficulty; and entity-level random splits leak drafter style.
The useful adjacent literature is molecular GNNs, matryoshka representations,
conformal prediction, DEQ-GNNs, and verifier environments — none about CAD.
The "extra" is necessary composition, not deliberation.

## Slide-level talking points

### Slide 4 (Technical) — "The stack"

M1 geometric perception (parser, snap, closure) → M2 object formation
(supervectors) → M3 graph construction (typed nodes + edges) → **mechanism
boundary** → M4 pair-relation scorer (sparse + conformal — the load-bearing
learned baseline) → M5 prototype / memory (low-label regime) → M6 GNN
consistency (only when M4 leaves a residual) → M7 structured readout (typed
edit proposals) → M8 validator loop (deterministic, **external** to the
learned stack).

Framing line: *numerical computation exposes the mechanism; neural networks
learn the geometry.* Lineage: Shi → Chern → fixed-point class theory →
NMM/DDA → Deep Manifold names what fixed-point engineers already built. See
[the lineage explanation below](#the-lineage-line-back-pocket) if asked.

### Slide 5 (Technical) — "Representation & mechanism"

Four node types: primitive (raw entities), supervector (composed candidates),
face (bounded regions), annotation (text/dims/leaders, layer name as
provenance only). Thirteen typed edges including `near`, `points_to`,
`labels`, `inside`, `bounds`, `parallel_offset`, `continuation`,
`companion_hatch`, `same_symbol_family`, `duplicate_footprint`,
`conflicts_with`. Heterogeneous message passing with relation-typed messages;
R ≈ 2–3 rounds (relation diameter of floor plans is small); GraphSAGE
baseline, GATv2 when small attention helps, PNA only when justified.

Bottom principle: **pool for geometry, tag for provenance.** Pool collapses
rewrite-equivalent inputs to one embedding; tag preserves drafter intent as a
side channel for audit. The same physical thing across rewrites; the
drafter's choice as metadata.

## How we get the supervectors

Supervectors are **deterministic** candidate groupings of primitives.
Over-generate at the candidate stage; the calibrated scorer picks the
survivors. Per-family rules: walls via closed polylines / elongated HATCH /
companion pairs / parallel offsets / face walk; columns via low-aspect
polygons / compact HATCH / column-size CIRCLEs; curtain walls via repeated
narrow rectangles / internal divisions / mullion layer pools; doors and
windows via INSERT or arc-and-line patterns; rooms via face walks on the wall
graph; symbols via canonical shape descriptors; annotations directly. Each
candidate carries provenance (formation rule, member primitives, source
layers) and an exact `geom_id` pointer.

The learned model **scores** candidates; it does not invent them. Domain
knowledge lives in the rules where it can be audited.

## DXF tokenization in one minute

DXF is an ASCII `(group_code, value)` stream. Parse loop is a state machine
that emits entities at `(0, …)` boundaries. Each entity becomes a typed
object with exact float64 coordinates kept in a sibling **geometry pack**
addressed by `geom_id`. The graph tensor never holds raw coordinates —
gradients never flow through the geometry pack. Five gotchas: OCS vs WCS,
recursive HATCH boundary parsing, INSERT explosion (keep both as supervector
AND exploded primitives), encoding (cp1252 default), polyline bulges expanded
to arcs before snapping. Detail in
[`17_dxf_tokenization.md`](17_dxf_tokenization.md).

## Core encoder → subagent → tool

One frozen encoder, many small heads. (1) Pretrain encoder on HATCH-IoU
prediction + rewrite-invariance contrast + masked-relation prediction. (2)
Specialize via small linear or MLP head per task. (3) Calibrate via conformal
prediction on a drawing-level holdout → output is a **band**
(accept / route / reject) with a coverage guarantee, not a softmax. (4)
Package as a JSON-in/JSON-out idempotent tool with a versioned schema and a
`does_not_do` contract. The frontier model spends tokens on judgment —
reading residual reports, proposing rules, deciding what to compile back into
deterministic code — not on rediscovering geometry the engine already
computed.

What changes for a tool-callable subagent vs a background application model:
calibration is mandatory (the LLM uses the band to pick its next action),
errors must be LLM-readable, the schema is strictly semver, and the
`does_not_do` list is the single most undervalued artifact. Without it, the
LLM tries to call the wall-classifier on a curtain wall and produces
confidently-wrong answers. Background pipeline models are looser — the
consumer is downstream code we also wrote.

## The bet ladder

If the conversation turns epistemic:

- **High-confidence (shown in this repo):** HATCH-IoU as supervision signal;
  cross-layer pooling at ~97% overlap; programmatic-vs-contextual merge
  decomposition (29/29 vs 1/28); snap=0.5 + joint coupling on the Pareto
  front.
- **Medium-confidence (extrapolations):** rewrite-invariance auxiliary loss;
  sparse beats GNN on most slices; conformal review bands at M4; drawing-level
  splits change rankings.
- **Speculative (named but flagged as bets):** matryoshka product knobs; SAE
  explainability; verifier environments at scale; objective-loop autonomy
  within a year.

The composition itself is the contribution — not any single architecture
choice. Cross the river by feeling the stones.

## Q1 — GNN experience

> My strongest shipped GNN work is T-UEBA: heterogeneous temporal GNN for
> real-time behavior analytics in tactical networks. PI on graph ontology,
> temporal reconstruction, feature schema, message-passing design, calibrated
> uncertainty, eval, and deployment. The lesson there is that the GNN only
> becomes useful once the world interface is right: typed entities, typed
> relations, update semantics, calibration, hard constraints. Augrade rhymes:
> evolving structured state, hard external constraints, cascading edits, and
> a need for representations that survive real workflow variation.

## Q2 — Frameworks and scale

> Hands-on with PyTorch Geometric, especially custom `MessagePassing`,
> heterogeneous schemas, typed edges, relation-aware attention, and
> production-oriented loops. Snapshot graphs in T-UEBA were hundreds to
> low-thousands of nodes with multi-relational edges. The hard scaling
> problem was repeatedly reconstructing useful graphs from messy event
> streams under inference budget. For Augrade I would not worship the
> framework: I would profile graph construction, feature generation,
> batching, and forward pass separately, and compare PyG-flexible against
> custom-batched-tensor paths only after graph construction cost is
> understood.

## What the GNN should own

- relation propagation over already-formed supervector candidates
- contextual duplicate-vs-distinct decisions
- dependency inference for edits
- route/system plausibility once rooms, shafts, fixtures, and access
  constraints exist
- uncertainty-aware review triage
- annotation-to-object correspondence

## What the GNN should not own

- exact geometry validity
- code/compliance truth
- raw DXF closure and winding
- all object formation from scratch (M2 stays deterministic)
- any auto-apply decision validators cannot bound

## Quick-reference definitions

- **BCE** — binary cross-entropy, `-[y·log(p) + (1−y)·log(1−p)]`. Per-relation
  multi-label binary, not softmax — relations are not mutually exclusive.
- **Conformal calibration** — wraps a scorer with a coverage guarantee:
  emits a prediction *set* with formal probability of containing the true
  label. Outputs become `{accept | route | reject}` bands.
- **L_inv** — `E‖f(x) − f(g(x))‖²` where `g` is an authored rewrite.
  Auxiliary loss to collapse rewrite-equivalent inputs to one embedding.
- **DEQ-GNN** — deep equilibrium GNN, treats message passing as a fixed-point
  iteration. Aligns with the editing-as-fixed-point framing.
- **Kalomaze move** — freeze a large backbone; train a single
  Bradley-Terry density-ratio linear head for edit acceptance.

## The lineage line — back pocket

If asked about *Shi → Chern → fixed-point class theory → NMM/DDA → Deep
Manifold*:

> Shiing-Shen Chern: foundational differential geometry, Chern classes.
> Gen-Hua Shi did two things — his PhD extended Nielsen fixed-point theory by
> introducing fixed-point classes (Chern lineage in topology), and his
> engineering work developed Discontinuous Deformation Analysis and the
> Numerical Manifold Method. NMM uses a dual cover system — a mathematical
> cover (overlapping patches that span the domain) and a physical cover (the
> actual material body with discontinuities) — and runs fixed-point iteration
> until contact statuses converge. The primitive/supervector graph mirrors
> that: primitives are the physical cover, supervectors are the mathematical
> cover (overlapping), message passing is the fixed-point iteration. Deep
> Manifold writing is the modern naming of what NMM has been doing rigorously
> since the 1980s. The lineage is a design tradition we are in dialogue with,
> not an isomorphism we are claiming.

If pushed hard: it is **structural shape borrowed**, not equations. The
predictions cash out — DEQ-friendly, small R, encoder pretrainable
independently of any specific task, discontinuity as feature type.

## Things to avoid saying

- "I will put a GNN on BIM." Wrong frame.
- "I have shipped a BIM GNN." Not true. Be honest about claim boundaries.
- "Layer names are reliable." This repo shows they are not.
- "Raster is enough." Vector-native literature disagrees; HATCH-vs-outline
  evidence shows why.
- "The frame ships; the geometry compounds." Aphorism. Replace with a
  concrete claim — that line is exactly what your friend flagged as slop.

## Open questions to surface (baby version, three)

1. At what grain does the annotation pipeline produce labels — primitive,
   supervector, relation, or edit-event? Decides where supervision lands.
2. Which constraints get first-class deterministic validators —
   code/compliance, structural, MEP clearance, fire-rating, accessibility?
   Decides what may auto-apply.
3. Which authored rewrites are safe to collapse, and which are
   family-conditioned — hatch ↔ outline, carrier swap, collinear split,
   schema remap? Decides the rewrite-invariance scope.

(Deeper list — workflow exhaust, deployment envelope, RL infra appetite — is
in the original deck slide 17 if needed.)

## Anchor citations by claim

| Claim | Strongest anchors |
|---|---|
| Representation-boundary, not architecture-name | Bronstein et al. 2021 (Geometric Deep Learning); Cai et al. 2026 (Scalable Co-Design); Censi 2015 (Mathematical Theory of Co-Design); Lei et al. 2026 (sim-and-real structured representation alignment) |
| Vector-native graph beats raster-first for CAD | Yang et al. CVPR 2023 (VectorFloorSeg); Carrara et al. JCCE 2025 (VectorGraphNET, 1.3M weights vs 35–65M for raster baselines); Liu et al. ICLR 2024 (SymPoint); Wang et al. 2024 (CADSpotting); Fan et al. ICCV 2021 (FloorPlanCAD) |
| Layer priors are leaky in practice | Local repo evidence: `reference/process/layer_normalization_analysis.md`, `reference/research/programmatic_vs_contextual_merges.md` |
| GNN as relational consistency above object formation | Ko & Lee Auto. in Construction 2025 (architectural detail GNN); Knechtel et al. 2024 (self-constructing graph for floor plans); Hu et al. 2025 (planar duality, vertex-edge-face message passing); MDPI 2024 (BIM element classification with GNN); Wang et al. MDPI 2022 (IFC BIM space function GNN) |
| Edit-cascade prediction needs graph context | Sun et al. 2023 (MEP clash context GCN); Kipf et al. ICML 2018 (Neural Relational Inference); IFC properties validation deep GNN |
| Calibration matters more than F1 in low-label regime | Vovk, Gammerman, Shafer (Algorithmic Learning in a Random World); local merge-lab calibration evidence |
| Residual edit framing | Goel et al. ICLR 2026 (any-subgroup equivariance); Wang et al. 2026 (Temporal Straightening for Latent Planning); Petrenko et al. ICLR 2026 (Entropy-Preserving RL) — all later-stage |

Detailed citations live in [`04_research_map.md`](04_research_map.md). The
operational reading is in [`SENSEMAKING.md`](SENSEMAKING.md).

## Closing line

> Build the smallest stack that survives contact with the product loop —
> deterministic geometry, stable object identity, typed relations, calibrated
> learned residual scoring, deterministic validators — then add learned
> components only where the deterministic scaffold leaves a real residual.
