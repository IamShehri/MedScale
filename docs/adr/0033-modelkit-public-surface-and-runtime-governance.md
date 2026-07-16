# ADR-0033 — ModelKit Public Surface and Runtime Governance Boundary

- **Status:** Accepted
- **Date:** 2026-07-15
- **Deciders:** Founder
- **Supersedes:** None
- **Superseded by:** None
- **Related:** ADR-0015, ADR-0020, ALIGN-15, ALIGN-16

## Approval record

Founder accepted ADR-0033 on 2026-07-15 after completion of the ALIGN-17 read-only preflight and full semantic content review.

Content review result: PASS.

Acceptance establishes the architectural governance decision recorded in this ADR and authorizes preparation of a separately scoped implementation or migration task only.

Acceptance does not authorize source-code changes, export changes, tests, runtime execution, model downloads, training, routing, registry mutation, promotion, lineage, deployment, infrastructure, release, or publication.

## Context

ADR-0015 established `medscale.modelkit` as the AI-Infrastructure layer's contract surface and introduced the core protocol objects. ADR-0020 bound public-frozen, data-contract, CLI-stable, and internal tiers under a written stability policy. Together, those decisions freeze the package's module topology and the three protocol objects they explicitly name, but they leave the wider `medscale.modelkit.__all__` surface without a per-symbol compatibility classification.

In addition, ALIGN-16 (the model runtime and governance boundary audit) subsequently identified unresolved ownership between `modelkit.reporting`, `bench.scorers`, and `BenchmarkRunArtifact`, unresolved ModelRef identity semantics for hosted and open-weight models, and the absence of any governance policy for current helper exports that are already exposed through the package facade.

This ADR resolves those items at the governance level without changing any source file, test, export, dependency, package facade, or runtime behavior.

## Decision

1. **Reaffirm existing public-frozen protocols.** ADR-0015 and ADR-0020 already freeze the following contracts as public-frozen: `TextGenerator`, `SpanExtractor`, `ModelRef`.

2. **Freeze request and result envelope contracts.** ADR-0033 proposes a new stable public compatibility commitment for the following dependency-safe envelope types: `GenerationRequest`, `GenerationResult`, `FinishReason`, `Span`. These four contracts were not previously listed in ADR-0020's public-frozen tier; ADR-0033 creates that commitment.

3. **Exact facade classification.** Every current symbol exported by `medscale.modelkit.__all__` is classified without omission in the sections below. No symbol is removed, added, renamed, or semantically repurposed by this ADR.

4. **DatasetRef submodule exposure.** `DatasetRef` is public through `medscale.modelkit.recipes.__all__`. It is not currently re-exported through `medscale.modelkit.__all__`. Its compatibility treatment is evaluated independently from facade exposure.

5. **Registry boundary.** `REGISTRY` is immutable, code-reviewed governance data; `ModelEntry`, `ModelKind`, and `Role` describe governed model facts. The registry is not a mutable runtime registry, provider discovery service, deployment state, or promotion state store. Registry entries and the registry tuple are provisional/governance-public. Query and validation helpers remain compatibility-carried internal tooling.

6. **ModelRef identity policy.** `model_id` identifies the governed model or catalog entry; `model_id` alone does not pin exact weights. `revision` remains `str | None`; publication-grade open-weight or local runs should pin the strongest available immutable revision, and `revision=None` remains supported but represents weaker reproducibility evidence. `quantization` is part of scientific model identity because it can alter outputs. `backend` is execution provenance rather than core scientific model identity; it remains a non-empty field with its current default and remains serialized by current recipes and manifests until a separately authorized migration. Hosted or API models must record the strongest provider model version, snapshot, or revision available, and a missing immutable provider revision must be disclosed as a provenance limitation. ADR-0033 does not introduce a mandatory model-weight digest.

7. **Recipes and manifests.** `TrainingRecipe` and `AdapterMethod` are schema contracts; training execution is not authorized. `ExperimentManifest`, `DatasetSnapshot`, `RunnerClass`, and `RunnerEnv` are deterministic experiment/provenance schemas. These contracts are provisional/governance-public. Recipe and manifest evolution requires explicit format/version compatibility treatment.

8. **Reporting ownership.** `modelkit.reporting` owns provisional general cross-seed statistical arithmetic. `bench.scorers` owns canonical benchmark scoring definitions and scorer-version semantics. `BenchmarkRunArtifact` owns canonical benchmark-result representation. `MetricSummary` is provisional/governance-public; `summarize_metric` is compatibility-carried internal tooling. No function or module moves in this ADR. A later ADR may split or relocate generic reporting utilities.

