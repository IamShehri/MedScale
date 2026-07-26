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

1. If B2A is explicitly authorized by the founder, implementation is limited to
the following four paths:
   - `src/medscale/mesc/_canonical_json_v1.py`
   - `src/medscale/mesc/_split_artifacts_v1.py`
   - `tests/test_mesc_canonical_json_v1.py`
   - `tests/test_mesc_split_artifacts_v1.py`
2. All available quality gates pass on the exact-head CI.
3. Deterministic golden vectors are byte-identical across Python 3.11, 3.12,
   Windows, Linux, and macOS. This requirement is retained in full and is not
   satisfied by the evidence currently obtainable. It is discharged in two
   separately evidenced parts:

   a. **Discharged by the B2A implementation PR (available evidence).**
      Current repository CI provides Linux evidence only, and tests exactly
      Python 3.11 and Python 3.12. Byte-identical golden vectors across Linux
      with Python 3.11 and Python 3.12 may therefore be evaluated by the B2A
      implementation PR on its exact head.

   b. **Not discharged by the B2A implementation PR (open obligation).**
      Windows and macOS byte-identity evidence does not currently exist and has
      not been produced. The B2A implementation PR is not authorized to modify
      `.github/**`, so it cannot create that evidence. Per PD-B2A-8, Windows and
      macOS evidence requires separately authorized validation infrastructure,
      which this package does not authorize.

   Until that infrastructure is separately authorized and the evidence is
   produced, the Windows and macOS portability obligation remains an explicitly
   recorded open item. It must not be treated as satisfied, waived, or removed,
   and no document may claim that cross-platform evidence has already been
   produced. B2A implementation acceptance under this criterion is therefore
   partial and conditional: satisfying part (a) does not discharge part (b).
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


## Implementation acceptance rules

If B2A is explicitly authorized by the founder, implementation acceptance
requires the following rules in addition to the criteria above.

- `split_summary` descriptor hashes only canonical bytes of `SplitSummaryIdentityCore`.
- Those bytes exclude `split_fingerprint`, authoritative use of B1 `split_hash`, dates, timestamps, provenance, runtime metadata, paths, hostnames, usernames, command logs, and environment data.
- `SplitFingerprintRecord` is produced only after the fingerprint is calculated.
- `SplitFingerprintRecord` is not one of its own four fingerprint inputs.
- A display or final summary may include the computed fingerprint after calculation, but its final bytes are not recursively fingerprinted.

Proposed validation sequence:

1. Canonicalize fingerprint-free `SplitSummaryIdentityCore`.
2. Calculate its `split_summary` descriptor.
3. Validate all four required descriptors.
4. Construct `SplitFingerprintIdentity`.
5. Canonicalize that identity.
6. Compute the full SHA-256 fingerprint.
7. Construct `SplitFingerprintRecord`.
8. Recompute all bound hashes, byte sizes, and final fingerprint during verification.
9. Reject every mismatch.

Exact schema identifiers for version 1:

- `split_summary`: `mesc-pilot-01-split-summary-identity-core/1`
- `excluded_ledger`: `mesc-pilot-01-excluded-ledger/1`
- `bundle`: `mesc-pilot-01-split-fingerprint-bundle/1`
- `group_registry`: `mesc-pilot-01-group-registry/1`
- `example_registry`: `mesc-pilot-01-example-registry/1`

Object keys are sorted by ascending Unicode code-point sequence using direct,
case-sensitive string comparison. Ordering is not locale-aware, case-folded,
normalized, filesystem-derived, or insertion-order-derived. Strings that cannot
be encoded as valid UTF-8 must fail closed with `canonicalization_failure`.
