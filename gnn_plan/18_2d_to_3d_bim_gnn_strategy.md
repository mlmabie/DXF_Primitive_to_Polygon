# 2D Drawings To 3D BIM — GNN Strategy

This is the CTO-facing version of the plan: what exact kind of GNN I would
start with, what it predicts, how it is trained, how it connects to frontier
AI, and what role this work should occupy in the product.

## One-Sentence Strategy

Do not train a GNN to hallucinate BIM from raw drawing vectors. Train a
heterogeneous graph model to recover object identity, typed relations, and
parametric BIM-lifting decisions over deterministically formed 2D candidates;
then let exact geometry, validators, and review bands decide what becomes
trusted 3D BIM state.

## Why This Is The Right GNN Strategy

The hard problem is not "classify every line." The hard problem is converting
authored 2D evidence into persistent object identity: walls, openings, rooms,
shafts, symbols, annotations, and the relations that let those objects lift
into BIM.

The strategy is right because it puts each responsibility in the layer that can
actually defend it:

- deterministic geometry owns parsing, snapping, closure, exact coordinates,
  source handles, and provenance;
- supervector formation owns over-generating candidate objects from primitives;
- sparse pair-relation scoring is the first learned baseline and the GNN's
  competitor;
- the GNN owns only residual context propagation where typed neighborhoods beat
  sparse geometry;
- BIM-lifting heads predict parametric decisions, not arbitrary meshes;
- validators decide whether a proposed BIM state is usable, reviewable, or
  rejected;
- frontier models call calibrated tools and spend tokens on judgment rather
  than rediscovering geometry.

The central evidence signal is HATCH-IoU: companion HATCH layers give a
self-supervised target for shape correctness that source-entity coverage misses
by construction.

## Starting Architecture

The first architecture should be boring on purpose: a heterogeneous,
relation-aware GraphSAGE baseline with edge-conditioned geometry features. It
should be strong enough to test the representation boundary and simple enough
to falsify.

```text
Input:
  PyG HeteroData graph
  node types:
    primitive, supervector, face, annotation, level_or_sheet, bim_candidate
  edge types:
    composed_of, bounds, inside, labels, measures, points_to,
    parallel_offset, continuation, companion_hatch, opens_into,
    same_symbol_family, duplicate_footprint, conflicts_with, lifts_to

Encoder:
  2-3 rounds of relation-aware heterogeneous GraphSAGE
  edge-conditioned MLPs for geometric edge attributes
  residual connections + LayerNorm
  hidden size around 128-256d

Readout:
  node heads for class/type
  edge heads for relation confidence
  supervector heads for BIM lifting parameters
  conformal calibration for accept / route_to_expert / reject
```

Concrete PyG shape:

```python
from torch_geometric.data import HeteroData
from torch_geometric.nn import HeteroConv, SAGEConv

data = HeteroData()

data["primitive"].x = primitive_features
data["supervector"].x = supervector_features
data["face"].x = face_features
data["annotation"].x = annotation_features
data["level_or_sheet"].x = level_features
data["bim_candidate"].x = bim_candidate_features

# Exact CAD geometry stays outside the tensor.
data["primitive"].geom_id = primitive_geom_ids
data["supervector"].geom_id = supervector_geom_ids
data["face"].geom_id = face_geom_ids

conv = HeteroConv(
    {
        ("primitive", "parallel_offset", "primitive"): SAGEConv((-1, -1), 256),
        ("primitive", "continuation", "primitive"): SAGEConv((-1, -1), 256),
        ("primitive", "companion_hatch", "primitive"): SAGEConv((-1, -1), 256),
        ("primitive", "composes", "supervector"): SAGEConv((-1, -1), 256),
        ("supervector", "bounds", "face"): SAGEConv((-1, -1), 256),
        ("annotation", "labels", "supervector"): SAGEConv((-1, -1), 256),
        ("annotation", "measures", "supervector"): SAGEConv((-1, -1), 256),
        ("supervector", "opens_into", "supervector"): SAGEConv((-1, -1), 256),
        ("supervector", "lifts_to", "bim_candidate"): SAGEConv((-1, -1), 256),
    },
    aggr="sum",
)
```

