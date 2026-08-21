# Plan — FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1

Status: **DRAFT PLAN — NO EXECUTION AUTHORITY**

Date: 2026-08-21

## Objective

Replace the unexecutable exact-target protected-ref lifecycle in canonical `FD-MESC-BT-EXEC-1-PREFLIGHT` with a GitHub.com-native canonical-merge lifecycle while preserving every scientific/content/no-model safety boundary.

This plan is docs/governance only. It must not read frozen Repair-2 content, create the old claim/result refs, access models/providers, or execute the tournament.

## Exact starting point

```text
CANONICAL_MAIN_AT_REPAIR_OPEN = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6
CANONICAL_TREE_AT_REPAIR_OPEN = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70
PR_131 = MERGED_CANONICAL
OLD_DECISION = FD-MESC-BT-EXEC-1-PREFLIGHT
OLD_ACTIVATION = NOT_PERFORMED
OLD_FROZEN_CONTENT_ACCESS = NOT_PERFORMED
BACKBONE_TOURNAMENT_EXECUTION = NOT_STARTED
```

Live GitHub/canonical truth always overrides this recorded opening snapshot.

## Repair package scope

The cumulative repair PR delta must contain exactly four new files under:

```text
specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/
```

Files:

1. `README.md`
2. `acceptance.md`
3. `founder-authorization.md`
4. `plan.md`

Do not modify original PR #131 authorization files, frozen Repair-2 paths, source/runtime code, tests, dependencies, workflows, model configuration, or model artifacts.

## Draft qualification sequence

1. Re-read canonical `main`, PR #133 base/head, changed paths, old-episode observable state, and exact inherited PR #131 blobs.
2. Keep PR #133 Draft while any exact-head automation or independent review is pending/failing.
3. Require cumulative base→head changed paths to remain exactly the four repair files.
4. Require exact-head CI PASS and exact-head CodeQL PASS.
5. Request fresh independent exact-head governance review in Draft.
6. Treat every material correctness/security/governance/determinism finding as blocking until repaired or proven stale against newer exact-head text.
7. Repair only by ordinary history-preserving commits; no force-push, destructive reset/rebase, or history rewrite.
8. Every new commit invalidates earlier exact-head CI/review evidence.
9. Resolve/outdate all blocking review threads only after the current exact head mechanically contains the repair.
10. Re-run CI/CodeQL and fresh exact-head review on the unchanged repaired head.
11. Mark Ready only when Draft gates are all proven and `main`/head remain stable.
12. Perform a fresh post-Ready exact-head reconciliation; Draft reviews alone do not authorize merge.
13. Immediately before merge reverify exact head, exact main, exact four-path scope, CI, CodeQL, reviews, zero blocking threads, and old-decision revalidation.
14. Merge only with `expected_head_sha = <fully reviewed exact repair head>`.
15. Re-read canonical `main`; verify returned merge SHA/tree/ordered parents/path delta/signature evidence.
16. Stop after repair merge verification unless the Founder separately instructs continuation into GH1 activation qualification.

## Review finding reconciliation requirements

Any review finding that changes result identity or result tree scope must be reflected consistently in **all** governance documents that describe those semantics.

The single normative lifecycle contract is `acceptance.md`. `README.md`, `founder-authorization.md`, and this plan must reference the same exact active identity and result-scope rules; no sibling document may retain vague old wording that allows a second interpretation.

## Canonical effect after repair merge

