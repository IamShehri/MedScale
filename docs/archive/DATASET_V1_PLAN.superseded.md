# Dataset v1 — Architecture Plan (Revised)
## Phase: Dataset Foundation
## Status: PROPOSED — NO REPOSITORY CHANGES
## Boundary: Stop after planning. No code. No commits. No training. No Colab. No HF release. No ADR merge.

M3 is complete and verified on `main`.
Current verified state:
- v0.1.0 released
- M1 complete
- M2 complete
- M3 complete
- All verification gates green: `ruff check .`, `mypy src tests`, `pytest`
- Replay framework operational

This document is detailed enough for another engineer to implement Dataset v1 without making architectural decisions.

---

## 1. Repository Audit — Existing Assets To Reuse

### 1.1 Core primitives
- **`medscale.reproducibility`**
  - `canonical_json(obj)` — sorted-keys compact JSON for deterministic serialization.
  - `content_hash(obj)` — SHA-256 over canonical JSON, used for content-derived identity.
  - `set_global_seed(seed)` — explicit seeding for determinism.
- **`medscale.provenance`**
  - `SourceAPI`, `RetrievalStatus`, `Provenance`, `validate_timestamp`.
  - `raw_response_sha256` is already auditable and type-checked.
- **`medscale.evidence`**
  - `StudyType`, `ExtractionMethod`, `VerificationState`, `EvidenceObject`.
  - `evidence_id` is content-derived via `content_hash`.
  - Verification state machine is frozen.

### 1.2 Research framework
- **`medscale.research.snapshot`**
  - `capture_snapshot` / `ResearchSnapshot` provides git_sha validation and canonical serialization for research artifacts.
  - **Dataset v1 must NOT depend on `medscale.research`.** The dataset layer is foundational and must not create upward dependencies. The plan defines a lightweight `DatasetSnapshot` concept in §1.3 instead.

### 1.3 Snapshot concept for Dataset v1
- **`DatasetSnapshot`** (concept only; to be defined in `medscale.dataset.snapshot` or `medscale.dataset.manifest` during implementation)
  - A frozen dataclass carrying only the immutable metadata required for dataset reproducibility:
    - `dataset_id`
    - `dataset_version`
    - `git_sha`
    - `software_version`
    - `created_at`
    - `fingerprint`
  - Populated from explicit CLI inputs (`--git-sha`, `--software-version`, `--created-at`); never from implicit runtime calls.
  - This preserves the same contract as `ResearchSnapshot` without coupling the dataset layer to the research layer.

### 1.4 Benchmark and CLI framework
- **`medscale.bench`**
  - `spec.py`, `run.py`, `store.py`, `validate.py`, `tasks/` package.
  - Uses frozen dataclasses, content hashing, manifest-style persistence, and deterministic replay.
- **`medscale.cli.bench.py`**
  - argparse-based command dispatcher under the `bench` namespace.
  - `dataset` CLI should live under `medscale.cli.dataset` and mirror the same command pattern: `init`, `manifest`, `validate`, `freeze`, `audit`.

### 1.5 Existing Dataset package
- **`src/medscale/dataset/` already exists and provides:**
  - `DatasetManifest` frozen dataclass
  - `compute_dataset_manifest`
  - `write_manifest`
  - `DatasetSchema` bundle with `LITERATURE_RECORD_SCHEMA`, `EVIDENCE_OBJECT_SCHEMA`, `BENCHMARK_ITEM_SCHEMA`
  - `DatasetValidationReport` + `ValidationIssue`
  - `validate_dataset` (read-only, fails loudly)
  - `DeterministicSplitter`, `SplitStrategy`
  - `split_literature_records`
  - `deterministic_hash_split` compat shim
  - `generate.py` with deterministic corpus-to-dataset conversion
  - `compat.py`, `licenses.py`
- **This package is the correct implementation surface.** Do not duplicate or rename it.

### 1.6 Storage layout
- **`data/litdb/`** is the current live workspace root.
- **`src/medscale/_runtime.py`** provides `git_sha()` and `utc_now()`, but the project prefers **explicit inputs** for all timestamps and SHAs.
- `medscale.reproducibility` and `medscale.dataset` primitives encode the hashing policy.

### 1.7 Tests that exercise adjacent behavior
- `tests/test_dataset_manifest.py`
- `tests/test_dataset_split.py`
- `tests/test_dataset_validation.py`
- `tests/test_dataset_cli.py`
- `tests/test_bench_replay.py`
- `tests/test_bench_tasks.py`

### 1.8 Documentation assets to align with
- `docs/adr/0009-evidence-model.md`
- `docs/adr/0017-identifier-stability-contract.md`
- `docs/adr/0029-benchmark-determinism-and-replay-contract.md`
- `docs/adr/0030-dataset-versioning-and-training-artifact-contract.md`
- `docs/releases/dataset_cards.md`
- `docs/releases/artifact_lifecycle.md`
- `docs/research/experiment_framework.md`

---

## 2. ADR-0030 Summary (Proposed)

