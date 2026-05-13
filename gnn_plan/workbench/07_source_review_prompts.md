# Source Review Prompts

Use this file as the review queue. For each source, copy the link and prompt into a fresh thread, ask for a poster-ready summary, then paste the result into `reference/reviews/compiled/` or a future literature-review doc.

## Review protocol

1. Start with Tier 0 sources.
2. Ask for poster-ready summaries, not generic abstracts.
3. Force every review to answer: adopt / avoid / test.
4. Keep the model honest: ask for limitations and what would break under Augrade's product constraints.
5. Compile summaries into a poster or one-page research board only after the Tier 0 set is done.

## Sources

### 1. Generalizing Floor Plans Using Graph Neural Networks (Tier 0 · Annotation / CAD graph substrate)
Source: https://resourcecenter.ieee.org/conferences/icip-2021/spsicip21vid276

Focus: CAD primitive graph extraction; node classification for doors; compare graph-vs-raster; what labels/data contract did they use?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Generalizing Floor Plans Using Graph Neural Networks (https://resourcecenter.ieee.org/conferences/icip-2021/spsicip21vid276). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: CAD primitive graph extraction; node classification for doors; compare graph-vs-raster; what labels/data contract did they use?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Annotation / CAD graph substrate.
```

### 2. Multi-Classification Of CAD Entities (Tier 0 · Annotation / CAD graph substrate)
Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4957759

Focus: Entity-as-node GNN for CAD floor plans; compare GAT/GATv2/PNA/UniMP-style choices; identify what they keep as vector features.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Multi-Classification Of CAD Entities (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4957759). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Entity-as-node GNN for CAD floor plans; compare GAT/GATv2/PNA/UniMP-style choices; identify what they keep as vector features.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Annotation / CAD graph substrate.
```

### 3. FloorPlanCAD (Tier 0 · Annotation / CAD graph substrate)
Source: https://researchportal.hkust.edu.hk/en/publications/floorplancad-a-large-scale-cad-drawing-dataset-for-panoptic-symbo/

Focus: Line-level annotations and class taxonomy; what is reusable for annotation-to-object correspondence and drawing-level splits?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: FloorPlanCAD (https://researchportal.hkust.edu.hk/en/publications/floorplancad-a-large-scale-cad-drawing-dataset-for-panoptic-symbo/). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Line-level annotations and class taxonomy; what is reusable for annotation-to-object correspondence and drawing-level splits?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Annotation / CAD graph substrate.
```

### 4. VectorGraphNET (Tier 0 · Annotation / CAD graph substrate)
Source: https://arxiv.org/abs/2410.01336

Focus: Vector-native graph attention for technical drawing segmentation; cost/accuracy vs raster baselines; what supports our vector-first claim?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: VectorGraphNET (https://arxiv.org/abs/2410.01336). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Vector-native graph attention for technical drawing segmentation; cost/accuracy vs raster baselines; what supports our vector-first claim?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Annotation / CAD graph substrate.
```

### 5. SymPoint (Tier 1 · Annotation / CAD graph substrate)
Source: https://openreview.net/forum?id=aOnUe8ah7j

Focus: Vector primitives as point cloud; spotting head; what does point-style geometry preserve/lose relative to graph supervectors?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: SymPoint (https://openreview.net/forum?id=aOnUe8ah7j). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Vector primitives as point cloud; spotting head; what does point-style geometry preserve/lose relative to graph supervectors?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Annotation / CAD graph substrate.
```

### 6. SymPoint-V2 (Tier 1 · Annotation / CAD graph substrate)
Source: https://arxiv.org/abs/2407.01928

Focus: Layer-feature enhancement and position-guided training; how does authored-layer signal help, and how should we ablate it against layer-blind first pass?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: SymPoint-V2 (https://arxiv.org/abs/2407.01928). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Layer-feature enhancement and position-guided training; how does authored-layer signal help, and how should we ablate it against layer-blind first pass?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Annotation / CAD graph substrate.
```

### 7. CADSpotting (Tier 1 · Scale / windowing)
Source: https://arxiv.org/abs/2412.07377

Focus: Large-scale CAD drawings; dense sampling and sliding-window aggregation; what is the scale failure mode of naive primitive graphs?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: CADSpotting (https://arxiv.org/abs/2412.07377). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Large-scale CAD drawings; dense sampling and sliding-window aggregation; what is the scale failure mode of naive primitive graphs?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Scale / windowing.
```

### 8. Raster-To-Graph (Tier 2 · Raster fallback)
Source: https://onlinelibrary.wiley.com/doi/10.1111/cgf.15007

Focus: Autoregressive graph prediction from raster floorplans; what is useful when clean DXF/DWG is unavailable?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Raster-To-Graph (https://onlinelibrary.wiley.com/doi/10.1111/cgf.15007). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Autoregressive graph prediction from raster floorplans; what is useful when clean DXF/DWG is unavailable?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: Raster fallback.
```

### 9. VectorFloorSeg (Tier 0 · Vector detail)
Source: https://openaccess.thecvf.com/content/CVPR2023/html/Yang_VectorFloorSeg_Two-Stream_Graph_Attention_Network_for_Vectorized_Roughcast_Floorplan_Segmentation_CVPR_2023_paper.html

Focus: Line/region dual stream and graph attention; extract lessons for explicit face/region nodes and room boundaries.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: VectorFloorSeg (https://openaccess.thecvf.com/content/CVPR2023/html/Yang_VectorFloorSeg_Two-Stream_Graph_Attention_Network_for_Vectorized_Roughcast_Floorplan_Segmentation_CVPR_2023_paper.html). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Line/region dual stream and graph attention; extract lessons for explicit face/region nodes and room boundaries.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Vector detail.
```

### 10. Indoor Elements Classification Via Floor Plan Graphs (Tier 1 · Vector detail)
Source: https://www.mdpi.com/2220-9964/10/2/97

Focus: Region adjacency graph; wall/door/symbol/room classification; what shape-preserving features matter?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Indoor Elements Classification Via Floor Plan Graphs (https://www.mdpi.com/2220-9964/10/2/97). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Region adjacency graph; wall/door/symbol/room classification; what shape-preserving features matter?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Vector detail.
```

### 11. Graph Neural Networks For 2D Architectural Detail Drawings (Tier 0 · Predictive editing)
Source: https://www.sciencedirect.com/science/article/abs/pii/S0926580524006721

Focus: Drawing graph standardization, classification, error detection; evaluate relevance to review/validator residual surfaces.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Graph Neural Networks For 2D Architectural Detail Drawings (https://www.sciencedirect.com/science/article/abs/pii/S0926580524006721). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Drawing graph standardization, classification, error detection; evaluate relevance to review/validator residual surfaces.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Predictive editing.
```

### 12. Semantic Floorplan Segmentation Using Self-Constructing Graph Networks (Tier 1 · Hybrid floorplan reasoning)
Source: https://www.sciencedirect.com/science/article/pii/S0926580524003856

Focus: CNN+GCN long-range dependencies; when is induced graph structure useful vs vector graph state?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Semantic Floorplan Segmentation Using Self-Constructing Graph Networks (https://www.sciencedirect.com/science/article/pii/S0926580524003856). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: CNN+GCN long-range dependencies; when is induced graph structure useful vs vector graph state?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Hybrid floorplan reasoning.
```

### 13. Predicting Building Layout Structure And Features Via Planar Duality (Tier 0 · Predictive editing)
Source: https://www.sciencedirect.com/science/article/abs/pii/S0926580525007216

Focus: Vertex-edge-face representation; face adjacency message passing; what supports explicit face nodes for edit reasoning?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Predicting Building Layout Structure And Features Via Planar Duality (https://www.sciencedirect.com/science/article/abs/pii/S0926580525007216). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Vertex-edge-face representation; face adjacency message passing; what supports explicit face nodes for edit reasoning?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Predictive editing.
```

### 14. Clash Context Representation And Change Component Prediction (Tier 0 · Edit cascades)
Source: https://www.sciencedirect.com/science/article/abs/pii/S1474034623000241

Focus: GCN for BIM clash context and change-component prediction; extract analogy for validator-driven edit cascades.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Clash Context Representation And Change Component Prediction (https://www.sciencedirect.com/science/article/abs/pii/S1474034623000241). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: GCN for BIM clash context and change-component prediction; extract analogy for validator-driven edit cascades.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Edit cascades.
```

### 15. Incorporating Context Into BIM-Derived Data With GNNs (Tier 1 · BIM enrichment)
Source: https://www.mdpi.com/2075-5309/14/2/527

Focus: Context-aware BIM classification; quantify what neighborhood reasoning adds over local features.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Incorporating Context Into BIM-Derived Data With GNNs (https://www.mdpi.com/2075-5309/14/2/527). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Context-aware BIM classification; quantify what neighborhood reasoning adds over local features.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: BIM enrichment.
```

### 16. IFC BIM Model Enrichment With Space Function Information Using GNNs (Tier 1 · BIM enrichment)
Source: https://www.mdpi.com/1996-1073/15/8/2937

Focus: Room/space function enrichment; relevance to room/zone/fixture semantics after graph recovery.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: IFC BIM Model Enrichment With Space Function Information Using GNNs (https://www.mdpi.com/1996-1073/15/8/2937). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Room/space function enrichment; relevance to room/zone/fixture semantics after graph recovery.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: BIM enrichment.
```

### 17. Optimized GNNs For Spatial Recognition In BIM Semantic Enrichment (Tier 2 · BIM enrichment)
Source: https://www.sciencedirect.com/science/article/abs/pii/S0952197625003653

Focus: Node/edge feature design and Graph-BERT-like methods; what typed edge features transfer?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Optimized GNNs For Spatial Recognition In BIM Semantic Enrichment (https://www.sciencedirect.com/science/article/abs/pii/S0952197625003653). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Node/edge feature design and Graph-BERT-like methods; what typed edge features transfer?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: BIM enrichment.
```

### 18. Automated BIM Generation For MEP Systems From CAD Data (Tier 1 · MEP inference)
Source: https://www.sciencedirect.com/science/article/abs/pii/S0926580525005825

Focus: Graph structures for MEP system generation from CAD; what is the minimum shell/fixture graph needed for system inference?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Automated BIM Generation For MEP Systems From CAD Data (https://www.sciencedirect.com/science/article/abs/pii/S0926580525005825). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Graph structures for MEP system generation from CAD; what is the minimum shell/fixture graph needed for system inference?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: MEP inference.
```

### 19. Neural Relational Inference (Tier 1 · Latent dependencies)
Source: https://proceedings.mlr.press/v80/kipf18a.html

Focus: Latent interaction graphs for dynamics; map to hidden edit dependencies and must-move-with relations.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Neural Relational Inference (https://proceedings.mlr.press/v80/kipf18a.html). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Latent interaction graphs for dynamics; map to hidden edit dependencies and must-move-with relations.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Latent dependencies.
```

### 20. Graph Edit Networks (Tier 0 · Graph edit actions)
Source: https://openreview.net/forum?id=dlEJsyHGeaL

Focus: Typed graph edit outputs; extract action grammar and loss lessons for M6 structured readout.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Graph Edit Networks (https://openreview.net/forum?id=dlEJsyHGeaL). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Typed graph edit outputs; extract action grammar and loss lessons for M6 structured readout.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Graph edit actions.
```

### 21. Temporal Straightening For Latent Planning (Tier 2 · Planning representation)
Source: https://arxiv.org/abs/2603.12231

Focus: Latent trajectory conditioning for planning; use as future objective for edit/residual paths, not MVP.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Temporal Straightening For Latent Planning (https://arxiv.org/abs/2603.12231). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Latent trajectory conditioning for planning; use as future objective for edit/residual paths, not MVP.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: Planning representation.
```

### 22. Geometric Deep Learning (Tier 0 · Representation boundary)
Source: https://arxiv.org/abs/2104.13478

Focus: Use as vocabulary for locality, symmetry, hierarchy, graphs; clarify what it does and does not justify for authored CAD.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Geometric Deep Learning (https://arxiv.org/abs/2104.13478). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Use as vocabulary for locality, symmetry, hierarchy, graphs; clarify what it does and does not justify for authored CAD.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Representation boundary.
```

### 23. A Mechanistic Analysis Of Sim-And-Real Co-Training (Tier 1 · Representation alignment)
Source: https://arxiv.org/abs/2604.13645

Focus: Cross-domain alignment while preserving domain identity; map to pool-for-geometry/tag-for-provenance and rewrite tests.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: A Mechanistic Analysis Of Sim-And-Real Co-Training (https://arxiv.org/abs/2604.13645). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Cross-domain alignment while preserving domain identity; map to pool-for-geometry/tag-for-provenance and rewrite tests.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Representation alignment.
```

### 24. Geometric Algebra Transformer (Tier 1 · Equivariance)
Source: https://arxiv.org/abs/2305.18415

Focus: Representation choices for geometric objects; what would multivectors buy for frames, surfaces, clearances, support relations?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Geometric Algebra Transformer (https://arxiv.org/abs/2305.18415). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Representation choices for geometric objects; what would multivectors buy for frames, surfaces, clearances, support relations?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Equivariance.
```

### 25. Choosing A Geometric Algebra For Equivariant Transformers (Tier 1 · Equivariance)
Source: https://proceedings.mlr.press/v238/haan24a.html

Focus: Carrier choice changes expressivity and compute; translate to primitive/supervector/face/edit-token design.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Choosing A Geometric Algebra For Equivariant Transformers (https://proceedings.mlr.press/v238/haan24a.html). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Carrier choice changes expressivity and compute; translate to primitive/supervector/face/edit-token design.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Equivariance.
```

### 26. Any-Subgroup Equivariant Networks Via Symmetry Breaking (Tier 2 · Equivariance)
Source: https://openreview.net/forum?id=jz3d7nvtGz

Focus: Family-conditioned invariance; compare shared trunk vs family heads vs separate models for rewrite collapse.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Any-Subgroup Equivariant Networks Via Symmetry Breaking (https://openreview.net/forum?id=jz3d7nvtGz). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Family-conditioned invariance; compare shared trunk vs family heads vs separate models for rewrite collapse.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: Equivariance.
```

### 27. Scalable Co-Design Via Linear Design Problems (Tier 1 · System interfaces)
Source: https://arxiv.org/abs/2603.29083

Focus: Compositional design interfaces; extract language for stable interfaces, coupling, and validator boundaries.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Scalable Co-Design Via Linear Design Problems (https://arxiv.org/abs/2603.29083). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Compositional design interfaces; extract language for stable interfaces, coupling, and validator boundaries.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: System interfaces.
```

### 28. A Mathematical Theory Of Co-Design (Tier 2 · System interfaces)
Source: https://arxiv.org/abs/1512.08055

Focus: Foundational co-design; background only. Pull vocabulary for feasibility/resource constraints.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: A Mathematical Theory Of Co-Design (https://arxiv.org/abs/1512.08055). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Foundational co-design; background only. Pull vocabulary for feasibility/resource constraints.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: System interfaces.
```

### 29. Algorithmic Learning In A Random World (Tier 0 · Calibration)
Source: https://www.alrw.net/

Focus: Conformal prediction as auto-merge/reject/review band; produce practical recipe for small-label CAD relations.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Algorithmic Learning In A Random World (https://www.alrw.net/). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Conformal prediction as auto-merge/reject/review band; produce practical recipe for small-label CAD relations.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Calibration.
```

### 30. Dense Associative Memory With Exponential Capacity (Tier 1 · Memory)
Source: https://arxiv.org/abs/2601.00984

Focus: Prototype memory for low-label merge/review cases; decide where memory helps vs sparse scores.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Dense Associative Memory With Exponential Capacity (https://arxiv.org/abs/2601.00984). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Prototype memory for low-label merge/review cases; decide where memory helps vs sparse scores.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Memory.
```

### 31. Goodfire EVEE (Tier 1 · Representation geometry)
Source: https://www.goodfire.ai/research/evee-explaining-genetic-variants

Focus: Feature geometry and probe/readout lessons; translate from biology to validator residuals and CAD motif geometry.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Goodfire EVEE (https://www.goodfire.ai/research/evee-explaining-genetic-variants). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Feature geometry and probe/readout lessons; translate from biology to validator residuals and CAD motif geometry.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Representation geometry.
```

### 32. Entropy-Preserving Reinforcement Learning (Tier 2 · RL/search)
Source: https://arxiv.org/abs/2603.11682

Focus: Maintain solution diversity in graph-edit policies; useful after action grammar and validators exist.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Entropy-Preserving Reinforcement Learning (https://arxiv.org/abs/2603.11682). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Maintain solution diversity in graph-edit policies; useful after action grammar and validators exist.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: RL/search.
```

### 33. FOCUS (Tier 2 · Object-centric world models)
Source: https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2025.1585386/full

Focus: Object-centric latent state plus relational dynamics; map to world-model bridge and graph substrate.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: FOCUS (https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2025.1585386/full). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Object-centric latent state plus relational dynamics; map to world-model bridge and graph substrate.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: Object-centric world models.
```

### 34. Dyn-O (Tier 2 · Object-centric world models)
Source: https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/dyno_neurips2025.pdf

Focus: Object-centric dynamics; look for lessons on multiscale graph state from latent worlds.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Dyn-O (https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/dyno_neurips2025.pdf). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Object-centric dynamics; look for lessons on multiscale graph state from latent worlds.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: Object-centric world models.
```

### 35. CADDesigner (Tier 2 · CAD agents)
Source: https://arxiv.org/html/2508.01031

Focus: LLM/CAD generation interface layer; contrast with vector graph substrate and validators.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: CADDesigner (https://arxiv.org/html/2508.01031). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: LLM/CAD generation interface layer; contrast with vector graph substrate and validators.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: CAD agents.
```

### 36. CAD-LLM (Tier 2 · CAD agents)
Source: https://www.research.autodesk.com/publications/ai-lab-cad-llm/

Focus: Natural-language/parametric CAD agents; what can be borrowed for intent interface above graph state?

Prompt:

```text
Read this source for the Augrade GNN Strategy review: CAD-LLM (https://www.research.autodesk.com/publications/ai-lab-cad-llm/). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Natural-language/parametric CAD agents; what can be borrowed for intent interface above graph state?

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: CAD agents.
```

### 37. Autodesk Constraint Generation (Tier 2 · CAD agents)
Source: https://www.research.autodesk.com/app/uploads/2025/10/Aligning-Constraint-Generation-with-Design-Intent-in-Parametric-CAD.pdf

Focus: Design-intent constraints; relevance to typed action grammar and validators.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Autodesk Constraint Generation (https://www.research.autodesk.com/app/uploads/2025/10/Aligning-Constraint-Generation-with-Design-Intent-in-Parametric-CAD.pdf). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Design-intent constraints; relevance to typed action grammar and validators.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 2. Category: CAD agents.
```

### 38. Matryoshka Representation Learning (Tier 0 · Nested embeddings)
Source: https://huggingface.co/papers/2205.13147

Focus: Nested representations; translate embedding size into product knobs: cache, routing, offline discovery.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Matryoshka Representation Learning (https://huggingface.co/papers/2205.13147). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Nested representations; translate embedding size into product knobs: cache, routing, offline discovery.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Nested embeddings.
```

### 39. Prime Intellect Verifiers (Tier 0 · Verifier environments)
Source: https://docs.primeintellect.ai/verifiers/overview

Focus: Environment = task inputs + harness + reward/rubric; map to CAD verifier environment after M7 matures.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Prime Intellect Verifiers (https://docs.primeintellect.ai/verifiers/overview). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Environment = task inputs + harness + reward/rubric; map to CAD verifier environment after M7 matures.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Verifier environments.
```

### 40. Prime Intellect Lab (Tier 1 · Verifier environments)
Source: https://docs.primeintellect.ai/hosted-training/what-is-lab

Focus: Hosted environments/training/evals; decide what to outsource vs keep in-house.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Prime Intellect Lab (https://docs.primeintellect.ai/hosted-training/what-is-lab). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Hosted environments/training/evals; decide what to outsource vs keep in-house.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Verifier environments.
```

### 41. Molecular GNN Review / Nature Machine Intelligence (Tier 1 · Molecular analogy)
Source: https://www.nature.com/articles/s42256-021-00438-4

Focus: Molecules as atom/bond graphs; extract substructure/motif analogy for supervector molecules.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Molecular GNN Review / Nature Machine Intelligence (https://www.nature.com/articles/s42256-021-00438-4). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Molecules as atom/bond graphs; extract substructure/motif analogy for supervector molecules.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 1. Category: Molecular analogy.
```

### 42. Goodfire public positioning (Tier 0 · Representation geometry)
Source: https://www.goodfire.ai/

Focus: Dictionary-to-geometry framing; use to sharpen the representation geometry and compiler-loop language.

Prompt:

```text
Read this source for the Augrade GNN Strategy review: Goodfire public positioning (https://www.goodfire.ai/). Create a poster-ready summary for my review.

Context: I am building a vector-first CAD/BIM graph substrate with deterministic geometry, supervectors, validators, calibrated relation scoring, optional GNN/local message passing, prototype/matryoshka memory, and a rule-compilation loop.

Focus for this source: Dictionary-to-geometry framing; use to sharpen the representation geometry and compiler-loop language.

Output format:
1. 5-sentence executive summary.
2. What representation does the paper/source use? Be concrete about nodes/tokens, edges/relations, labels, losses, and data contract.
3. What does it prove or fail to prove for Augrade?
4. What should I adopt, avoid, or test?
5. Poster block: one diagram idea, one key table, three takeaways, and one skeptical caveat.
6. Where it fits in the paper ladder: annotation-to-object, rewrite-stable graphs, matryoshka embeddings, supervector molecules, quality loops, verifier environments, or future mech-interp.

Priority: Tier 0. Category: Representation geometry.
```
