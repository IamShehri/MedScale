# ALIGN-16 — Model Runtime and Governance Boundary Acceptance Record

## Decision

```text
ALIGN-16 AUDIT DECISION: CONDITIONAL GO
ADR REQUIRED BEFORE IMPLEMENTATION
```

The audit is complete as a documentation and architecture-boundary exercise.

This decision does not authorize:

* model runtime implementation;
* real model inference;
* model downloads;
* training execution;
* routing;
* registry mutation;
* promotion;
* model lineage;
* checkpoint or adapter artifacts;
* deployment or infrastructure contracts;
* public export changes;
* ADR creation or acceptance;
* release or publication.

## Canonical baseline

```text
Repository: IamShehri/MedScale
Canonical branch: main
Baseline SHA: 3132de8789badead5a6f554a71dbaea559fe2233
```

This baseline includes the merged ALIGN-15 evaluation-boundary audit.

## Acceptance claims and evidence

### Claim 1 — Core installation is dependency-safe

Repository evidence:

* `pyproject.toml` declares no core runtime dependencies.
* Transformers and llama.cpp integrations are optional extras.
* `medscale.backends` imports safely without optional ML dependencies.
* backend modules are shipped in the wheel but do not imply that optional dependencies, model weights, or inference runtimes are installed.

Accepted distinction:

```text
Packaged module
!= installed optional dependency
!= available backend
!= loaded model
!= executed inference
```

### Claim 2 — Stable protocol contracts exist

The following provider-neutral contracts are accepted as the current stable protocol boundary:

* `TextGenerator`
* `SpanExtractor`
* `ModelRef`
* `GenerationRequest`
* `GenerationResult`
* `FinishReason`
* `Span`

They are defined without ML framework dependencies and do not themselves download models, access credentials, or execute infrastructure.

### Claim 3 — Current backend adapters are not real inference engines

The repository contains:

* `TransformersTextGenerator`
* `TransformersSpanExtractor`
* `LlamaCppTextGenerator`
* `LlamaCppSpanExtractor`

These adapters implement the protocol shape and return deterministic synthetic results for contract testing.

They do not:

* load model weights;
* download models;
* execute a Transformers pipeline;
* execute a llama.cpp model;
* prove production inference behavior.

Workflow and test evidence therefore qualifies as:

* core compatibility evidence;
* optional-dependency installation evidence;
* backend protocol-contract evidence;
* not real inference evidence.

### Claim 4 — Optional backend boundaries are isolated

Evidence includes:

* `tests/test_modelkit_backends.py`;
* `.github/workflows/optional-extras.yml`;
* missing-dependency validation helpers;
* import-boundary tests preventing backend dependencies on CLI, research, or dataset layers.

The correct test path is:

```text
tests/test_modelkit_backends.py
```

### Claim 5 — The model registry is immutable governance data

`REGISTRY` is an immutable tuple of frozen `ModelEntry` fact rows.

It is accepted as:

```text
Immutable governed model fact registry
```

It is not:

* a mutable runtime registry;
* a deployment registry;
* a provider discovery service;
* a promotion state store.

Its long-term public compatibility status remains unresolved and must be addressed by the future ADR.

### Claim 6 — Recipes and manifests are schemas, not execution systems

`TrainingRecipe` is schema-only and content-addressed.

`ExperimentManifest` is a deterministic experiment-record schema with canonical serialization and explicit provenance.

Neither contract performs:

* training;
* inference;
* scheduling;
* model downloads;
* deployment;
* infrastructure provisioning.

### Claim 7 — Model promotion and lineage contracts do not exist

The following concepts do not exist on canonical `main`:

* `ModelLineage`
* `PromotionDecision`
* `TrainingRun`
* `TrainingArtifact`
* `CheckpointArtifact`
* `AdapterArtifact`
* `DeploymentRecord`
* `InfrastructureSpec`

`src/medscale/litdb/lineage.py` governs literature-record lineage and must not be represented as model lineage.

### Claim 8 — Evaluation and runtime remain separate

ALIGN-15 remains authoritative:

> Evaluation consumes stable model identity and outputs. Evaluation does not own provider execution, routing, credentials, or deployment state.