**Title:** Dataset Versioning and Training-Artifact Contract

**Status:** Proposed. Do not merge.

**Core declarations:**
- Dataset has deterministic lineage: seed → deterministic split → artifact hash.
- Dataset is immutable after `freeze`; mutations create new dataset IDs via explicit `init`.
- Every dataset version carries a single manifest and checksum tree.
- Dataset manifest is independent from, but sharable with, benchmark manifests.
- `LiteratureRecord` and `EvidenceObject` schemas from `medscale.dataset.schema` remain the source of truth.
- Any incompatible schema change produces a new dataset version and new ADR.

**Canonical checksum layout (aligned with ADR-0030):**
- `checksums/manifest.sha256`
- `checksums/schema.sha256`
- `checksums/train.json.sha256`
- `checksums/validation.json.sha256`
- `checksums/test.json.sha256`

**Non-goals:**
- Dataset v1 does not enforce singular ground-truth label columns.
- Dataset v1 does not dictate training code, optimization, or model architecture.
- Dataset v1 does not create notebooks, Colab links, or HF repos.
- Dataset v1 does not define training manifests; those are deferred to a future ADR.

---

## 3. Dataset Directory Layout

```
data/datasets/
├── README.md
└── {dataset_id}/
    ├── manifest.json               # frozen dataset metadata and identity hashes
    ├── schema.json                  # emitted from DatasetSchema; frozen per version
    ├── README.md                    # human-readable provenance and license summary
    ├── CHANGELOG.md                 # append-only per dataset version only
    ├── checksums/
    │   ├── manifest.sha256
    │   ├── schema.sha256
    │   ├── train.json.sha256
    │   ├── validation.json.sha256
    │   └── test.json.sha256
    ├── splits/
    │   ├── train.json
    │   ├── validation.json
    │   └── test.json
    ├── metadata/
    │   ├── license.json             # SPDX + source scope + redistribution policy
    │   ├── sources.json             # identifiable source fingerprints
    │   └── statistics.json          # deterministic counts from split generation
    ├── licenses/
    │   └── LICENSE.txt              # copied legal text required by included works
    └── statistics/
        ├── class_balance.json       # optional distribution summary
        └── length_distribution.json # optional token/length summaries
```

### File roles and constraints
- **manifest.json** — the frozen contract. Contains: `dataset_id`, `version`, `created_at`, `dataset_snapshot`, `git_sha`, `seed`, `software_version`, `schema_version`, `split_strategy`, `record_count`, `license_summary`, `fingerprint`, and artifact references.
- **schema.json** — emitted once; frozen after `freeze`. Changing schema requires new dataset version.
- **splits/\*** — split membership only. No metadata mutation after freeze.
- **checksums/\*.sha256** — one sibling SHA-256 file per artifact. Validation recomputes and compares byte-for-byte. This is the single canonical checksum layout; no JSON checksum manifest is used.
- **metadata/license.json** — required fields: `spdx_id`, `source_scope`, `redistribution_allowed`, `attribution_required`, `commercial_allowed`. Validation fails if incomplete.
- **licenses/LICENSE.txt** — distributable legal text for training/evaluation redistribution.

---

## 4. Split Strategy

### 4.1 Deterministic assignment via existing primitive

Dataset v1 **must reuse** the existing deterministic split primitive used by MedScale.

**Canonical split identity:**

```python
content_hash(
    {
        "seed": seed,
        "record_id": record_id,
    }
)
```

This guarantees:
- **Consistency with existing tests.** `DeterministicSplitter` and `tests/test_dataset_split.py` already prove same-seed/identical-ID determinism and seed-change divergence using this exact primitive. Reusing it prevents split divergence between the dataset layer and any benchmark or research layer.
- **No duplicate implementations.** There is exactly one place where split determinism is defined: `medscale.dataset.split`.
- **Order independence.** Input record IDs must be sorted before assignment so the split result is identical regardless of input ordering.

**Assignment buckets:**
- `train` when hash bucket < 800
- `validation` when 800 ≤ hash bucket < 900
- `test` when 900 ≤ hash bucket

**Why this is correct:**
- Dependency is minimal and explicit: seed + stable record_id → deterministic byte-identical split.
- `content_hash` uses `canonical_json`, which guarantees stable serialization across machines and Python versions.
- Collision resistance follows from SHA-256; no record is assigned to more than one split.
- The existing implementation already encodes this contract; Dataset v1 does not redefine it.

### 4.2 Handling edge cases
- **Duplicated record IDs:** Fail loudly at split generation step; duplicate IDs indicate upstream ingest failure.
- **Empty dataset:** Reject with `ValidationIssue` on record count; an empty dataset cannot be frozen.
- **License mismatch across split:** Validation aggregates license coverage across all records first, before split generation.
- **Schema version migration:** Not automatic. A new dataset version is created instead; old datasets remain frozen and valid if checksums match.

---

## 5. Dataset Fingerprint

### 5.1 Concept
Dataset v1 introduces a **Dataset Fingerprint** as the canonical identity for downstream consumers.

