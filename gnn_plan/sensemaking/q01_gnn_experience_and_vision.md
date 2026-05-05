# Q1: GNN Experience And Vision

Question:

> Can you summarise your experience with Graph Neural Networks, including key
> projects and use cases?

This workbench keeps the answer from becoming a resume paragraph. The goal is
to answer the literal experience question while making the deeper technical
vision visible.

## Source Answer

The current canonical answer already has strong ingredients:

- T-UEBA as shipped heterogeneous temporal GNN work
- PI ownership across ontology, schemas, features, temporal encoding,
  architecture, training/eval, and deployment
- operational constraints: low latency, small footprint, low false positives,
  drift/adversarial/messy data
- architecture experimentation: custom PyG, typed message passing,
  continuous-time attention, conformal uncertainty, sparse-autoencoder
  interpretability, active learning, synthetic data, tabular baselines, HopCPT
  / energy-style thinking
- use cases: heterogeneous relational reasoning, evolving graphs, anomaly
  detection, hierarchical representation, graph-native decision systems

## Raw Thesis To Preserve

The real transfer is not:

> I built a cyber GNN, therefore I can build a BIM GNN.

It is:

> I have built graph systems where the hard part was choosing the ontology,
> temporal reconstruction, evaluator, uncertainty boundary, and deployment
> envelope before the neural architecture could matter.

This is the connective tissue to Augrade.

## Substantive Answer Shape

A better Q1 answer should have three layers:

1. **Shipped proof:** T-UEBA proves end-to-end graph-system ownership under
   constraints.
2. **Design philosophy:** graph schema and relation ontology matter as much as
   the GNN layer.
3. **Augrade transfer:** buildings and project workflows are evolving
   structured state, with typed entities, typed relations, hard constraints,
   and repeated re-evaluation after edits.

## Strong Version

I would answer Q1 like this:

> My strongest shipped GNN work is T-UEBA, where I was PI on a heterogeneous
> temporal GNN system for real-time behavior analytics in tactical networks.
> The important part was not just the model class. I owned the graph ontology,
> temporal reconstruction, feature schema, message-passing design, uncertainty
> handling, eval loop, and deployment envelope. That project taught me that a
> GNN only becomes useful once the world interface is right: typed entities,
> typed relations, update semantics, calibration, and constraints. That is the
> same reason Augrade is interesting to me. The domain is different, but the
> systems problem rhymes: evolving structured state, hard external constraints,
> cascading edits, and a need for representations that survive real workflow
> variation.

## What To Research Next

To make this more substantive than interview positioning, answer:

- Which relation types in Augrade are analogous to typed security/event
  relations in T-UEBA?
- What are the natural temporal windows or revision episodes in CAD/BIM
  workflows?
- Which failures require node classification, edge scoring, graph-level
  anomaly detection, or sequential edit prediction?
- What does calibration mean here: auto-fix, reject, or route to human review?
- What graph state must persist across edits?

## Model-Vision Answer

For Augrade, the GNN should likely own:

- relation propagation over already-formed objects
- contextual duplicate-vs-distinct decisions
- dependency inference for edits
- route/system plausibility once rooms, shafts, fixtures, and access constraints
  exist
- uncertainty-aware review triage

The GNN should not own:

- exact geometry validity
- code/compliance truth
- raw DXF closure and winding
- all object formation from scratch

## Voice Check

If this answer starts sounding like "I used PyG on graphs," it has lost the
plot. The story is graph-system design under reality pressure.
