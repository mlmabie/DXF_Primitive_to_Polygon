# Annotation Intake

The next input is expected to be 4-5 annotated examples. This file defines how
to land them so they are useful for both classification and predictive/editing
experiments.

## Folder Layout

Use one folder per example:

```text
gnn_plan/data/examples/
  2026-05-05_example-name/
    source.dwg
    source.dxf
    preview.png
    annotations.json
    notes.md
```

If only one CAD format is available, keep the original and record any conversion
steps in `notes.md`.

## Minimum Notes

Each example should answer:

- What file did the annotation refer to?
- Was the annotation made on a raster preview, CAD file, or both?
- What classes are marked?
- Are labels primitive-level, supervector-level, component-level, or relation
  labels?
- Are there before/after or edit-cascade annotations?
- Which labels are certain and which are speculative?

## Suggested Annotation Schema

```json
{
  "example_id": "2026-05-05_example-name",
  "source_files": {
    "dwg": "source.dwg",
    "dxf": "source.dxf",
    "preview": "preview.png"
  },
  "coordinate_system": {
    "type": "cad",
    "units": "unknown",
    "image_to_cad_transform": null
  },
  "labels": [
    {
      "label_id": "L001",
      "unit": "supervector",
      "class": "wall",
      "geometry_ref": {
        "entity_ids": [],
        "bbox": [0, 0, 0, 0],
        "polyline": []
      },
      "confidence": "high",
      "notes": ""
    }
  ],
  "relations": [
    {
      "relation_id": "R001",
      "source_label_id": "L001",
      "target_label_id": "L002",
      "class": "same_element",
      "confidence": "medium",
      "notes": ""
    }
  ],
  "edit_events": [
    {
      "event_id": "E001",
      "action": "move_wall",
      "target_label_ids": ["L001"],
      "expected_impacts": ["L003", "L004"],
      "conflicts": [],
      "notes": ""
    }
  ]
}
```

## First Pass Triage

For each example:

1. Preserve original files.
2. Convert DWG to DXF only if needed, and record the converter and version.
3. Generate a preview image aligned to CAD coordinates.
4. Assign stable ids to primitives and supervectors.
5. Map every annotation to one of:
   - primitive id
   - supervector id
   - component id
   - relation between ids
   - edit event
6. Record ambiguity instead of forcing a label.

## Label Policy

Use clear labels first:

- wall
- door
- window
- column
- fixture
- plumbing
- shell
- room/region
- annotation/text
- dimension
- grid
- symbol
- unknown

Then add project-specific classes after the first examples reveal what matters.
Avoid overfitting the taxonomy before seeing the annotation style.