**Fingerprint inputs:**
- `manifest.json` canonical content
- `schema.json` canonical content
- `splits/train.json`, `splits/validation.json`, `splits/test.json` canonical content
- `metadata/license.json` canonical content
- `metadata/statistics.json` canonical content

**Fingerprint computation:**
```python
fingerprint = content_hash(
    {
        "manifest": canonical_json(manifest),
        "schema": canonical_json(schema),
        "splits": {
            "train": canonical_json(train),
            "validation": canonical_json(validation),
            "test": canonical_json(test),
        },
        "license": canonical_json(license),
        "statistics": canonical_json(statistics),
    }
)
```

**Properties:**
- Fingerprint is deterministic: identical dataset contents → identical fingerprint.
- Any mutation to any included artifact produces a different fingerprint.
- Fingerprint is recorded in `manifest.json` at freeze time and is immutable thereafter.
- Fingerprint is the value benchmark manifests and experiment manifests reference; it is not recomputed by downstream consumers—they compare stored vs. recomputed during validation.

---

## 6. Dataset Versioning Vocabulary

### 6.1 Identities
- **`dataset_id`** — stable human-readable identifier for the dataset collection (e.g., `medscale-lit-dataset-v1`). Format: lowercase ASCII letters, digits, and hyphens only; must start with a letter; regex `^[a-z][a-z0-9-]{3,63}$`; max 63 characters.
- **`dataset_version`** — mutable version string for a specific instantiation of the dataset (e.g., `1.0.0`, `2026-07-13`). Changing any frozen artifact requires a new version.
- **`dataset_fingerprint`** — content-derived SHA-256 identity computed from the canonical contents listed in §5.1. Two dataset versions with identical contents have identical fingerprints; any difference produces a different fingerprint.

### 6.2 Examples
- `dataset_id = "medscale-lit-dataset-v1"`, `dataset_version = "1.0.0"`, `dataset_fingerprint = "a3f2..."` → first frozen release.
- Same `dataset_id`, `dataset_version = "1.0.1"`, `dataset_fingerprint = "b7c4..."` → patched release (e.g., corrected license metadata). Contents changed, so fingerprint changed.
- `dataset_id = "medscale-lit-dataset-v2"`, `dataset_version = "0.1.0"`, `dataset_fingerprint = "c9e1..."` → new dataset ID signals a schema or governance change requiring a new ADR.

### 6.3 Future Dataset v2 evolution
- Dataset v2 is signaled by a new `dataset_id` and a new ADR.
- Dataset v1 artifacts remain frozen and valid; `dataset validate` on v1 continues to pass against v1's own manifest and checksums.
- Benchmark manifests referencing v1 continue to resolve v1 by `dataset_id` + `dataset_version`; they do not silently upgrade to v2.

---

## 7. Checksum Policy

Dataset v1 adopts the **canonical sibling `.sha256` file layout** defined by ADR-0030.

**Files:**
- `checksums/manifest.sha256`
- `checksums/schema.sha256`
- `checksums/train.json.sha256`
- `checksums/validation.json.sha256`
- `checksums/test.json.sha256`

**Content:** each `.sha256` file contains a single lowercase SHA-256 hex digest with no filename prefix, no spaces, no newline ambiguity issues beyond standard trailing newline normalization.

**Validation rule:** for every sibling `.sha256` file, recompute `SHA256` over the corresponding artifact bytes and compare byte-for-byte. Mismatch fails loudly with artifact path, expected digest prefix, actual digest prefix.

**No alternative checksum layout is permitted in v1.** Mixed layouts (`checksums/manifest.json` plus `.sha256` files) are prohibited because they produce audit ambiguity.

---

## 8. Timestamp Policy

- `created_at` is immutable after freeze.
- `freeze` accepts an explicit `--created-at` CLI argument.
- If `--created-at` is omitted, the CLI generates a UTC ISO-8601 timestamp at invocation time and records it in the manifest.
- Once written to `manifest.json`, `created_at` is never overwritten.
- All timestamps must be explicit, timezone-aware ISO-8601 strings. Implicit or naive timestamps are rejected by validation.

**Why this satisfies reproducibility:**
- Explicit inputs remove hidden state from artifact identity. Two freeze invocations with the same inputs and same explicit timestamp produce identical manifests.
- When the timestamp is auto-generated, the user must record it alongside other freeze parameters to enable exact replay. This mirrors the existing MedScale convention that all reproducibility-relevant values are explicit inputs or explicitly recorded outputs.

---

## 9. Path Validation

Every path referenced by the dataset manifest or checksums must resolve inside the dataset root.

Implementations must reject:
- path traversal sequences (`..`)
- absolute paths
- symlinks or normalized paths that escape the dataset directory

Validation failures must be loud and include the offending path and the expected dataset root boundary.

This protects against corrupted or malicious manifests that would otherwise cause checksum validation to read files outside the dataset tree.

---

## 10. Storage Policy