Only after successful repair post-merge verification:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT = SUPERSEDED_NONREUSABLE
OLD_CLAIM_REF_CREATION = PERMANENTLY_FORBIDDEN
OLD_RESULT_REF_CREATION = PERMANENTLY_FORBIDDEN
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = AUTHORIZED_NOT_STARTED
```

The repair merge itself does not start GH1 and does not authorize Repair-2 frozen-content access.

## GH1 inheritance map

The exact old acceptance blob is:

```text
7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
```

GH1 inherits only old Sections A–D scientific/content rules. Old Section E result binding and old Sections F onward ref/CAS/result/adoption lifecycle are superseded.

Active GH1 fields are defined only by repair `acceptance.md` Sections C–M:

```text
decision = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1
authorization = canonical repair merge SHA/tree
activation = GH1_ACTIVATION_RECEIPT_ID + verified activation merge SHA
result root = GH1_RESULT_ROOT
manifest = MESC-BT-PREFLIGHT-GH1-RESULT-MANIFEST-V1
successor = FD-MESC-BT-EXEC-1-CANDIDATE-GH1-V1
consumption receipt = MESC-BT-PREFLIGHT-GH1-CONSUMPTION-V1
adoption record = MESC-BT-PREFLIGHT-GH1-CANONICAL-ADOPTION-V1
```

Old decision/authorization identity is historical provenance only inside `inherited_contract`.

## GH1 continuation plan after separate Founder instruction

### 1. Derive GH1 receipt identity

From the verified repair merge SHA/tree and exact four repair-package blob identities, derive `GH1_ACTIVATION_RECEIPT_ID` exactly as `acceptance.md` C specifies.

### 2. Metadata-only replay

Before activation candidate creation, enumerate the complete PR population and reserved GH1 namespaces under `acceptance.md` E. No frozen Repair-2 content read is permitted.

### 3. Activation candidate

Create the deterministic activation branch/PR with exactly two create-only canonical JSON paths:

```text
GH1_CLAIM_RECORD_PATH
GH1_ACTIVATION_RECEIPT_PATH
```

The PR/branch is staging only.

### 4. Exact-head activation qualification and merge

Require every `acceptance.md` G predicate: exact two-path delta, valid canonical JSON, complete replay, unchanged final-review main, exact reviewed head, CI/CodeQL, fresh independent review, zero blocking threads, expected-head merge, and post-merge SHA/tree/ordered-parent/path/signature/replay verification.

Only a fully verified canonical activation merge authorizes the bounded Repair-2 content read.

### 5. Inherited no-model scientific audit

Execute only old acceptance Sections A–D checks. Do not use old Section E manifest identity. Do not execute/call any model/provider.

### 6. GH1 result lineage — normative tree/commit scope

**`acceptance.md` Section I is mandatory and normative.** The result branch starts exactly at `GH1_ACTIVATION_MERGE_SHA`.

The only permitted result-root paths are:

```text
<GH1_RESULT_ROOT>r2-provenance-audit.json
<GH1_RESULT_ROOT>corpus-conformance-audit.json
<GH1_RESULT_ROOT>execution-binding-inventory.md
<GH1_RESULT_ROOT>preflight-verdict.md
<GH1_RESULT_ROOT>preflight-result-manifest.json
<GH1_RESULT_ROOT>execution-authorization-candidate.md   # conditional
<GH1_RESULT_ROOT>consumption-receipt.json              # terminal-only
```

Every result-lineage commit must satisfy all of these:

- exactly one parent;
- first result parent exactly `GH1_ACTIVATION_MERGE_SHA`;
- each later parent exactly the immediately preceding valid result target;
- no merge commit;
- no changed path outside `GH1_RESULT_ROOT`;
- no changed path outside the allowlist;
- activation files unchanged;
- frozen Repair-2 paths unchanged;
- no consumption receipt before terminal-receipt commit;
- no force-push/non-fast-forward/sideways retarget.

Intermediate commits may add/update only the six non-receipt allowlisted artifacts while building the package. The conditional successor may be removed only for a required blocked-package rebuild.

`TERMINAL_CONTENT_COMMIT` freezes every manifest-bound non-receipt artifact. No add/update/delete/rename/replacement of those bytes is permitted afterward.

`TERMINAL_RECEIPT_COMMIT` must be the direct child of terminal-content, have exactly one parent, and its only tree delta is creation of `consumption-receipt.json`. No later result-lineage commit is allowed before canonical result adoption.

Immediately before result merge, exact final-review main→reviewed-head diff must contain only the allowed GH1 result-root paths. Any unrelated path is a blocker.

### 7. Exact GH1 package binding

Construct only the GH1-specific package in `acceptance.md` J–K:

- active GH1 manifest identity;
- exact `inherited_contract` historical provenance object;
- unchanged frozen-input digest map from old Section E;
- exact three-artifact binding core;
- GH1 verdict binding;
- GH1 result manifest;
- conditional GH1 successor;
- non-self-referential terminal consumption receipt.

No old result manifest ID, old result root, old receipt identity, or old adoption schema may be substituted.

### 8. Exact-head result merge

Require every `acceptance.md` L predicate. Merge only the exact reviewed terminal-receipt head using `expected_head_sha`; post-verify result merge SHA/tree/ordered parents/path scope/signature and replay.

Canonical premerge-main→result-merge path delta must contain no path outside the reviewed GH1 result allowlist.

### 9. Create-only adoption record

Publish exactly one record under the merge-SHA-qualified GH1 adoption path using exact version:

```text
MESC-BT-PREFLIGHT-GH1-CANONICAL-ADOPTION-V1
```

Require the complete schema/failure-code/path/one-file-PR/post-merge predicates from `acceptance.md` M.

### 10. Stop

If the terminal state is ready, report only:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

Do not start tournament execution. Separate Founder execution authorization is mandatory.

## Fail-closed rules

At every stage:

- changed canonical `main` => re-read and reconcile; never assume;
- changed PR head => invalidate all stale exact-head evidence;
- incomplete PR enumeration => `BLOCKED`;
- conflicting reserved PR => `BLOCKED`;
- unexpected repository path => `BLOCKED`;
- result graph/parent/allowlist/immutability violation => `BLOCKED`;
- result identity/schema ambiguity => `BLOCKED`;
- failed signature/tree/parent/path verification => `BLOCKED`;
- frozen-content read before verified GH1 activation merge => protocol violation and `BLOCKED`;
- any model/provider interaction => protocol violation and immediate stop;
- any force-push/destructive history rewriting => protocol violation and immediate stop.

## Terminal repair report

Before any repair merge report at minimum:

```text
REPAIR_DECISION_ID
LIVE_MAIN_SHA
LIVE_MAIN_TREE
REPAIR_PR_NUMBER
REPAIR_HEAD_SHA
REPAIR_HEAD_TREE
CUMULATIVE_CHANGED_PATHS
CI_STATUS
CODEQL_STATUS
INDEPENDENT_REVIEW_STATUS
UNRESOLVED_BLOCKING_THREADS
OLD_DECISION_REVALIDATION
MERGE_AUTHORIZED = YES|NO
```

After a permitted repair merge additionally report:

```text
REPAIR_MERGE_SHA
REPAIR_MERGE_TREE
ORDERED_PARENTS
MERGE_SIGNATURE_VERIFICATION
FD-MESC-BT-EXEC-1-PREFLIGHT = SUPERSEDED_NONREUSABLE
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = AUTHORIZED_NOT_STARTED
```

Then stop unless the Founder separately authorizes continuation into GH1 activation qualification.