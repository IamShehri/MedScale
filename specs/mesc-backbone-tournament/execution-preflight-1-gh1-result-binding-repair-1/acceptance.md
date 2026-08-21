# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT-GH1-RESULT-BINDING-REPAIR-1

Status: **DRAFT ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-21

Every applicable predicate must be mechanically proven. Ambiguity, stale exact-head evidence, incomplete PR enumeration, or inability to reproduce a required byte preimage => `BLOCKED`.

## A. Exact anchors and defect identity

Canonical starting state for this repair candidate:

```text
PRE_REPAIR_MAIN_SHA = 4e259767a86c74a26967e0f19598a1f84a987df4
PRE_REPAIR_MAIN_TREE = c487c5a70abf865b364c96de1aa8c18da7bf6602
GH1_REPAIR_AUTHORIZATION_MERGE_SHA = 9d66538b96794429e29b7baa0c58dfa60a408cb7
GH1_REPAIR_AUTHORIZATION_MERGE_TREE = b80aceddcb7082fa8af8c40c34e4228c6e8f6a35
HISTORICAL_GH1_HOSTING_REPAIR_ACCEPTANCE_BLOB_SHA = 2d0c9765d22b435cd8e57d13e7d5972e9a095b40
INHERITED_ACCEPTANCE_BLOB_SHA = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
GH1_ACTIVATION_RECEIPT_ID = 6c3bb9a5e8b55c4bd3b9be81e59629dd9e257d4a1eb3a6d0e99dcaf00be9947c
GH1_ACTIVATION_HEAD_SHA = 8d525730705351afffc8ca67940e2cc50df9632a
GH1_ACTIVATION_MERGE_SHA = 4e259767a86c74a26967e0f19598a1f84a987df4
GH1_ACTIVATION_MERGE_TREE = c487c5a70abf865b364c96de1aa8c18da7bf6602
```

`HISTORICAL_GH1_HOSTING_REPAIR_ACCEPTANCE_BLOB_SHA` names only the already-canonical `execution-preflight-1-hosting-repair-1/acceptance.md` blob that defined GH1. It MUST NOT be interpreted as the acceptance blob of this current result-binding-repair PR. The current result-binding-repair acceptance blob is the Git blob SHA of **this file** at the exact reviewed PR head; reviewers/workers MUST read and record that SHA externally from Git metadata at every exact-head gate. It is deliberately not embedded in this file because doing so would create a self-referential blob identity.

The defect is mechanically established only if all are true:

1. historical GH1 hosting-repair Section J.2 at `HISTORICAL_GH1_HOSTING_REPAIR_ACCEPTANCE_BLOB_SHA` requires `frozen_input_digest_map` to preserve exactly the old Section E key/value object;
2. the exact inherited old Section E at `INHERITED_ACCEPTANCE_BLOB_SHA` requires an "exact Repair-2 frozen input digest map" but defines no literal JSON object, no exact member names, no member count, and no mapping from frozen constants to JSON keys;
3. repository code/search and the retained PR history reveal no canonical result artifact that supplies that missing object;
4. zero structurally selected GH1 result PRs exist and no GH1 result root exists on canonical `main`;
5. no valid GH1 result package has already made a different representation canonical.

Any contrary canonical evidence => stop and reassess; this repair must not merge on a false defect premise.

## B. GH1 post-activation fail-closed state

Before this repair may become Ready and again immediately before merge, mechanically verify **all** predicates in this section in one fresh snapshot.

Canonical `main` MUST equal the exact pre-repair activation state:

```text
PRE_REPAIR_MAIN_SHA = 4e259767a86c74a26967e0f19598a1f84a987df4
PRE_REPAIR_MAIN_TREE = c487c5a70abf865b364c96de1aa8c18da7bf6602
```

The GH1 result-PR identities used for complete replay/conflict classification are exactly:

```text
GH1_RESULT_PR_AUTH_PREFIX = governance/fd-mesc-bt-exec-1-preflight-gh1-result/9d66538b96794429e29b7baa0c58dfa60a408cb7/
GH1_RESULT_PR_HEAD_REF = governance/fd-mesc-bt-exec-1-preflight-gh1-result/9d66538b96794429e29b7baa0c58dfa60a408cb7/6c3bb9a5e8b55c4bd3b9be81e59629dd9e257d4a1eb3a6d0e99dcaf00be9947c
```

Enumerate the complete open + closed/merged PR population. A PR is a selected GH1 result PR iff base repository full name=`TheHalfMoon/MESC`, base ref=`main`, head repository full name=`TheHalfMoon/MESC`, and retained head ref exactly=`GH1_RESULT_PR_HEAD_REF`; PR state/title/labels/author/reviews are not selectors. Independently, any PR whose head repository is exactly `TheHalfMoon/MESC` and whose retained head ref begins with `GH1_RESULT_PR_AUTH_PREFIX` is in the reserved current-authorization result namespace. Such a PR is valid only if it also satisfies the exact selected-result predicate; every sibling suffix, malformed suffix, extra segment, wrong base repo/ref, or otherwise non-current structure is a reserved conflict even if its branch was deleted.

The exact replay/state result MUST be:

```text
GH1_SELECTED_ACTIVATION_PRS = 1
GH1_SELECTED_RESULT_PRS = 0
GH1_RESERVED_RESULT_NAMESPACE_CONFLICTS = 0
GH1_RESULT_ROOT_ON_MAIN = ABSENT
GH1_TERMINAL_RECEIPT_ON_MAIN = ABSENT
GH1_RESULT_MERGE = ABSENT
GH1_ADOPTION_RECORD = ABSENT
```

