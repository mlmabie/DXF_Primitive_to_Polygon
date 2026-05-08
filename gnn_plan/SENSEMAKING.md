# Sensemaking

This is the compact version of the support notes. It preserves the useful
judgment without making the repo a diary.

## Current Direction

The immediate goal is narrow:

> build small GNN products for classifying DWG/DXF primitives and supervectors,
> then use embeddings, uncertainty, and expert feedback to discover rules/forms
> that improve coverage and consistency of the deterministic modeling engine.

This is pro-GNN, but not "GNNs solve CAD." The GNN is useful where graph
context and learned embeddings reveal structure the deterministic engine cannot
easily hand-code yet.

## What To Keep In Mind

- The input distribution is not natural or balanced. CAD artifacts are authored,
  procedural, stylistic, and full of rare edge cases.
- The first win is not black-box scale. It is recall, calibration, and good
  retrieval of interesting failures for expert annotation.
- Expert feedback should update labels, rules, memories, and model behavior.
  Otherwise annotation becomes theater.
- SAEs, Hopfield/prototype memory, and embedding probes matter when they help
  decode structured intent: carrier style, hatch/outline equivalence, wall
  continuity, decomposition patterns, closure failures, snap regimes, etc.
- Parameter decomposition is the prize: split failures into meaningful knobs
  that the engine can act on.

## Working Loop

```text
deterministic engine output
-> primitive/supervector graph
-> sparse + GNN classifiers
-> calibrated uncertainty and embeddings
-> retrieve similar weird cases
-> expert annotation / review
-> update model + deterministic rules
-> verify coverage and consistency improvement
```

The GNN/embedding layer is a microscope for the modeling engine, not the whole
engine.

## What The GNN Should Own First

- primitive and supervector classification
- annotation-to-object correspondence, such as door/window tags to nearby
  openings, room names to containing faces, dimensions to measured spans, and
  leaders to target objects
- relation scoring where local geometry is ambiguous
- low-confidence / high-value annotation surfacing
- embedding neighborhoods for recurring failure families
- rule/form hypothesis generation, such as merge, split, extend, hatch-outline
  equivalence, repeated symbol decomposition, closure regime, or carrier-style
  family

## What It Should Not Own Yet

- exact geometry validity
- closure and winding truth
- code/compliance truth
- end-to-end BIM generation
- broad RL/search
- replacing deterministic validators

## The Active-Learning Center

The most important product dynamic is:

> can the system remember the right strange cases, stay calibrated about what it
> does not know, and surface genuinely predictive examples to experts?

For this data environment, that matters more than raw model scale. Authored
drawings are not iid examples from a clean distribution. They contain drafter
habits, carrier conventions, old standards, hidden phases, and exception cases.

Good active-learning candidates:

- high-confidence disagreement between sparse baseline and GNN
- low-confidence regions with high coverage impact
- embedding clusters with repeated validator failures
- near-duplicate cases where one succeeds and one fails
- prototype memories that collect the same failure under different carrier
  styles

## Parameter Decomposition

Useful decomposition blocks:

- geometry: length, thickness, curvature, orientation, closure, aspect, area
- topology: endpoints, intersections, containment, shared boundary, face
  adjacency
- style: carrier choice, hatch-vs-outline, snap behavior, decomposition
  granularity
- family: wall, door, column, fixture, plumbing, symbol, annotation
- rule: merge, split, extend, trace hatch boundary, infer missing face,
  detect grid regularity
- confidence: auto-accept, reject, inspect, route to expert

The best output is not just "class = wall." A better output is:

> this is probably wall mass expressed through hatch boundaries with a carrier
> convention the deterministic engine underuses; promote a hatch/outline
> equivalence rule here rather than changing global snap tolerance.

## Near-Term Products

Small products that could each become useful tooling or future verifiers:

- primitive/supervector classifier
- coverage-failure classifier
- merge/split/extend suggestion model
- hatch-vs-outline equivalence detector
- rule-candidate miner
- embedding inspector / interpretable factor decoder
- annotation queue ranked by information value

If these work, they become data engines and verifiers for larger future models:
transformer, JEPA, world model, or graph-edit policy. But narrow quality comes
first.

## Conversation Guardrails

Say:

- "representation boundary"
- "vector geometry stays source of truth"
- "GNN as context propagation and failure microscope"
- "calibrated annotation loop"
- "deterministic engine plus learned residual tools"

Avoid:

- "GNN on BIM"
- "black-box CAD generator"
- "we learn validity"
- "layers are reliable"
- "RL/search is the starting point"

## Repo Shape

Read in this order:

1. `prompt.md` — current objective
2. `TALK_TRACK.md` — what to say
3. `SYSTEM_SPEC.md` — what to build
4. `SENSEMAKING.md` — why this shape matters
5. `06_example_insights.md` — what the first received examples changed
6. `04_research_map.md` — evidence shelf

The older generated notes were consolidated here. The deeper DXF thesis and
paper trail under `reference/` should remain for now.
