# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1

Status: **DRAFT ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-21

This contract is complete only if every applicable predicate below is mechanically proven. Ambiguity, missing hosting data, stale exact-head evidence, or inability to prove a required predicate => `BLOCKED`.

## A. Exact inheritance anchors and replacement boundary

The prior authorization is fixed as:

```text
OLD_DECISION_ID = FD-MESC-BT-EXEC-1-PREFLIGHT
OLD_AUTHORIZATION_MERGE_SHA = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6
OLD_AUTHORIZATION_MERGE_TREE = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70
OLD_ACTIVATION_RECEIPT_ID = 5d544ddb1406992c703c4ae9274daba6701089b3fdb994a080207af107256634
```

Its exact four authorization-package blobs are:

```text
specs/mesc-backbone-tournament/execution-preflight-1/README.md                e801fb6d66c2f24e6a0294f7e7c80b35cac99a86
specs/mesc-backbone-tournament/execution-preflight-1/acceptance.md            7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
specs/mesc-backbone-tournament/execution-preflight-1/founder-authorization.md 9656fe06d791d86a960787c9451a0ee970e84c3a
specs/mesc-backbone-tournament/execution-preflight-1/plan.md                  b741fb1b7888a2ac861832390ce6586246818814
```

The replacement episode is:

```text
NEW_DECISION_ID = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1
INHERITED_ACCEPTANCE_BLOB_SHA = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
```

The original `acceptance.md` blob remains normative only for these scientific/content rules, with their exact original values and predicates:

1. original Section A Repair-2 canonical ancestry, path/blob identity, frozen-content digest verification, and derived prompt bindings;
2. original Section B `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` serialization and SHA-256 rule;
3. original Section C R2 provenance audit predicates; and
4. original Section D corpus specification / manifest conformance audit predicates.

Original Section E result-package identity/binding is **not inherited**. Original Sections F onward ref/claim/result/CAS/adoption lifecycle is **not inherited**. They are replaced in full by this GH1 contract. This prevents any worker from mixing the old decision/authorization identity with the GH1 result identity.

No Repair-2 frozen artifact path, blob, digest, schema, corpus rule, prompt rule, scoring rule, provenance rule, or conformance rule is changed by this repair.

## B. Old episode revalidation before repair adoption

Before this repair may be marked Ready and again immediately before merge, mechanically prove all currently observable hosting/repository predicates below using metadata only:

1. canonical `main` still descends from `OLD_AUTHORIZATION_MERGE_SHA`;
2. that commit's tree remains exactly `OLD_AUTHORIZATION_MERGE_TREE`;
3. the old authorization's exact current `CLAIM_REF` is absent;
4. the old authorization's exact current `RESULT_REF` is absent;
5. no PR is structurally selected as the old current-episode result PR;
6. no PR in the old current-authorization reserved result namespace conflicts with the old receipt identity;
7. no old activation receipt or consumption receipt is present on canonical `main`;
8. no canonical repository artifact asserts frozen Repair-2 content access under the old episode; and
9. the repair record remains consistent with the last verified live worker state:

```text
OLD_EPISODE_LAST_VERIFIED_STATE = NOT_STARTED
OLD_FROZEN_CONTENT_ACCESS = NOT_PERFORMED
OLD_MODEL_ACCESS = NOT_PERFORMED
OLD_TOURNAMENT_EXECUTION = NOT_PERFORMED
```

The old exact claim/result identities are derived exactly from `INHERITED_ACCEPTANCE_BLOB_SHA`. Any contrary current hosting/canonical evidence => `BLOCKED` and this repair MUST NOT merge.

