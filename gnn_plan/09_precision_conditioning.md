# Precision Conditioning

## Thesis

> Stable geometry makes good change cheap.

The goal is not merely to learn a good graph embedding. The goal is to learn a representation where small, trusted conditioning signals can precisely move behavior toward the right local convention, validator regime, customer preference, or edit objective.

## Definition

```text
stable representation geometry
+ small expert / customer / validator signal
-> precise behavior shift
without global retraining
without corrupting geometry
without forgetting other regimes
```

Call this **precision conditioning** or **boundary-conditioned adaptation**.

## Why it matters

Bad representation:

```text
small new convention -> lots of labels -> retrain -> regressions -> brittle behavior -> operator distrust
```

Good representation:

```text
small new convention -> a few precise examples / validator residuals -> local conditioning -> behavior moves correctly -> trust increases
```

A representation is strategically valuable when it makes the right update low-dimensional.

## Examples

The system should adapt from small signals like:

- this firm treats this hatch/outline pattern as wall mass
- this jurisdiction's clearance residual matters more
- this drafter's red tags are schedule labels, not review markup
- this customer rejects this class of auto-merge
- this project has a different shaft / wall / opening convention
- this objective prioritizes clearance over minimal geometry change

## What “good change” means

A good change improves validator-aligned or customer-aligned outcomes while preserving stable geometry, calibrated uncertainty, and prior competence.

Properties:

1. **Local** — affects the intended object/relation/convention slice.
2. **Precise** — moves the right boundary, not everything nearby.
3. **Verifier-aligned** — improves residuals or review acceptance.
4. **Auditable** — traces to examples, rules, memory, or adapter state.
5. **Data-efficient** — needs a few high-quality signals, not a full corpus.

## Adaptation surfaces

### Prototype memory

```text
new example -> prototype bank -> relation scorer shifts locally -> similar cases retrieved/ranked differently
```

Best for customer conventions and recurring weird cases.

### Matryoshka graph embeddings

Nested embeddings let conditioning operate at the right compute/resolution level:

```text
32d  -> cache / duplicate lookup
256d -> verifier routing / review triage
512d -> offline motif discovery / rule mining
```

### Low-rank adapters / heads

```text
base graph encoder = stable geometry
adapter/head = project, firm, jurisdiction, task, or objective conditioning
```

The base remains stable while local policy changes.

### Validator-conditioned scoring

```text
graph state + validator residual vector -> scorer / edit policy -> proposal that reduces active residual
```

This turns “good change” into a measurable target.

### Expert teaching models

The expert teaches a local boundary:

- these are the same object
- these are distinct despite overlap
- this text labels this opening
- this correction pattern means reroute
- this class should never auto-merge

The system converts that into prototype, rule candidate, adapter update, review-band shift, or validator threshold note.

### Rule compilation

The best adaptation stops needing the model:

```text
conditioned behavior succeeds repeatedly -> motif/rule discovered -> deterministic engine patch -> residual disappears
```

## Good latent geometry test

Signs the representation is good:

- one or two examples retrieve the right neighborhood
- a small adapter moves the intended boundary
- validator residual directions are smooth
- rewrite-equivalent cases stay close
- semantically distinct but geometrically near cases separate
- customer conventions form compact basins
- edit acceptance is rankable with a simple head
- discovered motifs compile into deterministic rules

Bad signs:

- every convention needs many labels
- prototype memory retrieves visually similar but semantically wrong cases
- adaptation improves one relation and breaks another
- layer/color/source metadata dominates geometry
- validator residuals are not recoverable from embedding space
- the GNN only works when retrained end-to-end

## Research concept

**Data-Efficient Boundary Conditioning for Vector CAD Graphs**

Core claim:

> If a graph representation learns the right latent geometry, small conditioning sets can precisely adapt behavior to new drafting conventions, validator regimes, and customer preferences.

Experiment:

- train base encoder on multiple drawings/projects
- hold out a firm, drafter, jurisdiction, or convention
- provide k examples: 1, 3, 5, 10, 25
- measure adaptation quality

Compare:

- no conditioning
- raw fine-tuning
- prototype memory
- low-rank adapter
- matryoshka retrieval
- validator-conditioned head
- hybrid memory + adapter

Hero metric:

> adaptation precision = target-slice improvement minus off-target regression.

## Product phrasing

> Teach Augrade how this project works in ten examples.

## Deck line

> A good representation makes the right update low-dimensional.
