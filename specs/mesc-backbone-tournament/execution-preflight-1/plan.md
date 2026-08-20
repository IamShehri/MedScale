# Plan — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **PRE-EXECUTION PLAN / MODEL ACCESS PROHIBITED**

## Phase 1 — Exact canonical input capture, replay proof, and atomic claim

- record then-current canonical authorization merge SHA/tree;
- mechanically require Repair-2 canonical merge `0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3` / tree `60e900daecea1cb9e64db95314bf9358387072b7` in ancestry; do not use a PR number as the predicate;
- verify the complete Repair-2 repository path→Git-blob map and every frozen SHA-256 binding listed in `README.md` / `acceptance.md`;
- verify the exact `SYSTEM_PROMPT_SHA256` and `PROMPT_PROTOCOL_SHA256` derivations from their bound source blobs;
- derive `ACTIVATION_RECEIPT_ID` from the exact ordered four-file authorization-package preimage under `MESC-BT-PREFLIGHT-RECEIPT-V1`;
- search canonical history plus every open/closed preflight-result PR for prior claim/receipt/episode evidence;
- require the state to be provably `UNUSED`; `ISSUED`, `IN_PROGRESS`, `BLOCKED`, `CONSUMED`, conflicting, or ambiguous evidence rejects reuse;
- before any audit or corpus-content inspection, atomically create the immutable claim ref defined in `acceptance.md` with create-only semantics and target exactly the canonical authorization merge SHA;
- if claim creation reports an existing ref or otherwise fails to prove exclusive creation, stop immediately without audit work and without modifying/deleting the existing claim;
- after successful claim only, create the unique preflight-result branch and matching `activation-receipt.json`;
- fail closed if any frozen binding, receipt, state, or claim invariant cannot be reproduced.

## Phase 2 — Deterministic R2 provenance audit

- verify compressed corpus storage identity before decompression;
- decompress the exact committed `materialized-corpus.jsonl.gz`;
- parse every one of the 240 JSONL records;
- reject duplicate JSON member names at every nesting level before any canonical JSON interpretation/hash operation;
- validate R2 source prohibitions over every payload;
- verify payload/gold separation;
- verify every scoring-key evidence reference resolves to the same item's model-visible evidence;
- emit `r2-provenance-audit.json` using `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` exactly; the audit contains no self-digest field.

## Phase 3 — Full corpus/spec/manifest conformance audit

- reproduce compressed and decompressed corpus SHA-256 values;
- reproduce logical scoring-key and every per-shard hash/count/byte-length binding;
- require the exact canonical item-ID set and order;
- require six axes × 40 items;
- recompute archetype and difficulty assignment from the frozen rule;
- verify axis task-template bindings and scoring-key contract compatibility;
- emit `corpus-conformance-audit.json` using the same canonical JSON rule and no self-digest field.

## Phase 4 — Execution-binding inventory

Without model access:

- carry forward only the four already-admitted immutable candidate identities;
- do not add a challenger;
- do not request or accept gated terms;
- do not finalize an execution subset until exact hardware/provider/runtime feasibility is bound;
- identify which candidates are public/ungated versus gated;
- identify the Phi-4 exact-revision `trust_remote_code` security binding as a later execution requirement;
- record every still-unbound execution requirement explicitly in `execution-binding-inventory.md`;
- serialize that Markdown as UTF-8 without BOM, LF line endings, exactly one final LF, then compute its full-file SHA-256.

## Phase 5 — Complete result-package binding

Create the four unconditional core outputs:

1. `r2-provenance-audit.json`;
2. `corpus-conformance-audit.json`;
3. `execution-binding-inventory.md`;
4. `preflight-verdict.md`.

Before constructing the manifest binding core, determine whether a successor candidate is provisionally eligible under `acceptance.md`. Provisional eligibility requires Sections A–D PASS plus a complete/truthful inventory for the ready path. If eligible, render exactly one `FD-MESC-BT-EXEC-1-CANDIDATE-V2` at `execution-authorization-candidate.md` solely as a hash input, normalize its Markdown bytes exactly as specified, and compute its exact SHA-256 and byte length. Provisional rendering grants no authority. If not eligible, no successor file may exist and `successor_candidate = null`.