A verified canonical merge of this repair permanently retires the old decision regardless of later branch/ref deletion or recreation:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT = SUPERSEDED_NONREUSABLE
OLD_CLAIM_REF_CREATION = PERMANENTLY_FORBIDDEN
OLD_RESULT_REF_CREATION = PERMANENTLY_FORBIDDEN
```

The replacement GH1 decision is a distinct one-shot authorization; it never treats a failed old protection predicate as PASS.

## C. Repair authorization receipt identity

After this repair package is canonically merged and post-merge verified, derive `GH1_ACTIVATION_RECEIPT_ID` as SHA-256 of canonical JSON under inherited `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` containing exactly:

- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `repair_authorization_merge_sha = <canonical repair merge SHA>`;
- `repair_authorization_merge_tree = <canonical repair merge tree>`;
- `repair_package_files = <ordered four-object array>`;
- `receipt_version = MESC-BT-PREFLIGHT-GH1-RECEIPT-V1`.

`repair_package_files` contains exactly, in this order, one object with exact keys `path` and `git_blob_sha` for each canonical repair-merge file:

1. `specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/README.md`;
2. `specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/acceptance.md`;
3. `specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/founder-authorization.md`;
4. `specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/plan.md`.

Missing, reordered, duplicated, extra, or mismatched path/blob entries => `BLOCKED`.

## D. GitHub-native deterministic identities

For the canonical repair authorization merge SHA/tree and derived GH1 receipt ID:

```text
GH1_ACTIVATION_HEAD = governance/fd-mesc-bt-exec-1-preflight-gh1-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>
GH1_RESULT_HEAD = governance/fd-mesc-bt-exec-1-preflight-gh1-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>

GH1_ACTIVATION_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-gh1-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>/
GH1_CLAIM_RECORD_PATH = <GH1_ACTIVATION_ROOT>claim-record.json
GH1_ACTIVATION_RECEIPT_PATH = <GH1_ACTIVATION_ROOT>activation-receipt.json

GH1_RESULT_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-gh1-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>/
GH1_ADOPTION_PREFIX = specs/mesc-backbone-tournament/execution-preflight-1-gh1-adoption/
```

The two head names are staging identities only. A branch by itself grants no authority and is not a claim/result. Canonical authority is determined only by the exact structurally selected PR and its verified merge into canonical `main`.

## E. GH1 replay state and namespace conflict detection

Before opening the activation PR, immediately before its merge, immediately before opening the result PR, and immediately before result merge, enumerate the complete PR population for `TheHalfMoon/MESC` in open + closed + merged states. Every page/cursor must be consumed.

Apply these structural rules to every PR.

### E.1 Activation selector

A PR is the GH1 activation PR iff all are true:

- base repository full name = `TheHalfMoon/MESC`;
- base ref = `main`;
- head repository full name = `TheHalfMoon/MESC`;
- retained `headRefName` = exact `GH1_ACTIVATION_HEAD`.

### E.2 Result selector

A PR is the GH1 result PR iff the same base/head repository predicates hold and retained `headRefName` = exact `GH1_RESULT_HEAD`.

### E.3 Namespace-conflict detector

Any same-repository PR whose retained head begins with either literal prefix:

```text
governance/fd-mesc-bt-exec-1-preflight-gh1-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/
governance/fd-mesc-bt-exec-1-preflight-gh1-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/
```

is valid only if it exactly matches its corresponding selector. Different receipt suffixes, malformed/non-64-lowercase-hex suffixes, extra path segments, or wrong base repository/ref => `BLOCKED`.

Before the activation PR is opened:

- `GH1_CLAIM_RECORD_PATH` absent from canonical `main`;
- `GH1_ACTIVATION_RECEIPT_PATH` absent from canonical `main`;
- complete `GH1_RESULT_ROOT` absent from canonical `main`;
- zero selected activation PRs;
- zero selected result PRs;
- zero reserved namespace conflicts.

Opening the exact activation PR changes GH1 replay state from `UNUSED` to `ISSUED` but grants no frozen-content authority. Once any selected activation PR record exists, GH1 can never be classified `UNUSED` again, even if its branch is deleted or PR is closed.

Branch/ref objects are explicitly non-authoritative for GH1. Durable one-shot replay evidence is the complete retained PR population plus canonical-main activation/result path presence. This is an intentional replacement of old Section F.2, not a claim that the old ref/history replay gate passed.

Any inability to enumerate the complete PR population or to read the structural fields required above => `BLOCKED`.

## F. Claim + activation candidate files

The activation PR changes exactly two repository paths, both newly added:

1. `GH1_CLAIM_RECORD_PATH`;
2. `GH1_ACTIVATION_RECEIPT_PATH`.

Relative to the exact final-review `main`, there must be zero modifications, deletions, renames, copies, replacements, or unrelated additions.

Both files are canonical JSON under inherited `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` and reject duplicate member names at every nesting level.

### F.1 `claim-record.json`

Exact top-level keys:

- `record_version = MESC-BT-PREFLIGHT-GH1-CLAIM-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `superseded_decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT`;
- `superseded_authorization_merge_sha = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6`;
- `superseded_activation_receipt_id = 5d544ddb1406992c703c4ae9274daba6701089b3fdb994a080207af107256634`;
- `claim_mode = CANONICAL_MAIN_MERGE`;
- `frozen_content_read_before_activation = false`.

