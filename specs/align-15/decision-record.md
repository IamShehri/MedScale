# ALIGN-15 — Evaluation Engine Boundary Audit Decision Record

## Context

The public-repository alignment plan (Phase 3) assumed an evaluation engine surface at `evaluation.pipeline.execution` with `EvaluationReport` and `EvaluationResult` classes. This audit found no such surface exists on current `main`.

Alternatives considered:

| Alternative | Description | Verdict |
|---|---|---|
| A. Do nothing | Leave registry stale and existing contracts unclassification | Rejected — stale registry misrepresents actual state; blocks correct Phase 3 sequencing |
| B. Audit and reconcile only | Update registry and documents without classification matrix | Rejected — founder requires explicit public/experimental/internal symbol classification |
| C. Audit, classify, reconcile, and define minimum slice | Full audit with classification and implementation-ready slice | Selected |
| D. Implement evaluation engine | Create `medscale.evaluation` package | Not authorized — out of scope for ALIGN-15 |
| E. Rename `BenchmarkRunArtifact` to `EvaluationResult` | Align with Phase 3 naming assumption | Rejected — unnecessary rename; `BenchmarkRunArtifact` is the frozen public result contract; renaming would break the stable `Benchmark.run()` facade |

## Selected boundary

The minimum dependency-complete evaluation capability boundary is the **existing benchmark runner** exposed through `medscale.workspace.Benchmark`:

- Production allowlist: existing `medscale.bench*` modules, `medscale.workspace.Benchmark` methods
- Test allowlist: existing tests under `tests/test_bench_*`
- Protections: no changes to `BenchmarkRunArtifact`, `EvidenceSystem`, `TaskItem`, `TaskOutput`, `BenchmarkSpec`
- Exclusions: no new contracts, no evaluation input contract, no report class, no `EvaluationResult`, no execution state retries, no scheduler, no cloud, no model execution

This slice is:
- offline-capable;
- deterministic;
- serializable;
- content-addressed;
- depends only on existing evidence, dataset, research, and reproducibility contracts;
- already on the public surface via `medscale.Benchmark` and `medscale.Workspace`.

## Rejected boundaries

- A separate `medscale.evaluation` package — rejected because the current benchmark runner is already the evaluation surface; splitting it out before a use case exists would create a duplicate root.
- A new `EvaluationResult` contract — rejected because `BenchmarkRunArtifact` already provides deterministic, versioned, content-addressed results.
- A new `ExecutionState` with retry/partial-failure — rejected because `run_benchmark` succeeds atomically or raises; adding retry semantics would introduce scheduler dependencies absent on `main`.
- Renaming `BenchmarkRunArtifact` to `EvaluationResult` — rejected because it would break the existing stable public facade.

## ADR requirement

```text
ADR NOT REQUIRED
```

The existing accepted ADRs fully determine ownership and serialization:
- ADR-0015 (`modelkit/interfaces.py`) establishes the `EvidenceSystem` plug pattern and `ModelRef` identity.
- ADR-0017 (`evidence/models.py`) freezes the evidence schema.
- ALIGN-14 (`dataset/builder/freeze.py`) establishes immutability, content hashing, and durable snapshot references.

No unresolved architectural decision exists that requires a new ADR for the *current* evaluation boundary. The benchmark runner contracts are already frozen and tested.

A future ADR **would be required** before any of:
- a separate `EvaluationResult` contract is introduced;
- an `ExecutionState` with retry or partial-failure is added;
- a general-purpose evaluation facade is created on `Workspace` parallel to `Benchmark`;
- `BenchmarkRunArtifact` fields are changed;
- a human-readable report class is added to the frozen public surface.

## Deferred decisions

- Whether the repository needs a general-purpose evaluation facade separate from `Benchmark` — deferred; no concrete use case on `main`.
- Whether `BenchmarkRunArtifact` terminology needs expanding in documentation — deferred; not a contract or naming change.
- Whether `EvaluationRun` (triage) needs promotion or reclassification — deferred; domain-specific.
