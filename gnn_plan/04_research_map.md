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

### Neural Relational Inference

Kipf, Fetaya, Wang, Welling, and Zemel, ICML 2018.

Why it matters:

- learns latent interaction graphs while modeling system dynamics
- useful analogy for discovering hidden dependency/interaction relations from
  edits, validation outcomes, and revision traces
- relevant to relation types such as same-element, depends-on, blocks,
  routes-through, must-move-with, and violates-with

Source: https://proceedings.mlr.press/v80/kipf18a.html

### Temporal Straightening For Latent Planning

Wang, Bounou, Zhou, Balestriero, Rudner, LeCun, and Ren, 2026.

Why it matters:

- optimizes representations so latent trajectories are better conditioned for
  planning
- supports the idea that edit/revision embeddings should make repair distance
  and validator-residual progress geometrically meaningful
- later-stage objective for residual edit trajectories, not an MVP requirement

Source: https://arxiv.org/abs/2603.12231

## Relevant To Representation Boundaries

### Geometric Deep Learning

Bronstein, Bruna, Cohen, and Velickovic, 2021.

Why it matters:

- gives the umbrella language for grids, groups, graphs, geodesics, gauges,
  locality, hierarchy, and symmetry
- supports graph/geometric priors for architectural data without requiring an
  end-to-end learned geometry engine
- helps explain why GNNs belong in the relational consistency layer above
  object formation

Source: https://arxiv.org/abs/2104.13478

### A Mechanistic Analysis Of Sim-And-Real Co-Training

Lei, Liu, Maddukuri, Jiang, and Zhu, 2026.

Why it matters:

- useful frame for cross-domain alignment while preserving domain identity
- maps cleanly onto "pool for geometry, tag for provenance"
- suggests testing rewrite-invariance rather than assuming authored CAD
  variation is random noise

Source: https://arxiv.org/abs/2604.13645

### Geometric Algebra Transformer

Brehmer, de Haan, Behrends, and Cohen, 2023.

Why it matters:

- representation choice is central: put geometric objects in a space where
  geometric queries are natural
- relevant to frames, directions, surfaces, clearances, and support relations
- useful as design vocabulary even if CAD rewrite symmetries are not clean Lie
  group actions

Source: https://arxiv.org/abs/2305.18415

### Choosing A Geometric Algebra For Equivariant Transformers

de Haan, Cohen, and Brehmer, AISTATS 2024.

Why it matters:

- emphasizes that carrier choice changes expressivity, compute, and the
  symmetry group the model respects
- reinforces choosing primitive, supervector, relation, face, component,
  constraint, and edit tokens around the task interface

Source: https://proceedings.mlr.press/v238/haan24a.html

### Any-Subgroup Equivariant Networks Via Symmetry Breaking

Goel, Lim, Lawrence, Jegelka, and Huang, ICLR 2026.

Why it matters:

- useful vocabulary for family-conditioned invariance
- supports testing shared model vs family-conditioned heads vs separate
  family models
- later-stage architecture idea, not the first baseline

Source: https://openreview.net/forum?id=jz3d7nvtGz

## Relevant To System Interfaces, Calibration, And Memory

### Scalable Co-Design Via Linear Design Problems

Cai, Huang, Alharbi, and Zardini, 2026.

Why it matters:

- compositional design problems need stable interfaces
- closer to the practical Augrade claim than generic end-to-end generation
- supports freezing object identity, edit grammar, validator boundary, evidence
  links, and traces

Source: https://arxiv.org/abs/2603.29083

### A Mathematical Theory Of Co-Design

Censi, 2015.

Why it matters:

- foundational background for compositional design interfaces
- useful for thinking about feasibility, resources, and constraints across
  coupled engineered subsystems
- background citation; Cai et al. is the more tactical reference for this plan

Source: https://arxiv.org/abs/1512.08055

### Algorithmic Learning In A Random World

Vovk, Gammerman, and Shafer, 2005 / 2022.

Why it matters:

- conformal prediction is a natural fit for auto-merge/reject/review bands
- calibration and review-load reduction matter more than a single average F1
- especially relevant for small labels and drafter-style shift

Sources:

- https://www.alrw.net/
- https://link.springer.com/book/10.1007/978-3-031-06649-8

### Dense Associative Memory With Exponential Capacity

Shafiei Kafraj, Krotov, and Latham, 2026.

Why it matters:

- possible low-label prototype memory after relation features stabilize
- useful for positive/negative merge exemplars and ambiguous boundary cases
- should augment sparse pair scoring, not replace geometry or validators

Source: https://arxiv.org/abs/2601.00984

### Goodfire EVEE

Goodfire, 2026.

Why it matters:

- industry example of turning rich embeddings into structured, interpretable
  predictions
- transferable lesson is the probe/readout layer, not the biology domain
- cite as an industry research resource rather than a peer-reviewed BIM paper

Source: https://www.goodfire.ai/research/evee-explaining-genetic-variants

### Entropy-Preserving Reinforcement Learning

Petrenko, Lipkin, Chen, Wijmans, Cusumano-Towner, Giryes, and Krähenbühl,
ICLR 2026.

Why it matters:

- policy-gradient training can reduce trajectory diversity unless entropy is
  monitored and controlled
- relevant to future graph-edit policies where multiple valid repairs should
  remain discoverable
- belongs after typed actions, validators, and sparse baselines are working

Source: https://arxiv.org/abs/2603.11682

## Working Takeaways

- Start with a vector-native graph, not a raster-first model.
- Add supervector nodes so the GNN is not forced to learn every composition
  rule from primitives alone.
- Include faces/regions explicitly once shell and route reasoning starts.
- Keep convolutional/raster chips as optional context and as a baseline
  comparison.
- Use non-GNN baselines first. A graph model is useful only where relation
  propagation or component consistency beats local geometry features.
- Keep deterministic validators outside the learned model.
- Use calibrated uncertainty to decide auto-merge, reject, or review.
- Test rewrite-invariance across authored CAD variations before trusting a
  learned relation scorer.
- Treat future RL/search as an entropy-monitored sequential graph-edit loop,
  not as the starting point.