The retained selected activation PR must be PR #134 with exact head `8d525730705351afffc8ca67940e2cc50df9632a`. Canonical `main` must still be activation merge `4e259767a86c74a26967e0f19598a1f84a987df4` with exact tree `c487c5a70abf865b364c96de1aa8c18da7bf6602`, and the authoritative hosting verification object for that merge MUST satisfy all four field-level predicates:

```text
verification.verified = true
verification.reason = valid
verification.signature = NON_NULL_SOURCE_TEXT
verification.payload = NON_NULL_SOURCE_TEXT
```

Any main SHA/tree drift, incomplete PR enumeration, unreadable selector field, selected-result PR, reserved result conflict, or failed hosting-verification predicate => `BLOCKED`; this repair MUST NOT become Ready or merge.

Worker-state evidence recorded by this repair is:

```text
GH1_FROZEN_REPAIR2_CONTENT_ACCESS = PERFORMED_AFTER_VALID_ACTIVATION
GH1_BOUNDED_SCIENTIFIC_INSPECTION = PERFORMED_NO_MODEL
GH1_SCIENTIFIC_AUDIT_ARTIFACTS = NOT_PUBLISHED
GH1_MODEL_WEIGHT_ACCESS = NOT_PERFORMED
GH1_GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_PERFORMED
GH1_PROMPT_SERIALIZATION_TO_MODEL = NOT_PERFORMED
GH1_INFERENCE = NOT_PERFORMED
GH1_GENERATION = NOT_PERFORMED
GH1_TRAINING = NOT_PERFORMED
GH1_MODEL_RETRIEVAL = NOT_PERFORMED
GH1_RANKING = NOT_PERFORMED
GH1_WINNER_SELECTION = NOT_PERFORMED
GH1_BACKBONE_TOURNAMENT_EXECUTION = NOT_PERFORMED
```

Because GH1 was already issued and canonically activated, it can never return to `UNUSED`. Because its result-binding preimage is underdefined, no result artifact may claim `CONSUMED` or canonical `BLOCKED` under GH1.

After a verified canonical merge of this repair:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = SUPERSEDED_NONREUSABLE_POST_ACTIVATION_CONTRACT_DEFECT
GH1_RESULT_CREATION = PERMANENTLY_FORBIDDEN
GH1_RETRY = PERMANENTLY_FORBIDDEN
```

Existing GH1 activation records remain immutable historical evidence.

## C. Why in-place GH1 repair is forbidden

The following proof is normative:

1. historical GH1 hosting-repair Section I requires first GH1 result commit parent exactly `GH1_ACTIVATION_MERGE_SHA`;
2. every GH1 result-lineage commit may change only the GH1 result-root allowlist;
3. historical GH1 hosting-repair Section L requires the final premerge-main to reviewed-result-head changed-path set to contain only that result allowlist;
4. a canonical clarification merged to `main` after activation would not be present in a result branch rooted at the activation merge and therefore would appear as an unrelated path difference;
5. inserting that clarification into the result lineage would itself violate the result allowlist.

Therefore no canonical clarification can make GH1 result construction valid without violating another canonical GH1 predicate. In-place repair is prohibited.

## D. GH2 replacement authorization receipt

Only after this repair PR is canonically merged and post-merge verified may a new receipt identity be derived.

Define:

```text
NEW_DECISION_ID = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
GH2_REPAIR_DECISION_ID = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1-RESULT-BINDING-REPAIR-1
```

`GH2_ACTIVATION_RECEIPT_ID` is SHA-256 of canonical JSON under inherited `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` containing exactly:

- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2`;
- `repair_authorization_merge_sha = <verified canonical merge SHA of this repair>`;
- `repair_authorization_merge_tree = <verified canonical merge tree of this repair>`;
- `repair_package_files = <ordered four-object array>`;
- `receipt_version = MESC-BT-PREFLIGHT-GH2-RECEIPT-V1`.

`repair_package_files` contains exactly four objects, in this order, each with exact keys `path` and `git_blob_sha`:

1. `specs/mesc-backbone-tournament/execution-preflight-1-gh1-result-binding-repair-1/README.md`;
2. `specs/mesc-backbone-tournament/execution-preflight-1-gh1-result-binding-repair-1/acceptance.md`;
3. `specs/mesc-backbone-tournament/execution-preflight-1-gh1-result-binding-repair-1/founder-authorization.md`;
4. `specs/mesc-backbone-tournament/execution-preflight-1-gh1-result-binding-repair-1/plan.md`.

The `git_blob_sha` values are **derived evidence, never caller-selected values**. After the repair merge is returned and verified, read the authoritative Git tree for `repair_authorization_merge_sha`; for each ordered path above, resolve the exact blob entry and require:

```text
repair_package_files[i].git_blob_sha = authoritative Git blob SHA for repair_package_files[i].path at repair_authorization_merge_sha
```

All four paths MUST resolve to regular Git blobs, and the exact blob bytes at the verified repair merge MUST equal the reviewed exact-head bytes for the corresponding path. Construct `repair_package_files` only from these verified path/blob pairs. Only after all four equality predicates pass may canonical receipt-preimage bytes be serialized and `GH2_ACTIVATION_RECEIPT_ID` be computed. Unknown, missing, duplicate, extra, reordered, malformed, caller-supplied, unresolved, or mismatched path/blob entries => `BLOCKED`.

