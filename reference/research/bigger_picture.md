# Bigger Picture

## What This Folder Is Actually About

This take-home is not just a geometry exercise. It sits inside a larger line of thought that was already developing before the assignment:

- the real problem is representation, not just architecture choice
- geometry should stay explicit at the bottom
- object identity should become stable in the middle
- typed relations should carry global coherence at the top
- hard validators should remain outside the learned system
- workflow traces should become the supervision moat

The older Augrade prep files in this folder are not random noise. They are early attempts to articulate that broader thesis in different formats:

- recruiter Q&A
- spoken versions
- compressed thesis
- deeper-dive research note
- supporting notes packet

This file consolidates that material into one throughline, then connects it directly to the current DXF work.

## The Pre-Take-Home Thesis

The most consistent idea across the prep material is:

> This is not really “put a GNN on BIM.” It is a representation-boundary problem.

That appears in different forms across:

- [`augrade_thesis_compressed.md`](/Users/malachi/augrade_takehome/augrade_thesis_compressed.md)
- [`augrade_deeper_dive_representations.md`](/Users/malachi/augrade_takehome/augrade_deeper_dive_representations.md)
- [`augrade_supporting_notes.tex`](/Users/malachi/augrade_takehome/augrade_supporting_notes.tex)
- [`augrade_spoken_versions.md`](/Users/malachi/augrade_takehome/augrade_spoken_versions.md)
- [`augrade_recruiter_questionnaire_charlie_final.md`](/Users/malachi/augrade_takehome/augrade_recruiter_questionnaire_charlie_final.md)

The core stack from those notes is:

1. geometric substrate
2. stable object tokens
3. typed relational graph
4. multiscale compression
5. deterministic validators around the loop

This was already the main worldview before touching the DXF.

## Why The Take-Home Matters In That Thesis

The take-home turned out to be a clean test of layers 1 and 2:

- geometric substrate
- token formation / object recovery

That is why the “tokenization” analogy landed so strongly.

In this file:

- primitives are the raw carriers
- closure is the grammar
- polygons are the tokens
- family inference is typed semantics on top of token formation

The take-home therefore became a microcosm of the bigger architecture rather than a disconnected coding puzzle.

## The Shared Representation View

Across the pre-take-home files, several ideas repeat with high consistency.

### 1. Geometry Should Not Be Compressed Away Too Early

The prep notes repeatedly argue that the graph layer should not be asked to recover geometry that was already destroyed.

Preserve:

- boundaries
- support interfaces
- openings
- alignment cues
- clearance envelopes
- provenance back to source geometry

This directly matches the current DXF work:

- if primitive carriers are collapsed too early, cleanup and merging become underdetermined
- if geometry remains explicit long enough, quotient structure becomes visible

### 2. The Right Middle Layer Is Persistent Object State

Another repeated theme is that one scene embedding is too lossy, while brittle symbolic BIM is too hand-authored.

The useful middle layer is:

- object-centric
- persistent
- editable
- tied to evidence

The take-home currently produces first-pass polygon candidates rather than full stable objects, but that is the right precursor.

### 3. GNNs Are Not The Whole Story

The older notes are quite consistent here:

- GNNs are useful for constraint propagation and relational synchronization
- they are not substitutes for perception
- they are not substitutes for deterministic validity
- they are not substitutes for the right decomposition

This is still the right stance after the DXF work.

### 4. Workflow Data Matters More Than Architecture Novelty

The prep material repeatedly points toward:

- edits
- rejections
- repairs
- validator failures
- substitutions
- revision history

as the real moat.

That connects directly to the merge lab:

- the merge lab is not just a convenience UI
- it is the start of a workflow trace and expert-label surface

## What The Take-Home Added

The take-home sharpened the pre-existing thesis in several important ways.

### 1. The Variability Is Authored, Not Sensor Noise

Before the take-home, the general representation story still lived at a fairly abstract level.

The DXF forced a more precise statement:

`observed_representation = R(style, decomposition, layering, snapping, carrier_choice)(latent_object)`

So the issue is not random corruption.

It is:

- decomposition choice
- carrier choice
- layer schema choice
- drafting convention
- local junction policy

That is much closer to an equivalence / quotient problem than a denoising problem.

### 2. Pair Relations Matter More Than Isolated Objects

The prep notes emphasized object-centric state, but the merge task showed something more specific:

for cleanup and merging, the useful learning object is often the candidate relation between two polygons, not either polygon by itself.

That leads to:

- pair features
- pair labels
- relation embeddings
- candidate graphs

This is one of the most important concrete refinements that came out of the take-home.

### 3. Provenance Must Survive

The older notes care a lot about evidence links and system legibility.

The DXF and layer analysis made this concrete:

- pooling layers for geometry can be correct
- collapsing provenance entirely is wrong

This is the right updated formula:

> pool for geometry, tag for provenance

The quotient should simplify semantic equivalence, but the residual should preserve drafting history and schema clues.

## Layer Normalization As The Bridge

[`layer_normalization_analysis.md`](/Users/malachi/augrade_takehome/layer_normalization_analysis.md) is probably the single strongest bridge between the older representation thesis and the current DXF work.

It shows that:

- name normalization is not enough
- spatial overlap matters
- entity-type profile matters
- provenance matters
- geometry pooling and provenance preservation must coexist

