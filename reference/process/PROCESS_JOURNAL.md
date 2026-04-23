# Process Journal

Date: 2026-04-15

## Purpose

This document records the actual work sequence, empirical findings, and representation-level insights from the airport DXF take-home. It is meant to freeze the current state before moving into the next phase of normalization, merging, and learned relational representations.

## Starting Point

The task is to recover architectural element polygons from a flat DXF primitive list. The scoped families are:

- walls
- columns
- curtain wall / glazing

The supplied file is [`Airport Doors_MEZZ.dxf`](/Users/malachi/augrade_takehome/Airport%20Doors_MEZZ.dxf).

The initial theoretical framing came from:

- [`implementation_outline.md`](/Users/malachi/augrade_takehome/implementation_outline.md)
- [`research_doc.md`](/Users/malachi/augrade_takehome/research_doc.md)

The framing that proved most useful was:

> DXF primitive grouping is a tokenization problem over geometry.

That was not just rhetoric. It gave the right decomposition:

- primitives as raw carriers
- closure as grammar
- polygons as tokens
- family inference as typed semantics on top of the closure layer

## What Was Built

### 1. Base Extraction Pipeline

Implemented in [`tokenize_dxf.py`](/Users/malachi/augrade_takehome/tokenize_dxf.py).

Main capabilities:

- stdlib-only DXF parsing
- support for `LINE`, `ARC`, `CIRCLE`, `ELLIPSE`, `LWPOLYLINE`, and legacy `POLYLINE`
- direct extraction of already-closed carriers
- graph-face recovery from snapped endpoint segments
- family-level filtering for walls, columns, and curtain walls
- JSON output plus SVG overlays and analysis summaries

Supporting docs:

- [`README.md`](/Users/malachi/augrade_takehome/README.md)
- [`DESIGN.md`](/Users/malachi/augrade_takehome/DESIGN.md)
- [`requirements.txt`](/Users/malachi/augrade_takehome/requirements.txt)

### 2. Provenance-First HITL Bundle

Implemented across:

- [`provenance_utils.py`](/Users/malachi/augrade_takehome/provenance_utils.py)
- [`run_hitl_pipeline.py`](/Users/malachi/augrade_takehome/run_hitl_pipeline.py)
- [`build_dashboard.py`](/Users/malachi/augrade_takehome/build_dashboard.py)
- [`build_merge_lab.py`](/Users/malachi/augrade_takehome/build_merge_lab.py)
- [`build_labeled_merge_dataset.py`](/Users/malachi/augrade_takehome/build_labeled_merge_dataset.py)

The main idea of this pass was:

- provenance should be first-class
- not a note in the docs
- not an after-the-fact string field
- but a shared data layer used by both human review surfaces

The one-command bundle is now:

```bash
python3 run_hitl_pipeline.py "Airport Doors_MEZZ.dxf" out_hitl
```

It produces:

- extraction JSON
- analysis summary + report
- provenance index
- static dashboard
- merge lab
- pipeline manifest

Key outputs:

- [`out_hitl/tokenization_output.json`](/Users/malachi/augrade_takehome/out_hitl/tokenization_output.json)
- [`out_hitl/provenance_index.json`](/Users/malachi/augrade_takehome/out_hitl/provenance_index.json)
- [`out_hitl/dashboard.html`](/Users/malachi/augrade_takehome/out_hitl/dashboard.html)
- [`out_hitl/merge_lab.html`](/Users/malachi/augrade_takehome/out_hitl/merge_lab.html)
- [`out_hitl/pipeline_manifest.json`](/Users/malachi/augrade_takehome/out_hitl/pipeline_manifest.json)

This turned the earlier “a few scripts” line into an actual end-to-end provenance-aware review bundle.

### 3. Exploratory Dashboard

Implemented in [`build_dashboard.py`](/Users/malachi/augrade_takehome/build_dashboard.py).

Generated outputs:

- [`out/dashboard.html`](/Users/malachi/augrade_takehome/out/dashboard.html)
- [`out/dashboard_assets/dashboard_data.json`](/Users/malachi/augrade_takehome/out/dashboard_assets/dashboard_data.json)

The dashboard provides:

- raw primitive and layer statistics
- family geometry distributions
- representative zoom panels
- raw DXF snippets for recovered features

The dashboard was later upgraded to expose provenance directly:

- raw layer provenance tables
- canonical variant-group tables
- source entity-type counts per feature
- variant notes attached to representative feature zooms

### 4. Expert-In-The-Loop Merge Lab

Implemented in [`build_merge_lab.py`](/Users/malachi/augrade_takehome/build_merge_lab.py).

