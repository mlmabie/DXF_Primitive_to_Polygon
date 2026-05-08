# GNN Architecture And Training Minutia

Date: 2026-05-08

This note captures the low-level model and training choices behind the higher
level plan. It is intentionally biased by the T-UEBA lesson: the model only
worked because the ontology, temporal reconstruction, feature schema,
calibration, and deployment budget were treated as first-class engineering
objects.

## Architecture Bias

Use GNNs as narrow graph products, not as the final universal architecture.
The first GNN should answer:

> where does typed neighborhood propagation beat deterministic geometry
> features and sparse relation baselines?

That implies small, inspectable models first:

- GraphSAGE for robust local aggregation and easy batching
- GAT/GATv2 when relation attention is useful and interpretable enough to
  inspect
- PNA when degree variation matters across sparse symbols, dense annotations,
  and repeated plan regions
- lightweight heterogeneous message passing when node/edge types are already
  stable
- graph transformer only after scope resolver, batching, and candidate graph
  construction are working

Do not start with a large graph transformer just because the final system may
eventually use transformer or JEPA-style representations. A large model can
hide graph-construction errors that a small GNN would expose.

## Graph Schema

Start with typed nodes:

- `primitive`
- `endpoint`
- `supervector`
- `face`
- `annotation`

Add later:

- `component`
- `constraint`
- `edit`
- `memory`

Start with typed edges:

- geometry: `touches`, `intersects`, `near_endpoint`, `collinear_with`,
  `parallel_offset_from`, `contains`, `inside`, `bounds`
- composition: `composed_of`, `same_element_candidate`, `same_symbol_family`
- annotation: `labels`, `measures`, `points_to`
- system/edit: `route_candidate`, `conflicts_with`, `must_move_with`

Each edge should carry explicit pair features: gap, angle, overlap, offset,
IoU, containment ratio, continuation score, crossing type, shared boundary
length, and provenance flags.

## Feature Normalization

Normalize geometry without destroying project scale:

- local-frame coordinates per node or scoped subgraph
- drawing-level scale metadata as a separate feature
- orientation as `sin(theta), cos(theta)`, not raw angle
- log-scaled lengths/areas when heavy-tailed
- categorical embeddings for entity kind, source kind, linetype, block/layout
  state
- layer/color as hidden provenance in the first layer-blind run, then ablate
  them explicitly

Preserve exact coordinates in storage. Normalize only for model input.

## Candidate Model Stack

### Baseline Stack

1. primitive feature classifier
2. pair-feature relation classifier
3. deterministic grouping heuristic
4. raster/rendered-chip baseline
5. calibrated ensemble or shallow tree where useful

This is the floor. The GNN must report delta over this floor by class and
relation type.

### First GNN

Recommended first model:

```text
typed input encoders
-> 2-4 message-passing layers
-> residual connections
-> layer norm or graph norm
-> dropout
-> node heads + edge heads + calibration head
```

Keep hidden width modest: 64-256. CAD graphs are not internet-scale language
models; the risk is overfitting to drafter conventions, not underparameterizing
a universal world model.

### Heterogeneous Variant

Use type-specific input projections and relation-specific message functions,
but avoid a parameter explosion:

- shared trunk for geometry-heavy relations
- small relation embeddings for edge type
- basis decomposition or grouped relations if using R-GCN-style weights
- edge-conditioned MLP only for the relations that need it

Group relations by role:

- topology
- metric geometry
- composition
- annotation
- system/edit

## Losses

Use multi-task losses:

- primitive class cross entropy or focal loss
- supervector class cross entropy
- relation type cross entropy
- binary relation existence loss
- annotation-to-object contrastive or softmax target loss
- validator residual regression
- uncertainty/calibration loss
- rewrite consistency loss
- edit/review action loss when workflow labels exist

Class imbalance will be severe. Use:

- class-balanced sampling
- focal loss for rare but important classes
- per-relation metrics instead of a single aggregate loss
- hard-negative mining for `same_element_candidate`, `labels`, and `measures`

## Self-Supervised Objectives

Before enough labels exist, train on graph structure:

- masked primitive attributes
- masked relation type
- missing edge prediction
- subgraph denoising after snap jitter or carrier rewrite
- hatch/outline equivalence prediction
- text/tag-to-nearby-object consistency
- validator residual prediction
- drawing-family or style contrastive objective, with caution

