# Plan — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **PRE-EXECUTION PLAN / MODEL ACCESS PROHIBITED**

`acceptance.md` is normative. This plan defines execution order and MUST NOT weaken its replay, protection, CAS, graph/tree, receipt, or adoption-verification requirements.

## Phase 1A — Pre-claim replay proof; frozen Repair-2 content prohibited

Before claim creation:

- do not read/hash/parse/decompress/derive from any frozen Repair-2 corpus, prompt, scoring-key, parser/scoring/report contract, or other frozen content;
- inspect only authorization/replay Git metadata plus permitted non-Repair-2 episode receipts and the exact marker-delimited PR evidence block defined in `acceptance.md` from structurally selected current-episode preflight-result PRs;
- do not fetch or interpret PR patches, diffs, changed-file contents, review comments, or free-form PR prose outside that evidence block;
- verify the exact Repair-2 canonical merge `0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3` / tree `60e900daecea1cb9e64db95314bf9358387072b7` in ancestry;
- verify the complete Repair-2 path→Git-blob identity map without reading those blobs;
- derive `ACTIVATION_RECEIPT_ID` only from the exact ordered four-file authorization-package Git metadata preimage;
- use the literal `RESULT_REF_PREFIX` / `CLAIM_REF_PREFIX` and exact current episode refs from `acceptance.md`;
- define `PREFLIGHT_RESULT_PR_AUTH_PREFIX = governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/` and `PREFLIGHT_RESULT_PR_HEAD_REF = governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>` exactly as in `acceptance.md`;
- apply both deterministic PR classification rules from `acceptance.md` to every enumerated PR: (1) the **current-episode selector**, requiring base repo=`TheHalfMoon/MESC`, base ref=`main`, head repo=`TheHalfMoon/MESC`, and retained head ref exactly `PREFLIGHT_RESULT_PR_HEAD_REF`; and (2) the **current-authorization namespace-conflict detector**, under which any PR with head repo=`TheHalfMoon/MESC` and retained head ref beginning with `PREFLIGHT_RESULT_PR_AUTH_PREFIX` is valid only if it also satisfies the current-episode selector;
- PR state is not a selector; title/labels/reviews/issue linkage/author/free-form body never select it. A reserved-namespace PR with a different receipt suffix, malformed/non-64-lowercase-hex suffix, extra segment, wrong base repo/ref, or any other non-current structure => `BLOCKED`, even when its branch/ref was deleted;
- when a current-episode selected PR exposes a current head OID, require it to equal the authoritative `RESULT_REF` target in the same replay snapshot; when the branch was deleted and the OID is unavailable, retain the PR as replay evidence and reconcile its lifecycle through history, permitted receipts, and the exact evidence block; missing structural fields, unreconcilable selected PRs, incomplete classification, or any reserved-namespace conflict => `BLOCKED`;
- validate every descendant syntax; for the current authorization SHA, any same-SHA ref with a different receipt ID is conflicting sibling evidence and => `BLOCKED`;
- exhaustively enumerate every result-prefix ref and every claim-prefix ref, consuming all pages/cursors;
- traverse all canonical history reachable from then-current `main`, following every parent to roots and proving no shallow/truncated boundary;
- enumerate the full open + closed/merged PR population, consuming all pages/cursors, apply **both** deterministic PR classification rules to every PR, reject any namespace conflict, and inspect only current-episode selected PR structural records plus their exact evidence blocks;
- require the PR evidence object keyset/version and replay-snapshot keyset/version exactly as defined in `acceptance.md`; unknown/duplicate/missing keys or wrong constant values fail closed;
- reject failed/permission-limited/truncated/incomplete searches, unreadable required PR structural fields, incomplete PR classification, and malformed/conflicting evidence fail-closed;
- validate exact claim/result targets and, for result targets, the required commit graph/tree/lifecycle/CAS evidence using only permitted non-Repair-2 episode evidence;
- classify replay state with terminal canonical receipt → in-progress → claim-only → unused precedence; any ambiguity => `BLOCKED`;
- require proven `UNUSED`.

### Replay/claim linearization