Unknown, missing, duplicate, or extra top-level keys => `BLOCKED`.

### F.2 `activation-receipt.json`

Exact top-level keys:

- `receipt_version = MESC-BT-PREFLIGHT-GH1-ACTIVATION-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `claim_record_sha256` = SHA-256 of exact canonical `claim-record.json` bytes;
- `inherited_acceptance_blob_sha = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`;
- `state = IN_PROGRESS`;
- `content_read_started = false`.

Unknown, missing, duplicate, or extra top-level keys => `BLOCKED`.

Neither file contains its containing commit SHA, future merge SHA, or its own file digest.

## G. Atomic canonical claim + activation merge

The activation branch/PR is staging only. Frozen Repair-2 content remains forbidden until all of these pass on one exact head:

1. activation PR delta relative to exact final-review `main` is exactly the two create-only paths in Section F;
2. both canonical JSON files validate exactly;
3. complete PR replay recheck finds exactly one selected activation PR, zero selected result PRs, and zero reserved conflicts;
4. canonical `main` equals the exact premerge main SHA used for final review;
5. activation PR head equals the exact reviewed head SHA;
6. CI and CodeQL pass at exact head;
7. fresh independent governance review passes at exact head;
8. unresolved blocking review threads = 0;
9. merge uses `expected_head_sha = <exact reviewed activation head>`;
10. GitHub reports merge success;
11. canonical `main` is re-read and equals the returned merge SHA;
12. merge commit has ordered parents exactly `[PREMERGE_MAIN_SHA, REVIEWED_ACTIVATION_HEAD_SHA]`;
13. merge tree and premerge-main→merge changed paths prove exactly the two activation files and no other repository path;
14. hosting merge verification reports `verified = true`, `reason = valid`, with non-null source `verification.signature` and `verification.payload`;
15. `GH1_CLAIM_RECORD_PATH` and `GH1_ACTIVATION_RECEIPT_PATH` exist on canonical `main` with exact reviewed bytes; and
16. a fresh complete PR replay check finds no unexpected concurrent GH1 activation/result conflict.

Only after item 16 passes does state become:

```text
GH1_CLAIM = CANONICAL
GH1_ACTIVATION = CANONICAL
FROZEN_REPAIR2_CONTENT_ACCESS = AUTHORIZED_FOR_BOUNDED_PREFLIGHT_ONLY
```

Any failure through item 16 => `BLOCKED`; no frozen-content read is permitted. A merge that succeeds but fails post-merge verification burns GH1 and requires a separately reviewed Founder repair/authorization; it must not be retried as `UNUSED`.

Define the verified merge SHA from this section as `GH1_ACTIVATION_MERGE_SHA` and its tree as `GH1_ACTIVATION_MERGE_TREE`.

## H. Post-activation scientific audit

Only after Section G passes, execute the exact inherited scientific/content checks from `INHERITED_ACCEPTANCE_BLOB_SHA` original Sections A–D for:

- canonical Repair-2 ancestry and path/blob identities;
- exact frozen content digests and derived prompt bindings;
- canonical JSON serialization;
- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`.

