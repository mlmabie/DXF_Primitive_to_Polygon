# DXF Tokenization — How We Get To Primitives

This is the M1 layer in the stack. It turns raw DXF bytes into the typed primitive table that supervector formation (M2) consumes. The existing `tokenize_dxf.py` in the repo root is the first-pass implementation of what this document describes.

## What DXF actually is

A DXF file is an ASCII text stream of `(group_code, value)` pairs on consecutive lines:

```
0
SECTION
2
ENTITIES
0
LINE
8
A-EXTERNAL WALL
10
145.250
20
22.875
11
145.250
21
86.125
0
LWPOLYLINE
...
```

- Group code `0` introduces a new entity or section
- Group code `8` is the layer name
- Group codes `10`/`20`/`30` are the first point's x/y/z
- Each entity type has its own per-code map (line/arc/polyline/circle/hatch/text/dimension/insert/spline)
- Sections are delimited by `(0, SECTION)` and `(0, ENDSEC)`
- For floor-plan work we need the **TABLES**, **BLOCKS**, and **ENTITIES** sections; HEADER and CLASSES and OBJECTS are optional

There is a binary variant, but most CAD exports for review are ASCII DXF, which is what we parse. DWG is the proprietary AutoCAD binary; DWG → DXF is a preprocessing step (Teigha File Converter, ODA, or commercial tooling).

## The parse loop

The spine is a state machine that consumes `(code, value)` pairs and emits entities at `(0, …)` boundaries:

```python
def iter_pairs(path):
    with open(path, 'r', encoding='cp1252', errors='replace') as f:
        while True:
            code_line = f.readline()
            if not code_line:
                return
            value_line = f.readline()
            yield int(code_line.strip()), value_line.rstrip()

def parse_entities(pairs):
    current = None
    for code, value in pairs:
        if code == 0:
            if current is not None:
                yield current
            current = {'type': value, 'codes': {}}
        else:
            current['codes'].setdefault(code, []).append(value)
    if current is not None:
        yield current
```

That is the spine. Real implementations also handle section transitions, BLOCKS definitions, and per-entity-type structural codes (HATCH boundary paths nest, splines have control-point lists, etc.). The existing `tokenize_dxf.py` is large mostly because of those per-entity expansions.

## Entity-typed extraction

After the raw stream, each entity becomes a typed object with exact geometry:

| Entity | Extracted fields |
|---|---|
| `LINE` | `(x1, y1, z1)`, `(x2, y2, z2)`, layer, handle |
| `LWPOLYLINE` | vertex list `[(x, y), …]`, per-vertex bulges, `closed` flag, layer |
| `POLYLINE` (older form) | as LWPOLYLINE but composed of VERTEX sub-entities until `SEQEND` |
| `ARC` | center, radius, start_angle, end_angle (in OCS, see below) |
| `CIRCLE` | center, radius |
| `HATCH` | one or more boundary paths (each a closed sequence of line/arc segments), pattern name, solid flag |
| `TEXT` / `MTEXT` | position, contents, height, rotation, anchor |
| `DIMENSION` | definition points, text, dim style |
| `LEADER` | vertex list, annotation reference |
| `INSERT` | block name, insertion point, scale (x, y, z), rotation, layer |
| `SPLINE` | control points, knots, weights, degree |

Each entity carries a stable **handle** (group code `5`, hex string) that uniquely identifies it within the file. That handle becomes the primitive's stable id across re-tokenizations.

## Five gotchas the existing solver already handles

1. **OCS vs WCS.** `CIRCLE`, `ARC`, `LWPOLYLINE`, and `HATCH` define geometry in their own Object Coordinate System with an extrusion vector (codes `210`/`220`/`230`). For nearly all floor plans the extrusion is `(0, 0, 1)` and OCS = WCS — but you must check. Otherwise you get mirrored or rotated geometry on a small fraction of entities.
2. **HATCH boundary parsing is recursive.** A HATCH has an outer boundary plus optional holes; each boundary is a sequence of edges; each edge can be a line, arc, ellipse arc, or spline. Group code `92` gives the boundary count, `93` the edge count per boundary, `72` the edge type per edge. Most naive parsers break here. The companion-layer pairing for HATCH-IoU supervision lives downstream of this.
3. **INSERT resolution.** Blocks are defined in the `BLOCKS` section. When the entity stream contains an `INSERT (name=BLK_DOOR, pos=…, scale=…, rot=…)`, two options:
   - Keep it as a named supervector (good for symbol identity)
   - Explode into constituent primitives at the transform (good for raw coverage)
   - The pipeline does **both**: emit the INSERT as a supervector AND emit the exploded primitives with an `exploded_from_insert` flag plus a `parent_of` edge back to the INSERT.
