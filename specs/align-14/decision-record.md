# ALIGN-14 Planning — Decision Record

- **Planning status:** Complete
- **Implementation status:** NOT AUTHORIZED

## Selected capability

ALIGN-14 selects the deterministic dataset split-assignment freeze contract.

This capability:
- captures the exact membership of stable record identifiers in train, validation, and test splits;
- binds those assignments to explicit splitter inputs and fingerprints;
- produces a stable identity designed for possible future reference by release or benchmark artifacts; formal integration is deferred and is outside the ALIGN-14 minimum slice;
- reuses the existing deterministic splitter and `DatasetReleaseManifest`;
- does not change splitter behavior or release-manifest behavior in the minimum slice.

## Corrected candidate analysis

C1 remains the evidence-backed winner after correcting for existing splitter and release-manifest overlap.

Revised score: **93/100**

The reduction from earlier estimates reflects that ALIGN-14 is now defined as the narrower freeze-record gap rather than a broader splitter or manifest redesign.

## Rejected alternatives

- **C2 Evidence contract boundary:** independent of ALIGN-13 and would require duplicate-root resolution before implementation.
- **C3 v0.2 release-hygiene package:** orthogonal governance cleanup, not a direct successor capability.
- **C4 FHIR expansion:** currently blocked by missing JRE + HL7 validator.
- **C5 Reproducibility namespace consolidation:** already governed by ADR-0014 and not a direct ALIGN-13 successor.

## Why existing splitting is reused

`src/medscale/dataset/split.py` already provides deterministic, sorted, fixed-seed assignments with no global random state. Reimplementing this would duplicate tested behavior and expand scope unnecessarily.

## Why existing release manifest is reused

`medscale.dataset.builder.DatasetReleaseManifest` already carries release identity, lineage, and checksums. ALIGN-14 adds only a reference path for split-freeze identity in the minimum slice.

## Why an immutable value contract is preferred

A lifecycle state machine would introduce mutable runtime semantics, possible filesystem mutation, or workflow-state drift. An immutable value contract preserves the repository's evidence-first, reproducibility-first model and aligns with ADR-0031.

## Why timestamps are excluded from identity

Timestamps are excluded because freeze identity must be stable across reproduction runs. Timestamps belong to release metadata, not to deterministic identity.

## Proposed implementation boundary

Maximum: three files

- `src/medscale/dataset/builder/freeze.py`
- `src/medscale/dataset/builder/__init__.py`
- `tests/test_dataset_freeze.py`

Any expansion beyond this boundary requires a new founder scope decision.

## ADR dependency

Proposed ADR-0032 must be accepted before implementation authorization.

## Founder decisions still required

- Approve Proposed ADR-0032.
- Authorize ALIGN-14 implementation within the three-file allowlist.
- Confirm empty-split behavior and identity semantics if ADR-0032 leaves them undecided.

## Rejected alternatives summary

- duplicate-splitter approach: rejected to preserve existing tested behavior;
- duplicate-release-manifest approach: rejected to preserve ALIGN-13 contract surface;
- lifecycle-state-machine approach: rejected to preserve pure deterministic semantics.
