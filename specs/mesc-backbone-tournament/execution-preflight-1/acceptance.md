# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **CANDIDATE ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-20

The preflight is complete only if every requirement below is satisfied on one exact canonical input state.

## A. Canonical ancestry and input identity

1. canonical base SHA is recorded and contains PR #130 in ancestry;
2. canonical base tree is recorded;
3. every frozen Repair-2 artifact consumed by the audit is identified by repository path and Git blob SHA;
4. the following declared SHA-256 bindings match the exact bytes consumed:
   - corpus specification;
   - compressed corpus storage artifact;
   - decompressed logical corpus;
   - corpus manifest;
   - logical scoring keys and every scoring-key shard;
   - prompt/parser/scoring/protocol/report-validation/report-schema contracts as applicable;
5. no corpus substitution, regeneration, or rematerialization is permitted.

## B. R2 provenance audit

A committed deterministic audit artifact must report `RESULT = PASS` only if all are true:

1. exactly 240 model-visible synthetic/hand-authored payload records are present;
2. Pilot-01 content is absent;
3. real patient/clinician records, PHI, product telemetry, credentialed clinical data, and external benchmark examples are absent;
4. every payload is self-contained synthetic/hand-authored material under the frozen R2 policy;
5. model-visible payload contains no gold answer/scoring-key fields;
6. every evidence reference used by a scoring key resolves to evidence present in that item's payload;
7. the audit records deterministic input hashes, check counts, failure records, result, and audit SHA-256.

Any unresolved provenance ambiguity or prohibited-source indication => `BLOCKED`.

## C. Corpus specification / manifest conformance audit

A second committed deterministic audit artifact must report `RESULT = PASS` only if all are true:

1. decompressed logical corpus SHA-256 equals `48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd`;
2. compressed storage SHA-256 equals `667cd68e5ccc9356321eb5857c6e9203e1320ec33d866ccf514411c211ceb632`;
3. logical corpus count is exactly 240;
4. canonical item IDs are exactly `BT-A-001..040` through `BT-F-001..040`, each once, in frozen order;
5. each axis has exactly 40 records;
6. archetype assignment and difficulty bands match `corpus-specification.json`;
7. each item uses the frozen task-template binding for its axis;
8. expected answer-state/scoring-key fields conform to the frozen schemas/contracts;
9. logical scoring-key count is exactly 240 and its SHA-256 equals `bb3524bc8dd1f05bad433c664ac3c48a5110939ac78b5ffa2ad8853f944c6318`;
10. each manifest shard count/hash/byte-length binding is reproduced;
11. no duplicate, missing, extra, reordered, or malformed item is accepted;
12. the audit records deterministic input hashes, check counts, failure records, result, and audit SHA-256.

Any mismatch => `BLOCKED`.

## D. Remaining execution-binding inventory

The result must explicitly report the status of every `FD-MESC-BT-EXEC-1` mandatory pre-activation binding:

- exact canonical code SHA/tree;
- selected candidate subset (`>=2` distinct) — may remain `UNBOUND` in preflight;
- tokenizer/processor/custom-code revisions;
- exact hardware/provider/runtime/precision identity — may remain `UNBOUND` in preflight;
- peak-VRAM and latency measurement capability;
- gated-access authorization status;
- bounded run attempts and artifact destinations;
- audit artifact SHA-256 values;
- exact report-validation/report-schema bindings;
- later exact-head CI/review/merge gates.

An `UNBOUND` execution item must remain explicitly blocking for execution; it does not make a successful corpus audit false.

## E. Terminal state

The preflight may conclude:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

only when sections A–C pass and section D truthfully lists every remaining execution blocker.

Otherwise:

```text
BLOCKED
```

Neither terminal state authorizes model access or execution. Only a separately reviewed and canonically adopted `FD-MESC-BT-EXEC-1` can do that.
