# Dataset v1

MedScale Dataset v1 is a deterministic, reproducible corpus derived from the
internal literature database. It satisfies ADR-0030, uses sibling `.sha256`
checksums, content-hash splitting with seed 42, and is validated by
`medscale dataset validate`.

## Layout

```
data/datasets/medscale-dataset-v1/
├── manifest.json      # deterministic dataset manifest
├── schema.json        # dataset JSON schema
├── README.md          # human-readable overview
├── records.json       # complete corpus snapshot
├── metadata/
│   └── license.json   # SPDX coverage summary
├── splits/
│   ├── train.json
│   ├── validation.json
│   └── test.json
└── checksums/
    ├── manifest.json.sha256
    ├── schema.json.sha256
    ├── records.json.sha256
    ├── train.json.sha256
    ├── validation.json.sha256
    └── test.json.sha256
```

## Generation

```bash
uv run python -m medscale.dataset.generate
```

This module is deterministic: the same inputs and seed produce identical
artifacts. No external datasets are fetched at runtime.

## CLI

```bash
# Initialize a new dataset tree
uv run medscale dataset init medscale-dataset-v1 --write

# Preview manifest without mutation
uv run medscale dataset manifest medscale-dataset-v1

# Persist manifest
uv run medscale dataset manifest medscale-dataset-v1 --write

# Validate a dataset directory
uv run medscale dataset validate medscale-dataset-v1
```

## Validation

The validation checks:

1. `manifest.json`, `schema.json`, `records.json`, and split files are valid JSON
2. `metadata/license.json` exists and contains the required ADR-0030 fields
3. All artifact paths resolve inside the dataset root; path traversal is rejected
4. Every sibling `.sha256` file matches its artifact bytes
5. `dataset_fingerprint` in `manifest.json` matches recomputed canonical contents
6. Dataset ID format, timestamps, and synthetic-first policy are enforced

Validation is read-only and fails loudly on any mismatch.

## Split Strategy

Records are assigned deterministically using the existing content-hash primitive:

```python
content_hash({"seed": seed, "record_id": record_id})
```

- Train: 70%
- Validation: 15%
- Test: 15%

Split assignments are stable for a fixed seed and record set.

## License Metadata

`metadata/license.json` is required before freeze and must include ADR-0030
fields such as `spdx_id`, `source_scope`, `redistribution_allowed`,
`attribution_required`, and `commercial_allowed`. Validation fails if the file
is missing or incomplete.

## Checksum Policy

Dataset v1 uses sibling `.sha256` files only; no JSON checksum manifest is used.
Each `.sha256` contains a single lowercase hex digest. Validation recomputes and
compares byte-for-byte.
