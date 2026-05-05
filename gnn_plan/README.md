# GNN Plan Setup

This folder is the working surface for the next phase: graph learning over
DWG/DXF vector soup, plus predictive modeling for architectural systems and
edit impacts. It is intentionally top-level so it can stay inside this repo or
be split into a standalone repo later.

## Current Assumptions

- Inputs are DWG and DXF.
- Treat all primitives as if they are on one effective layer.
- Do not rely on layer names, layer groups, or authored object metadata.
- Input geometry is an unsorted soup of primitives: lines, arcs, polylines,
  circles, hatches, blocks once exploded, and similar CAD carriers.
- The first learned target is classification of primitives or composed
  "supervectors" into representative architectural elements.
- Detail preservation matters. Rasterization can provide auxiliary context, but
  should not be the primary representation if it loses exact vector geometry.

## Priority Threads

1. **Classification with graph methods.**
   Build a graph representation over primitive/supervector candidates and test
   whether graph structure helps classify them into walls, doors, fixtures,
   plumbing, annotations, shell elements, or other representative classes.

2. **Predictive modeling and editing.**
   Explore two use cases:

   - infer likely systems inside an architectural shell, such as how plumbing
     fits given walls, rooms, shafts, fixtures, and access constraints
   - predict what changes, conflicts, or dependencies cascade after an edit

## Reading Order

1. [`01_problem_framing.md`](01_problem_framing.md)
2. [`02_graph_representations.md`](02_graph_representations.md)
3. [`03_predictive_editing.md`](03_predictive_editing.md)
4. [`04_research_map.md`](04_research_map.md)
5. [`05_annotation_intake.md`](05_annotation_intake.md)
6. [`experiments/README.md`](experiments/README.md)

## Link To Existing Work

This plan builds on the current deterministic scaffold:

- [`../README.md`](../README.md) describes the DXF primitive-to-polygon solver.
- [`../reference/research/thesis.md`](../reference/research/thesis.md) states
  the evidence-first thesis.
- [`../reference/research/programmatic_vs_contextual_merges.md`](../reference/research/programmatic_vs_contextual_merges.md)
  motivates pair-relation learning.
- [`../reference/experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md`](../reference/experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md)
  gives the previous staged experiment plan.

The new layer-blind assumption is stricter than the current solver. Existing
layer priors should be treated as optional evaluation metadata, not as model
inputs for the first GNN pass.

## Working Principle

Vector first, raster second.

The graph should keep exact coordinates, primitive type, curve parameters,
connectivity, containment, overlap, and provenance. Raster views can be used as
image chips for local context or for comparison against raster baselines, but
the authoritative object should remain the vector graph.

