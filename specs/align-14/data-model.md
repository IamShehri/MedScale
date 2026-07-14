# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** NOT AUTHORIZED

## Existing concepts

### `SplitResult`

- **Module:** `medscale.dataset.split`
- **Role:** Computes deterministic split assignments from a fixed seed and sorted record identifiers.
- **Status:** Existing public capability; must not be modified or wrapped by ALIGN-14.
- **Reuse:** ALIGN-14 accepts `SplitResult` as the upstream computation artifact when constructing a freeze record from explicit inputs.

### `DatasetReleaseManifest`

- **Module:** `medscale.dataset.builder.manifest`
- **Role:** Records immutable release metadata, including dataset identity, version, fingerprint, release identity, checksums, validation summaries, and prior-release lineage.
- **Status:** Existing ALIGN-13 public capability; must not be duplicated or modified by the minimum ALIGN-14 slice.

## Proposed concept

### Split-assignment freeze object

- **Proposed module:** `medscale.dataset.builder.freeze`
- **Role:** Immutable value contract that identifies exact split assignments and binds them to explicit inputs.
- **Status:** Proposed; pending ADR-0032 acceptance and founder approval.

#### Stored immutable state

- `contract_version`
- `source_dataset_fingerprint`
- `strategy`
- `seed`
- `train`
- `validation`
- `test`

#### Derived state

- `assignment_count`
- `freeze_fingerprint`

#### Identity inputs

| Field | In identity | Notes |
|---|---|---|
| `contract_version` | Yes | Fixed to `split-freeze/v1` in the v1 contract |
| `source_dataset_fingerprint` | Yes | Dataset fingerprint bound to source inputs |
| `strategy` | Yes | Stable existing strategy value |
| `seed` | Yes | Integer seed; booleans are invalid |
| `train` | Yes | Canonical sorted tuple of stable record identifiers |
| `validation` | Yes | Canonical sorted tuple of stable record identifiers |
| `test` | Yes | Canonical sorted tuple of stable record identifiers |

#### Identity exclusions

- `assignment_count`
- `freeze_fingerprint`
- timestamps;
- user identity;
- filesystem paths;
- runtime environment;
- working directory;
- hostname;
- Python version;
- insertion order;
- arbitrary metadata not explicitly approved.

#### Validation and normalization

- Each identifier must be a string, be non-empty, and contain at least one non-whitespace character.
- Whitespace-only identifiers are rejected.
- Unicode is preserved.
- Case is preserved.
- Leading and trailing whitespace are not silently removed.
- No case folding or Unicode normalization is performed.
- Canonical ordering uses Python string lexicographic ordering on the preserved identifier values.
- Empty individual splits are allowed.
- A completely empty assignment is invalid.
- Seed must be an integer; `True` and `False` are rejected.
- Duplicate identifiers within one split are rejected.
- No identifier may appear in more than one split.

#### Relationships

```text
source dataset
    ↓
existing deterministic splitter
    ↓
existing SplitResult
    ↓
standalone SplitAssignmentFreeze
    ↓
future release / benchmark integration
```

The freeze object references the existing deterministic path. It does not change splitter behavior, manifest behavior, or release semantics in the minimum slice.

## Stability rules

- The freeze object is immutable after construction.
- Regeneration from the same explicit inputs must produce equal identity payloads.
- Changes to identity inputs must produce a different identity.
- Release and benchmark artifacts may reference the freeze identity later, but formal release-manifest integration is deferred.
