# Augrade Model Prep Import

Date: 2026-05-05

Source workspace:

`/Users/mabie/agent-workspace/augrade-model-prep`

This note consolidates the older pre-take-home prep workspace into the GNN plan
branch. The source workspace mixed canonical interview materials, public
company-framing notes, and deeper research notes. The durable technical content
has been folded into:

- `augrade_strategy_from_model_prep.md`
- `augrade_representation_reading_notes.md`
- `../01_problem_framing.md`
- `../02_graph_representations.md`
- `../03_predictive_editing.md`
- `../04_research_map.md`

## Source Categories

### Canonical Prep

- `docs/augrade_model_focus_from_questionnaire.md`
- `docs/augrade_interview_prep_keshav.md`
- `docs/augrade_recruiter_questionnaire_charlie_final.md`
- `docs/augrade_founder_call_focus.md`
- `docs/augrade_thesis_compressed.md`
- `docs/augrade_spoken_versions.md`

Use these for spoken framing and interview-specific phrasing. The reusable
technical core is the representation boundary, graph role, validator boundary,
RL/search placement, and compute-aware system bias.

### Context Guardrails

- `context/source_map.md`
- `context/current_public_framing_2026-04-08.md`
- `context/linkedin_thread_march_2026.md`

Use these to avoid mixing older AR/VR-era public material with newer
preconstruction/project-delivery framing. The current working read is:

> Augrade is best treated as AI-powered preconstruction and project-delivery
> automation: turning drawings and requirements into editable BIM/CAD outputs,
> take-offs, schedules, documentation, and downstream construction artifacts.

### Deep Research Notes

- `research/augrade-research-notebook-spatial-world-models.md`
- `research/augrade-representation-thesis-compressed.md`
- `research/first-class-primitives-for-spatial-models.md`
- `research/future-proofing-spatial-models-for-invariance-and-compositionality.md`
- `research/augrade-gnn-engineer.md`

Use these as research fuel, not direct product claims. They contribute the
first-class primitive stack, residual edit framing, graph-program hybrid idea,
workflow-exhaust moat, and future-proofing rubric.

## Consolidation Decision

I did not copy the old prep workspace wholesale. Some files are interview
duplicates, some are Obsidian mirrors with front matter, and one is a PDF copy
of a questionnaire already represented elsewhere. Instead, the GNN setup branch
now carries compact notes that preserve the parts useful for model planning.

## Working Rule

If a future note sounds like broad interview positioning, route it to
`gnn_plan/notes/`. If it defines a graph representation, experiment, annotation
schema, or model interface, promote the relevant part into the main numbered
GNN plan files.
