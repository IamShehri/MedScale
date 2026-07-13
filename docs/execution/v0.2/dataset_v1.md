# Dataset v1

MedScale Dataset v1 is a deterministic, reproducible corpus derived from the
internal `data/litdb/corpus/records.jsonl` literature database.  It satisfies
ADR-0030, uses content-hash splitting with seed 42, and is validated by
`medscale dataset validate`.

## Layout

```
data/datasets/medscale-dataset-v1/
├── manifest.json      # deterministic dataset manifest
├── schema.json        # dataset JSON schema
├── README.md          # human-readable overview
├── records.json       # complete corpus snapshot
├── licenses.json      # license coverage summary
├── splits/
│   ├── train.json
│   ├── validation.json
│   └── test.json
└── checksums/
    ├── manifest.json.sha256
    ├── schema.json.sha256
    ├── train.json.sha256
    ├── validation.json.sha256
    └── test.json.sha256

metadata/
└── licenses.json      # SPDX coverage summary
```

## Generation

```bash
uv run python -m medscale.dataset.generate
```

This module is deterministic: the same inputs and seed produce identical
artifacts.  No external datasets are used.

## CLI

```bash
# Preview without mutation
uv run medscale dataset manifest medscale-dataset-v1

# Persist manifest
uv run medscale dataset manifest medscale-dataset-v1 --write

# Validate a dataset directory
uv run medscale dataset validate data/datasets/medscale-dataset-v1
```

## Validation

The validation checks:

1. manifest.json is valid JSON
2. schema.json is valid JSON
3. All splits ({train,validation,test}.json) exist and are valid JSON
4. checksums manifest maps artifact paths to SHA-256 digests
5. Computed SHA-256 digests match expected values

Validation is read-only and fails loudly on any mismatch.

## Split Strategy

Records are assigned deterministically based on content hash of `record_id`:

- Train: 70%
- Validation: 15%
- Test: 15%

Split assignments are stable for a fixed seed and record set.

## License Metadata

`metadata/licenses.json` is generated from the corpus and records the
license_summary field from each literature record.
