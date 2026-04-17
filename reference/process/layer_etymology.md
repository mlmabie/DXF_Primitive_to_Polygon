# Layer Name Etymology and AIA/NCS Grammar

## The Standard

Architectural DXF files follow (or approximate) the **AIA CAD Layer Standard** (US National CAD Standard / NCS). The grammar is:

```
LAYER_NAME := DISCIPLINE "-" MAJOR [" " MINOR]* [" " STATUS]
```

| Field | Values in this file | Meaning |
|-------|-------------------|---------|
| **Discipline** | `A` (Architectural), `S` (Structural), `E` (Electrical), `P` (Plumbing) | Which engineering trade owns the layer |
| **Major** | `WALL`, `COLUMN`, `POST`, `GLAZING`, `GLASS`, `SILL`, `FLOOR`, `DOOR`, ... | Element class |
| **Minor** | Material: `STEEL`, `CONCRETE`; Location: `EXTERNAL`, `INTERNAL`, `MEZZANINE`; Type: `FULL`, `FINISH`, `MULLION`, `ARRAY`, `PANEL`, `PARAPET`, `NICHE`; Variant: `1`, `2` | Qualifiers within the class |
| **Status** | `HATCH` (fill pattern companion) | Drawing representation variant |

Non-standard prefixes in this file:
- `GR_` = Group/Block reference (firm-specific convention for reusable block definitions)
- `AL` = Unknown (possibly Aluminum or miscoded Plumbing)

## Decomposition of Target Layers

### Walls

| Layer | Discipline | Major | Material | Qualifier | Notes |
|-------|-----------|-------|----------|-----------|-------|
| `A-EXTERNAL WALL` | A | WALL | — | EXTERNAL | Exterior building envelope |
| `A-MEZZANINE WALL FULL` | A | WALL | — | MEZZANINE, FULL | Full-height walls on mezzanine level |
| `A-MEZZANINE WALL FINISH` | A | WALL | — | MEZZANINE, FINISH | Finish layer (paint/cladding) on mezzanine walls |
| `A-WALL 1` | A | WALL | — | variant 1 | Wall type 1 (construction phase or material class) |
| `A-WALL 2` | A | WALL | — | variant 2 | Wall type 2 (different phase/material) |
| `A-PARTITION WALL` | A | WALL | — | PARTITION | Interior non-load-bearing dividers |
| `A-WALL PARAPET` | A | WALL | — | PARAPET | Low wall at roof/floor edge |
| `A-WALL NICHE` | A | WALL | — | NICHE | Recessed wall section |
| `A-WALL PANEL` | A | WALL | — | PANEL | Prefab or cladding panel |
| `S-CONCRETE WALL` | S | WALL | CONCRETE | — | Structural load-bearing concrete wall |

### Columns

| Layer | Discipline | Major | Material | Qualifier |
|-------|-----------|-------|----------|-----------|
| `S-COLUMN` | S | COLUMN | — | — (generic structural column) |
| `S-STEEL COLUMN` | S | COLUMN | STEEL | — |
| `S-CONCRETE COLUMN` | S | COLUMN | CONCRETE | — |
| `S-STEEL POST` | S | POST | STEEL | — (smaller than column, supports local load) |
| `S-COLUMN PROTECTION` | S | COLUMN | — | PROTECTION (fireproofing/bollard wrapping) |

### Curtain Wall / Glazing

| Layer | Discipline | Major | Material | Qualifier | Notes |
|-------|-----------|-------|----------|-----------|-------|
| `A-GLAZING MULLION` | A | GLAZING | — | MULLION | Vertical/horizontal framing bars |
| `A-GLAZING-MULLION` | A | GLAZING | — | MULLION | **Hyphen variant** — same element, different convention |
| `A-GLAZING FULL` | A | GLAZING | — | FULL | Full-panel glazing |
| `A-GLAZING-FULL` | A | GLAZING | — | FULL | **Hyphen variant** — different spatial zone |
| `A-GLAZING INTERNAL` | A | GLAZING | — | INTERNAL | Interior-facing glass |
| `A-GLAZING ARRAY` | A | GLAZING | — | ARRAY | Repeating panel pattern |
| `A-GLAZING SILL` | A | GLAZING | — | SILL | Bottom frame of glazing unit |
| `A-WALL SILL` | A | SILL | — | WALL | Sill at wall-glazing boundary (cross-classified) |
| `A-EXTERNAL GLASS` | A | GLASS | — | EXTERNAL | Exterior glass pane |
| `A-INTERNAL GLASS` | A | GLASS | — | INTERNAL | Interior glass pane |

## Naming Anomalies

### 1. Space vs Hyphen (`A-GLAZING FULL` / `A-GLAZING-FULL`)

The AIA standard separates words within a field using **spaces**. The hyphen is reserved for **field boundaries** (discipline-major). The hyphen-variant layers (`A-GLAZING-FULL`, `A-GLAZING-MULLION`) violate this convention.

