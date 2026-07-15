# ALIGN-15 — Evaluation Engine Boundary Audit — Repository Evidence

## Discovery methodology

Audit inspected `origin/main` at `99b024aaf6831ad15296cb85210b8ae7f8df6998` using:
- `find src/medscale -type f | sort`
- `find tests -type f | sort`
- `git grep -n -E 'EvaluationReport|EvaluationResult|evaluation|evaluator|pipeline|execution|metric|benchmark|uncertainty|report bundle' -- src tests docs specs`
- Read-only inspection of all discovered evaluation-adjacent modules

## Key finding: no standalone evaluation engine exists

The repository does not contain a module named `medscale.evaluation` or `medscale.evaluation.pipeline.execution`.

There are no `EvaluationReport`, `EvaluationResult`, or `EvaluationEngine` classes in the production source.

The grep results that mention "evaluation" are overwhelmingly:
- ADR and architecture discussion in `docs/`
- Model-kit backend type annotations (`evaluation-only` roles in `registry.py`)
- Layout constants (`_layout.py` defines `EVALUATION_DIR` for a docstring path)
- Query strings containing "evaluation methodology" in litdb search queries
- Historical plans referring to future evaluation execution

The only production module named around evaluation is:
- `src/medscale/litdb/triage_eval.py` — domain-specific metrics for the AI Triage Assistant, **not** a general-purpose evaluation engine

## Actual evaluation-adjacent modules that exist on main

### `medscale.bench` — benchmark execution surface

This is the closest thing to an "evaluation engine" in the current codebase. It is a deterministic snapshot-bound benchmark runner, not a general ML evaluation harness.

**Production files:**
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

**Test files:**
- `tests/test_bench_engine.py`
- `tests/test_bench_replay.py`
- `tests/test_bench_tasks.py`

**Facade exposure:**
- `src/medscale/bench/__init__.py` exports: `SCORER_VERSION`, `BenchmarkRunArtifact`, `BenchmarkSpec`, `EmptySystem`, `EvidenceSystem`, `GoldEvidenceSet`, `GoldOracle`, `Statement`, `TaskItem`, `TaskOutput`, `TaskType`, `load_benchmark`, `run_benchmark`, `score_item`, `validate_benchmark`, `write_benchmark`
- `src/medscale/workspace.py` re-exports `BenchmarkRunArtifact`, `EvidenceSystem`, `run_benchmark`, `BenchmarkSpec`, `load_benchmark`, `list_benchmarks`, `TaskItem`, `validate_benchmark` through the `Benchmark` class
- Top-level `medscale.__init__.py` does not import `BenchmarkRunArtifact`, `EvidenceSystem`, `run_benchmark`, `BenchmarkSpec`, or any bench symbol directly; it only exposes `Benchmark` through the workspace facade

**Dependencies (from `bench/run.py`):**
- `medscale._layout` — layout constants
- `medscale.bench.scorers` — deterministic scoring
- `medscale.bench.store` — benchmark store
- `medscale.bench.tasks` — task contracts
- `medscale.bench.validate` — benchmark validation
- `medscale.evidence_store` — evidence loading (no model execution)
- `medscale.modelkit.interfaces.ModelRef` — model identity only
- `medscale.provenance.validate_timestamp` — timestamp validation
- `medscale.reproducibility` — canonical JSON, content hash
- `medscale.research.index.ResearchIndex` — read-only index

**Dependencies (from `workspace.py`):**
- `medscale.bench.run`, `medscale.bench.spec`, `medscale.bench.store`, `medscale.bench.tasks`, `medscale.bench.validate`
- `medscale.evidence` — evidence data model
- `medscale.evidence_checks` — verification checks
- `medscale.litdb.integrity` — integrity report
- `medscale.litdb.records` — record model
- `medscale.research.index`, `medscale.research.query`, `medscale.research.snapshot`, `medscale.research.stats`

**CLI exposure:**
- `src/medscale/cli/bench.py` — `medscale bench {list|validate|run|replay|init}`
- `src/medscale/cli/__init__.py` — registers `bench` subcommand

**Tests:**
- `tests/test_bench_engine.py` — end-to-end runner tests
- `tests/test_bench_replay.py` — replay contract tests
- `tests/test_bench_tasks.py` — task fixture tests

### `medscale.litdb.triage_eval` — domain-specific evaluation

**Production file:**
- `src/medscale/litdb/triage_eval.py`

**Exports:**
- `EvaluationRun`, `compute_metrics`, `evaluate`, `load_goldset`, `write_goldset`

