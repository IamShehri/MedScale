# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1

Status: **DRAFT ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-21

This contract is complete only if every applicable predicate below is mechanically proven. Ambiguity, missing hosting data, stale exact-head evidence, or inability to prove a required predicate => `BLOCKED`.

## A. Exact inheritance anchors

The superseded-unstarted authorization is fixed as:

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
```

The original `acceptance.md` blob above remains the normative source for its Sections A–E scientific/content/serialization/package rules and all no-model/no-PHI constraints, except where a field or step explicitly depends on the old `CLAIM_REF`, `RESULT_REF`, ref-protection, ref-CAS, or old result-PR evidence lifecycle. Those lifecycle-dependent fields/steps are replaced only by this document.

No Repair-2 frozen artifact path, blob, digest, schema, corpus rule, prompt rule, scoring rule, provenance rule, or conformance rule is changed by this repair.

## B. Old episode must be provably unstarted

Before this repair may be marked Ready and again immediately before merge, mechanically prove all of the following using hosting/repository metadata only:

1. canonical `main` still descends from `OLD_AUTHORIZATION_MERGE_SHA`;
2. its tree remains exactly `OLD_AUTHORIZATION_MERGE_TREE` at that commit;
3. the old authorization's exact `CLAIM_REF` does not exist;
4. the old authorization's exact `RESULT_REF` does not exist;
5. no PR is structurally selected as the old current-episode result PR;
6. no PR in the old current-authorization reserved result namespace conflicts with the old receipt identity;
7. no old activation receipt or consumption receipt is present on canonical `main`;
8. no prior worker report or canonical artifact asserts frozen Repair-2 content access under the old episode; and
9. the current repair record truth remains:

```text
OLD_EPISODE = NOT_STARTED
OLD_FROZEN_CONTENT_ACCESS = NOT_PERFORMED
OLD_MODEL_ACCESS = NOT_PERFORMED
OLD_TOURNAMENT_EXECUTION = NOT_PERFORMED
```

The old exact claim/result refs are derived exactly from the old acceptance blob. Any observed old claim/result/receipt/result-PR evidence means this repair cannot supersede the old authorization and => `BLOCKED`.

## C. Repair activation receipt identity

After this repair package is canonically merged and post-merge verified, derive `GH1_ACTIVATION_RECEIPT_ID` as SHA-256 of canonical JSON under inherited `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` containing exactly:

- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- `repair_authorization_merge_sha = <canonical repair merge SHA>`;
- `repair_authorization_merge_tree = <canonical repair merge tree>`;
- `repair_package_files = <ordered four-object array>`;
- `receipt_version = MESC-BT-PREFLIGHT-GH1-RECEIPT-V1`.

`repair_package_files` contains exactly, in this order, the canonical repair-merge Git blob SHA for:

1. `README.md`;
2. `acceptance.md`;
3. `founder-authorization.md`;
4. `plan.md`;

all under `specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/`.

Missing/reordered/extra paths or mismatched blob identities => `BLOCKED`.

## D. GitHub-native reserved identities

For the canonical repair authorization merge SHA and derived GH1 receipt ID:

```text
GH1_ACTIVATION_HEAD = governance/fd-mesc-bt-exec-1-preflight-gh1-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>
GH1_RESULT_HEAD = governance/fd-mesc-bt-exec-1-preflight-gh1-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>

GH1_ACTIVATION_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-gh1-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>/
GH1_CLAIM_RECORD_PATH = <GH1_ACTIVATION_ROOT>claim-record.json
GH1_ACTIVATION_RECEIPT_PATH = <GH1_ACTIVATION_ROOT>activation-receipt.json

