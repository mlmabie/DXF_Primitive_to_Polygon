# 2027 Publishable Paper Trajectory

Publication north star:

> turn authored CAD into a verifier-backed learning environment where models reduce residual complexity and compile discoveries into persistent mechanisms.

## Sequencing principle

Do not lead with “we trained a CAD GNN.” Lead with the system boundary: vector graph state, rewrite stability, validator residuals, workflow memory, and rule compilation.

Publish in the order that de-risks the product. Annotation alignment and rewrite benchmarks create the substrate; embeddings and motif discovery create compounding product memory; verifier environments create the agentic loop.

Treat model architecture as replaceable. The publishable invariant is the environment and representation geometry, not any single message-passing layer.

## What not to publish first

1. Generic “GNN for CAD classification” with static labels and no validator loop.
2. Pure architecture before sparse relational baselines and rewrite stability tests exist.
3. Mechanistic interpretation that names features but does not compile discoveries into engine rules.
4. RL/autoresearch before action grammar and validators define rewards.

## Ladder

| # | Paper concept | Why it matters | Minimum proof |
|---|---|---|---|
| 1 | Annotation-to-object correspondence in layer-blind vector CAD graphs | Easiest first; turns CAD annotations into supervision without pretending every colored entity is a clean label. | Graph export + annotation semantics + drawing-level splits. |
| 2 | Rewrite-stable vector graphs for authored CAD | Strongest substrate paper; CAD variation is authored rewrite structure, not random noise. | Rewrite generators + score variance + sparse/GNN/embedding comparison. |
| 3 | Matryoshka graph embeddings for interactive CAD verification | Systems/product paper; one representation supports many latency and retrieval budgets. | Nested embeddings for cache, verifier routing, review retrieval, offline rule mining. |
| 4 | Supervector molecules: motif discovery and rule compilation | Most original research contribution; molecular-GNN analogy for CAD motifs that become engine primitives. | Discover motifs -> expert validation -> deterministic supervector/rule -> measured engine improvement. |
| 5 | Engagement-aware verifier loops for CAD automation | Human loop as product surface and training environment. | Embedded review vs abstract labels; label yield, trust, residual closure. |
| 6 | CAD verifier environments for typed edit repair | Autoresearch/RL paper; verifiable rewards over graph edit actions. | Environment = drawing graph + action grammar + validators + reward/rubric. |
| 7 | Mechanistic interpretation of pretrained CAD graph networks | Frontier thread; publish only when interpretation compiles into engine improvements. | Latent features/circuits -> motif/rule proposal -> validator-backed patch. |

## Paper 1 — Annotation-to-object correspondence

Claim: architectural annotations are supervision, but not clean labels. The first dataset should learn what annotations refer to, not merely what primitives are.

Recommended framing:

- Task: map text, tags, leaders, dimensions, colored marks, and room names onto primitive/supervector/face/component targets.
- Model comparison: geometry-only baseline, metadata ablation, sparse relation features, small GNN only where local ambiguity remains.
- Eval split: by drawing/project, never randomly by entity.
- Win condition: useful supervision recovered and ambiguous annotation edges routed to review.
- Fatal risk: assuming all colored marks are labels.

## Paper 2 — Rewrite-stable vector graphs

Claim: CAD equivalence is authored and categorical, not clean Euclidean symmetry. The model should collapse safe rewrite orbits and preserve semantic boundaries.

Rewrite set:

- collinear split/merge
- carrier swap
- snap jitter
- schema remap
- hatch-outline equivalence

Metric: score variance and embedding drift across rewrite generators by relation type.

Negative-result value: if a rewrite fails, the system learns the equivalence is family-conditioned or unsafe.

## Paper 3 — Matryoshka graph embeddings

Claim: embedding size should be a product knob, not a retraining event.

| Embedding scale | Product surface | Metric |
|---|---|---|
| 32–64d | Interactive cache invalidation, duplicate retrieval, local edit hints | Latency, cache hit rate, local retrieval precision |
| 128–256d | Verifier routing, annotation queue triage, prototype memory | Routing accuracy, review yield, calibration |
| 512d+ | Offline failure clustering, cross-project motif discovery, mech-interp probes | Motif purity, rule conversion, cross-project retrieval |

## Paper 4 — Supervector molecules

Claim: the interesting CAD unit is often not the primitive; it is the reusable motif. The model should discover CAD “molecules” and compile them into engine objects.

| Chemistry analogy | CAD analogue |
|---|---|
| Atom | Primitive: line, arc, hatch, text, insert |
| Bond | Endpoint, adjacency, containment, label/leader edge |
| Functional group | Supervector: hatch-outline wall mass, door-swing/opening/tag, repeated panel cell |
| Molecule/scaffold | Room/wall/opening assembly, shaft cluster, repeated symbol family |
| Reaction mechanism | Typed edit rule: merge, split, attach, reroute, reassign |
| Energy/property | Validator residual, edit acceptance, review time saved |

## Paper 5 — Engagement-aware verifier loops

Claim: annotation quality is endogenous to product experience. Make review feel like high-leverage design work, not data labeling.

Natural venues: AEC venues, CSCW, CHI. Treat benchmark-style evaluation as supporting evidence, not headline.

Measure:

- review yield
- correction compression
- repeat-error decay
- rule conversion
- time-to-trust

## Paper 6 — CAD verifier environments

Claim: agentic CAD repair becomes tractable only after state, action, and validators are explicit.

- Environment state: drawing graph + protected geometry + workflow context.
- Action grammar: merge, split, attach, reroute, reassign, resize, repair, delete.
- Reward/rubric: validator accepts, residual decreases, edit cost is minimal, protected geometry unchanged.

Use Prime-style environments for breadth experiments only after validators mature; do not outsource M1–M3 or M7.

## 2026–2027 sequencing

| Window | Primary target | Proof artifact | Decision gate |
|---|---|---|---|
| 2026 Q2–Q3 | Substrate + annotation alignment | Graph manifests, annotation residual reports, sparse calibrated baseline | Can we build trusted graph state and review triage without a GNN? |
| 2026 Q3–Q4 | Rewrite benchmark | Rewrite generators + stability report + cross-drawing split | Which rewrite orbits are safe, family-conditioned, or unsafe? |
| 2027 Q1 | Matryoshka embeddings + retrieval memory | Nested embeddings for cache/routing/offline discovery | Does embedding size become an operational product knob? |
| 2027 Q2 | Supervector molecule discovery | Motif clusters, expert validation, engine rule patch | Does a discovered motif improve deterministic coverage/review time? |
| 2027 Q3–Q4 | Verifier environments + objective loops | Typed edit environment, validator rewards, agent search comparison | Can the model loop below the expert until a higher-order objective is review-ready? |
