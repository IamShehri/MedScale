# MESC Pilot-01 — P01-04B2A Specification

Status:
**PROPOSED AUTHORIZATION GATE — FOUNDER DECISION PENDING**

Implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Canonical planning baseline:
`1a9169f7229bb72eba6772448724c54ec71937c5`

---

## Functional scope

P01-04B2A defines deterministic artifact types and canonical in-memory
serialization for future P01-04B outputs. B2A types must be private
immutable contracts that do not modify B1 behavior.

B2A may later provide:

- `CanonicalJsonValue` typing and canonical JSON/JSONL serialization;
- artifact descriptor records for deterministically produced registry and
  summary outputs;
- a non-circular two-layer split-fingerprint identity model;
- typed fail-closed validation errors for contract violations.

## Non-goals

B2A does not authorize and does not reference:

- leakage detection, normalization, or classification;
- fixture facade, public splitter activation, or execution entry points;
- CLI, filesystem publication, atomic rename/write behavior, or side effects;
- real P01-03G loading, partition generation, dataset access, model access,
  inference, training, metrics, benchmark evaluation, or clinical claims;
- P01-04C–G or P01-05 or later.

## Deterministic behavior

All B2A serializers operate over caller-supplied Python objects and return
bytes only. They perform no filesystem I/O and emit no runtime metadata.
Canonical output must be byte-identical for the same logical input across
authorized Python runtimes when locale and timezone are uncontrolled.

## Validation behavior

B2A validation is strict and fail-closed. Unsupported or prohibited value
types raise typed private errors. Floating-point values are prohibited in
fingerprinted promotable payloads. Binary floating-point quantities required
later must use integer, versioned fixed-point, or canonical decimal-string
representation frozen by contract.

## Security and provenance boundaries

B2A must not accept, retain, or emit:

- dates, timestamps, local paths, usernames, hostnames, runtime versions,
  command logs, environment data, or the authoritative fingerprint itself;
- per-example answer labels, raw question text, or raw context text in
  promoted identity inputs;
- binary floating-point values in fingerprinted payloads;
- B1 mutable state or public API surface changes;

D1–D10 and FD-B2-1 through FD-B2-8 remain controlling on conflict.

## No-filesystem and no-CLI boundary

B2A artifacts remain in-memory only. Filesystem writes, atomic publication,
CLI surfaces, and integration fixtures are out of scope for B2A and require
separate founder authorization.


## Non-circular fingerprint proposal

The following behavior is proposed as a pending founder decision and is not
authoritative until explicitly ratified.

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