This is exactly the kind of move the pre-take-home material was gesturing toward in abstract terms:

- learn the right compressions
- do not erase the interfaces
- preserve residual structure that may matter later

## The Quotient View

The current best synthesis of the old and new material is:

> cleanup and merging should factor through a quotient by semantics-preserving drafting rewrites, while preserving provenance as a residual side channel

Examples of rewrites:

- one edge split into many collinear segments
- one circle represented as `CIRCLE`, arcs, or faceted polyline
- one object duplicated across outline, fill, and protection layers
- same family expressed with different layer schemas
- same structure encoded through different local face decompositions

The question is no longer merely:

- what geometry algorithm works?

It is:

- what equivalence structure is the file implicitly using?
- what invariants survive that structure?
- what residuals should stay attached for debugging and future learning?

## How The Folder Now Organizes Conceptually

### Core Task Surface

These are now the main take-home files:

- [`Airport Doors_MEZZ.dxf`](/Users/malachi/augrade_takehome/Airport%20Doors_MEZZ.dxf)
- [`Task Overview.docx`](/Users/malachi/augrade_takehome/Task%20Overview.docx)
- [`implementation_outline.md`](/Users/malachi/augrade_takehome/implementation_outline.md)
- [`research_doc.md`](/Users/malachi/augrade_takehome/research_doc.md)
- [`tokenize_dxf.py`](/Users/malachi/augrade_takehome/tokenize_dxf.py)
- [`build_dashboard.py`](/Users/malachi/augrade_takehome/build_dashboard.py)
- [`build_merge_lab.py`](/Users/malachi/augrade_takehome/build_merge_lab.py)
- [`build_labeled_merge_dataset.py`](/Users/malachi/augrade_takehome/build_labeled_merge_dataset.py)
- [`out/`](/Users/malachi/augrade_takehome/out)

### Current Research Layer

These are the take-home-adjacent reflection docs:

- [`PROCESS_JOURNAL.md`](/Users/malachi/augrade_takehome/PROCESS_JOURNAL.md)
- [`layer_normalization_analysis.md`](/Users/malachi/augrade_takehome/layer_normalization_analysis.md)
- [`layer_etymology.md`](/Users/malachi/augrade_takehome/layer_etymology.md)
- [`INDEPENDENT_LATENT_DIMENSIONS_MEMO.md`](/Users/malachi/augrade_takehome/INDEPENDENT_LATENT_DIMENSIONS_MEMO.md)
- [`LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md`](/Users/malachi/augrade_takehome/LATENT_DIMENSIONS_EXPERIMENT_CHECKLIST.md)

### Older Prep / Thesis Sources

These are still useful, but they are source material rather than core task artifacts:

- [`augrade_deeper_dive_representations.md`](/Users/malachi/augrade_takehome/augrade_deeper_dive_representations.md)
- [`augrade_recruiter_questionnaire_charlie_final.md`](/Users/malachi/augrade_takehome/augrade_recruiter_questionnaire_charlie_final.md)
- [`augrade_recruiter_questionnaire_charlie_final.tex`](/Users/malachi/augrade_takehome/augrade_recruiter_questionnaire_charlie_final.tex)
- [`augrade_recruiter_questionnaire_charlie_final.pdf`](/Users/malachi/augrade_takehome/augrade_recruiter_questionnaire_charlie_final.pdf)
- [`augrade_spoken_versions.md`](/Users/malachi/augrade_takehome/augrade_spoken_versions.md)
- [`augrade_supporting_notes.tex`](/Users/malachi/augrade_takehome/augrade_supporting_notes.tex)
- [`augrade_supporting_notes.pdf`](/Users/malachi/augrade_takehome/augrade_supporting_notes.pdf)
- [`augrade_thesis_compressed.md`](/Users/malachi/augrade_takehome/augrade_thesis_compressed.md)

These are not irrelevant in substance. They are just no longer the main execution surface.

## The Clean Throughline

If all of the prep material and the take-home work are reduced to one coherent statement, it is this:

1. The hard problem is choosing the right compression boundary.
2. Geometry must stay explicit long enough for stable object recovery.
3. Object identity must persist across edits and rewrites.
4. Relations, not isolated embeddings, carry much of the real semantic burden.
5. Provenance should survive as residual structure.
6. Learned systems should sit on top of explicit invariants and hard validators, not replace them.
7. Workflow traces are the real path to robust adaptation.

The DXF assignment did not replace the older thesis. It made it more concrete and more testable.

## What I Would Remove Or Archive Later

Now that this consolidation exists, the files that look most like archive candidates are not the substantive notes, but the duplicated presentation forms:

- duplicate PDF / TEX renderings of the same prep material
- duplicate verification output in [`out_verify/`](/Users/malachi/augrade_takehome/out_verify)
- local junk like `.DS_Store` and `__pycache__/`

I would not delete the older `.md` source notes yet. They are still useful as source material for the broader research framing.

## Current Best Summary

The older prep material was already circling the right center of gravity:

- explicit geometry
- stable object tokens
- typed relations
- residual provenance
- deterministic validators
- workflow supervision

The take-home sharpened that into a specific research program:

- quotient authored drafting rewrites
- keep provenance residuals
- learn on candidate relations
- validate independence of the latent dimensions empirically

That is the bigger picture this folder now contains.