Then bind the result without a digest cycle:

1. hash both canonical audit files and the exact execution-binding inventory bytes;
2. build the exact `manifest_binding_core` defined in `acceptance.md`, binding authorization merge SHA/tree, all frozen Repair-2 input digests, the three known output paths/hashes, the verdict path, and either the exact successor-candidate id/path/SHA-256/byte-length object or `null`;
3. compute `MANIFEST_BINDING_CORE_SHA256` over the canonical binding-core JSON bytes;
4. generate `preflight-verdict.md` containing that exact core hash and terminal state, then compute its full-file SHA-256;
5. generate canonical `preflight-result-manifest.json` containing the full binding core plus exact path/SHA-256/byte-length entries for all four unconditional core outputs and the successor candidate when present;
6. if any later acceptance, claim, receipt, binding, or package check forces `BLOCKED`, remove any provisionally rendered successor, set `successor_candidate = null`, and rebuild the core, verdict, and manifest; stale hashes are invalid;
7. compute the full manifest SHA-256 externally; do not insert it into the manifest itself;
8. generate canonical `consumption-receipt.json` outside the manifest artifact set for **both** terminal outcomes:
   - ready terminal => `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, `state = CONSUMED`;
   - blocked terminal => `terminal_state = BLOCKED`, `state = BLOCKED`;
   - both forms bind the same activation receipt identity, immutable claim ref, and exact final result-manifest SHA-256;
9. publish the final manifest SHA-256 in the result PR description as an independently reviewable binding.

Any edit to any bound result artifact, including a present successor candidate, must change the manifest binding and invalidate stale evidence.

## Phase 6 — Single successor execution-authorization candidate

The successor lifecycle is strictly two-stage:

1. provisional rendering after Sections A–D PASS and inventory readiness is permitted only to compute Section E hashes;
2. the provisional file is not authoritative and grants no execution authority;
3. it becomes a valid inactive preflight output only when Sections A–G all pass and the terminal package is ready;
4. any later failure removes it, sets `successor_candidate = null`, and rebuilds the blocked package.

The only permitted successor identity/path is:

```text
CANDIDATE_ID = FD-MESC-BT-EXEC-1-CANDIDATE-V2
AUTHORITATIVE_PATH = specs/mesc-backbone-tournament/execution-preflight-1-result/execution-authorization-candidate.md
```

The prior `readiness-repair-2-result/execution-authorization-candidate.md` is immutable historical seed evidence and is superseded only after the V2 result package is canonically merged and post-merge verified. The successor remains inactive and grants no execution authority.

## Phase 7 — Preflight result

Terminal result is only:

- `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, or
- `BLOCKED`.

Every claimed episode must carry the matching terminal `consumption-receipt.json`. A blocked or otherwise burned episode cannot silently restart under this authorization.

## Phase 8 — Independent exact-head result gate

Before canonical adoption of the preflight result:

- exact-head CI = PASS;
- exact-head CodeQL = PASS;
- fresh independent exact-head review = no blocker;
- zero unresolved blocking review threads;
- Ready only after all gates;
- expected-head merge protection;
- post-merge canonical SHA/tree/ordered-parent/signature verification;
- verify the canonical merged terminal `consumption-receipt.json` against the exact final manifest SHA-256;
- verify its state matches the verdict (`CONSUMED` for ready, `BLOCKED` for blocked);
- verify the immutable claim ref still exists and points to the exact authorization merge SHA.

## Execution remains out of scope

This plan never sends a prompt to a model and never accesses model weights. A later `FD-MESC-BT-EXEC-1` authorization package must separately bind the selected candidate subset, exact runtime/provider/hardware, run bounds, artifact destinations, any gated-access decision, and all remaining activation requirements.
