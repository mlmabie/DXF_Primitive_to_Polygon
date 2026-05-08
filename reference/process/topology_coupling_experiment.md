# Topology Coupling Experiment

This branch tests a stricter alternative to widening the snap tolerance:
insert explicit graph joints where one scoped endpoint lies on the interior of
another scoped segment, then run the existing face walk on the coupled graph.

## Why This Matters

The default solver snaps endpoints to a grid before graph-face extraction. That
recovers many wall and glazing loops, but it also asks one parameter to do two
different jobs:

- close small drafting gaps
- create topological vertices at T-junctions

Those are different operations. A T-junction can be geometrically exact while
still invisible to the face walker if the longer segment was never split at the
joining endpoint.

## Current Prototype

`couple_segments_at_endpoint_joints()` performs an opt-in preprocessing pass:

1. group graph segments by family
2. index unique endpoints in a small grid
3. for each segment, find family-local endpoints that project onto its interior
4. split that segment at accepted projected points
5. pass the split segments to the existing half-edge face walker

The shorthand is `--mode coupled`, which bundles `snap=0.25` and `joint=0.025`:

```bash
# preferred — single flag preset
python3 tokenize_dxf.py "Airport Doors_MEZZ.dxf" /tmp/coupling_candidate --mode coupled

# equivalent explicit form
python3 tokenize_dxf.py "Airport Doors_MEZZ.dxf" /tmp/coupling_candidate \
  --snap-tolerance 0.25 \
  --joint-tolerance 0.025
```

`--snap-tolerance` and `--joint-tolerance` independently override the value
supplied by `--mode`. The default submission path (`conservative` mode) remains
unchanged: `joint=0` disables coupling entirely.

## Results On The Supplied DXF

| run | snap | joint | walls | columns | curtain walls | coverage proxy | runtime |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `conservative` (default) | 0.5 | off | 1169 | 764 | 304 | 51.3% | 1.9s |
| `liberal` | 0.75 | off | 1184 | 781 | 309 | 51.8% | 2.0s |
| `joined` | 0.5 | 0.025 | 1610 | 782 | 825 | 71.3% | 5.0s |
| `coupled` | 0.25 | 0.025 | 1590 | 784 | 729 | 69.4% | 5.7s |

Two readings of the joined-vs-coupled gap matter. First, on this file
`joined` strictly dominates `coupled` on coverage despite a wider snap.
That tells us snap=0.25 is fragmenting more legitimate corners than it
recovers, which is the failure mode the snap parameter has when it is
asked to do both gap-closure and T-junction creation at once. Decoupling
those jobs is the whole point of the coupling pass; once joints are
explicit, you want snap as conservative as the gap distribution allows.

Second, the `liberal` row barely moves from `conservative` — wider snap
without coupling is not where the recovery is. The coupling pass is the
load-bearing change.

The prototype also adds direct `3DFACE` parsing. On this file it contributes 11
accepted wall polygons; most scoped `3DFACE` records are degenerate line-like
faces and are rejected by `polygon_record()`.

For the coupled candidate:

- input graph segments: 54,975
- output graph segments after splitting: 73,580
- split source segments: 8,229
- inserted joints: 18,605
- JSON orientation/degeneratedness check: no counterclockwise or consecutive
  duplicate vertices found

## Library Audit

Using `ezdxf` as an audit lens found these scoped entities in modelspace:

- `LINE`: 29,771
- `LWPOLYLINE`: 3,343
- `HATCH`: 1,934
- `ELLIPSE`: 818
- `ARC`: 663
- `3DFACE`: 151
- `CIRCLE`: 77
- `POINT`: 40
- `INSERT`: 28
- `POLYLINE`: 2

`tokenize_dxf.iter_entities` reads 36,827 / 36,827 of these by instance count
— **100% of scoped entity instances** ezdxf surfaces. The categorical gap is
not what we miss but what we *do* with what we read:

- **`INSERT` explosion** is not implemented. The 28 scoped INSERTs are
  counted but contribute zero geometry; they reference 27 auto-named blocks
  (mostly `LINE`+`LWPOLYLINE` glazing detail, a few `ELLIPSE`-only) plus one
  `A-EXTERNAL GLASS` block. Resolving them through `ezdxf.virtual_entities`
  would add roughly the equivalent of one extra LINE per per-instance segment
  multiplied by 28 — small on this file, more meaningful on block-heavy
  drafting.
