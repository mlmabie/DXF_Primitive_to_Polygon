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

For current sensemaking:

1. [`sensemaking/README.md`](sensemaking/README.md)
2. [`sensemaking/voice_and_vision_ledger.md`](sensemaking/voice_and_vision_ledger.md)
3. [`sensemaking/q01_gnn_experience_and_vision.md`](sensemaking/q01_gnn_experience_and_vision.md)
4. [`sensemaking/q02_frameworks_scale_and_systems.md`](sensemaking/q02_frameworks_scale_and_systems.md)

For the derived technical plan:

1. [`01_problem_framing.md`](01_problem_framing.md)
2. [`02_graph_representations.md`](02_graph_representations.md)
3. [`03_predictive_editing.md`](03_predictive_editing.md)
4. [`04_research_map.md`](04_research_map.md)
5. [`notes/augrade_representation_reading_notes.md`](notes/augrade_representation_reading_notes.md)
6. [`notes/augrade_strategy_from_model_prep.md`](notes/augrade_strategy_from_model_prep.md)
7. [`05_annotation_intake.md`](05_annotation_intake.md)
8. [`experiments/README.md`](experiments/README.md)

## Link To Existing Work

This plan builds on the current deterministic scaffold:

- [`../README.md`](../README.md) describes the DXF primitive-to-polygon solver.
- [`../reference/research/thesis.md`](../reference/research/thesis.md) states
  the evidence-first thesis.
- [`../reference/research/programmatic_vs_contextual_merges.md`](../reference/research/programmatic_vs_contextual_merges.md)
  motivates pair-relation learning.
- [`../reference/experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md`](../reference/experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md)
  gives the previous staged experiment plan.
- [`notes/augrade_representation_reading_notes.md`](notes/augrade_representation_reading_notes.md)
  folds the cited representation, co-design, calibration, and memory papers
  into this plan.
- [`notes/augrade_model_prep_import.md`](notes/augrade_model_prep_import.md)
  records the older model-prep workspace that was consolidated into this
  branch.
- [`notes/augrade_strategy_from_model_prep.md`](notes/augrade_strategy_from_model_prep.md)
  distills the pre-take-home strategy notes into first-class primitives,
  workflow exhaust, residual edits, future-proofing, and compute-aware
  implementation guidance.

The new layer-blind assumption is stricter than the current solver. Existing
layer priors should be treated as optional evaluation metadata, not as model
inputs for the first GNN pass.

## Working Principle

Vector first, raster second.

The graph should keep exact coordinates, primitive type, curve parameters,
connectivity, containment, overlap, and provenance. Raster views can be used as
image chips for local context or for comparison against raster baselines, but
the authoritative object should remain the vector graph.
