# M2 — Evidence Infrastructure

## Purpose

Extract the evidence model from the legacy flat module into a dedicated capability layer while preserving behavior, public APIs, and stored data compatibility.

## Before Architecture

- `src/medscale/evidence.py` contained all evidence types, enums, and logic in a single module.
- Evidence concepts were tightly coupled to the flat file.
- Layer boundaries: evidence logic lived outside the evidence capability layer.

## After Architecture

- `src/medscale/evidence/` is a dedicated package with:
  - `models.py` — frozen data model and state machine
  - `grading.py` — deterministic level mapping
  - `protocol.py` — `EvidenceSystem` protocol for verification backends
  - `__init__.py` — public re-exports matching the old flat module
- `src/medscale/evidence.py` is now a compatibility shim preserving the legacy import path.
- Layer rule enforced: evidence must not import `litdb`, `modelkit`, or `bench`.

## Migration Decisions

1. **Public API preserved**: `from medscale.evidence import EvidenceObject` continues working via the shim.
2. **Data compatibility preserved**: `format: 1` artifacts load unchanged through `evidence_store.py`.
3. **No stored data rewritten**: No JSONL mutations; no hash changes.
4. **Architecture tests updated**: Added explicit evidence-layer boundary rule.

## Tests Performed

- `tests/test_evidence_subpackage.py` — public imports, subpackage symbol parity, format-1 artifact load/round-trip, optional-dependency import safety
- `tests/test_architecture.py` — evidence-layer import boundary enforcement
- Full suite: `282 passed`

## Validation Results

- ruff PASS
- mypy PASS: 93 source files
- pytest 282/282 PASS

## Risks

- **Low**: Compatibility shim could become stale if future refactors drift from it. Mitigation: subpackage tests verify `__all__` parity.
- **Low**: Circular-import risk during package transition. Mitigation: models import only spine modules (`provenance`, `reproducibility`).
