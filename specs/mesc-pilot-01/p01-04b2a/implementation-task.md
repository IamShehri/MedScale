# MESC Pilot-01 — P01-04B2A Implementation Task

Status:
**PROPOSED AUTHORIZATION GATE — FOUNDER DECISION PENDING**

Implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Canonical planning baseline:
`1a9169f7229bb72eba6772448724c54ec71937c5`

---

## Authorization preconditions

This task is **NOT EXECUTABLE UNTIL EXPLICIT FOUNDER AUTHORIZATION**.

It records a proposed future implementation brief only. No code, test, branch,
PR, push, merge, or execution action is authorized by this document.

## Proposed implementation paths

- `src/medscale/mesc/_canonical_json_v1.py`
- `src/medscale/mesc/_split_artifacts_v1.py`
- `tests/test_mesc_canonical_json_v1.py`
- `tests/test_mesc_split_artifacts_v1.py`

## Required behavior

- Private immutable artifact-contract types under `medscale.mesc`.
- Canonical in-memory JSON and JSONL serialization returning bytes only.
- SHA-256 artifact descriptors with required roles.
- Non-circular two-layer split-fingerprint identity model.
- Typed private fail-closed validation errors.
- Deterministic unit and golden-vector tests using synthetic inputs only.
- No public export, public facade, or execution entry point.
- No modification to frozen B1 files:
  `src/medscale/mesc/__init__.py`, `src/medscale/mesc/split.py`,
  `src/medscale/mesc/_split_v1.py`, `src/medscale/cli/**`,
  `pyproject.toml`, `uv.lock`, `.github/**`.

## Forbidden behavior

Do not implement:

- leakage detection, classification, normalization, or audit execution;
- fixture facade, public splitter activation, CLI, filesystem write path,
  atomic publication, or side effects;
- real P01-03G loading, partition generation, dataset access, model access,
  inference, training, metrics, or clinical claims;
- new public exports or mutation of B1 serialization/behavior;
- promotion of unratified bundle schema versions or unknown artifact roles.

## Test matrix

- Canonical JSON unit tests for supported/unsupported/prohibited values.
- JSONL canonical tests including zero-record edge case.
- Descriptor validation tests for required roles, invalid SHA-256, invalid
  byte size, duplicate roles, unknown roles.
- Deterministic golden-vector tests on Python 3.11 and 3.12.
- Fingerprint identity tests verifying full 64-hex SHA-256 and non-circular
  construction.
- Fail-closed rejection tests for prohibited categories.

## Stop conditions

Stop without mutation if:

- founder authorization is absent or later withdrawn;
- the canonical main SHA differs from the recorded authorization baseline;
- any proposed file path conflicts with P01-04A or frozen B1 boundaries;
- Stop if implementation begins before explicit founder authorization.
- Stop if Ready or merge is attempted before exact-head CI and independent Opus review are complete.
- any hidden execution, data access, or external I/O is introduced;
- any document claims B2A is accepted or implemented.

## Execution rules

- One atomic implementation PR only.
- Exact-head CI is required for every head submitted for review.
- CI reruns are permitted for transient infrastructure failures and additive corrective commits.
- Independent Opus review is required.
- An additive corrective commit after review requires a delta re-review.
- No push or PR before explicit founder authorization unless later instructed.
- No merge until explicit founder/ChatGPT authorization after Opus review.
- B2B authorization is not granted by B2A authorization.
