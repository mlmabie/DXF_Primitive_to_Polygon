# Voice And Vision Ledger

This ledger exists because the research plan is supposed to serve the vision,
not sand it down.

## Core Voice

These are the claims that should remain legible even after technical cleanup:

- This is not "put a GNN on BIM." It is a representation-boundary problem.
- Freeze the world interface, not the current model trick.
- Build for future model gains.
- Workflow exhaust may matter more than static final labels.
- Real work is residual repair: move, reroute, split, merge, preserve
  everything else.
- Complexity must compress into reliability.
- Separate what changes from what must be stable.
- Experience drives design.

## What These Mean Technically

| Voice claim | Technical commitment |
|---|---|
| representation-boundary problem | define stable interfaces between raw geometry, object state, typed relations, validators, and edit actions |
| freeze the world interface | make object ids, edit grammar, validator outputs, evidence links, and traces durable while encoders/backbones stay swappable |
| workflow exhaust | capture edits, rejections, repairs, validator failures, comments, substitutions, disagreement, and time-to-fix |
| residual repair | prefer typed edit deltas and validator residual reduction over whole-scene regeneration |
| complexity into reliability | keep deterministic geometry and validation outside the learned model where exactness matters |

## Phrases To Keep Alive

Use these sparingly, but do not erase them:

- "object-centric state"
- "typed relational synchronization"
- "validator boundary"
- "residual edit tokens"
- "graph-program hybrid"
- "world interface"
- "workflow-aware model stack"
- "compute-realistic"
- "use the lightest model stack that survives contact with the product loop"

## Smoothing Warnings

When editing, watch for these bad conversions:

- "vision" becoming "best practices"
- "workflow exhaust" becoming merely "more data"
- "residual edit tokens" becoming merely "actions"
- "validator boundary" becoming merely "post-processing"
- "future-proofing" becoming merely "modularity"
- "physical-design intuition" becoming merely "domain interest"

The sharpened version should sound technical, but still like it came from a
person with a specific worldview.
