# ADR-0031 — Deterministic Dataset Contract Ownership and Boundary

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Founder
- **Supersedes:** None
- **Superseded by:** None
- **Related:** ADR-0020, ADR-0030, `specs/public-repository-alignment/phase2-boundary-audit.md`

## Approval record

ADR-0031 was explicitly approved by the Founder on 2026-07-14.

This approval applies only to the architecture decision recorded by this ADR. It does not:

- approve ALIGN-13;
- authorize capability implementation;
- authorize creation of a dataset-builder capability branch;
- authorize source, test, dependency, packaging, CLI, release, model, MESC, or Hugging Face changes.

ALIGN-13 remains a separate founder gate. The exact capability implementation allowlist still requires separate explicit founder approval.

## Context

The canonical v0.2.0 dataset surface is defined by `medscale.dataset.schema`, `medscale.dataset.manifest`,
and the reproducibility primitives in `medscale.reproducibility`. A separate read-only Phase 2 audit
concluded that a finite, deterministic dataset-builder contract slice exists and is viable, but that
an architectural decision record is required before any implementation or public-surface expansion.

This ADR records that boundary and ownership decision only. It does not authorize capability
implementation. ALIGN-13 remains pending explicit founder approval.

## Decision

### 1. Canonical ownership

The first deterministic dataset-builder contract slice is owned by:

- `medscale.dataset.builder.contracts`
- `medscale.dataset.builder.manifest`
- `medscale.dataset.builder.fingerprint`

`medscale.dataset.governance.contracts` and `medscale.evidence.contract` are not canonical public
roots for this slice. Any future consolidation or migration of those roots requires a separate audit
and ADR or an explicit amendment to this ADR.

### 2. Exact proposed public symbols

The complete proposed public surface for the first slice is:

| Symbol | Canonical module |
|---|---|
| `StageResult` | `medscale.dataset.builder.contracts` |
| `StageDefinition` | `medscale.dataset.builder.contracts` |
| `PipelineContext` | `medscale.dataset.builder.contracts` |
| `DatasetReleaseManifest` | `medscale.dataset.builder.manifest` |
| `AuditReport` | `medscale.dataset.builder.manifest` |
| `QualityReport` | `medscale.dataset.builder.manifest` |
| `pipeline_fingerprint` | `medscale.dataset.builder.fingerprint` |
| `context_fingerprint` | `medscale.dataset.builder.fingerprint` |

Existing schema symbols remain owned by `medscale.dataset.schema` and outside this ADR's new
builder-contract ownership decision. ADR-0030 is referenced as the existing Dataset v1 proposal;
this ADR does not alter its status.

| Symbol | Canonical module |
|---|---|
| `DatasetSchema` | `medscale.dataset.schema` |
| `LITERATURE_RECORD_SCHEMA` | `medscale.dataset.schema` |
| `EVIDENCE_OBJECT_SCHEMA` | `medscale.dataset.schema` |
| `BENCHMARK_ITEM_SCHEMA` | `medscale.dataset.schema` |

No other symbols are proposed public in this ADR. Placeholder labels such as
`FingerprintInput`, `ManifestRecord`, `DatasetBinding`, or `DatasetSchema.version`
are not authorized here; they require a separate formal amendment if they later prove
to exist in inspected source.

### 3. Stability classification

This ADR reconciles the proposed surface with ADR-0020 as follows:

- The explicitly listed builder contract, manifest, and fingerprint symbols are proposed
  **data-contract/public module surfaces** under `medscale.dataset.builder`.
- All unlisted names and helpers under these modules remain internal.
- No top-level `medscale.__all__` expansion is authorized.
- Public access is through the explicit `medscale.dataset.builder` subpackage boundary only.
- No accidental public status is created merely because a module can be imported.

### 4. Deterministic serialization and digest policy

The future implementation must use the existing canonical reproducibility primitives only:

- `medscale.reproducibility.canonical_json`
- `medscale.reproducibility.content_hash`

Required rules:

- canonical JSON uses sorted keys, UTF-8 encoding, and fixed compact separators.
- non-ASCII characters are preserved, not escaped.
- digest algorithm is SHA-256 through `content_hash`.
- identical semantic input must produce byte-identical canonical output and identical digest.
- no timestamps, local paths, random identifiers, environment values, host metadata, or unordered
  collection traversal may affect the digest.
