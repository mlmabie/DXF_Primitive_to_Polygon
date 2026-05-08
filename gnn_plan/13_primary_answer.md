# Primary Answer: Training A GNN Over DXF/PDF Vector Soup

Date: 2026-05-08

## The Primary Question

Given a dirty soup of DXF, DWG, PDF-derived, and rendered drawing material, how
do we train a graph model to classify unordered vectors into primitives and
supervectors with high fidelity, data efficiency, and a clean partition between
epistemologically robust exemplars and cases that should stay uncertain?

## Short Answer

Do not start by asking the GNN to discover architecture from raw vector soup.
Start by building a deterministic evidence engine, then train graph products on
top of stable candidate state:

```text
raw DWG/DXF/PDF/render evidence
-> deterministic entity extraction and canonical render overlays
-> primitive table with stable ids and provenance
-> supervector candidate generator
-> heterogeneous primitive/supervector/annotation/face graph
-> sparse baselines and validator residuals
-> small calibrated GNN where graph context beats local features
-> robust exemplar bank + uncertainty/review partition
-> rule/prototype/memory updates
```

The GNN is not the truth engine. It is a calibrated context-propagation and
candidate-ranking layer over exact vector evidence.

## What Makes The GNN Worth Training

The graph model should be evaluated as a product-quality mechanism, not as an
architecture label. It is worth training when graph propagation creates trusted
work that deterministic geometry, sparse pair features, retrieval, or broad
foundation-model context do not already provide.

For this plan, the useful GNN is one that:

- preserves editable vector state and evidence links;
- beats sparse/local baselines on at least one relation or object-formation
  task where neighborhood context matters;
- improves annotation-to-object, supervector, or dependency recovery rather
  than only primitive classification;
- stays calibrated under review bands;
- remains stable under safe authored rewrites; and
- helps surface motifs, rules, or failure families that can improve the
  deterministic engine.

## What The Model Should Classify

The first target should not be only raw primitive labels. It should be a
multi-level target:

| Unit | Examples | Training role |
|---|---|---|
| primitive | line, arc, polyline, circle, hatch boundary, text, leader, dimension | preserve evidence and attach low-level labels |
| supervector | wall-face candidate, door swing, closed loop, fixture symbol, route-like path, tag group | main review/classification target |
| relation | labels, bounds, opens-into, parallel-offset, same-element, measures, conflicts-with | where message passing matters |
| face/region | room, shaft, terrace, balcony, ceiling zone | context for annotation and system reasoning |
| residual edit | merge, split, reassign, route, mark uncertain | future workflow supervision |

The practical first win is often supervector classification plus relation
recovery: "this cluster is a door swing" and "this `D1` tag labels that
opening."

## Data Contract

Every training example should carry:

- stable `prim_id`, `sv_id`, and `face_id`
- exact coordinates and canonical local frame
- source handle, layer, color, linetype, block/layout membership, and file path
- source kind: direct DXF/DWG entity, PDF vector extraction, raster-derived
  proposal, or rendered-view detection
- composition links from supervectors back to primitives
- typed edges and pair features
- optional raster crop or rendered-view evidence as a side channel
- validator residuals and review outcomes

Layer names and colors can be provenance, weak supervision, ablation features,
and review filters. They should not be trusted as the only semantic input.

## Graph Construction

Use a heterogeneous graph:

- `primitive` nodes for raw entities
- `endpoint` nodes for topology and closure
- `supervector` nodes for deterministic candidate groups
- `face` nodes for bounded regions
- `annotation` nodes for text, dimensions, leaders, tags, and colored markup
- later `constraint`, `edit`, and `memory` nodes

Use typed edges:

- `touches`
- `intersects`
- `near_endpoint`
- `collinear_with`
- `parallel_offset_from`
- `contains`
- `inside`
- `composed_of`
- `bounds`
- `labels`
- `measures`
- `opens_into`
- `same_element_candidate`
- `same_symbol_family`
- `route_candidate`
- `conflicts_with`

This makes the graph a substrate for reasoning, not just a pile of vectors.

## Training Recipe

### 1. Deterministic candidate generation first

Build primitive tables, endpoint/intersection topology, and supervector
candidates without the GNN:

- chains
- closed loops
- hatch boundaries
- wall-face candidates
- door-swing candidates
- repeated-cell candidates
- fixture-like symbol groups
- annotation/tag groups

The GNN should rank and correct candidates, not invent every candidate from
scratch.

### 2. Use sparse baselines as the floor

Before message passing, train:

- primitive feature classifier
- pair-relation classifier
- deterministic grouping heuristic
- raster/rendered-view baseline for visual context

The GNN ships only where it improves the hard cases: ambiguous tags, repeated
symbols, weak layer signal, carrier-style variation, relation recovery, and
supervector disambiguation.

### 3. Pretrain on structure before labels

Good low-label pretraining tasks:

- masked primitive attributes
- masked source carrier kind
- missing edge prediction
- relation type prediction
- local subgraph denoising
- rewrite-invariance classification
- object-to-annotation consistency
- validator residual prediction

These tasks use abundant unlabeled drawings and make the supervised labels go
farther.

### 4. Train multi-head, not one giant classifier

Separate heads:

- primitive class
- supervector class
- relation type/confidence
- annotation-to-object target
- validator residual
- uncertainty/calibration
- edit/review action

Separate heads make it easier to see whether the model knows geometry,
semantics, relations, or review policy.

### 5. Use precision conditioning

After a base model exists, adapt locally with:

- prototype memory for recurring project conventions
- small adapters or heads for customer/firm/jurisdiction conventions
- validator-conditioned scoring
- k-shot exemplars for new carrier patterns
- rule compilation when a learned motif becomes deterministic

The goal is:

> teach this project convention in ten examples without breaking the base
> geometry.

## Robust Exemplar Partition

The system should explicitly separate cases that are safe to learn from as
truth from cases that should remain uncertain, reviewed, or used only as weak
evidence.

### Robust Exemplars

A robust exemplar is not merely a high-confidence model prediction. It should
pass several evidence tests:

- stable id and provenance
- exact geometry preserved
- label aligns with deterministic geometry or metadata
- relation is validator-consistent
- label survives rewrite perturbations such as split/merge, carrier swap,
  snap jitter, hatch/outline replacement, and layer-schema remap
- agreement across at least one independent signal: annotation, layer/color
  weak label, text/tag semantics, rendered view, expert review, or validator
  residual
- low disagreement with sparse baseline or explainable disagreement that
  improves validation
- accepted by expert or repeatedly confirmed by workflow outcomes

These exemplars can enter the strong training set, prototype memory, eval set,
and rule-candidate queue.

### Non-Robust Or Ambiguous Cases

A non-robust case has one or more of:

- uncertain DWG/PDF conversion fidelity
- missing handles, text, colors, layout, or block membership
- label depends strongly on layer/color conventions
- multiple plausible object targets
- weak or contradictory annotation meaning
- rendered view and vector evidence disagree
- rewrite perturbation changes the prediction
- sparse baseline and GNN disagree without validator support
- low conformal confidence or poor calibration
- no expert/workflow confirmation

These cases should not be discarded. They are high-value review and active
learning material. Route them to:

- human review
- before/after overlay inspection
- prototype memory as weak examples
- query expansion through the scope resolver
- conversion QA
- new deterministic rule candidates

### Partition Policy

Use four lanes:

| Lane | Meaning | Action |
|---|---|---|
| Gold | expert-confirmed, validator-consistent, rewrite-stable | train/eval/rule mining |
| Silver | strong weak supervision, stable across checks, no contradiction | train with lower weight |
| Amber | plausible but ambiguous or under-scoped | review/active learning |
| Red | conversion error, contradiction, invalid geometry, or out-of-distribution | do not train as truth; fix pipeline or quarantine |

This is the "epistemological" boundary: the system should know the difference
between evidence it owns, evidence it borrows, and evidence it merely suspects.

## Data Efficiency Loop

The loop should be:

```text
unlabeled drawings
-> deterministic graph and rendered QA
-> self-supervised graph pretraining
-> weak labels from layers/tags/geometry/validators
-> small expert-confirmed gold set
-> calibrated sparse baseline
-> small hetero GNN
-> conformal review bands
-> active learning on high-value uncertainty
-> prototype/rule/memory update
-> new deterministic candidate generation
```

The active-learning queue should prioritize:

- high disagreement between sparse baseline and GNN
- high validator impact
- repeated uncertain motifs
- examples that affect many candidate objects
- cases that separate two project conventions
- cases where a single review can promote a deterministic rule

## Evaluation

Measure more than average F1:

- primitive macro-F1
- supervector macro-F1
- relation macro-F1 by relation type
- annotation-to-object accuracy
- calibration and expected calibration error
- conformal coverage
- review-load reduction at fixed precision
- rewrite stability
- drawing-level generalization
- conversion fidelity failure rate
- validator residual reduction
- rule conversion rate

Split by drawing/project, not randomly by primitive. Random primitive splits
leak drafter style, repeated symbols, layers, geometry scale, and conventions.

## PDF/Rendered Evidence

PDF/rendered views should be used as a perception and QA channel:

- render canonical views and tiles
- detect visible objects, labels, and regions
- align visual hypotheses back to vector primitives and supervectors
- flag vector/PDF disagreement as conversion or interpretation risk

Rendered views can bootstrap semantic grouping, but editable truth must land
back on exact vector ids and graph state.

## Gaps To Close

The current plan still needs:

1. **Conversion fidelity proof.** We need a DWG/PDF/DXF extraction harness that
   proves handles, text, color, layers, layouts, blocks, hatches, and geometry
   survive.
2. **Annotation semantics.** We need to distinguish architectural labels,
   schedule tags, dimensions, ordinary CAD text, and actual reviewer markup.
3. **Gold labels.** We need a small expert-confirmed gold set at primitive,
   supervector, relation, and annotation-to-object levels.
4. **Negative examples.** We need explicit "not same object," "not labels,"
   "not route," and "do not merge" labels.
5. **Rewrite benchmark.** We need authored equivalence transforms and a metric
   for whether labels survive them.
6. **Calibration set.** We need held-out drawings for conformal/review-band
   calibration.
7. **Validator inventory.** We need to enumerate which residuals are exact now
   and which are future policy or engineering heuristics.
8. **Project memory schema in practice.** We need real examples of conventions,
   rejected details, and workflow outcomes to test memory retrieval.
9. **PDF/vector alignment.** We need evidence IDs linking rendered detections
   back to exact vector entities.
10. **Compute profile.** We need to know whether graph construction, feature
    generation, model inference, or scope resolution is the bottleneck.

## Final Form

> Train the GNN on a deterministic, provenance-rich, heterogeneous graph of
> primitives, supervectors, annotations, faces, and typed relations. Use
> self-supervision, weak labels, validators, prototype memory, and expert
> review to make labels data-efficient. Partition examples into gold, silver,
> amber, and red evidence lanes so only robust exemplars become truth, while
> ambiguous cases become active-learning, QA, memory, or rule-discovery fuel.
