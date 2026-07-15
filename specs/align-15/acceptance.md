# ALIGN-15 — Evaluation Engine Boundary Audit Adoption Record

## Audit claims and repository evidence

### Claim 1 — Canonical main verified

```text
origin/main: 99b024aaf6831ad15296cb85210b8ae7f8df6998
ALIGN-13 (6c47a910fb6cc9ce41e309d891e58e0b3750f21d) ancestor: YES
ALIGN-14 IMPL (65f3685bac1668149550003382ca2da95715346e) ancestor: YES
ALIGN-14 GOV (99b024aaf6831ad15296cb85210b8ae7f8df6998) ancestor: YES
```

### Claim 2 — No standalone evaluation engine exists

Repository evidence: `git grep` of `EvaluationReport`, `EvaluationResult`, `evaluation.pipeline.execution` across `src/`, `tests/`, `docs/`, `specs/` returns:
- architecture documents and plans referencing future evaluation concepts;
- domain-specific `EvaluationRun` in `litdb/triage_eval.py`;
- no `EvaluationReport`, `EvaluationResult`, or `EvaluationEngine` class in production source.

### Claim 3 — Actual evaluation-adjacent modules inventoried

Production modules:
- `src/medscale/bench/__init__.py`
- `src/medscale/bench/baselines.py`
- `src/medscale/bench/run.py`
- `src/medscale/bench/scorers.py`
- `src/medscale/bench/spec.py`
- `src/medscale/bench/store.py`
- `src/medscale/bench/tasks/__init__.py`
- `src/medscale/bench/tasks/task_001_literature_classification.py`
- `src/medscale/bench/tasks/task_002_evidence_extraction.py`
- `src/medscale/bench/tasks/task_003_screening_prioritization.py`
- `src/medscale/bench/validate.py`
- `src/medscale/workspace.py` (contains `Benchmark` facade)
- `src/medscale/litdb/triage_eval.py` (domain-specific, internal)

Tests:
- `tests/test_bench_engine.py`
- `tests/test_bench_replay.py`
- `tests/test_bench_tasks.py`

Facade exports confirmed via:
- `src/medscale/__init__.py` — exposes `Benchmark` through `Workspace`
- `src/medscale/workspace.py` — `__all__` excludes individual bench symbols
- `src/medscale/bench/__init__.py` — internal subpackage with its own `__all__`
- `src/medscale/cli/__init__.py` — registers `bench` subcommand

### Claim 4 — Symbol classification matrix

| Symbol | Current path | Current exposure | Recommended classification | Rationale |
|---|---|---|---|---|
| `Benchmark` | `workspace.py` | public via `medscale.__init__` | public | Immutable facade for snapshot-bound benchmark execution. Deterministic, serializable, content-addressed input/output. |
| `BenchmarkSpec` | `bench/spec.py` | public-frozen via `Benchmark` | public | Versioned, immutable scientific contract. Content-hashed identity. Already accepted into public API. |
| `TaskItem` | `bench/tasks.py` | public-frozen via `Benchmark` | public | Immutable unit of work with human-validated gold. Restricted to implemented task types. |
| `TaskOutput` | `bench/tasks.py` | public-frozen via `Benchmark` | public | Immutable system output contract (id references and statements). |
| `BenchmarkRunArtifact` | `bench/run.py` | public-frozen via `Benchmark` | public | Immutable, content-addressed deterministic result. Already returned by `Benchmark.run()`. |
| `EvidenceSystem` | `bench/run.py` | internal protocol | internal | Backend plug contract; not in top-level `__init__.py`. Stability depends on model-kit interface stability. |
| `TaskType` | `bench/spec.py` | public-frozen via `Benchmark` | public | Stable enum of implemented task types with reserved extension point. |
| `GoldEvidenceSet` | `bench/tasks.py` | public-frozen via `Benchmark` | public | Immutable human-validated gold contract. |
| `Statement` | `bench/tasks.py` | public-frozen via `Benchmark` | public | Immutable summary statement with evidence citations. |
| `SCORER_VERSION` | `bench/scorers.py` | internal constant | internal | Recorded in artifact; not part of public surface. |
| `score_item` | `bench/scorers.py` | internal function | internal | Deterministic per-item scoring; public exposure not required. |
| `set_precision`, `set_recall` | `bench/scorers.py` | internal functions | internal | Implementation details of scoring. |
| `validate_benchmark` | `bench/validate.py` | internal function | internal | Validation; exposed through `Benchmark.validate()`. |
| `load_benchmark`, `write_benchmark` | `bench/store.py` | internal functions | internal | Persistence; not in public surface. |
| `run_benchmark` | `bench/run.py` | internal function | internal | Underlying runner; public surface is `Benchmark.run()`. |
| `EvaluationRun` | `litdb/triage_eval.py` | internal | internal | Domain-specific to AI Triage. Not a general evaluation engine. |
| `EvaluationResult` | N/A | N/A | N/A | Does not exist. Do not create without a follow-up ADR and concrete use case. |
| `EvaluationReport` | N/A | N/A | N/A | Does not exist. Do not create without a follow-up ADR and concrete use case. |

