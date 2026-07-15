# ALIGN-14 Implementation Task

- **Task status:** Implemented / Merged / Closed

```yaml
task_id: ALIGN-14-IMPLEMENTATION
title: Implement SplitAssignmentFreeze
status: Implemented / Merged / Closed
adr: ADR-0032
scope: Minimum standalone Option A contract
```

## Readiness disclaimer

`Ready for Implementation Authorization` does not mean implementation is currently authorized.

This task document becomes actionable only after a separate explicit founder authorization to implement ALIGN-14 within the accepted three-file boundary.

## Objective

Implement one immutable deterministic dataset split-assignment freeze contract:

```python
SplitAssignmentFreeze
```

This document provides all architecture, validation, ordering, identity, API, immutability, disjointness, and acceptance-guide details required by a later implementation agent without requiring further product or architecture invention.

### Out of scope

- release-manifest integration;
- benchmark-manifest integration;
- snapshot integration;
- CLI support;
- persistence;
- migration logic;
- network or database behavior;
- new hashing primitives;
- additional public helpers.

## Canonical repository evidence

The accepted ADR-0032 and this task were prepared from direct `origin/main` inspection of the following canonical repository artifacts. Do not broaden the implementation boundary without explicit founder authorization.

### Public facade and package exports

- `origin/main:src/medscale/__init__.py`
- `origin/main:src/medscale/dataset/__init__.py`
- `origin/main:src/medscale/dataset/builder/__init__.py`

Current builder exports on `origin/main`:

```python
__all__ = [
    "AuditReport",
    "DatasetReleaseManifest",
    "PipelineContext",
    "QualityReport",
    "StageDefinition",
    "StageResult",
    "context_fingerprint",
    "pipeline_fingerprint",
]
```

Current builder count: 8.

Expected builder count after implementation: 9.

Expected new symbol: `SplitAssignmentFreeze`.

### Immutable contract conventions

- `origin/main:src/medscale/dataset/builder/contracts.py`

Relevant existing frozen dataclass examples:

- `StageResult`
- `StageDefinition`
- `PipelineContext`

Relevant existing immutable mapping helper:

- `_FrozenMapping`
- `_freeze`
- `_deep_freeze`

Relevant existing validation helpers in `contracts.py`:

- `_validate_identifier`
- `_validate_boolean`
- `_validate_counts`
- `_validate_tuple_members`
- `_validate_mapping`
- `_validate_json_compatible_mapping`
- `_validate_json_scalar`
- `_validate_proportions`

`_validate_identifier` already rejects whitespace-only strings via `name.strip()`. Boolean rejection in `_validate_boolean` is helper-specific; the implementation task must explicitly reject boolean seeds for `seed` even though Python treats `bool` as `int`.

### Hashing and serialization primitives

- `origin/main:src/medscale/reproducibility.py`

Canonical primitives:

```python
canonical_json(obj: Any) -> str
content_hash(obj: Any) -> str
```

`content_hash` returns a 64-character lowercase hexadecimal SHA-256 digest via `canonical_json` then `hashlib.sha256(...).hexdigest()`.

### Existing builder fingerprint helpers

- `origin/main:src/medscale/dataset/builder/fingerprint.py`

Existing helpers:

- `context_fingerprint`
- `pipeline_fingerprint`

These demonstrate deterministic payload construction and delegation to `content_hash`. The new contract must reuse `content_hash` only and must not reuse or duplicate `_freeze` internals from manifest.py or contracts.py for the identity payload; the freeze contract may adopt compatible tuple/mapping representation behavior only where aligned.

### Existing dataset split contracts

- `origin/main:src/medscale/dataset/split.py`

Existing public symbols:

- `DeterministicSplitter`
- `SplitResult`
- `SplitStrategy`
- `split_literature_records`

`SplitResult.seed` is an `int`. The ALIGN-14 contract must extend this semantics to reject boolean values at the public constructor surface.

### Existing dataset manifest contracts

- `origin/main:src/medscale/dataset/manifest.py`
- `origin/main:src/medscale/dataset/builder/manifest.py`

These modules must not be modified by ALIGN-14. Use them only to confirm that deferred integration is architecturally compatible.

### Existing builder tests

- `origin/main:tests/test_dataset_builder.py`