- no second canonical-JSON implementation may be introduced in `dataset.builder`.
- changing canonical bytes or digest semantics requires a new ADR and a migration plan.

### 5. Schema ownership

- Existing dataset artifact schemas remain owned by `medscale.dataset.schema` and outside this
  ADR's new builder-contract ownership decision. ADR-0030 is referenced as the existing Dataset v1
  proposal; this ADR does not alter its status.
- `dataset.builder` consumes those schemas but does not redefine them.
- builder manifests may carry an explicit version marker where the inspected contract supports one,
  but the initial capability PR may not mutate existing schema semantics merely to fit candidate
  builder code.
- schema-breaking changes require a new dataset version and a new ADR.

### 6. Competing contract roots

`medscale.dataset.governance.contracts` and `medscale.evidence.contract` are not canonical public
roots for this first slice.

For the initial capability PR:

- do not import them;
- do not export them;
- do not create aliases to them;
- do not migrate them;
- do not delete them from the preserved original workspace;
- do not combine evidence contracts with dataset-builder contracts.

Any future consolidation or migration of competing roots requires a separate audit and ADR or an
explicit amendment to this ADR.

### 7. Compatibility commitment

- additive evolution only for the first public contract version;
- no silent renaming or semantic reinterpretation;
- persisted manifest/digest changes require tolerant readers or an explicit migration;
- determinism is part of compatibility: changing output bytes for unchanged inputs is a contract
  change;
- pre-1.0 changes must comply with ADR-0020 and the repository's versioning policy.

### 8. First capability PR boundary

This proposed ADR records, without approving implementation, the exact implementation and test
allowlist recommended by the merged Phase 2 audit:

Implementation allowlist:

- `src/medscale/dataset/__init__.py`
- `src/medscale/dataset/schema.py`
- `src/medscale/dataset/builder/__init__.py`
- `src/medscale/dataset/builder/contracts.py`
- `src/medscale/dataset/builder/manifest.py`
- `src/medscale/dataset/builder/fingerprint.py`

Test allowlist:

- `tests/test_dataset_builder.py`

Even if this ADR is later accepted, its acceptance alone does not authorize implementation.
ALIGN-13 remains a separate founder gate. The implementation allowlist is provisional and does not
become authorized until the founder explicitly approves the exact capability scope.

### 9. Explicit exclusions

The first capability PR must exclude:

- `src/medscale/dataset/builder/pipeline.py`
- `src/medscale/dataset/builder/release_packager.py`
- `src/medscale/dataset/builder/export_artifacts.py`
- `src/medscale/dataset/builder/audit.py`
- `src/medscale/dataset/builder/layout.py`
- `src/medscale/dataset/builder/errors.py`
- `src/medscale/dataset/connectors/**`
- `src/medscale/dataset/governance/**`
- `src/medscale/validation/**`
- `src/medscale/evidence/contract.py`
- `tests/test_evidence_contract.py`

Also exclude:

- CLI additions or changes;
- top-level facade expansion;
- external APIs;
- network access;
- model execution;
- evaluation execution;
- training;
- orchestration;
- schedulers;
- cloud SDKs;
- MESC implementation or strategy;
- Hugging Face work;
- dependency changes;
- packaging metadata changes;
- version bump;
- tag or release.

### 10. Compliance and enforcement

The future capability PR must include mechanical tests for:

- exact public symbol allowlist;
- contract field/default freeze;
- deterministic manifest serialization;
- stable pipeline and context fingerprints;
- identical-input byte equality;
- malformed-input rejection;
- schema compatibility;
- no runtime metadata in canonical payloads;
- clean-wheel import of the dataset-builder surface;
- no import dependency on evidence contracts, validation, connectors, models, evaluation, or
  execution layers.

## Public / experimental / internal matrix

