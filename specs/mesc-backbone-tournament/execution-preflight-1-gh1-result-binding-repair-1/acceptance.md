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
GH1_REPAIR1_ACCEPTANCE_BLOB_SHA = 2d0c9765d22b435cd8e57d13e7d5972e9a095b40
INHERITED_ACCEPTANCE_BLOB_SHA = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
GH1_ACTIVATION_RECEIPT_ID = 6c3bb9a5e8b55c4bd3b9be81e59629dd9e257d4a1eb3a6d0e99dcaf00be9947c
GH1_ACTIVATION_HEAD_SHA = 8d525730705351afffc8ca67940e2cc50df9632a
GH1_ACTIVATION_MERGE_SHA = 4e259767a86c74a26967e0f19598a1f84a987df4
GH1_ACTIVATION_MERGE_TREE = c487c5a70abf865b364c96de1aa8c18da7bf6602
```

The defect is mechanically established only if all are true:

1. repair-1 J.2 requires `frozen_input_digest_map` to preserve exactly the old Section E key/value object;
2. the exact inherited old Section E requires an "exact Repair-2 frozen input digest map" but defines no literal JSON object, no exact member names, no member count, and no mapping from frozen constants to JSON keys;
3. repository code/search and the retained PR history reveal no canonical result artifact that supplies that missing object;
4. zero structurally selected GH1 result PRs exist and no GH1 result root exists on canonical `main`;
5. no valid GH1 result package has already made a different representation canonical.

Any contrary canonical evidence => stop and reassess; this repair must not merge on a false defect premise.

## B. GH1 post-activation fail-closed state

Before this repair may become Ready and again immediately before merge, mechanically verify:

```text
GH1_SELECTED_ACTIVATION_PRS = 1
GH1_SELECTED_RESULT_PRS = 0
GH1_RESULT_ROOT_ON_MAIN = ABSENT
GH1_TERMINAL_RECEIPT_ON_MAIN = ABSENT
GH1_RESULT_MERGE = ABSENT
GH1_ADOPTION_RECORD = ABSENT
```

The retained selected activation PR must be PR #134 with exact head `8d525730705351afffc8ca67940e2cc50df9632a`, and canonical activation merge must remain `4e259767a86c74a26967e0f19598a1f84a987df4` with tree `c487c5a70abf865b364c96de1aa8c18da7bf6602` and verified signature/payload.

Worker-state evidence recorded by this repair is:

```text
GH1_FROZEN_REPAIR2_CONTENT_ACCESS = PERFORMED_AFTER_VALID_ACTIVATION
GH1_SCIENTIFIC_AUDIT_WORK = PERFORMED_NO_MODEL
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

1. repair-1 Section I requires first GH1 result commit parent exactly `GH1_ACTIVATION_MERGE_SHA`;
2. every GH1 result-lineage commit may change only the GH1 result-root allowlist;
3. repair-1 Section L requires the final premerge-main to reviewed-result-head changed-path set to contain only that result allowlist;
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

Unknown, missing, duplicate, extra, reordered, malformed, or mismatched entries => `BLOCKED`.

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
- `frozen_content_read_before_gh2_activation = false`.

`activation-receipt.json` has exactly:

- `receipt_version = MESC-BT-PREFLIGHT-GH2-ACTIVATION-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `claim_record_sha256`;
- `inherited_acceptance_blob_sha = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`;
- `state = IN_PROGRESS`;
- `content_read_started = false`.

Both use inherited canonical JSON, reject duplicate keys, and contain no containing/future commit SHA or self digest.

## G. GH2 activation merge gate

Before any GH2 frozen Repair-2 content access require all on one exact reviewed head:

1. activation delta exactly the two create-only paths in Section F;
2. exact canonical JSON bytes validate;
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
15. canonical activation file bytes equal reviewed bytes;
16. fresh replay finds no concurrent GH2 conflict.

Only after item 16:

```text
GH2_CLAIM = CANONICAL
GH2_ACTIVATION = CANONICAL
FROZEN_REPAIR2_CONTENT_ACCESS = AUTHORIZED_FOR_BOUNDED_GH2_PREFLIGHT_ONLY
```

Any failure burns GH2 and requires a separate Founder repair. No pre-activation frozen-content read is permitted.

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

It may exist only if inherited Sections A-D PASS and the execution-binding inventory truthfully records every remaining execution requirement. It grants no execution authority.

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

`successor_candidate` is null or contains exactly `id`, `path`, `sha256`, `byte_length` with the GH2 successor identity above.

Compute `MANIFEST_BINDING_CORE_SHA256 = SHA256(canonical_manifest_binding_core_bytes)`.

`preflight-verdict.md` is UTF-8 without BOM, LF line endings, exactly one final LF, and must contain the exact decision ID, repair SHA/tree, activation receipt ID, activation merge SHA, manifest ID, binding-core SHA-256, and terminal state.

`preflight-result-manifest.json` is canonical JSON with exactly:

- `manifest_version = MESC-BT-PREFLIGHT-GH2-RESULT-MANIFEST-V1`;
- `manifest_binding_core`;
- `manifest_binding_core_sha256`;
- `artifacts`.

Its `artifacts` map contains exact `path`, `sha256`, `byte_length` for the two audits, inventory, verdict, and conditional successor iff non-null. It excludes `consumption-receipt.json` and its own digest. Any later blocker removes a provisional successor and rebuilds the package before terminal content freeze.

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

The receipt contains no containing receipt-commit SHA, future result merge SHA, or self digest.

## M. Result merge and canonical adoption

The result PR uses exact `GH2_RESULT_HEAD`, base `main`, same repository.

Before merge require: exactly one selected GH2 activation PR and one selected GH2 result PR; zero reserved conflicts; activation bytes unchanged; complete Section J graph/immutability proof; exact Section K/L bindings; final-review `main` to result head changes only GH2 result allowlist paths; exact-head CI and CodeQL PASS; fresh independent exact-head governance review with no blocker; unresolved blocking threads 0; unchanged final-review main/head; expected-head merge.

After merge require canonical main equals returned result merge; ordered parents exactly `[PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA]`; exact tree/path scope; hosting verification `verified=true`, `reason=valid`, non-null signature/payload; merged result bytes identical to reviewed head; fresh replay still exactly one activation and result PR with zero conflicts.

Only then create one create-only adoption PR containing exactly one new path:

```text
specs/mesc-backbone-tournament/execution-preflight-1-gh2-adoption/<RESULT_MERGE_SHA>/canonical-adoption-verification.json
```

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
- `preflight_result_manifest_sha256`;
- `result_package_artifacts`;
- `terminal_receipt_commit`;
- `terminal_receipt_sha256`;
- `merge_signature_verification`;
- `failed_checks`;
- `outcome`.

`ordered_parents` equals exactly `[PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA]`. `result_package_artifacts` is the complete lexical-path-ordered array of all reviewed GH2 result files, each object containing exactly `path`, `sha256`, `byte_length`. `merge_signature_verification` contains exactly `verified`, `reason`, `signature_sha256`, `payload_sha256`, with SHA-256 values derived from the non-null authoritative source texts. `failed_checks` is `[]` only if every post-result-merge predicate passes; otherwise it contains lexically sorted deterministic predicate IDs and `outcome = BLOCKED`. If `failed_checks=[]`, `outcome` equals the receipt terminal state.

The adoption PR itself must have an exact one-file create-only delta, exact-head CI/CodeQL/review gates, expected-head merge, and post-merge verification. Only after that merge may GH2 be reported canonically terminal.

## N. Hard stop

If GH2 becomes canonically terminal ready, report only:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

Do not start tournament execution. A separate Founder `FD-MESC-BT-EXEC-1` authorization is mandatory.

Throughout repair/GH2: no model weights, gated access/terms acceptance, provider prompts, inference, generation, training, model retrieval, ranking, winner selection, PHI, or tournament execution.