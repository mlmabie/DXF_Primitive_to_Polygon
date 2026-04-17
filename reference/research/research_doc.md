# Research Document: From Grammar-GNN Architecture to Primitive-to-Polygon Reconstruction

**Author:** Malachi Mabie  
**Date:** April 2026  
**Context:** Augrade Technical Assessment

---

## Executive Summary

This document connects the theoretical ML architecture we discussed—grammar-learning tokenizers, GNN relational embeddings, sparse interpretable features, and knowledge graph alignment—to the concrete problem of reconstructing architectural elements from raw DXF primitives. The take-home task is, in a very real sense, a microcosm of the larger system architecture.

**Core insight:** The DXF→polygon reconstruction problem *is* the tokenization problem. Just as BPE tokenizers group characters into tokens without grammatical awareness, naive DXF parsers give you primitives without semantic structure. The challenge is identical: recover compositional structure from flat sequences.

---

## 1. The Theoretical Framework (From Our Conversation)

### 1.1 The Grammar-GNN Architecture

We discussed a system with two components:

| Component | Role | Entropy Profile |
|-----------|------|-----------------|
| **Grammar Induction** | Learn compositional rules for how primitives combine | Low-entropy scaffold |
| **GNN Embeddings** | Learn relational structure over parse/dependency graphs | High-entropy learning space |

The key insight was that standard tokenizers (BPE, etc.) are *grammatically blind*—they learn statistical co-occurrence, not compositional structure. A grammar-aware tokenizer would recognize that certain combinations form valid "phrases" (closed polygons, in our case).

### 1.2 The Sparse Feature Bridge

From the Goodfire EVEE architecture:

```
Dense Embeddings → Annotation Probes → Sparse Features → Knowledge Graph
```

Sparse features act as a *translation layer* between opaque neural representations and interpretable domain concepts. The same pattern applies here:

```
Raw Primitives → Spatial Graph → Polygon Features → Element Types (wall/column/glazing)
```

### 1.3 Temporal Persistence Hierarchy

We identified five timescales:

| Timescale | What Changes | Augrade Context |
|-----------|--------------|-----------------|
| Fundamental (years) | Ontology schema | Element types, polygon validity rules |
| Slow (quarterly) | Model weights, KG content | Layer→type mappings, tolerance params |
| Medium (weekly) | Project embeddings | Per-file heuristics |
| Fast (session) | Edit history | Current polygon state |
| Streaming (continuous) | Incoming events | Primitive-by-primitive processing |

---

## 2. The Take-Home Task: A Concrete Instance

### 2.1 The Problem Structure

**Input:** 67,000 primitives (LINE, ARC, LWPOLYLINE, CIRCLE, ELLIPSE, HATCH) across 111 layers

**Output:** Closed polygons grouped by element type (walls, columns, curtain walls)

**Challenge:** No grouping metadata. A "wall" is stored as disconnected line segments that a human perceives as belonging together due to spatial arrangement.

### 2.2 Mapping to Our Architecture

| Theoretical Concept | Take-Home Implementation |
|--------------------|--------------------------| 
| Grammar rules | Polygon closure rules (endpoints must connect, CW winding) |
| GNN nodes | Line/arc endpoints |
| GNN edges | Primitives connecting endpoints |
| Message passing | Connectivity propagation to find cycles |
| Sparse features | Polygon properties (area, aspect ratio, layer composition) |
| KG alignment | Layer name → element type mapping |

---

## 3. Algorithm Design: Three Strategies

### 3.1 Strategy 1: Graph Cycle Detection (Primary)

**Concept:** Build a spatial graph where nodes = endpoints, edges = primitives. Closed polygons = cycles in this graph.

```
Primitives → Endpoint Graph → Cycle Enumeration → Filter Valid Polygons
```

**Implementation:**
1. Snap endpoints within tolerance (handle drafting imprecision)
2. Build adjacency list from snapped endpoints
3. Find all simple cycles (DFS with backtracking, or NetworkX)
4. Filter: must be simple (non-self-intersecting), CW winding, reasonable size

