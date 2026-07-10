# ADR-0014 — Spine Code Namespace: `medscale.core`

- **Status:** Proposed (awaiting operator approval)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [ADR-0004](0004-t0-foundation-scope.md),
  [ADR-0012](0012-layered-architecture-model.md) (spine + capability layers),
  [ADR-0013](0013-language-strategy.md)

## Context

The founder's roadmap names "Phase 1 — `medscale.core`" (identifiers, hashing,
timestamps, provenance, validation, schemas, reproducibility metadata). **Those
capabilities already exist and are tested** — as top-level modules:
`medscale.reproducibility` (hashing, canonical JSON, seeds) and `medscale.provenance`
(identifiers, timestamps, retrieval provenance), with schema validation living in each
schema's own module (`medscale.evidence`, `medscale.litdb.*`).

So Phase 1 is functionally complete; the open question is purely **namespace shape**:
should spine code be consolidated under `medscale.core` so the ADR-0012 architecture
(spine vs capability layers) is visible in the import graph itself?

## Decision (proposed)

Consolidate the spine under **`medscale.core`** — **now, before any external release**,
when the rename is free:

1. `medscale.core.reproducibility` (moves `medscale/reproducibility.py`) and
   `medscale.core.provenance` (moves `medscale/provenance.py`).
2. Top-level re-exports preserved (`medscale.canonical_json` etc. keep working), so the
   public convenience surface is unchanged.
3. **Layer modules stay put**: `medscale.evidence` (Evidence layer) and `medscale.litdb`
   (Knowledge layer) are capability layers, not spine — moving them into `core` would
   blur exactly the distinction ADR-0012 draws. Future spine additions (release
   manifests, schema-validation helpers) land in `core`.
4. One mechanical commit: move + import updates + full gate green; no behavior change,
   no new code.

**Why now and not at v0.2:** today there are zero external consumers, so the rename
costs one commit and zero deprecation machinery. At v0.2 (PyPI) the same change needs
deprecation shims and a versioning note, forever. The cheapest moment is this one.

**Why not skip it:** in a 10–20-year, hundreds-of-contributors repo, "which code is the
non-negotiable spine?" should be answerable from the package tree, not from tribal
knowledge. `medscale.core` makes the architecture self-documenting — the directive's
discoverability-over-cleverness principle applied to the import graph.

## Consequences

**Positive:** import graph mirrors the accepted architecture; contributor intuition
("core = spine, touch with care") comes free; future spine components have an obvious
home.

**Negative / costs:** one-time churn in ~10 files and the docs that cite module paths;
`git blame` indirection through the move (mitigated: pure `git mv` + import edits).

## Alternatives considered

- **Keep the flat layout.** Viable — the code works and ADR-0004's minimalism favors
  it. Rejected on the 10-year lens: flat layouts stop scaling the moment the spine
  grows its next module, and the rename only gets more expensive.
- **Put everything (evidence, litdb) under `core`.** Rejected: erases the
  spine/capability-layer distinction that is the architecture.
- **Defer to v0.2.** Rejected: strictly more expensive later (deprecation shims,
  public-API break notes) for zero added information.

## Compliance

Implementation only after operator approval, as one mechanical commit with the full
quality gate. Docs citing module paths are updated in the same commit.
