# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** NOT AUTHORIZED

## Problem

Deterministic dataset splitting already exists in `medscale.dataset.split`, and release metadata already exists in the ALIGN-13 `DatasetReleaseManifest`. However, there is no immutable first-class contract that records the exact assignment of stable record identifiers to splits, binds that assignment to explicit inputs and fingerprints, and produces a stable identity referenceable by release artifacts without changing splitter behavior or release-manifest behavior in the minimum slice.

## Capability

A pure immutable split-assignment freeze value object with deterministic identity.

## Existing capabilities reused

- `DeterministicSplitter`, `SplitResult`, `SplitStrategy`, `split_literature_records` from `medscale.dataset.split`
- `DatasetReleaseManifest` from `medscale.dataset.builder.manifest`

ALIGN-14 does not replace, wrap, or modify these existing capabilities. It adds a freeze record that references them.

## Functional requirements

1. Capture split strategy.
2. Capture seed.
3. Capture source dataset fingerprint.
4. Capture contract/schema version.
5. Capture canonical train membership.
6. Capture canonical validation membership.
7. Capture canonical test membership.
8. Produce a stable split-freeze identity from explicit inputs only.
9. Validate assignment integrity.
10. Provide JSON-compatible deterministic serialization.
11. Support reference from release and benchmark artifacts without changing `DatasetReleaseManifest` in the minimum slice.

## Validation requirements

Reject:
- empty required identifiers;
- non-string record identifiers;
- whitespace-only record identifiers;
- boolean seed values, even though `bool` is a Python subclass of `int`;
- duplicate identifiers within a split;
- identifiers appearing in multiple splits;
- unsupported strategy;
- non-canonical or non-JSON-compatible metadata;
- invalid contract version;
- assignment where train, validation, and test are all empty.

## Deterministic requirements

- identical explicit inputs produce identical freeze identity;
- input iterable order does not change identity;
- mapping insertion order does not change identity;
- timestamps and runtime environment do not affect identity;
- Unicode and case are preserved without normalization.

## Compatibility requirements

- additive evolution only;
- no silent renaming or semantic reinterpretation;
- existing public exports remain unchanged;
- `DatasetReleaseManifest` behavior remains unchanged in the minimum slice;
- no formal release-manifest integration is claimed by the minimum slice.

## Public API

The only proposed new public symbol is `SplitAssignmentFreeze`. Fingerprint computation remains an internal implementation detail of `freeze.py`.

## Contract semantics

- constructor fields: `contract_version`, `source_dataset_fingerprint`, `strategy`, `seed`, `train`, `validation`, `test`
- derived fields: `assignment_count`, `freeze_fingerprint`
- contract version accepts only `split-freeze/v1`
- empty individual splits are allowed
- completely empty assignment is rejected
- seed must be an integer; `True`/`False` are invalid
- identifiers must be non-empty strings with at least one non-whitespace character

## Non-goals

- split computation;
- ingestion;
- storage;
- filesystem writes;
- checksum-file generation;
- export packaging;
- publication;
- CLI changes;
- pipeline orchestration;
- connectors;
- network access;
- model execution;
- FHIR validation;
- timestamps in deterministic identity;
- environment inspection;
- implicit randomness.
