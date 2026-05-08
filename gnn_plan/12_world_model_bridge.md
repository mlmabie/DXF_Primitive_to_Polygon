# World-Model Bridge: Raw Geometry To Multiscale Graph

## Motivation

A possible junction between 3D reconstruction and GNN/BIM is not a direct jump from raw pixels/points to BIM objects. It is a bridge:

```text
raw multimodal evidence
-> geometric encoding on non-Euclidean manifolds
-> object/patch/region latent state
-> multiscale graph substrate
-> validators + typed edit proposals
```

The raw encoder may come from a VLA, JEPA, diffusion/autoencoder, point/mesh transformer, Gaussian/NeRF-style representation, or another world-model substrate. The graph does not need to own the raw modality. It needs to own stable state, scope, dependencies, validators, and memory.

## Why non-Euclidean geometry matters

Buildings are not just Euclidean point clouds. Useful state often lives on:

- surfaces
- rooms/faces/regions
- routes and circulation graphs
- containment hierarchies
- structural/MEP dependency graphs
- visibility/occlusion manifolds
- drawing-sheet and annotation manifolds
- time/version/edit trajectories

A raw encoder can learn local geometric or semantic indexing over these manifolds, but the product still needs persistent graph state for multiplayer edits, validator routing, and scope.

## Bridge architecture

```text
Raw evidence
  photos, scans, point clouds, DWG/DXF, specs, issue comments

Latent geometric encoder
  image/point/mesh/world-model representation
  non-Euclidean patches, surfaces, regions, route spaces

Index layer
  semantic and geometric retrieval
  links raw evidence to graph regions

Multiscale graph
  primitives -> supervectors -> faces -> components -> assemblies -> project

Validator/readout layer
  hard checks, residuals, typed edits, scope certificates
```

## Minimal product use: semantic/geometric indexing

Even before reconstruction is solved, this bridge is useful as an index.

Examples:

- retrieve site photos relevant to a room/duct/wall cluster
- link scan evidence to a validator residual
- find similar wall/opening assemblies across projects
- index repeated motifs or customer conventions
- map real-world evidence to a scoped graph region
- decide whether multimodal evidence is worth promoting to typed state

## Typed vs latent split

Do not type everything. That creates a cascade of volume for trivial details.

Type what unlocks:

- scope
- validation
- edit action
- cache invalidation
- customer trust
- reviewer affordance

Keep latent what only guides:

- retrieval
- ranking
- uncertainty
- similarity
- motif discovery
- global context

## Evidence promotion rule

Real-world evidence becomes typed only when it affects an edit, validator, or review decision.

```text
site photo suggests installed duct conflicts with modeled clearance
-> evidence node links to duct/ceiling zone
-> embedded scorer flags likely contradiction
-> validator asks for typed duct geometry only if edit depends on it
```

This avoids turning every image/scan into a brittle typed ontology.

## Training tasks

Useful pretraining or fine-tuning objectives:

- contrast raw evidence with graph regions
- predict which graph nodes a scan/photo/spec paragraph supports or contradicts
- reconstruct scoped local geometry from latent evidence
- align room/route/surface manifolds with graph faces/components
- predict validator residuals from latent evidence + graph state
- retrieve similar cases across drawings and real-world observations

## Relation to the scope resolver

The scope resolver can request multimodal context only when needed:

```text
query: clearance residual in ceiling zone
scope resolver: graph region + validator dependencies + relevant scan/photo evidence
model: proposes edit or asks for evidence promotion
validator: checks typed state after promotion
```

This is how world-model context enters the product loop without making every agent step wait on the whole project file.

## Research direction

Potential paper thread:

> Multiscale Geometry Indexing for Verifier-Backed CAD/BIM Graphs

Claim:

> raw multimodal world models become useful in design automation when their latent geometry is connected to a persistent multiscale graph that owns scope, validation, and edit semantics.

Minimum proof:

- map raw evidence to graph regions
- retrieve context for validator residuals
- improve annotation/review speed
- avoid full-scene typing except when validators require it

## Deck line

> The graph does not replace world models. It gives them a product interface: scope, memory, validators, and edit semantics.
