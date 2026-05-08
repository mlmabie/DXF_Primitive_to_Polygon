# Received DWG Examples

Three annotated DWG examples for grounding the GNN plan:

| File | Signal |
|---|---|
| `3256-FIRST FLOOR PLAN-A.dwg` | compact residential plan; Autodesk view showed red door/window-style tags such as `D1` plus structured layers |
| `3256-GROUND FLOOR PLAN-A.dwg` | larger residential plan; thumbnail shows red/yellow annotation signal |
| `3326-FLOOR PLAN-FF.dwg` | tall repeated layout; thumbnail shows dense red/green/cyan/yellow signal |

## Key Observation

These are not just raster-marked drawings. In Autodesk Viewer, drawing objects expose CAD metadata such as handle, layer, type, and linetype. One selected object was a `Line` with handle `16b` on layer `A-SHAFT`.

Visible layers included semantic carriers such as `A-WALL`, `A-WALL HATCH`, `A-ROOM NAME`, `A-DIMENSION`, `A-LEADER`, `A-DOOR AND WINDOW SCHEDULE TEXT`, `GR_A-WINDOW 1/2`, `S-COLUMN`, and `S-COLUMN HATCH`.

## GNN Takeaway

The useful target is an annotation-to-object graph, not only primitive classification.

Model:

- base CAD primitives and supervectors
- annotation nodes for text, dimensions, leaders, tags, and colored marks
- relation edges such as `labels`, `points_to`, `inside`, `measures`, `near`, and `conflicts_with`

Training stance:

- keep vector geometry and CAD metadata as source of truth
- use layers, colors, and text as provenance and weak supervision
- hide raw layer names in the first layer-blind inference test
- use raster only for QA or optional context chips

## Next Useful Extraction

For each DWG, preserve:

- handle
- entity type
- layer
- color
- text content and insertion point
- block/insert membership
- dimensions/leaders
- model-space vs layout membership
- geometry coordinates

That is enough to turn the examples into supervised graph data.
