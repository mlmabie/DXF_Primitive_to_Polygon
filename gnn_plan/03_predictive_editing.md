# Predictive Modeling And Editing

This is the second-priority thread. It depends on the classification graph, but
it has different targets.

## Flavor 1: Infer Systems Inside An Architecture Shell

Question:

> Given an architectural shell, what hidden or partially shown system layout is
> plausible?

For plumbing, the graph needs more than walls:

- rooms and room types when known
- fixtures and fixture groups
- shafts, risers, chases, wet walls, cores
- slabs, structural obstacles, fire-rated walls, or no-route zones when known
- vertical alignment across floors if multi-level data appears later
- access and service constraints

Useful tasks:

- node prediction: likely fixture, shaft, wet wall, cleanout, riser
- link prediction: fixture connects to stack, route passes through chase
- path prediction: likely pipe run or service corridor
- graph completion: missing system elements implied by shell and fixtures
- uncertainty readout: plausible alternatives, not a single forced answer

Model shape:

- start with deterministic shell graph
- add fixture and system candidate nodes
- score route candidates with geometric cost and learned context
- use constraints to reject impossible paths
- use GNN/diffusion/sequence model only for uncertain completion

The model should not invent plumbing from architectural shell alone unless the
labels contain enough examples of plumbing intent. With only a few annotated
examples, the right output is a ranked set of hypotheses plus uncertainty.

## Flavor 2: Predict Edit Cascades, Conflicts, And Dependencies

Question:

> If I perform action X, what else changes or becomes invalid?

Represent an edit as an event on the graph:

- move wall
- delete element
- extend route
- add fixture
- resize opening
- merge/split wall segment
- change room boundary
- change shaft/core position

Predict outputs:

- impacted nodes
- impacted relations
- conflicts
- required follow-up edits
- invalidated assumptions
- confidence and explanation features

This should be a hybrid system:

- deterministic graph update for geometry that directly changes
- constraint/rule checks for hard violations
- learned model for likely secondary impacts and ambiguous dependencies

Hard constraints should stay explicit. Examples:

- route crosses blocked wall
- fixture loses connection
- room boundary opens
- clearance is violated
- duplicate candidate now conflicts with an existing element

Learned predictions should explain why the model thinks an impact cascades:

- adjacency path
- shared component
- inferred dependency
- route conflict
- repeated pattern break
- changed face topology

## Annotation Needs

For predictive editing, static labels are not enough. We need at least one of:

- before/after drawing pairs
- annotations that mark intended dependencies
- comments like "moving this wall forces these fixtures/routes to change"
- issue examples where an edit caused a conflict

Without before/after data, the first pass should be a rule-backed what-if graph
simulator plus a place to record predicted cascades for review.

