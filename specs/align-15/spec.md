# ALIGN-15 — Evaluation Engine Boundary Audit

## Problem

The central public-repository alignment documents present the evaluation engine boundary as a future capability to be audited in Phase 3, with assumptions about a module path `evaluation.pipeline.execution` and types `EvaluationReport` / `EvaluationResult` that do not exist on current `main`.

The stale baseline SHA and pending status misrepresent the current repository state and could drive an authorization decision against a false map of the code surface.

## Objective

Audit the actual evaluation-related surface on current `main` and produce:
- an exact inventory of evaluation-adjacent modules, symbols, tests, and dependencies;
- a symbol classification matrix (public / experimental / internal);
- a determination of whether an ADR is required;
- the minimum dependency-complete future slice;
- reconciled central alignment registry records;
- an implementation-ready planning package without authorizing implementation.

## Scope

- read-only inspection of `src/`, `tests/`, `docs/`, `specs/`, `pyproject.toml`;
- reconciliation of `specs/public-repository-alignment/{tasks,plan,spec}.md`;
- creation of `specs/align-15/` planning package;
- **no production source changes**;
- **no test changes**;
- **no public export changes**;
- **no CLI changes**;
- **no workflow, dependency, or lockfile changes**;
- **no implementation**;
- **no ADR creation or acceptance**.

## Non-goals

- Do not implement an evaluation engine.
- Do not rename any existing symbol.
- Do not create a `medscale.evaluation` package.
- Do not expand the top-level `medscale.__all__`.
- Do not change benchmark semantics.
- Do not authorize future implementation; future slices remain separately gated.
- Do not modify ALIGN-14 branches or clean them up.

## Success criteria

- Every evaluation-adjacent symbol on `main` is inventoried and classified.
- The central alignment registry accurately records ALIGN-13, ALIGN-14, and ALIGN-15 status.
- The audit documents the actual relationship between execution, result, and report concepts.
- The minimum future slice has a finite production and test allowlist.
- ADR requirement is explicitly decided.
- All changes are documentation-only under `specs/`.
- Verification evidence is recorded without requiring pytest for the commit.

## Constraints

- Branch from the exact `origin/main` at `99b024aaf6831ad15296cb85210b8ae7f8df6998`.
- Preserve all ALIGN-14 commit history.
- Do not modify the dirty main worktree or the implementation worktree.
- Do not push, open a PR, merge, tag, release, or start another ALIGN task.
- Do not run inference, model execution, network calls, or external APIs during inspection.
