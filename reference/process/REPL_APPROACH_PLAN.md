# REPL Approach Plan

Date: 2026-04-16

## Goal

Build a domain REPL for the DXF cleanup / extraction / provenance / merge workflow.

This should not be a raw Python shell. It should be an interactive workbench over the actual project objects:

- DXF document
- normalization state
- provenance state
- polygon candidates
- merge candidates
- expert labels
- learned scorers
- emitted review artifacts

The REPL should let a human move fluidly between:

- geometry inspection
- provenance inspection
- rule tuning
- merge labeling
- model experimentation
- artifact emission

## Design Principle

The REPL should be stateful, typed, and provenance-first.

Not:

- `python` with helper imports
- a notebook
- a thin wrapper around shell commands

But:

- a session with explicit domain objects
- commands over those objects
- inspectable intermediate state
- deterministic artifact emission

## State Model

One session object should hold:

```text
session
  input_dxf
  doc
  normalization
  provenance
  extraction
  polygons
  merge_graph
  rules
  labels
  models
  artifacts
```

Suggested internal layout:

- `doc`
  - path
  - file metadata
- `normalization`
  - anomalies
  - merge groups
  - layer map
  - id prefix map
- `provenance`
  - layer summaries
  - variant groups
  - entity-level provenance
- `extraction`
  - snap tolerance
  - metrics
  - polygon families
- `merge_graph`
  - candidate pairs
  - current rules
  - current accepted edges
  - components
- `labels`
  - expert labels
  - import/export path history
- `models`
  - heuristic weights
  - prototype memory
  - trained edge scorers
- `artifacts`
  - dashboard paths
  - merge lab paths
  - DXF output paths

## Existing Modules To Reuse

The REPL should sit on top of the existing code, not replace it:

- [`normalize_layers.py`](/Users/malachi/augrade_takehome/normalize_layers.py)
- [`tokenize_dxf.py`](/Users/malachi/augrade_takehome/tokenize_dxf.py)
- [`provenance_utils.py`](/Users/malachi/augrade_takehome/provenance_utils.py)
- [`build_dashboard.py`](/Users/malachi/augrade_takehome/build_dashboard.py)
- [`build_merge_lab.py`](/Users/malachi/augrade_takehome/build_merge_lab.py)
- [`build_labeled_merge_dataset.py`](/Users/malachi/augrade_takehome/build_labeled_merge_dataset.py)
- [`emit_dxf.py`](/Users/malachi/augrade_takehome/emit_dxf.py)
- [`run_hitl_pipeline.py`](/Users/malachi/augrade_takehome/run_hitl_pipeline.py)

The REPL should call library-like functions from these modules, not shell out unless there is no clean import path.

## Command Surface

### Session Commands

```text
open "Airport Doors_MEZZ.dxf"
status
save-session .augrade-session.json
load-session .augrade-session.json
reset
```

### Normalization Commands

```text
normalize
normalize --auto-heal
normalize --strict
layers anomalies
layers summary
layers variants curtain_walls
layers show "A-GLAZING-FULL"
```

### Extraction Commands

```text
extract --snap 0.5
extract metrics
polys count
polys list walls
polys list walls --multi
show wall_0042
show cw_0017
```

### Provenance Commands

```text
provenance wall_0042
provenance layers wall_0042
provenance variants wall_0042
provenance compare "A-GLAZING FULL" "A-GLAZING-FULL"
```

### Merge Commands

```text
pairs list walls
pair walls:3:5
merge score walls:3:5
rules show walls
rules set walls.max_boundary_gap 32
rules set walls.w_alignment 1.8
recompute merges walls
components walls
```

### Labeling Commands

```text
label positive walls:3:5
label negative walls:19:22
label clear walls:3:5
labels summary
labels export labels/walls_round1.json
labels import labels/walls_round1.json
```

### Modeling Commands

```text
dataset export labels/walls_round1.json out/labeled_pairs
train heuristic walls
train memory walls
train edge-model walls
eval edge-model walls
ablate walls thickness_rel_diff
```

### Artifact Commands

```text
emit dashboard out_hitl
emit merge-lab out_hitl
emit dxf out/review.dxf
emit bundle out_hitl
open-artifact dashboard
open-artifact merge-lab
```

## Output Style

Every inspect command should be compact, structured, and provenance-rich.

Example:

```text
augrade> show a_glaz_mull_multi_0017

id: a_glaz_mull_multi_0017
family: curtain_walls
area: 25.0
aspect: 4.00
source_layers:
  - A-GLAZING MULLION
  - A-GLAZING-MULLION
source_entity_types:
  LINE: 4
  LWPOLYLINE: 1
variant_group:
  canonical: A GLAZING MULLION
  kind: complementary
```

And pair inspection:

```text
augrade> pair walls:3:5

candidate_id: walls:3:5
status: review
boundary_gap: 8.2
angle_diff_deg: 1.4
thickness_rel_diff: 0.09
gap_major_norm: 0.3
gap_minor_norm: 0.1
layer_jaccard: 0.0
memory_margin: 0.42
provenance:
  a layers: A-WALL 2
  b layers: S-CONCRETE WALL
```

## Geometry Preview

The REPL should be preview-first.

Useful commands:

- `show <polygon-id>`
- `pair <candidate-id>`
- `component <component-id>`

These should generate:

- temp SVG preview
- temp PNG preview if possible
- path to a DXF review artifact when requested

Since BlinkCAD is already part of the review workflow, `emit dxf` should remain a first-class command.

## Implementation Approach

### Phase 1: Thin Stateful CLI

Build:

- `repl.py`
- a `SessionState` dataclass
- a command dispatcher

Use:

- `cmd.Cmd` from the standard library, or
- `prompt_toolkit` only if line editing / completion becomes important

Keep the first version stdlib-first if possible.

### Phase 2: Read-Only Inspection

Support:

- open
- normalize
- extract
- show
- provenance
- pair
- components
- emit bundle

Do not add training yet.

### Phase 3: Mutable Rule Tuning

Support:

- `rules show`
- `rules set`
- `recompute merges`
- component consequences

This is where the REPL becomes a true workbench instead of just an inspector.

### Phase 4: Label Flow

Support:

- label commands
- import/export labels
- dataset export

This lets the REPL become a front end to the supervised-learning loop.

### Phase 5: Modeling

Support:

- heuristic scorer evaluation
- prototype memory evaluation
- edge-model training/evaluation hooks

The REPL should expose results, not hide them behind notebooks.

## What The REPL Should Not Try To Be

Avoid:

- a full CAD editor
- a notebook replacement
- a hidden wrapper over browser-only dashboards
- a generic shell for arbitrary Python

The REPL should stay tightly scoped to:

- normalization
- provenance
- extraction
- merge reasoning
- labeling
- artifact emission

## Why This Matters

The real value is not convenience.

It is that the REPL would unify the currently separate review modes:

- machine-readable normalization
- extraction metrics
- provenance residuals
- merge candidate reasoning
- expert label collection
- DXF review artifact generation

That would make the project feel like one system instead of a folder of related scripts.

## Recommended First Deliverable

A minimal first REPL should support this exact flow:

```text
open "Airport Doors_MEZZ.dxf"
normalize --auto-heal
extract --snap 0.5
polys count
show a_glaz_mull_multi_0017
pair walls:3:5
rules set walls.max_boundary_gap 32
recompute merges walls
label positive walls:3:5
labels export labels/session1.json
emit dxf out/review.dxf
emit bundle out_hitl
```

If that works cleanly, the REPL is already useful.
