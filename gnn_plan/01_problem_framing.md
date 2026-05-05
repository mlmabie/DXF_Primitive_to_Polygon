# Problem Framing

## Classification Target

The classification problem is not "read a drawing image." It is:

> Given unordered DWG/DXF primitives with no useful layer signal, infer which
> primitives or supervectors represent real architectural elements.

A supervector is a composed candidate above a raw primitive but below a final
BIM object. Examples:

- a connected chain of collinear line segments
- a closed polyline or hatch boundary
- a repeated panel/mullion cell
- a compact fixture-like symbol group
- a wall-face candidate recovered from endpoint closure
- a door-swing candidate composed from an arc plus adjacent lines

The model can classify at several granularities:

| Unit | Example label | Why it matters |
|---|---|---|
| primitive | wall-line, symbol-line, text-leader, noise | lowest-level supervision |
| supervector | wall face, door swing, fixture, pipe run, grid line | main target for this phase |
| relation | same element, adjacent, crosses, blocks, depends-on | merge and cascade target |
| component | wall assembly, room shell, plumbing route | downstream predictive target |

## Constraints

- No layer priors in the first experimental target.
- Preserve full vector detail and original coordinates.
- Avoid irreversible raster downsampling.
- Keep DWG-to-DXF conversion provenance if DWG is converted for processing.
- Keep labels tied to stable entity ids or derived geometry hashes.

## Why A Graph

CAD primitives are relational by construction. A line segment only becomes
meaningful when interpreted through neighboring endpoints, parallel offsets,
closures, repeated spacing, containment, and intersections. A graph gives a
natural place to represent those relationships without flattening everything
into pixels.

Useful graph signals include:

- endpoint coincidence or near-coincidence
- intersections and T-junctions
- parallelism and collinearity
- offset distance and wall thickness consistency
- containment and overlap
- repeated spacing
- local face adjacency
- symbol subgraph shape
- room, shaft, fixture, and wet-wall adjacency once inferred

## Rasterization Risk

Rasterization helps when annotations arrive as images or when a visual model
needs local context. It hurts when the system needs exact snapping, curve
fidelity, small gaps, line widths, or provenance. The setup should therefore
support raster context as a derived feature, not as the source of truth.

Recommended stance:

- **Core graph:** exact vector primitives, derived supervectors, typed edges.
- **Optional raster chip:** small local crop aligned to a node or edge for
  visual context.
- **Evaluation:** compare vector graph, raster baseline, and hybrid graph plus
  raster-chip model.

## Success Criteria

A useful setup should answer these questions on the first 4-5 annotated
examples:

- Can we build stable graph nodes from the unsorted primitive soup?
- Can annotations be mapped back to graph nodes without manual rework?
- Which classes are visually obvious but vector-ambiguous?
- Which classes require neighborhood context beyond local geometry?
- Does a non-graph baseline already solve most of the task?
- Where does message passing add value over hand-built geometry features?

