# ADR-0030: Dataset Versioning and Training-Artifact Contract

## Status

Proposed

## Context

MedScale has frozen its evidence model, benchmark replay contract, and release
engineering. The next scientific boundary is the dataset: without a versioned,
reproducible dataset contract, benchmark results, model cards, and future
experiments cannot be tied to a fixed corpus state.

A dataset artifact is not just a directory of JSON files. It is a first-class
research artifact that must carry:

1. a deterministic manifest that can be recomputed byte-for-byte from the same
   inputs;
2. a schema that reuses existing MedScale contracts rather than introducing
   duplicate types;
3. split boundaries that are reproducible for a fixed seed and record order,
   using the existing `medscale.dataset.split` primitive;
4. per-artifact SHA-256 checksums so any silent mutation is detectable;
5. provenance and license metadata at both record and dataset level;
6. a content-derived dataset fingerprint that downstream consumers can reference
   without loading the full dataset.

Existing MedScale primitives already provide most of the building blocks:

- `medscale.dataset.schema` for `LiteratureRecord`, `EvidenceObject`, and
  `BenchmarkItem` schemas;
- `medscale.dataset.split.DeterministicSplitter` for reproducible splits;
- `medscale.reproducibility.content_hash` and `canonical_json` for deterministic
  identity and serialization;
- `medscale.provenance.Provenance` for source provenance.

Dataset v1 must not depend on `medscale.research` or any higher-level package.
The dataset package is foundational; upward dependencies create layering
violations and future circularity risk.

## Decision

Introduce a versioned dataset contract under:

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

### Dataset manifest contract

`manifest.json` fields:

```json
{
  "dataset_id": "<lowercase-hyphenated-id>",
  "dataset_version": "<semver or date>",
  "created_at": "<ISO-8601 UTC>",
  "dataset_snapshot": {
    "git_sha": "<commit sha>",
    "software_version": "< MedScale version >",
    "created_at": "<ISO-8601 UTC>",
    "fingerprint": "<SHA-256>"
  },
  "git_sha": "<commit sha>",
  "seed": 42,
  "record_count": 0,
  "license_summary": [],
  "schema_version": "1",
  "split_strategy": "deterministic_hash_split",
  "dataset_fingerprint": "<SHA-256>",
  "hash_algorithm": "sha256"
}
```

`dataset_snapshot` is a lightweight frozen metadata concept defined within
`medscale.dataset`, populated from explicit CLI inputs. It is not imported from
`medscale.research`.

`fingerprint` inside `dataset_snapshot` and `dataset_fingerprint` at the manifest
top level are the same value; the top-level field exists for convenient lookup by
downstream consumers.

### Dataset fingerprint

`dataset_fingerprint` is computed from the canonical contents of:

- `manifest.json`
- `schema.json`
- `splits/train.json`
- `splits/validation.json`
- `splits/test.json`
- `metadata/license.json`
- `metadata/statistics.json`

Computation uses `canonical_json` on each component, then `content_hash` over the
ordered mapping. Any mutation to any included artifact produces a different
fingerprint. Benchmark manifests reference `dataset_id` + `dataset_version` +
`dataset_fingerprint`.

### Dataset identity vocabulary

- `dataset_id` — stable identifier for the dataset collection. Allowed format:
  lowercase letters, digits, and hyphens; must start with a letter; regex
  `^[a-z][a-z0-9-]{3,63}$`; max 63 characters.
- `dataset_version` — mutable version string for a specific frozen instantiation.
- `dataset_fingerprint` — content-derived SHA-256 identity. Two versions with
  identical contents have identical fingerprints; any difference produces a
  different fingerprint.

Future Dataset v2 uses a new `dataset_id` and a new ADR. Dataset v1 artifacts
remain frozen and valid; old datasets are never mutated.

### Dataset schema contract

`schema.json` defines three top-level entry types by reference, not by duplication:

- `LiteratureRecord` — `id`, `title`, `abstract`, `identifiers`, `provenance`,
  `license_spdx`;
- `EvidenceObject` — `evidence_id`, `source_record_id`, `verification`,
  `provenance`;
- `BenchmarkItem` — `task_id`, `input_reference`, `expected_output_reference`,
  `metadata`.

Split files contain arrays of lightweight wrapper objects that reference these
types by id; the canonical record data lives in the source corpus.

### Split strategy

Dataset v1 reuses the existing deterministic split primitive:

```python
content_hash({"seed": seed, "record_id": record_id})
```

This is the same primitive implemented by `medscale.dataset.split.DeterministicSplitter`
and verified by `tests/test_dataset_split.py`. Assigning records to splits by
this hash, after sorting record IDs deterministically, guarantees order
independence and compatibility with existing tests. No alternative hashing
algorithm is permitted in v1.

Ratios:
- train: 80%
- validation: 10%
- test: 10%

### Data integrity

Every dataset artifact gets a sibling `.sha256` file in `checksums/`. Validation
reads the artifact, computes `sha256(...)`, and compares it to the stored value.

The canonical checksum layout in v1 is sibling `.sha256` files only:

- `checksums/manifest.sha256`
- `checksums/schema.sha256`
- `checksums/train.json.sha256`
- `checksums/validation.json.sha256`
- `checksums/test.json.sha256`

A JSON checksum manifest (`checksums/manifest.json`) is not used in v1. Mixed
layouts are prohibited because they produce audit ambiguity.

### Path validation

Every path referenced by the dataset manifest or checksums must resolve inside
the dataset root. Implementations must reject path traversal sequences, absolute
paths, and normalized paths that escape the dataset directory. Validation failures
must be loud and include the offending path and expected boundary.

### Timestamp policy

- `created_at` is immutable after freeze.
- `freeze` accepts an explicit `--created-at` CLI argument.
- If omitted, the CLI generates a UTC ISO-8601 timestamp and records it in the
  manifest.
- Once written, `created_at` is never overwritten.
- All timestamps must be explicit, timezone-aware ISO-8601 strings. Implicit or
  naive timestamps are rejected by validation.

Explicit timestamps remove hidden state from artifact identity. Two freeze
invocations with identical inputs and the same explicit timestamp produce
identical manifests.

### Provenance

Provenance metadata is preserved from the source corpus; the dataset layer adds
only `dataset_snapshot` and derived split metadata. Dataset v1 does not redefine
`Provenance`; it reuses `medscale.provenance.Provenance` from the evidence layer.

### License tracking

Every dataset must define explicit license coverage before freeze.

`metadata/license.json` required fields:
- `spdx_id`
- `source_scope`
- `redistribution_allowed`
- `attribution_required`
- `commercial_allowed`

Validation fails if `metadata/license.json` is missing, incomplete, or if any
record in the dataset lacks license coverage.

Dataset v1 is synthetic-first. A record with `source_scope` not including
`"synthetic"` requires explicit governance approval before freeze.

### Storage policy

`data/datasets/` is gitignored. Reproducibility survives local deletion through:

- `dataset_id` + `dataset_version` + `dataset_fingerprint` as stable identifiers
- `checksums/*.sha256` for byte-level integrity verification
- optional `storage_uri` in `manifest.json` for future remote retrieval

No dataset artifact may reference local files outside the dataset root by
relative path.

### Large-dataset policy

Future implementations must support streaming validation for checksum
calculation, manifest validation, and split verification. Dataset v1 design must
not hardcode patterns that assume the entire dataset fits in memory.

### CLI verbs

- `medscale dataset init <dataset-id>` — scaffold dataset directories and
  metadata. Preview-only by default.
- `medscale dataset manifest <dataset-dir>` — write or preview `manifest.json`.
  Preview by default; write mutates the filesystem.
- `medscale dataset validate <dataset-dir>` — check schema, checksums, splits,
  paths, licenses, synthetic-first policy, and dataset ID format. Loud failure
  on any mismatch.
- `medscale dataset freeze <dataset-dir>` — write checksums, fingerprint, and
  immutable manifest. Validates licenses and paths before writing.
- `medscale dataset audit <dataset-dir>` — recompute full integrity readback
  without mutation.

CLI commands must never modify the source corpus automatically. They create
explicit artifacts under `data/datasets/`.

### Benchmark linkage

Benchmark manifests reference datasets by `dataset_id`, `dataset_version`, and
`dataset_fingerprint`. Benchmark replay validates that the frozen dataset
fingerprint referenced by the benchmark manifest matches the recomputed
fingerprint of the dataset currently available at the referenced path. Mismatch
fails loudly with dataset path, stored fingerprint prefix, and recomputed
fingerprint prefix.

### Training artifacts

Dataset v1 does not define training manifests, model card fields, metrics fields,
parameters schemas, or experiment artifact layouts. Future training manifests
will be specified in a separate ADR after Dataset v1 is complete.

## Constraints

- v1 uses the MedScale internal corpus only; no external datasets.
- Dataset generation remains separate from model training. No training code is
  introduced in this phase.
- Existing data contracts (`LiteratureRecord`, `EvidenceObject`, `Provenance`,
  `TaskItem`) are not modified; only their usage in dataset artifacts is
  formalized.
- Dataset v1 must not depend on `medscale.research`, `medscale.bench`,
  `medscale.evidence`, `medscale.litdb`, `medscale.modelkit`, training code,
  Colab, or Hugging Face.

## Consequences

- Adds a new top-level data directory `data/datasets/`.
- Requires new modules under `src/medscale/dataset/`.
- Requires new CLI verbs in `src/medscale/cli/dataset.py`.
- Requires new tests and documentation.
- Freezes the dataset contract at v1; future versions require a new ADR.
- Establishes dataset fingerprint as the canonical downstream identity.
- Aligns dataset layering with MedScale architecture: dataset is foundational,
  not dependent on research or training layers.

## References

- docs/execution/v0.2/DATASET_V1_PLAN.md
- docs/adr/0009-evidence-model.md
- docs/adr/0017-identifier-stability-contract.md
- docs/adr/0029-benchmark-determinism-and-replay-contract.md
- docs/adr/0022-screening-decision-semantics.md
- docs/releases/artifact_lifecycle.md
- docs/research/reproducibility_policy.md