GH1_RESULT_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-gh1-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/<GH1_ACTIVATION_RECEIPT_ID>/
```

The two head names are staging identities only. A branch by itself grants no authority and is not a claim. Canonical authority is determined by exact PR structure and verified merge into `main`.

## E. Replay state without mutable-ref authority

Before opening the activation PR, and again immediately before its merge, enumerate the complete PR population for `TheHalfMoon/MESC` in open + closed + merged states. Every page/cursor must be consumed.

Apply these structural rules to every PR:

### E.1 Activation selector

A PR is the GH1 activation PR iff:

- base repository = `TheHalfMoon/MESC`;
- base ref = `main`;
- head repository = `TheHalfMoon/MESC`;
- retained `headRefName` = exact `GH1_ACTIVATION_HEAD`.

### E.2 Result selector

A PR is the GH1 result PR iff the same base/head repository predicates hold and retained `headRefName` = exact `GH1_RESULT_HEAD`.

### E.3 Namespace-conflict detector

Any same-repository PR whose retained head begins with either:

```text
governance/fd-mesc-bt-exec-1-preflight-gh1-activation/<REPAIR_AUTHORIZATION_MERGE_SHA>/
governance/fd-mesc-bt-exec-1-preflight-gh1-result/<REPAIR_AUTHORIZATION_MERGE_SHA>/
```

is valid only if it exactly matches its corresponding selector. Different receipt suffixes, malformed suffixes, extra segments, or wrong base => `BLOCKED`.

Before the activation PR is opened, `GH1_CLAIM_RECORD_PATH`, `GH1_ACTIVATION_RECEIPT_PATH`, and the complete `GH1_RESULT_ROOT` must be absent from canonical `main`; zero selected activation PRs and zero selected result PRs must exist. Any reserved conflict => `BLOCKED`.

Opening the exact activation PR changes state from `UNUSED` to `ISSUED` but does not authorize frozen-content access. Once any exact activation PR record exists, the episode can never be classified `UNUSED` again, even if the branch is deleted or the PR is closed.

No exhaustive traversal of unrelated historical commit objects is required for GH1 replay classification because branch/ref objects are explicitly non-authoritative. Durable replay evidence is the complete retained PR population plus canonical-main path presence. This is an intentional replacement of the old F.2 history/ref search, not a claim that the old search passed.

## F. Claim + activation candidate files

The activation PR changes exactly two repository paths, both newly added:

1. `GH1_CLAIM_RECORD_PATH`;
2. `GH1_ACTIVATION_RECEIPT_PATH`.

No modification/deletion/rename/copy/unrelated addition is permitted.

Both files are canonical JSON under inherited `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` and reject duplicate member names.

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

### F.2 `activation-receipt.json`

Exact top-level keys:

- `receipt_version = MESC-BT-PREFLIGHT-GH1-ACTIVATION-V1`;
- `decision_id`;
- `repair_authorization_merge_sha`;
- `repair_authorization_merge_tree`;
- `activation_receipt_id`;
- `claim_record_sha256` = SHA-256 of exact canonical `claim-record.json` bytes;
- `inherited_acceptance_blob_sha = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`;
- `state = IN_PROGRESS`;
- `content_read_started = false`.

Neither file contains its containing commit SHA, future merge SHA, or its own file digest.

## G. Atomic canonical claim + activation

The activation branch/PR is staging only. Frozen Repair-2 content remains forbidden until all of these pass on one exact head:

1. activation PR delta is exactly the two create-only paths in Section F;
2. both canonical JSON files validate exactly;
3. complete PR replay recheck finds exactly one selected activation PR, zero selected result PRs, and zero reserved conflicts;
4. canonical `main` equals the exact premerge main SHA used for final review;
5. activation PR head equals the exact reviewed head SHA;
6. CI and CodeQL pass at exact head;
7. required fresh independent governance review passes at exact head;
8. unresolved blocking review threads = 0;
9. merge uses `expected_head_sha = <exact reviewed activation head>`;
10. GitHub reports merge success;
11. canonical `main` is re-read and equals the returned merge SHA;
12. merge tree, ordered parents, changed paths, and hosting signature verification are mechanically checked;
13. `GH1_CLAIM_RECORD_PATH` and `GH1_ACTIVATION_RECEIPT_PATH` exist on canonical `main` with exact reviewed bytes; and
14. no unexpected concurrent GH1 activation/result PR conflict appeared.

Only after item 14 passes does the state become:

```text
GH1_CLAIM = CANONICAL
GH1_ACTIVATION = CANONICAL
FROZEN_REPAIR2_CONTENT_ACCESS = AUTHORIZED_FOR_BOUNDED_PREFLIGHT_ONLY
```

Any failure through item 14 => `BLOCKED`; no frozen-content read is permitted. A merge that succeeded but fails post-merge verification burns the episode and requires a separately reviewed repair; it must not be retried as `UNUSED`.

## H. Post-activation scientific audit

After Section G passes, execute the inherited original acceptance blob's exact scientific/content checks for:

- canonical Repair-2 path/blob identities;
- exact frozen content digests and derived prompt bindings;
- canonical JSON serialization;
- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`;
- `preflight-result-manifest.json`;
- conditional `execution-authorization-candidate.md` only when all inherited readiness predicates pass.

