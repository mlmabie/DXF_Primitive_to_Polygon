# Augrade Q&A Alpha Refinement

Date: 2026-05-05

This note captures the technical "alpha" from the late-March Q&A/chat thread
that was not fully explicit in the first consolidation pass.

## Already Integrated Well

The durable center of the Q&A is already well represented in the setup branch:

- representation boundary over "GNN on BIM"
- geometry-native evidence -> object tokens -> typed graph -> validators
- RL/search only after graph state and edit grammar are clean
- compute-aware implementation choices
- workflow-first, hybrid, lightweight systems
- static vs dynamic graph construction as a real design choice
- PyG/custom path selection based on speed and stability, not fashion

## What Needed Sharpening

The chat had several high-value but under-integrated edges:

- convolutional filtering as a baseline and local-context feature extractor
- Neural Relational Inference as a useful analogy for latent relation discovery
- Temporal Straightening for latent planning as a representation objective
- Entropy-Preserving RL as a caution for sequential training loops
- cluster/compute questions as architecture constraints rather than casual ops
  curiosity

Those pieces are now folded into this note, the research map, and the
experiment plan.

## Convolutional Filtering

Convolutional filters should be treated as a strong baseline, not as a threat
to the vector-first thesis.

Useful roles:

- raster baseline for floorplan/object recognition
- local image chip around a primitive, supervector, or edge candidate
- denoising or edge/orientation context where vector provenance is incomplete
- comparison point for whether graph features are actually earning their cost

Boundary:

- convolutional filtering can supply local perceptual context
- vector primitives remain the authoritative geometry and provenance source

## Neural Relational Inference

Reference:

- Kipf et al., *Neural Relational Inference for Interacting Systems*, ICML
  2018. https://proceedings.mlr.press/v80/kipf18a.html

Why it matters:

NRI frames the problem as inferring a latent interaction graph while learning
the dynamics. For Augrade, the transfer is not unsupervised physics simulation
directly. The transfer is the idea that useful relations may be partially
latent and should be inferred from behavior, geometry, edits, and validation
outcomes.

Practical Augrade mapping:

- observed state: primitives, supervectors, components, rooms, annotations
- latent relations: same element, depends-on, blocks, routes-through,
  must-move-with, violates-with
- dynamics: graph edits, validator failures, repair sequences, revision traces

Do not oversell this as "use NRI out of the box." Use it as an analogy for
learning relation structure and interaction types when labels are incomplete.

## Temporal Straightening For Latent Planning

Reference:

- Wang et al., *Temporal Straightening for Latent Planning*, 2026.
  https://arxiv.org/abs/2603.12231

Why it matters:

The paper argues that planning improves when latent trajectories are locally
straightened, making simple distances in latent space better match planning
distance and improving objective conditioning.

Augrade relevance:

- edit sequences should ideally be smooth in representation space
- a good latent should make "small repair" and "large redesign" geometrically
  distinguishable
- residual edit tokens are a natural place to test whether latent transitions
  become simpler or more predictable

Practical test:

- compare graph/edit embeddings with and without a curvature/smoothness
  regularizer over revision or synthetic repair trajectories
- measure whether nearest latent states correspond to similar validator
  residuals, edit distance, and repair effort

## Entropy-Preserving Reinforcement Learning

Reference:

- Petrenko et al., *Entropy-Preserving Reinforcement Learning*, ICLR 2026.
  https://arxiv.org/abs/2603.11682

Why it matters:

The paper argues that policy-gradient objectives can collapse policy entropy
and reduce exploration diversity during training; it proposes explicit entropy
control methods so policies remain trainable and diverse.

Augrade relevance:

- if sequential edit optimization is added later, premature collapse would be
  bad: the model may repeatedly propose the same repair pattern even when the
  project admits multiple valid alternatives
- exploration diversity matters for routing, layout repair, and design option
  generation
- entropy monitoring should be part of the training dashboard for any future
  policy/search loop

Boundary:

This is a later-stage training concern. It should not distract from the first
task: stable graph state, typed actions, validators, and sparse baselines.

## Compute And Cluster Questions

The chat's cluster question should be treated as a system-design question:

- Are graphs static per drawing, dynamic after each edit, or mixed?
- Are graph shapes regular enough for compilation/static batching?
- Does the target hardware favor dense tensorized kernels, sparse PyG-style
  message passing, or custom batched edge-index code?
- Is graph construction or model forward pass the bottleneck?
- Is inference CPU-bound for interactive use, GPU-bound for batch review, or
  both?

Implication:

Start with a representation that can export both:

- inspectable heterogeneous graph data for research iteration
- flattened/batched tensors for fast baselines and deployment tests

## Refined Live Version

> The Q&A references all collapse into one practical stance: start with
> convolutional and sparse vector baselines, preserve exact vector state, infer
> latent relations where labels are incomplete, and design the training loop
> around the actual compute available. If we later add sequential policies, I
> would monitor exploration and entropy explicitly, because real design repair
> needs diverse valid options, not one collapsed edit habit.