This is the regression backup for existing builder facade and contract behavior. Implementation must keep `test_builder_module_exports_are_exact`, `test_contracts_module_exports_are_exact`, `test_manifest_module_exports_are_exact`, `test_fingerprint_module_exports_are_exact`, `test_placeholder_names_are_not_exported`, all exact-export/placeholders assertions, and all dataclass shape/immutability/mapping tests green.

## Proposed file scope

Use exactly three files:

1. `src/medscale/dataset/builder/freeze.py` — production contract, exported class, and private helpers for validation, normalization, identity payload construction, and fingerprint derivation.
2. `src/medscale/dataset/builder/__init__.py` — additive facade update only.
3. `tests/test_dataset_freeze.py` — focused regression and acceptance tests.

No additions to existing production or test files are permitted beyond the additive facade update in `__init__.py`.

## Public API

The only new public symbol is:

```python
SplitAssignmentFreeze
```

Requirements:

- exported from `medscale.dataset.builder` only;
- current facade count: 8;
- expected facade count after implementation: 9;
- no public `split_assignment_fingerprint`;
- no additional helper exported;
- no unrelated top-level `medscale` facade expansion;
- no expansion into `medscale.dataset.__all__` unless canonical `origin/main` evidence explicitly requires it; current evidence shows `dataset/__init__.py` exports split and manifest symbols but not builder symbols.

## Constructor contract

Implement the exact constructor fields and types accepted in ADR-0032.

Constructor fields:

| Field | Required | Type |
|---|---|---|
| `source_dataset_fingerprint` | Yes | `str` |
| `strategy` | Yes | `SplitStrategy` |
| `seed` | Yes | `int` |
| `train` | Yes | `Sequence[str]` |
| `validation` | Yes | `Sequence[str]` |
| `test` | Yes | `Sequence[str]` |
| `contract_version` | Yes | `str` |

Implementation must reject types, sequence elements, and values that violate the accepted validation rules. Do not rename fields or introduce optional convenience fields.

## Immutable state requirements

- caller-owned mappings and sequences cannot mutate the created value object;
- record identifier collections must be stored as tuples or an equivalent immutable representation;
- the assignment mapping must be exposed indirectly through canonical immutable tuple collections;
- the constructor must normalize mutable inputs to immutable internal state before completion;
- no mutable internal aliases may remain after construction;
- derived properties must be read-only and must not be stored in constructor-provided state.

The implementation must ensure mutating the caller's original `train`/`validation`/`test` after construction does not change the created value object.

## Validation rules

Implement explicit construction-time validation for every rule listed in ADR-0032.

Required checks, with exact required behavior:

| Input | Required behavior | Source |
|---|---|---|
| `seed=True` | Rejected | ADR-0032 §8 |
| `seed=False` | Rejected | ADR-0032 §8 |
| `seed=0` | Accepted | ADR-0032 §8 acceptance |
| negative `seed` | Accepted as an `int` unless the accepted ADR explicitly forbids it | ADR-0032 §8 |
| very large integer `seed` | Accepted | ADR-0032 §8 |
| non-integer `seed` | Rejected | ADR-0032 §8 |
| non-string `strategy` | Rejected | ADR-0032 §9 |
| empty `source_dataset_fingerprint` | Rejected by existing identifier-style validation | ADR-0032 §8 via `_validate_identifier` |
| non-string `source_dataset_fingerprint` | Rejected | ADR-0032 §8 |
| empty split name in mapping | Rejected because split names are fixed constants in constructor | ADR-0032 §5/§8 |
| whitespace-only identifier | Rejected | ADR-0032 §8 |
| empty identifier | Rejected | ADR-0032 §8 |
| non-string identifier | Rejected | ADR-0032 §8 |
| Unicode-only identifier | Accepted | ADR-0032 §8 |
|Identifiers with leading/trailing whitespace | Accepted and preserved | ADR-0032 §8 |
| case differences between equivalent identifiers | Accepted; do not normalize | ADR-0032 §8 |
| duplicate identifiers within one split | Rejected | ADR-0032 §7 |
| duplicate identifiers across splits | Rejected | ADR-0032 §7 |
| empty `train` only | Accepted | ADR-0032 §6 |
| empty `validation` only | Accepted | ADR-0032 §6 |
| empty `test` only | Accepted | ADR-0032 §6 |
| all splits empty | Rejected | ADR-0032 §6 |
| `contract_version="split-freeze/v1"` | Accepted | ADR-0032 §12 |
| unsupported `contract_version` | Rejected | ADR-0032 §12 |

