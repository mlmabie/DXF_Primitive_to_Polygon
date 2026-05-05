# Q2: Frameworks, Scale, And Systems

Question:

> Which GNN frameworks/tools have you used, and at what scale?

This is not only a framework question. It is a taste question: can you choose
the right implementation path for the graph, data, hardware, and product loop?

## Source Answer

The current canonical answer says:

- main hands-on framework: PyTorch Geometric
- custom `MessagePassing`, heterogeneous schemas, typed edges, attention over
  relations, training/inference pipelines
- temporal graph work mostly in core PyG rather than PyTorch Geometric Temporal
  for tighter control over graph reconstruction and temporal encoding
- graph sizes: hundreds to low-thousands of nodes per snapshot,
  multi-relational edges, 32-128 dimensional node features
- real scaling challenge: continuous reconstruction from large multi-year event
  streams under fast inference constraints

## Raw Thesis To Preserve

The strong answer is not:

> I know PyG.

It is:

> I know when PyG helps, when custom tensor paths may be faster, and why graph
> construction, batching, temporal reconstruction, calibration, and deployment
> constraints often dominate the choice of GNN layer.

## Substantive Answer Shape

A better Q2 answer should cover:

1. **Tool familiarity:** PyTorch, PyG, custom message passing, profiling,
   deployment-aware training loops.
2. **Scale realism:** modest per-graph size can still be a serious systems
   problem when graphs are rebuilt continuously or used interactively.
3. **Implementation judgment:** static vs dynamic graph construction, sparse
   message passing vs flattened/custom tensors, CPU/GPU target, graph export
   cost, and baseline comparisons.

## Strong Version

I would answer Q2 like this:

> My most hands-on GNN tooling is PyTorch Geometric, especially custom
> `MessagePassing`, heterogeneous schemas, typed edges, relation-aware
> attention, and production-oriented training/inference loops. For temporal
> graph work I mostly stayed closer to core PyG and PyTorch instead of leaning
> too hard on PyG Temporal, because I needed control over reconstruction,
> temporal windows, batching, and feature flow. In T-UEBA the snapshots were
> typically hundreds to low-thousands of nodes with multi-relational edges and
> 32-128 dimensional node features. The hard scaling problem was not one giant
> graph. It was repeatedly reconstructing useful graphs from messy event
> streams and keeping inference cheap enough to deploy.
>
> For Augrade I would make the same distinction. I would start with PyG because
> it is fast for iteration, but I would not worship the framework. If the graph
> structure becomes static or regular enough, a flattened/custom batched tensor
> path may be faster and simpler. If the graph changes after every edit, dynamic
> construction and feature generation may dominate the runtime. I would profile
> graph construction, feature generation, batching, and inference separately
> before choosing the final stack.

## Framework Decision Matrix

| Situation | Likely path |
|---|---|
| research iteration over heterogeneous graph schemas | PyG |
| custom typed edge semantics and quick ablations | PyG custom `MessagePassing` |
| very regular static graphs | compiled/static batching or custom tensors |
| tiny interactive graphs with CPU latency needs | simple PyTorch / NumPy feature scorer first |
| many dynamic edit updates | incremental graph update path before model tuning |
| raster context needed | convolutional chip as auxiliary feature, not source of truth |
| few labels | sparse baselines, calibrated uncertainty, prototype memory |

## Compute Questions That Matter

Ask these before algorithm commitment:

- Is training GPU-rich or GPU-constrained?
- Is inference interactive, batch, or both?
- Are graphs static per drawing or rebuilt after edits?
- Are graph sizes regular enough for static batching?
- Is the bottleneck graph construction, message passing, or validator calls?
- Do they need CPU fallback?
- Is the goal classification, relation scoring, edit-impact prediction, or all
  three?

## Substantive Research Direction

For the setup branch, Q2 should turn into experiments:

- PyG heterogeneous graph export
- flattened edge-feature table baseline
- convolutional/raster-chip baseline
- static graph vs dynamic update benchmark
- graph-construction profiling
- model forward-pass profiling
- calibration and review-band measurement

## Voice Check

The answer should sound compute-realistic, not framework-loyal.

The live thesis:

> I optimize the representation and data flow before the kernel. Frameworks are
> tools; graph construction and deployment constraints decide the architecture.