9. **Compatibility and migration policy.** No current facade export is removed by ADR-0033. Stable contracts cannot be removed or incompatibly changed without a later accepted ADR. Provisional and compatibility-carried exports remain available until a separately accepted migration decision is implemented. No symbol may disappear silently. Removal or rename requires explicit deprecation documentation, changelog and migration guidance, at least one prior released compatibility notice unless an urgent correctness or security exception is separately approved, aliases or shims where practical, clean-wheel import verification, and separately authorized source and test changes. ADR acceptance alone does not execute the migration.

10. **Runtime exclusions.** Real provider execution, model downloads, credentials, retry policies, routing, mutable runtime registries, deployment state, infrastructure provisioning, and training execution remain internal or separately gated. Optional backend adapters remain dependency-isolated. Current deterministic Transformers and llama.cpp adapters are contract-test adapters and are not proof of real inference.

11. **Deferred ADR topics.** Placeholder schemas are prohibited for `ModelLineage`, `PromotionDecision`, `TrainingRun`, `TrainingArtifact`, `CheckpointArtifact`, `AdapterArtifact`, `DeploymentRecord`, and `InfrastructureSpec`. Later dedicated ADRs are required for runtime execution and provider routing; credential and retry governance; mutable runtime registry; promotion ownership and evidence; model-lineage semantics; training and artifact contracts; deployment and infrastructure; mandatory weight digests; execution of export migrations; and future relocation or splitting of reporting utilities.

## Consequences

### Positive

- exact facade classification removes compatibility ambiguity;
- dependency-safe public contracts remain provider-neutral;
- scientific identity is separated from execution provenance;
- the ALIGN-15 evaluation/runtime boundary is preserved;
- accidental architecture through currently exposed helpers is prevented;
- a finite governance path toward runtime work is created.

### Costs

- wider provisional exports remain supported temporarily;
- runtime implementation remains blocked;
- several later ADRs are required;
- future backend separation from `ModelRef` serialization may require migration work;
- ADR governance adds release and compatibility overhead.

## Alternatives considered

1. **Freeze all current facade exports permanently.** Rejected: package exposure is not proof of intended long-term compatibility commitment, and the package documentation currently describes a narrower frozen surface.

2. **Remove helper exports immediately.** Rejected: ADR-0033 governs compatibility only; removal without a separately accepted migration path would be a silent breaking change.

3. **Treat package exposure as proof of stable public intent.** Rejected: `__all__` membership alone does not create a compatibility promise; explicit governance classification is required.

4. **Make `revision` mandatory immediately.** Rejected: hosted providers and legacy reproducibility evidence legitimately use `revision=None`; a mandatory schema change requires compatibility impact assessment and a separate migration.

5. **Add mandatory model-weight digests now.** Rejected: no accepted schema change, compatibility migration, or infrastructure evidence supports immediate enforcement.

6. **Treat `backend` as core scientific model identity permanently.** Rejected: `backend` names the serving implementation and is execution provenance; pinning it as core identity couples scientific reproducibility to serving infrastructure.

7. **Treat `REGISTRY` as a mutable runtime registry.** Rejected: it is an immutable tuple of governed model facts and performs no runtime discovery, deployment, or mutation.

8. **Move reporting code during the ADR task.** Rejected: ADR-0033 is documentation-only; code movement requires a separately authorized implementation allowlist.

9. **Define promotion, lineage, and deployment placeholder contracts now.** Rejected: ownership, versioning, evidence dependencies, and compatibility semantics are unresolved.

10. **Put runtime credentials or routing inside evaluation contracts.** Rejected: provider credentials, routing, retry policy, and deployment state do not belong in deterministic scientific evaluation artifacts.

## Compliance

ADR-0033 is documentation-only. It introduces no:

- source-code change;
- test change;
- package export change;
- optional dependency change;
- inference or training execution;
- runtime routing;
- registry mutation;
- promotion or lineage implementation;
- deployment or infrastructure implementation;
- release or publication.

ALIGN-10 remains pending. Phases 5–7 remain not started. The release gate is unchanged.

## Authorization boundary

Acceptance of ADR-0033 would authorize preparation of an exact implementation or migration task only.

Acceptance would not automatically authorize:

- source-code changes;
- export changes;
- tests;
- runtime execution;
- model downloads;
- training;
- routing;
- promotion;
- lineage;
- deployment;
- infrastructure;
- release or publication.

Any implementation requires a separate founder-approved allowlist and a separate governed branch, commit, pull request, review, and merge sequence.
