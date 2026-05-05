# Experiments

This folder is for experiment plans and run outputs once implementation starts.

## Phase 0: Graph Export

Goal:

- parse DWG/DXF into layer-blind primitive records
- build deterministic supervector candidates
- export a typed graph JSON or parquet bundle

Candidate outputs:

- `primitives.json`
- `supervectors.json`
- `faces.json`
- `edges.json`
- `graph_manifest.json`

## Phase 1: Annotation Alignment

Goal:

- map incoming annotations to graph ids
- preserve ambiguous mappings
- produce a small labeled graph snapshot per example

## Phase 2: Non-GNN Baselines

Goal:

- establish whether local geometry features already classify the examples
- train or hand-score node and edge classifiers
- identify classes that need neighborhood reasoning

Baselines:

- rules over geometry features
- sparse logistic regression
- shallow tree or boosted tree
- nearest prototype over normalized feature blocks

## Phase 3: Small GNN

Goal:

- test whether message passing improves the hard cases
- keep model small and inspectable

Candidate models:

- GraphSAGE
- GAT/GATv2
- PNA
- heterogeneous message passing over primitive/supervector/face nodes

## Phase 4: Raster Context Ablation

Goal:

- compare vector-only, raster-only, and hybrid graph plus raster-chip models
- measure whether raster context helps without losing vector detail

## Phase 5: Predictive Editing

Goal:

- represent edits as graph events
- predict impacted nodes, conflicts, and dependencies
- combine deterministic geometry updates, explicit constraints, and learned
  impact scoring

