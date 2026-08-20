# Plan — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **PRE-EXECUTION PLAN / MODEL ACCESS PROHIBITED**

## Phase 1 — Metadata-only replay proof, protected atomic claim, then exact input verification

### Phase 1A — Pre-claim metadata only

Before claim creation, perform **metadata-only** checks. Do not read, hash, parse, decompress, or derive values from any frozen Repair-2 artifact content, including `task-prompts.json`, corpus bytes, scoring-key bytes, parser/scoring/report JSON, or other content blobs.

Permitted pre-claim operations are limited to:

- record then-current canonical authorization merge SHA/tree;
- mechanically require Repair-2 canonical merge `0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3` / tree `60e900daecea1cb9e64db95314bf9358387072b7` in ancestry; do not use a PR number as the predicate;
- compare the expected Repair-2 repository paths to their Git blob IDs from the canonical tree, without reading blob contents;
- derive `ACTIVATION_RECEIPT_ID` only from the exact ordered four-file authorization-package path/blob-ID preimage under `MESC-BT-PREFLIGHT-RECEIPT-V1`;
- use exactly `RESULT_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/` and `RESULT_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>`; `RESULT_REF_PREFIX` is a literal ref-name prefix, never a glob;
- use exactly `CLAIM_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/` and `CLAIM_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>`; `CLAIM_REF_PREFIX` is also a literal ref-name prefix, never a glob;
- for both prefixes, define membership as full ref name starts with that exact prefix; the only well-formed descendant shape is exactly two non-empty path segments after the prefix, `<AUTHORIZATION_MERGE_SHA>` as 40 lowercase hexadecimal characters and `<ACTIVATION_RECEIPT_ID>` as 64 lowercase hexadecimal characters; any other descendant under either prefix => `BLOCKED`;
- independently and exhaustively enumerate every ref whose full name starts with `RESULT_REF_PREFIX` **and** every ref whose full name starts with `CLAIM_REF_PREFIX` from the authoritative Git hosting ref store, consuming every page/cursor for each prefix until completeness of both enumerations is mechanically proven;
- traverse the **complete canonical history** reachable from then-current `main`, following every parent edge to repository roots; prove the authoritative object graph is not shallow/truncated and that every reachable commit/parent edge in scope was visited;
- enumerate the **complete PR population in open and closed/merged states**, consuming every page/cursor, and inspect every preflight-result PR metadata record relevant to the decision/receipt/result identity;
- treat any failed request, missing object, permission limit, shallow boundary, truncation, partial pagination, omitted page/cursor, malformed ref, or otherwise non-exhaustive ref/history/PR search as `BLOCKED` before claim creation;
- treat any exact `RESULT_REF` or exact `CLAIM_REF` as replay evidence preventing `UNUSED`, and treat any malformed/unexpected descendant under either prefix as `BLOCKED`;
- integrity-check existing exact refs rather than merely counting them: `CLAIM_REF` must be readable and target exactly `AUTHORIZATION_MERGE_SHA`; `RESULT_REF` must be readable and either equal that SHA at initial issuance or be a lifecycle-valid ordinary-fast-forward descendant on the single result lineage; unreadable, non-descendant, force/sideways-retargeted, or state-inconsistent targets => `BLOCKED`;
- classify state using the mutually exclusive predicates and precedence in `acceptance.md`: terminal → in-progress → claim-only → unused, with any conflict/ambiguity => `BLOCKED`;
- require the state to be provably `UNUSED`;
- mechanically prove storage-boundary protection for both prefixes: `CLAIM_REF_PROTECTION` must permit controlled first creation while denying all later claim updates/force-updates/deletions and worker bypass; `RESULT_REF_PROTECTION` must permit controlled first creation at the authorization SHA and then only designated-principal expected-old-target ordinary fast-forwards on the single authorization-descendant result lineage, deny force/non-fast-forward retargets/deletion/recreation, and support terminal freeze against all later updates/deletion;
- if any replay search, exact-ref target check, or protection cannot be proven, terminate `BLOCKED` before claim creation and before any frozen-content read.

### Phase 1B — Atomic claim and protected non-self-referential result-ref activation lifecycle

