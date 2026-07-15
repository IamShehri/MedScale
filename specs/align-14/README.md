# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** Implemented / Merged / Closed

## Closeout

- Capability PR: #12
- Merge commit: `65f3685bac1668149550003382ca2da95715346e`
- Merged head: `56ffe65bda2be170cd2834fbb038af439d72e3d6`
- Merge timestamp: `2026-07-15T11:33:29Z`
- Merge method: merge commit

Final contract:

- Public symbol: `SplitAssignmentFreeze`
- Public constructor input: `Sequence[str]`
- Immutable stored representation: `tuple[str, ...]`
- Strategy: `SplitStrategy`
- Strategy identity: `strategy.value`
- Builder facade: 9 symbols
- Contract version: `split-freeze/v1`

Validation:

- `uv run ruff format --check .` PASS
- `uv run ruff check .` PASS
- `uv run mypy` PASS — 143 source files
- `uv run pytest tests/test_dataset_freeze.py -q` PASS — 30 tests
- `uv run pytest` PASS — 427 passed, 2 skipped
- CI run `29411540771` SUCCESS
- CodeQL run `29411540965` SUCCESS

Deferred integration:

- Release-manifest integration: deferred
- Benchmark-manifest integration: deferred

Implementation history:

1. implementation commit `6b68b6852ed4c228ee6ba61161f3ae39e7274500`
2. Ruff-format correction `7c13240b0581a63daadb93426a49ae151a1769d5`
3. sequence-typing correction `56ffe65bda2be170cd2834fbb038af439d72e3d6`

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
