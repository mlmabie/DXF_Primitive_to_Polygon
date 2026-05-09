# Epistemic Controls For The Research Workbench

Date: 2026-05-08

## Purpose

Because of the wide and deep scope of the plan, this branch separates repo
updates, slide edits, companion docs, source leads, implementation sketches, and
counterfactuals into a falsifiable workbench. The breadth is intentional: it
creates a map of the problem, the candidate mechanisms, and the failure modes.

Ownership comes from pointed source reads,
counterfactual baselines, small reproductions, and claim-status tracking.

The goal of this file is to prevent four failure modes:

1. **Reference spoofing** — a source exists but does not support the transferred
   claim.
2. **Method-transfer spoofing** — a method works in another domain but not under
   CAD/AEC constraints.
3. **Approach drift** — a candidate mechanism quietly becomes doctrine because
   it sounds elegant.
4. **Cognitive-security drift** — the plan's confidence exceeds the actual
   evidence after repeated summarization, reuse, and recombination.

## Status categories

Every load-bearing idea should be placed in one of these lanes.

| Lane | Meaning | Examples |
|---|---|---|
| Commitment | We can defend this from first principles or direct repo evidence. | vector-first state, stable ids, validators outside learned stack, sparse baselines before GNNs |
| Hypothesis | Plausible and central, but must be tested. | hetero primitive/supervector/annotation/face graph beats simpler baselines on some relation tasks |
| Candidate mechanism | Useful tool to try if a residual calls for it. | GraphSAGE, GATv2, PNA, matryoshka embeddings, Hopfield memory, rewrite loss |
| Reference prompt | Source lead to review; not yet load-bearing. | paper/source entries in `07_source_review_prompts.md` |
| Deferred | Interesting but premature until substrate is stable. | large graph transformer, hosted RL verifier environments, mech-interp on large pretrained CAD GNN |

## Claim ledger

Use `reference/reviews/claim_ledger_template.csv` for every claim that would
change design decisions.

Minimum fields:

- `claim_id`
- `claim`
- `status_lane`
- `source_or_doc`
- `why_it_matters`
- `source_check_status`
- `pointed_read_status`
- `counterfactual_or_baseline`
- `minimal_reproduction`
- `decision_if_false`
- `next_action`

Rule:

> A claim should not become a commitment until it has either direct local
> evidence, a pointed source read, or a small reproduction / counterfactual test.

## Source-review gate

For each source in [`07_source_review_prompts.md`](07_source_review_prompts.md),
the reviewer should answer:

1. What representation does the paper actually use?
2. What are the nodes, edges, labels, losses, splits, and metrics?
3. What is the strongest claim the paper truly supports?
4. What claim does it **not** support, despite sounding relevant?
5. What should Augrade adopt, avoid, or test?
6. What counterfactual or baseline should be run because of this source?
7. What would be required to reproduce the core idea on a small CAD slice?

If a source cannot answer at least one of these, it is not load-bearing for the
plan.

## Counterfactual gate

Every proposed architecture mechanism needs at least one counterfactual.

Current required counterfactuals:

- heterogeneous graph vs homogeneous primitive graph
- primitive-only classifier vs primitive + supervector + relation recovery
- vector-first vs raster/rendered-first
- sparse baseline vs small GNN
- small GNN vs scoped graph transformer when enough data exists
- layer-blind vs layer/color-aware ablation
- full graph vs scope-resolved subgraph
- no memory vs prototype / matryoshka retrieval
- pure rules vs learned residuals
- foundation-model harness vs graph-native state

Decision rule:

> A counterfactual wins if it produces better trusted work, not if it is
> theoretically cleaner. Trusted work means fewer false merges, better
> calibrated review bands, lower scope/compute cost, stronger validator
> agreement, and more discoveries compiled into deterministic rules.

## Minimal reproduction gate

Before a mechanism becomes part of the default path, ask whether it can be
reproduced on a minimal local slice.