- `data/datasets/` is **gitignored** by default.
- Reproducibility survives local deletion through the combination of:
  - `dataset_id` + `dataset_version` + `dataset_fingerprint` as stable identifiers
  - `checksums/*.sha256` for byte-level integrity verification
  - External artifact storage reference in `manifest.json` (e.g., `storage_uri`) for future remote retrieval
- For v1, `storage_uri` is optional. Implementations may store datasets locally only; the field exists so future distribution mechanisms do not require a manifest schema change.
- No dataset artifact may reference local files outside the dataset root by relative path.

---

## 11. Large-Dataset Architecture

Future implementations must support streaming validation for:
- checksum calculation (streamed SHA-256, not full-file `read_bytes()`)
- manifest validation (field-by-field, not full JSON materialization when unnecessary)
- split verification (line-by-line or chunked JSON parsing for large split files)

Dataset v1 design must not hardcode patterns that assume the entire dataset fits in memory. Validation APIs should accept paths and stream artifacts.

---

## 12. License Governance

Every dataset must define explicit license coverage before freeze.

**Required `metadata/license.json` fields:**
- `spdx_id` — SPDX license identifier
- `source_scope` — list of source categories included (e.g., `["synthetic"]`, `["open_access"]`)
- `redistribution_allowed` — boolean
- `attribution_required` — boolean
- `commercial_allowed` — boolean

**Validation rule:** `freeze` must fail loudly if any record in the dataset lacks license coverage, or if `metadata/license.json` is missing or incomplete.

Dataset v1 is synthetic-first. A record with `source_scope` not including `"synthetic"` requires explicit governance approval before freeze; the validator emits a warning by default and can be configured to error via a future policy flag.

---

## 13. Synthetic-First Governance

Dataset v1 is synthetic-first by policy.

- All records in v1 must carry `source_scope` containing `"synthetic"` in `metadata/license.json`.
- Real-world datasets require future governance approval and a superseding ADR before they may enter a frozen dataset version.
- This policy is enforced at validation time, not by code review alone.

---

## 14. Dataset ID Format

Allowed `dataset_id` format:
- Regex: `^[a-z][a-z0-9-]{3,63}$`
- Must start with a lowercase letter
- May contain lowercase letters, digits, and hyphens
- Maximum 63 characters
- No underscores, no spaces, no uppercase letters

Validation fails loudly on format violation. This prevents filesystem bugs, manifest key inconsistencies, and cross-platform path issues.

---

## 15. CLI Design

**Namespace:** `medscale dataset`

**Dependency rule:** CLI imports only from `medscale.dataset` and uses explicit inputs for git/time. CLI never imports training, Colab, HF, or benchmark execution modules.

### 15.1 `medscale dataset init`

```
medscale dataset init --id <dataset_id> --version <version> \
  --schema-version 1 --seed 42
```

- Creates `data/datasets/{dataset_id}/` with empty split placeholders, skeleton `manifest.json`, `schema.json`, `checksums/*.sha256`, `metadata/`, `licenses/`, `statistics/`.
- Error if directory already exists unless `--force` with matching manifest is confirmed.
- Reuses `DatasetSchema` for schema emission.
- Reuses `DatasetManifest` for manifest typing.

### 15.2 `medscale dataset manifest`

```
medscale dataset manifest --id <dataset_id> --version <version> \
  --records <records.jsonl> --license-summary <summary.json> \
  --git-sha abc1231 --software-version 0.0.0
```

- Reads canonical JSONL records.
- Counts records, validates licenses, writes `manifest.json`.
- Does not mutate split files.
- Error if records contain duplicate IDs, empty licenses, invalid timestamps, or malformed identifiers.

### 15.3 `medscale dataset validate`

```
medscale dataset validate --id <dataset_id> --version <version>
```

- Validates manifest, schema, splits, checksums, path safety, license coverage, synthetic-first policy, and dataset ID format.
- Exits 0 on pass, exits 1 on any validation issue.
- Diagnostic output includes exact field, expected value prefix, actual value prefix, and suggested remediation when unambiguous.

### 15.4 `medscale dataset freeze`

```
medscale dataset freeze --id <dataset_id> --version <version> \
  --scorer-version 1.0 --seed 42 \
  [--created-at "2026-07-13T00:00:00+00:00"]
```

- Reads canonical `manifest.json`, `schema.json`, split files, license text, statistics.
- Computes SHA-256 for every artifact and writes sibling `.sha256` files under `checksums/`.
- Computes `dataset_fingerprint` from canonical contents and writes it into `manifest.json`.
- Validates license coverage across all records; fails loudly if coverage drops below declared bounds.
- Validates `dataset_id` format.
- Validates all manifest paths resolve inside the dataset root.
- Freeze makes the dataset immutable; subsequent mutation requires a new version or new dataset ID.

### 15.5 `medscale dataset audit`

```
medscale dataset audit --id <dataset_id> --version <version>
```

- Recomputes every checksum, fingerprint, and manifest field from persisted artifacts.
- Prints pass/fail per artifact with expected and actual digest prefixes.
- Does not mutate any artifact.
- Intended as the human-readable readback step after freeze.