**Why this works:** Directly implements the "grammar" of closed polygons—a polygon IS a cycle in the endpoint graph.

### 3.2 Strategy 2: Spatial Clustering + Convex Hull (Fallback for Columns)

**Concept:** Columns are small, spatially isolated clusters. Find dense regions, take convex hull or alpha shape.

```
Primitives → Spatial Clustering (DBSCAN) → Cluster → Alpha Shape
```

**When to use:** When cycle detection fails (open curves, drafting errors) but spatial isolation is clear.

### 3.3 Strategy 3: LWPOLYLINE/HATCH Extraction (Fast Path)

**Concept:** Some DXF entities are already closed—LWPOLYLINEs with `closed=True`, HATCH boundaries.

```
LWPOLYLINE[closed] ∪ HATCH.boundary → Direct Polygon Extraction
```

**When to use:** Always check this first. ~3,400 LWPOLYLINEs in the file, many already represent complete elements.

---

## 4. Per-Family Strategy

### 4.1 Walls (10 layers, ~17,000 primitives)

**Characteristics:**
- Long, thin rectangles or L-shapes
- Often represented by parallel line pairs
- May span multiple layers (outline + fill)

**Approach:**
1. Extract cycles from endpoint graph
2. Filter by aspect ratio (length >> width)
3. Merge polygons from related layers (e.g., outline + hatch fill)

**Grammar rule:** `WALL := RECT(aspect > 3) | L_SHAPE | PARALLEL_PAIR`

### 4.2 Columns (5 layers, ~9,000 primitives)

