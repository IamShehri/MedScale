# M5 — FHIR Boundary

Deterministic, trust-preserving FHIR interoperability boundary.

## Purpose

fhirkit provides:

- FHIR validation boundary
- deterministic `ValidationReport` schema
- content-addressed artifact storage
- optional validator integration
- no PHI leakage

This is NOT a healthcare product. It is a deterministic trust boundary.

## Components

- `src/medscale/fhirkit/report.py`: `ValidationReport` contract
- `src/medscale/fhirkit/validate.py`: optional validator boundary
- `src/medscale/fhirkit/storage.py`: content-addressed storage
- `src/medscale/fhirkit/errors.py`: error hierarchy
- `src/medscale/cli/fhir.py`: `medscale fhir validate`

## ValidationReport Contract

Fields:

- `report_id`
- `input_hash`
- `validator_name`
- `validator_version`
- `status`
- `errors`
- `warnings`
- `created_at`
- `format_version`

Serialization:

- deterministic field ordering
- canonical JSON output
- hash reproducibility

## Storage Format

Storage layout:

```text
data/fhirkit/<report_hash>/report.json
```

Properties:

- content addressed
- immutable
- deterministic

## Optional Dependency Behavior

No mandatory external validator dependency.
No network calls.
No downloading validators automatically.
No hidden installation.

Validators are invoked explicitly via `validate_fhir_with_validator(command=...)`.

## Verification

- ruff PASS
- mypy PASS
- pytest 330 passed, 2 skipped