A verified repair merge has exactly this governance effect:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT-GH2 = AUTHORIZED_NOT_STARTED
```

It does not itself create a GH2 claim, activate frozen-content access, or begin scientific audit work.

## E. Exact GH2 identities and replay

For the verified repair merge SHA and derived receipt ID:

```text
GH2_ACTIVATION_HEAD = governance/fd-mesc-bt-exec-1-preflight-gh2-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH2_ACTIVATION_RECEIPT_ID>
GH2_RESULT_HEAD = governance/fd-mesc-bt-exec-1-preflight-gh2-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH2_ACTIVATION_RECEIPT_ID>
GH2_ACTIVATION_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-gh2-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH2_ACTIVATION_RECEIPT_ID>/
GH2_CLAIM_RECORD_PATH = <GH2_ACTIVATION_ROOT>claim-record.json
GH2_ACTIVATION_RECEIPT_PATH = <GH2_ACTIVATION_ROOT>activation-receipt.json
GH2_RESULT_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-gh2-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH2_ACTIVATION_RECEIPT_ID>/
GH2_ADOPTION_PREFIX = specs/mesc-backbone-tournament/execution-preflight-1-gh2-adoption/
```

Before activation PR publication and at every later replay gate, enumerate the complete open+closed+merged PR population and apply exact structural selectors: base repo `TheHalfMoon/MESC`, base ref `main`, head repo `TheHalfMoon/MESC`, and retained head name exactly equal to the relevant GH2 head above. Any same-repository PR under either current repair-SHA GH2 namespace prefix that does not exactly match its selector is a reserved conflict => `BLOCKED`.

Before opening the GH2 activation PR require zero selected GH2 activation PRs, zero selected GH2 result PRs, zero reserved conflicts, activation root absent on canonical `main`, and result root absent on canonical `main`.

Once an exact GH2 activation PR record exists, GH2 becomes `ISSUED` and can never return to `UNUSED`.

## F. GH2 claim and activation files

The GH2 activation PR adds exactly two new canonical JSON files and no other path.

`claim-record.json` has exactly these top-level keys:

- `record_version = MESC-BT-PREFLIGHT-GH2-CLAIM-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `superseded_decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `superseded_activation_merge_sha = 4e259767a86c74a26967e0f19598a1f84a987df4`;
- `supersession_reason = RESULT_BINDING_SCHEMA_UNDERDEFINED`;
- `claim_mode = CANONICAL_MAIN_MERGE`;
- `gh2_episode_frozen_content_read_before_activation = false`.

The final field is scoped only to the new GH2 episode. It does not deny or rewrite the valid historical GH1 post-activation bounded read recorded in Section B.

Define:

```text
CLAIM_RECORD_SHA256 = SHA256(exact canonical claim-record.json bytes)
```

`activation-receipt.json` has exactly:

- `receipt_version = MESC-BT-PREFLIGHT-GH2-ACTIVATION-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `claim_record_sha256`;
- `inherited_acceptance_blob_sha = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`;
- `state = IN_PROGRESS`;
- `gh2_episode_content_read_started = false`.

The final field is scoped only to content access under GH2 authority.

Both files use inherited canonical JSON, reject duplicate keys, and contain no containing/future commit SHA or self digest. Their semantic values are equality-bound, not descriptive. Before the activation package can pass require all of:

```text
claim-record.json.decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
claim-record.json.repair_authorization_merge_sha = REPAIR_AUTHORIZATION_MERGE_SHA
claim-record.json.repair_authorization_merge_tree = REPAIR_AUTHORIZATION_MERGE_TREE
claim-record.json.activation_receipt_id = GH2_ACTIVATION_RECEIPT_ID
activation-receipt.json.decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
activation-receipt.json.repair_authorization_merge_sha = REPAIR_AUTHORIZATION_MERGE_SHA
activation-receipt.json.repair_authorization_merge_tree = REPAIR_AUTHORIZATION_MERGE_TREE
activation-receipt.json.activation_receipt_id = GH2_ACTIVATION_RECEIPT_ID
activation-receipt.json.claim_record_sha256 = CLAIM_RECORD_SHA256
```

`CLAIM_RECORD_SHA256` MUST be recomputed from the exact reviewed canonical claim-record bytes and again from canonical merged claim-record bytes after activation merge; both values must equal the activation receipt field. Any identity mismatch or cross-file hash mismatch => `BLOCKED`.

## G. GH2 activation merge gate

Before any frozen Repair-2 content access performed under GH2 authority require all on one exact reviewed head:

1. activation delta exactly the two create-only paths in Section F;
2. exact canonical JSON bytes validate and every Section F equality/cross-file hash predicate passes;
3. replay finds exactly one selected GH2 activation PR, zero selected GH2 result PRs, zero reserved conflicts;
4. canonical `main` equals exact final-review premerge SHA;
5. activation head equals exact reviewed head;
6. exact-head CI PASS;
7. exact-head CodeQL PASS;
8. fresh independent exact-head governance review has no blocker;
9. unresolved blocking review threads = 0;
10. merge uses exact `expected_head_sha`;
11. returned merge is canonical `main`;
12. ordered parents are exactly `[PREMERGE_MAIN_SHA, REVIEWED_ACTIVATION_HEAD_SHA]`;
13. merge tree/path delta contains exactly the two activation paths;
14. hosting verification is `verified=true`, `reason=valid`, and source signature/payload are non-null;
15. canonical activation file bytes equal reviewed bytes, and the canonical merged claim-record SHA-256 still equals `activation-receipt.json.claim_record_sha256`;
16. fresh replay finds no concurrent GH2 conflict.

Only after item 16:

```text
GH2_CLAIM = CANONICAL
GH2_ACTIVATION = CANONICAL
FROZEN_REPAIR2_CONTENT_ACCESS = AUTHORIZED_FOR_BOUNDED_GH2_PREFLIGHT_ONLY
```