**Characteristics:**
- Small, roughly equilateral shapes (circles, squares, H-profiles)
- Spatially isolated (columns don't touch each other)
- Often include CIRCLE primitives (round columns)

**Approach:**
1. Direct extraction: CIRCLE, closed LWPOLYLINE
2. Cycle detection for LINE-based columns
3. DBSCAN clustering as fallback
4. Filter by size (area < threshold) and aspect ratio (~1)

**Grammar rule:** `COLUMN := CIRCLE | RECT(aspect ≈ 1) | H_PROFILE`

### 4.3 Curtain Walls / Glazing (10 layers, ~9,000 primitives)

**Characteristics:**
- Linear arrays of rectangular panels
- Mullions form grid patterns
- Often co-located with wall layers (sill)

**Approach:**
1. Detect grid structure (regular spacing)
2. Extract individual panel rectangles
3. Group panels by alignment (same row/column in grid)

**Grammar rule:** `CURTAIN_WALL := GRID(PANEL+) where PANEL := RECT`

---

## 5. What This Demonstrates About the Larger Architecture

### 5.1 The "Easy Intelligence" vs "Hard Intelligence" Split

| Category | This Task | Full System |
|----------|-----------|-------------|
| **Easy intelligence** (absorb from tools/libs) | Shapely geometry, NetworkX cycles, ezdxf parsing | Frontier VLMs, perception encoders |
| **Hard intelligence** (build yourself) | Layer→type mapping, aspect ratio thresholds, tolerance calibration | Domain ontology, validator logic, workflow traces |

The take-home tests whether you know *where the hard problems are*. Cycle detection is easy (library call). Deciding *which* cycles are walls vs noise is hard (domain knowledge).

### 5.2 The Offramp Ladder

This task sits at **Layer 1-2** of the architecture we discussed:

```
Layer 1: Geometric Perception (primitives → endpoints)     ← THIS TASK
Layer 2: Object Formation / Tokenization (endpoints → polygons) ← THIS TASK  
Layer 3: Graph Construction (polygons → typed relationships)
Layer 4: GNN Core (constraint propagation)
Layer 5: Sparse Feature Bridge (interpretable properties)
Layer 6: Knowledge Alignment (building codes, physics)
Layer 7: Edit/Plan Layer (autonomous modification)
```

Demonstrating competence at Layers 1-2 is the *entry point*. The interview conversation should pivot to: "Given this foundation, here's how the higher layers work."

### 5.3 The Grammar Induction Connection

The per-family "grammar rules" above (`WALL := RECT(aspect > 3)`, etc.) are exactly the low-entropy scaffold we discussed. They're:

- **Stable:** These rules don't change across projects
- **Compositional:** Walls are made of rectangles, curtain walls are made of panel grids
- **Interpretable:** A human can read and validate them

The GNN's job (in the full system) is to *learn* these rules from data, not have them hand-coded. But for a take-home, hand-coding demonstrates you understand *what the rules are*.

---

## 6. Failure Modes and Mitigations

| Failure Mode | Cause | Mitigation |
|--------------|-------|------------|
| Unclosed cycles | Drafting gaps > tolerance | Increase snap tolerance, then prune by gap size |
| Self-intersecting polygons | Complex wall shapes | Convex decomposition or accept as multiple polygons |
| Over-segmentation | One wall = many small polygons | Merge adjacent polygons with shared edges |
| Under-segmentation | Multiple walls = one polygon | Layer-based splitting, geometric heuristics |
| Missing elements | Primitives on unexpected layers | Log warnings, document coverage metrics |

---

## 7. Implementation Plan

### Phase 1: Data Loading & Exploration (30 min)
- Parse DXF with ezdxf
- Inventory primitives per layer
- Visualize sample regions

### Phase 2: Core Algorithm - Cycle Detection (2 hr)
- Implement endpoint snapping
- Build adjacency graph
- Find cycles with NetworkX
- Basic filtering (size, winding)

### Phase 3: Per-Family Specialization (2 hr)
- Walls: aspect ratio filtering, parallel pair detection
- Columns: direct circle extraction, DBSCAN fallback
- Glazing: grid detection

### Phase 4: Output & Visualization (1 hr)
- JSON serialization with metrics
- SVG/DXF overlay visualization
- Coverage calculation

### Phase 5: Documentation (30 min)
- README with run instructions
- Design document (this, condensed to 1 page)
- requirements.txt

---

## 8. Conclusion: The Larger Bet

This take-home is a hiring filter, but it's also a *research question*: Can the primitives→polygons problem be solved robustly without ML?

**My hypothesis:** For well-drafted files with consistent conventions, yes—geometric algorithms suffice. For messy real-world files from diverse drafters, no—you need learned representations that can handle variation.

The full Augrade system needs both:
1. **Geometric algorithms** as the low-entropy scaffold (what this task tests)
2. **Learned representations** as the high-entropy adaptation layer (what the GNN provides)

Demonstrating #1 competently earns the right to discuss #2 in the interview.

---

## Appendix: Code Skeleton

```python
# Conceptual structure - not runnable code
class DXFPolygonExtractor:
    def __init__(self, tolerance=0.1):
        self.tolerance = tolerance
        self.layer_families = {
            'walls': ['A-EXTERNAL WALL', ...],
            'columns': ['S-STEEL COLUMN', ...],
            'glazing': ['A-GLAZING MULLION', ...]
        }
    
    def extract(self, dxf_path):
        primitives = self.load_primitives(dxf_path)
        
        results = {}
        for family, layers in self.layer_families.items():
            family_primitives = self.filter_by_layers(primitives, layers)
            
            if family == 'columns':
                polygons = self.extract_columns(family_primitives)
            elif family == 'walls':
                polygons = self.extract_walls(family_primitives)
            else:
                polygons = self.extract_glazing(family_primitives)
            
            results[family] = polygons
        
        return results
    
    def extract_columns(self, primitives):
        # Fast path: circles and closed polylines
        direct = self.extract_direct_shapes(primitives)
        
        # Slow path: cycle detection for LINE-based columns
        graph = self.build_endpoint_graph(primitives)
        cycles = self.find_cycles(graph)
        
        # Filter by column-like properties
        return self.filter_by_shape(direct + cycles, 
                                     max_area=10000, 
                                     aspect_ratio_range=(0.5, 2.0))
```

---

*End of Research Document*
