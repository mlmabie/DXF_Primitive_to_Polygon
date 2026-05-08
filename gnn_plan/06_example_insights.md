# Example DWG Insights

This note consolidates what changed after opening the three received example
DWGs and inspecting one of them in Autodesk Viewer. It belongs in the main GNN
planning flow because the examples affect the training setup, not just intake
logistics.

## What We Actually Saw

Three local files are present:

- `3256-FIRST FLOOR PLAN-A.dwg`
- `3256-GROUND FLOOR PLAN-A.dwg`
- `3326-FLOOR PLAN-FF.dwg`

All three are AutoCAD 2018/2019/2020 DWGs. Embedded thumbnail previews confirm
that each contains colored drawing signal:

| File | Thumbnail-level signal |
|---|---|
| `3256-FIRST FLOOR PLAN-A.dwg` | sparse red marks on a compact residential floor plan |
| `3256-GROUND FLOOR PLAN-A.dwg` | red and yellow marks on a larger residential floor plan |
| `3326-FLOOR PLAN-FF.dwg` | dense red, green, cyan/blue, and yellow marks on a tall repeated layout |

Autodesk Viewer was then used for `3256-FIRST FLOOR PLAN-A.dwg`. That view was
much more informative than the embedded thumbnails:

- the drawing is a residential first-floor plan with thick wall linework,
  rooms, doors/windows, stairs, terraces, balcony, title block, dimensions,
  leaders, and schedule-style tags
- colored CAD entities are embedded in the drawing, including repeated red
  door/window-style tags such as `D1`
- selecting an object exposes stable CAD metadata; one selected object was:
  - type: `Line`
  - handle: `16b`
  - layer: `A-SHAFT`
  - linetype: `Continuous`
- the layer list is semantically structured, including `A-WALL`,
  `A-WALL HATCH`, `A-ROOM NAME`, `A-DIMENSION`, `A-LEADER`, `A-STAIR`,
  `A-DOOR AND WINDOW SCHEDULE TEXT`, `GR_A-WINDOW 1`, `GR_A-WINDOW 2`,
  `S-COLUMN`, and `S-COLUMN HATCH`

The important correction: these files are not just raster-marked images.
They are CAD drawings whose visible labels, colors, and annotation geometry
should be recoverable as vector entities if the DWG can be converted or
metadata-exported with handles, layers, colors, entity types, layouts, and
coordinates intact.

## The Annotation Ambiguity

"Annotation" means at least three different things in these examples:

1. **Architectural annotation**: room names, dimensions, leaders, sheet text,
   door/window tags, stair text, and title-block text.
2. **Drawing semantics**: labels like `D1`, `W1`, room names, or schedule tags
   that describe architectural objects and can supervise object recognition.
3. **Reviewer or workflow markup**: colored marks that may encode corrections,
   status, conflicts, or examples of desired output.

The training pipeline should not assume every colored object is a human ML
label. In the first Autodesk view, some red marks appear to be ordinary
door/window tags rather than external review markup. That is still useful
supervision, but it is a different target: it links a symbol/text entity to a
nearby door/window object instead of declaring a corrected model element.

## Impact On Representation

The examples strengthen the case for a heterogeneous graph:

- `primitive` nodes for CAD entities such as lines, polylines, arcs, circles,
  hatches, text, dimensions, inserts, and blocks
- `supervector` nodes for composed wall faces, door/window candidates, room
  labels, repeated fixture/symbol groups, and schedule tags
- `face` nodes for rooms, shafts, terraces, balconies, and other bounded regions
- `annotation` nodes for text, dimensions, leaders, colored marks, comments,
  and schedule-style labels
- typed edges such as `near`, `points_to`, `labels`, `inside`, `bounds`,
  `opens_into`, `same_symbol_family`, `same_schedule_tag`, and `conflicts_with`

This is a stronger target than a plain entity-classification graph. The model
needs to learn not only "what class is this primitive?" but also "what does this
annotation refer to?"

## What To Do With Layers

The examples have meaningful layers, but the research assumption remains
layer-blind classification.

Recommended split:

- keep `source_layer` as provenance, weak supervision, ablation input, and
  debugging metadata
