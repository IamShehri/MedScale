# ALIGN-15 — Contract Boundaries

## Existing contracts

| Contract | Path | Stability | Status |
|---|---|---|---|
| `BenchmarkSpec` | `src/medscale/bench/spec.py` | public-frozen via `Benchmark` facade | On main, stable |
| `TaskItem` | `src/medscale/bench/tasks.py` | public-frozen via `Benchmark` facade | On main, stable |
| `TaskOutput` | `src/medscale/bench/tasks.py` | public-frozen via `Benchmark` facade | On main, stable |
| `BenchmarkRunArtifact` | `src/medscale/bench/run.py` | public-frozen via `Benchmark` facade | On main, stable |
| `EvidenceSystem` | `src/medscale/bench/run.py` | internal protocol (not in top-level `__init__.py`) | On main, stable |
| `TaskType` | `src/medscale/bench/spec.py` | public-frozen via `Benchmark` facade | On main, stable |
| `SCORER_VERSION` | `src/medscale/bench/scorers.py` | internal constant, referenced in artifact | On main, stable |
| `EvidenceObject` | `src/medscale/evidence/models.py` | public-frozen per ADR-0017 | On main, stable |
| `ResearchSnapshot` | `src/medscale/research/snapshot.py` | public-frozen via `Workspace` facade | On main, stable |
| `EvaluationRun` | `src/medscale/litdb/triage_eval.py` | internal, domain-specific to AI Triage | On main, internal |
| `GoldEvidenceSet` | `src/medscale/bench/tasks.py` | public-frozen via `Benchmark` facade | On main, stable |
| `Statement` | `src/medscale/bench/tasks.py` | public-frozen via `Benchmark` facade | On main, stable |

## Candidate contracts (do not exist yet)

| Candidate | Rationale | Dependency risk |
|---|---|---|
| `EvaluationInput` | Would represent the inputs to a general-purpose evaluation | Would need to reference `EvidenceObject`, `BenchmarkSpec`, dataset state, and optionally model identity. Currently no stable input contract exists for a general evaluation engine because no such engine exists. |
| `EvaluationResult` | Would represent a single-item or aggregate metric outcome | `BenchmarkRunArtifact` already serves as the deterministic result contract for benchmark execution. Introducing a separate `EvaluationResult` without a concrete use case would duplicate semantics and risk incompatibility. |
| `EvaluationReport` | Would human-readable or machine-readable report form of a result | `BenchmarkRunArtifact` is the concrete report format today. A human-readable derived report can be built from it without a new frozen contract. |
| `MetricResult` | Would carry metric name, value, confidence, provenance | Currently embodied in `BenchmarkRunArtifact.per_item` and `.aggregates` dicts. A structured type would add clarity but is not required for current offline execution. |
| `EvaluationReportBundle` | Would aggregate multiple `EvaluationResult`s or `EvaluationRun`s | No concrete use case on `main`. The `BenchmarkRunArtifact` format already supports append-only run artifacts in a `benchmarks/<id>/runs/` directory. |
| `ExecutionState` | Would track pipeline phase, partial failures, retry state | `run_benchmark` currently raises on invalid benchmarks and otherwise succeeds atomically. Partial-failure and retry semantics would require scheduler/retry assumptions outside the current deterministic offline slice. |

## Boundaries

### Frozen (do not modify without ADR)

- `BenchmarkSpec` — frozen via `Benchmark` facade
- `TaskItem` — frozen via `Benchmark` facade
- `TaskOutput` — frozen via `Benchmark` facade
- `BenchmarkRunArtifact` — frozen via `Benchmark` facade
- `EvidenceObject` — frozen per ADR-0017
- `ResearchSnapshot` — frozen via `Workspace` facade
- `GoldEvidenceSet` — frozen via `Benchmark` facade
- `Statement` — frozen via `Benchmark` facade

### Internal (not in top-level `medscale.__init__.py`)

- `EvidenceSystem` protocol
- `SCORER_VERSION`
- `run_benchmark`
- `validate_benchmark`
- `load_benchmark`
- `write_benchmark`
- `benchmark_dir`
- `list_benchmarks`
- `score_item`
- `set_precision`
- `set_recall`
- `provenance_completeness`
- `EvidenceSystem` (protocol in `bench/run.py`)
- `ModelRef`, `GenerationRequest`, `GenerationResult`, `FinishReason`, `TextGenerator`, `Span`, `SpanExtractor` (in `modelkit/interfaces.py`)
- `EvaluationRun`, `compute_metrics`, `evaluate`, `load_goldset`, `write_goldset` (in `litdb/triage_eval.py`)

### Not in scope for this audit

- ADR-0007 extraction adapters
- ADR-0015 model kit interfaces
- ADR-0017 evidence schema — already frozen
- dataset builder contracts — already frozen
- MESC/HuggingFace training or model execution
