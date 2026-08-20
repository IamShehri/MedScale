# Plan — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **PRE-EXECUTION PLAN / MODEL ACCESS PROHIBITED**

## Phase 1 — Exact canonical input capture

- record then-current canonical `main` SHA/tree;
- require PR #130 in ancestry;
- enumerate exact Repair-2 artifact paths, Git blob SHAs, byte lengths, and frozen SHA-256 values;
- fail closed if any frozen binding has moved or cannot be reproduced.

## Phase 2 — Deterministic R2 provenance audit

- decompress the exact committed `materialized-corpus.jsonl.gz` only after storage SHA verification;
- parse every one of the 240 JSONL records;
- validate R2 source prohibitions over every payload;
- verify payload/gold separation;
- verify every scoring-key evidence reference resolves to the same item's model-visible evidence;
- emit a closed, sorted-key JSON audit artifact with explicit PASS/FAIL checks and negative findings.

## Phase 3 — Full corpus/spec/manifest conformance audit

- reproduce compressed and decompressed corpus SHA-256 values;
- reproduce logical scoring-key and per-shard hashes/counts/byte lengths;
- require the exact canonical item-ID set and order;
- require six axes × 40 items;
- recompute archetype and difficulty assignment from the frozen rule;
- verify axis task-template bindings and scoring-key contract compatibility;
- emit a second closed, sorted-key JSON audit artifact with explicit PASS/FAIL checks and negative findings.

## Phase 4 — Execution-binding inventory

Without model access:

- carry forward only the four already-admitted immutable candidate identities;
- do not add a challenger;
- do not request or accept gated terms;
- do not finalize an execution subset until exact hardware/provider/runtime feasibility is bound;
- identify which candidates are public/ungated versus gated;
- identify the Phi-4 exact-revision `trust_remote_code` security binding as a later execution requirement;
- record every still-unbound execution requirement explicitly.

## Phase 5 — Preflight result

Create a result package containing:

- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`;
- exact SHA-256 values for both audit artifacts.

Terminal result is only:

- `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, or
- `BLOCKED`.

## Phase 6 — Independent exact-head gate

Before canonical adoption of the preflight result:

- exact-head CI = PASS;
- exact-head CodeQL = PASS;
- fresh independent exact-head review = no blocker;
- zero unresolved blocking review threads;
- Ready only after all gates;
- expected-head merge protection;
- post-merge canonical SHA/tree/ordered-parent/signature verification.

## Execution remains out of scope

This plan never sends a prompt to a model and never accesses model weights. A later `FD-MESC-BT-EXEC-1` authorization package must separately bind the selected candidate subset, exact runtime/provider/hardware, run bounds, artifact destinations, any gated-access decision, and all remaining activation requirements.