The graph tensor carries relational features and stable geometry pointers.
Exact CAD geometry remains in a sibling `geom_pack`, so embeddings can warp
while validators and BIM lifting operate on source-of-truth coordinates.

## What Makes It 2D-To-3D

The model does not emit a freeform 3D mesh. It emits parametric BIM hypotheses
with evidence pointers:

- wall footprint source: `geom_id` of centerline, outline, or HATCH boundary;
- wall thickness, base level, top constraint, and height;
- opening host wall, position along wall, width, height, sill/head height;
- room/space face, level, boundary membership, and shaft/corridor/room type;
- column footprint, level span, and structural/nonstructural classification;
- annotation-to-object mappings that set BIM parameters or constraints.

The lift from 2D to 3D is therefore a set of typed decisions:

```text
2D object identity + relation recovery + parameter inference
-> candidate BIM elements
-> validator-bounded 3D state
```

This keeps the output editable and auditable. If the model says a candidate is
a wall, the BIM writer still knows which exact 2D geometry, annotation, and
relation evidence supported that wall.

## Output Heads

### Element Class Head

Predicts the class of each supervector or BIM candidate:

```text
wall / column / door / window / slab_edge / shaft / room / symbol / unknown
```

Loss: cross entropy or focal cross entropy.

### Relation Heads

Predict typed edge existence/confidence:

```text
door hosted_by wall
annotation labels opening
dimension measures wall span
two carriers form the same wall mass
face bounded_by wall set
two symbols belong to same family
```

Loss: multi-label binary cross entropy per relation. Not softmax: relations
are not mutually exclusive.

### Wall-Lifting Head

For each wall candidate:

```text
class: wall / not_wall / unknown
thickness: regression or candidate-bin classification
base_level: classification
top_constraint: classification
height: regression or annotation-derived class
structural_flag: binary/multiclass
```

Loss:

```text
L_wall =
  CE(wall_class)
+ SmoothL1(thickness)
+ SmoothL1(height)
+ BCE(host_or_adjacency_relations)
+ validator_penalty(unclosed_or_impossible_wall_state)
```

### Opening Head

For door/window candidates:

```text
host_wall_id
position_along_host
width
height
sill_or_head_height
opening_type
swing_or_handedness when visible
```

Loss:

```text
L_opening =
  CE(opening_type)
+ BCE(host_wall)
+ SmoothL1(position_along_wall)
+ SmoothL1(width, height, sill_or_head)
+ containment_penalty(opening_not_inside_host_wall)
```

### Space / Room Head

For bounded faces:

```text
room / shaft / corridor / terrace / unknown
space boundary membership
level
floor_to_floor_height if inferable
```

Loss:

```text
L_space =
  CE(space_type)
+ BCE(boundary_membership)
+ IoU(predicted_space_boundary, held_out_hatch_or_BIM_space)
+ adjacency_consistency_loss
```

### Cross-View / Level Consistency Head

When plans, sections, elevations, or multiple floors are available:

```text
same_element_across_views
vertical_stack_relation
level_alignment
section_plan_correspondence
```

Loss:

```text
L_cross_view =
  contrastive_same_element
+ BCE(vertical_stack_relation)
+ SmoothL1(level_elevation)
```

## Total Loss

The full objective is multi-task, but each term is gated by data availability:

```text
L_total =
  lambda_1 * L_element_class
+ lambda_2 * L_relation_BCE
+ lambda_3 * L_hatch_IoU
+ lambda_4 * L_parametric_geometry
+ lambda_5 * L_annotation_alignment
+ lambda_6 * L_rewrite_invariance
+ lambda_7 * L_cross_view_consistency
+ lambda_8 * L_validator_residual
+ lambda_9 * L_calibration
```

Definitions:

```text
L_hatch_IoU = 1 - IoU(predicted_wall_or_column_footprint,
                      held_out_companion_HATCH)

L_rewrite_invariance = E || f(x) - f(g(x)) ||^2

L_validator_residual =
  penalty(unclosed_rooms)
+ penalty(openings_outside_host_walls)
+ penalty(duplicate_footprints)
+ penalty(impossible_containment)
+ penalty(clearance_or_clash_violations)
```

Calibration is not optional. Heads should publish review bands:

```text
accept / route_to_expert / reject
```

