# ALIGN-16 — Contracts

## Stable protocol contracts

These symbols are dependency-free, evaluated as compatibility-worthy, and supported by
accepted ADR or audit evidence.

```text
TextGenerator            interfaces  Public-frozen protocol
SpanExtractor            interfaces  Public-frozen protocol
ModelRef                 interfaces  Public-frozen identity envelope
GenerationRequest        interfaces  Public-frozen request envelope
GenerationResult         interfaces  Public-frozen result envelope
FinishReason             interfaces  Public enum
Span                     interfaces  Public span envelope
```

Current exposure:
- shipped via `medscale.modelkit.__all__`;
- no ML dependency required for import;
- immutable/frozen where applicable.

Recommended class without additional ADR:
- Public or public-frozen.

Other instances of these tutorials:

- `docs/adr/0015-model-agnostic-platform.md` defines the protocol layer as the contract surface.
- `docs/adr/0020-public-api-stability.md` lists `TextGenerator`, `SpanExtractor`, and `ModelRef` as public-frozen.

## Experimental / governance-public contracts

These symbols are dependency-free or schema-only, have tests or manifest/reporting
coverage, but are not explicitly listed in ADR-0020 public-frozen tiers.

```text
TrainingRecipe           recipes     Schema-only; content-addressed identity
DatasetRef               recipes     Dataset identity anchor
AdapterMethod            recipes     Enum for recipe method
ExperimentManifest       manifests   Deterministic canonical-JSON experiment schema
DatasetSnapshot          manifests   Dataset version/snapshot record
RunnerClass              manifests   Pure environment classifier enum
RunnerEnv                manifests   Recorded provenance metadata
MetricSummary            reporting   Deterministic scientific summary
ModelEntry               registry    Frozen immutable fact row
ModelKind                registry    Canonical model-kind enum
Role                     registry    Canonical role enum
REGISTRY                 registry    Immutable governed facts registry
```

Current exposure:
- shipped via `medscale.modelkit.__all__`;
- importing is dependency-safe;
- several have dedicated test files or manifest tests.

Recommended class without additional ADR:
- Experimental or governance-public; promotion to public-frozen requires explicit ADR.

## Internal helpers

These symbols perform I/O, enumeration over global facts, or validation bookkeeping.

```text
detect_runner            manifests   Pure/injectable env classifier helper
read_manifest            manifests   Filesystem I/O helper
write_manifest           manifests   Filesystem I/O helper
summarize_metric         reporting   Pure arithmetic helper
get_entry                registry    Global-fact query helper
eligible_bases           registry    Global-fact query helper
extraction_baselines     registry    Global-fact query helper
validate_registry        registry    Governance-only cross-entry invariant checker
```

Recommended class:
- Internal or internal/governance tooling.

## Nonexistent contracts

The following concepts do not exist on canonical main.

```text
ModelLineage             Does not exist
PromotionDecision        Does not exist
TrainingArtifact         Does not exist
TrainingRun              Does not exist
CheckpointArtifact       Does not exist
AdapterArtifact          Does not exist
DeploymentRecord         Does not exist
InfrastructureSpec       Does not exist
```

## Runtime boundary exclusions

These surfaces are internal, not public reproducibility contracts.

```text
_filesystem paths                  internal storage detail
_backend routing tables            internal
_mutable global state             internal
_secret or credential material     never public
_provider configuration            internal
_deployment state                 internal
_execution request/result pump    internal
_training execution engine        gated; not implemented
```

## Registry status

`REGISTRY` is an immutable governed fact registry, not a mutable runtime registry.

- rows are frozen `ModelEntry` dataclass facts;
- constructor enforcement guarantees Tier-1 generatives for `BASE_CANDIDATE`;
- `validate_registry` is governance tooling;
- provenance metadata `verified_at` is audit timestamping, not scientific identity;
- `source_url` is a citation pointer, not license-verification evidence by itself;
- model revision is stored in `ModelRef`; dataset identity is anchored by
  `DatasetRef.content_sha256`.

## Backend contracts

```text
BackendError                        Exception hierarchy root
BackendMissingDependencyError       Missing optional dependency signal
BackendUnsupportedModelError        Unsupported model signal
GenerationConfig                    Backend configuration dataclass
ModelBackend                        Lightweight availability wrapper
TransformersTextGenerator           Deterministic contract-test adapter
TransformersSpanExtractor           Deterministic contract-test adapter
LlamaCppTextGenerator               Deterministic contract-test adapter
LlamaCppSpanExtractor               Deterministic contract-test adapter
```

Current backend adapters:

```text
TransformersTextGenerator and LlamaCppTextGenerator implement the TextGenerator
protocol shape as deterministic contract-test adapters. They return synthetic
GenerationResult values. They do not load model weights or perform real Transformers
or llama.cpp inference.
```