### 15.6 Error contract
All CLI commands return:
- 0 — success
- 1 — validation failure with diagnostic lines
- 2 — usage/system error

Diagnostics include:
- file path
- field name
- expected value or expected hash prefix
- actual value prefix
- suggested remediation when unambiguous

### 15.7 Intended lifecycle

```
init
↓
manifest
↓
validate
↓
freeze
↓
audit
```

- `init` scaffolds the directory.
- `manifest` writes or previews metadata without mutating splits.
- `validate` checks schema, checksums, splits, paths, licenses, and synthetic-first policy.
- `freeze` writes checksums, fingerprint, and final immutable manifest.
- `audit` recomputes and prints the full integrity readback.

---

## 16. Model Training Contract (Design Only)

Design how Dataset v1 will later connect to model training, experiment directories, and evaluation outputs **without writing training code.**

### 16.1 Boundary
Dataset v1 exposes only structural contracts for later training:

- `dataset_id`
- `dataset_version`
- `dataset_fingerprint`
- `seed`
- `split_assignments` from `splits/{split}.json`
- `statistics/*.json` for distribution summaries
- `metadata/license.json` for usage constraints

### 16.2 Future training manifests
Future training manifests will be specified in a separate ADR after Dataset v1 is complete. Dataset v1 itself does not define `TrainingManifest`, model card fields, metrics fields, parameters schemas, or experiment artifact layouts.

### 16.3 Google Colab boundary
A future Colab notebook imports only from `medscale.dataset`.
- Notebook loads dataset by `dataset_id`/`version` and `seed`.
- Notebook does not mutate `data/datasets/`; experiments write under a separate `data/experiments/` tree.
- Notebook publishes neighbor experiment artifacts, not new dataset versions.

### 16.4 Evaluation output contract
Evaluation outputs are written under `data/experiments/`, never under `data/datasets/`.
Dataset v1 does not validate training or evaluation outputs; it guarantees only dataset-level reproducibility.

---

## 17. Benchmark Compatibility

### 17.1 Linkage protocol
Benchmark manifests reference datasets by three fields:
- `dataset_id`
- `dataset_version`
- `dataset_fingerprint`

### 17.2 Replay validation
`medscale bench replay` must verify that the frozen dataset fingerprint referenced by the benchmark manifest matches the recomputed fingerprint of the dataset currently available at the referenced path. Mismatch fails loudly with the dataset path, stored fingerprint prefix, and recomputed fingerprint prefix.

### 17.3 Benchmark directory layout
```
data/bench/
├── manifests/
│   └── medscale-bench-v1.json
├── specs/
└── runs/
```

Benchmark manifests never mutate dataset artifacts. They reference dataset identity and defer dataset integrity to `medscale dataset validate` and `medscale dataset audit`.

---

## 18. Repository Impact Analysis

### 18.1 New files to create
- `docs/execution/v0.2/DATASET_V1_PLAN.md` — this document
- `docs/execution/v0.2/DATASET_V1_PLAN_REVISED.md` — this revision record
- `data/datasets/README.md` — repo-level dataset registration and governance
- New CLI test file: `tests/test_dataset_freeze.py`
- New architecture test additions in `tests/test_architecture.py`

### 18.2 Files to extend
- `src/medscale/dataset/__init__.py` — add `freeze_dataset`, `compute_dataset_checksums`, `compute_dataset_fingerprint` public APIs after implementation
- `src/medscale/dataset/validate.py` — extend to verify checksum files, path safety, synthetic-first policy, dataset ID format, and license completeness
- `src/medscale/dataset/manifest.py` — add `dataset_snapshot` and `fingerprint` support
- `src/medscale/dataset/snapshot.py` — new lightweight frozen dataclass for dataset snapshot metadata (concept defined here; implementation later)
- `src/medscale/cli/dataset.py` — add `freeze` and `audit` commands
- `tests/test_dataset_manifest.py` — add snapshot + fingerprint + checksum coverage
- `tests/test_dataset_validation.py` — add checksum, path-safety, synthetic-first, dataset-id-format coverage
- `tests/test_dataset_cli.py` — cover the new commands

### 18.3 Files to remove or deprecate
- None in v1 plan.
- `src/medscale/bench/presets/` — confirm removed; if still present, remove before v1.
- Avoid any new package renames; preserve both `medscale.bench.tasks` package and `medscale.dataset` namespace.

### 18.4 Architecture boundaries
- `medscale.dataset` → dependencies: `medscale.reproducibility` only. No dependency on `medscale.research`, `medscale.bench`, `medscale.evidence`, `medscale.litdb`, or `medscale.modelkit`.
- `medscale.cli` → dependencies: `medscale.dataset` only.
- `medscale.litdb`, `medscale.modelkit`, `medscale.evidence`, `medscale.research` → untouched.
- Dataset must not import Colab, HF, training, or benchmark execution code.