Validation must not trim, case-fold, or Unicode-normalize identifiers.

## Ordering rules

Deterministic ordering rules for internal state, normalization, and fingerprint generation are fixed by the accepted contract:

- sort split names lexicographically when constructing the identity payload mapping keys: `train`, `test`, `validation`;
- sort record identifiers within each split in deterministic lexicographic order;
- sort any top-level identity payload sequences when producing the hashing payload;
- maintain stable key order in the domain-separated identity payload dict;
- do not depend on Python `dict` insertion order for equality across implementation languages; use sorted deterministic payload construction.

## Identity payload

Use the exact accepted domain-separated identity payload.

Payload structure:

```json
{
  "kind": "medscale.dataset.split_assignment_freeze",
  "contract_version": "split-freeze/v1",
  "source_dataset_fingerprint": "<value>",
  "strategy": "<stable strategy string>",
  "seed": 42,
  "train": ["<sorted identifiers>"],
  "validation": ["<sorted identifiers>"],
  "test": ["<sorted identifiers>"]
}
```

Implementation rules:

- `kind` is the fixed literal `medscale.dataset.split_assignment_freeze`;
- `contract_version` is the fixed literal `split-freeze/v1` in this contract version;
- `seed` is encoded as a JSON integer;
- split assignment sequences are encoded as JSON arrays;
- empty individual splits are encoded as empty arrays;
- derived fields such as `assignment_count` and `freeze_fingerprint` are not in the payload.

Stored immutable constructor state and hashing payload representation must be aligned so that two conforming implementations generate the same fingerprint for the same explicit inputs.

## Hashing

Require reuse of the existing repository `content_hash` primitive only.

The implementation must not:

- add a new hash function;
- add a new digest prefix;
- change canonical JSON behavior;
- change Unicode behavior;
- change `content_hash`;
- expose a separate public fingerprint helper.

Fingerprint format expected from canonical evidence:

```text
64 lowercase hexadecimal SHA-256 characters
```

## Derived properties

Implement both required derived properties as read-only computed properties:

```python
assignment_count: int
freeze_fingerprint: str
```

Definitions:

- `assignment_count` is the total number of assigned record identifiers across all splits;
- `freeze_fingerprint` is the SHA-256 hex digest computed from the accepted identity payload via `content_hash`;
- both must be computed from immutable state only;
- both must be deterministic;
- both must be read-only;
- both must be excluded from constructor-provided mutable state;
- both must be stable across equivalent input orderings.

Equality is structural through the chosen `frozen=True` dataclass implementation and immutable field normalization. Do not add custom comparison, ordering, ordering helpers, `__repr__` overrides, or serialization behavior unless required by existing repository conventions or the accepted ADR.

## Acceptance tests

Map each accepted ADR binding decision to at least one focused test. Test categories below must be covered by `tests/test_dataset_freeze.py`.

### 1. Exact public API and facade

- The builder facade contains exactly the existing eight exports plus `SplitAssignmentFreeze`.
- No public `split_assignment_fingerprint` helper is exported by `medscale.dataset.builder`.
- No placeholder names from existing repository conventions are introduced under the new module or symbol set.

### 2. Construction

- Valid inputs produce a stable frozen value object.
- `contract_version="split-freeze/v1"` is accepted.
- Unsupported `contract_version` values are rejected.
- Valid `strategy` is accepted.
- Non-string `strategy` is rejected.
- Valid `seed` integers are accepted.

### 3. Immutability

- All public constructor fields are non-mutable after construction.
- Mapped caller-owned lists or dicts mutated after construction do not affect the value object.
- Derived properties cannot be assigned.

### 4. Validation

- `seed=True` is rejected.
- `seed=False` is rejected.
- `seed=0` is accepted.
- Negative `seed` follows the accepted ADR behavior and is not rejected by this contract unless the ADR explicitly required it; current evidence treats negative `seed` as accepted at contract boundary.
- Very large integer `seed` is accepted.
- Non-integer `seed` is rejected.
- Whitespace-only identifier is rejected.
- Empty identifier is rejected.
- Non-string identifier is rejected.
- Unicode-only identifier is accepted.
- Leading and trailing whitespace in otherwise valid identifiers is preserved.
- Case differences are preserved.
- Empty individual splits are accepted.
- All splits empty are rejected.
- Duplicate identifiers within one split are rejected.
- Duplicate identifiers across splits are rejected.