`BenchmarkRunArtifact` remains the canonical benchmark-result artifact.

Runtime implementation must not move provider configuration, credentials, routing state, retry policy, or deployment state into deterministic evaluation contracts.

### Claim 9 — The wider modelkit export surface is unresolved

`medscale.modelkit` documents a narrow public-frozen protocol boundary but currently exports additional registry, manifest, recipe, runner, and reporting symbols through `__all__`.

The audit does not:

* declare all current exports public-frozen;
* remove exports;
* modify compatibility commitments;
* authorize a breaking facade change.

This mismatch is a required future ADR topic.

### Claim 10 — Reporting ownership requires an architectural decision

`modelkit.reporting` provides deterministic experiment metric summaries.

`bench.scorers` and `BenchmarkRunArtifact` own benchmark scoring and benchmark-result representation.

The boundary between statistical model-experiment reporting and benchmark/evaluation reporting remains partially unresolved.

No reporting code is moved or reclassified by ALIGN-16.

## Contract classification

### Stable protocol contracts

* `TextGenerator`
* `SpanExtractor`
* `ModelRef`
* `GenerationRequest`
* `GenerationResult`
* `FinishReason`
* `Span`

### Experimental or governance-public contracts

* `TrainingRecipe`
* `DatasetRef`
* `AdapterMethod`
* `ExperimentManifest`
* `DatasetSnapshot`
* `RunnerClass`
* `RunnerEnv`
* `MetricSummary`
* `ModelEntry`
* `ModelKind`
* `Role`
* `REGISTRY`

### Internal helpers and governance tooling

* `detect_runner`
* `read_manifest`
* `write_manifest`
* `summarize_metric`
* `get_entry`
* `eligible_bases`
* `extraction_baselines`
* `validate_registry`

These classifications are audit recommendations only. ALIGN-16 does not change actual exports.

## Minimum future slice

A future dependency-safe governance slice may include:

* provider-neutral identity and protocol envelopes;
* deterministic immutable registry facts;
* deterministic schema-only training recipes;
* deterministic experiment manifests;
* explicit evaluation evidence references;
* offline validation and serialization tests.

The future slice must exclude:

* model weight loading;
* model downloads;
* network APIs;
* credentials;
* GPU requirements;
* schedulers;
* mutable global registries;
* runtime routing;
* real inference;
* training execution;
* deployment and infrastructure provisioning.

## ADR requirement

```text
ADR REQUIRED BEFORE IMPLEMENTATION
```

The future ADR must resolve:

1. the exact stable `medscale.modelkit` public allowlist;
2. compatibility status of the wider current `modelkit.__all__`;
3. registry public, governance-public, experimental, and internal boundaries;
4. helper-function exposure;
5. manifest and recipe versioning commitments;
6. reporting ownership relative to `bench.scorers` and `BenchmarkRunArtifact`;
7. model revision and weight-digest identity policy;
8. runtime request and result ownership;
9. training-execution boundaries;
10. promotion decision ownership and evidence requirements;
11. model-lineage semantics;
12. training-run, checkpoint, and adapter-artifact schemas;
13. routing, credentials, deployment, and infrastructure exclusions;
14. migration policy for accidental or provisional exports.

## Verification boundary

ALIGN-16 is documentation-only.

Applicable gates:

```text
git diff --check
documentation-only path scope
clean post-commit worktree
one commit above canonical main
```

`pytest` is not applicable as a required gate for this Markdown-only audit commit.

Repository-level automated tests may run later after publication, but they do not replace documentation scope verification.

## Safety confirmation

ALIGN-16 introduces no:

* production source change;
* test change;
* workflow change;
* dependency or lockfile change;
* package export change;
* model execution;
* model download;
* training execution;
* ADR;
* release;
* branch cleanup;
* ALIGN-10 closure.

## Next founder gate

Founder may authorize publication of the completed ALIGN-16 documentation audit.

Model-runtime or governance implementation remains blocked until:

1. ALIGN-16 is reviewed and merged;
2. a separate ADR-only task is authorized;
3. the ADR is reviewed and accepted;
4. an exact implementation allowlist receives separate founder authorization.