### Claim 5 — Minimum slice defined

**Production allowlist:**

```text
src/medscale/bench/__init__.py
src/medscale/bench/baselines.py
src/medscale/bench/run.py
src/medscale/bench/scorers.py
src/medscale/bench/spec.py
src/medscale/bench/store.py
src/medscale/bench/tasks/__init__.py
src/medscale/bench/tasks/task_001_literature_classification.py
src/medscale/bench/tasks/task_002_evidence_extraction.py
src/medscale/bench/tasks/task_003_screening_prioritization.py
src/medscale/bench/validate.py
src/medscale/workspace.py (Benchmark facade only)
```

**Test allowlist:**

```text
tests/test_bench_engine.py
tests/test_bench_replay.py
tests/test_bench_tasks.py
```

**Protected files:**

```text
src/medscale/bench/run.py (BenchmarkRunArtifact)
src/medscale/bench/spec.py (BenchmarkSpec)
src/medscale/bench/tasks.py (TaskItem, TaskOutput)
src/medscale/__init__.py (top-level exports)
src/medscale/workspace.py (public facade)
```

**Explicit exclusions:**

```text
src/medscale/litdb/triage_eval.py (domain-specific)
src/medscale/evaluation/ (does not exist)
src/medscale/evaluation/pipeline/ (does not exist)
src/medscale/evaluation/pipeline/execution.py (does not exist)
EvaluationReport, EvaluationResult, EvaluationEngine (do not exist)
```

### Claim 6 — ADR decision

```text
ADR NOT REQUIRED
```

The existing accepted ADRs (ADR-0015, ADR-0017, ALIGN-14) fully determine ownership, public API, serialization, versioning, and compatibility for the current benchmark runner surface. No unresolved architectural decision exists.

A future ADR would be required before introducing:
- `EvaluationResult` contract;
- `EvaluationReport` class;
- `ExecutionState` with retry semantics;
- a general-purpose evaluation facade parallel to `Benchmark`.

### Claim 7 — Registry reconciliation

**ALIGN-13:** status updated to completed with PR #10 evidence.

**ALIGN-14:** status updated to completed with PRs #11, #12, #13 evidence.

**ALIGN-15:** status set to complete (audit); implementation remains blocked.

**Phase 2:** marked complete.

**Phase 3:** redefined as evaluation boundary audit, not implementation.

### Claim 8 — Naming analysis

- `BenchmarkRunArtifact` is the de facto public result contract for benchmark execution. It is frozen, deterministic, content-addressed, and serializable.
- There is no `EvaluationReport` or `EvaluationResult` class in the current repository.
- The Phase 3 assumption of an `EvaluationReport` != `EvaluationResult` layering does not match the current flat `BenchmarkRunArtifact` model.
- The triage evaluation (`EvaluationRun` in `litdb/triage_eval.py`) is a separate domain concept and should not be generalized.

## Verification evidence

```text
git diff --check: PASS
Documentation scope gate: PASS (no production, test, workflow, dependency, or lockfile changes)
Worktree: CLEAN
Staging: CLEAN
pytest: NOT APPLICABLE
```

## Next founder gate

```text
After CI and CodeQL complete successfully on the corrected head, founder authorization is required for the guarded merge of PR #13.
```

Wait — correction. This is ALIGN-15. The correct next gate is:

```text
After the ALIGN-15 documentation PR is reviewed, merged, and CI/CodeQL complete, any future evaluation implementation remains separately gated by a new founder authorization and, if required by a subsequent audit, a separately approved ADR.
```

```text
After the ALIGN-15 documentation PR is reviewed, merged, and CI/CodeQL complete, any future evaluation implementation remains separately gated by a new founder authorization and, if required by a subsequent audit, a separately approved ADR.
```