| Mechanism | Minimal reproduction |
|---|---|
| rewrite-invariance loss | generate split/merge and hatch-outline variants for one drawing slice; measure score drift |
| annotation-to-object alignment | align 20 tags/leaders/dimensions to candidate supervectors; compare sparse vs GNN |
| scope resolver | run full vs scoped validator on one edit/residual class; measure decision fidelity and scope size |
| matryoshka embeddings | train nested embeddings for retrieval on a small failure bank; measure latency/precision tradeoff |
| prototype memory | add 5 positive/negative exemplars and measure review-band movement on similar cases |
| verifier environment | define one typed edit action and one validator reward; run a small search baseline before RL |

## Approach-revision gate

When a source read, baseline, or reproduction contradicts the plan, revise the
architecture instead of patching the narrative.

Common revision patterns:

- sparse features beat GNN -> ship sparse scorer and keep GNN for later residuals;
- labels are weak -> invest in annotation semantics and residual reports first;
- rewrite variance is high -> fix quotient / family conditioning, not model size;
- conversion loses metadata -> pause ML and harden extraction;
- graph construction dominates runtime -> prioritize scope resolver and batching;
- foundation model handles global context better -> use it for broad reasoning,
  not native geometry or validators;
- pure rules cover a motif reliably -> compile it into the engine and remove it
  from the learned residual burden.

## Cognitive-drift review

Run this check before the branch is presented as an implementation plan:

1. Which ideas are still just attractive vocabulary?
2. Which references have not been pointed-read yet?
3. Which claims would break if sparse baselines win?
4. Which claims would break if conversion is lossy?
5. Which model components are being proposed before a residual demands them?
6. Which terms have drifted from technical meaning into vibe words?
7. Which examples have direct evidence from the repo or uploaded files?
8. Which decisions are irreversible product semantics and should be paced?

Terms that need extra care:

- fixed point
- Deep Manifold
- equivariance
- world model
- matryoshka embeddings
- mechanistic interpretation
- verifier environment
- GNN consistency
- representation geometry

None of these terms should carry a decision by themselves.

## KISS algorithmic spine

This is the simplest path to defend:

```text
1. Parse / convert vector evidence.
2. Preserve exact geometry, handles, layers, colors, text, blocks, layouts.
3. Emit primitive table with stable ids.
4. Build deterministic topology: endpoints, intersections, containment, closure.
5. Generate candidate supervectors: chains, loops, hatches, wall faces, tags, symbols.
6. Build typed edges with explicit pair features.
7. Train sparse baselines on primitives, supervectors, and relations.
8. Calibrate auto-accept / reject / review bands.
9. Use scope resolver to shrink context for each query/edit/residual.
10. Add GNN only where relation propagation beats sparse features.
11. Partition evidence into gold/silver/amber/red.
12. Compile stable discoveries back into deterministic rules.
```

Anything more complex should point to the residual it solves.

## Reader-facing language

Use this in README / call setup:

> This branch is a strategy workbench. It separates what I am committed to,
> what I suspect, what I have evidence for, and what must be falsified before
> implementation hardens.

Use this for reader context:

> Because of the wide and deep scope of the plan, I am treating this branch as
> a strategy workbench rather than a finished architecture claim. The repo
> separates commitments, hypotheses, candidate mechanisms, and reference
> prompts, then uses pointed reads, sparse baselines, counterfactuals, small
> reproductions, and validator-backed experiments to decide what survives.

Use this for model minutia:

> I would not defend GraphSAGE versus GATv2 versus PNA as settled. I would
> defend the experiment: run local/sparse baselines, then small hetero GNNs,
> then ablate layer/color, supervectors, annotation nodes, rewrite invariance,
> memory, and scope-resolved subgraphs. The architecture wins only if it
> improves a context-heavy slice without hurting calibration or compute.

## Operating doctrine

> Because of the wide and deep scope of the plan, the materials are a map to be
> owned through pointed reads, counterfactuals, reproductions, and
> validator-backed experiments.