Do not let style contrastive learning collapse into layer/color memorization.
Keep provenance-tagged ablations.

## Sampling And Batching

CAD graphs can be too large for full-graph training. Use scoped batching:

- ego subgraphs around candidate supervectors
- relation-centric batches around hard pairs
- face/room scopes for shell reasoning
- annotation-to-object scopes around text, leaders, tags, and dimensions
- validator scopes emitted by the scope resolver

Sampling should preserve:

- all positive target edges in the batch
- hard negatives near the same target
- containing face/room when relevant
- linked annotation nodes
- provenance needed for debugging, even if not used as model input

Avoid random primitive minibatches. They destroy the structure the GNN is meant
to use.

## Negative Examples

Most early failures will come from weak negatives. Add explicit negatives:

- near but not same object
- overlapping but distinct object
- tag near two candidates but labels only one
- dimension line near several spans but measures one
- hatch carrier visually similar to wall mass but not wall
- repeated symbol family that should not merge
- route candidate geometrically short but construction-invalid

The model needs to learn "do not merge" as carefully as "merge."

## Calibration And Partitioning

Use conformal or conformal-style review bands after the sparse baseline and
again after the GNN:

- high-confidence positive -> auto-accept candidate relation only if validators
  agree
- high-confidence negative -> reject
- middle band -> review
- contradiction band -> QA/conversion investigation

Report:

- ECE
- conformal coverage
- precision at auto-accept threshold
- review load at fixed precision
- gold/silver/amber/red evidence-lane movement

The partition is part of the product. A useful model knows when it is looking
at robust geometry and when it is merely guessing.

## Training Schedule

Recommended sequence:

1. deterministic graph export and overlays
2. sparse node and edge baselines
3. self-supervised graph pretraining
4. supervised primitive/supervector/relation heads
5. calibration and review bands
6. rewrite-invariance training
7. prototype memory or matryoshka retrieval
8. project/firm/jurisdiction adapters
9. residual edit and validator-conditioned heads

Do not add later-stage machinery until the earlier stage exposes a real
residual.

## Ablations

Required ablations:

- local features only vs graph features
- with vs without layer/color
- primitive-only vs primitive + supervector
- supervector-only vs multi-level graph
- graph without annotation nodes vs graph with annotation nodes
- edge features only vs message passing
- sparse baseline vs GNN
- full graph vs scoped subgraph
- no pretraining vs masked/rewrite pretraining
- no calibration vs calibrated review bands
- no memory vs prototype/matryoshka retrieval

The important result is not "GNN wins." It is where and why propagation wins.

## T-UEBA Transfer

Useful instincts from T-UEBA:

- graph ontology is model architecture
- temporal reconstruction quality dominates clever message passing
- typed relations beat generic adjacency
- calibration matters when the model is part of an operational loop
- small efficient models can win when the deployment envelope is real
- uncertainty and active learning are system features, not evaluation garnish
- schema drift and data provenance need to be visible

Differences:

- CAD geometry has exact deterministic structure that should not be learned
  from scratch
- annotation semantics are messier than event labels
- rewrite invariance is authored and partial, not a clean temporal process
- construction validity depends on external validators and project memory

## Failure Modes To Watch

- layer/color leakage masquerading as intelligence
- GNN only learning drafter style
- supervector generator hiding primitive evidence
- random splits inflating performance
- graph construction cost dominating inference
- attention weights looking interpretable but tracking artifacts
- high F1 with poor calibration
- no explicit negative labels for merge/relation tasks
- weak PDF/vector alignment poisoning labels
- model confidence rising on conversion errors

## Minimum Viable Training Run

For the first credible run:

1. 3-5 drawings with preserved DWG/DXF metadata
2. primitive table, supervector table, edge table, annotation table
3. drawing-level split
4. sparse baseline
5. small hetero GraphSAGE or GATv2 model
6. primitive, supervector, relation, and annotation-to-object heads
7. hard negatives
8. calibration report
9. rewrite perturbation report
10. overlay review of 20 high-confidence correct, 20 high-confidence wrong,
    and 20 uncertain cases

That run is enough to answer whether the GNN is discovering useful contextual
structure or just memorizing local CAD artifacts.

## Core Principle

> Treat every GNN choice as an experiment in representation geometry: does this
> layer, loss, sample, or memory make the correct project-specific update
> lower-dimensional, better calibrated, and easier to compile back into the
> deterministic engine?
