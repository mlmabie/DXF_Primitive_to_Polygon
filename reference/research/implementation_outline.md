# Practical Implementation Outline: Augrade Take-Home

## What You Have (From Our Conversation That Applies Directly)

### 1. The Core Insight: This IS Tokenization

The DXF→polygon problem maps 1:1 to the grammar-tokenization framing:

| Grammar-GNN Concept | DXF Implementation |
|---------------------|-------------------|
| Characters | Individual LINE, ARC primitives |
| Tokens | Closed polygons |
| Grammar rules | Closure rules (endpoints connect, CW winding) |
| Parse tree | Polygon → primitives containment hierarchy |

**Implication:** Don't think "geometry algorithm." Think "how would I tokenize this?"

### 2. The Entropy Split: What's Stable vs What Varies

**Stable (hard-code confidently):**
- Polygon closure definition (cycle in endpoint graph)
- Winding direction check (CW = exterior)
- Basic validity (non-self-intersecting)
- Layer name → family mapping (given in spec)

**Variable (parameterize, log, don't over-engineer):**
- Snap tolerance (drafters vary; try 0.1, 0.5, 1.0 inches)
- Aspect ratio thresholds (what counts as "thin" wall vs column)
- Area bounds (min/max polygon size per family)
- Merge heuristics (when are two polygons really one wall?)

### 3. The Offramp Strategy: Ship Early, Iterate

**Offramp 1 (Minimum Viable):**
- Extract CIRCLE and closed LWPOLYLINE directly
- Call these "columns" if small, "walls" if large
- ~30% coverage, 1 hour work

**Offramp 2 (Solid Submission):**
- Add LINE→endpoint graph→cycle detection
- Filter cycles by family-specific heuristics
- ~60% coverage, 3 hours work

**Offramp 3 (Strong Submission):**
- Handle ARC interpolation
- Parallel pair detection for walls
- Grid detection for glazing
- ~80% coverage, 5+ hours work

**Ship Offramp 2 with clear documentation of what Offramp 3 would add.**

---

## Implementation Recipe

### Step 1: Data Loading (30 min)

```python
import ezdxf
from collections import defaultdict

def load_primitives(dxf_path, layer_families):
    dxf = ezdxf.readfile(dxf_path)
    msp = dxf.modelspace()
    
    primitives = defaultdict(list)
    for family, layers in layer_families.items():
        for layer in layers:
            for entity in msp.query(f'*[layer=="{layer}"]'):
                primitives[family].append({
                    'type': entity.dxftype(),
                    'layer': layer,
                    'entity': entity
                })
    return primitives
```

### Step 2: Fast Path Extraction (30 min)

```python
from shapely.geometry import Polygon, Point

def extract_direct_shapes(primitives):
    """Extract already-closed shapes: CIRCLE, closed LWPOLYLINE, HATCH bounds"""
    polygons = []
    
    for p in primitives:
        if p['type'] == 'CIRCLE':
            # Approximate circle as polygon
            center = p['entity'].dxf.center
            radius = p['entity'].dxf.radius
            circle = Point(center.x, center.y).buffer(radius, resolution=32)
            polygons.append({
                'vertices': list(circle.exterior.coords),
                'source_layers': [p['layer']],
                'source_type': 'CIRCLE'
            })
        
        elif p['type'] == 'LWPOLYLINE' and p['entity'].closed:
            pts = [(pt[0], pt[1]) for pt in p['entity'].get_points()]
            if len(pts) >= 3:
                polygons.append({
                    'vertices': pts,
                    'source_layers': [p['layer']],
                    'source_type': 'LWPOLYLINE'
                })
    
    return polygons
```

### Step 3: Endpoint Graph + Cycle Detection (1.5 hr)

```python
import networkx as nx
import numpy as np
from collections import defaultdict

def snap_endpoints(primitives, tolerance=0.5):
    """Snap nearby endpoints to same coordinate"""
    endpoints = []
    
    for p in primitives:
        if p['type'] == 'LINE':
            e = p['entity']
            endpoints.append((e.dxf.start.x, e.dxf.start.y, p))
            endpoints.append((e.dxf.end.x, e.dxf.end.y, p))
        elif p['type'] == 'ARC':
            # Interpolate arc to line segments
            e = p['entity']
            pts = list(e.flattening(0.1))  # Approximate arc
            for pt in [pts[0], pts[-1]]:
                endpoints.append((pt.x, pt.y, p))
    
    # Snap to grid
    snapped = {}
    for x, y, prim in endpoints:
        key = (round(x / tolerance) * tolerance, 
               round(y / tolerance) * tolerance)
        if key not in snapped:
            snapped[key] = []
        snapped[key].append((x, y, prim))
    
    return snapped

def build_graph(snapped_endpoints):
    """Build graph where edges are primitives"""
    G = nx.Graph()
    
    # Add edges for each primitive
    primitive_endpoints = defaultdict(list)
    for coord, points in snapped_endpoints.items():
        for x, y, prim in points:
            primitive_endpoints[id(prim)].append(coord)
    
    for prim_id, coords in primitive_endpoints.items():
        if len(coords) == 2:
            G.add_edge(coords[0], coords[1], primitive_id=prim_id)
    
    return G

def find_polygons(G, max_cycle_length=20):
    """Find all simple cycles (potential polygons)"""
    cycles = []
    for cycle in nx.simple_cycles(G):
        if 3 <= len(cycle) <= max_cycle_length:
            cycles.append(cycle)
    return cycles
```

### Step 4: Polygon Filtering by Family (1 hr)

```python
from shapely.geometry import Polygon as ShapelyPolygon

def filter_polygons(cycles, family):
    """Apply family-specific filters"""
    valid = []
    
    for cycle in cycles:
        poly = ShapelyPolygon(cycle)
        
        if not poly.is_valid or not poly.is_simple:
            continue
        
        area = poly.area
        bounds = poly.bounds
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        aspect = max(width, height) / (min(width, height) + 0.001)
        
        if family == 'columns':
            # Small, roughly square
            if area < 10000 and aspect < 3:
                valid.append((cycle, poly, area, aspect))
        
        elif family == 'walls':
            # Long and thin, OR larger area
            if aspect > 2 or area > 5000:
                valid.append((cycle, poly, area, aspect))
        
        elif family == 'glazing':
            # Similar to walls but check for grid alignment
            if aspect > 1.5:
                valid.append((cycle, poly, area, aspect))
    
    return valid
```

### Step 5: Output Generation (30 min)

```python
import json

def generate_output(results, output_path):
    output = {
        'walls': [],
        'columns': [],
        'curtain_walls': [],
        'metrics': {
            'runtime_seconds': 0,
            'primitives_consumed': 0,
            'primitives_total': 0
        }
    }
    
    for family, polygons in results.items():
        key = 'curtain_walls' if family == 'glazing' else family
        for i, (cycle, poly, area, aspect) in enumerate(polygons):
            output[key].append({
                'id': f'{family[:3]}_{i:04d}',
                'source_layers': [],  # Fill from tracking
                'vertices': [{'x_coord': x, 'y_coord': y} for x, y in cycle]
            })
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
```

### Step 6: Visualization (30 min)

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

def visualize(dxf_path, results, output_path):
    fig, ax = plt.subplots(figsize=(20, 20))
    
    # Draw raw primitives in gray
    dxf = ezdxf.readfile(dxf_path)
    for e in dxf.modelspace().query('LINE'):
        ax.plot([e.dxf.start.x, e.dxf.end.x], 
                [e.dxf.start.y, e.dxf.end.y], 
                color='lightgray', linewidth=0.5)
    
    # Draw polygons by family
    colors = {'walls': 'blue', 'columns': 'red', 'glazing': 'green'}
    for family, polygons in results.items():
        for cycle, poly, _, _ in polygons:
            patch = MplPolygon(cycle, fill=True, alpha=0.3, 
                              facecolor=colors[family], edgecolor=colors[family])
            ax.add_patch(patch)
    
    ax.set_aspect('equal')
    ax.autoscale()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
```

---

## Design Document (1-Page Version)

### Algorithm Choice: Graph Cycle Detection

**Why:** The problem of finding closed polygons from line segments is isomorphic to finding cycles in a graph where nodes are endpoints and edges are primitives. This is a well-studied problem with efficient solutions (NetworkX's cycle enumeration).

**Alternative considered:** DBSCAN clustering + alpha shapes. Works for isolated elements (columns) but fails for connected elements (walls sharing vertices).

### Per-Family Handling

| Family | Primary Strategy | Fallback |
|--------|-----------------|----------|
| **Walls** | Cycle detection + aspect ratio > 2 | Parallel pair detection |
| **Columns** | Direct CIRCLE/LWPOLYLINE extraction | Cycle detection + area < 10k |
| **Glazing** | Cycle detection + grid alignment check | Treat as thin walls |

### Known Failure Modes

1. **Unclosed primitives:** Some drafting leaves gaps > tolerance. Mitigation: adaptive tolerance, gap-closing heuristic.

2. **Over-segmentation:** One wall becomes many polygons due to internal lines. Mitigation: polygon merging by shared edges.

3. **Arc handling:** Arcs interpolated to polylines may lose precision. Mitigation: finer interpolation, arc-aware snapping.

### Trade-offs

| Decision | Trade-off |
|----------|-----------|
| Snap tolerance 0.5" | Risks false merges vs missing true connections |
| Max cycle length 20 | Limits complex shapes vs runtime |
| Aspect ratio 2.0 for walls | May miss square rooms vs include false positives |

### What More Time Would Enable

1. **Learned tolerance:** Use ML to predict optimal snap tolerance per file
2. **Hierarchical extraction:** Detect rooms (large polygons) then walls (boundaries)
3. **Cross-layer fusion:** Merge polygons from outline + hatch layers

---

## File Structure

```
augrade-takehome/
├── extract_polygons.py      # Main script
├── requirements.txt         # ezdxf, shapely, networkx, matplotlib, numpy
├── README.md               # Run instructions
├── DESIGN.md               # 1-page design doc
├── output/
│   ├── polygons.json       # Extracted polygons
│   └── visualization.png   # Overlay visualization
└── research_notes.md       # This document (optional, for interview discussion)
```

---

## Interview Pivot Points

When they ask "what would you do with more time?", pivot to our architecture:

1. **"The tolerance problem is learnable"** → GNN can learn per-element tolerances
2. **"Layer semantics are noisy"** → Sparse features can disambiguate
3. **"This doesn't scale to messy files"** → Need streaming/incremental approach
4. **"How do you validate?"** → Knowledge graph alignment with building codes

The take-home proves you can do the geometry. The interview proves you see the larger system.