| Symbol | Module | Classification | Export policy | Compatibility commitment |
|---|---|---|---|---|
| `StageResult` | `medscale.dataset.builder.contracts` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `StageDefinition` | `medscale.dataset.builder.contracts` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `PipelineContext` | `medscale.dataset.builder.contracts` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `DatasetReleaseManifest` | `medscale.dataset.builder.manifest` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `AuditReport` | `medscale.dataset.builder.manifest` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `QualityReport` | `medscale.dataset.builder.manifest` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `pipeline_fingerprint` | `medscale.dataset.builder.fingerprint` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `context_fingerprint` | `medscale.dataset.builder.fingerprint` | Proposed public | `medscale.dataset.builder` subpackage | Additive-only |
| `DatasetSchema` | `medscale.dataset.schema` | Public-frozen | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged |
| `LITERATURE_RECORD_SCHEMA` | `medscale.dataset.schema` | Public-frozen | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged |
| `EVIDENCE_OBJECT_SCHEMA` | `medscale.dataset.schema` | Public-frozen | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged |
| `BENCHMARK_ITEM_SCHEMA` | `medscale.dataset.schema` | Public-frozen | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged | existing `medscale.dataset.schema` contract; ADR-0030 status unchanged |
| All other symbols in `dataset.builder.*` | `medscale.dataset.builder.*` | Internal | not exported | not committed |

### Top-level facade

- `medscale.__all__`: unchanged.
- `medscale.dataset.__all__`: unchanged for this ADR; builder symbols are accessed through the
  explicit subpackage boundary.
- `medscale.dataset.builder.__all__`: to be defined in the capability PR under ADR approval.

## Alternatives considered

1. **Make `dataset.governance.contracts` canonical.**
   Rejected: it introduces a second public contract root before the first slice is stable and
   increases duplication risk without evidence-backed ownership.

2. **Make `evidence.contract` the shared canonical root.**
   Rejected: evidence and dataset contracts have different stability and dependency profiles;
   merging them creates accidental coupling and violates the dataset/evidence boundary.

3. **Expose all candidate builder modules publicly.**
   Rejected: the candidate set includes pipeline, packaging, audit, layout, errors, connectors, and
   governance helpers that are not ready for public commitment; exposing them enlarges the
   compatibility surface prematurely.

4. **Duplicate canonical JSON or hashing inside `dataset.builder`.**
   Rejected: a second canonical-JSON implementation creates divergence risk; the existing
   `medscale.reproducibility` primitives are sufficient and already public-frozen.

5. **Import the whole candidate dataset pipeline in one PR.**
   Rejected: the pipeline, release packager, export artifacts, audit, layout, errors, connectors,
   and governance modules introduce execution, ordering, packaging, and runtime concerns that are
   out of scope for the first deterministic slice.

6. **Leave ownership implicit until implementation.**
   Rejected: implicit ownership creates duplicate roots and compatibility disputes later; the
   boundary must be decided before code is published.

## Consequences

**Positive:**

- exact ownership and symbol surface are recorded before implementation;
- deterministic serialization reuses existing frozen primitives;
- duplicate-contract risk is contained to one public root;
- future capability work has an explicit architectural gate.

**Negative / costs:**

- the ADR adds governance overhead before any capability PR;
- any later change to the approved surface requires a new ADR;
- the provisional allowlist is not an authorization and may await founder review.

## Validation requirements

Before any capability implementation is authorized, the future PR must fresh-run:

- Ruff lint;
- Ruff format;
- strict Mypy;
- full pytest;
- coverage threshold;
- `medscale check`;
- build;
- clean-wheel imports;
- deterministic serialization tests;
- fingerprint stability tests;
- manifest determinism tests;
- malformed-input tests;
- schema compatibility tests;
- public/subpackage export allowlist tests;
- confirmation that top-level facade remains unchanged;
- confirmation of no network/cloud/scheduler/GPU assumptions.

## Migration policy

- duplicate roots: freeze one public root; migrate or reconcile competing roots only under a
  subsequent ADR;
- persisted manifest/digest changes: require tolerant readers or explicit migration;
- schema changes: require a new dataset version and a new ADR;
- public symbol removal/rename: comply with ADR-0020 deprecation policy.

## Relationship to existing ADRs

- ADR-0020 governs public API stability, deprecation, and compatibility tiers.
- ADR-0030 is the existing Dataset v1 versioning and training-artifact proposal; this ADR does
  not alter its Proposed status.
- `phase2-boundary-audit.md` supplies the dependency and boundary evidence for this decision.

## Authorization boundary

This ADR does not authorize capability implementation. ALIGN-13 remains pending explicit founder
approval. No dataset capability branch may be created until this ADR is accepted, merged, and the
exact implementation allowlist receives explicit founder approval.