### 5. Empty-split semantics

- `train=[]`, `validation=[]`, `test=[]` together rejected.
- Exactly one empty split accepted.
- Exactly two empty splits accepted.

### 6. Unicode, case, whitespace preservation

- Identifiers are compared and sorted in a manner consistent with `content_hash` Unicode behavior.
- Concrete cases must prove case and Unicode are preserved, not normalized.

### 7. Deterministic ordering

- Inputs with different caller-provided ordering produce equivalent fingerprints.
- Inputs with different internal representation types but equivalent normalized content produce equivalent fingerprints.

### 8. Equivalent-input fingerprint equality

- Two independently constructed values with identical normalized inputs produce identical `freeze_fingerprint` values.

### 9. Material-difference fingerprint inequality

- Semantically different assignments produce different fingerprints.
- Different seeds produce different fingerprints.
- Different `source_dataset_fingerprint` values produce different fingerprints.
- Different `strategy` values produce different fingerprints.

### 10. Assignment count derivation

- `assignment_count` equals the sum of lengths of `train`, `validation`, and `test` as stored in normalized immutable state.
- Changing only empty-split composition does not change count in unexpected ways.

### 11. Fingerprint derivation

- `freeze_fingerprint` equals `content_hash(accepted_payload)`.
- Changing any accepted mutable constructor input changes the fingerprint.
- Changing `assignment_count` externally does not change the fingerprint.

### 12. Fixed-version enforcement

- Version `split-freeze/v1` accepted.
- Any other version string rejected at construction time.

### 13. Regression protection for existing builder symbols

- Existing eight builder exports remain exported from `src/medscale/dataset/builder/__init__.py`.
- Existing exact-test patterns in `tests/test_dataset_builder.py` are protected against accidental regression.
- Placeholder-name exclusion remains enforced for the builder package.

### 14. No release-manifest changes

- `src/medscale/dataset/builder/manifest.py` is not modified.
- `DatasetReleaseManifest` dataclass shape remains unchanged.
- No typed release-manifest freeze field is introduced.
- `DatasetReleaseManifest.__all__` remains unchanged.

## Quality gates

A later implementation agent must execute the repository's actual canonical commands after implementation.

Use at least:

```bash
uv run ruff check .
uv run mypy src
uv run pytest
```

Baseline contextual evidence:

```text
397 passed, 2 skipped
```

This baseline is evidence only; fresh verification is required after implementation.

## Explicit non-goals

Do not:

- add release-manifest integration;
- add benchmark-manifest integration;
- change existing split algorithms;
- change existing dataset generation code;
- add CLI commands;
- add persistence or migration logic;
- add a new ADR;
- perform unrelated refactoring;
- add runtime or third-party dependencies;
- add public helper function exports;
- expand the three-file allowlist;
- modify tests unrelated to the new contract.

## Stop conditions

The later implementation agent must stop and report rather than invent a decision if:

- canonical `origin/main` evidence contradicts the accepted contract;
- `content_hash` cannot support the specified payload without modification;
- the exact facade location differs materially from the accepted package on `origin/main`;
- implementation requires release-manifest changes;
- an additional public symbol appears necessary;
- a validation rule is contradictory in the accepted package;
- the baseline test suite is already failing before implementation begins.

## Required implementation report

After implementation, the responsible author must report:

1. Files changed.
2. Contract implemented, including exact constructor fields and derived properties.
3. Validation behavior for all accepted edge cases.
4. Exact identity payload structure and deterministic ordering rules used.
5. Fingerprint determinism evidence: identical-input stability and materially-different-input inequality.
6. Public facade before and after change.
7. Focused test results for `tests/test_dataset_freeze.py`.
8. Full quality-gate results for `ruff`, `mypy`, and `pytest`.
9. Confirmation that release manifests and existing builder contracts were not modified.
10. `git status` output demonstrating no unintended scope expansion.
11. Any deviations from this task or unresolved issues.
