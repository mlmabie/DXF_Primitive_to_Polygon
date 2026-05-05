# Augrade Strategy From Model Prep

Date: 2026-05-05

This note distills the older `augrade-model-prep` workspace into model-planning
decisions for this branch. It is less a literature map and more a system-design
rubric.

## Current Company Framing

Use the newer public framing as the default:

> AI-powered preconstruction and project-delivery automation that turns
> drawings and requirements into editable BIM/CAD outputs, take-offs,
> schedules, construction documents, and downstream artifacts.

Treat older AR/VR and wearable-tech material as legacy context only.

## Center Of Gravity

The core technical problem is not "should we use GNNs?" It is:

> What representation and action interface makes graph reasoning, constraint
> propagation, and sequential optimization actually work?

The model stack should be described as:

1. geometry-native evidence
2. stable object formation
3. typed relational graph over components, spaces, systems, and hierarchy
4. multiscale compression and retrieval
5. deterministic validators outside the model
6. planner, search, or RL over structured edit actions

The GNN belongs in the middle: synchronization, relation propagation, contextual
merge decisions, dependency inference, and edit-impact prediction. It should
not replace perception, exact geometry checks, or code/compliance logic.

## First-Class Primitives

The system should not rely on one giant scene embedding. It should expose
primitives the product can preserve, update, retrieve, validate, and compose.

### Object Token

- persistent id
- canonical geometry parameters
- local frame
- type/material/function when known
- uncertainty
- evidence pointers to raw primitives, scans, drawings, or annotations

### Relation Token

- support
- adjacency
- containment
- alignment
- clearance
- connectivity
- circulation
- routing
- code-relevant separation

### Hierarchy Token

- primitive -> supervector -> component
- component -> assembly
- room -> zone -> floor -> building

### Constraint Token

- hard-validity flag
- residual to threshold
- validator provenance
- violated relation or object ids

### Residual Edit Token

- move
- resize
- attach
- split
- merge
- reroute
- delete
- repair
- reassign

Real workflows are mostly constrained repair and revision, not whole-scene
regeneration. Residual edit tokens are therefore first-class, not an
afterthought.

## Graph-Program Hybrid

Graphs are strong for typed message passing and nonlocal relational
propagation. Program-like structure is strong for hierarchy, repetition,
compact editability, and reusable motifs.

The medium-term target should therefore be a graph-program hybrid:

- graph state for components, spaces, systems, and relations
- program-like structure for repeated motifs, assemblies, hierarchy, and edit
  grammar
- validators as explicit external checks
- learned proposal/ranking loop over typed actions

This is especially relevant for architectural domains because buildings are not
only adjacency fields. They have repeated layouts, assemblies, routing motifs,
code templates, and project-specific constraints.

## Future-Proofing Rubric

Freeze the world interface, not the current model trick.

Keep stable:

- object identity and edit history
- typed scene graph / scene program
- deterministic validators
- action grammar for graph edits
- evidence links back to raw geometry
- workflow traces
- eval suites for symmetry shift, composition shift, and constraint satisfaction

Keep replaceable:

- perceptual encoder
- geometric compression scheme
- graph backbone
- planner / RL / search layer
- canonicalization hacks
- curriculum and training tricks

If invariance improves, the product should need fewer normalization hacks. If
compositional generalization improves, the product should reuse the same
objects, relations, hierarchy tokens, and edit primitives in more novel
combinations.

## Workflow Exhaust

The moat is likely not only static labels or final BIM outputs. It is workflow
exhaust:

- edits
- rejections
- repairs
- code-check failures
- substitutions
- comments and rationales
- revision history
- designer disagreement
- time-to-fix

This data teaches what the ontology should preserve, which ambiguities are
operationally expensive, and what a meaningful residual repair looks like.

## Evaluation Targets

Static class accuracy is necessary but not sufficient. The setup should also
support:

- symmetry shift tests: viewpoint, rotation, scale, modality, partial
  observation, drafting style
- composition shift tests: larger assemblies, new room/floor compositions,
  deeper hierarchy, unusual valid constraint combinations
- residual repair tests: start from broken scenes and measure minimal valid
  edits, structure preservation, and validator-residual reduction
- workflow realism tests: predict or rank the next competent correction from
  real revision traces

## RL And Search Placement

RL is not the starting point. First define:

- stable object state
- typed relations
- graph edit grammar
- deterministic state transition
- hard validator feedback
- useful soft objectives

Then RL/search can operate over structured actions:

- state: component graph plus requirements and validator outputs
- action: place, move, resize, split, merge, connect, reroute, remove
- transition: deterministic graph update plus validation
- reward: hard invalidity penalties plus soft design objectives

This is a sequential control problem over changing graph state, not a direct
transplant of text-prompt RL.

## Compute-Aware Bias

The old prep notes repeatedly emphasized lightweight, efficient, scalable
systems matched to actual compute and data realities. Preserve that bias:

- start with sparse and inspectable baselines
- profile graph construction and feature generation, not only the forward pass
- prefer hybrid systems where model complexity earns its keep
- ask whether static or dynamic graph construction is the actual bottleneck
- choose PyG/custom paths based on scale and stability, not framework fashion

## Strongest Short Form

> Build a vector/object-centric world interface first: stable object tokens,
> typed relations, residual edit actions, external validators, and evidence
> links. Use GNNs where relational context has to propagate, use search/RL only
> after the edit grammar is clean, and use workflow traces to teach the system
> what real repair looks like.
