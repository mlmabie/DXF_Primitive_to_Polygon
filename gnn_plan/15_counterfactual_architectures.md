# Counterfactual Architectures

Date: 2026-05-08

This note records why the current plan favors a heterogeneous
primitive/supervector/annotation/face graph instead of simpler or more direct
alternatives. The goal is not to defend the chosen design dogmatically. The
goal is to make the architectural bet falsifiable.

## How To Read These Counterfactuals

These counterfactuals are controls for a serious CAD graph-learning program.
They should not be read as reducing the value of training a CAD-native GNN;
they define what would make that GNN's contribution real.

The target is trusted work: better supervector recovery, better
annotation-to-object links, better relation calibration, lower false-merge
risk, stronger validator agreement, lower scope/compute cost, and more learned
discoveries that compile back into deterministic rules.

If a simpler counterfactual produces more trusted work, use it. If graph
propagation produces the residual lift, it has earned its place.

## Counterfactual 1: One Homogeneous Combined-Layer Graph

Alternative:

> Put every extracted vector entity into one graph, ignore node-type
> distinctions, add generic proximity/intersection edges, and train a node
> classifier directly.

Why it is attractive:

- simpler implementation
- easier batching
- fewer schema decisions
- direct fit to entity-as-node GNN papers
- lower overhead for a first baseline

Why it is probably insufficient:

- lines, arcs, text, hatches, leaders, dimensions, and inferred faces do not
  have the same semantics
- generic adjacency mixes topology, annotation, containment, composition, and
  system dependency into one relation
- many labels belong to composed objects, not raw entities
- a line can be evidence for wall mass, hatch boundary, symbol geometry,
  dimension text, leader, or title-block decoration depending on role
- annotations need typed links like `labels`, `measures`, and `points_to`, not
  only proximity
- message passing over one generic graph can blur operational distinctions that
  validators and edit policies need later

When to still run it:

- as an early baseline
- as an ablation against heterogeneous graph state
- as a smoke test for feature extraction and labels

What would change the decision:

- homogeneous graph matches heterogeneous performance on supervector labels,
  annotation-to-object links, and relation recovery
- homogeneous graph has materially better calibration
- typed edge construction dominates runtime and gives little accuracy or
  review-yield benefit

Default verdict:

Use homogeneous graph classification as a baseline, not as the product
representation.

## Counterfactual 2: Direct Primitive Classification Only

Alternative:

> Classify every primitive independently or with light local context, then
> compose objects after classification.

Why it is attractive:

- labels are easy to attach to original CAD entities
- simpler objective
- easier confusion matrix
- less dependence on supervector candidate quality

Why it is probably insufficient:

- real objects are often multi-primitive
- door swings, fixtures, hatches, curtain grids, tags, and wall faces are
  compositional
- relation errors can be more expensive than node-class errors
- object formation becomes a brittle post-processing step
- expert review wants to inspect candidate objects, not thousands of raw lines

When to still run it:

- as the first supervised model
- as a feature source for supervector classification
- as a diagnostic for conversion/layer/entity coverage

What would change the decision:

- primitive labels compose into high-fidelity objects with simple deterministic
  rules
- reviewers prefer primitive-level labeling and correction
- supervector generation is too noisy to improve review yield

Default verdict:

Primitive classification is necessary but not sufficient. The main target
should be primitive + supervector + relation prediction.

## Counterfactual 3: Raster Or Rendered-View First

Alternative:

> Treat DXF/DWG like modern PDF parsing: render views, use a vision model, and
> reconstruct semantic structure from pixels.

Why it is attractive:

- robust to ugly CAD internals and PDF extraction artifacts
- leverages strong foundation vision models
- sees the drawing as the human sees it
- can work when vector extraction is incomplete

Why it is probably insufficient alone:

- output must be editable native geometry
- validators need exact coordinates, handles, object identity, and provenance
- small gaps, arcs, hatches, line widths, and block membership can be lost or
  distorted
- visual plausibility can hide invalid construction state
- rendered evidence does not naturally produce branchable edit history

When to use it:

- conversion QA
- local image-chip baseline
- semantic proposal generation
- PDF fallback
- visual confirmation of graph predictions

What would change the decision:

- vision system can reliably align predictions back to exact vector ids
- rendered proposals improve hard annotation-to-object cases without corrupting
  geometry
- many customer inputs arrive only as PDFs/renders

Default verdict:

