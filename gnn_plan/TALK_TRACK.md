# Talk Track

Single-page version of the live conversation. Source for the follow-up call.
Detailed material is in the numbered plan, the sensemaking workbenches, and
the research map.

## One-Sentence Frame

Augrade is a representation-boundary problem first and a GNN problem second:
choose where geometry, object state, typed relations, learned residual scoring,
and deterministic validators live in the stack, then put each model class only
where it earns its keep.

## Three Claims I Want To Defend Live

1. **Geometry stays deterministic.** Closure, winding, family scoping,
   provenance, validators. The take-home solver is the smallest concrete
   instance of this layer; it produces 1158 walls / 764 columns / 304
   curtain-walls under a stdlib pipeline with `pool for geometry, tag for
   provenance` as the rule.

2. **Object formation is a graph problem above geometry, not a perception
   trick.** Primitives → supervectors → faces → components → assemblies. The
   GNN belongs in the relational consistency layer above object formation and
   below validators. CAD-domain evidence: VectorGraphNET, VectorFloorSeg,
   FloorPlanCAD line-level supervision, Ko & Lee detail-drawing GNN, and the
   IFC BIM space-function GNN line of work.

3. **Real work is residual repair, not whole-scene generation.** The system's
   first-class actions should be typed edits over object/relation state, with
   validator residuals readable before and after each action. Workflow exhaust
   (edits, rejections, repairs, validator failures, time-to-fix) is more
   valuable than static class labels.

## What I Would Say For Q1 (GNN Experience)

> My strongest shipped GNN work is T-UEBA: heterogeneous temporal GNN for
> real-time behavior analytics in tactical networks. PI on graph ontology,
> temporal reconstruction, feature schema, message-passing design, calibrated
> uncertainty, eval, and deployment. The lesson there is that the GNN only
> becomes useful once the world interface is right: typed entities, typed
> relations, update semantics, calibration, hard constraints. Augrade rhymes:
> evolving structured state, hard external constraints, cascading edits, and a
> need for representations that survive real workflow variation.

## What I Would Say For Q2 (Frameworks And Scale)

> Hands-on with PyTorch Geometric, especially custom MessagePassing,
> heterogeneous schemas, typed edges, relation-aware attention, and
> production-oriented loops. Snapshot graphs in T-UEBA were hundreds to
> low-thousands of nodes with multi-relational edges. The hard scaling
> problem was repeatedly reconstructing useful graphs from messy event
> streams under inference budget. For Augrade I would not worship the
> framework: I would profile graph construction, feature generation, batching,
> and forward pass separately, and I would compare PyG-flexible against
> custom-batched-tensor paths only after graph construction cost was
> understood.

## What The GNN Should Own

- relation propagation over already-formed objects
- contextual duplicate-vs-distinct decisions
- dependency inference for edits
- route/system plausibility once rooms, shafts, fixtures, and access
  constraints exist
- uncertainty-aware review triage

## What The GNN Should Not Own

- exact geometry validity
- code/compliance truth
- raw DXF closure and winding
- all object formation from scratch
- replacing the validator boundary

## Anchor Citations By Claim

| Claim | Strongest anchors |
|---|---|
| representation-boundary, not architecture-name | Bronstein et al. 2021 (Geometric Deep Learning); Cai et al. 2026 (Scalable Co-Design); Censi 2015 (Mathematical Theory of Co-Design); Lei et al. 2026 (sim-and-real structured representation alignment) |
| vector-native graph beats raster-first for CAD | Yang et al. CVPR 2023 (VectorFloorSeg); Carrara et al. JCCE 2025 (VectorGraphNET, 1.3M weights vs 35–65M for raster baselines); Liu et al. ICLR 2024 (SymPoint); Wang et al. 2024 (CADSpotting); Fan et al. ICCV 2021 (FloorPlanCAD) |
| layer priors are leaky in practice | Local repo evidence: `reference/process/layer_normalization_analysis.md`, `reference/research/programmatic_vs_contextual_merges.md` |
| GNN as relational consistency above object formation | Ko & Lee Auto. in Construction 2025 (architectural detail GNN); Knechtel et al. 2024 (self-constructing graph for floor plans); Hu et al. 2025 (planar duality, vertex-edge-face message passing); MDPI 2024 (BIM element classification with GNN); Wang et al. MDPI 2022 (IFC BIM space function GNN) |
| edit-cascade prediction needs graph context | Sun et al. 2023 (MEP clash context GCN); Kipf et al. ICML 2018 (Neural Relational Inference); IFC properties validation deep GNN |
| calibration matters more than F1 in low-label regime | Vovk, Gammerman, Shafer (Algorithmic Learning in a Random World); local merge-lab calibration evidence |
| residual edit framing | Goel et al. ICLR 2026 (any-subgroup equivariance); Wang et al. 2026 (Temporal Straightening for Latent Planning); Petrenko et al. ICLR 2026 (Entropy-Preserving RL) — all later-stage |

Detailed citations live in [`04_research_map.md`](04_research_map.md). The
operational reading is in
[`notes/augrade_representation_reading_notes.md`](notes/augrade_representation_reading_notes.md).

## Things To Avoid Saying

- "I will put a GNN on BIM." That is the wrong frame and the cited literature
  already shows the harder questions are representation choice, calibration,
  and validator boundary.
- "I have shipped a BIM GNN." I have not. The repo is a deterministic geometry
  tokenizer plus a research extension. Be honest about claim boundaries.
- "Layer names are reliable." This file shows they are not. The honest claim
  is that layer schema is provenance, not a model input.
- "Raster is enough." The vector-native CAD literature already disagrees, and
  the local HATCH-vs-outline evidence shows why.

## Open Questions Worth Surfacing

- Which authored rewrites do they consider in scope for invariance: collinear
  split/merge, carrier swap, snap perturbation, layer schema remap,
  HATCH-vs-outline carrier?
- What does the annotation pipeline produce: primitive-level, supervector,
  component, relation, edit-event, or workflow trace?
- Where is workflow exhaust captured today: revision history, validator
  residuals, designer comments, time-to-fix? Anything that exists is gold for
  later supervision.
- What is the deployment envelope: interactive CPU loop, batch GPU review,
  both? That decides PyG vs custom batched tensor paths.
- Which constraints are first-class: code/compliance, structural, MEP
  clearance, fire-rating, accessibility? Validator boundary should be
  enumerated, not hand-waved.

## Closing Line

> I would build the smallest stack that survives contact with the product
> loop: deterministic geometry, stable object identity, typed relations,
> calibrated learned residual scoring, and explicit validators. Then I would
> add learned components only where the deterministic scaffold leaves a real
> residual problem. That gives the model class room to evolve without
> rewriting the world interface every time.
