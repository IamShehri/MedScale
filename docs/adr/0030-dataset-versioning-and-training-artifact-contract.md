# ADR-0030: Dataset Versioning and Training-Artifact Contract

## Status

Accepted

## Context

MedScale has frozen its evidence model, benchmark replay contract, and release
engineering. The next scientific boundary is the dataset: without a versioned,
reproducible dataset contract, benchmark results, model cards, and Colab
experiments cannot be tied to a fixed corpus state.

A dataset artifact is not just a directory of JSON files. It is a first-class
research artifact that must carry:

1. a deterministic manifest that can be recomputed byte-for-byte from the same
   inputs;
2. a schema that reuses existing MedScale contracts rather than introducing
   duplicate types;
3. split boundaries that are reproducible for a fixed seed and record order;
4. per-artifact SHA-256 checksums so any silent mutation is detectable;
5. provenance and license metadata at both record and dataset level.

Existing MedScale primitives already provide most of the building blocks:

- `medscale.litdb.records.LiteratureRecord` for bibliographic records;
- `medscale.evidence.models.EvidenceObject` for evidence entries;
- `medscale.bench.tasks` for benchmark item references;
- `medscale.provenance.Provenance` for source provenance;
- `medscale.reproducibility.content_hash` for deterministic identity.

## Decision

Introduce a versioned dataset contract under:

```
data/datasets/medscale-dataset-v1/
├── manifest.json
├── schema.json
├── licenses.json
├── README.md
├── splits/
│   ├── train.json
│   ├── validation.json
│   └── test.json
└── checksums/
    ├── manifest.sha256
    ├── schema.sha256
    ├── licenses.sha256
    ├── train.json.sha256
    ├── validation.json.sha256
    └── test.json.sha256
```

## Dataset manifest contract

`manifest.json` fields:

```json
{
  "dataset_id": "medscale-dataset-v1",
  "version": "1.0",
  "created_at": "<ISO-8601>",
  "source_snapshot": "<source snapshot id>",
  "git_sha": "<tree sha256 or commit sha>",
  "record_count": 0,
  "license_summary": [],
  "schema_version": "1",
  "split_strategy": "deterministic_hash_split",
  "split_seed": 42,
  "hash_algorithm": "sha256"
}
```

`license_summary` is an array of `{ spdx, count }` objects derived from
`LiteratureRecord.license_spdx`.

## Dataset schema contract

`schema.json` defines three top-level entry types by reference, not by duplication:

- `LiteratureRecord` — `id`, `title`, `abstract`, `identifiers`, `provenance`,
  `license_spdx`;
- `EvidenceObject` — `evidence_id`, `source_record_id`, `verification`,
  `provenance`;
- `BenchmarkItem` — `task_id`, `input_reference`, `expected_output_reference`,
  `metadata`.

Split files contain arrays of lightweight wrapper objects that reference these
types by id; the canonical record data lives in the source corpus.

## Split strategy

Deterministic hash split with fixed parameters:

- strategy: `deterministic_hash_split`
- seed: `42`
- ratios: train `70%`, validation `15%`, test `15%`

The assignment of a record to a split depends only on its stable identifier and
the fixed seed. Sorting the stable identifier set before assignment guarantees
determinism across machines and runs.

## Data integrity

Every dataset artifact gets a sibling `.sha256` file in `checksums/`. Validation
reads the artifact, computes `sha256(...)`, and compares it to the stored value.

Provenance metadata is preserved from the source corpus; the dataset layer adds
only `source_snapshot` and derived split metadata.

## CLI verbs

- `medscale dataset init <dataset-id>` — scaffold dataset directories and
  metadata. Preview-only by default.
- `medscale dataset manifest <dataset-dir>` — write or preview manifest.json.
  Preview by default; `--write` mutates the filesystem.
- `medscale dataset validate <dataset-dir>` — check schema, checksums, and split
  determinism. Loud failure on any mismatch.

CLI commands must never modify the source corpus automatically. They create
explicit artifacts under `data/datasets/`.

## Constraints

- v1 uses the MedScale internal corpus only; no external datasets.
- Dataset generation remains separate from model training. No training code is
  introduced in this phase.
- Existing data contracts (`LiteratureRecord`, `EvidenceObject`, `Provenance`,
  `TaskItem`) are not modified; only their usage in dataset artifacts is
  formalized.

## Consequences

- Adds a new top-level data directory `data/datasets/`.
- Requires new modules under `src/medscale/dataset/`.
- Requires new CLI verbs in `src/medscale/cli/dataset.py`.
- Requires new tests and documentation.
- Freezes the dataset contract at v1; future versions require a new ADR.
