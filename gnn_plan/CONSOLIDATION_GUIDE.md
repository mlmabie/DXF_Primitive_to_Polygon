# Consolidation Guide

This pack consolidates the current Augrade GNN work state into repo-ready Markdown. It is designed to be dropped into the `gnn-plan-setup` branch without editing the slide deck.

## Source state being consolidated

- Latest deck: `Augrade GNN Strategy v2.pptx`, 18 slides.
- Paper companion: `Augrade Paper Trajectory Supplement v2.docx`.
- Operating doctrine: `Augrade Operating Doctrine Companion v2.docx`.
- Current repo branch: `gnn-plan-setup`.
- Discussion-thread concepts since the deck/doc pass:
  - scope resolver: objective/edit/residual -> minimal sufficient subgraph
  - precision conditioning: stable geometry makes good change cheap
  - graph as compute-scope engine for large project files
  - multiplayer drawing/state management
  - building-code split: validators for hard constraints, embedded scoring for interpretive affordances
  - non-Euclidean / world-model bridge from raw 3D reconstruction to multiscale graph state
  - paper-review workflow: source link + prompt for every source

## Recommended file placement

Copy these files into the repo as-is:

```text
gnn_plan/07_source_review_prompts.md
gnn_plan/08_scope_resolver.md
gnn_plan/09_precision_conditioning.md
gnn_plan/10_operating_doctrine_addendum.md
gnn_plan/11_paper_trajectory.md
gnn_plan/12_world_model_bridge.md
gnn_plan/CONSOLIDATION_GUIDE.md
reference/reviews/source_review_tracker.csv
reference/reviews/source_review_tracker.jsonl
```

## Suggested README update

Add this block to `gnn_plan/README.md` under **Reading Order**, after `06_example_insights.md`:

```md
7. [`07_source_review_prompts.md`](07_source_review_prompts.md) — paper/source review queue with source links and per-source prompts.
8. [`08_scope_resolver.md`](08_scope_resolver.md) — trainable scope resolver: objective/edit/residual -> minimal sufficient subgraph.
9. [`09_precision_conditioning.md`](09_precision_conditioning.md) — stable geometry makes good change cheap.
10. [`10_operating_doctrine_addendum.md`](10_operating_doctrine_addendum.md) — pessimist route, hybrid GNN/FM/validator/memory doctrine, and quality loops.
11. [`11_paper_trajectory.md`](11_paper_trajectory.md) — publishable-paper ladder and sequencing gates.
12. [`12_world_model_bridge.md`](12_world_model_bridge.md) — bridge from raw 3D / VLA / JEPA / world-model encoders into a multiscale graph substrate.
```

## Suggested `04_research_map.md` update

Keep `04_research_map.md` as the citation shelf. Add a pointer near the top:

```md
For the review workflow, source links, and per-source poster prompts, see [`07_source_review_prompts.md`](07_source_review_prompts.md) and `reference/reviews/source_review_tracker.csv`.
```

## Suggested `SYSTEM_SPEC.md` update

Add a new module after M3 or before M4:

```md
### M3.5 Scope Resolver

`augrade.scope.resolve(query, graph_manifest, policy)`

Input: objective, edit proposal, validator residual, annotation, or user selection.
Output: minimal sufficient subgraph, validators to run, dirty cache keys, retrieval queries, risk band, and scope certificate.

A scoped subgraph is sufficient when the downstream scorer, validator, or edit policy returns the same decision/residual/proposal as the full graph within risk tolerance. It is minimal enough when it preserves that result while reducing compute, context, and review burden.
```

## Suggested branch hygiene

- Keep the deck in `/docs/` or `/gnn_plan/decks/` only if you want the repo to own presentation assets.
- Keep these Markdown files under `gnn_plan/` because they are plan/spec material.
- Keep source-review CSV/JSONL under `reference/reviews/` because they are literature-review workflow assets.
- Do not merge source summaries into `04_research_map.md` yet. First run the source-review prompts in fresh threads and compile poster outputs.

## Immediate next action

Run the Tier 0 and Tier 1 source prompts first. The deck is already meeting-ready; the research map needs refreshed source comprehension.