### 18.5 Dependency graph (v1-relevant)
```
medscale.reproducibility
    └── medscale.dataset
            └── medscale.cli.dataset
medscale.dataset.schema
    └── medscale.dataset.validate
    └── medscale.dataset.manifest
medscale.dataset.split
    └── medscale.dataset.manifest
```

### 18.6 Public API changes
- Add `freeze_dataset`, `compute_dataset_checksums`, `compute_dataset_fingerprint` to `medscale.dataset`.
- Add `DatasetSnapshot` frozen dataclass to `medscale.dataset`.
- CLI namespace `dataset` gains `freeze` and `audit`.
- No removal, rename, or deprecation of existing public exports.

---

## 19. Testing Plan

### 19.1 Unit tests
- `compute_dataset_manifest`: identical inputs produce identical manifest digest; differs with version, git sha, seed, record ID set change, or created_at change.
- `DeterministicSplitter`: same seed and same ID set produce byte-identical split files; different seed produces different split; reversed input order produces same split.
- `validate_dataset`: missing file, malformed JSON, checksum mismatch, schema mismatch, empty dataset, path traversal, invalid dataset ID format, incomplete license metadata, synthetic-first violation.
- `compute_dataset_checksums`: deterministic output for identical content; tamper detection; ordering is stable.

### 19.2 Integration tests
- End-to-end `dataset init` → `dataset manifest` → `dataset validate` → `dataset freeze` → `dataset audit` → second `dataset validate` passes.
- Re-validate frozen dataset after JSON copy; checksums and fingerprint must still match.
- Cross-version boundary: validate dataset vN accepts frozen vN; validate rejects files changed after freeze.
- Benchmark linkage: benchmark manifest referencing dataset vN passes replay validation only when dataset fingerprint matches.

### 19.3 Architecture tests
- `medscale.dataset` imports do not transitively import `medscale.litdb`, `medscale.modelkit`, `medscale.evidence`, `medscale.research`, training code, Colab, or HF modules.
- CLI imports live only in `medscale.cli.dataset`.
- `DatasetManifest`, `DatasetSchema`, `DatasetValidationReport`, `DatasetSnapshot` remain dataclass-frozen.

### 19.4 Checksum tests
- Tamper with one byte in any artifact after freeze; `freeze` or `validate` must fail with exact path and expected/actual digest.
- Replace a `.sha256` file with stale values from another dataset; fail with diagnostic.
- Verify deterministic ordering of checksum filenames.
- Verify path-traversal entries in checksum manifest are rejected.

### 19.5 Split reproducibility tests
- Generate split with seed 0; recompute with seed 0 on same IDs; byte-identical output.
- Reverse input ID order; same seed; identical split output.
- Increment seed by 1; split must change.
- Duplicate IDs must raise `ValidationIssue`.

### 19.6 Manifest replay tests
- Load frozen manifest; recompute expected checksums from on-disk artifacts; compare to `checksums/*.sha256`.
- Frozen manifest must contain `dataset_id`, `version`, `created_at`, `dataset_snapshot`, `git_sha`, `software_version`, `seed`, `schema_version`, `fingerprint`, and checksum references.
- Mismatch in any of: manifest hash, dataset hash, git SHA, software version, scorer version, seed, fingerprint, path safety, dataset ID format → fail loudly with diagnostic.

### 19.7 Test coverage targets
- Minimum 90% line coverage for `src/medscale/dataset`.
- 100% coverage for CLI happy-path and each failure-mode CLI entry point.
- Each CLI command must have at least one success and one failure test.

---

## 20. Risks and Mitigations

### 20.1 Schema drift
- **Risk:** Future dataset versions silently accept incompatible record shapes.
- **Mitigation:** Freeze `schema.json` at dataset creation; version upgrades require explicit `dataset init` with incremented version. Enforce backward-compatible additions only; never remove required fields without an ADR.

### 20.2 Dataset corruption
- **Risk:** Storage medium or sync layer corrupts files after freeze.
- **Mitigation:** Sibling `.sha256` files enable byte-level verification. `dataset validate` and `dataset audit` must run before any training or benchmarking pipeline uses the dataset.

### 20.3 License violations
- **Risk:** Records with incompatible licenses enter redistribution.
- **Mitigation:** `metadata/license.json` is required with explicit SPDX, redistribution, attribution, and commercial fields. `licenses/LICENSE.txt` is required. CLI rejects datasets with incomplete or insufficient license coverage before freeze.

### 20.4 PHI leakage
- **Risk:** Raw literature records contain private health information or identifiers.
- **Mitigation:** Dataset v1 is synthetic-first per MedScale governance. Validation enforces `source_scope` includes `"synthetic"` unless a future override ADR is present.

### 20.5 Non-deterministic splits
- **Risk:** Seed drift or unordered collections produce inconsistent splits.
- **Mitigation:** Reuse existing `content_hash({"seed": seed, "record_id": record_id})` primitive. Enforce `seed` in manifest and fingerprint. Freeze makes split changes invalid.

### 20.6 Duplicate records
- **Risk:** Same source appears multiple times, padding counts or skewing splits.
- **Mitigation:** Duplicate record IDs are rejected at `manifest` / `freeze` time with explicit diagnostic.

