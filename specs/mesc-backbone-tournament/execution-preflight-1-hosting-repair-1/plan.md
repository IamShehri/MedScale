# Plan — FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1

Status: **DRAFT PLAN — NO EXECUTION AUTHORITY**

Date: 2026-08-21

## Objective

Replace the unexecutable GitHub.com ref-protection lifecycle in canonical `FD-MESC-BT-EXEC-1-PREFLIGHT` with a GitHub-native canonical-merge lifecycle while preserving every scientific/content/no-model safety boundary.

This plan is docs/governance only. It must not read frozen Repair-2 content, create the old claim/result refs, access models, or execute the tournament.

## Live starting point

```text
CANONICAL_MAIN = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6
CANONICAL_TREE = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70
PR_131 = MERGED_CANONICAL
OLD_EPISODE = NOT_STARTED
OLD_CLAIM_REF = NOT_CREATED
OLD_RESULT_REF = NOT_CREATED
OLD_FROZEN_CONTENT_ACCESS = NOT_PERFORMED
```

The repair branch must be created from the exact canonical main above unless live truth moves first, in which case rebase-by-recreation or destructive history rewriting is forbidden; instead reconcile from the new canonical base using ordinary history-preserving commits.

## Repair package

Create exactly four new files under:

```text
specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/
```

Files:

1. `README.md`
2. `acceptance.md`
3. `founder-authorization.md`
4. `plan.md`

Do not modify the four original PR #131 authorization files. Do not modify frozen Repair-2 paths, source code, runtime code, tests, dependencies, workflows, model configuration, or model artifacts.

## Draft review sequence

1. Verify exact canonical `main` and tree immediately before branch creation.
2. Create one repair commit containing only the four new governance files.
3. Open a **Draft** PR to `main`.
4. Verify changed paths are exactly the four repair files.
5. Verify PR base/head SHAs and mergeability.
6. Wait for exact-head CI and CodeQL results; no Ready transition on pending/failure.
7. Obtain a fresh independent exact-head governance review in Draft.
8. Resolve every blocking review thread by history-preserving repair commits only.
9. Any repair commit invalidates prior exact-head review evidence.
10. When Draft gates are green, mark Ready.
11. Obtain any required post-Ready exact-head review on the unchanged head.
12. Reverify CI, CodeQL, unresolved threads, `main`, and exact head.
13. Merge only with `expected_head_sha` equal to the exact fully reviewed head.
14. Verify canonical merge SHA/tree/ordered parents/signature and exact four-path tree delta.

No merge occurs merely because this plan exists.

## Mandatory external hosting finding preserved in the PR

The PR description must state the exact reason for the repair:

- GitHub.com repository rulesets support restricting matching ref creation/update/deletion based on bypass eligibility;
- the native `creation` rule does not express an exact required initial target OID;
- GitHub pre-receive hooks capable of old/new/ref predicate enforcement are documented for GitHub Enterprise Server, not ordinary GitHub.com repositories;
- therefore the original exact-target storage-boundary predicate was not proven and was correctly blocked before claim creation.

The repair must not claim that the original protection gate passed.

## Replacement lifecycle after repair merge

If and only if this repair is canonically merged and verified:

### 1. Derive GH1 receipt identity

Use the repair merge SHA/tree and exact four repair-package blob identities under the canonical serialization rule in `acceptance.md`.

### 2. Reprove superseded episode is unstarted

Re-enumerate complete PR population and exact old reserved identities using metadata only. Any old claim/result/activation evidence blocks GH1.

### 3. Construct GH1 activation candidate

Create deterministic activation branch and same-repository PR with exactly two new canonical JSON paths: claim record + activation receipt. No Repair-2 content read.

### 4. Exact-head activation qualification

Require exact-head CI/CodeQL/review, unchanged `main`, replay recheck, zero namespace conflict, and expected-head merge.

### 5. Post-merge activation verification

Verify returned merge became canonical `main`, verify tree/ordered parents/signature and exact reviewed activation files. Only then may frozen Repair-2 content be read for the bounded audit.

### 6. Execute inherited no-model audits

Perform only the exact inherited provenance/conformance/input-digest/package checks. Do not execute or call any model/provider.

### 7. Build deterministic GH1 result PR

Produce inherited result package under the GH1 result root. Finalize terminal-content commit, then one direct child terminal-receipt commit.

### 8. Exact-head result qualification and merge

Require exact-head CI/CodeQL/fresh independent review/zero blocking threads/unchanged main. Merge with expected-head SHA and mechanically post-verify.

### 9. Create canonical adoption verification record

One create-only path, one exact-head PR, expected-head merge, post-merge verification.

### 10. Stop

If terminal state is ready, report only `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`. Do not start tournament execution. A separate Founder authorization is mandatory.

## Fail-closed handling

At every stage:

- changed `main` => re-read and reconcile; never assume;
- changed PR head => invalidate stale review evidence;
- incomplete PR enumeration => `BLOCKED`;
- conflicting reserved PR => `BLOCKED`;
- unexpected path => `BLOCKED`;
- failed signature/tree/parent verification => `BLOCKED`;
- any old episode claim/result evidence => `BLOCKED`;
- any frozen-content read before verified GH1 activation merge => `BLOCKED`;
- any model/provider interaction => protocol violation and immediate stop;
- any force-push/destructive history rewriting => protocol violation and immediate stop.

## Terminal report for this repair PR

Before any repair merge, report at minimum:

```text
REPAIR_DECISION_ID
LIVE_MAIN_SHA
LIVE_MAIN_TREE
REPAIR_PR_NUMBER
REPAIR_HEAD_SHA
REPAIR_HEAD_TREE
CHANGED_PATHS
CI_STATUS
CODEQL_STATUS
INDEPENDENT_REVIEW_STATUS
UNRESOLVED_BLOCKING_THREADS
OLD_EPISODE_REVALIDATION
MERGE_AUTHORIZED = YES|NO
```

After a permitted merge, additionally report:

```text
REPAIR_MERGE_SHA
REPAIR_MERGE_TREE
ORDERED_PARENTS
MERGE_SIGNATURE_VERIFICATION
FD-MESC-BT-EXEC-1-PREFLIGHT = SUPERSEDED_UNSTARTED
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = AUTHORIZED_NOT_STARTED
```

Stop after repair merge verification unless the Founder separately instructs continuation into GH1 activation qualification.