Use rendered views as a proposal and QA channel. The source of truth remains
vector graph state.

## Counterfactual 4: Graph Transformer First

Alternative:

> Skip small GNNs and train a larger graph transformer or transformer over
> serialized drawing entities.

Why it is attractive:

- long-range context
- easier path toward foundation-model compatibility
- potentially better on repeated motifs, schedules, and global drawing
  conventions

Why it is risky:

- graph construction and label quality are not yet proven
- large models can hide ontology errors
- compute may go into irrelevant global context
- harder to inspect why relation propagation helped
- scope resolver and batching are not mature yet

When to use it:

- after scoped subgraphs are stable
- when long-range schedule/motif reasoning beats local propagation
- as a comparison to small hetero GNNs on relation recovery and calibration

What would change the decision:

- small GNNs fail specifically due to missing long-range context
- scoped graph transformer improves relation recovery without hurting
  calibration or latency
- training data volume becomes large enough to justify it

Default verdict:

Defer graph transformers. Build small calibrated GNN products first.

## Counterfactual 5: Pure Rules And No GNN

Alternative:

> Keep extending deterministic geometry, layer heuristics, and rule-based
> grouping without a learned graph model.

Why it is attractive:

- exact and auditable
- easier to validate
- no model training overhead
- deterministic behavior is valuable in CAD

Why it is probably insufficient:

- authored CAD conventions drift by drafter, firm, project, and jurisdiction
- annotation-to-object correspondence can be ambiguous
- repeated motifs and carrier styles create too many brittle cases
- workflow preferences and review outcomes are difficult to encode manually
- rule discovery benefits from embedding neighborhoods and active learning

When to use it:

- always, as the base engine and validator layer
- whenever a learned motif becomes stable enough to compile back into rules

What would change the decision:

- deterministic rules reach high coverage with low exception burden
- learned models fail to improve review yield or rule conversion rate

Default verdict:

Rules are the substrate and destination for stable discoveries. The GNN is the
failure microscope and data-efficiency layer.

## Counterfactual 6: End-To-End Foundation Model Harness

Alternative:

> Use a foundation model to ingest rendered pages, serialized entities, and
> tool outputs, then ask it to classify/repair the drawing directly.

Why it is attractive:

- broad context
- natural language explanation
- fast iteration
- strong multimodal priors

Why it is risky:

- weak native edit state
- hallucinated geometry or relations
- hard to calibrate auto-actions
- context windows do not equal durable project memory
- validators still need exact operands

When to use it:

- query/reasoning layer over retrieved subgraphs
- explanation and review assistance
- source-review and research synthesis
- proposal generation with validator checks

What would change the decision:

- foundation model reliably calls graph tools and validators
- edits are grounded to exact ids and branch histories
- uncertainty and provenance are good enough for review routing

Default verdict:

Use foundation models as harness and reasoning layer. Do not make them the
primary memory or geometry engine.

## Why Heterogeneous Graph Is The Current Default

The hetero graph preserves distinctions that matter operationally:

- evidence vs object candidate
- raw primitive vs composed supervector
- geometry relation vs annotation relation
- region/face context vs local entity context
- validator residual vs model score
- robust exemplar vs ambiguous review case

It lets the system ask more precise questions:

- which object does this tag label?
- do these primitives compose one wall face?
- is this relation a geometric fact, a weak annotation, or a learned guess?
- what minimal subgraph is sufficient to validate this edit?
- which cases are gold exemplars and which are active-learning material?

## Required Counterfactual Experiments

Run these before claiming the architecture is settled:

1. homogeneous primitive graph vs heterogeneous graph
2. primitive-only labels vs primitive + supervector + relation labels
3. vector-only vs vector + rendered-chip side channel
4. sparse baseline vs small GNN
5. small GNN vs scoped graph transformer when enough data exists
6. with layer/color vs layer-blind
7. full graph vs scope-resolved subgraph
8. no memory vs prototype/matryoshka memory

Each experiment should report:

- accuracy by target type
- calibration
- review-load reduction
- rewrite stability
- conversion sensitivity
- compute cost
- rule conversion value

## Decision Rule

The winning architecture is not the one with the cleanest name. It is the one
that gives the best combination of:

- native editable state
- high-fidelity supervector recovery
- calibrated uncertainty
- data-efficient adaptation
- validator alignment
- review yield
- compute/scoping efficiency
- discoveries that compile back into deterministic rules