All original no-model, no-provider, no-PHI, no-regeneration, no-substitution rules remain binding.

The result-package construction itself is GH1-specific and is defined below; no worker may use the old Section E manifest identity or old result root.

## I. Exact GH1 result graph, path allowlist, and immutability

The only permitted paths under `GH1_RESULT_ROOT` are:

1. `r2-provenance-audit.json`;
2. `corpus-conformance-audit.json`;
3. `execution-binding-inventory.md`;
4. `preflight-verdict.md`;
5. `preflight-result-manifest.json`;
6. conditional `execution-authorization-candidate.md`;
7. terminal-only `consumption-receipt.json`.

No other path under or outside `GH1_RESULT_ROOT` may be changed by the GH1 result lineage.

The result branch is created from exact `GH1_ACTIVATION_MERGE_SHA`. Every result-lineage commit before canonical result merge MUST:

- have exactly one parent;
- have its parent equal to the immediately preceding valid GH1 result target, with the first result commit parent exactly `GH1_ACTIVATION_MERGE_SHA`;
- contain no merge commit;
- change paths only inside `GH1_RESULT_ROOT` and only from the allowlist above;
- never modify/delete `GH1_CLAIM_RECORD_PATH` or `GH1_ACTIVATION_RECEIPT_PATH`;
- never change any frozen Repair-2 path;
- never contain `consumption-receipt.json` before the terminal-receipt commit.

Before terminal-content finalization, intermediate result commits may add/update the six non-receipt allowlisted outputs. The conditional successor may be removed only when a required blocked-package rebuild sets successor binding to null.

`TERMINAL_CONTENT_COMMIT` is the first commit at which the complete byte-final non-receipt result package is finalized. At and after this commit, these paths are immutable:

- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`;
- `preflight-result-manifest.json`;
- `execution-authorization-candidate.md` when present.

`TERMINAL_RECEIPT_COMMIT` MUST be the direct child of `TERMINAL_CONTENT_COMMIT`, have exactly one parent, and its only tree delta MUST be creation of `<GH1_RESULT_ROOT>consumption-receipt.json`. No later commit is permitted on the result lineage before canonical result adoption. Any force-push, non-fast-forward/sideways retarget, merge commit, parent mismatch, out-of-scope path, post-terminal artifact mutation, receipt replacement, or extra post-receipt commit => `BLOCKED`.

Immediately before canonical result merge, compare exact final-review `main` to exact reviewed result head and require every changed repository path to be inside `GH1_RESULT_ROOT` and in the allowlist above. Any unrelated path => `BLOCKED`.

## J. Exact GH1 result-package binding

Original Section E is replaced completely by this section.

### J.1 GH1 successor identity

If and only if all inherited scientific/content checks pass and the execution-binding inventory is complete for the provisional ready path, the conditional successor identity is:

```text
GH1_SUCCESSOR_ID = FD-MESC-BT-EXEC-1-CANDIDATE-GH1-V1
GH1_SUCCESSOR_PATH = <GH1_RESULT_ROOT>execution-authorization-candidate.md
```

Provisional rendering grants no execution authority. If prerequisites do not pass or any later GH1 check blocks, the successor file MUST be absent and its manifest binding MUST be `null`.

### J.2 `manifest_binding_core`

Construct canonical JSON under inherited Section B with **exactly these top-level keys**:

- `manifest_id = MESC-BT-PREFLIGHT-GH1-RESULT-MANIFEST-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `repair_authorization_merge_sha` = exact canonical repair authorization merge SHA;
- `repair_authorization_merge_tree` = exact canonical repair authorization merge tree;
- `activation_receipt_id` = exact `GH1_ACTIVATION_RECEIPT_ID`;
- `activation_merge_sha` = exact `GH1_ACTIVATION_MERGE_SHA`;
- `inherited_contract` = exact object defined below;
- `frozen_input_digest_map` = exact unchanged Repair-2 digest-map object required by old Section E at `INHERITED_ACCEPTANCE_BLOB_SHA`;
- `artifacts` = exact object defined below for the two audits and execution-binding inventory;
- `verdict_path = <GH1_RESULT_ROOT>preflight-verdict.md`;
- `successor_candidate` = `null` or exact object defined below.

