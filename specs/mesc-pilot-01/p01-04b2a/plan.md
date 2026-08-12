# MESC Pilot-01 — P01-04B2A Plan

Status:
**PROPOSED AUTHORIZATION GATE — FOUNDER DECISION PENDING**

Implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Canonical planning baseline:
`1a9169f7229bb72eba6772448724c54ec71937c5`

---

## Gate sequence

B2A documentation gate
→ founder decision
→ implementation authorization
→ atomic implementation PR
→ exact-head CI
→ independent Opus review
→ founder/ChatGPT merge decision
→ B2A acceptance
→ only then may B2B authorization be considered

No parallel B2B, B2C, or B2D work is authorized.

## Future implementation scope

If founder authorization is granted, the proposed B2A implementation paths are:

- `src/medscale/mesc/_canonical_json_v1.py`
- `src/medscale/mesc/_split_artifacts_v1.py`
- `tests/test_mesc_canonical_json_v1.py`
- `tests/test_mesc_split_artifacts_v1.py`

These paths remain proposals until founder authorization. They are not created,
modified, or executed by this documentation package.

## Future B2A implementation constraints

Future B2A implementation must not modify:

- `src/medscale/mesc/__init__.py`
- `src/medscale/mesc/split.py`
- `src/medscale/mesc/_split_v1.py`
- `src/medscale/cli/**`
- `pyproject.toml`
- `uv.lock`
- `.github/**`

No new public export is permitted in B2A. Public exposure, fixture
integration, and execution entry points belong to later separately authorized
increments.

## Relationship to B2B–D

B2B requires separate authorization after B2A acceptance.
B2C requires separate authorization after B2A and B2B acceptance.
B2D requires separate authorization after B2A, B2B, and B2C acceptance.

Ratification of P01-04B2 design decisions does not authorize any B2
increment. Merge of this documentation PR does not authorize B2A.

## Stop conditions

Stop without mutation if:

- canonical main SHA does not match the recorded authorization baseline;
- any proposed implementation conflicts with P01-04A decisions D1–D10;
- any document claims execution has started;
- any document claims leakage has been ruled out;
- any document includes source-data redistribution claims beyond the canonical
  rights-and-provenance record;
- an unauthorized path is modified.
