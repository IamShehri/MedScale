# Founder Authorization — FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1

Status: **DRAFT FOUNDER AUTHORIZATION CANDIDATE — NO EXECUTION AUTHORITY UNTIL CANONICAL MERGE + VERIFICATION**

Date: 2026-08-21

## Decision identity

```text
REPAIR_DECISION_ID = FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1
REPLACEMENT_EPISODE_ID = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1
```

## Founder decision

Authorize a hosting-compatibility repair for canonical `FD-MESC-BT-EXEC-1-PREFLIGHT`, which failed closed before activation because its exact-target protected-ref lifecycle cannot be mechanically satisfied on the current GitHub.com hosting surface.

This repair does **not** reinterpret the old protection failure as PASS. It does **not** execute the old episode. It creates a distinct replacement authorization whose authority is carried by deterministic PR records and verified canonical `main` merges.

## Exact old authorization anchors

```text
OLD_DECISION_ID = FD-MESC-BT-EXEC-1-PREFLIGHT
OLD_AUTHORIZATION_MERGE_SHA = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6
OLD_AUTHORIZATION_MERGE_TREE = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70
OLD_ACTIVATION_RECEIPT_ID = 5d544ddb1406992c703c4ae9274daba6701089b3fdb994a080207af107256634
OLD_ACCEPTANCE_BLOB_SHA = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
```

The repair may be merged only while current live/canonical metadata remains consistent with the last verified state: old claim/result refs absent, no selected old result PR, no canonical old activation/consumption receipt, no canonical artifact asserting old frozen-content access, and no model/tournament operation performed by this workflow.

Any contrary live evidence => `BLOCKED`.

## Repair merge prerequisites

Before this repair leaves Draft, and again immediately before merge, require:

1. canonical `main` still descends from `OLD_AUTHORIZATION_MERGE_SHA` and that commit tree remains `OLD_AUTHORIZATION_MERGE_TREE`;
2. the four PR #131 package blobs still match the exact anchors recorded by this repair;
3. cumulative repair PR delta is exactly the four new files under `specs/mesc-backbone-tournament/execution-preflight-1-hosting-repair-1/`;
4. no original PR #131 file, frozen Repair-2 artifact, source/runtime/test/dependency/workflow/model path is changed;
5. exact-head CI = PASS;
6. exact-head CodeQL = PASS;
7. fresh independent exact-head governance review = no blocking finding;
8. unresolved blocking review threads = 0;
9. every prior review finding is either repaired on the exact current head or explicitly proven stale/outdated;
10. PR head and canonical `main` equal the exact final-review values;
11. merge uses `expected_head_sha = <fully reviewed exact repair head>`; and
12. post-merge canonical SHA/tree/ordered-parent/path/signature verification passes.

Any changed head invalidates previous exact-head CI/review evidence.

## Canonical effect of a verified repair merge

