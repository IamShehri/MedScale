# ADR-0032 — Deterministic Dataset Split-Assignment Freeze Contract

- **Status:** Accepted
- **Date:** 2026-07-15
- **Deciders:** Founder
- **Supersedes:** None
- **Superseded by:** None
- **Related:** ADR-0020, ADR-0030, ADR-0031, `specs/public-repository-alignment/phase2-boundary-audit.md`

## Approval record

Founder accepted ADR-0032 after a full read-only governance re-review.

Governance re-review result: APPROVE WITH NON-BLOCKING NOTES

Acceptance authorizes preparation of an implementation task only. Production implementation remains separately gated.

This ADR does not authorize ALIGN-14 implementation. ALIGN-14 remains a separate founder gate.

## Context

Deterministic dataset splitting is already implemented in `medscale.dataset.split`. Release metadata is already implemented in `medscale.dataset.builder.DatasetReleaseManifest`. The ALIGN-13 capability PR established the builder contract, manifest, and fingerprint foundation.

What is missing is an immutable first-class contract that records the exact assignment of stable record identifiers to splits, binds that assignment to explicit inputs and fingerprints, and produces a stable identity suitable for possible future reference by release or benchmark artifacts without changing splitter behavior or release-manifest behavior in the minimum slice.

## Decision

### 1. Standalone freeze contract (Option A)

ALIGN-14 selects **Option A — Standalone freeze contract**.

The minimum slice creates and identifies an immutable split-assignment freeze value object only.

It does not add a typed field to `DatasetReleaseManifest`.

It does not define a convention for embedding the freeze identity into `validation_summary`, `quality_summary`, or any other existing manifest mapping.

Formal release-manifest integration is deferred to a later capability or ADR.

The standalone freeze identity is designed for possible future reference by release or benchmark artifacts, but formal integration is outside the minimum ALIGN-14 slice.

### 2. Reuse the existing deterministic splitter

`medscale.dataset.split.DeterministicSplitter`, `SplitResult`, `SplitStrategy`, and `split_literature_records` remain the canonical split computation surface. ALIGN-14 does not reimplement, wrap, or modify this splitter.

### 3. Reuse the existing release manifest

`medscale.dataset.builder.DatasetReleaseManifest` remains the canonical release metadata surface. ALIGN-14 does not duplicate or modify it in the minimum slice.

### 4. Immutable value contract, not lifecycle engine

ALIGN-14 introduces an immutable split-assignment freeze value object only. No mutable state machine, filesystem watcher, workflow engine, or runtime lifecycle is introduced.

### 5. Canonical membership representation

Split membership is represented as canonical sorted immutable tuples of stable string record identifiers. This representation is deterministic, JSON-compatible, and order-independent with respect to input iteration.

Empty individual splits are represented as empty immutable tuples.

### 6. Empty-assignment semantics

Empty individual splits are allowed.

A completely empty assignment is invalid. The contract must reject the state where `train`, `validation`, and `test` are all empty.

### 7. Cross-split uniqueness

No identifier may appear in more than one split. Duplicate identifiers within a split are rejected by validation.

### 8. Identifier and seed validation

Each identifier must be a non-empty string containing at least one non-whitespace character. Whitespace-only identifiers are rejected. Identifier values are preserved exactly: Unicode is preserved, case is preserved, and no normalization is performed.

The seed must be an integer. Boolean values are rejected explicitly.

### 9. Deterministic identity payload

Freeze identity is computed from explicit inputs only:

- `contract_version`
- `source_dataset_fingerprint`
- `strategy`
- `seed`
- `train_identifiers` (canonical sorted immutable tuple)
- `validation_identifiers` (canonical sorted immutable tuple)
- `test_identifiers` (canonical sorted immutable tuple)

No timestamps, user identity, filesystem paths, runtime environment, working directory, hostname, Python version, insertion order, or arbitrary metadata are included in identity.

The canonical identity payload is domain-separated by a stable `kind` field:

```json
{
  "kind": "medscale.dataset.split_assignment_freeze",
  "contract_version": "split-freeze/v1",
  "source_dataset_fingerprint": "<value>",
  "strategy": "<stable strategy value>",
  "seed": 42,
  "train": ["<sorted identifiers>"],
  "validation": ["<sorted identifiers>"],
  "test": ["<sorted identifiers>"]
}
```

Rules:

