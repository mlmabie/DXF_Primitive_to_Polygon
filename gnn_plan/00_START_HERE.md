# Start Here: Augrade GNN Workbench

This folder is the front door for the Augrade GNN planning materials and the
workbench for the next technical phase. It is not a finished implementation
claim and it is not a claim that one exact GNN architecture is already correct.

The purpose is to turn a broad, high-leverage prompt into an executable and
falsifiable plan: what to build first, what to baseline, what to defer, which
references to review, and where graph learning is actually load-bearing.

## Original project prompt

Lightly reformatted from the project prompt:

> Focus on two things:
>
> **1. DWG/DXF vector classification**
>
> - have the DWG and DXF
> - assume all primitives on one layer
> - unsorted soup of vectors
> - one line of thought to explore: classification using GNNs
> - preserve the level of detail and accuracy
> - rasterization and detail: look into this method
> - any sort of graph approach that helps classify the supervectors into
>   representative elements
>
> **2. Predictive modeling or editing**
>
> Two flavors:
>
> - architecture shell: trying to guess how the plumbing fits
> - if I do X action, how does that affect all the other things — cascade,
>   conflicts, and dependencies
>
> Thursday/Friday: let's meet.
>
> There is no consistency in representation; whatever they build breaks in
> certain situations.
>
> Three annotated files included for reference.

## Reader contract

Because of the wide and deep scope of the plan, these materials intentionally
separate commitments, hypotheses, candidate mechanisms, counterfactuals, and
reference prompts. The branch should be read as a map to be owned through
pointed source reads, counterfactuals, small reproductions, and validator-backed
experiments.

Read the branch with this status model:

1. **Commitments.**
   Vector-first representation, exact geometry/provenance, stable ids,
   deterministic validators, sparse baselines before GNNs, drawing-level splits,
   calibrated review bands, and counterfactual experiments.

2. **Hypotheses.**
   A heterogeneous primitive/supervector/annotation/face graph should beat
   simpler baselines on at least some relation tasks where local neighborhood
   context matters.

3. **Candidate mechanisms.**
   GraphSAGE, GATv2, PNA, prototype memory, matryoshka embeddings,
   rewrite-invariance losses, verifier environments, and world-model bridges
   are tools to test, not doctrine.

4. **Counterfactuals.**
   Homogeneous graphs, primitive-only classifiers, raster-first perception,
   graph transformers, pure rules, embedding-first retrieval, and
   foundation-model harnesses remain live alternatives until evaluation decides.

5. **Reference prompts.**
   The research-map sources are not authority by themselves. Each source should
   either sharpen a data contract, identify a baseline, expose a counterfactual,
   define an evaluation metric, or suggest a later-stage mechanism.

The strongest claim is not that one exact GNN architecture is right. The
strongest claim is that Augrade needs a trustworthy graph substrate: vector
fidelity, object identity, typed relations, validators, workflow memory, and a
loop that compiles learned residuals back into deterministic mechanisms.

## KISS first slice

The simplest credible path is:

1. convert / parse one drawing with metadata preserved;
2. emit primitive, supervector, face, edge, annotation, and manifest tables;
3. render overlays for human inspection;
4. generate deterministic supervector candidates;
5. train sparse node/relation baselines;
6. calibrate auto-accept / reject / review bands;
7. inspect high-confidence correct, high-confidence wrong, and uncertain cases;
8. run rewrite perturbations;
9. add a GNN only where sparse/local features fail for a reason message passing
   can plausibly fix;
10. compile repeated stable discoveries back into deterministic rules or
    supervectors.

Everything beyond this is optional until this slice exposes a real residual.

## What the GNN should and should not own

The GNN should own only the residual tasks where typed neighborhood context
beats deterministic geometry and sparse pair features:

- primitive and supervector classification when local composition is ambiguous;
- annotation-to-object correspondence, such as tags, dimensions, leaders, and
  room names;
- relation recovery where geometry alone is underdetermined;
- context propagation over scoped subgraphs;
- uncertainty surfacing and failure retrieval.

It should not own exact geometry validity, closure/winding truth,
code/compliance truth, arbitrary whole-scene generation, global drawing context
when a broader context model or retrieval harness is the better mechanism, or
any auto-apply decision that validators cannot bound.

## Quality bar for graph learning

The graph-learning target is valuable when it creates trusted work that simpler
local features, deterministic rules, retrieval, or broad context do not already
provide. In this plan, a useful CAD-native graph model should:

- preserve exact vector evidence and provenance;
- improve at least one context-heavy primitive, supervector, relation, or
  annotation-to-object task over sparse/local baselines;
- stay calibrated enough to support auto-accept / reject / review bands;
- remain stable under safe authored rewrites;
- respect validator boundaries; and
- improve review yield, scope efficiency, or rule-discovery value.

## What would make the default architecture wrong

The heterogeneous graph is a default, not a doctrine. It loses if a simpler
counterfactual produces better trusted work.

Trusted work means fewer false merges, better calibrated review bands, lower
scope/compute cost, stronger validator agreement, better annotation-to-object
recovery, better drawing-level generalization, and more discoveries compiled
into deterministic rules.

The main counterfactuals live in [`15_counterfactual_architectures.md`](15_counterfactual_architectures.md).

## How to use this folder

If you have **5 minutes**:

1. [`workbench/TALK_TRACK.md`](workbench/TALK_TRACK.md)
2. [`13_primary_answer.md`](13_primary_answer.md) — consolidated post-call
   answer
3. [`SYSTEM_SPEC.md`](SYSTEM_SPEC.md) — goal, module stack, first slice
4. [`15_counterfactual_architectures.md`](15_counterfactual_architectures.md) —
   decision rule

If you have **20 minutes**, add:

5. [`17_dxf_tokenization.md`](17_dxf_tokenization.md)
6. [`workbench/SENSEMAKING.md`](workbench/SENSEMAKING.md)
7. [`08_scope_resolver.md`](08_scope_resolver.md)
8. [`10_operating_doctrine_addendum.md`](10_operating_doctrine_addendum.md)

If you want the **research lane**, add:

9. [`04_research_map.md`](04_research_map.md)
10. [`workbench/07_source_review_prompts.md`](workbench/07_source_review_prompts.md)
11. [`11_paper_trajectory.md`](11_paper_trajectory.md)
12. [`16_epistemic_controls.md`](16_epistemic_controls.md)

## Reader Context Language

If asked how much is implemented versus planned:

> The take-home implements the deterministic geometry layer. This branch is a
> research and system plan for the next phase. I am not claiming every paper
> lead or architecture choice is already validated. I am claiming the boundary
> is right: vector-first graph state, stable ids, provenance, sparse baselines,
> calibration, validators, and counterfactual tests before GNN complexity. The
> goal of this branch is to make the next experiments hard to fool.

If asked why GNNs:

> I would not oversell GNNs as the answer to all drawing context. Foundation
> models are moving fast on broad context, and most successful GNN systems are
> hybrid. The graph substrate matters because drawings need persistent object
> identity, typed relations, local cache invalidation, validator residuals, and
> workflow memory. The GNN is useful only where local relational propagation
> beats sparse features.

If asked what survives frontier-model progress:

> Borrow model capacity; own problem shape. The persistent edge is the
> environment, verifier, memory, trusted edit loop, and rule compiler.
