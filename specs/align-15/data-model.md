# ALIGN-15 — Evaluation Domain Data Model

## Concepts

The audit identifies six domain concepts relevant to any future evaluation boundary:

| Concept | Current implementation | Notes |
|---|---|---|
| Evaluation input | `BenchmarkSpec` + `TaskItem[]` + frozen `ResearchSnapshot` + `EvidenceObject[]` | Immutable, snapshot-bound. No separate evaluation input contract exists because no general evaluation engine consumes a generic input contract. |
| Execution state | Iteration over sorted `TaskItem`s inside `run_benchmark` | Deterministic, single-threaded (sorted by task_id), no partial results, no retry semantics. |
| Metric output | `TaskOutput` per item → `score_item` → `dict[str, float]` per item | `BenchmarkRunArtifact.per_item` holds per-item metrics. `aggregates` holds unweighted mean per metric. |
| Final result | `BenchmarkRunArtifact` | Immutable, content-addressed (`results_id`), deterministic, serializable. |
| Human-readable report | No separate class | Currently derived from `BenchmarkRunArtifact` by downstream consumers (CLI JSON, replay). A frozen report class is not required for deterministic offline operation. |
| Persisted artifact | `{results_id[:16]}.json` under `benchmarks/<id>/runs/` | Canonical JSON, append-only, content-addressed by `results_id`. |

## Boundary notes

The current code conflates "result" and "artifact" because `BenchmarkRunArtifact` is both the in-memory deterministic result and the persisted JSON form. This is a design choice, not a naming mismatch requiring refactoring.

There is no `EvaluationReport` / `EvaluationResult` hierarchy in the current code. The architecture docs reference these as future concepts; Phase 3 assumed their existence. The audit confirms they do not exist and are not required for the minimum slice.

The triage evaluation (`EvaluationRun` in `litdb/triage_eval.py`) is a separate domain concept with its own frozen dataclass. It is internal, domain-specific, and should not be confused with a general-purpose evaluation result.

## Proposed future slice data model

For the minimum future slice (benchmark runner), the existing data model is already complete and dependency-safe:

```text
Input:
  - BenchmarkSpec (frozen, published)
  - TaskItem[] (frozen, published)
  - EvidenceSystem protocol (internal)
  - ResearchIndex (frozen, read-only)

Execution state:
  - sorted TaskItem iteration
  - per-item TaskOutput
  - per-item dict[str, float] metrics
  - aggregate dict[str, float]

Result:
  - BenchmarkRunArtifact (frozen, content-addressed)
    - per_item: dict[str, dict[str, float]]
    - aggregates: dict[str, float]
    - results_id: content_hash of identity fields

Persisted artifact:
  - canonical JSON of BenchmarkRunArtifact.to_dict()
  - path: benchmarks/<id>/runs/{results_id[:16]}.json
```

No new frozen contract is required.

If a future evaluation engine extends beyond benchmark execution, the following new contracts would be candidates for a follow-up ADR:

- `MetricResult` (name, value, confidence, provenance fields)
- `EvaluationReport` (human-readable, derived from `BenchmarkRunArtifact`)
- `ExecutionState` (retry/partial-failure tracking)

These are **excluded** from the current slice because they introduce scheduler or presentation assumptions not present on `main`.