- keys are stable;
- the membership collections are immutable sorted tuples in contract state;
- the hashing payload uses JSON-compatible list representations;
- caller-provided order does not affect identity;
- timestamps and runtime metadata are excluded;
- assignment count is excluded because it is derivable;
- freeze fingerprint is excluded to avoid recursive identity.

### 10. Computed fingerprint authority

`SplitAssignmentFreeze` does not accept or store a caller-provided fingerprint field.

It exposes one computed, read-only property:

```python
freeze_fingerprint: str
```

This property is derived from the normalized immutable contract state.

There is no second stored fingerprint and no independent public helper that could disagree with the object.

The computed fingerprint is an internal implementation detail of `freeze.py`. No standalone public fingerprint helper is proposed.

### 11. Canonical hashing

Freeze identity reuses the repository's `medscale.reproducibility.content_hash` primitive.

The fingerprint format is the unchanged output format of `content_hash`: 64 lowercase hexadecimal SHA-256 characters.

### 12. Contract version

The first contract version uses the fixed literal:

```text
split-freeze/v1
```

Changing this literal defines a different identity contract and requires a future compatibility decision.

### 13. Exact public API

The only proposed new public symbol is:

```text
SplitAssignmentFreeze
```

No existing public symbol is removed or renamed.

Proposed builder facade delta after acceptance:

```text
existing eight symbols
+ SplitAssignmentFreeze
```

### 14. Constructor and derived state

Constructor state:

- `contract_version`
- `source_dataset_fingerprint`
- `strategy`
- `seed`
- `train`
- `validation`
- `test`

Derived state:

- `assignment_count`
- `freeze_fingerprint`

### 15. Exact maximum implementation scope

The implementation allowlist is:

- `src/medscale/dataset/builder/freeze.py`
- `src/medscale/dataset/builder/__init__.py`
- `tests/test_dataset_freeze.py`

Any expansion beyond this boundary requires a new founder scope decision.

### 16. Prohibited runtime effects

The proposed freeze contract must not perform:

- filesystem reads or writes;
- checksum-file creation;
- network access;
- subprocess execution;
- CLI mutation;
- storage access;
- publication;
- ingestion;
- model execution;
- FHIR validation;
- runtime timestamp generation;
- environment inspection;
- implicit randomness.

It may only validate, normalize, freeze, serialize, and fingerprint explicit inputs.

## Consequences

**Positive**

- closes the gap between deterministic splitting and immutable release artifacts;
- enables citation-stable dataset references without changing existing splitter or manifest behavior;
- preserves the repository's reproducibility-first and evidence-first model;
- limits compatibility surface to a narrow additive facade delta.

**Negative / costs**

- adds governance overhead before implementation;
- any later change to the approved surface requires a new ADR;
- the proposed allowlist is not an authorization and awaits founder review.

## Alternatives considered

1. **Extend `DatasetReleaseManifest` with a typed freeze field.** Rejected: it exceeds the three-file boundary and requires separate scope authorization.
2. **Embed freeze identity in an existing manifest mapping field.** Rejected: it implies informal coupling to release metadata and is unnecessary in the minimum slice.
3. **Duplicate the existing splitter under `dataset.builder`.** Rejected: it duplicates tested behavior and expands scope unnecessarily.
4. **Duplicate `DatasetReleaseManifest` semantics in the freeze contract.** Rejected: the manifest already covers release metadata; the freeze contract adds only split-assignment identity.
5. **Introduce a mutable freeze lifecycle engine.** Rejected: mutable state conflicts with the repository's deterministic, immutable-value model and ADR-0031.
6. **Include timestamps in freeze identity for audit trails.** Rejected: timestamps destroy reproducibility and are already captured in release metadata.
7. **Expand scope to connectors, storage, or export packaging.** Rejected: outside the three-file boundary and not supported by current evidence.

## Compliance

- deterministic identity inputs are explicit and finite;
- canonical JSON and SHA-256 digest policy reuse `medscale.reproducibility` primitives;
- no duplicate public contract roots are introduced;
- future implementation must pass repository-wide ruff, format, mypy, pytest, coverage, `medscale check`, clean-wheel import, and post-merge CI/CodeQL/Optional Extras verification.

## Authorization boundary

This ADR does not authorize production implementation. ALIGN-14 remains pending explicit founder approval. The accepted ADR authorizes preparation of an implementation task only. No capability branch, commit, push, PR, merge, or runtime change may be created until the exact three-file implementation allowlist receives separate founder authorization.