Any failure burns GH2 and requires a separate Founder repair. No GH2-episode pre-activation frozen-content read is permitted.

Define the verified merge as `GH2_ACTIVATION_MERGE_SHA` / `GH2_ACTIVATION_MERGE_TREE`.

## H. Inherited scientific/content contract

GH2 inherits exactly and only original preflight `acceptance.md` Sections A-D at blob `7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`:

- Repair-2 ancestry/path/blob/digest and derived prompt bindings;
- `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1`;
- R2 provenance audit predicates;
- corpus specification/manifest conformance predicates.

Old Section E and later old lifecycle sections are not inherited. GH1 result Sections I-M are not inherited. No result schema may be filled by analogy.

All scientific audit work is repeated under GH2 after GH2 activation. Earlier GH1 bounded reads are historical evidence only and cannot substitute for a GH2 audit artifact.

## I. Exact frozen input binding object — no implicit digest map

GH2 result binding uses exactly:

```text
FROZEN_INPUT_BINDINGS_VERSION = MESC-BT-REPAIR2-FROZEN-INPUT-BINDINGS-V1
```

`frozen_input_bindings` is a canonical JSON object with **exactly these 15 member names and values**, no more and no fewer:

```json
{"CORPUS_MANIFEST_SHA256":"201fa1351923a72097ff7e467b6dce2eb8bd0cfa1e88c73157788f77dd89e745","CORPUS_SPEC_SHA256":"49f554d57e29da4b1d04223d43f1630731e5f8c9b72e7a1e15f959e38c00643b","MATERIALIZED_CORPUS_GZIP_SHA256":"667cd68e5ccc9356321eb5857c6e9203e1320ec33d866ccf514411c211ceb632","MATERIALIZED_CORPUS_ITEM_COUNT":240,"MATERIALIZED_CORPUS_SHA256":"48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd","NORMALIZED_OUTPUT_SCHEMA_SHA256":"3e0a1523af45a61db77e3287a3333361fa26411f521321bbef0804dec7a63ed4","PARSER_CONTRACT_SHA256":"9905096b491ddc3bce2b5d668c1f8726f638dde9dba383ac1bb755f1b6b42071","PROMPT_PROTOCOL_SHA256":"a2a42aef340e27f9396b40810999d5f2c4136af467ce27ee9e3c149e3257c89c","PROTOCOL_CONFIG_SHA256":"097cdd11f5389203cf432760ec316a78b12d157c0676477de69dde707e058203","REPORT_SCHEMA_SHA256":"cb3fc506b41cc6236959bb4a89bce249db13c99aeb0c7178ff233f6de44e026d","REPORT_VALIDATION_CONTRACT_SHA256":"c68fcac507e4ebc164632370d2392631b9fec9c388369eb5b8bfa495e5877c1a","SCORING_CONTRACT_SHA256":"a61471d467521b59eb62ee2825d23fa15891bb45a664360aaf2e4ef5882c7d40","SCORING_KEYS_SHA256":"bb3524bc8dd1f05bad433c664ac3c48a5110939ac78b5ffa2ad8853f944c6318","SYSTEM_PROMPT_SHA256":"02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867","TASK_PROMPT_BUNDLE_SHA256":"54d9da5cf3dad58c0bf9fb28761c15d8f82568013895b8467f1cb7d532c314b7"}
```

The object above is the literal semantic object. Canonical serialization still sorts member names per inherited Section B. Renaming to lowercase, changing the item count to a string, adding Git blob IDs, omitting a member, adding a version member inside the object, or substituting any alternate representation => `BLOCKED`.

## J. GH2 result graph and allowlist

The only paths permitted under `GH2_RESULT_ROOT` are:

1. `r2-provenance-audit.json`;
2. `corpus-conformance-audit.json`;
3. `execution-binding-inventory.md`;
4. `preflight-verdict.md`;
5. `preflight-result-manifest.json`;
6. conditional `execution-authorization-candidate.md`;
7. terminal-only `consumption-receipt.json`.

The result branch begins exactly at `GH2_ACTIVATION_MERGE_SHA`. Every result commit has exactly one parent, no merge commit, parent equal to the immediately preceding valid result target, and no changed path outside the allowlist/root. Activation files and frozen Repair-2 paths are immutable.

Intermediate commits may add/update only non-receipt result files. `TERMINAL_CONTENT_COMMIT` freezes every manifest-bound non-receipt artifact. `TERMINAL_RECEIPT_COMMIT` is its direct child and may only create `consumption-receipt.json`. No later result-lineage commit is permitted before canonical result adoption.

Force-push, non-fast-forward/sideways retarget, parent mismatch, out-of-root path, post-terminal mutation, receipt replacement, or extra post-receipt commit => `BLOCKED`.

## K. Exact GH2 result-package binding

Conditional successor:

```text
GH2_SUCCESSOR_ID = FD-MESC-BT-EXEC-1-CANDIDATE-GH2-V1
GH2_SUCCESSOR_PATH = <GH2_RESULT_ROOT>execution-authorization-candidate.md
```

It may exist only if inherited Sections A-D PASS and the execution-binding inventory is complete under K.1. It grants no execution authority.

### K.1 Canonical execution-binding inventory bytes

`execution-binding-inventory.md` is manifest-bound and therefore has one canonical byte grammar. It MUST be UTF-8 without BOM, use LF (`0x0a`) only, contain no CR, and end with exactly one final LF.

The file contains **exactly 16 non-empty lines** and no other bytes. Line 1 is exactly:

```text
MESC-BT-PREFLIGHT-GH2-EXECUTION-BINDING-INVENTORY-V1
```

Lines 2-16 correspond in exactly this order to:

```text
CANONICAL_CODE_SHA_TREE
SELECTED_CANDIDATE_SUBSET
CANDIDATE_MODEL_REVISIONS
TOKENIZER_PROCESSOR_CUSTOM_CODE_REVISIONS
HARDWARE_PROVIDER_RUNTIME_PRECISION
PEAK_VRAM_MEASUREMENT_CAPABILITY
LATENCY_MEASUREMENT_CAPABILITY
GATED_ACCESS_AUTHORIZATION
BOUNDED_RUN_ATTEMPTS
ARTIFACT_DESTINATIONS
R2_PROVENANCE_AUDIT_SHA256
CORPUS_CONFORMANCE_AUDIT_SHA256
REPORT_VALIDATION_CONTRACT_BINDING
REPORT_SCHEMA_BINDING
LATER_EXACT_HEAD_EXECUTION_AUTHORIZATION_GATES
```

Each of lines 2-16 has exactly four tab-separated fields and exactly three U+0009 TAB separators, with no leading/trailing whitespace:

```text
<LABEL><TAB><STATUS><TAB><VALUE_JSON><TAB><BLOCKER_JSON>
```

Normative field grammar:

- `<LABEL>` is the exact label assigned to that line by the ordered list above.
- `<STATUS>` is exactly `BOUND` or `UNBOUND`.
- `<VALUE_JSON>` is either `null` or one canonical JSON string token using inherited JSON string escaping; its decoded string MUST be non-empty and MUST NOT contain U+0009, U+000A, or U+000D.
- `<BLOCKER_JSON>` follows the same token grammar.
- For `BOUND`: `<VALUE_JSON>` MUST be a non-empty JSON string and `<BLOCKER_JSON>` MUST be literal `null`.
- For `UNBOUND`: `<VALUE_JSON>` MUST be literal `null`; `<BLOCKER_JSON>` MUST be a non-empty JSON string whose decoded value begins exactly `BLOCKED_FOR_FUTURE_TOURNAMENT_EXECUTION: ` and contains at least one character after that prefix.

No blank line, comment, Markdown heading, fence, duplicate label, omitted label, reordered label, alternate separator, extra tab, extra field, `UNKNOWN`, `N/A`, `PASS` status alias, trailing spaces, or extra text is permitted. Parsing then canonical reserialization under this grammar MUST reproduce the original bytes exactly or the artifact is `BLOCKED`.

`UNBOUND` items do not make successful inherited A-D corpus/provenance audits false and do not prevent a provisional inactive GH2 successor. They remain future execution blockers. The inventory itself grants no execution authority.

### K.2 Canonical conditional successor bytes

If `GH2_SUCCESSOR_PATH` exists, it is manifest-bound and MUST be UTF-8 without BOM, LF only, exactly one final LF, no CR, and exactly these eight lines in this order with no spaces around `=` and no extra text:

```text
record_version=MESC-BT-PREFLIGHT-GH2-SUCCESSOR-CANDIDATE-V1
candidate_id=FD-MESC-BT-EXEC-1-CANDIDATE-GH2-V1
source_decision_id=FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
repair_authorization_merge_sha=<REPAIR_AUTHORIZATION_MERGE_SHA>
activation_receipt_id=<GH2_ACTIVATION_RECEIPT_ID>
activation_merge_sha=<GH2_ACTIVATION_MERGE_SHA>
state=DRAFT_INACTIVE_NOT_AUTHORIZED
execution_authority=NONE
```

The three placeholder values MUST equal the active GH2 episode identities exactly. Any alternate representation, line order, whitespace, extra commentary, or missing/extra line => `BLOCKED`.

### K.3 Manifest binding core and canonical verdict bytes

`manifest_binding_core` is canonical JSON with exactly these top-level keys:

- `manifest_id = MESC-BT-PREFLIGHT-GH2-RESULT-MANIFEST-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `activation_merge_sha`;
- `inherited_contract`;
- `frozen_input_bindings_version = MESC-BT-REPAIR2-FROZEN-INPUT-BINDINGS-V1`;
- `frozen_input_bindings` = exact Section I object;
- `artifacts`;
- `verdict_path`;
- `successor_candidate`.

`inherited_contract` has exactly:

- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT`;
- `authorization_merge_sha = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6`;
- `authorization_merge_tree = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70`;
- `acceptance_blob_sha = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`.

`artifacts` has exactly three keys `r2_provenance_audit`, `corpus_conformance_audit`, `execution_binding_inventory`; each value contains exactly `path`, `sha256`, `byte_length` and points to the corresponding GH2 result path.

`verdict_path = <GH2_RESULT_ROOT>preflight-verdict.md`.

`successor_candidate` is null or contains exactly `id`, `path`, `sha256`, `byte_length` with the GH2 successor identity and canonical bytes above.

Compute `MANIFEST_BINDING_CORE_SHA256 = SHA256(canonical_manifest_binding_core_bytes)`.

`preflight-verdict.md` is manifest-bound and MUST be UTF-8 without BOM, LF only, exactly one final LF, no CR, and exactly these nine lines in this order, with no spaces around `=` and no extra text:

```text
record_version=MESC-BT-PREFLIGHT-GH2-VERDICT-V1
decision_id=FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
repair_authorization_merge_sha=<REPAIR_AUTHORIZATION_MERGE_SHA>
repair_authorization_merge_tree=<REPAIR_AUTHORIZATION_MERGE_TREE>
activation_receipt_id=<GH2_ACTIVATION_RECEIPT_ID>
activation_merge_sha=<GH2_ACTIVATION_MERGE_SHA>
manifest_id=MESC-BT-PREFLIGHT-GH2-RESULT-MANIFEST-V1
manifest_binding_core_sha256=<MANIFEST_BINDING_CORE_SHA256>
terminal_state=<TERMINAL_STATE>
```

