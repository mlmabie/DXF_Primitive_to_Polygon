# Future Research Repo Blueprint

This branch can stay inside the DXF repo for now, but the work probably wants
a standalone repo once it becomes broader than the take-home artifact.

## Split Trigger

Create the standalone repo when *any* of these is true:

- the research docs no longer need the local DXF solver to make sense
- a second CAD/BIM example arrives that is not the airport mezzanine
- implementation starts for graph export, baselines, or annotation intake
  (i.e., this leaves the docs-only stage)
- the work becomes a reusable thesis/model-design package rather than a branch
  attached to the take-home

Until any of those fires, this branch is the incubation surface.

## Working Name

Pick the name only when the new repo is being created. Candidates:

- `augrade-spatial-gnn-research`
- `spatial-world-interface`
- `augrade-model-research`

The name should preserve "world interface" as the center of gravity, not
"GNN architecture."

## Concrete Migration Plan

When the trigger fires, run these steps in order.

### Step 1: Stay In Place (Take-Home-Specific)

These files belong to the DXF artifact and should *not* move:

- `tokenize_dxf.py`, `DESIGN.md`, the airport-doors DXF, `out/` outputs
- `agent_merge_review.py`, `agent_labels.json`
- `augrade/` library and `augrade/review/` subpackage
- `reference/process/*` (per-file analyses tied to this drawing)
- `reference/research/thesis.md` (file-backed claims tied to this artifact)
- `reference/research/programmatic_vs_contextual_merges.md`
- `reference/experiments/*` (latent-dimensions memo and checklist that
  reference per-family evidence in this drawing)

### Step 2: Promote To The New Repo

| Source                                                  | Destination in new repo                       |
|---------------------------------------------------------|-----------------------------------------------|
| `gnn_plan/TALK_TRACK.md`                                | `README.md` (top-level pitch)                 |
| `gnn_plan/SYSTEM_SPEC.md`                               | `model_plan/system_spec.md`                   |
| `gnn_plan/01_problem_framing.md`                        | `research/problem_framing.md`                 |
| `gnn_plan/02_graph_representations.md`                  | `model_plan/graph_representation.md`          |
| `gnn_plan/03_predictive_editing.md`                     | `model_plan/predictive_editing.md`            |
| `gnn_plan/04_research_map.md`                           | `research/literature_map.md`                  |
| `gnn_plan/05_annotation_intake.md`                      | `data_contracts/annotation_schema.md`         |
| `gnn_plan/sensemaking/*`                                | `sensemaking/`                                |
| `gnn_plan/notes/augrade_strategy_from_model_prep.md`    | `research/representation_boundary.md`         |
| `gnn_plan/notes/augrade_representation_reading_notes.md`| `research/reading_notes.md`                   |
| `gnn_plan/notes/augrade_qa_alpha_refinement.md`         | `research/qa_alpha_refinement.md`             |
| `gnn_plan/experiments/README.md`                        | `experiments/README.md`                       |
| `reference/research/research_extension.md`              | `research/representation_boundary_dxf_case.md` (archived) |

### Step 3: Top-Level Shape

```text
README.md                           # talk-track pitch + reading order
sensemaking/
  voice_and_vision_ledger.md
  q01_gnn_experience_and_vision.md
  q02_frameworks_scale_and_systems.md
  open_questions.md                 # promote from notes when this exists
research/
  literature_map.md
  problem_framing.md
  representation_boundary.md
  reading_notes.md
  qa_alpha_refinement.md
  representation_boundary_dxf_case.md
  workflow_exhaust.md               # spin up when traces are accessible
model_plan/
  system_spec.md
  graph_representation.md
  predictive_editing.md
  rl_search_later.md                # only when RL stage is real
experiments/
  README.md
  graph_export/
  baselines/
  relation_discovery/
  edit_trajectories/
data_contracts/
  annotation_schema.md
  graph_manifest_schema.md          # extract from SYSTEM_SPEC.md tables
  workflow_trace_schema.md          # spin up when traces are accessible
```

### Step 4: Cross-Repo Wiring

- pin a commit hash of this DXF repo as the case-study reference inside
  `representation_boundary_dxf_case.md`
- copy `agent_labels.json` as a frozen snapshot if any baseline experiment
  will use it
- keep a `compat/dxf_case_study.md` page in the new repo that lists the
  exact commands to reproduce the artifact from this DXF repo, so the new
  repo never has to vendor the airport-doors file
- do not move the DXF file itself; large binary in a research repo is a
  smell

### Step 5: Cleanup On The DXF Side

- leave `gnn_plan/` here as a redirect: a one-line README pointing to the
  new repo
- keep `reference/research/research_extension.md` because it stays
  meaningful as the originating case study, but link it from the new repo
- run `git mv` for the moved files (preserves blame); use `git rm` only for
  the redirect-only `gnn_plan/` once the redirect README is committed
