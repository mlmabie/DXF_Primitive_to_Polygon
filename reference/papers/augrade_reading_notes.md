# Augrade Research Reading Notes

Date: 2026-05-05

## Local Docs Found

- `../research/thesis.md`: evidence-first thesis for the DXF reconstruction work.
- `../research/research_extension.md`: broader representation-learning framing and the citation spine.
- `../research/programmatic_vs_contextual_merges.md`: the most interview-useful proof that the merge problem splits into deterministic equivalence and contextual semantic identity.
- `../experiments/INDEPENDENT_LATENT_DIMENSIONS_MEMO.md`: follow-on hypothesis about typed quotient coordinates.
- `../experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md`: practical experimental plan.

## One-Line Thesis

For Augrade, frame the work as a representation-boundary problem, not a "put a GNN on BIM" problem:

geometry-native evidence -> stable object tokens -> typed relation graph -> learned pair/context scoring -> deterministic validators and edit planning.

The local DXF solver is a small, concrete instance of this: it keeps closure, winding, family priors, layer provenance, and source carriers deterministic, then identifies the residual merge/review layer where learning can actually help.

## Reading Order

1. `thesis.md`, `programmatic_vs_contextual_merges.md`, and the latent-dimensions memo.
2. Bronstein et al., *Geometric Deep Learning*, for the language of inductive bias, symmetry, and graph/geometric priors.
3. GATr and de Haan et al., for geometric representation choices.
4. Lei et al., *Sim-and-Real Co-Training*, for "structured representation alignment"; this is the best direct conceptual support for "pool for geometry, tag for provenance."
5. Cai et al. and Censi, for compositional design interfaces and validator/planner boundaries.
6. Vovk/Gammerman/Shafer plus conformal prediction references, for uncertainty gates: auto-merge, reject, or route to reviewer.
7. Dense associative memory and Goodfire EVEE, for low-label prototype memory and interpretable feature/probe heads.
8. ASEN last: useful vocabulary for subgroup-style equivariance, but speculative for this DXF/BIM setting.

## Opinionated Summaries

### Lei et al. 2026 - Sim-and-Real Co-Training

Source: https://arxiv.org/abs/2604.13645

Core idea: co-training works when a representation both aligns cross-domain structure and preserves enough domain identity to avoid destructive collapse.

Augrade relevance: this is the cleanest support for the repo's "pool for geometry, tag for provenance" principle. The DXF problem has multiple authored views of the same latent objects: layer variants, direct polygons, graph faces, HATCH boundaries, snap perturbations. The goal is not to erase those differences. It is to align them where they describe the same object while keeping residual provenance as evidence.

Talk track: "I would treat CAD/BIM authoring variation like a structured rewrite domain. I want invariant object/relation coordinates for decisions, but I do not want to destroy provenance, because provenance is exactly how the system knows when to trust, review, or debug a merge."

### Brehmer et al. 2023 - Geometric Algebra Transformer

Source: https://arxiv.org/abs/2305.18415

Core idea: choose a representation space where geometric objects and transformations become natural, then build the network around those symmetries.

Augrade relevance: this is useful less as "use GATr directly" and more as a design lesson. BIM/CAD systems have geometry, frames, distances, orientations, support surfaces, penetrations, and clearances. Those should not be forced into arbitrary flat features if a more geometric carrier makes the query simpler.

Caution: drafting rewrites are not clean Euclidean symmetry groups. Split/merge linework, HATCH-vs-outline carriers, and layer schema remaps are authored equivalences, not just rotations/translations. Borrow the representation-design mindset, not the theorem wholesale.

### de Haan/Cohen/Brehmer 2024 - Choosing a Geometric Algebra

Source: https://proceedings.mlr.press/v238/haan24a.html

Core idea: the algebra you choose changes expressivity, compute, sample efficiency, and the symmetry group the model naturally respects.

Augrade relevance: this is the "representation choice is an engineering decision" paper. For Augrade, the analog is choosing between raw primitives, polygons, object tokens, relation tokens, constraint tokens, hierarchy tokens, and residual edit tokens. The architecture should follow the representational job.

Talk track: "I would start by asking which objects and relations need to be stable across edits. Then I would pick the model class around that interface, not the other way around."

### Bronstein et al. 2021 - Geometric Deep Learning

Source: https://arxiv.org/abs/2104.13478

Core idea: deep learning succeeds when it exploits the regularities of the domain: grids, groups, graphs, manifolds, gauges, locality, hierarchy, and symmetries.

Augrade relevance: this is the foundation for why a building should not be treated as a generic token soup. Buildings have hierarchy, locality, typed relations, repeated motifs, physical constraints, and edit locality. A GNN is appropriate in the middle of the stack because constraints and context propagate over typed relations.

CTO-safe phrasing: "The graph is not the geometry engine. It is the relational consistency layer above object formation and below deterministic validation."

### Goel et al. 2026 - Any-Subgroup Equivariant Networks

Source: https://arxiv.org/abs/2603.19486