### 20.7 Benchmark incompatibility
- **Risk:** Future benchmark versions expect record fields that v1 freezes against.
- **Mitigation:** Dataset v1 exports deterministic `statistics/*.json` summaries and a `dataset_fingerprint`. Benchmark manifests reference `dataset_id` + `dataset_version` + `dataset_fingerprint`; benchmark validation checks dataset fingerprint compatibility.

### 20.8 Future migration
- **Risk:** vN+1 requires breaking schema changes.
- **Mitigation:** Versioned dataset IDs and directory hierarchy under `data/datasets/{dataset_id}/{version}/`. Old datasets never mutate; new dataset IDs inaugurate new lines.

### 20.9 Large-dataset memory pressure
- **Risk:** Validation loads entire datasets into memory.
- **Mitigation:** Architecture requires streaming validation for checksums and split verification from the start. Implementations must not assume full-file materialization.

---

## 21. Implementation Plan

### Task 1: Audit and preparations
- **Objective:** Confirm repository state and remove any stale `bench/presets/` or placeholder files.
- **Files touched:** None
- **Tests:** Run existing `tests/test_dataset_*.py`; all must pass.
- **Acceptance criteria:** Existing tests green. `find src/medscale/bench -maxdepth 2` shows no `presets/`.
- **Complexity:** Low
- **Blocking:** None

### Task 2: DatasetSnapshot concept
- **Objective:** Define a lightweight `DatasetSnapshot` frozen dataclass in `medscale.dataset` with only immutable reproducibility metadata.
- **Files touched:** `src/medscale/dataset/snapshot.py` (new, concept only)
- **Tests:** Round-trip serialization; equality; immutability.
- **Acceptance criteria:** No dependency on `medscale.research`; only `medscale.reproducibility` is used.
- **Complexity:** Low
- **Blocking:** Task 1

### Task 3: Dataset fingerprint API
- **Objective:** Add `compute_dataset_fingerprint` that hashes canonical contents of manifest, schema, splits, license, and statistics.
- **Files touched:** `src/medscale/dataset/manifest.py` or `src/medscale/dataset/fingerprint.py`
- **Tests:** Deterministic fingerprint for identical inputs; fingerprint changes when any included artifact changes; missing artifact raises `ValidationIssue`.
- **Acceptance criteria:** Fingerprint is recorded in `manifest.json` at freeze time and is immutable.
- **Complexity:** Medium
- **Blocking:** Task 2

### Task 4: Freeze manifest API extension
- **Objective:** Extend `DatasetManifest` with `dataset_snapshot`, `fingerprint`, and checksum file references.
- **Files touched:** `src/medscale/dataset/manifest.py`
- **Tests:** Unit tests for new fields; default behavior unchanged for existing callers.
- **Acceptance criteria:** `DatasetManifest(...)` accepts new optional fields with defaults.
- **Complexity:** Low
- **Blocking:** Task 3

### Task 5: Checksum API with sibling `.sha256` files
- **Objective:** Pure function returning ordered mapping of relative artifact path to SHA-256; write output as sibling `.sha256` files.
- **Files touched:** `src/medscale/dataset/checksums.py`
- **Tests:** Deterministic checksum ordering; tamper detection; empty directory edge case; path-traversal rejection.
- **Acceptance criteria:** For identical directory contents, output is byte-identical; missing file raises `ValidationIssue`; traversal paths are rejected.
- **Complexity:** Medium
- **Blocking:** Task 4

### Task 6: Validate dataset frozen content checks
- **Objective:** Extend `validate_dataset` to verify checksum files, content hashes, path safety, synthetic-first policy, dataset ID format, and license completeness.
- **Files touched:** `src/medscale/dataset/validate.py`
- **Tests:** Tamper detection across manifest, schema, splits, README, license text; missing checksum file; path traversal; invalid dataset ID; incomplete license metadata; synthetic-first violation.
- **Acceptance criteria:** All mismatch modes yield `ValidationIssue` with artifact path, expected prefix, actual prefix, and remediation.
- **Complexity:** Medium
- **Blocking:** Task 5

### Task 7: CLI command `dataset freeze`
- **Objective:** Write checksum files, compute fingerprint, verify licenses, freeze dataset.
- **Files touched:** `src/medscale/cli/dataset.py`, `src/medscale/dataset/checksums.py`, `src/medscale/dataset/manifest.py`, `src/medscale/dataset/validate.py`
- **Tests:** Success, license mismatch, duplicate record ID, tampered post-freeze file, missing artifact, path traversal, invalid dataset ID, synthetic-first violation.
- **Acceptance criteria:** After successful freeze, `dataset validate` exits 0; tampering after freeze exits 1 with exact path and digest mismatch.
- **Complexity:** High
- **Blocking:** Task 6

