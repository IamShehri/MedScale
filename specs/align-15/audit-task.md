# ALIGN-15 — Evaluation Engine Boundary Audit — Task Definition

## Task identity

- ID: ALIGN-15
- Title: Evaluation Engine Boundary Audit and Alignment Registry Reconciliation
- Owner: MedScale principal architect / governance auditor
- Status: Complete

## Task definition

Complete a documentation-only, repository-grounded audit of the existing MedScale evaluation-engine surface. The audit must:

1. Reconcile the stale central alignment registry (`specs/public-repository-alignment/{tasks,plan,spec}.md`).
2. Inspect actual evaluation-related code, tests, exports, and dependencies currently on `main`.
3. Determine the smallest dependency-complete evaluation capability boundary.
4. Classify symbols as public, experimental, or internal.
5. Determine whether an ADR is required.
6. Produce an implementation-ready planning package without implementing anything.

This task does not authorize production code.

## Artifacts

- `specs/align-15/README.md`
- `specs/align-15/research.md`
- `specs/align-15/spec.md`
- `specs/align-15/plan.md`
- `specs/align-15/audit-task.md`
- `specs/align-15/contracts.md`
- `specs/align-15/data-model.md`
- `specs/align-15/decision-record.md`
- `specs/align-15/acceptance.md`
- Updated `specs/public-repository-alignment/tasks.md`
- Updated `specs/public-repository-alignment/plan.md`
- Updated `specs/public-repository-alignment/spec.md`

## Verification

- `git diff --check`: PASS
- Documentation scope gate: PASS (no `src/`, `tests/`, `.github/`, `pyproject.toml`, or lockfile changes)
- Worktree: clean
- Staging: clean
- commit: `docs(align-15): audit evaluation engine boundary`

## Next gate

After the documentation-only PR is reviewed and merged, any future evaluation implementation remains separately gated by a new founder authorization and, if required by the audit, a separately approved ADR.