**Dependencies:**
- `medscale.litdb.ai_triage` — triage log loading
- `medscale.litdb.review.ReviewDecision` — review decision enum
- `medscale.reproducibility.canonical_json` — serialization

**Classification:** internal — domain-specific to AI Triage, not a general-purpose evaluation engine surface

### `medscale.evidence` — evidence data model

**Production files:**
- `src/medscale/evidence.py`
- `src/medscale/evidence/__init__.py`
- `src/medscale/evidence/grading.py`
- `src/medscale/evidence/models.py`
- `src/medscale/evidence/protocol.py`
- `src/medscale/evidence_store.py`
- `src/medscale/evidence_checks.py`

**Exposure:** public-frozen data model per ADR-0017, but not an evaluation engine

### `medscale.workspace.Benchmark` — public facade for benchmark execution

**Path:** `src/medscale/workspace.py`

**Public methods:**
- `Benchmark.validate()` — tuple[str, ...] issues
- `Benchmark.run(system) -> BenchmarkRunArtifact` — executes against evidence system

**Classification:** this is the stable public surface for benchmark execution. It does not expose `EvaluationReport`, `EvaluationResult`, or a generic evaluation engine.

## Naming analysis: execution, result, report

The current repository uses three distinct concepts with different ownership:

| Concept | Actual symbol(s) | Owner | Notes |
|---|---|---|---|
| execution | `run_benchmark` function | `medscale.bench.run` | Internal runner; accepts `EvidenceSystem` protocol |
| result | `BenchmarkRunArtifact` | `medscale.bench.run` | Frozen dataclass; content-addressed via `results_id` |
| report | `BenchmarkResult` (not present) vs `BenchmarkRunArtifact` | workspace facade only | Public `Benchmark.run()` returns `BenchmarkRunArtifact`; no separate report class |

**Answers to Phase 3 naming questions:**

1. Is there a real naming mismatch? **Partially.** The repository has `BenchmarkRunArtifact` (a frozen result dataclass) but no separate human-readable "report" class. The docstrings and architecture documents use "report" loosely — `BenchmarkRunArtifact` serves as both the machine-readable result and the reproducible artifact. This is not a technical mismatch requiring renaming; it is a documentation-level inconsistency between the natural-language "report" concept and the actual dataclass name.

2. Are `Report` and `Result` distinct domain concepts? **In the architecture docs, yes; in the code, no.** The architecture references a layered model: `evaluation.pipeline.execution` → `EvaluationReport` → `EvaluationResult` → human-readable evidence. No such layered domain exists in the current code. The actual boundary is: `BenchmarkSpec` (contract) → `TaskItem` (unit of work) → `EvidenceSystem.solve()` (execution) → `TaskOutput` (system output) → `BenchmarkRunArtifact` (deterministic result/artifact). There is no `EvaluationReport` class.

3. Is one only an internal execution artifact? **Yes.** `BenchmarkRunArtifact` is the closest analog to a combined result + persisted artifact. It is immutable, content-addressed, and deterministic. The raw per-item scores (`per_item`) and aggregates are embedded within it. There is no separate internal execution artifact distinct from the public result.

4. Does the repository expose duplicate or competing contract roots? **No.** There is exactly one contract root for benchmark results: `BenchmarkRunArtifact`. The evidence data model (`EvidenceObject`) is separate and address-level. The triage evaluation (`EvaluationRun`) is domain-specific and internal. No duplicate or competing root exists.

5. Would renaming create a compatibility issue? **N/A — no rename is required or authorized in this audit.** The current names are stable and used consistently in production code.

6. Should execution remain internal? **Already internal.** `run_benchmark` is imported by `workspace.py` but not re-exported through `medscale.__init__.py`. The public surface is `Benchmark.run()` which returns a `BenchmarkRunArtifact`.

7. Which symbol, if any, is suitable for a stable public surface? **`BenchmarkRunArtifact` is already on the public surface via `medscale.workspace.Benchmark.run()`.** It is frozen, deterministic, serializable, and content-addressed. It is the de facto public result contract for benchmark execution. No additional evaluation result symbol exists yet.

## Unresolved questions

1. Does the repository need a separate `EvaluationReport` / `EvaluationResult` hierarchy, or is `BenchmarkRunArtifact` sufficient for the evaluation domain?
2. If an evaluation engine is ever implemented, should it reuse `BenchmarkRunArtifact` or introduce a new contract?
3. Is there demand for a general-purpose evaluation facade on the `Workspace` object parallel to `Benchmark`?
4. Does `EvaluationRun` in `triage_eval.py` need public/experimental/internal reclassification?