1. After the first complete replay search, construct canonical `PRECLAIM_REPLAY_SNAPSHOT` exactly as defined in `acceptance.md`: exact top-level keys `snapshot_version`, `authorization_merge_sha`, `activation_receipt_id`, `main_tip`, `history_reachable_commit_count`, `history_graph_sha256`, `result_refs`, `claim_refs`, `selected_prs`; `snapshot_version` exactly `MESC-BT-PREFLIGHT-REPLAY-SNAPSHOT-V1`; exact per-array record schemas/order; exact history-graph preimage/digest.
2. Immediately before claim creation, repeat all four exhaustive searches and require the canonical snapshot bytes to be byte-identical.
3. Atomically create exactly `CLAIM_REF` create-only at `AUTHORIZATION_MERGE_SHA`.
4. Immediately repeat all four searches again before creating `RESULT_REF`; the only permitted relevant delta is appearance of that exact claim at that exact target.
5. `main_tip`, history digest/count, result refs, sibling claim refs, and selected PR evidence must otherwise remain identical. Any other change => `BLOCKED`, no result-ref creation, no frozen-content read. The claim remains permanent replay evidence and the episode is burned/non-reusable.

## Phase 1B — Server protections and atomic result-ref update protocol

Before claim creation, prove:

- `CLAIM_REF_PROTECTION = PASS`: controlled initial creation, then no update/force-update/delete, with no configured repository/organization bypass actor capable of mutation;
- `RESULT_REF_PROTECTION = PASS`: before terminal freeze, only the designated preflight principal may make ordinary fast-forwards on the single authorization-descendant result lineage; no force/non-fast-forward retarget, delete/recreate, other-principal update, or configured repository/organization administrative/automation bypass; terminal frozen state denies every later update/delete with no configured bypass;
- `RESULT_REF_CAS_PROTOCOL` exists and is usable: every post-creation update is one atomic operation with full ref, immediately re-read `expected_old_oid`, `new_oid`, server-side stale-old rejection, and no mutation on mismatch;
- `RESULT_REF_CAS_EVIDENCE` can be preserved externally for every attempt: protocol identity, ref, expected old OID, new OID, outcome, observed post-target, and pre/post server-protection identity/version.

Git receive-pack old/new/ref semantics or an equivalent explicit old-OID-precondition hosting operation qualifies. Read + unconditional PATCH does not. If any required protection/CAS capability/evidence path cannot be proven, stop `BLOCKED` before claim creation and before any frozen-content read.

## Phase 1C — Result ref creation, activation, and content-read gate

After successful claim creation and post-claim snapshot revalidation:

1. create `RESULT_REF` create-only at `AUTHORIZATION_MERGE_SHA` and re-read the exact target/protection;
2. construct an activation commit with exactly one parent=`AUTHORIZATION_MERGE_SHA` and only one tree delta: add `RESULT_ROOT/activation-receipt.json`;
3. activation receipt records authorization parent, current protection identity/version, selected CAS protocol, `state = IN_PROGRESS`, and `content_read_started = false`, but never its own containing commit SHA;
4. once activation commit SHA is known, immediately re-read target + protection and require the approved values;
5. atomically CAS from authorization SHA to activation SHA; preserve CAS evidence;
6. re-read target + protection; validate exact activation parent/tree/receipt; reconcile CAS evidence;
7. only then define external `RESULT_REF_ACTIVATION_COMMIT` and permit frozen Repair-2 content access.

Any target/protection/graph/tree/CAS drift => `BLOCKED`; frozen-content access remains prohibited.

## Phase 1D — Exact RESULT_REF graph/tree contract

```text
RESULT_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-result/
```

Allowed paths only:

- `activation-receipt.json`;
- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`;
- `preflight-result-manifest.json`;
- conditional `execution-authorization-candidate.md`;
- terminal-only `consumption-receipt.json`.

Every post-creation `RESULT_REF` target commit has exactly one parent; merge commits are forbidden. Parent must equal the immediately previous valid ref target / CAS expected-old OID. Every tree delta is confined to `RESULT_ROOT`.

- Activation commit: only adds activation receipt.
- Intermediate result commits: may add/update only non-terminal outputs; activation receipt immutable; no consumption receipt; candidate deletion only for required blocked-package rebuild; no other established path deletion.
- Terminal-content commit: byte-final non-terminal result package and manifest; no consumption receipt; manifest-bound artifacts become immutable.
- Terminal-receipt commit: direct child of terminal-content commit; only adds consumption receipt; all other blobs byte-identical.

Every result-ref update repeats: immediate target read → fresh protection identity/version read → atomic old-OID CAS → external CAS evidence → target/protection re-read → exact parent/tree/path/immutability validation → evidence reconciliation.

## Phase 2 — Post-activation exact frozen-input verification

Only after Phase 1C succeeds:

- read the exact frozen Repair-2 blobs identified by canonical Git identity;
- verify all frozen SHA-256 values, shard count/hash/byte-length bindings, and decompressed corpus identity/count;
- parse canonical JSON with duplicate-member rejection;
- reproduce exact `SYSTEM_PROMPT_SHA256` and `PROMPT_PROTOCOL_SHA256` from the normative preimages;
- verify all prompt/parser/scoring/protocol/report contract bindings;
- fail closed on mismatch or evidence of any forbidden pre-activation frozen-content access.

## Phase 3 — Deterministic R2 provenance audit

- verify compressed storage before decompression;
- parse exactly 240 corpus records;
- validate R2 source prohibitions, payload/gold separation, and evidence-reference integrity;
- emit canonical `r2-provenance-audit.json` with no self-digest field.

## Phase 4 — Corpus/spec/manifest conformance audit

- reproduce compressed/decompressed corpus SHA-256 values;
- reproduce logical scoring-key and per-shard identities/counts/byte lengths;
- require exact canonical item IDs/order and six axes × 40;
- recompute archetype/difficulty assignment;
- verify task-template and scoring-key contract compatibility;
- emit canonical `corpus-conformance-audit.json` with no self-digest field.

## Phase 5 — Execution-binding inventory

Without model access:

- retain only already-admitted immutable candidate identities;
- no challenger, no gated request/acceptance, no execution subset finalization until runtime/hardware feasibility is bound;
- record public/gated status and all still-unbound execution requirements explicitly;
- normalize/hash `execution-binding-inventory.md` exactly as required.

## Phase 6 — Result package and two-commit terminal closure

Produce the four unconditional core outputs:

1. `r2-provenance-audit.json`;
2. `corpus-conformance-audit.json`;
3. `execution-binding-inventory.md`;
4. `preflight-verdict.md`.

Optionally render only the uniquely identified provisional V2 successor when Sections A–D and inventory readiness permit it. It exists only as a Section E hash input and grants no authority. Any later blocker removes it, sets `successor_candidate = null`, and rebuilds the blocked binding package.

Construct the result binding in the exact non-cyclic order from `acceptance.md`: audits/inventory hashes → optional successor hash → `manifest_binding_core` → core SHA → verdict → verdict SHA → canonical `preflight-result-manifest.json` → external manifest SHA.

### Terminal content commit

When result artifacts are byte-final:

- create `TERMINAL_CONTENT_COMMIT` as a one-parent valid result-lineage commit with no consumption receipt;
- immediately re-read current result target + fresh protection identity/version;
- CAS from that exact observed old target to the content commit;
- preserve CAS evidence;
- re-read target/protection and validate exact graph/tree/path/immutability; reconcile evidence.

### Terminal receipt commit

Then:

- construct canonical `consumption-receipt.json` binding the already-known activation commit, terminal-content commit, final manifest SHA-256, claim/ref identities, server protections, selected CAS protocol/evidence through the content commit, and terminal state;
- never embed the future receipt-commit SHA inside that receipt;
- create `TERMINAL_RECEIPT_COMMIT` as direct child of `TERMINAL_CONTENT_COMMIT`, only adding the receipt;
- immediately re-read result target + protection and require target=`TERMINAL_CONTENT_COMMIT`;
- CAS to the observed receipt commit and preserve final external evidence;
- re-read target/protection; verify exact direct-parent/tree delta and receipt bytes; reconcile final CAS evidence;
- activate terminal frozen result-ref protection and re-read it, requiring no configured bypass.

The terminal receipt becomes canonical only after that entire final sequence succeeds. Publish the externally observed receipt-commit SHA, final manifest SHA, and final CAS/freeze evidence inside the exact PR evidence block, not free-form evidence prose.

If final publication/re-read/graph/tree/CAS/freeze fails, the receipt is noncanonical even if a commit object exists. The episode remains burned/non-reusable through claim/result/history evidence as `ISSUED` or `IN_PROGRESS`; do not fabricate `BLOCKED` or `CONSUMED` terminal closure. A new attempt requires a new separately reviewed Founder authorization.

Canonical ready closure:

```text
terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
state = CONSUMED
```

Canonical blocked closure:

```text
terminal_state = BLOCKED
state = BLOCKED
```

`CONSUMED` means this preflight episode was consumed; it is not execution authority.

## Phase 7 — Pre-merge exact-head result gate

Before canonical adoption of a future preflight **result** package:

- the result PR itself must satisfy the exact current-episode structural PR predicate from Phase 1A / `acceptance.md`;
- exact-head CI = PASS;
- exact-head CodeQL = PASS;
- fresh independent exact-head review = no blocker;
- unresolved blocking review threads = 0;
- Ready only after those gates;
- expected-head merge protection;
- immediately before merge, re-read claim ref, frozen result ref, server protections, all CAS evidence, and final graph/tree/manifest/receipt bindings;
- require claim at authorization SHA;
- require result ref at exact terminal-receipt commit;
- require terminal-receipt commit one-parent direct child of the receipt-bound terminal-content commit with only receipt tree delta;
- require terminal frozen protection with no configured bypass.

Any failure before merge means do not merge the result package. It does not create a canonical terminal outcome.

## Phase 8 — Post-merge canonical adoption verification and immutable record

After a result-package merge, mechanically verify:

- canonical `main` equals the returned result merge SHA;
- exact merged tree is expected;
- ordered parents are exact expected old main then exact reviewed result head;
- hosting commit signature verification is valid and its exact signature text and verification payload are available for hashing;
- merged result artifacts/receipt/manifest are byte-identical to reviewed exact head;
- permanent claim and frozen result ref/protections still match the reviewed terminal evidence.

Then construct exactly:

```text
ADOPTION_RECORD_PATH = specs/mesc-backbone-tournament/execution-preflight-1-adoption/<RESULT_MERGE_SHA>/canonical-adoption-verification.json
```

The file is canonical JSON under `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1`, contains no self-digest field, and MUST contain exactly these top-level keys: `record_version`, `decision_id`, `authorization_merge_sha`, `activation_receipt_id`, `result_merge_sha`, `result_merge_tree`, `ordered_parents`, `reviewed_result_head_sha`, `preflight_result_manifest_sha256`, `result_package_artifacts`, `terminal_receipt_commit`, `terminal_receipt_sha256`, `claim_ref`, `claim_ref_target`, `result_ref`, `result_ref_terminal_target`, `terminal_result_ref_protection`, `merge_signature_verification`, `failed_checks`, and `outcome`. Unknown, missing, or duplicate top-level keys invalidate the record.

Apply the exact value and nested-schema rules from `acceptance.md`: `record_version = MESC-BT-PREFLIGHT-CANONICAL-ADOPTION-V1`; `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT`; ordered parents exactly `[PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA]`; complete exact `result_package_artifacts` map with each value containing only `sha256` and `byte_length`; exact `terminal_result_ref_protection` keys `mechanism_identity`, `mechanism_version`, `observed_result_ref_target`, `terminal_frozen`, `no_configured_bypass`; exact `merge_signature_verification` keys `verified`, `reason`, `signature_sha256`, `payload_sha256`; deterministic unique NFC `failed_checks` strings sorted by Unicode code point; and `outcome` exactly `CANONICAL_ADOPTION_VERIFIED` or `CANONICAL_ADOPTION_VERIFICATION_FAILED`. Unknown/missing/duplicate nested keys or a value that does not mechanically revalidate invalidates the record.

Publication is exact and create-only. Substitute `<RESULT_MERGE_SHA>` in `ADOPTION_RECORD_PATH` with the exact record `result_merge_sha`, which must equal the mechanically verified canonical result merge SHA. Immediately before opening the adoption-verification PR and again immediately before merging it, prove the exact path is absent from canonical premerge `main`. The PR/head/tree delta must contain **exactly one changed repository path**, `ADOPTION_RECORD_PATH`, with status added/create-only; no other addition, modification, deletion, rename, copy, replacement, or pre-existing-path edit is permitted. A pre-existing path, mismatched path SHA component, non-create-only status, or any other tree change invalidates the record publication and makes PASS unavailable.

Publish only that one-path create-only record through a separate adoption-verification PR. The PR must itself receive exact-head review and expected-head merge protection. It must not change `RESULT_ROOT`, the frozen `RESULT_REF`, terminal receipt, or result-package bytes.

A successful result verification does **not** become canonically usable PASS merely because a local check printed PASS. `CANONICAL_ADOPTION_VERIFIED = PASS` becomes usable only after the adoption-record file is canonical on `main`, has `outcome = CANONICAL_ADOPTION_VERIFIED`, and all record fields revalidate against the result merge/head/tree/parents/signature, manifest/artifact digests, claim/result refs, terminal target, and terminal protection.

If any result-adoption verification predicate fails, publish `outcome = CANONICAL_ADOPTION_VERIFICATION_FAILED` with exact deterministic failed checks; the successor candidate stays inactive/unusable. Do **not** rewrite the immutable terminal receipt or claim that it changed from `CONSUMED` to `BLOCKED`.

Any later execution authorization must reference the canonical adoption-record merge SHA/tree plus the exact record path, Git blob SHA, and full-file SHA-256; it must re-read/re-hash/revalidate the record, require `outcome = CANONICAL_ADOPTION_VERIFIED`, and still obtain its own separately reviewed Founder authorization.

## Execution remains out of scope

This plan never sends a prompt to a model, accesses model weights, accepts gated terms, runs inference, executes the tournament, scores/ranks model outputs, trains, retrieves, or selects a winner.

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
