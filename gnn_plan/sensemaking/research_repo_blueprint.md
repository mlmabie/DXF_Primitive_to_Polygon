# Future Research Repo Blueprint

This branch can stay inside the DXF repo for now, but the work probably wants a
standalone repo once it becomes broader than the take-home artifact.

## Working Name

Possible names:

- `augrade-spatial-gnn-research`
- `spatial-world-interface`
- `augrade-model-research`

The name should preserve the idea that this is about a world interface, not
only about GNN architecture.

## Proposed Top-Level Shape

```text
README.md
sensemaking/
  voice_and_vision_ledger.md
  q01_gnn_experience_and_vision.md
  q02_frameworks_scale_and_systems.md
  open_questions.md
research/
  literature_map.md
  representation_boundary.md
  first_class_primitives.md
  workflow_exhaust.md
model_plan/
  graph_representation.md
  baselines.md
  predictive_editing.md
  rl_search_later.md
experiments/
  graph_export/
  baselines/
  relation_discovery/
  edit_trajectories/
data_contracts/
  annotation_schema.md
  graph_manifest_schema.md
  workflow_trace_schema.md
```

## What Moves First

From this branch:

- `gnn_plan/sensemaking/`
- `gnn_plan/notes/augrade_strategy_from_model_prep.md`
- `gnn_plan/notes/augrade_representation_reading_notes.md`
- `gnn_plan/notes/augrade_qa_alpha_refinement.md`
- `gnn_plan/01_problem_framing.md`
- `gnn_plan/02_graph_representations.md`
- `gnn_plan/03_predictive_editing.md`
- `gnn_plan/04_research_map.md`
- `gnn_plan/05_annotation_intake.md`
- `gnn_plan/experiments/README.md`

What should stay in this DXF repo:

- direct solver documentation
- take-home-specific extraction notes
- DXF artifact analysis
- references that only make sense because of the Airport mezzanine file

## Split Trigger

Create the standalone repo when one of these happens:

- the research docs no longer depend on the local DXF solver
- there are multiple CAD/BIM examples
- implementation starts for graph export or model baselines
- the work becomes a reusable thesis/model-design package rather than a branch
  attached to the take-home

Until then, this branch is a good incubation surface.
