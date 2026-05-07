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

| run | walls | columns | curtain walls | coverage proxy | runtime | graph faces |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `conservative` (default) | 1169 | 764 | 304 | 51.3% | 1.9s | 436 |
| `coupled` (`--mode coupled`) | 1590 | 784 | 729 | 69.4% | 5.7s | 1302 |

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
- `INSERT`: 28

The scoped `INSERT`s are mostly on `A-GLAZING FULL`, with a few on external wall
and external glass layers. They reference small line/polyline blocks. A library
branch would be useful for robust block transforms and DXF edge cases, but it
would not replace the topology decision: even with `ezdxf`, the solver still has
to decide which primitive graph couplings produce valid architectural polygons.

## Read

This is a strong next-step direction, not a default replacement yet. The recovery
gain is real, but the coupled run is about 3x slower and needs closer visual
review at local zoom before it should replace the current submission default.
