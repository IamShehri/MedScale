# ALIGN-16 — Model Runtime and Governance Boundary Decision Record

## Status

```text
ALIGN-16 AUDIT DECISION: CONDITIONAL GO
ADR REQUIRED BEFORE IMPLEMENTATION
```

This decision authorizes documentation and architectural planning only. It does not authorize runtime, training, routing, registry, promotion, lineage, deployment, infrastructure, export, or packaging implementation.

## Context

MedScale already contains:

* provider-neutral model identity and generation/extraction protocol contracts;
* deterministic request and result envelopes;
* schema-only training recipes;
* deterministic experiment manifests;
* an immutable governed model fact registry;
* optional Transformers and llama.cpp backend adapters;
* deterministic reporting helpers.

However, the current package boundary is not fully governed:

* `medscale.modelkit` describes a narrow public-frozen protocol surface;
* `modelkit.__all__` exports a wider set of registry, manifest, recipe, runner, and reporting symbols;
* promotion, model lineage, training-run, checkpoint, adapter-artifact, deployment, and infrastructure contracts do not exist;
* ownership overlap remains between `modelkit.reporting`, `bench.scorers`, and `BenchmarkRunArtifact`.

## Repository findings

### Stable protocol boundary

The following contracts are suitable to remain stable public contracts:

* `TextGenerator`
* `SpanExtractor`
* `ModelRef`
* `GenerationRequest`
* `GenerationResult`
* `FinishReason`
* `Span`

They are provider-neutral, dependency-safe, deterministic at the contract layer, and do not themselves load models or execute infrastructure.

### Optional backend boundary

The repository contains:

* `TransformersTextGenerator`
* `TransformersSpanExtractor`
* `LlamaCppTextGenerator`
* `LlamaCppSpanExtractor`

These currently provide deterministic protocol-contract behavior and synthetic results.

They do not:

* load model weights;
* download models;
* perform real Transformers inference;
* perform real llama.cpp inference;
* prove production runtime capability.

Optional backend installation and import safety are distinct from real inference.

### Model registry boundary

`REGISTRY` is an immutable, code-reviewed model fact registry.

It is not:

* a mutable runtime registry;
* a deployment registry;
* a provider discovery service;
* a promotion state store.

Its wider public compatibility status remains unresolved.

### Training boundary

`TrainingRecipe` is a deterministic schema and does not execute training.

No canonical contracts currently exist for:

* `TrainingRun`;
* `TrainingArtifact`;
* `CheckpointArtifact`;
* `AdapterArtifact`.

Training execution remains deferred and unauthorized.

### Lineage and promotion boundary

`src/medscale/litdb/lineage.py` governs literature-record lineage, not model lineage.

The following model-governance concepts do not exist on canonical `main`:

* `ModelLineage`;
* `PromotionDecision`;
* `DeploymentRecord`;
* `InfrastructureSpec`.

They must not be invented without a separately accepted architectural decision.

### Evaluation boundary

ALIGN-15 remains authoritative:

> Evaluation consumes stable model identity and outputs. Evaluation does not own provider execution, routing, credentials, or deployment state.

`BenchmarkRunArtifact` remains the canonical benchmark-result artifact.

## Selected boundary

1. Keep model identity and protocol envelopes provider-neutral and stable.
2. Keep runtime orchestration, routing, credentials, and deployment state internal.
3. Keep optional backend adapters isolated from the core dependency set.
4. Treat current backend implementations as contract adapters, not production inference engines.
5. Treat the model registry as immutable governance data, not runtime mutable state.
6. Treat recipes and manifests as schemas, not execution systems.
7. Preserve the ALIGN-15 evaluation/runtime separation.
8. Do not create promotion, lineage, training-artifact, or infrastructure contracts before an ADR.
9. Do not change the current public export surface during ALIGN-16.

## Alternatives rejected

### Treat all `modelkit.__all__` symbols as public-frozen

Rejected because package exposure alone does not prove an intended long-term compatibility commitment, and the package documentation describes a narrower frozen surface.

### Remove wider exports immediately

Rejected because ALIGN-16 is documentation-only and export removal could be a breaking API change.

### Treat `REGISTRY` as a runtime registry

Rejected because it is an immutable tuple of governed model facts and performs no runtime discovery, deployment, or mutation.

### Treat optional backend tests as real inference validation

Rejected because current adapters return synthetic deterministic results and do not load model weights.

### Introduce placeholder promotion and lineage contracts

Rejected because their ownership, versioning, evidence dependencies, and compatibility semantics are unresolved.

### Put runtime configuration inside evaluation contracts

Rejected because provider credentials, routing, retry policy, and deployment state do not belong in deterministic scientific evaluation artifacts.

## ADR requirement

```text
ADR REQUIRED BEFORE IMPLEMENTATION
```

The future ADR must resolve:

1. the exact stable `medscale.modelkit` public allowlist;
2. the meaning and compatibility status of the wider current `modelkit.__all__`;
3. registry public, governance-public, experimental, and internal boundaries;
4. whether registry query and validation helpers are public API or governance tooling;
5. manifest and recipe versioning and compatibility commitments;
6. ownership of statistical reporting relative to `bench.scorers` and `BenchmarkRunArtifact`;
7. model revision and model-weight digest policy;
8. runtime execution request and result ownership;
9. training-execution boundaries;
10. promotion-decision ownership and required evidence;
11. model-lineage graph semantics;
12. training-run, checkpoint, and adapter-artifact schemas;
13. routing, credentials, deployment, and infrastructure exclusions;
14. migration policy for any accidental or provisional exports.

## Consequences

### Positive

* preserves dependency-safe core installation;
* avoids premature compatibility commitments;
* maintains provider neutrality;
* keeps evaluation artifacts independent from runtime infrastructure;
* prevents placeholder contracts from becoming accidental architecture;
* creates a finite path toward governed runtime work.

### Costs

* model runtime implementation remains blocked;
* promotion and lineage cannot proceed;
* the wider current export surface remains provisional until the ADR;
* real backend inference remains outside the approved scope.

## Deferred work

The following remain separately gated:

* ADR drafting and acceptance;
* public export changes;
* real model inference;
* model downloads;
* training execution;
* runtime routing;
* mutable registries;
* model promotion;
* model lineage;
* checkpoint and adapter artifacts;
* deployment and infrastructure contracts;
* release and publication work.

## Next founder gate

Founder may authorize publication of the completed ALIGN-16 documentation audit.

Runtime or governance implementation remains blocked until:

1. ALIGN-16 is reviewed and merged;
2. a separate ADR-only task is authorized;
3. the ADR is reviewed and accepted;
4. an exact implementation allowlist receives separate founder authorization.
