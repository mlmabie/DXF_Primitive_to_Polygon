# Scope Resolver

## Core question

> Given this objective, edit, residual, annotation, or user selection, what is the minimal sufficient subgraph?

This is the practical reason graphs matter. The graph is not only a prediction object. It is a **compute-scope engine** for giant project files, multiplayer drawing state, validator routing, cache invalidation, and agent context control.

## Definition

Let:

```text
q = objective | edit proposal | validator residual | annotation | user selection
G = full project graph
S = scoped subgraph
F = downstream function: validator, scorer, edit ranker, annotation aligner, or agent tool call
```

A scoped subgraph is **sufficient** if:

```text
F(S, q) ~= F(G, q)
```

within risk tolerance.

It is **minimal enough** if it preserves the result while reducing compute, context, validator calls, cache invalidation, and review burden.

Do not optimize exact minimality first. Optimize:

```text
safety -> decision fidelity -> sparsity -> speed
```

## Scope certificate

Every model/tool/agent call should carry a scope certificate:

```json
{
  "scope_id": "door_clearance:D1:room_204",
  "query_type": "validator_residual",
  "nodes": ["door_17", "opening_17", "wall_44", "room_204", "tag_D1", "route_8"],
  "edges": ["opens_into", "labels", "bounds", "near", "clearance_depends_on"],
  "validators": ["door_clearance", "route_connectivity", "schedule_consistency"],
  "cache_invalidation": {
    "embedding_radius": 2,
    "geometry_radius": 1,
    "validator_radius": "dependency_closure"
  },
  "excluded_reason": "unrelated floors and unconnected schedule families outside validator dependency closure",
  "missing_state": ["door_swing_confidence_medium"],
  "review_mode": "before_after_overlay"
}
```

The certificate answers:

- why this context is enough
- what was excluded
- what validators will check the result
- what cache entries become dirty
- what missing evidence would force expansion
- what risk band applies

## Deterministic baseline first

Before training, write a deterministic scope baseline. Given `q`, include:

- selected object or residual target
- type-specific dependency edges
- containing face / room / zone
- linked annotations, dimensions, leaders, schedules
- validator dependency closure
- spatial near-neighborhood
- same-symbol or same-schedule edges
- relevant prototype-memory cases

Example: door edit scope = door, opening, host wall, adjacent room faces, swing arc, schedule tag, clearance zone, route/circulation edges, validators depending on door/opening.

This baseline becomes the teacher and the floor.

## Training signals

### 1. Validator traces

Every validator can emit the objects it touched. Those objects become positive scope labels.

Example:

```text
door_clearance_validator(door_17)
  touches door_17, opening_17, wall_44, room_204, swing_arc_17, route_8, clearance_zone_204
```

### 2. Edit diffs

Accepted/rejected edits create before/after affected sets:

```text
edit = move door
changed nodes = door, opening, wall segment
invalidated nodes = tag, schedule row, room boundary
validators rerun = clearance, containment, schedule consistency
```

Affected + invalidated + validator-touched nodes are positives. Nearby but unused objects are hard negatives.

### 3. Full-run vs scoped-run distillation

Run the expensive full-graph pipeline offline. Train the resolver to find a smaller `S` that reproduces the same result:

```text
y_full = F(G, q)
y_scope = F(S, q)
loss = D(y_full, y_scope) + sparsity/risk penalties
```

### 4. Synthetic edit/residual tasks

Generate controlled corruptions with known causal scope:

- move opening
- break containment
- duplicate footprint
- mislabel tag
- shift room boundary
- create clearance conflict
- remove hatch-outline evidence

### 5. Human expansion behavior

If the review UI shows a scope and the operator expands it, clicks another object, or says “this also matters,” that is a label.

## Model architecture

```text
1. Candidate generator
   deterministic superset: k-hop + spatial radius + validator deps + retrieval memory

2. Query encoder
   encodes objective/edit/residual/annotation/user selection

3. Node/edge scorer
   relevance score conditioned on query

4. Subgraph selector
   top-k or learned sparse mask

5. Closure engine
   adds required dependencies deterministically

6. Sufficiency estimator
   predicts whether scope is enough

7. Validator check
   scoped result compared to full or expanded result during training
```

## Loss

```text
min_theta E_q [
    D(F(G, q), F(S_theta(G, q), q))
  + lambda * cost(S_theta)
  + mu * risk_missing(S_theta)
  + nu * closure_violation(S_theta)
]
```

Where:

- `D` = full-vs-scoped decision/residual/proposal difference
- `cost` = nodes, edges, tokens, validator calls, latency, cache dirtied
- `risk_missing` = asymmetric penalty for excluding critical nodes
- `closure_violation` = missing required dependency edges

## Metrics

| Metric | Definition |
|---|---|
| Scope recall | Percent of truly required nodes included. |
| Scope precision | Percent of included nodes actually needed. |
| Decision fidelity | Scoped result matches full result. |
| Validator fidelity | Scoped residual matches full residual. |
| Latency reduction | Full-graph runtime divided by scoped runtime. |
| False exclusion rate | Critical omitted dependency rate. |
| Expansion rate | How often uncertainty forces a larger scope. |
| Human expansion rate | How often users add missing context. |
| Cache invalidation size | Affected graph/cache footprint per edit. |
| Review usefulness | Operator accepts/rejects without asking for more context. |

Hero metric:

> sufficient-context rate at fixed false-exclusion risk.

## Storage/inference split

Do not make one graph database do everything.

```text
CAD/vector engine       exact geometry and local operations
Column/event store      facts, features, validator runs, timings
Vector index            similar cases, motifs, convention memory
Graph adjacency layer   dependency closure, L-hop neighborhoods, dirty sets
Agent runtime           scope resolver + tool calls + validator loop
```

ClickHouse-style storage can own high-volume facts and event traces. Turbopuffer-style vector retrieval can own embeddings/prototypes/motifs. The graph adjacency layer owns dependency closure and scope.

## Deck line

> Graphs are not only for prediction. They are for compute scope. In large project files, speed comes from knowing what not to touch.

## Live CTO phrasing

> The reason I keep coming back to graphs is not that message passing is magic. It is that a graph gives compute scope. In a giant AutoCAD project, an agent cannot afford to repeatedly re-read and rethread the whole file. The system needs to know which objects, annotations, validators, schedules, memories, and cache entries are implicated by a proposed edit. If we build that scoped substrate, some changes become 100x faster and whole classes of multiplayer sync problems disappear. The GNN is optional on top; the scope graph is not.
