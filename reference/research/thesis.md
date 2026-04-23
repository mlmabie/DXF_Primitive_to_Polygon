# Thesis

Consolidated from the earlier research notes and the findings that survived contact with the file.

## Abstract

This project treats the DXF take-home as a structured representation problem rather than a bag-of-primitives cleanup exercise. Architectural drawings are authored with clean intent, so the right first move is to recover the low-entropy scaffold: closure, typed polygon formation, and provenance-preserving alignment across drafting variants. The direct solution here is geometric and reproducible: extract closed carriers, recover additional faces from a snapped endpoint graph, and retain `source_layers` as residual provenance. The exploratory work matters because it clarifies which irregularities are semantic and which are just authored representation choices. That same distinction defines the future ML substrate: pairwise merge relations, rewrite-invariant training objectives, and reviewer-facing annotation workflows. If the problem starts turning into brittle hand-negotiation with edge cases, that is a sign to move upward into scalable learned methods rather than keep hard-coding exceptions.

## The Task

**Input.** Roughly 67,000 DXF primitives (`LINE`, `ARC`, `LWPOLYLINE`, `CIRCLE`, `ELLIPSE`, `HATCH`, `POLYLINE`) across roughly 111 layers, with no grouping metadata. A wall or column is not stored as an object. It is only implied by drafting primitives that a human perceives as belonging together.

**Output.** Closed polygons grouped by element type:

- walls
- columns
- curtain walls

Each output polygon also retains the raw drafting layers it came from.

**Difficulty.** The object-level footprint is not in the file. It has to be reconstructed from primitive-level authoring work. The variability is not sensor noise. It is authored choice about:

- layer schema
- carrier type (`LINE`, `LWPOLYLINE`, `HATCH`, `CIRCLE`, ...)
- decomposition granularity
- local junction policy

## The Approach

Treat the DXF as a tokenization problem over geometry.

| Concept | DXF form |
|---|---|
| characters | primitives |
| closure rules | endpoints connect, CW winding |
| tokens | closed polygons |
| typed semantics | family inference from layer priors + family-relevant geometry |
| residual metadata | `source_layers` attached to every polygon |

The implementation is deliberately low-entropy:

- extract already-closed carriers directly
- flatten the rest into segments
- snap endpoints
- walk bounded faces on the resulting planar graph
- keep the faces that pass family-specific geometric filters
- preserve provenance

No learned components are required for the direct take-home solution.

## Framing: Structured Representation Alignment

The framing that fits this problem most closely is **structured representation alignment**: a useful representation must do two things at once.

- **cross-domain alignment**: pull together views that describe the same underlying object despite surface differences
- **domain discernibility**: preserve which source the view came from, so the system can know when to trust or distrust it

That is exactly the move this repo makes at the drafting level.

- Different layer variants, carrier choices, and decomposition conventions are different “domains.”
- The geometric pipeline aligns them when they describe the same underlying element.
- The system still preserves provenance through `source_layers`, `source_kind`, and layer/provenance analysis.

The practical slogan used elsewhere in the repo is:

> pool for geometry, tag for provenance

### Operational Test: Inner-Product Geometry

“Structured representation alignment” is the frame, but the operational question is:

> what representation makes compatible merges close and incompatible merges far under the drafting-rewrite symmetries the file actually exhibits?

The relevant symmetries here are not viewpoint transformations. They are authored rewrites such as:

- split/merge collinear segments
- swap direct-vs-graph-face carriers
- perturb the snap lattice within tolerance class
- remap between companion layer schemas

A useful reference point is the geometric-equivariance literature (GATr, de Haan et al.), which argues that the right design move is to pick a representation space where the downstream query reduces to an inner product under the relevant symmetries — equivariance then falls out of linear algebra rather than being bolted on via message passing. That literature works with Lie-group actions on Euclidean coordinates, which is not quite our setting: drafting rewrites are categorical equivalences induced by authored convention, not group actions in the clean sense. The vocabulary and training recipes transfer; the theorems do not directly apply.

The operational form of the question for this problem is therefore: rewrite-invariance is a candidate inductive bias for any future learned scorer, and the choice of mechanism is itself a research question. Three options worth examining:

