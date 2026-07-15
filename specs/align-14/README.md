# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** NOT AUTHORIZED

## Canonical baseline

- Branch: `main`
- Baseline SHA: `6c47a910fb6cc9ce41e309d891e58e0b3750f21d`
- ALIGN-13: post-merge closed

## Selected capability

ALIGN-14 plans an immutable deterministic split-assignment freeze contract layered on the existing deterministic splitter and the existing `DatasetReleaseManifest`.

This package does not authorize implementation. No branch, commit, push, PR, or capability code may be created without a separate founder authorization.

## Documents

| Document | Purpose |
|---|---|
| `README.md` | Planning package index and authorization summary |
| `spec.md` | Capability definition, functional requirements, and non-goals |
| `research.md` | Evidence inventory, candidate scoring, and overlap analysis |
| `plan.md` | High-level implementation phase plan |
| `data-model.md` | Existing and proposed concepts, lineage, and field semantics |
| `contracts.md` | Proposed public and internal symbols, serialization, and facade impact |
| `acceptance.md` | Measurable acceptance gates |
| `decision-record.md` | Selection rationale, rejected alternatives, and required founder decisions |

## Dependencies

- Proposed ADR-0032 must be accepted before implementation authorization.
- ALIGN-13 builder contracts, manifest, and fingerprint surfaces remain the foundational layer.
- ALIGN-14 must reuse `medscale.dataset.split` and must not duplicate `DatasetReleaseManifest`.

## Explicit prohibition

Implementation, code changes, runtime-test changes, public API changes, branch creation, commits, pushes, PRs, issues, tags, releases, merges, roadmap updates, and ADR status changes are all outside this authorization.
