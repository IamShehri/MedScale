# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** NOT AUTHORIZED

## Proposed public symbols

| Symbol | Responsibility | Serialization shape | Determinism rules | Validation behavior | Compatibility policy | Why public |
|---|---|---|---|---|---|---|
| `SplitAssignmentFreeze` | Immutable value contract for a frozen split assignment | JSON-compatible payload | Identity excludes timestamps, environment, unordered inputs, derived values, and recursive fingerprint | Reject duplicates, cross-split reuse, invalid seed/strategy/version, whitespace-only identifiers, boolean seeds, and fully empty assignments | Additive only; existing exports unchanged | Release and benchmark consumers must reference an authoritative freeze record |

## Internal-only symbols

- Any helper names used to canonicalize identifier lists or serialize payloads remain internal unless explicitly approved by ADR-0032.
- No standalone public fingerprint helper is proposed. Fingerprint computation remains an internal implementation detail of `freeze.py`.

## Existing reused contracts

- `medscale.dataset.split.SplitStrategy`
- `medscale.dataset.split.SplitResult`
- `medscale.dataset.builder.DatasetReleaseManifest`

These are not altered by ALIGN-14 planning.

## Constructor fields

- `contract_version`
- `source_dataset_fingerprint`
- `strategy`
- `seed`
- `train`
- `validation`
- `test`

## Derived properties

- `assignment_count`
- `freeze_fingerprint`

## Normalization and tuple immutability

- Split membership is represented as canonical sorted immutable tuples of stable string record identifiers.
- Empty individual splits are represented as empty immutable tuples.
- Caller-provided order does not affect identity.
- No competing fingerprint authority is exposed publicly.

## Validation rules

- Every record identifier must be a non-empty string containing at least one non-whitespace character.
- Whitespace-only identifiers are rejected.
- Unicode is preserved.
- Case is preserved.
- Leading and trailing whitespace are not silently removed.
- No case folding or Unicode normalization is performed.
- No duplicate identifier may appear within one split.
- No identifier may appear in more than one split.
- Total assigned count must equal unique assigned identifier count.
- Seed must be an integer. Boolean values are rejected explicitly.
- Strategy must be a supported existing strategy.
- Contract version must be `split-freeze/v1`.
- A completely empty assignment is invalid.
- Payload must remain JSON-compatible.

## Determinism rules

- Identical explicit inputs produce identical freeze identity payloads.
- Split membership ordering is normalized.
- Input iterable order does not change identity during canonicalization.
- Runtime environment does not affect identity.

## Identity payload

The canonical identity payload is:

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
- membership collections are immutable sorted tuples in contract state;
- the hashing payload uses JSON-compatible list representations;
- assignment count is excluded because it is derivable;
- freeze fingerprint is excluded to avoid recursive identity;
- timestamps and runtime metadata are excluded.

## Digest format

The fingerprint reuses `medscale.reproducibility.content_hash` and uses its unchanged output format: 64 lowercase hexadecimal SHA-256 characters.

The `kind` field provides domain separation.

## Contract version

The first contract version uses the fixed literal `split-freeze/v1`. Other values are invalid under the v1 contract.

## Release-integration boundary

ALIGN-14 selects Option A — Standalone freeze contract.

It does not modify `DatasetReleaseManifest`, add a typed manifest field, or define a key inside `validation_summary` or `quality_summary`.

The standalone freeze identity is suitable for future reference by release and benchmark artifacts. Formal release-manifest integration is deferred to a later capability or ADR.

## Proposed builder facade delta

Existing eight public symbols remain unchanged.

Proposed addition after ADR-0032 acceptance and founder approval:

- `SplitAssignmentFreeze`

No public fingerprint helper is included in the proposed facade.

This is a proposed delta, not an authorization.

## Prohibited facade behavior

- No removal or rename of existing public builder symbols.
- No top-level `medscale.dataset` public API change.
- No exposure of evidence, governance, validation, CLI, pipeline, connectors, or runtime surfaces.
