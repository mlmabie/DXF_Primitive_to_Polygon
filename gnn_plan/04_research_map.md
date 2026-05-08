# Research Map

Retrieved: 2026-05-05. Last updated: 2026-05-08.

This is a seed map, not a complete literature review. The useful thread across
the papers is consistent: vector-native or graph-structured representations are
the right place to preserve detail, while raster or CNN features can help as
auxiliary context.

For the review workflow, source links, and per-source poster prompts, see
[`07_source_review_prompts.md`](07_source_review_prompts.md) and
`reference/reviews/source_review_tracker.csv`.

For the per-claim anchor list (which paper supports which talk-track claim) see
[`TALK_TRACK.md`](TALK_TRACK.md).

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
- 1.3M weights vs 31–65M for raster baselines (PanCADNet, CADTransformer,
  SymPoint), a strong cost-of-vector-native argument

Source: https://portal.fis.tum.de/en/publications/vectorgraphnet-graph-attention-networks-for-accurate-segmentation/

Preprint: https://arxiv.org/abs/2410.01336

### Symbol As Points (SymPoint) And SymPoint-V2

Liu, Tang, Hu, and Yu, ICLR 2024 (SymPoint); Liu et al. 2024 (SymPoint-V2).

Why it matters:

- frames vector primitives as a point cloud and uses a point transformer
  with a Mask2Former-style spotting head
- SymPoint-V2 reaches 90.1 PQ on FloorplanCAD by adding layer-feature
  enhancement and position-guided training
- the layer-feature module explicitly demonstrates how authored-layer signal
  *helps* large-graph reasoning, which makes it a useful counterpoint to the
  layer-blind first-pass assumption: the right move is not to reject layers
  forever but to first prove the model can stand without them

Sources:

- https://openreview.net/forum?id=aOnUe8ah7j
- https://arxiv.org/abs/2401.10556
- https://arxiv.org/abs/2407.01928

### CADSpotting

Wang et al., 2024.

Why it matters:

- targets large-scale CAD drawings where naive primitive graphs run out of
  memory or context budget
- densely samples points along graphic primitives, then runs Point
  Transformer V3 plus a sliding-window aggregation with weighted voting and
  NMS
- relevant as a scale baseline: when the take-home file already has 67k
  primitives, real BIM drawings will dwarf that and need windowed strategies

Source: https://arxiv.org/abs/2412.07377

### Raster-To-Graph

Hu, Chen, Yao, Xu, and Sun, Computer Graphics Forum 2024.

Why it matters:

- autoregressive graph prediction with an attention transformer for
  floorplan recognition
- complementary to vector-first approaches: useful when the input arrives as
  a raster scan instead of clean DXF

Source: https://onlinelibrary.wiley.com/doi/10.1111/cgf.15007

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

### Clash Context Representation And Change Component Prediction (MEP GCN)

Sun and colleagues, Advanced Engineering Informatics 2023.

Why it matters:

- direct evidence that GCN-based models can predict which BIM components
  must change in response to a clash, given local context features
- closest published analogue to the edit-cascade flavor in
  [`03_predictive_editing.md`](03_predictive_editing.md)
- supports the validator-driven framing: cascades follow from clashes
  detected by deterministic checks, with a learned head deciding *which*
  components change

Source: https://www.sciencedirect.com/science/article/abs/pii/S1474034623000241

### Incorporating Context Into BIM-Derived Data With GNNs

MDPI Buildings 2024.

Why it matters:

- frames BIM element classification as a context-aware GNN problem
- explicitly motivates moving beyond single-element features to neighborhood
  reasoning
- useful as a "do GNNs help here" anchor for the IFC/BIM end of the stack

Source: https://www.mdpi.com/2075-5309/14/2/527

### IFC BIM Model Enrichment With Space Function Information Using GNNs

Wang et al., MDPI Energies 2022.

Why it matters:

- three-step method enriching IFC representations with room-function labels
  via GNN
- useful when the system later has to assign function-level semantics
  (kitchen / living / wet wall / chase) to recovered regions

Source: https://www.mdpi.com/1996-1073/15/8/2937

### Optimized GNNs For Spatial Recognition In BIM Semantic Enrichment

Engineering Applications of Artificial Intelligence 2025.

Why it matters:

- explores node-feature design and edge-feature use for BIM enrichment
- proposes Node-Enhanced Graph-BERT incorporating edge features
- direct support for the typed-edge feature inventory in
  [`02_graph_representations.md`](02_graph_representations.md)

Source: https://www.sciencedirect.com/science/article/abs/pii/S0952197625003653

### Automated BIM Generation For MEP Systems From CAD Data

Automation in Construction 2025.

Why it matters:

- uses graph structures to represent MEP systems and integrate information
  across multiple CAD drawings
- pipeline-component matching with missing-information inference
- aligns with the "infer systems inside a shell" flavor of predictive
  editing once shell + fixtures + chases exist as graph nodes

Source: https://www.sciencedirect.com/science/article/abs/pii/S0926580525005825

### Neural Relational Inference

Kipf, Fetaya, Wang, Welling, and Zemel, ICML 2018.

Why it matters:

- learns latent interaction graphs while modeling system dynamics
- useful analogy for discovering hidden dependency/interaction relations from
  edits, validation outcomes, and revision traces
- relevant to relation types such as same-element, depends-on, blocks,
  routes-through, must-move-with, and violates-with

Source: https://proceedings.mlr.press/v80/kipf18a.html

### Graph Edit Networks

Paassen, Schulz, Stewart, and Hammer, ICLR 2021.

Why it matters:

- explicit output layer that emits a sequence of typed graph edits to
  transform an input graph into an output graph
- direct architectural support for the residual-edit-token framing in
  [`03_predictive_editing.md`](03_predictive_editing.md) and
  [`SYSTEM_SPEC.md`](SYSTEM_SPEC.md) module M6
- shows that learning over edit deltas is feasible without going through
  whole-scene regeneration

Source: https://openreview.net/forum?id=dlEJsyHGeaL

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

## Adjacent Threads Worth Naming

These do not anchor the core plan but are useful to acknowledge so the
direction is not surprised by them in conversation.

### Object-Centric World Models

FOCUS (Frontiers in Neurorobotics 2025), Slot Structured World Models, and
Dyn-O (NeurIPS 2025) all argue that object-centric latent state plus a
relational dynamics module (typically a GNN or relational transformer) gives
better multi-step generalization than monolithic encoders. The Augrade
analogy is exact: typed object tokens, typed relation tokens, and a small
relational module above them, with a deterministic state transition for the
parts that should stay exact.

Sources:

- https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2025.1585386/full
- https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/dyno_neurips2025.pdf

### CAD-LLM / Design-Intent Agents

CADDesigner, CAD-LLM, and the Autodesk constraint-generation work explore
LLM agents that emit parametric CAD code from natural language and sketches.
This is orthogonal to the GNN thread: it lives at the intent-and-program
end, not the geometry-and-relation end. Useful to keep on the radar as a
later interface layer above the structured graph state, not as a competitor
to it.

Sources:

- https://arxiv.org/html/2508.01031 (CADDesigner)
- https://www.research.autodesk.com/publications/ai-lab-cad-llm/
- https://www.research.autodesk.com/app/uploads/2025/10/Aligning-Constraint-Generation-with-Design-Intent-in-Parametric-CAD.pdf

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