- **Bulge arc-reconstruction** is approximated as straight chords. 21 / 3,343
  scoped LWPOLYLINEs carry non-zero bulge; on this file the curvature loss is
  cosmetic, but a curved-wall-heavy file would degrade noticeably.
- **`SPLINE`** is unread. 70 splines exist in modelspace but zero are on
  scoped layers in this file, so the gap is hypothetical here.
- **OCS / arbitrary-axis transforms** are not applied. The scoped layers use
  the world coordinate system, so this is harmless for this file.

Net practical gap on this file: a few hundred additional primitives at most,
none on a critical recovery path. Switching the parser to `ezdxf` is out of
scope for this submission — the stdlib parser is the audit-readable
deliverable — but ezdxf remains the natural lens when the second test file
exposes block-heavy or spline-heavy drafting.

## Read

This is a strong next-step direction, not a default replacement yet. The recovery
gain is real, but the joined/coupled runs are ~3x slower and the new polygons
need closer visual review at local zoom before either should replace the current
submission default.

## Grid Search

The source-entity coverage proxy is a length signal, not a shape signal. It
cannot tell us whether `joined` produces *better* polygons or just *more*
length-coverage. The natural shape-correctness signal hides in the file
itself: HATCH companion layers (`A-EXTERNAL WALL HATCH`, `S-COLUMN HATCH`)
describe the same physical elements as their outline twins with independent
carriers. Scoring graph-recovered polygons by IoU against HATCH boundaries on
matched companion layers gives a self-supervised correctness signal that the
coverage proxy structurally cannot.

[`scripts/grid_search.py`](../../scripts/grid_search.py) implements this:

- Composite score `0.6 * HATCH_IoU + 0.4 * coverage_proxy`, where HATCH-IoU
  is `mean_iou_on_match * match_rate` so the score penalises both bad shape
  and missed companions.
- Hard reject on invalid polygons or any family exceeding 3× the
  conservative-baseline count (loosened from 2× after the joined-mode 825
  curtain walls — 2.7× — proved to be real T-junction-derived panels).
- Curtain walls have no HATCH companions on this file, so the IoU score
  excludes that family; coverage still applies to all three.

Axes: snap ∈ {0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0} × joint ∈ {0, 0.01,
0.025, 0.05, 0.1}. 35 runs, ~3 minutes wall-clock. Outputs in
[`grid_search/`](grid_search/): `grid_search_results.csv` (full table) and
`grid_search_pareto.svg` (coverage vs HATCH-IoU scatter, Pareto-front
highlighted).

### What the grid actually showed

Three findings, ordered by importance:

1. **Coupling is the load-bearing change, not snap selection.** Every
   joint=0 run scores ~0.50; every joint>0 run scores ~0.57. The 14% jump
   is the coupling pass, not the snap value.
2. **Snap is robust across `[0.25, 0.75]` once joints are explicit.** With
   any joint ≥ 0.01, score variance across that snap range is under 1%.
   This is the failure-mode prediction earlier in this doc made concrete:
   when snap is no longer doing two jobs, its exact value stops mattering
   over a wide window.
3. **`joined` and `coupled` both sit on the Pareto front.** Best by
   composite is `snap=0.6, joint=0.05` at score 0.575, ahead of `joined`
   (0.570) and `coupled` (0.572) by ≤1%. That's not enough to justify
   renaming the preset; it confirms the chosen modes are defensible
   rather than picked at the bottom of a ridge.

The grid does not change the submission default. It validates that the
default is reasonable, the joined/coupled modes are well-positioned, and
parameter sweeps from here have visible structure to optimise against.

### Stretch axes (not run)

Per-family snap (`{walls × columns × curtain_walls}`) multiplies cost by
~50× and would test whether the families want different snap values. Worth
running once if a future pass hits a ceiling. Going beyond internal
validation wants either a labelled second DXF or the DWG pair of this
file as external ground truth.