Only after all post-merge verification passes:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT = SUPERSEDED_NONREUSABLE
OLD_CLAIM_REF_CREATION = PERMANENTLY_FORBIDDEN
OLD_RESULT_REF_CREATION = PERMANENTLY_FORBIDDEN
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = AUTHORIZED_NOT_STARTED
```

The old authorization is retired and cannot be reused even if historical branch/ref objects are later deleted or recreated. GH1 is a distinct one-shot decision with a receipt identity derived from the canonical repair merge.

A verified repair merge does **not** itself create the GH1 claim, activate frozen-content access, or start a preflight audit.

## Exact inheritance and active GH1 field mapping

GH1 inherits only the scientific/content predicates from old `acceptance.md` Sections A–D at blob `OLD_ACCEPTANCE_BLOB_SHA`:

- Repair-2 ancestry/path/blob/digest and prompt binding checks;
- `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1`;
- R2 provenance audit predicates;
- corpus specification / manifest conformance predicates.

Old Section E result-package identity and old Sections F onward lifecycle are **superseded**, not inherited.

The active GH1 result binding is exactly:

```text
active decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1
active authorization SHA/tree = canonical hosting-repair merge SHA/tree
active receipt identity = GH1_ACTIVATION_RECEIPT_ID
active activation merge = verified GH1 activation merge SHA
active result root = GH1_RESULT_ROOT
active manifest version = MESC-BT-PREFLIGHT-GH1-RESULT-MANIFEST-V1
active successor id = FD-MESC-BT-EXEC-1-CANDIDATE-GH1-V1
active consumption receipt version = MESC-BT-PREFLIGHT-GH1-CONSUMPTION-V1
active adoption record version = MESC-BT-PREFLIGHT-GH1-CANONICAL-ADOPTION-V1
```

The old decision/authorization values may appear in a GH1 result only inside `inherited_contract` with exactly the four historical provenance fields defined in `acceptance.md` J.2. They may not be used as active manifest identity, result-root identity, receipt identity, successor identity, or adoption identity.

`acceptance.md` Sections J–M are the single normative source for complete GH1 manifest, terminal receipt, canonical result adoption, and adoption-record schemas. No worker may fill unspecified lifecycle/result fields by analogy to PR #131.

## Authorized GH1 lifecycle after this repair becomes canonical

A later Founder instruction may continue into GH1 activation qualification. The authorized bounded lifecycle is:

### Phase 1 — metadata-only replay and activation candidate

Before verified activation merge:

- only Git/repository/PR metadata and non-Repair-2 governance evidence may be inspected;
- enumerate complete PR population and reserved GH1 namespaces;
- create at most the exact structurally selected activation PR;
- activation PR changes exactly two new paths: `claim-record.json` and `activation-receipt.json`;
- opening/approving/readying the PR grants no frozen-content authority.

### Phase 2 — canonical activation

Frozen Repair-2 content authority begins only after the exact reviewed activation head is merged to unchanged canonical `main` using `expected_head_sha` and the merge passes all SHA/tree/ordered-parent/path/signature/replay verification in `acceptance.md` G.

Failed/stale merge or failed post-merge verification => `BLOCKED`; no content read.

### Phase 3 — inherited no-model scientific audit

After canonical activation only, execute old Sections A–D scientific/content checks. No model/provider operation is allowed.

### Phase 4 — exact GH1 result lineage

The result branch is staging only and starts exactly at the verified GH1 activation merge.

The **normative result tree/commit contract is `acceptance.md` Section I**. It requires:

```text
allowed result paths only:
  r2-provenance-audit.json
  corpus-conformance-audit.json
  execution-binding-inventory.md
  preflight-verdict.md
  preflight-result-manifest.json
  execution-authorization-candidate.md   # conditional
  consumption-receipt.json              # terminal-only
```

Every result-lineage commit has exactly one parent and no merge commit; every delta is confined to the allowlist under `GH1_RESULT_ROOT`; activation files and frozen Repair-2 paths are immutable. `TERMINAL_CONTENT_COMMIT` freezes every manifest-bound non-receipt result. Its direct child `TERMINAL_RECEIPT_COMMIT` may add only `consumption-receipt.json`. No later result-lineage commit is permitted before canonical result adoption.

Any out-of-root path, non-allowlisted path, delete/replace after terminal freeze, parent mismatch, force/non-FF history rewrite, receipt replacement, or extra post-receipt commit => `BLOCKED`.

### Phase 5 — canonical result and adoption verification

The exact terminal-receipt head requires fresh exact-head CI/CodeQL/review and merges with `expected_head_sha`. The final premerge-main→result-merge changed-path set must be exactly the reviewed GH1 result allowlist subset and contain no unrelated path.

After verified result merge, publish one create-only adoption record using exactly `MESC-BT-PREFLIGHT-GH1-CANONICAL-ADOPTION-V1` at the merge-SHA-qualified path and satisfy all `acceptance.md` M predicates.

Only then may GH1 be reported as canonically terminal.

## No tournament authority

Even if GH1 reaches:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

that means only that a separate Founder execution-authorization decision may be considered. It does not authorize tournament execution.

## Absolute prohibitions

Throughout this repair and any GH1 preflight:

- no model-weight access/download/load;
- no gated model access request or terms acceptance;
- no prompt serialization to a model/provider API;
- no inference or generation;
- no training/fine-tuning;
- no retrieval involving model execution or external clinical data;
- no candidate ranking or winner selection;
- no backbone tournament execution;
- no PHI or real patient/clinician data;
- no mutation/regeneration/substitution of frozen Repair-2 artifacts;
- no force-push or destructive history rewriting.

Any prohibited operation is a protocol violation and requires immediate fail-closed stop.