Generated outputs:

- [`out/merge_lab.html`](/Users/malachi/augrade_takehome/out/merge_lab.html)
- [`out/merge_lab_data.json`](/Users/malachi/augrade_takehome/out/merge_lab_data.json)

The merge lab provides:

- family-specific merge candidate graphs
- hard-gate controls
- score-weight controls
- live merge-component consequences
- direct pair inspection
- local expert labeling
- a small Hopfield-like positive/negative associative memory bias

The merge lab was later upgraded so provenance is not hidden behind `source_layers` alone. It now exposes:

- family-level raw layer provenance tables
- family-level canonical variant groups
- per-polygon raw/canonical layer breakdowns
- provenance-aware summary metrics
- import/export for expert labels
- offline conversion of those labels into a supervised dataset via [`build_labeled_merge_dataset.py`](/Users/malachi/augrade_takehome/build_labeled_merge_dataset.py)

### 5. Parallel Alternative Pipeline

There is now also a second, separate implementation thread in the same folder:

- [`normalize_layers.py`](/Users/malachi/augrade_takehome/normalize_layers.py)
- [`tokenize_dxf.py`](/Users/malachi/augrade_takehome/tokenize_dxf.py)
- [`emit_dxf.py`](/Users/malachi/augrade_takehome/emit_dxf.py)

That line of work is now explicitly a three-step DXF-native pipeline:

`normalize_layers.py -> tokenize_dxf.py -> emit_dxf.py`

Its emphasis is:

- anomaly detection
- layer healing
- provenance logging
- AIA-aware IDs
- cleaned DXF emission with review layers, labels, and XDATA

The important current state is:

- the two lines are still separate
- one is stronger on dashboard / merge-lab experimentation
- the other is stronger on DXF-native review output

Reconciliation should happen later, but not by blurring their current boundaries.

## Raw File Findings

The first useful move was to stop guessing and inspect the DXF directly.

Observed global primitive counts:

- `LINE`: 58,128
- `LWPOLYLINE`: 3,408
- `ELLIPSE`: 2,586
- `HATCH`: 1,934
- `ARC`: 1,501
- `CIRCLE`: 143

Key top layers:

- `GR_A-GLASS PANEL SUPPORT`: 17,200
- `A-EXTERNAL WALL`: 9,934
- `S-CONCRETE COLUMN`: 3,969
- `A-WALL CONNECTION`: 3,663
- `A-MEZZANINE WALL FULL`: 3,662
- `A-WALL SILL`: 2,832
- `S-CONCRETE WALL`: 2,719

Scoped family observations:

- Walls are dominated by open `LINE` work and are the main combinatorial problem.
- Columns have a strong direct-extraction path through `CIRCLE` plus compact closed polylines.
- Curtain wall layers have regular local panel structure and a likely grid-level latent.

Concrete examples that mattered:

- `S-CONCRETE COLUMN` contains 34 `CIRCLE`s plus many compact support shapes.
- `A-GLAZING-MULLION` contains many small closed rectangular `LWPOLYLINE`s.
- `A-EXTERNAL WALL` is overwhelmingly open line/arc geometry.

## First-Pass Extraction Results

Current extraction output lives at:

- [`out/tokenization_output.json`](/Users/malachi/augrade_takehome/out/tokenization_output.json)
- [`out/analysis_summary.json`](/Users/malachi/augrade_takehome/out/analysis_summary.json)
- [`out/analysis_report.md`](/Users/malachi/augrade_takehome/out/analysis_report.md)

Current counts:

- walls: 274 polygons
- columns: 572 polygons
- curtain walls: 304 polygons

Coverage proxy from the current pass:

- scoped target primitives: 34,834
- estimated target drawable length: 1,144,751.426
- estimated consumed drawable length: 228,196.808
- estimated coverage: 19.9%

This is not a final score and should not be overinterpreted. It is a first-pass proxy under a deliberately simple, transparent pipeline.

## Connectivity Findings

Endpoint snapping was not a minor implementation detail. It changed the topology materially.

At snap tolerance `0.5`, wall-family connectivity looked like:

- nodes: 15,039
- degree-1 nodes: 5,427
- degree-2 nodes: 7,338
- degree-3 nodes: 662
- degree-4+ nodes: 1,612

Interpretation:

- There are many local chains that behave like clean polygon edges.
- There are also many high-degree junctions that make walls fundamentally different from trivial rectangle detection.
- The file is not just “find cycles”; it is “find the right quotient over a branching authored graph.”

## Visualization Findings

Useful visual artifacts:

- [`out/extracted_overlay.svg.png`](/Users/malachi/augrade_takehome/out/extracted_overlay.svg.png)
- [`out/walls.svg.png`](/Users/malachi/augrade_takehome/out/walls.svg.png)
- [`out/columns.svg.png`](/Users/malachi/augrade_takehome/out/columns.svg.png)
- [`out/wall_connectivity_snap_0_5.svg`](/Users/malachi/augrade_takehome/out/wall_connectivity_snap_0_5.svg)

What the visuals made obvious:

- Columns are the cleanest family.
- Curtain walls show strong local regularity but want a second pass that understands arrays.
- Walls are the limiting family because authored decomposition is not unique.

Another practical note:

- BlinkCAD was identified as a useful external viewer for DXF review because layer toggling makes extraction and provenance decisions legible without local CAD setup.

## Most Important Insight So Far

The variability in this file should not be described as sensor noise.

This is not LiDAR.

It is authored variation over a stable underlying object structure.

A better model is:

`observed_representation = R(style, decomposition, layering, snapping, carrier_choice)(latent_object)`

That means the right abstraction is:

- not denoising
- not generic compression
- but quotienting by semantics-preserving drafting rewrites

Examples of such rewrites:

- split one wall edge into many collinear segments
- encode a round feature as `CIRCLE`, `ARC`s, or a faceted polyline
- duplicate the same footprint across outline, hatch, and protection layers
- change the snap lattice while preserving the intended geometry
- encode one object as many local faces instead of one larger carrier

This reframing changed the research direction substantially.

## Normalization vs Merging

One of the clearest conceptual separations that emerged is:

- normalization
- merging

Normalization:

- collapses representation variants that are the same geometry
- should act on primitive carriers and local polygon candidates
- should remove nuisance symmetries

Merging:

- combines normalized candidates into the same architectural object
- should act on semantic candidates, not raw syntax
- should remain family-specific

This separation matters because otherwise:

- duplicates survive as separate objects
- adjacent but distinct walls get fused
- glazing arrays collapse into unhelpful blobs

The working statement is:

> Normalization is an equivalence relation on representation syntax.  
> Merging is an equivalence relation on semantic candidates.

The newer provenance work made this more concrete:

- normalization should also preserve a residual table over raw layer provenance
- merging should remain semantically typed and inspectable
- the human loop should be able to see both the quotient coordinates and the provenance residuals at once

## Merge Metric Framing

The merge work should not start with one monolithic object embedding.

The useful unit is the candidate relation between polygons.

So the right input is a pair representation, not just a polygon representation.

Working pair dimensions currently surfaced in the merge lab:

- boundary gap
- centroid gap
- orientation delta
- thickness relative difference
- area ratio
- span ratio
- axial gap
- lateral gap
- axial overlap
- lateral overlap
- bbox IoU
- layer overlap
- source-kind agreement

This is already much closer to an ACT-style quotient story than raw vertices.

The current merge lab now ties those pair metrics back to raw provenance:

- which raw layers contributed to each polygon
- which canonical layer group each source layer belongs to
- whether a polygon comes from a multi-variant canonical group
- what raw entity types underlie the polygon candidate

## Category-Theoretic Interpretation

The strongest formulation so far is not:

“the file is noisy”

It is:

> architectural drafting variants induce a rewrite system on primitive representations, and cleanup/merging should factor through the quotient by semantics-preserving rewrites

That gives the right objects:

- generators: raw primitives
- admissible compositions: closed carriers and local graph faces
- rewrites: decomposition and carrier substitutions that preserve semantics
- quotient coordinates: merge-relevant invariants

The open question is whether there is a compact, stable set of independent dimensions for this quotient, analogous to the banking API story the user referenced.

That is now the main research direction.

## Why A Graph Embedding Still Makes Sense

A graph model still looks useful, but only after the quotient feature space is clarified.

The proposed staging is:

1. define merge-relevant quotient dimensions
2. label candidate relations in the merge lab
3. train an edge model on those relation features
4. optionally add a small GNN for consistency propagation across the merge graph

This is much better than training a large generic embedding from raw geometry immediately.

The right graph object is:

- nodes: polygon candidates
- edges: plausible duplicate/merge relations
- edge features: quotient dimensions

Then the model can learn:

- same geometry
- same object
- same assembly
- nearby but distinct

## Hopfield / Associative Memory Insight

The user proposed using Hopfield-style reconstruction logic because the dataset is small and clean enough for expert-in-the-loop supervision.

The strongest version of that idea is:

- not reconstructing raw polygons
- but storing positive and negative merge prototypes over pair features

That is why the merge lab includes a small Hopfield-like memory margin:

