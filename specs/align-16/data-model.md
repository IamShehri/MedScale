# ALIGN-16 — Data Model

## Model identity

```text
ModelRef
```

Status:
- present;
- immutable/frozen;
- deterministic identity fields: `model_id`, `revision`, `quantization`, `backend`;
- validation enforced in constructor.

Ownership:
- `medscale.modelkit.interfaces`

Public class:
- public-frozen protocol support object.

Notes:
- model revision is stored here;
- weight digest pinning is not represented on canonical main;
- provider-neutral identity.

## Generation request/result

```text
GenerationRequest
GenerationResult
FinishReason
```

Status:
- present;
- frozen/deterministic envelopes;
- grammar field is a first-class request member;
- backend unable to enforce grammar must raise.

Ownership:
- `medscale.modelkit.interfaces`

Public class:
- public-frozen.

## Backend adapter

```text
TransformersTextGenerator
TransformersSpanExtractor
LlamaCppTextGenerator
LlamaCppSpanExtractor
```

Status:
- present as deterministic contract-test adapters;
- synthetic output only;
- no real inference, model download, or external API use.

Ownership:
- `medscale.backends.transformers`
- `medscale.backends.llamacpp`

Public class:
- internal/experimental adapter boundary.

## Backend configuration

```text
GenerationConfig
```

Status:
- present;
- frozen dataclass;
- backend_name/temperature/seed/grammar/stop validated.

Ownership:
- `medscale.backends.common`

Public class:
- internal helper.

## Immutable model fact registry

```text
ModelEntry
ModelKind
Role
REGISTRY
get_entry
eligible_bases
extraction_baselines
validate_registry
```

Status:
- present;
- immutable governed facts;
- licence-tier and role enforcement by constructor;
- cross-entry invariant check via `validate_registry`.

Ownership:
- `medscale.modelkit.registry`

Public class:
- `REGISTRY`: governance-public immutable artifact;
- `ModelEntry`, `ModelKind`, `Role`: experimental/governance-public types;
- query/validation helpers: internal/governance tooling.

Notes:
- `verified_at` is provenance timestamping, not scientific identity;
- `source_url` is citation pointer, not standalone license verification;
- no replacement-weight digest stored in registry rows.

## Training recipe

```text
TrainingRecipe
DatasetRef
AdapterMethod
```

Status:
- present;
- schema-only;
- no execution behavior;
- content-addressed identity via `recipe_id`.

Ownership:
- `medscale.modelkit.recipes`

Public class:
- experimental/governance-public.

Notes:
- training execution is gated at T5 and not implemented;
- dataset identity anchored by `DatasetRef.content_sha256`;
- QLoRA base-quantization constraint validated.

## Experiment manifest

```text
ExperimentManifest
DatasetSnapshot
RunnerClass
RunnerEnv
detect_runner
read_manifest
write_manifest
```

Status:
- present;
- deterministic canonical JSON;
- LF-only bytes;
- runner detection is pure and injectable;
- dirty-tree and no-RQ guards enforced.

Ownership:
- `medscale.modelkit.manifests`

Public class:
- `ExperimentManifest`, `DatasetSnapshot`, `RunnerClass`: experimental/governance-public;
- `RunnerEnv`: experimental/internal mixed;
- helpers: internal.

Notes:
- environment metadata is operational provenance only;
- environment metadata does not enter scientific identity on canonical main.

## Metric summary

```text
MetricSummary
summarize_metric
```

Status:
- present;
- deterministic mean ± 95% CI implementation.

Ownership:
- `medscale.modelkit.reporting`

Public class:
- experimental/governance-public.

## BenchmarkRunArtifact

```text
BenchmarkRunArtifact
EvidenceSystem
```

Status:
- present;
- canonical ALIGN-15 evaluation output surface;
- accepts `EvidenceSystem`, not a model execution backend.

Ownership:
- `medscale.bench.run`

Public class:
- public-frozen evaluation artifact.

## Promotion evidence

```text
Does not exist
```

No promotion contract exists on canonical main.

## Model lineage

```text
Does not exist
```

`litdb.lineage` exists as literature-record merge lineage only. It is not a model-lineage module.

## Training artifact

```text
Does not exist
```

No training-artifact contract exists on canonical main.

## Deployment/infrastructure state

```text
Does not exist
```

No deployment record or infrastructure specification contract exists on canonical main.