`<TERMINAL_STATE>` is exactly `BLOCKED` or `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`; all other placeholders MUST equal the active episode/binding identities exactly. Parsing then canonical reserialization MUST reproduce the original verdict bytes exactly. Alternate order, whitespace, duplicate/omitted/extra line, comment, heading, fence, or free text => `BLOCKED`.

`preflight-result-manifest.json` is canonical JSON with exactly:

- `manifest_version = MESC-BT-PREFLIGHT-GH2-RESULT-MANIFEST-V1`;
- `manifest_binding_core`;
- `manifest_binding_core_sha256`;
- `artifacts`.

Its `artifacts` map contains exact `path`, `sha256`, `byte_length` for the two audits, inventory, verdict, and conditional successor iff non-null. It excludes `consumption-receipt.json` and its own digest. Every listed digest/length MUST equal the exact artifact bytes at `TERMINAL_CONTENT_COMMIT`. Any later blocker removes a provisional successor and rebuilds the package before terminal content freeze.

## L. GH2 terminal receipt

`consumption-receipt.json` is canonical JSON and contains exactly:

- `receipt_version = MESC-BT-PREFLIGHT-GH2-CONSUMPTION-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `activation_merge_sha`;
- `terminal_content_commit`;
- `preflight_result_manifest_sha256`;
- `terminal_state`;
- `state`.

All receipt values are equality-bound, not descriptive fields. Validation MUST prove:

```text
decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
repair_authorization_merge_sha = REPAIR_AUTHORIZATION_MERGE_SHA
repair_authorization_merge_tree = REPAIR_AUTHORIZATION_MERGE_TREE
activation_receipt_id = GH2_ACTIVATION_RECEIPT_ID
activation_merge_sha = GH2_ACTIVATION_MERGE_SHA
terminal_content_commit = TERMINAL_CONTENT_COMMIT
preflight_result_manifest_sha256 = SHA256(exact <GH2_RESULT_ROOT>preflight-result-manifest.json bytes at TERMINAL_CONTENT_COMMIT)
```

Additionally:

1. `TERMINAL_CONTENT_COMMIT` MUST be the exact final non-receipt result commit whose tree contains the manifest-bound bytes validated in Section K;
2. `TERMINAL_RECEIPT_COMMIT` MUST have exactly one parent equal to `TERMINAL_CONTENT_COMMIT`;
3. `TERMINAL_RECEIPT_COMMIT` may create only `<GH2_RESULT_ROOT>consumption-receipt.json` and MUST change no other path or byte;
4. every non-receipt result artifact at `TERMINAL_RECEIPT_COMMIT` MUST be byte-identical to its bytes at `TERMINAL_CONTENT_COMMIT`;
5. the receipt's `preflight_result_manifest_sha256` MUST also equal the SHA-256 of those unchanged manifest bytes at `TERMINAL_RECEIPT_COMMIT`.

Ready pairing is exactly:

```text
terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
state = CONSUMED
```

Blocked pairing is exactly:

```text
terminal_state = BLOCKED
state = BLOCKED
```

The receipt contains no containing receipt-commit SHA, future result merge SHA, or self digest. Define `TERMINAL_RECEIPT_SHA256 = SHA256(exact canonical consumption-receipt.json bytes at TERMINAL_RECEIPT_COMMIT)` for later adoption binding.

## M. Result merge and canonical adoption

The result PR uses exact `GH2_RESULT_HEAD`, base `main`, same repository. Its reviewed head MUST equal `TERMINAL_RECEIPT_COMMIT`.

Before result merge require: exactly one selected GH2 activation PR and one selected GH2 result PR; zero reserved conflicts; activation bytes unchanged; complete Section J graph/immutability proof; exact Section K/L bindings; final-review `main` to result head changes only GH2 result allowlist paths; exact-head CI and CodeQL PASS; fresh independent exact-head governance review with no blocker; unresolved blocking threads 0; unchanged final-review main/head; expected-head merge.

After GitHub reports result-PR merge success, evaluate every post-result-merge predicate below whether it passes or fails. A failed predicate does not permit terminal authority; it must be represented deterministically in the adoption verification record rather than silently preventing the record from existing.

The closed total predicate-to-failure-code mapping is:

```text
canonical main equals returned result merge SHA                  -> GH2-RM-01_CANONICAL_MAIN_EQUALS_RETURNED_RESULT_MERGE
ordered parents equal [PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA] -> GH2-RM-02_ORDERED_PARENTS_MATCH
result merge tree equals expected reviewed merge tree             -> GH2-RM-03_RESULT_MERGE_TREE_MATCH
premerge-main to result-merge changed paths stay in GH2 allowlist -> GH2-RM-04_RESULT_MERGE_PATH_SCOPE
verification.verified is true                                     -> GH2-RM-05_MERGE_VERIFICATION_VERIFIED
verification.reason is exactly valid                              -> GH2-RM-06_MERGE_VERIFICATION_REASON_VALID
verification.signature source text is non-null                    -> GH2-RM-07_SIGNATURE_SOURCE_PRESENT
verification.payload source text is non-null                      -> GH2-RM-08_PAYLOAD_SOURCE_PRESENT
merged GH2 result artifact bytes equal reviewed exact-head bytes  -> GH2-RM-09_MERGED_RESULT_BYTES_MATCH_REVIEWED_HEAD
fresh replay selected GH2 activation PR count equals 1            -> GH2-RM-10_REPLAY_SELECTED_ACTIVATION_COUNT
fresh replay selected GH2 result PR count equals 1                -> GH2-RM-11_REPLAY_SELECTED_RESULT_COUNT
fresh replay reserved GH2 namespace conflict count equals 0       -> GH2-RM-12_REPLAY_RESERVED_CONFLICTS_ZERO
```

`EXPECTED_FAILED_CHECKS` is exactly the lexical sort of the failure code for every failed predicate above, with no omission, addition, alias, duplicate, or alternate code. `failed_checks` in the record MUST equal `EXPECTED_FAILED_CHECKS` byte-for-byte after canonical JSON serialization.

Immediately **after all twelve result-merge predicates have been evaluated** and before constructing any adoption branch, read canonical `main` again and freeze:

```text
ADOPTION_PREMERGE_MAIN_SHA = exact canonical main SHA observed after result-merge evaluation
ADOPTION_PREMERGE_MAIN_TREE = exact tree of ADOPTION_PREMERGE_MAIN_SHA
```

This capture is mandatory whether `GH2-RM-01` passed or failed. It is the publication base for the adoption verification record and is intentionally independent of ancestry from `RESULT_MERGE_SHA`. If canonical `main` cannot be read with an authoritative SHA/tree, adoption publication is `BLOCKED`; do not fabricate a base. If `main` moves after this capture but before adoption PR issuance, discard the unpublished adoption branch candidate, repeat only the canonical-main capture, derive a new adoption head identity from the new captured SHA, and re-render the adoption record with that new exact base. The immutable result-merge predicate outcomes and `RESULT_MERGE_SHA` do not change. Once an adoption PR is issued, any base drift is fail-closed and no alternate PR may be issued in the same GH2 episode.

### M.1 Exact adoption identity and PR selector

For the returned result merge SHA and frozen adoption publication base define exactly:

```text
GH2_ADOPTION_PR_AUTH_PREFIX = governance/fd-mesc-bt-exec-1-preflight-gh2-adoption/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH2_ACTIVATION_RECEIPT_ID>/<RESULT_MERGE_SHA>/
GH2_ADOPTION_HEAD = governance/fd-mesc-bt-exec-1-preflight-gh2-adoption/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH2_ACTIVATION_RECEIPT_ID>/<RESULT_MERGE_SHA>/<ADOPTION_PREMERGE_MAIN_SHA>
GH2_ADOPTION_RECORD_PATH = specs/mesc-backbone-tournament/execution-preflight-1-gh2-adoption/<RESULT_MERGE_SHA>/canonical-adoption-verification.json
```

A PR is the selected GH2 adoption PR iff base repository full name=`TheHalfMoon/MESC`, base ref=`main`, head repository full name=`TheHalfMoon/MESC`, and retained head ref exactly=`GH2_ADOPTION_HEAD`; PR state/title/labels/author/reviews are not selectors.

Any PR whose head repository is exactly `TheHalfMoon/MESC` and whose retained head ref begins with `GH2_ADOPTION_PR_AUTH_PREFIX` but is not the exact selected adoption PR is a reserved adoption conflict, including sibling/malformed suffixes, extra segments, or wrong base repo/ref. Deleted branches do not erase retained PR identity.

Before opening the adoption PR require:

```text
canonical main = ADOPTION_PREMERGE_MAIN_SHA
canonical main tree = ADOPTION_PREMERGE_MAIN_TREE
GH2_SELECTED_ADOPTION_PRS = 0
GH2_RESERVED_ADOPTION_NAMESPACE_CONFLICTS = 0
GH2_ADOPTION_RECORD_PATH_ON_MAIN = ABSENT
```

The adoption branch starts from exactly `ADOPTION_PREMERGE_MAIN_SHA`, **not** from `RESULT_MERGE_SHA`. This rule applies in both passing and failing result-merge verification cases and guarantees that the proposed adoption-record PR can have a one-file delta against the actual canonical publication base even if the returned result merge is not an ancestor of canonical `main`.

After publication and immediately before adoption merge require:

```text
GH2_SELECTED_ADOPTION_PRS = 1
GH2_RESERVED_ADOPTION_NAMESPACE_CONFLICTS = 0
canonical main = ADOPTION_PREMERGE_MAIN_SHA
canonical main tree = ADOPTION_PREMERGE_MAIN_TREE
```

Any selected-count, reserved-conflict, or base mismatch => `BLOCKED` and no adoption merge.

### M.2 Canonical adoption record value bindings

Create exactly one adoption-verification candidate record at `GH2_ADOPTION_RECORD_PATH`, regardless of whether `EXPECTED_FAILED_CHECKS` is empty.

The record is canonical JSON with exactly these top-level keys:

- `record_version = MESC-BT-PREFLIGHT-GH2-CANONICAL-ADOPTION-V1`;
- `decision_id`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `activation_merge_sha`;
- `result_merge_sha`;
- `result_merge_tree`;
- `ordered_parents`;
- `reviewed_result_head_sha`;
- `adoption_premerge_main_sha`;
- `adoption_premerge_main_tree`;
- `preflight_result_manifest_sha256`;
- `result_package_artifacts`;
- `terminal_receipt_commit`;
- `terminal_receipt_sha256`;
- `merge_signature_verification`;
- `failed_checks`;
- `outcome`.

Every identity/value is mechanically equality-bound as follows:

```text
decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
repair_authorization_merge_sha = REPAIR_AUTHORIZATION_MERGE_SHA
repair_authorization_merge_tree = REPAIR_AUTHORIZATION_MERGE_TREE
activation_receipt_id = GH2_ACTIVATION_RECEIPT_ID
activation_merge_sha = GH2_ACTIVATION_MERGE_SHA
result_merge_sha = authoritative returned RESULT_MERGE_SHA
result_merge_tree = authoritative tree of RESULT_MERGE_SHA
ordered_parents = authoritative ordered parent array of RESULT_MERGE_SHA
reviewed_result_head_sha = REVIEWED_RESULT_HEAD_SHA = TERMINAL_RECEIPT_COMMIT
adoption_premerge_main_sha = ADOPTION_PREMERGE_MAIN_SHA
adoption_premerge_main_tree = ADOPTION_PREMERGE_MAIN_TREE
preflight_result_manifest_sha256 = SHA256(exact reviewed preflight-result-manifest.json bytes)
terminal_receipt_commit = TERMINAL_RECEIPT_COMMIT
terminal_receipt_sha256 = TERMINAL_RECEIPT_SHA256
```

Further required graph/byte predicates:

1. `TERMINAL_RECEIPT_COMMIT` has exactly one parent equal to `TERMINAL_CONTENT_COMMIT`;
2. `REVIEWED_RESULT_HEAD_SHA` equals `TERMINAL_RECEIPT_COMMIT`;
3. the result merge's ordered second parent equals `REVIEWED_RESULT_HEAD_SHA` when `GH2-RM-02` passes;
4. `preflight_result_manifest_sha256` equals the SHA-256 of exact manifest bytes at `TERMINAL_CONTENT_COMMIT`, `TERMINAL_RECEIPT_COMMIT`, reviewed result head, and merged canonical result path when `GH2-RM-09` passes;
5. `terminal_receipt_sha256` equals SHA-256 of exact receipt bytes at `TERMINAL_RECEIPT_COMMIT`, reviewed result head, and merged canonical result path when `GH2-RM-09` passes;
6. `result_package_artifacts` is the complete lexical-path-ordered array of every reviewed GH2 result file present at `REVIEWED_RESULT_HEAD_SHA`, including `consumption-receipt.json`; each object contains exactly `path`, `sha256`, `byte_length`, and each digest/length equals the exact reviewed bytes and, when `GH2-RM-09` passes, the merged canonical bytes;
7. `ADOPTION_PREMERGE_MAIN_SHA` / tree are re-read immediately before PR publication and MUST still match canonical `main` exactly.

`merge_signature_verification` contains exactly `verified`, `reason`, `signature_sha256`, `payload_sha256`:

- `verified` equals authoritative hosting `verification.verified` for `RESULT_MERGE_SHA`;
- `reason` equals authoritative hosting `verification.reason` for `RESULT_MERGE_SHA`;
- `signature_sha256 = null` iff authoritative `verification.signature` is null, otherwise `SHA256(UTF8(exact verification.signature source text))` with no normalization;
- `payload_sha256 = null` iff authoritative `verification.payload` is null, otherwise `SHA256(UTF8(exact verification.payload source text))` with no normalization.

`failed_checks` equals exact `EXPECTED_FAILED_CHECKS`.

`outcome` is deterministic:

- if `failed_checks` is non-empty, `outcome = BLOCKED`;
- if `failed_checks = []`, `outcome` equals exactly the terminal receipt `terminal_state` (`BLOCKED` or `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`).

### M.3 Adoption merge and post-merge replay

The adoption-record PR must have an exact one-file create-only `ADOPTION_PREMERGE_MAIN_SHA`-to-reviewed-head delta at `GH2_ADOPTION_RECORD_PATH`, exact-head CI/CodeQL, fresh independent exact-head review with no blocker, zero unresolved blocking threads, unchanged final-review base/head, `GH2_SELECTED_ADOPTION_PRS = 1`, `GH2_RESERVED_ADOPTION_NAMESPACE_CONFLICTS = 0`, and expected-head merge.

After GitHub reports adoption merge success, mechanically require all of:

1. canonical `main` equals the returned adoption merge SHA;
2. ordered parents are exactly `[ADOPTION_PREMERGE_MAIN_SHA, REVIEWED_ADOPTION_HEAD_SHA]`;
3. `ADOPTION_PREMERGE_MAIN_SHA` tree equals recorded `adoption_premerge_main_tree`;
4. `ADOPTION_PREMERGE_MAIN_SHA` to adoption-merge changed paths equal exactly `GH2_ADOPTION_RECORD_PATH`;
5. canonical adoption-record bytes equal reviewed exact-head bytes;
6. authoritative adoption-merge `verification.verified=true`, `verification.reason=valid`, `verification.signature` non-null source text, and `verification.payload` non-null source text;
7. fresh complete PR replay returns `GH2_SELECTED_ADOPTION_PRS = 1` and `GH2_RESERVED_ADOPTION_NAMESPACE_CONFLICTS = 0`;
8. no second adoption record exists for the same `RESULT_MERGE_SHA`.

Any failed adoption-merge predicate means the adoption is not canonically terminal and the GH2 episode grants no execution authority.

If the canonical adoption record reports any non-empty `failed_checks`, canonical publication records a failed result-merge verification only; GH2 remains non-terminal/non-authoritative for execution and no replacement attempt may reuse the same GH2 episode. If `failed_checks=[]`, only a fully verified canonical merge of that exact adoption record under M.3 may make the receipt terminal state canonical.

## N. Hard stop

If GH2 becomes canonically terminal ready, report only:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

Do not start tournament execution. A separate Founder `FD-MESC-BT-EXEC-1` authorization is mandatory.

Throughout repair/GH2: no model weights, gated access/terms acceptance, provider prompts, inference, generation, training, model retrieval, ranking, winner selection, PHI, or tournament execution.