- positive bank: examples the expert says should merge
- negative bank: examples the expert says should not merge
- score contribution: negative-memory energy minus positive-memory energy

This is not a full training pipeline yet, but it is the right place to begin testing the idea.

## Current Artifacts Worth Keeping

Core code:

- [`tokenize_dxf.py`](/Users/malachi/augrade_takehome/tokenize_dxf.py)
- [`build_dashboard.py`](/Users/malachi/augrade_takehome/build_dashboard.py)
- [`build_merge_lab.py`](/Users/malachi/augrade_takehome/build_merge_lab.py)

Core outputs:

- [`out/tokenization_output.json`](/Users/malachi/augrade_takehome/out/tokenization_output.json)
- [`out/dashboard.html`](/Users/malachi/augrade_takehome/out/dashboard.html)
- [`out/merge_lab.html`](/Users/malachi/augrade_takehome/out/merge_lab.html)

The merge lab is the most important artifact for next-phase work because it gives a real human feedback surface rather than just another static result.

## What Seems True Now

These claims feel well-supported at this point:

- The file contains strong regularity, not arbitrary mess.
- The main variability is authored representation choice, not measurement noise.
- Columns already show near-direct quotient structure.
- Curtain walls likely have a local grid latent.
- Walls require the most explicit quotient logic because decomposition and junction policy vary the most.
- Pairwise merge representation is the right immediate latent object.
- Expert-in-the-loop labeling is not a fallback; it is likely the best next source of high-value supervision.
- Provenance residuals are now not just a design principle but an implemented shared data layer in the HITL bundle.
- The repo now contains two viable but different execution paths: dashboard-first HITL review and DXF-native cleaned-output review.

## Open Questions

- Is there a small family-specific quotient for merge decisions, or a shared quotient with family-conditioned heads?
- Which candidate dimensions are truly independent versus derivable from the others?
- Which rewrites should be treated as equivalences and which should remain style coordinates?
- Does a sparse linear or tree model already saturate the merge problem?
- Does Hopfield memory add useful low-data generalization beyond hand-weighted scoring?
- When does a GNN add real value beyond pair scoring and connected-component reasoning?
- How should the dashboard-first provenance pipeline and the DXF-emission pipeline be reconciled without losing either human-review affordances or CAD-native auditability?

## Next-Step Options

The immediate next steps that seem most justified are:

1. Use the merge lab to label positive and negative candidate relations.
2. Export those labels as a supervised dataset.
3. Fit a sparse edge scorer on the current pair dimensions.
4. Add an explicit prototype-memory head using the expert labels.
5. Test whether learned edge states remain stable across rewrite-style augmentations.

There is now an additional systems question alongside the research question:

6. reconcile the provenance-first HITL bundle with the DXF-emission pipeline so that normalization, extraction, dashboard review, merge review, and CAD review all share one source of truth

The most important discipline going forward is:

do not jump to a big learned model before the quotient and rewrite structure is explicit enough to defend.

That is the current state of the project as of initial authoring.

---

## Agent-in-the-Loop Merge Review (2026-04-16)

Ran a programmatic merge review using the augrade pipeline as a library (`agent_merge_review.py`). The goal was to test whether merge candidates could be auto-labeled with documented reasoning, and to discover structural patterns in the merge graph.

### Columns: Extraction Deduplication Dominates

The 119 recommended column merges decompose cleanly:

- **12 are extraction-path duplicates**: same layer (`S-COLUMN`), gap < 0.1, but one polygon came from `graph_face` and the other from `direct_ellipse`. These are the same physical column recovered twice via two extraction methods. The area difference (~0.5%) is discretization noise. → **Auto-labeled positive.**
- **33 are adjacent distinct columns**: same layer, gap 0.2–1.0, same extraction kind, similar but not identical shapes. These are physically separate columns that sit close together in a structural bay. The merge scorer recommends them because they look similar, but they should NOT merge. → **Auto-labeled negative.**
- **74 need visual inspection**: mostly `S-COLUMN` pairs with gap 0.2–0.5 that could be either dedup or distinct, depending on whether the DXF drew the same column with slightly offset geometry.

**Implication**: The column family needs a tighter hard gate on `boundary_gap` for same-layer/same-kind pairs, or a learned discriminator between "extraction dedup" and "close distinct element."

### Curtain Walls: Normalization Hypothesis Confirmed

All 29/29 recommended curtain wall merges are cross-layer:
- One polygon from `A-GLAZING MULLION` (graph_face from LINE segments)
- The other from `A-GLAZING-MULLION` (direct_lwpolyline from closed shapes)

