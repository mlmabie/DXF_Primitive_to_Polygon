# GNN Plan Setup

This folder is the working surface for the next phase: graph learning over
DWG/DXF vector soup, plus predictive modeling for architectural systems and
edit impacts. It is intentionally top-level so it can stay inside this repo or
be split into a standalone repo later.

For the short front door, original project prompt, KISS first slice, and
reader contract, start with [`00_START_HERE.md`](00_START_HERE.md). The rest of this
folder is a workbench for making that plan executable and falsifiable.

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

Read in this order:

1. [`00_START_HERE.md`](00_START_HERE.md) — original project prompt, reader
   contract, KISS path, and epistemic-status model.
2. [`prompt.md`](prompt.md) — current objective.
3. [`TALK_TRACK.md`](TALK_TRACK.md) — single-page talk track for the
   follow-up conversation, with per-claim citation anchors.
4. [`SYSTEM_SPEC.md`](SYSTEM_SPEC.md) — concrete buildable system: modules,
   data contracts, eval bar, and the first slice (Phases 0–2).
5. [`SENSEMAKING.md`](SENSEMAKING.md) — compact consolidation of the useful
   support notes and current research judgment.
6. [`06_example_insights.md`](06_example_insights.md) — example-driven update
   from the three received annotated DWGs.
7. [`13_primary_answer.md`](13_primary_answer.md) — direct answer to the
   vector-soup-to-supervector GNN training question.
8. [`14_architecture_training_minutia.md`](14_architecture_training_minutia.md)
   — model architecture, losses, sampling, calibration, and ablation details.
9. [`15_counterfactual_architectures.md`](15_counterfactual_architectures.md)
   — why not simpler homogeneous, raster-first, or end-to-end alternatives.
10. [`07_source_review_prompts.md`](07_source_review_prompts.md) — paper/source
   review queue with source links and per-source prompts.
11. [`08_scope_resolver.md`](08_scope_resolver.md) — trainable scope resolver:
   objective/edit/residual -> minimal sufficient subgraph.
12. [`09_precision_conditioning.md`](09_precision_conditioning.md) — stable
   geometry makes good change cheap.
13. [`10_operating_doctrine_addendum.md`](10_operating_doctrine_addendum.md) —
   pessimist route, hybrid GNN/FM/validator/memory doctrine, and quality loops.
14. [`11_paper_trajectory.md`](11_paper_trajectory.md) — publishable-paper
    ladder and sequencing gates.
15. [`12_world_model_bridge.md`](12_world_model_bridge.md) — bridge from raw
    3D / VLA / JEPA / world-model encoders into a multiscale graph substrate.
16. [`16_epistemic_controls.md`](16_epistemic_controls.md) — controls against
    reference spoofing, approach drift, over-claiming, and cognitive-security
    drift in the research workbench.
17. [`04_research_map.md`](04_research_map.md) — citation shelf.

Supporting docs:

- [`01_problem_framing.md`](01_problem_framing.md)
- [`02_graph_representations.md`](02_graph_representations.md)
- [`03_predictive_editing.md`](03_predictive_editing.md)
- [`05_annotation_intake.md`](05_annotation_intake.md)
- [`CONSOLIDATION_GUIDE.md`](CONSOLIDATION_GUIDE.md)
- [`experiments/README.md`](experiments/README.md)

## Epistemic Posture

Because of the wide and deep scope of the plan, this folder separates
commitments, hypotheses, candidate mechanisms, counterfactuals, and reference
prompts. Use [`16_epistemic_controls.md`](16_epistemic_controls.md) and
`reference/reviews/claim_ledger_template.csv` to track which claims have been
source-checked, baseline-tested, reproduced, or revised.

## Link To Existing Work

This plan builds on the current deterministic scaffold:

- [`../README.md`](../README.md) describes the DXF primitive-to-polygon solver.
- [`../reference/research/thesis.md`](../reference/research/thesis.md) states
  the evidence-first thesis.
- [`../reference/research/programmatic_vs_contextual_merges.md`](../reference/research/programmatic_vs_contextual_merges.md)
  motivates pair-relation learning.
- [`../reference/experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md`](../reference/experiments/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md)
  gives the previous staged experiment plan.
- [`SENSEMAKING.md`](SENSEMAKING.md) consolidates the useful generated support
  notes into the current research judgment.

The new layer-blind assumption is stricter than the current solver. Existing
layer priors should be treated as optional evaluation metadata, not as model
inputs for the first GNN pass.

## Working Principle

Vector first, raster second.

The graph should keep exact coordinates, primitive type, curve parameters,
connectivity, containment, overlap, and provenance. Raster views can be used as
image chips for local context or for comparison against raster baselines, but
the authoritative object should remain the vector graph.
