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
- convolutional filtering or raster-chip classifier for local visual context
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

Relation-discovery probes:

- NRI-style latent relation head over candidate dependencies
- supervised edge classifier where relation labels exist
- comparison between static per-drawing graphs and dynamic graph updates after
  edits

First runnable slice:

```bash
python3 gnn_plan/experiments/primitive_graph_classifier.py
```

This uses the existing `Airport Doors_MEZZ.dxf`, derives supervision from the
known family layers, hides raw layer names from model features, builds primitive
nodes with geometric features, connects them with spatial/snap-proximity edges,
and compares a feature-only baseline to a small 2-layer graph convolution.
The current implementation is NumPy-only so it runs before PyTorch/PyG is added.

## Future-Facing Evaluation

Once the first annotation path works, add tests that match the product loop:

- symmetry shift: drafting style, rotation, scale, partial observation, and
  modality changes
- composition shift: larger assemblies, new room/floor compositions, deeper
  hierarchy, and unusual valid constraint combinations
- residual repair: start from broken graph states and measure minimal valid
  edits, structure preservation, and validator-residual reduction
- workflow realism: use revision traces to predict or rank the next competent
  correction

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

Optional later probes:

- temporal-straightening loss over synthetic or real edit trajectories
- entropy monitoring for any sequential edit policy
- hardware-aware comparison of PyG message passing vs flattened/custom batched
  tensor paths