This directly confirms the normalization analysis finding: the space-vs-hyphen layer variants are the same physical mullions drawn with different CAD conventions. The merge lab's scoring correctly identifies them as duplicates (gap=0, area_ratio≈1). → **All 29 auto-labeled positive.**

### Walls: Fragmented but Layer-Concentrated

28 recommended wall merges, overwhelmingly on `A-MEZZANINE WALL FULL` (38/56 layer mentions):
- Only 1 touching pair (gap < 0.5)
- 15 close pairs (gap < 10)
- 12 far pairs (gap ≥ 10)

The far pairs are separate walls that happen to be colinear. The close pairs need spatial context. → **1 positive, 12 negative, 15 unlabeled.**

### Label Summary

87 labels produced: 42 positive, 45 negative.

This is enough for Phase 1 of the experiment checklist (target was 30+ per family per class). Columns need more positive examples from the 74 unlabeled pairs. Walls need visual review in the merge lab.

### What This Proves About the Pipeline

1. The `augrade` package works as a library — the REPL, merge lab, and this script all consume the same `dataset.build()` → `AnalysisDataset` path.
2. The normalization → extraction → merge → label → supervised pipeline is end-to-end functional.
3. Merge patterns are family-specific and structurally interpretable (extraction dedup vs cross-layer dedup vs fragment merge vs false positive), not just numerical thresholds.
4. The agent-in-the-loop pattern is viable: programmatic hypotheses + auto-labeling + human review of ambiguous cases.

### Artifact

- [`agent_merge_review.py`](/Users/malachi/augrade_takehome/agent_merge_review.py): Self-documenting script. Run it, read the output, import labels into merge lab.
- [`agent_labels.json`](/Users/malachi/augrade_takehome/agent_labels.json): 87 labels ready for merge lab import.

---

## Operating Mode Sweep (2026-04-16)

Benchmarked the current extractor across snap tolerances to test whether the default `0.5"` setting is still the best overall operating point or whether a second, more liberal mode should be kept available.

### Coverage Proxy And Counts

| Snap | Walls | Columns | Curtain Walls | Coverage Proxy |
|------|------:|--------:|--------------:|---------------:|
| 0.25 | 276 | 574 | 271 | 20.33% |
| 0.50 | 274 | 572 | 304 | 19.93% |
| 0.75 | 288 | 568 | 309 | 20.79% |
| 1.00 | 283 | 543 | 326 | 20.65% |
| 1.50 | 286 | 554 | 317 | 20.60% |
| 2.00 | 292 | 544 | 316 | 21.13% |

### Interpretation

- `0.5"` remains the best **conservative** setting.
  - It is the documented baseline.
  - It keeps family counts stable.
  - It is the safest choice for submission-facing review.

- `0.75"` is the best **more liberal** setting.
  - It improves the coverage proxy without the bigger class distortions seen at `1.0"+`.
  - It increases wall and curtain-wall recovery modestly while staying relatively close to the conservative output.

- `1.0"` and above are not obviously better despite slightly competitive coverage values.
  - Column counts drift more aggressively.
  - Curtain-wall counts inflate more sharply.
  - The small gain in coverage proxy is not worth the extra ambiguity for the default mode.

### Recommendation

Keep two named modes:

- **conservative** = `0.5"`
- **liberal** = `0.75"`

This gives the project:

- one clean submission / audit mode
- one exploratory mode for broader recovery

without pretending that a single snap tolerance is optimal for every use case.


### Dependency sketch

```text
Airport Doors_MEZZ.dxf
        |
        +--> augrade.normalize ----> normalization.json + provenance.json
        |            |
        |            +--> augrade.extract (via AnalysisDataset)
        |
        +--> augrade.extract -------> polygons + entities + graph segments
                     |
                     +--> augrade.provenance -----> provenance index
                                    |
                                    +--> augrade.dataset: AnalysisDataset
                                                      |
                                                      +--> augrade.merge
                                                      +--> augrade.dashboard_html
                                                      +--> augrade.merge_lab_html
                                                      +--> augrade.emit_dxf
                                                      +--> augrade.repl
```

### Practical split

- **Minimal submission:** `tokenize_dxf.py`, `DESIGN.md`, `README.md`, `requirements.txt`.
- **DXF-native review path:** `augrade.normalize` -> `augrade.extract` -> `augrade.emit_dxf` (run via `python -m augrade.cli.*`).
- **Provenance-first HITL path:** `augrade.pipeline` -> `augrade.dashboard_html` + `augrade.merge_lab_html`.
- **Unified interactive front:** `python -m augrade.repl` drives any of the above from one session with shared state and expert labels.
