# Programmatic vs Contextual Merges

The boundary between programmatic and contextual merges isn't about who or what makes the decision — it's about whether the decision is contained in the metadata or requires interpretation beyond it. That's an epistemic property of the problem, not an implementation choice.

**Programmatic merges** are decidable from provenance metadata and degenerate geometry alone. They collapse representation variants: the same geometry recovered twice via different extraction paths, or drawn on complementary layer-name variants.

Sufficient signals: `source_kind` disagreement, `canonical_layer` match, `variant_group` relationship, `boundary_gap ≈ 0`, `area_ratio ≈ 1`.

**Contextual merges** require spatial neighborhood, alignment continuity, thickness consistency, or architectural plausibility — information the pair metadata does not contain.

## Evidence: Columns

119 recommended merges decompose into three categories:

**12 programmatic positives.** Same raw layer (`S-COLUMN`), boundary gap < 0.1, one recovered via `graph_face` (half-edge walk over snapped LINEs), the other via `direct_ellipse` (closed ELLIPSE recognized directly). Area difference ~0.5% from discretization. Decision requires only: `same_layer AND gap ≈ 0 AND source_kind ≠ source_kind`.

**33 contextual negatives.** Same layer, gap 0.2–1.0, same or similar extraction kind, similar area. Physically adjacent but distinct columns — paired at a structural bay, or a column next to its fireproofing ring. Metadata says "similar and close." Only spatial context says "two separate elements."

**74 ambiguous.** Gap 0.1–0.5. Metadata alone cannot distinguish "same column drawn with slight offset" from "two columns 0.3 units apart."

## Evidence: Curtain Walls

29 recommended merges. All 29 are programmatic:

- One polygon from `A-GLAZING MULLION` (LINE → graph_face)
- The other from `A-GLAZING-MULLION` (closed LWPOLYLINE → direct extraction)
- Boundary gap = 0, area ratio ≈ 1

The normalization analysis already proved these layers are complementary — 97% spatial overlap, zero shared entity types, same mullions drawn with two CAD conventions. Decision requires only: `canonical_layer_match AND gap ≈ 0 AND complementary_variant_group`.

## Evidence: Walls

28 recommended merges. Only 1 is programmatic (touching, aligned, same layer).

**15 close pairs** (gap 2–10) on `A-MEZZANINE WALL FULL`. Could be two faces of one wall split during extraction, or two parallel walls. Gap alone doesn't say — need the neighborhood.

**12 far pairs** (gap > 10). Separate walls that happen to be colinear. Programmatically negative, but the threshold is family- and file-dependent.

Layer distribution across all 28: `A-MEZZANINE WALL FULL` (38 mentions), `A-WALL 2` (14), `A-WALL 1` (4).

## Merge problem structure

The merge problem factors into two sequential quotients:

**Quotient 1 — representation equivalence (programmatic).** Two candidates represent the same geometry if they share the same footprint and differ only in authoring or extraction method. Apply exhaustively first. Reduces the candidate set without judgment. Analogous to Unicode normalization or BPE merge rules.

**Quotient 2 — semantic identity (contextual).** Two candidates represent the same architectural element if they are parts of one physical thing decomposed during drafting or extraction. Requires neighborhood features, alignment reasoning, or expert labels. This is where learning adds value, where the merge lab earns its keep, and where a GNN over the candidate graph would propagate real signal.

## Investment consequences

| | Programmatic | Contextual |
|---|---|---|
| Rules | Exhaustive, deterministic, write once | Family-specific, tune per file |
| Learning | Not needed — metadata suffices | High value: pair features + neighborhood |
| Labels | Auto-generatable (87 labels, zero visual inspection) | Expensive: merge lab or spatial review |
| Failure mode | False merge of adjacent distinct elements (tight gap gate mitigates) | Under-merge of fragmented walls (learned scoring or expert review mitigates) |
| Scaling | Any file with same layer conventions | Needs adaptation per drafter/file/family |

Get the programmatic quotient right first. Then the contextual learning problem is smaller, cleaner, and better-defined.
