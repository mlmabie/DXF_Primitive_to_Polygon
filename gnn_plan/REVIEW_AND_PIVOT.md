# Review and Pivot — 2026-05-09

External review of the handoff package surfaced three distinct problems
and one recommended pivot. This document captures the critique so the
later docs in this folder can be re-read against it.

## The critique

A friend (ex-Liquid AI, post-training at OpenAI) reviewed the deck and
called out three failures. They are independent and need separate fixes.

### 1. Slop — the AI-rhetoric tell

When a reader at that level asks "what did you use to make the slides,"
they have already pattern-matched LLM-generated prose. The giveaway lines
are the well-formed-but-content-free aphorisms:

- "the frame ships; the geometry compounds; the best discoveries compile
  back into the engine"
- "publish the substrate, then the invariances, then the discovered
  supervectors"
- "dictionary → geometry → compiler"

These read as conviction; they are not conviction. They could appear
unchanged in five other decks. Fix: cut every line of that shape.
Replace with a concrete claim, a number, a counterexample, or a specific
design choice.

### 2. Density and meta-commentary

Eighteen slides each carrying three to six ideas. The reader wanted one
idea per slide. Several slides — Quality loops, Persistent edge in a
world of SAI, AI + compute (accelerate then pace) — describe how the
author thinks about the work rather than what they will build and how
they will know it works. Cut every slide that does not contain either:

- a concrete proposal,
- an empirical result, or
- a specific risk and how it would be tested.

That probably halves the deck.

### 3. Breadth without conviction

The package puts on the table: matryoshka embeddings, online RL, sparse
autoencoders, calibrated ranker, JEPA / world-model bridge, scope
resolver, predictive editing, paper-trajectory ladder, and the
"publish substrate → invariances → supervectors" sequence. Each is a
real research program. Listing them reads as taste, not commitment.
The reviewer's recommendation: pick one or two and own them.

## The pivot

The one bet with empirical evidence in this repo is:

> HATCH companion layers are hidden ground truth. A graph-recovered
> polygon's IoU against the HATCH boundary on the companion layer is a
> self-supervised correctness signal that the source-entity coverage
> proxy misses by construction.

This is concrete, novel-feeling, defensible from the existing
`scripts/grid_search.py` results, and it is shown on real data. Most of
the GNN architecture choices (heterogeneous graph, GAT vs GIN,
supervector pooling, scope resolver) are downstream of having a real
training signal — and HATCH-IoU is one nobody else is talking about.

### Three moves before the next interview

1. **Headline rebuild around HATCH-IoU as the supervision story.**
   "Layer-blind classification needs a self-supervised target. I found
   one in the data. Here is the IoU map, here is how it ranks model
   variants, here is what falls out of training against it." A
   five-slide deck with a result.

2. **Demote everything else to future directions or appendix.**
   Matryoshka, SAE, online RL, world-model bridge — none of these are
   required to make the HATCH-IoU pitch land. They distract from it.

3. **Kill the meta slides outright.** Quality loops, SAI persistence,
   AI-and-compute pacing. Those go in a personal doctrine doc, not a
   research pitch.

### The question that has to be answerable in three sentences

> If you could only ship one technical claim from `gnn_plan/` in the
> next 90 days, what would it be, and what would the experiment look
> like?

If that has a three-sentence answer, the rest of the deck rewrites
itself. If it does not, that is the work.

## How this relates to the rest of the folder

The earlier "claim overlap" observation pointed at the same root cause
from a different angle. The issue is not that the same claim appears
in multiple files. It is that the underlying portfolio is too wide,
which forces every document to gesture at all of it, which produces
vague summarizing prose, which reads as slop.

When re-reading the numbered docs (`01_problem_framing.md` through
`16_epistemic_controls.md`), `SYSTEM_SPEC.md`, `TALK_TRACK.md`, and
`SENSEMAKING.md`, treat this critique as the lens. Anything that
survives is load-bearing for the HATCH-IoU pitch or for a single
high-conviction follow-up. Everything else is appendix or scratch.

`CONSOLIDATION_GUIDE.md` (migration scratch for a now-dead branch) and
`prompt.md` (redundant with `00_START_HERE.md`'s embedded prompt) were
deleted as part of the pivot.
