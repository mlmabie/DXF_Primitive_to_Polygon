# Augrade Representation Reading Notes

Date: 2026-05-05

These notes incorporate the cited thesis/research-extension papers into the GNN
plan branch. They are intentionally opinionated toward the immediate Augrade
goal: learn useful representation design, GNN placement, and ML-system
engineering for a take-home plus CTO conversation.

## Local Thread

Start from the repo's own evidence before jumping into papers:

- `../../reference/research/thesis.md`: evidence-first DXF reconstruction
  thesis.
- `../../reference/research/programmatic_vs_contextual_merges.md`: strongest
  practical argument for separating deterministic equivalence from contextual
  semantic identity.
- `../../reference/research/research_extension.md`: broader research framing
  and citation spine.
- `../../reference/experiments/INDEPENDENT_LATENT_DIMENSIONS_MEMO.md`: typed
  quotient hypothesis for pair relations.
- `../../reference/experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md`:
  staged plan before adding a GNN.

## Core Thesis

The strongest Augrade framing is not "put a GNN on BIM." It is:

> Choose the right representation boundary between raw geometry, stable object
> state, typed relations, learned residual judgments, and deterministic
> validators.

For this repo, the concrete version is:

1. Keep closure, winding, family-scoped geometry, and provenance deterministic.
2. Form primitive, supervector, face, and component candidates.
3. Score pair relations with sparse baselines first.
4. Use calibrated uncertainty to split auto-merge, reject, and review.
5. Add a GNN only where neighborhood consistency beats local edge features.

## What Each Paper Should Do For The Plan

### Geometric Deep Learning

Source: https://arxiv.org/abs/2104.13478

Use this as the conceptual foundation for why buildings and drawings should
not be modeled as unstructured token soup. Architectural drawings have locality,
hierarchy, repeated motifs, typed relations, physical constraints, and
symmetries. That supports graph/geometric priors, but it does not imply the GNN
should own raw geometry extraction or exact validity.

Plan implication:

- Put graph learning above deterministic vector tokenization.
- Make hierarchy explicit: primitive -> supervector -> face -> component.
- Treat message passing as relational consistency propagation.

### Sim-And-Real Co-Training

Source: https://arxiv.org/abs/2604.13645

Use this for the "pool for geometry, tag for provenance" idea. The important
transfer is not robotics policy details; it is cross-domain alignment without
destroying domain identity.

Plan implication:

- Treat layer variants, HATCH-vs-outline carriers, snap perturbations, and
  primitive decomposition as authored rewrite domains.
- Learn or test invariance over semantics-preserving rewrites.
- Keep provenance as a residual side channel for debugging, trust, and review.

### GATr And Choosing A Geometric Algebra

Sources:

- https://arxiv.org/abs/2305.18415
- https://proceedings.mlr.press/v238/haan24a.html

Use these as representation-choice papers, not as direct implementation
requirements. They show that the carrier space matters: choose the object
representation that makes the relevant query simple under the relevant
symmetries.

Plan implication:

- Keep geometry carriers rich enough for distances, frames, orientations,
  clearances, penetrations, and support surfaces.
- Do not prematurely flatten everything into generic scalar features.
- Be careful: CAD drafting rewrites are authored equivalences, not clean
  Euclidean group actions.

### Any-Subgroup Equivariant Networks

Sources:

- https://openreview.net/forum?id=jz3d7nvtGz
- https://arxiv.org/abs/2603.19486

Use this as vocabulary for family-conditioned invariance. Walls, columns, and
curtain walls likely need different quotient structure.

Plan implication:

- Compare one shared model, shared trunk with family heads, and fully separate
  family models before claiming a universal latent.
- Keep ASEN-style mechanisms as later research, after sparse baselines and
  rewrite tests.

### Cai 2026 And Censi 2015 Co-Design

Sources:

- https://arxiv.org/abs/2603.29083
- https://arxiv.org/abs/1512.08055

Use these to justify stable interfaces. The product moat is not a single model
trick. It is the compositional interface between learned proposal generation,
explicit project state, edit grammar, and hard validators.

Plan implication:

- Freeze object identity, typed relations, edit primitives, validator boundary,
  evidence links, and trace format early.
- Let learned components propose, score, rank, and route.
- Let exact geometry/code/constructability checks decide final validity.

### Algorithmic Learning In A Random World / Conformal Prediction

Sources:

- https://www.alrw.net/
- https://link.springer.com/book/10.1007/978-3-031-06649-8

Use this for review gates. A merge or edit-impact model should not produce only
one brittle yes/no answer.

Plan implication:

- Add calibrated uncertainty around pair scorers.
- Route high-confidence positives to auto-merge, high-confidence negatives to
  reject, and uncertain cases to review.
- Measure calibration and review-load reduction, not just F1.

### Dense Associative Memory

Source: https://arxiv.org/abs/2601.00984

Use this as a possible low-label prototype-memory layer after the relation
feature space stabilizes.

Plan implication:

- Store positive and negative merge exemplars by family.
- Test whether memory improves ambiguous boundary cases.
- Do not use memory as a substitute for deterministic geometry or validators.

### Goodfire EVEE

Source: https://www.goodfire.ai/research/evee-explaining-genetic-variants

Use this as an industry example of turning foundation embeddings into
interpretable, structured scientific predictions. The domain is genomics, so
keep the claim boundary modest.

Plan implication:

- If rich embeddings enter the system, add probe/readout layers that produce
  inspectable concepts and evidence.
- Keep predictions framed as hypotheses that experts and validators can test.

## CTO-Safe Talk Track

"I would not make the GNN the geometry engine. I would use deterministic vector
processing to form stable candidates, keep provenance visible, and then learn
the residual relation layer: duplicate-vs-distinct, continuation, contextual
merge, likely dependency, and edit impact. The graph model belongs where local
evidence has to propagate through typed relations. Exact validity should stay
with deterministic validators."

## Take-Home Implementation Bias

For the next branch of work:

1. Export a layer-blind primitive/supervector table.
2. Build pair features for gap, overlap, alignment, containment, family,
   source-kind, and neighborhood.
3. Train heuristic, logistic, and shallow-tree baselines first.
4. Add conformal-style review bands.
5. Generate rewrite augmentations and measure prediction stability.
6. Add a small heterogeneous GNN only after the non-graph relation baseline has
   exposed cases that truly need context propagation.