`inherited_contract` has exactly:

- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT`;
- `authorization_merge_sha = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6`;
- `authorization_merge_tree = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70`;
- `acceptance_blob_sha = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`.

The GH1 result identity is therefore always the top-level GH1 decision/repair/activation identity; the old identity may appear only inside `inherited_contract` as the immutable source of scientific rules.

`frozen_input_digest_map` MUST preserve exactly the old Section E key/value object derived from the frozen Repair-2 bindings. It may not contain GH1 lifecycle fields and no digest value may be changed, omitted, renamed, or added.

`artifacts` has exactly three keys whose values each contain exactly `path`, `sha256`, and `byte_length`:

- `r2_provenance_audit` -> `<GH1_RESULT_ROOT>r2-provenance-audit.json`;
- `corpus_conformance_audit` -> `<GH1_RESULT_ROOT>corpus-conformance-audit.json`;
- `execution_binding_inventory` -> `<GH1_RESULT_ROOT>execution-binding-inventory.md`.

Each SHA-256 is 64 lowercase hex and each byte length is a positive base-10 integer.

When non-null, `successor_candidate` contains exactly:

- `id = FD-MESC-BT-EXEC-1-CANDIDATE-GH1-V1`;
- `path = <GH1_RESULT_ROOT>execution-authorization-candidate.md`;
- `sha256` = exact full-file SHA-256;
- `byte_length` = exact positive integer.

Compute:

```text
MANIFEST_BINDING_CORE_SHA256 = SHA256(canonical_manifest_binding_core_bytes)
```

### J.3 Verdict

Generate `<GH1_RESULT_ROOT>preflight-verdict.md` as UTF-8 without BOM, LF line endings, exactly one final LF. It MUST contain the exact:

- `decision_id`;
- repair authorization merge SHA/tree;
- GH1 activation receipt ID;
- GH1 activation merge SHA;
- manifest ID;
- `MANIFEST_BINDING_CORE_SHA256`; and
- terminal preflight state (`BLOCKED` or `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`).

Compute its exact full-file SHA-256 and byte length.

### J.4 `preflight-result-manifest.json`

Generate canonical JSON under inherited Section B with exactly these top-level keys:

- `manifest_version = MESC-BT-PREFLIGHT-GH1-RESULT-MANIFEST-V1`;
- `manifest_binding_core` = exact J.2 object;
- `manifest_binding_core_sha256` = exact 64-lowercase-hex digest;
- `artifacts` = complete final result artifact map.

The complete final `artifacts` map contains exactly `path`, `sha256`, and `byte_length` for:

- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`;
- conditional `execution-authorization-candidate.md` iff J.2 successor is non-null.

It MUST NOT contain `consumption-receipt.json`, because the manifest is finalized in `TERMINAL_CONTENT_COMMIT` before the receipt exists. It MUST NOT contain its own file SHA-256. Its exact full-file SHA-256 is computed externally after serialization and bound by the terminal receipt and adoption record.

If any later predicate forces terminal `BLOCKED`, remove any provisional successor, set `successor_candidate = null`, rebuild J.2/J.3/J.4 from the blocked package, and only then create `TERMINAL_CONTENT_COMMIT`. Stale hashes or stale ready successor bytes => `BLOCKED`.

