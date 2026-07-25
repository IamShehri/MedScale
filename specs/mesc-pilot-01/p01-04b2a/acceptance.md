# MESC Pilot-01 — P01-04B2A Acceptance Criteria

Status:
**PROPOSED AUTHORIZATION GATE — FOUNDER DECISION PENDING**

Implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Canonical planning baseline:
`1a9169f7229bb72eba6772448724c54ec71937c5`

---

## Documentation-gate acceptance

P01-04B2A passes documentation-gate acceptance when:

1. All proposed decisions PD-B2A-1 through PD-B2A-8 are visible in
   `decision-record.md`.
2. Exact proposed implementation/test paths are recorded and labeled as
   proposals only.
3. No document claims implementation or execution has started.
4. No hidden authorization is embedded in contracts, specifications, or
   acceptance criteria.
5. Historical P01-04A identity and provenance are not rewritten.
6. Cross-document references are internally consistent.
7. Changed-path scope is limited to documentation only:
   - `specs/mesc-pilot-01/p01-04b2a/**`
   - `specs/mesc-pilot-01/p01-04b2/README.md`
   - `specs/mesc-pilot-01/p01-04b2/plan.md`
   - `specs/mesc-pilot-01/tasks.md`
8. `git diff --check` produces no whitespace errors.
9. No document contains placeholder text or markers indicating unfinished
   drafting work.
10. No document contains local paths, usernames, hostnames, or timestamps.

P01-04B2A documentation-gate acceptance does not authorize B2A implementation
or execution. Separate founder authorization is required.

## Future implementation acceptance

P01-04B2A passes implementation acceptance when:

1. Implementation is limited to the four authorized paths:
   - `src/medscale/mesc/_canonical_json_v1.py`
   - `src/medscale/mesc/_split_artifacts_v1.py`
   - `tests/test_mesc_canonical_json_v1.py`
   - `tests/test_mesc_split_artifacts_v1.py`
2. All available quality gates pass on the exact-head CI.
3. Deterministic golden vectors are byte-identical across Python 3.11, 3.12,
   Windows, Linux, and macOS.
4. Full 64-hex `split_fingerprint` is the sole authoritative fingerprint.
5. No date, timestamp, path, username, hostname, runtime version, or command
   log is stored in promoted artifact types.
6. Required artifact roles are exactly:
   - `group_registry`
   - `example_registry`
   - `split_summary`
   - `excluded_ledger`
7. Fail-closed validation rejects unsupported value types, floating-point
   values, non-string object keys, missing/unknown/duplicate roles, invalid
   SHA-256 or byte size, forbidden runtime metadata, forbidden dates, and
   fingerprint mismatches.
8. No CLI, filesystem publication, public export, fixture facade, public
   splitter activation, leakage detection, or real data access is introduced.
9. No execution has been performed during implementation acceptance.

P01-04B2A implementation acceptance requires separate founder authorization.

## Execution prohibition

P01-04B2A does not authorize and does not reference:

- real split generation or partition assignment;
- leakage detection, normalization, classification, or audit execution;
- access to real P01-03G registries or other datasets;
- model access, inference, training, metrics, or benchmark evaluation;
- P01-04B2B, P01-04B2C, P01-04B2D, or any later stage;
- P01-04C–G or P01-05 or later.