Empirical finding: these are **not typos**. They occupy different spatial regions of the building and use different entity types. The naming difference likely encodes a different drafter, CAD tool, or project phase.

### 2. Unicode Non-Breaking Hyphen (U+2011)

Seven `A‑FLOOR *` layers use Unicode non-breaking hyphen (U+2011) instead of ASCII hyphen-minus (U+002D). This is a strong authorship signal — these layers were likely created by copy-pasting from a Word document, PDF, or non-AutoCAD tool into the DXF layer table.

Not in our target scope but relevant for generalization: the second test file may have similar encoding artifacts.

### 3. Cross-Discipline Elements

`S-CONCRETE WALL` is the only structural wall in a file dominated by architectural walls. The same physical concrete wall appears as `A-*` in the architectural model and `S-*` in the structural model. This is standard multi-discipline BIM practice — the discipline prefix tells you which engineer is responsible, not what the element is.

### 4. Cross-Classification (`A-WALL SILL`)

`A-WALL SILL` is assigned to the glazing family despite having `WALL` in its name. Architecturally correct: a sill is the bottom frame of a window or curtain wall opening. It belongs with the glazing system even though it interfaces with the wall.

### 5. Numeric Variants (`A-WALL 1`, `A-WALL 2`)

Each has its own HATCH companion layer (`A-WALL 1 HATCH`, `A-WALL 2 HATCH`), confirming they are intentionally separate. Common in multi-phase construction or when distinguishing wall types (e.g., drywall vs masonry).

### 6. Typo: `A-URNITURE FREE AREA`

Missing initial F (should be `A-FURNITURE FREE AREA`). Not a target layer but confirms the file was hand-authored.

## HATCH Companion Layers

Four wall layers have HATCH companions that represent the same physical elements as filled regions:

| Target Layer | Companion | Count | Notes |
|-------------|-----------|-------|-------|
| `A-EXTERNAL WALL` | `A-EXTERNAL WALL HATCH` | 24 HATCH entities | Sparse but authoritative |
| `A-MEZZANINE WALL FULL` | `A-MEZZANINE WALL FULL HATCH` | 1301 entities (LINE + LWPOLYLINE + HATCH) | Dense — both outlines and fills |
| `A-WALL 1` | `A-WALL 1 HATCH` | 11 HATCH entities | Sparse |
| `A-WALL 2` | `A-WALL 2 HATCH` | 126 entities (LINE + HATCH + LWPOLYLINE) | Mixed |

Three column layers also have HATCH companions not in the target scope:
- `S-COLUMN HATCH`
- `S-CONCRETE COLUMN HATCH`
- `S-STEEL COLUMN HATCH`

These are ground-truth polygon shapes for validation.

## ID Naming Scheme

Given the AIA grammar, output polygon IDs should preserve the discipline/major/qualifier decomposition:

```
{discipline}_{major}_{qualifier}_{index:04d}
```

### Examples

| Layer(s) | ID Pattern | Example |
|----------|-----------|---------|
| `A-EXTERNAL WALL` | `a_wall_ext_{N}` | `a_wall_ext_0001` |
| `A-PARTITION WALL` | `a_wall_part_{N}` | `a_wall_part_0042` |
| `A-MEZZANINE WALL FULL` | `a_wall_mezz_{N}` | `a_wall_mezz_0003` |
| `A-WALL 1` | `a_wall_v1_{N}` | `a_wall_v1_0010` |
| `S-CONCRETE WALL` | `s_wall_conc_{N}` | `s_wall_conc_0005` |
| `S-STEEL COLUMN` | `s_col_steel_{N}` | `s_col_steel_0015` |
| `S-CONCRETE COLUMN` | `s_col_conc_{N}` | `s_col_conc_0008` |
| `S-STEEL POST` | `s_post_steel_{N}` | `s_post_steel_0001` |
| `S-COLUMN PROTECTION` | `s_col_prot_{N}` | `s_col_prot_0003` |
| `A-GLAZING MULLION` + `-MULLION` | `a_glaz_mull_{N}` | `a_glaz_mull_0023` |
| `A-GLAZING FULL` + `-FULL` | `a_glaz_full_{N}` | `a_glaz_full_0107` |
| `A-GLAZING SILL` | `a_glaz_sill_{N}` | `a_glaz_sill_0044` |
| `A-WALL SILL` | `a_sill_wall_{N}` | `a_sill_wall_0012` |
| `A-EXTERNAL GLASS` | `a_glass_ext_{N}` | `a_glass_ext_0001` |
| Multi-layer polygon | `a_glaz_multi_{N}` | `a_glaz_multi_0005` |

### Edge Cases

- **Multi-layer polygons**: When a polygon has `source_layers` from multiple raw layers, the ID uses the canonical major + `multi` qualifier.
- **Cross-discipline**: `S-CONCRETE WALL` gets `s_wall_` prefix (not `a_wall_`) to preserve the structural discipline signal.
- **Unknown layers on second test file**: Fall back to `{discipline}_{major}_{N}` with no qualifier.