with drawing-level conformal calibration. The product needs bounded decisions,
not just logits.

## Supervision Sources

Use three sources in order:

1. **Programmatic supervision.** Existing solver labels, HATCH pairs, closure,
   containment, parallel offsets, T-junctions, merge candidates, validator
   accept/reject outcomes.
2. **Synthetic supervision from BIM.** Take known BIM models, generate 2D
   drawings/views, and train the model to recover the source BIM elements and
   relations. This is the cleanest 2D-to-3D signal when available.
3. **Real drawing supervision.** Expert corrections, annotations, HATCH-IoU,
   dimensions, schedules, review outcomes, and workflow exhaust.

The train/test split must be by drawing or project, not by entity, because
entity splits leak drafter style and repeated symbols.

## Architecture Search Plan

Start conservative. Search only after the substrate and sparse baselines exist.

1. **Heterogeneous GraphSAGE baseline.** First implementation. Stable, local,
   easy to debug.
2. **Edge-conditioned message passing.** Add when gap distance, offset,
   angle, IoU, or containment margin materially improves relations.
3. **GATv2 on annotation ambiguity.** Use attention where many nearby objects
   compete for one text/leader/dimension target.
4. **PNA for repeated motifs.** Try where degree and neighborhood statistics
   matter: mullion grids, repeated symbols, room-boundary neighborhoods.
5. **Hierarchical pooling.** Primitive -> supervector -> face/room -> BIM
   element. This is likely necessary for trusted BIM lifting.
6. **DEQ-GNN / fixed-point variant.** Later, if edit propagation behaves like
   convergence over graph state: edit -> propagate constraints -> validators
   stabilize.
7. **Graph transformer counterfactual.** Keep as an ablation for global
   context, not as the first bet. The current bottleneck is object formation,
   relation typing, calibration, and validator-bounded lifting, not long-token
   mixing.

The line: start with hetero GraphSAGE, then let the failure modes earn more
complex machinery.

## Future Strategy With Frontier AI

Frontier models should not own geometry. They should orchestrate calibrated
tools:

- call the wall candidate scorer;
- call the hatch-outline pair scorer;
- call annotation-to-object resolution;
- inspect validator residual summaries;
- propose which stable motif should compile into a deterministic rule;
- explain why an item was routed to expert review.

The frontier model spends tokens on judgment, ambiguity, synthesis, and
planning. The graph tools provide bounded answers with `does_not_do` contracts.

## Product-Research Roadmap

```text
Phase 0: deterministic graph export
Phase 1: annotation alignment
Phase 2: sparse pair-relation baseline + conformal bands
Phase 3: HATCH-IoU SSL pretraining
Phase 4: supervised object/relation heads
Phase 5: BIM lifting heads for walls/openings/rooms
Phase 6: validator-bounded repair actions
Phase 7: frontier-model orchestration over tool-callable heads
```

GPU-heavy experiments belong behind those gates:

- low-dimensional autoencoders over primitive/supervector neighborhoods;
- STE or binary-latent probes for discrete rule candidates;
- SAE-style probes for validator residual directions;
- verifier environments for typed edit repair once validators mature.

A100 access changes experiment appetite, not the first-principles order.

## Role Alignment

The work is broader than "Gen AI developer." The appropriate role is closer to:

- Principal AI Engineer, 2D-to-3D BIM Automation;
- Senior MTS, BIM Intelligence;
- Principal / Senior Research Engineer, Geometric AI Systems;
- AI Systems Architect for CAD-to-BIM Automation.

The role owns the intelligence layer that turns messy 2D authored drawings into
trusted 3D BIM state: vector extraction, graph state, relation recovery,
learned residual scoring, deterministic validators, and frontier-model tool
orchestration.

## CTO-Facing Summary

I would not start with a graph transformer or an end-to-end BIM generator. I
would start with a hetero GraphSAGE encoder over a deterministic 2D evidence
graph, use HATCH-IoU and programmatic validators as supervision, and train
specific heads for object identity, relations, and BIM lifting parameters. The
GNN earns its keep only if it beats sparse pair-relation baselines on
drawing-level holdouts. Frontier AI then calls these calibrated heads as tools
and spends its reasoning budget on ambiguity, synthesis, and rule promotion.
