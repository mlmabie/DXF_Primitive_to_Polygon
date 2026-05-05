# Graph Representations

## Candidate Graphs

### 1. Endpoint Graph

Nodes are snapped endpoints and intersections. Edges are primitive spans.

Best for:

- closure
- face recovery
- detecting gaps
- preserving exact topology

Limits:

- too low-level for direct element classification
- high node count
- arcs, hatches, and symbols need careful normalization

### 2. Primitive-As-Node Graph

Nodes are original CAD entities or faceted primitive carriers. Edges encode
nearby, touching, intersecting, parallel, collinear, containing, or overlapping
relations.

Best for:

- layer-blind CAD entity classification
- entity-level annotations
- preserving raw provenance

Limits:

- many architectural objects are multi-primitive
- message passing has to learn composition from scratch unless we add
  supervector nodes

### 3. Supervector Graph

Nodes are composed candidates produced by deterministic grouping:

- chains
- closed loops
- hatch boundaries
- repeated cells
- candidate symbols
- candidate wall faces

Edges encode pair relations such as same-element, adjacent, crosses, blocks,
parallel-offset, continuation, containment, or duplicate-footprint.

Best for:

- representative element classification
- merge decisions
- human annotation review
- low-label experiments

Limits:

- depends on candidate generation quality
- bad grouping can hide primitive-level evidence unless composition is retained

### 4. Region / Face Graph

Nodes are bounded faces or regions. Edges are shared boundaries, doors,
openings, adjacency, containment, or visibility.

Best for:

- rooms
- shell reasoning
- plumbing route likelihood
- cascade impacts that flow through spaces

Limits:

- requires robust face recovery
- not enough by itself for symbol and detail classification

### 5. Heterogeneous Multi-Level Graph

Use multiple node types:

- `primitive`
- `endpoint`
- `supervector`
- `face`
- `component`

Use typed edges:

- `touches`
- `intersects`
- `parallel_to`
- `collinear_with`
- `offset_from`
- `contains`
- `inside`
- `composed_of`
- `adjacent_to`
- `same_element_candidate`
- `route_candidate`
- `conflicts_with`

This is the recommended target representation. It preserves low-level detail
while giving the model higher-level places to attach labels.

## Node Features

Common features:

- primitive type
- normalized coordinates plus absolute scale metadata
- length, area, perimeter, curvature, arc angle
- orientation encoded as sin/cos
- bbox dimensions and aspect ratio
- compactness
- closure flag
- line width or CAD width when available
- source carrier kind
- local density
- number of intersections
- number of near endpoints
- local repeated-spacing statistics

Layer name should be excluded from the first layer-blind experiment. It can be
retained as hidden provenance for debugging and later ablation.

## Edge Features

Pair features:

- endpoint gap
- minimum distance
- intersection type
- angle difference
- axial overlap
- lateral offset
- bbox IoU
- containment ratio
- area ratio
- continuation score
- crossing penalty
- shared boundary length
- route cost through free space

These edge features also serve as a non-GNN baseline. The GNN has to beat this
baseline to justify itself.

## Recommended MVP

1. Export a layer-blind primitive table from the current parser.
2. Generate deterministic supervector candidates without using layer names.
3. Build a typed primitive/supervector graph.
4. Map the first annotation examples onto graph node ids.
5. Train or hand-score simple baselines:
   - node feature classifier
   - edge relation classifier
   - connected-component heuristic
6. Add a small graph model only after the baseline exposes where neighborhood
   propagation helps.

The first graph model should be small and inspectable: GraphSAGE, GAT/GATv2,
PNA, or a lightweight heterogeneous GNN. The task is not to discover CAD
geometry from scratch; it is to propagate local evidence across a structured
candidate graph.