- atomically create exactly `CLAIM_REF` with create-only semantics and target exactly the canonical authorization merge SHA;
- if creation reports an existing claim or otherwise cannot prove exclusive creation, stop immediately without modifying/deleting the existing ref and without any frozen-content read;
- immediately re-read the claim ref and both protection mechanisms; any missing/changed claim target, deletion evidence, or protection drift => `BLOCKED` and the episode is permanently non-reusable; absence of a later terminal receipt cannot restore `UNUSED`;
- atomically create exactly `RESULT_REF` with create-only semantics and target it exactly to the canonical authorization merge SHA; if it already exists or exclusive creation cannot be proven => `BLOCKED` before any frozen-content read;
- immediately re-read the exact initial result-ref target and `RESULT_REF_PROTECTION`; unreadable/mismatched target or protection drift => `BLOCKED`;
- construct `activation-receipt.json` and an activation commit whose single parent is exactly the canonical authorization merge SHA; the receipt records `result_ref_activation_parent = AUTHORIZATION_MERGE_SHA`, both protection identities/enforcement facts, `state = IN_PROGRESS`, and `content_read_started = false`, but it MUST NOT contain the SHA of the activation commit that contains it;
- after the activation commit object exists and its SHA is known, atomically fast-forward `RESULT_REF` from exactly the authorization merge SHA to that commit using compare-and-swap/expected-old-target semantics;
- re-read `RESULT_REF`, require the exact observed activation commit SHA, inspect that commit and require its single parent to equal the authorization merge SHA and its tree to contain the exact expected activation-receipt bytes; define that externally observed SHA as `RESULT_REF_ACTIVATION_COMMIT`;
- interpret `state = IN_PROGRESS` as the replay state created by publication of activation/result evidence; `content_read_started = false` records only the issuance-time content-access fact;
- do not read any frozen Repair-2 content until that protected activation fast-forward is published and re-read/structurally verified successfully;
- after activation, advance `RESULT_REF` only through designated-principal expected-old-target ordinary fast-forwards on the same authorization-descendant episode lineage; force/non-fast-forward updates, sideways retargets, deletion, recreation, unexpected updaters, and ancestry breaks => `BLOCKED`;
- terminal closure is two commits: first a byte-final `TERMINAL_CONTENT_COMMIT` containing the result package and manifest but no `consumption-receipt.json`; then a direct-child `TERMINAL_RECEIPT_COMMIT` adding only `consumption-receipt.json` and altering no bound result artifact;
- the terminal receipt binds the already-known `RESULT_REF_ACTIVATION_COMMIT`, already-known `TERMINAL_CONTENT_COMMIT`, final manifest SHA-256, claim/ref identities, protection facts, and terminal state, but MUST NOT contain the SHA of its own containing `TERMINAL_RECEIPT_COMMIT`;
- fast-forward `RESULT_REF` from exactly `TERMINAL_CONTENT_COMMIT` to the externally observed `TERMINAL_RECEIPT_COMMIT`, re-read and verify the exact parent/tree relation, then freeze the ref against every further update/delete through and after canonical result adoption.

### Phase 1C — Post-claim exact frozen-input verification

Only after Phase 1B succeeds:

- read the exact frozen Repair-2 blobs identified by the canonical path→Git-blob map;
- verify every frozen byte-level SHA-256 binding listed in `README.md` / `acceptance.md`;
- verify the canonical corpus manifest shard hash/count/byte-length bindings;
- parse `task-prompts.json` with duplicate-member rejection and reproduce exact `SYSTEM_PROMPT_SHA256`;
- reproduce `PROMPT_PROTOCOL_SHA256` from its exact canonical four-field preimage;
- verify prompt/parser/scoring/protocol/report contract bytes and digests;
- fail closed on any mismatch or if any pre-claim content access is discovered.

The logical episode state is already `IN_PROGRESS` once the activation receipt/result ref exists. The first post-claim frozen-content operation does not create a new replay state.

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

## Phase 5 — Complete result-package binding and non-self-referential terminal closure

Create the four unconditional core outputs:

1. `r2-provenance-audit.json`;
2. `corpus-conformance-audit.json`;
3. `execution-binding-inventory.md`;
4. `preflight-verdict.md`.

Before constructing the manifest binding core, determine whether a successor candidate is provisionally eligible under `acceptance.md`. Provisional eligibility requires Sections A–D PASS plus a complete/truthful inventory for the ready path. If eligible, render exactly one `FD-MESC-BT-EXEC-1-CANDIDATE-V2` at `execution-authorization-candidate.md` solely as a hash input, normalize its Markdown bytes exactly as specified, and compute its exact SHA-256 and byte length. Provisional rendering grants no authority. If not eligible, no successor file may exist and `successor_candidate = null`.

Then bind and close the result without a digest or commit-identity cycle:

1. hash both canonical audit files and the exact execution-binding inventory bytes;
2. build the exact `manifest_binding_core` defined in `acceptance.md`, binding authorization merge SHA/tree, all frozen Repair-2 input digests, the three known output paths/hashes, the verdict path, and either the exact successor-candidate id/path/SHA-256/byte-length object or `null`;
3. compute `MANIFEST_BINDING_CORE_SHA256` over the canonical binding-core JSON bytes;
4. generate `preflight-verdict.md` containing that exact core hash and terminal state, then compute its full-file SHA-256;
5. generate canonical `preflight-result-manifest.json` containing the full binding core plus exact path/SHA-256/byte-length entries for all four unconditional core outputs and the successor candidate when present;
6. if any later acceptance, claim, protection, binding, or package check forces `BLOCKED`, remove any provisionally rendered successor, set `successor_candidate = null`, and rebuild the core, verdict, and manifest; stale hashes are invalid;
7. compute the full manifest SHA-256 externally; do not insert it into the manifest itself;
8. once the terminal result artifacts are byte-final, create `TERMINAL_CONTENT_COMMIT` on the permitted result lineage containing the exact package/manifest and no `consumption-receipt.json`; after its SHA is known, fast-forward `RESULT_REF` to it using expected-old-target semantics and re-read it;
9. generate canonical `consumption-receipt.json` outside the manifest artifact set for the terminal outcome:
   - ready terminal => `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, `state = CONSUMED`;
   - blocked terminal => `terminal_state = BLOCKED`, `state = BLOCKED`;
   - both forms bind the same activation receipt identity, exact claim ref/target, exact claim-protection identity and terminal re-verification facts, exact `result_ref`, exact already-observed `result_ref_activation_commit`, exact already-observed `result_ref_terminal_content_commit`, result-ref protection/lifecycle facts, and exact final result-manifest SHA-256;
   - the receipt MUST NOT contain the SHA of the commit that will contain the receipt;
10. create `TERMINAL_RECEIPT_COMMIT` as the direct child of `TERMINAL_CONTENT_COMMIT`, with the only tree delta being addition of `consumption-receipt.json`; atomically fast-forward `RESULT_REF` from exactly the content commit to that receipt commit, re-read the exact target and parent/tree relation, then freeze result-ref protection against every later update/delete;
11. publish both the final manifest SHA-256 and externally observed `TERMINAL_RECEIPT_COMMIT` SHA in the result PR description as independently reviewable bindings.

Any edit to any bound result artifact, including a present successor candidate, must change the manifest binding and invalidate stale evidence. Any self-referential commit-SHA field or terminal receipt commit that changes another bound artifact => `BLOCKED`.

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

A claimed episode that reaches terminal-package construction must carry the matching terminal `consumption-receipt.json` through the two-commit closure above. A claimed episode that cannot reach terminal receipt closure is still burned and cannot silently restart under this authorization; the claim/result/history evidence prevents `UNUSED` even without a terminal receipt. Any observation that the protected claim was later deleted, changed, retargeted, or became bypassable, or that `RESULT_REF` violated its protected single-lineage lifecycle/frozen target, forces `BLOCKED` and can never restore `UNUSED`.

## Phase 8 — Independent exact-head result gate and terminal claim/result-ref verification

Before canonical adoption of the preflight result:

- exact-head CI = PASS;
- exact-head CodeQL = PASS;
- fresh independent exact-head review = no blocker;
- zero unresolved blocking review threads;
- Ready only after all gates;
- expected-head merge protection;
- immediately before merge, re-read the exact claim ref, exact result ref, and both storage-boundary protections and require all unchanged from their required terminal state;
- require `CLAIM_REF` still points to the exact authorization merge SHA;
- require `RESULT_REF` to point exactly to the externally observed `TERMINAL_RECEIPT_COMMIT`/result PR HEAD; require that commit to have exactly one parent equal to the receipt's bound `result_ref_terminal_content_commit`, require the parent to be a permitted fast-forward descendant of the authorization SHA on the single episode lineage, and require the receipt commit tree delta to add only `consumption-receipt.json` while leaving all manifest-bound result artifacts byte-identical;
- require terminal result-ref protection to deny every further update/delete;
- post-merge canonical SHA/tree/ordered-parent/signature verification;
- verify the canonical merged `consumption-receipt.json` against the exact final manifest SHA-256 and its bound activation/content commit identities;
- verify its state matches the verdict (`CONSUMED` for ready, `BLOCKED` for blocked);
- verify the permanent claim ref still exists, points to the exact authorization merge SHA, and remains protected against update/force-update/delete without worker bypass;
- verify the permanent frozen result ref still exists at the exact externally observed terminal receipt commit with its protection/freeze evidence intact;
- any claim/result-ref/protection/parent-tree integrity failure => terminal `BLOCKED`; it never permits replay or reclassification as `UNUSED`.

## Execution remains out of scope

This plan never sends a prompt to a model and never accesses model weights. A later `FD-MESC-BT-EXEC-1` authorization package must separately bind the selected candidate subset, exact runtime/provider/hardware, run bounds, artifact destinations, any gated-access decision, and all remaining activation requirements.