- **Explicit invariance penalty.** Add `L_inv = E[||f(x) - f(g(x))||]` over rewrite generators `g` as an auxiliary loss. Auditable; loss value reads directly as “how invariant is the scorer.”
- **Augmentation along rewrite orbits.** Train on `(x, g(x))` pairs without an explicit penalty. Simpler to implement; invariance emerges indirectly and is harder to read off.
- **Architectural symmetry-breaking inputs** (cf. Goel et al., *Any-Subgroup Equivariant Networks via Symmetry Breaking*, 2026). Start from a broad equivariance and specify the effective subgroup per instance via an auxiliary input. A note of caution: if provenance features are used as that input, the scorer’s semantic equivalence becomes parameterized by provenance — the opposite of what “pool for geometry, tag for provenance” requires. This is a live architectural question, not a default to reach for.

Either of the first two is compatible with the extension plan below. The third is a structural commitment that would need its own justification.

## The Stack

This take-home sits at the bottom of a longer system:

```text
Layer 1: Geometric Perception (primitives -> endpoints)           <- this task
Layer 2: Object Formation / Tokenization (endpoints -> polygons)  <- this task
Layer 3: Graph Construction (polygons -> typed relationships)
Layer 4: Pair-Relation Scoring
Layer 5: Prototype / Memory Head
Layer 6: GNN Consistency Propagation
Layer 7: Structured Readout / Validator Interface
Layer 8: Validator Loop
```

The entropy split is explicit:

| Entropy profile | What belongs here |
|---|---|
| low-entropy scaffold | closure, winding, validity, family priors, family geometric filters, rewrite-invariance constraints |
| high-entropy adaptation | tolerance selection under drafting style, pair-relation scoring, family-conditioned merge heads, prototype memory, reviewer feedback |

The take-home tests the scaffold. The merge lab begins to expose the next layer.

## What The File Actually Contains

The most important empirical findings:

### Normalization

`A-GLAZING MULLION` and `A-GLAZING-MULLION` are not just naming variants. They overlap strongly in space while using different primitive carriers. They are effectively the same physical mullions authored with two CAD conventions.

`A-GLAZING FULL` and `A-GLAZING-FULL` have similar names but mostly disjoint spatial zones. So naive name normalization is wrong. Spatial overlap and entity-type profile both matter.

See:

- [`../process/layer_normalization_analysis.md`](../process/layer_normalization_analysis.md)

### Programmatic vs Contextual Merges

The merge problem factors into two sequential quotients:

- **programmatic**: decidable from provenance + degenerate geometry alone
- **contextual**: requires neighborhood reasoning or learned judgment

On this file:

- all curtain-wall recommended merges are effectively programmatic
- only a small minority of wall merges are

See:

- [`programmatic_vs_contextual_merges.md`](programmatic_vs_contextual_merges.md)

### Family-Typed Structure

Columns behave like a duplicate-overlap problem.

Walls behave like a continuity-and-compatibility problem.

Curtain walls behave like a panel-lattice problem.

That is why the merge layer should be family-typed rather than monolithic.

## Why The Programmatic / Contextual Split Matters

This is not just a convenient observation about this one file.

It says that part of the merge problem has **compositional structure that survives composition**.

The programmatic quotient collapses the provenance-decidable part cheaply. The contextual quotient is the residual that actually requires learned judgment.

That is why the merge lab is worth treating as a first-class surface instead of a one-off utility.

## The Extension Plan

The extension path is already sketched in:

- [`../experiments/INDEPENDENT_LATENT_DIMENSIONS_MEMO.md`](../experiments/INDEPENDENT_LATENT_DIMENSIONS_MEMO.md)
- [`../experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md`](../experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md)

The ordering matters:

0. **Rewrite-invariance as a candidate training-time inductive bias.** Generate equivalent views of the same merge relation using rewrite generators (collinear split/merge, carrier swap, snap-lattice perturbation, schema remap). Incorporate via explicit invariance penalty, orbit-based augmentation, or — with the caveat above about provenance — symmetry-breaking auxiliary inputs. Choice of mechanism is itself a research question the merge lab can discriminate.
1. **Label candidate pairs** through the merge lab.
2. **Train sparse edge scorers** on pair features, with calibrated uncertainty — conformal prediction (Vovk, Gammerman, Shafer) is the natural tool, as it provides distribution-free coverage under drafter-style shift without assuming a clean test distribution.
3. **Add prototype memory** in the small-clean-label regime. Recent work on dense associative memories with threshold nonlinearities (Kafraj, Krotov et al.) gives a regime match: compositional hidden encoding over pair-feature prototypes yields high capacity without winner-take-all basin rigidity, which suits the small-data, geometrically-compositional setting of expert-labeled merge pairs.
4. **Add a GNN** only as consistency propagation across already-scored pair relations. Candidate handle for “which invariances does propagation respect”: 2-closure represented as edge features (Goel et al.), a tractable approximation for subgroup equivariance that integrates into standard GNN backbones without architectural surgery.
5. **Emit typed edit proposals / structured readouts** over typed adjacency templates and validator-facing state.

The GNN is not the first step. It is what comes after the quotient is reasonably right. The point of the scaffold is to prevent the project from collapsing into brittle edge-case patching before the scalable representation is even defined.

## What The Take-Home Proved Empirically

- A geometry-first pipeline can recover `1158 / 764 / 304` walls / columns / curtain walls on the supplied file in a few seconds after adding explicit HATCH boundary extraction; the earlier graph/direct-only baseline was `274 / 572 / 304`.
- The hyphen/space layer variants can collapse programmatically in the right cases.
- Column merge candidates separate into interpretable buckets:
  - extraction duplicates
  - distinct-but-close elements
  - ambiguous cases
- Adaptive or family-aware tolerance tuning is meaningful, but the basic scaffold already reveals stable structure.

Those are useful because they are low-entropy invariants surfaced by the scaffold, not learned artifacts.

## Reading Order

For a reviewer or interview conversation:

1. [`../../DESIGN.md`](../../DESIGN.md)
2. this document
3. [`../process/layer_normalization_analysis.md`](../process/layer_normalization_analysis.md)
4. [`programmatic_vs_contextual_merges.md`](programmatic_vs_contextual_merges.md)
5. [`../experiments/INDEPENDENT_LATENT_DIMENSIONS_MEMO.md`](../experiments/INDEPENDENT_LATENT_DIMENSIONS_MEMO.md)

## References

### Framing

- Lei et al., *A Mechanistic Analysis of Sim-and-Real Co-Training in Generative Robot Policies*, 2026 (`arXiv:2604.13645`)

### Operational test / equivariance

- Brehmer, de Haan, Behrends, Cohen, *Geometric Algebra Transformer*, 2023. Source of the “inner-product-under-symmetry” framing adapted as the operational test.
- de Haan, Cohen, Brehmer, *Euclidean, Projective, Conformal: Choosing a Geometric Algebra for Equivariant Transformers*, 2024. Representation-space-choice analysis over three candidate algebras; the tradeoff vocabulary is useful beyond the specific algebras it discusses.
- Bronstein, Bruna, Cohen, Veličković, *Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges*, 2021. Equivariance-as-inductive-bias as the unifying principle.
- Goel, Lim, Lawrence, Jegelka, Huang, *Any-Subgroup Equivariant Networks via Symmetry Breaking*, 2026. ASEN: per-instance subgroup equivariance via auxiliary symmetry-breaking inputs; 2-closure as a tractable edge-feature approximation.

### Compositionality

- Censi, *A Mathematical Theory of Co-Design*, 2015
- Cai, Huang, Alharbi, Zardini, *Scalable Co-Design via Linear Design Problems: Compositional Theory and Algorithms*, 2026 (`arXiv:2603.29083`)

### Scoring / calibration / memory

- Vovk, Gammerman, Shafer, *Algorithmic Learning in a Random World*, 2005 / 2022. Conformal prediction as distribution-free coverage guarantee under drafter-style shift.
- Goodfire, EVEE work on annotation probes / sparse feature bridges. Pattern for routing dense embeddings through interpretable feature axes; adapted here as the sparse basis for pair scoring (Block A + B).
- Shafiei Kafraj, Krotov, Latham, *A Biologically Plausible Dense Associative Memory with Exponential Capacity*, 2026 (`arXiv:2601.00984`). Compositional hidden encoding and exponential capacity for prototype-memory retrieval in the small-clean-label regime.