4. **Encoding.** DXF files are often Windows-1252, sometimes UTF-8, occasionally mixed. Open with `cp1252` and a fallback on `TEXT` / `MTEXT` / layer-name decoding.
5. **Polyline bulges.** `LWPOLYLINE` vertices can carry a `bulge` value (group code `42`) that turns a straight segment into an arc. The bulge is `tan(theta/4)` where `theta` is the included angle. Bulge-bearing segments must be expanded into arc parameters before snapping.

## Token-stream output schema

After parsing, the output is a typed primitive table plus a sibling exact-geometry pack:

```text
primitives.parquet:
  primitive_id | entity_type | layer | handle | geom_id | feature_vec (D_p ≈ 24)
  1            | LINE        | A-WALL          | 7F | g1 | [...]
  2            | LWPOLYLINE  | A-GLAZING       | 80 | g2 | [...]
  3            | HATCH       | A-WALL HATCH    | 81 | g3 | [...]

geom_pack:
  geom_id | exact_coords (float64) | bulges | vertices | bbox | handle
  g1      | [[145.25, 22.875], [145.25, 86.125]]   | []         | ...     | ...  | 7F
  g2      | [[...], ...]                           | [...]      | ...     | ...  | 80
  g3      | boundary_paths: [[...]]                | ...        | ...     | ...  | 81

layers.parquet:
  layer_name | color | linetype | frozen | (provenance only)

blocks.parquet:
  block_name | n_member_primitives | transforms_used

drawing_meta.parquet:
  drawing_id | units (in/mm) | bbox | INSUNITS_code | dxf_version
```

This is the M1 output. Everything downstream — M2 supervector formation, M3 graph construction, the snap graph, the HATCH-IoU computation — operates on this typed primitive table plus the geom pack.

## What changes vs the existing solver

The current `tokenize_dxf.py` produces a usable token stream and filters to `wall` / `column` / `curtain_wall` carriers for the scoped polygon-reconstruction task. The GNN pipeline needs three extensions:

1. **Persist every primitive, not just the scoped families.** TEXT, DIMENSION, LEADER, INSERT, SPLINE, every layer. Annotation-to-object correspondence and symbol-family detection need the full set.
2. **Emit the geom pack as a sibling artifact.** Today coordinates are inlined in the JSON output for the scoped families. For the GNN pipeline, exact geometry goes into a separate columnar store addressed by `geom_id` so the feature tensor stays decoupled from float64 coordinates.
3. **Compute the layer-name embedding offline, mask at train time.** Build a low-dim embedding over all layer names seen across the corpus (e.g., 16d learned from clustering on layer-name n-grams). Carry as a feature with a `is_layer_blind` mask flag set at training time. This lets the same parser support layer-blind training and layer-aware ablation.

## Stdlib vs `ezdxf`

The current solver is stdlib-only and that is deliberate — reviewers can run it without an install step. For the GNN pipeline:

- **Stdlib is sufficient for `LINE`, `LWPOLYLINE`, `ARC`, `CIRCLE`, `INSERT`, `TEXT`, and the basic HATCH boundary cases** common in floor plans.
- **`ezdxf` is worth the dependency** when handling arbitrary HATCH patterns, complex SPLINEs, OLE entities, complex blocks, dimension styles, paperspace vs modelspace, and unusual encodings. The repo already optionally uses `ezdxf` for two library modules.

The right rule is: stdlib for the runnable reviewer entry point, `ezdxf` for the production pipeline that has to handle messy real-world files. Both produce the same downstream token-stream schema.

## Talk-track line

> DXF tokenization is mostly already done — it's the M1 layer, deterministic, stdlib-feasible. The pipeline preserves exact geometry in a sibling pack so the learned layers can warp the relational space without touching the validators' source of truth. Going from this token stream to the supervector graph is the next deterministic step; going from the supervector graph to learned scores is where the GNN starts.