All original no-model, no-provider, no-PHI, no-regeneration, no-substitution rules remain binding.

The replacement result files live under `GH1_RESULT_ROOT`; their internal inherited result-relative names remain unchanged.

## I. Terminal result PR and non-self-referential receipt

The deterministic result PR uses exact `GH1_RESULT_HEAD`, base `main`, same repository.

The final result branch contains a byte-final **terminal-content commit** followed by one direct child **terminal-receipt commit**. The terminal receipt commit's only delta relative to terminal-content is creation of:

```text
<GH1_RESULT_ROOT>consumption-receipt.json
```

`consumption-receipt.json` is canonical JSON and binds only already-known objects. Exact top-level keys:

- `receipt_version = MESC-BT-PREFLIGHT-GH1-CONSUMPTION-V1`;
- `decision_id`;
- `repair_authorization_merge_sha`;
- `activation_receipt_id`;
- `activation_merge_sha` = verified Section G merge SHA;
- `terminal_content_commit` = direct parent of the receipt commit;
- `preflight_result_manifest_sha256`;
- `terminal_state = BLOCKED | PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`;
- `state = BLOCKED | CONSUMED`.

It MUST NOT contain its own containing commit SHA or future result merge SHA.

A ready receipt requires `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` and `state = CONSUMED`. A blocked receipt requires `terminal_state = BLOCKED` and `state = BLOCKED`.

## J. Canonical terminal adoption

Before result merge, require:

1. exactly one selected result PR and no namespace conflict;
2. exact reviewed final head is the terminal-receipt commit;
3. terminal receipt direct-parent relationship and one-path receipt delta validate;
4. result package/manifest/artifact hashes validate;
5. CI and CodeQL pass at exact head;
6. fresh independent exact-head governance review has no blocker;
7. unresolved blocking review threads = 0;
8. canonical `main` remains the exact final-review premerge SHA;
9. merge uses `expected_head_sha = <exact reviewed result head>`;
10. returned merge SHA becomes canonical `main` and post-merge tree/parents/signature are verified;
11. the canonical merge contains exactly the reviewed GH1 result package bytes plus normal merge ancestry effects; and
12. the terminal receipt remains byte-identical to the reviewed head.

Only then is the terminal state canonically adopted.

The result branch may later be deleted or change without changing canonical authority; canonical authority is the verified result merge and retained PR record. Any branch movement before merge invalidates exact-head evidence and requires a fresh review cycle.

## K. Adoption record

After verified result merge, publish exactly one create-only canonical adoption record at:

```text
specs/mesc-backbone-tournament/execution-preflight-1-gh1-adoption/<RESULT_MERGE_SHA>/canonical-adoption-verification.json
```

It must bind the repair authorization merge, GH1 receipt ID, activation merge, result merge SHA/tree/ordered parents/signature, reviewed result head, terminal-content commit, terminal receipt SHA-256, manifest SHA-256, and complete artifact path/hash/length map.

The adoption PR changes exactly that one new path and merges with expected-head protection after exact-head review. A pre-existing path, replacement, unrelated delta, path/SHA mismatch, or failed post-merge verification => adoption verification failure.

## L. Absolute non-authority boundary

Neither this repair nor a successful GH1 preflight authorizes model/tournament execution. Throughout this repair and GH1 preflight:

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
