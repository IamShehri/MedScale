# ALIGN-17 — ADR Acceptance Criteria and Record

## Decision outcome

```text
ADR-0033 STATUS: ACCEPTED
FOUNDER DECISION DATE: 2026-07-15
IMPLEMENTATION AUTHORIZATION: NOT GRANTED
```

## Acceptance criteria

Satisfied:

- ALIGN-16 audit merged;
- post-merge CI green;
- read-only ADR preflight completed;
- next ADR number verified as 0033;
- bounded ADR strategy selected;
- full ModelKit facade inventory classified;
- `DatasetRef` submodule exposure handled;
- `ModelRef` identity policy resolved;
- reporting ownership resolved;
- migration policy defined;
- runtime and absent systems deferred;
- proposed ADR received complete semantic review;
- founder explicitly accepted ADR-0033;
- acceptance-record review passed;
- no implementation occurred.

## Stable facade record

```text
FinishReason
GenerationRequest
GenerationResult
ModelRef
Span
SpanExtractor
TextGenerator
```

## Provisional/governance-public facade record

```text
REGISTRY
AdapterMethod
DatasetSnapshot
ExperimentManifest
MetricSummary
ModelEntry
ModelKind
Role
RunnerClass
RunnerEnv
TrainingRecipe
```

## Compatibility-carried internal helpers

```text
detect_runner
eligible_bases
extraction_baselines
get_entry
read_manifest
summarize_metric
validate_registry
write_manifest
```

## Submodule-only record

```text
DatasetRef: provisional submodule-public through medscale.modelkit.recipes; not re-exported by medscale.modelkit.
```

## Verification applicability

```text
git diff --check: required
scope gate: required
semantic review: required
pytest: not applicable to documentation-only changes
```

## Preserved project gates

```text
ALIGN-10: pending
Phases 5–7: not started
Release gate: unchanged
Model runtime implementation: blocked
```

## Non-authorization statement

This record does not authorize code, exports, tests, runtime work, migration execution, release, or publication.

No ALIGN-17 merge commit or PR number exists yet.