- exclude raw layer names from the first layer-blind model input
- use layer names to build candidate labels and evaluation slices, such as
  text-like entities, wall-like entities, hatch carriers, door/window tags,
  dimensions, and sheet objects
- report model performance both with and without layer features

This avoids two failure modes:

- overfitting to one drafter's layer schema
- throwing away high-value supervision that the examples clearly contain

## Training Setup Changes

The first training product should be an annotation-to-object graph, not only a
primitive classifier.

### 1. Preserve DWG Metadata During Conversion

DWG-to-DXF conversion is now a research-critical preprocessing step. The
conversion chain must preserve:

- entity handle
- entity type
- layer
- color
- linetype
- block/insert membership
- model-space vs paper-space/layout membership
- text content and text insertion point
- dimension and leader geometry
- hatch boundaries

If a converter drops handles, text, colors, or layouts, it is not good enough
for this phase.

### 2. Build Separate Base And Annotation Graphs

For each drawing, construct:

- a base geometry graph for architectural entities
- an annotation graph for text, dimensions, leaders, colored tags, and markup
- correspondence edges between annotation nodes and nearby/pointed-to base
  objects

Examples:

- `D1` text node -> `labels` -> nearby door candidate
- room-name text -> `inside` -> room face
- dimension line -> `measures` -> wall span or opening
- leader arrow -> `points_to` -> projection/sill/lintel object
- colored correction mark -> `conflicts_with` or `requires_edit` -> target
  object, if that meaning is confirmed

This gives labels and relations without flattening everything into pixels.

### 3. Use Geometry-Only Baselines First

Before a GNN, train simple baselines on:

- primitive geometry
- local neighborhood statistics
- text content patterns
- color
- entity type
- relation features such as gap, containment, nearest object, arrow direction,
  overlap, and room-face membership

The GNN earns its place only where message passing improves relation recovery:
for example, resolving which object a tag labels when several candidates are
nearby, or detecting that repeated symbols belong to the same schedule family.

### 4. Split By Drawing, Not By Entity

Do not randomly split primitives from the same drawing across train and test.
That leaks drafter style, layer naming, geometry scale, and repeated symbols.

Use drawing-level or project-level splits:

- train on some examples
- validate on a held-out drawing
- keep one layout/style as a small stress test

The contrast between the compact 3256 plans and the tall repeated 3326 layout
is already useful as a distribution-shift check.

### 5. Treat Raster As QA And Optional Context

Raster views are useful for:

- human inspection
- annotation QA
- detecting missing conversion entities
- optional local image chips around graph nodes

Raster should not be the source of truth. The authoritative training object is
the vector graph plus metadata.

## Near-Term Experiment

The next concrete experiment after conversion:

1. Convert the three DWGs to DXF while preserving handles, layers, colors, text,
   blocks, and layouts.
2. Export a primitive table and layer/color/entity inventory for each file.
3. Render high-resolution overlays with color-preserving layers.
4. Identify candidate supervision layers:
   - wall and hatch layers
   - door/window tag layers
   - room-name layers
   - dimension/leader layers
   - any explicitly colored review-markup layers
5. Build an annotation-to-object correspondence dataset:
   - text/tag to nearest object
   - room name to containing face
   - dimension to measured span
   - leader to target object
6. Train:
   - geometry/entity baseline
   - relation-feature baseline
   - small graph model only after the baselines expose hard relation cases

Success is not "GNN classifies all CAD." Success is:

> the graph can recover useful supervision from CAD annotations and route
> ambiguous cases to a calibrated review loop.

## Open Questions For More Viewer Passes

The next manual viewer checks should answer:

- Are the colored marks in `3326-FLOOR PLAN-FF.dwg` true reviewer markup,
  schedule labels, or layer-coded architectural elements?
- Do the examples contain explicit annotation layers, or are color and text
  style the main carriers?
- Are labels in model space, paper space, or both?
- Do room names and door/window tags select cleanly as text entities with
  handles?
- Do leaders/dimensions expose enough geometry to infer their target objects?
- Does Autodesk Viewer expose object color in the property panel, or only layer
  and linetype?

Those answers determine whether the first dataset is mostly node labels,
annotation-to-object edges, or edit/conflict events.
