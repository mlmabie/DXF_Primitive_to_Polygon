# Research Map

Retrieved: 2026-05-05.

This is a seed map, not a complete literature review. The useful thread across
the papers is consistent: vector-native or graph-structured representations are
the right place to preserve detail, while raster or CNN features can help as
auxiliary context.

## Directly Relevant To Layer-Blind CAD Graph Classification

### Generalizing Floor Plans Using Graph Neural Networks

Simonsen, Thiesson, Philipsen, and Moeslund, ICIP 2021.

Why it matters:

- extracts graphs directly from CAD primitives
- classifies graph nodes as door or non-door
- compares against a raster Faster R-CNN baseline
- publishes graph and image floor-plan representations

Source: https://resourcecenter.ieee.org/conferences/icip-2021/spsicip21vid276

### Multi-Classification Of CAD Entities

Kurupathi, Bosse, Park, and Eisert, 2024.

Why it matters:

- explicitly frames CAD floor-plan recognition as entity-as-node GNN
- argues that GNNs preserve CAD structure without rasterization
- compares GAT, GATv2, GANet, PNA, and UniMP-style architectures
- targets symbols such as walls, doors, and windows

Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4957759

### FloorPlanCAD

Fan et al., ICCV 2021.

Why it matters:

- large vector CAD dataset with more than 10,000 floor plans
- line-grained annotations across 30 object categories
- combines CNN and GCN for panoptic symbol spotting
- useful benchmark reference for line-level labels and class taxonomy

Source: https://researchportal.hkust.edu.hk/en/publications/floorplancad-a-large-scale-cad-drawing-dataset-for-panoptic-symbo/

### VectorGraphNET

Carrara, Nousias, and Borrmann, Journal of Computing in Civil Engineering
2025.

Why it matters:

- technical drawing segmentation over vector data
- graph attention transformer
- hierarchical labels
- evaluated on FloorPlanCAD among other datasets
- relevant to line-level classification and AEC drawing workflows

Source: https://portal.fis.tum.de/en/publications/vectorgraphnet-graph-attention-networks-for-accurate-segmentation/

## Relevant To Preserving Vector Detail Instead Of Raster Detail

### VectorFloorSeg

Yang, Jiang, Pan, and Xiao, CVPR 2023.

Why it matters:

- directly operates on vector floorplans
- dual stream: line segments and partitioned regions
- graph attention fuses heterogeneous line/region evidence
- reports stronger room segmentation and boundary regularity than image-based
  approaches

Source: https://openaccess.thecvf.com/content/CVPR2023/html/Yang_VectorFloorSeg_Two-Stream_Graph_Attention_Network_for_Vectorized_Roughcast_Floorplan_Segmentation_CVPR_2023_paper.html

### Indoor Elements Classification Via Floor Plan Graphs

Song and Yu, ISPRS IJGI 2021.

Why it matters:

- converts floor plan data to a region adjacency graph
- classifies walls, doors, symbols, rooms, and corridors
- stresses shape preservation over pixel-only segmentation
- introduces distance-weighted graph learning for spatial graph data

Source: https://www.mdpi.com/2220-9964/10/2/97

## Relevant To Predictive Editing And System Reasoning

### Graph Neural Networks For 2D Architectural Detail Drawings

Ko and Lee, Automation in Construction 2025.

Why it matters:

- standardizes architectural drawings into graph format
- evaluates GNN architectures, pooling, node features, and masking
- includes classification and error detection
- points toward explainable AI for drawing review

Source: https://www.sciencedirect.com/science/article/abs/pii/S0926580524006721

### Semantic Floorplan Segmentation Using Self-Constructing Graph Networks

Knechtel, Rottmann, Haunert, and Dehbi, Automation in Construction 2024.

Why it matters:

- combines CNN and GCN for long-range floor-plan dependencies
- learns or induces graph structure from image features
- includes layout graph inference, connectivity, adjacency, and missing-link
  style use cases
- useful as a hybrid baseline, not as the primary vector-preserving path

Source: https://www.sciencedirect.com/science/article/pii/S0926580524003856

### Predicting Building Layout Structure And Features Via Planar Duality

Hu, Zhang, Yao, Xu, Chen, and Sun, Automation in Construction 2025.

Why it matters:

- uses vertex-edge-face representation
- improves message passing through face adjacency
- predicts architectural layout structure and feature parameters
- supports the idea that faces/regions should be explicit graph objects for
  predictive editing

Source: https://www.sciencedirect.com/science/article/abs/pii/S0926580525007216

## Working Takeaways

- Start with a vector-native graph, not a raster-first model.
- Add supervector nodes so the GNN is not forced to learn every composition
  rule from primitives alone.
- Include faces/regions explicitly once shell and route reasoning starts.
- Keep raster chips as optional context and as a baseline comparison.
- Use non-GNN baselines first. A graph model is useful only where relation
  propagation or component consistency beats local geometry features.