Core idea: one network can be made equivariant to different permutation subgroups using symmetry-breaking auxiliary inputs; the paper uses 2-closure to make this tractable.

Augrade relevance: useful for vocabulary around family-conditioned invariance. Walls, columns, and curtain walls do not share exactly the same quotient. Curtain walls may have grid/periodicity structure; columns may be concentric/duplicate-heavy; walls may be continuity-heavy. A single model with family-conditioned behavior is plausible.

Caution: this is not the first implementation step. For the take-home, a sparse pair scorer plus rewrite-invariance tests is more credible than an ASEN-style architecture.

### Cai et al. 2026 - Scalable Co-Design via Linear Design Problems

Source: https://arxiv.org/abs/2603.29083

Core idea: isolate a tractable compositional subclass of co-design problems, prove it is closed under interconnection, and compute exact scalable feasible sets through linear/polyhedral structure.

Augrade relevance: this is a strong conceptual anchor for "freeze the interface." If components expose capabilities, resource requirements, and constraints through stable interfaces, local design choices can compose into system-level reasoning. For Augrade, this maps to object tokens, typed constraints, validator boundaries, and edit grammars.

Talk track: "The product moat is not one model trick. It is a stable compositional interface between learned proposal generation, project state, and hard validators."

### Censi 2015 - A Mathematical Theory of Co-Design

Source: https://arxiv.org/abs/1512.08055

Core idea: complex engineered systems can be modeled as interdependent design problems whose feasible functionality/resource tradeoffs compose through subsystem interfaces.

Augrade relevance: this gives the older formal backbone for the same idea. It is more abstract and less immediately practical than Cai et al. for this conversation, but it supports the validator/planner boundary: learned models should propose and rank; exact feasibility belongs to explicit design constraints.

Use it as background, not as the lead citation.

### Vovk, Gammerman, Shafer - Algorithmic Learning in a Random World

Sources: https://www.alrw.net/ and https://link.springer.com/book/10.1007/978-3-031-06649-8

Core idea: conformal prediction gives model-agnostic uncertainty sets with validity guarantees under exchangeability-style assumptions and variants/extensions for drift/testing.

Augrade relevance: this is the right uncertainty language for merge/review workflows. The system should not produce one brittle "merge yes/no" output. It should route decisions into auto-merge, reject, or human review bands, with calibrated uncertainty and explicit evidence.

Talk track: "In the low-label regime, I would rather have a calibrated review gate than a model that acts confident because the metric average looks good."

### Goodfire EVEE 2026 - Interpretable Variant Effect Prediction

Source: https://www.goodfire.ai/research/evee-explaining-genetic-variants

Core idea: foundation-model embeddings can be turned into structured, interpretable scientific predictions using probes and explanation layers, while keeping predictions framed as hypotheses.

Augrade relevance: the domain is genomics, not BIM, but the system idea transfers: rich embeddings are not enough. You need a translation layer from latent representation to structured, inspectable concepts that domain experts can interrogate.

Caution: cite this as an industry research resource. Do not lean on it like a peer-reviewed BIM/geometry paper.

### Shafiei Kafraj/Krotov/Latham 2026 - Dense Associative Memory

Source: https://arxiv.org/abs/2601.00984

Core idea: distributed hidden representations can store compositional memory patterns with far higher capacity than winner-take-all associative memory.

Augrade relevance: useful for small-label merge prototypes. A future system could store positive/negative merge exemplars or repair patterns and retrieve them compositionally. This is a good adjunct to sparse pair scoring, not a replacement for geometry and validators.

Talk track: "I would test prototype memory only after the pair-relation feature space is stable. The memory should help on ambiguous examples, not become a magic nearest-neighbor bucket."

## Practical Take-Home Shape

The strongest next step is:

1. Keep deterministic polygon recovery, family inference, winding, and provenance as the substrate.
2. Build a candidate relation graph over polygons.
3. Add edge features for gap, overlap, alignment, containment, family, source kind, canonical layer, and local neighborhood context.
4. Train a sparse baseline before any GNN: heuristic, logistic regression, shallow tree/GBDT.
5. Add conformal calibration to create three actions: auto-merge, reject, route-to-review.
6. Test rewrite invariance using generated equivalent views: split/merge lines, snap jitter, HATCH-vs-outline, carrier swaps, layer schema remaps.
7. Only then add a GNN to propagate consistency over the candidate graph.

This lets you say, credibly:

"The take-home is a deterministic tokenizer with provenance. The research extension is a learned residual review layer. I would not ask a GNN to recover raw geometry or decide exact validity. I would use it after object formation, where relational consistency and cascading edit effects actually matter."

## CTO Conversation Priorities

- Lead with representation boundaries, not architecture names.
- Put GNNs in the middle of the stack: relation propagation, consistency, contextual merge scoring.
- Keep validators external and deterministic.
- Emphasize workflow exhaust: edits, rejections, repairs, code-check failures, comments, review traces.
- Treat residual edits as more important than whole-scene generation.
- Be honest about claim boundaries: strong graph ML and physical-design intuition; not claiming shipped BIM GNN production.