## K. Terminal consumption receipt

`TERMINAL_RECEIPT_COMMIT` adds only `<GH1_RESULT_ROOT>consumption-receipt.json` as required by Section I.

The receipt is canonical JSON under inherited Section B and contains exactly these top-level keys:

- `receipt_version = MESC-BT-PREFLIGHT-GH1-CONSUMPTION-V1`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `activation_merge_sha` = exact `GH1_ACTIVATION_MERGE_SHA`;
- `terminal_content_commit` = exact direct parent of `TERMINAL_RECEIPT_COMMIT`;
- `preflight_result_manifest_sha256` = exact SHA-256 of J.4 file bytes in terminal-content;
- `terminal_state = BLOCKED | PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`;
- `state = BLOCKED | CONSUMED`.

It MUST NOT contain its own containing commit SHA, future result merge SHA, or its own file digest.

A ready receipt requires:

```text
terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
state = CONSUMED
```

A blocked receipt requires:

```text
terminal_state = BLOCKED
state = BLOCKED
```

Any other pairing => `BLOCKED`.

## L. Canonical terminal result adoption

The deterministic result PR uses exact `GH1_RESULT_HEAD`, base `main`, and head repository `TheHalfMoon/MESC`.

Before result merge require all of these on one exact final head:

1. complete PR replay finds exactly one selected activation PR, exactly one selected result PR, and zero reserved namespace conflicts;
2. canonical activation files remain present and byte-identical on canonical `main`;
3. exact reviewed result head is `TERMINAL_RECEIPT_COMMIT`;
4. all Section I parent-count/parent/path/allowlist/immutability/terminal-receipt predicates pass for the complete result lineage from `GH1_ACTIVATION_MERGE_SHA`;
5. J.2/J.3/J.4 package bindings and K receipt validate exactly;
6. final-review `main` -> exact result head diff changes only allowlisted paths under `GH1_RESULT_ROOT`;
7. CI and CodeQL pass at exact head;
8. fresh independent exact-head governance review reports no blocking finding;
9. unresolved blocking review threads = 0;
10. canonical `main` remains the exact final-review premerge SHA;
11. merge uses `expected_head_sha = <exact reviewed TERMINAL_RECEIPT_COMMIT>`;
12. GitHub reports merge success;
13. returned merge SHA is freshly re-read as canonical `main`;
14. result merge ordered parents are exactly `[PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA]`;
15. premerge-main -> result-merge changed paths are exactly the reviewed allowlisted `GH1_RESULT_ROOT` paths and no others;
16. result merge tree contains exact reviewed result bytes;
17. hosting merge verification reports `verified = true`, `reason = valid`, with non-null source `verification.signature` and `verification.payload`; and
18. fresh replay finds no conflicting GH1 activation/result PR record.

Only after item 18 passes is the terminal state canonically adopted. Define returned verified merge SHA/tree as `GH1_RESULT_MERGE_SHA` / `GH1_RESULT_MERGE_TREE`.

A result branch by itself is never canonical authority. Branch deletion after canonical adoption does not remove authority because the verified canonical merge and retained PR record are durable. Any branch movement before merge invalidates exact-head evidence and requires a fresh full review cycle.

## M. Exact GH1 adoption-record schema and publication

After verified result merge, publish exactly one create-only record at:

```text
GH1_ADOPTION_RECORD_PATH = specs/mesc-backbone-tournament/execution-preflight-1-gh1-adoption/<GH1_RESULT_MERGE_SHA>/canonical-adoption-verification.json
```

The record is canonical JSON under inherited Section B with:

```text
record_version = MESC-BT-PREFLIGHT-GH1-CANONICAL-ADOPTION-V1
```

and exactly these top-level keys:

- `record_version`;
- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `activation_merge_sha`;
- `result_merge_sha`;
- `result_merge_tree`;
- `ordered_parents` = exactly `[PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA]`;
- `reviewed_result_head_sha` = exact `TERMINAL_RECEIPT_COMMIT`;
- `terminal_content_commit`;
- `preflight_result_manifest_sha256`;
- `terminal_receipt_sha256` = exact SHA-256 of canonical `consumption-receipt.json` bytes in reviewed result head;
- `result_package_artifacts` = complete path/SHA-256/byte-length map for every final `GH1_RESULT_ROOT` file including the consumption receipt;
- `merge_signature_verification` = exact nested object below;
- `failed_checks` = deterministic lexical array of failed predicates from the closed allowlist below;
- `outcome = CANONICAL_ADOPTION_VERIFIED | CANONICAL_ADOPTION_VERIFICATION_FAILED`.

`merge_signature_verification` contains exactly:

- `verified` = hosting verification boolean;
- `reason` = hosting verification reason NFC string;
- `signature_sha256` = SHA-256 of exact hosting `verification.signature` UTF-8 text, or `null` iff hosting source is null;
- `payload_sha256` = SHA-256 of exact hosting `verification.payload` UTF-8 text, or `null` iff hosting source is null.

A signature PASS requires `verified = true` and both hosting source texts present/non-null; otherwise adoption verification fails.

The only permitted `failed_checks` values are:

```text
ACTIVATION_BINDING_MISMATCH
ADOPTION_PATH_ALREADY_EXISTS
ADOPTION_PATH_SHA_MISMATCH
MANIFEST_BINDING_MISMATCH
RESULT_HEAD_MISMATCH
RESULT_MERGE_NOT_CANONICAL
RESULT_MERGE_PARENT_MISMATCH
RESULT_MERGE_TREE_MISMATCH
RESULT_PATH_SCOPE_INVALID
SIGNATURE_EVIDENCE_INVALID
SIGNATURE_NOT_VERIFIED
TERMINAL_RECEIPT_MISMATCH
```

The array is the complete failed-predicate set in lexical order with no aliases or unknown values. `outcome = CANONICAL_ADOPTION_VERIFIED` iff `failed_checks = []` and every record field revalidates.

Immediately before opening the adoption PR and again immediately before its merge, `GH1_ADOPTION_RECORD_PATH` MUST be absent from canonical `main`. The path's `<GH1_RESULT_MERGE_SHA>` segment must exactly equal the record's and mechanically verified result merge SHA.

The adoption PR changes exactly one repository path, `GH1_ADOPTION_RECORD_PATH`, as a newly added file. No modification/deletion/rename/copy/replacement/unrelated addition is permitted. Require exact-head CI/CodeQL/fresh independent review/zero blocking threads, unchanged final-review `main`, merge with exact `expected_head_sha`, and post-merge SHA/tree/ordered-parent/signature/path verification.

`CANONICAL_ADOPTION_VERIFIED = PASS` only after the adoption record itself is present on canonical `main` with `outcome = CANONICAL_ADOPTION_VERIFIED` and all fields revalidate. The adoption record never changes GH1 result bytes or grants tournament execution authority.

## N. Absolute non-authority boundary

Neither this hosting repair, its canonical adoption, nor a successful GH1 preflight authorizes model/tournament execution. Throughout this repair and GH1 preflight:

```text
MODEL_WEIGHT_ACCESS = FORBIDDEN
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = FORBIDDEN
PROMPT_SERIALIZATION_TO_MODEL = FORBIDDEN
INFERENCE = FORBIDDEN
GENERATION = FORBIDDEN
TRAINING = FORBIDDEN
RETRIEVAL = FORBIDDEN
RANKING = FORBIDDEN
WINNER_SELECTION = FORBIDDEN
BACKBONE_TOURNAMENT_EXECUTION = FORBIDDEN
```

A GH1 ready verdict is only eligible for a separately reviewed Founder execution-authorization decision.