### Task 8: CLI command `dataset audit`
- **Objective:** Human-readable readback of frozen dataset integrity.
- **Files touched:** `src/medscale/cli/dataset.py`
- **Tests:** Success path prints pass/fail per artifact; tampered dataset reports exact mismatch.
- **Acceptance criteria:** `audit` never mutates artifacts; output is deterministic for a given dataset state.
- **Complexity:** Medium
- **Blocking:** Task 7

### Task 9: Replay and benchmark linkage tests
- **Objective:** Verify benchmark manifest can reference dataset identity and replay validates compatibility.
- **Files touched:** `tests/test_dataset_manifest.py`, `tests/test_bench_replay.py`
- **Tests:** Frozen manifest matches recomputed hashes; benchmark manifest references dataset fingerprint; mismatch emits diagnostic; benchmark replay fails when dataset fingerprint diverges.
- **Acceptance criteria:** Any mismatch fails loudly with deterministic message.
- **Complexity:** Medium
- **Blocking:** Task 8

### Task 10: Architecture boundary tests
- **Objective:** Guard against accidental coupling to Colab, HF, modelkit, training, or research code.
- **Files touched:** `tests/test_architecture.py`
- **Tests:** Import boundary check for `medscale.dataset` and `medscale.cli.dataset`.
- **Acceptance criteria:** Import graph remains clean; test fails on forbidden dependency.
- **Complexity:** Low
- **Blocking:** Task 7

### Task 11: Full verification gate
- **Objective:** Run the M3-standard gate on the complete Dataset v1 surface.
- **Files touched:** None
- **Tests:** `uv run ruff check . && uv run mypy src tests && uv run pytest`
- **Acceptance criteria:** Exit 0; all previous test counts remain green; new dataset tests pass.
- **Complexity:** Low
- **Blocking:** Tasks 1–10

---

## 22. Benchmark Directory Layout (dataset-relevant)

```
data/datasets/
├── README.md
└── {dataset_id}/
    ├── manifest.json
    ├── schema.json
    ├── README.md
    ├── CHANGELOG.md
    ├── checksums/
    │   ├── manifest.sha256
    │   ├── schema.sha256
    │   ├── train.json.sha256
    │   ├── validation.json.sha256
    │   └── test.json.sha256
    ├── splits/
    │   ├── train.json
    │   ├── validation.json
    │   └── test.json
    ├── metadata/
    │   ├── license.json
    │   ├── sources.json
    │   └── statistics.json
    ├── licenses/
    │   └── LICENSE.txt
    └── statistics/
        ├── class_balance.json
        └── length_distribution.json
```

Benchmark directory layout remains unchanged:
```
data/bench/
├── manifests/
│   └── medscale-bench-v1.json
├── specs/
└── runs/
```

Benchmark manifests reference dataset versions by `dataset_id` + `dataset_version` + `dataset_fingerprint`; they never mutate dataset artifacts.

---

## 23. Replay Guarantees

For every frozen dataset version:

- **Checksum integrity:** Sibling `.sha256` files must recompute to identical SHA-256 digests across any execution.
- **Fingerprint integrity:** `dataset_fingerprint` in `manifest.json` must match recomputed fingerprint from canonical artifact contents.
- **Path safety:** Every path referenced by manifest or checksums must resolve inside the dataset root; traversal and absolute paths are rejected.
- **Git SHA binding:** `git_sha` is stored and checked during `dataset validate` and `dataset audit`.
- **Software version binding:** `software_version` is stored and checked.
- **Seed binding:** `seed` is stored and must agree with the split-generation parameters actually used via the canonical `content_hash({"seed": seed, "record_id": record_id})` primitive.
- **Dataset ID format:** `dataset_id` must match `^[a-z][a-z0-9-]{3,63}$`.
- **License completeness:** `metadata/license.json` must include all required fields; validation fails if incomplete.
- **Synthetic-first policy:** v1 datasets must declare `source_scope` containing `"synthetic"` unless a future override ADR is present.
- **Any mismatch:** CLI or API returns exit 1 with diagnostic including field, expected hash prefix, actual hash prefix, artifact path, and suggested remediation when unambiguous.

---

## 24. Remaining Known Limitations (Pre-Implementation)

- No real-world record ingestion UI; ingest remains programmatic only.
- No model training code; training integration is contract-only.
- No Colab notebook generation.
- No Hugging Face release automation.
- No FHIR ingestion path.
- No collaboration workflow metadata.
- Dataset v1 is synthetic-first; real-world datasets require future governance approval.
- Streaming validation for very large datasets is an architecture requirement but not yet implemented.

---

## 25. Final Statement

This revised plan reconciles the original proposal with the completed architectural review. It reuses every existing primitive in the repository: `canonical_json`, `content_hash`, `DatasetManifest`, `DatasetValidationReport`, `DeterministicSplitter`, `Provenance`, `EvidenceObject`. It does not introduce duplicate abstractions, does not modify repository files, does not implement Dataset v1, and does not touch Dataset v1 implementation boundaries. The dataset layer is explicitly isolated from `medscale.research`, training code, Colab, and Hugging Face.

Dataset v1 architecture planning complete. Awaiting implementation approval.
