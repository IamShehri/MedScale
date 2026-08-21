# Founder Authorization — GH1 Result-Binding Repair 1

Status: **DRAFT FOUNDER AUTHORIZATION CANDIDATE — NO EXECUTION AUTHORITY**

Date: 2026-08-21

## Decision

Authorize a governance-only repair candidate for a deterministic result-binding defect discovered after valid canonical activation of `FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`.

```text
REPAIR_DECISION_ID = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1-RESULT-BINDING-REPAIR-1
REPLACEMENT_EPISODE_ID = FD-MESC-BT-EXEC-1-PREFLIGHT-GH2
```

This authorization candidate does not reinterpret any failed predicate as PASS and does not grant model or tournament authority.

## Exact defect anchors

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

`HISTORICAL_GH1_HOSTING_REPAIR_ACCEPTANCE_BLOB_SHA` names only the already-canonical hosting-repair `acceptance.md` that defined GH1. It is not the acceptance blob of this current result-binding-repair PR. The current repair acceptance blob is the Git blob of this repair's `acceptance.md` at the exact reviewed head and must be recorded externally from Git metadata at every exact-head gate.

The defect is that historical GH1 hosting-repair J.2 requires an exact inherited `frozen_input_digest_map` object, but the canonical old Section E never defines a literal JSON object/keyset for it. GH1's already-canonical result graph prevents an in-place clarification from being introduced without violating its path/diff rules.

## Founder state of GH1

The Founder records GH1 as issued and canonically activated, with bounded frozen Repair-2 scientific inspection performed only after valid activation, but with no result lineage published and no model/tournament operation performed.

If this repair becomes canonical and passes post-merge verification:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = SUPERSEDED_NONREUSABLE_POST_ACTIVATION_CONTRACT_DEFECT
GH1_RESULT_CREATION = PERMANENTLY_FORBIDDEN
GH1_RETRY = PERMANENTLY_FORBIDDEN
```

The existing GH1 claim/activation files remain immutable historical evidence. No synthetic terminal receipt may be created for GH1 after supersession.

## GH2 authorization

A verified canonical merge of this repair may authorize `FD-MESC-BT-EXEC-1-PREFLIGHT-GH2` as `AUTHORIZED_NOT_STARTED` only.

GH2 must create its own one-shot activation PR and receive full post-merge activation verification before any GH2 frozen-content read. Earlier GH1 reads cannot satisfy GH2 scientific-audit artifacts.

GH2 inherits only original old preflight Sections A-D. It does not inherit old Section E or historical GH1 result-binding identity.

The repair's normative `acceptance.md` defines a literal 15-member `frozen_input_bindings` object and complete GH2 result/receipt/adoption identities. No worker may reconstruct any unspecified field by analogy.

## Repair PR gates

The repair PR must remain Draft until all are true on one unchanged exact head:

1. canonical `main` equals exactly `PRE_REPAIR_MAIN_SHA = 4e259767a86c74a26967e0f19598a1f84a987df4` and its tree equals exactly `PRE_REPAIR_MAIN_TREE = c487c5a70abf865b364c96de1aa8c18da7bf6602`;
2. complete open + closed/merged PR replay under the exact selector/conflict rule in normative `acceptance.md` Section B confirms exactly one selected GH1 activation PR, zero selected GH1 result PRs, and `GH1_RESERVED_RESULT_NAMESPACE_CONFLICTS = 0`;
3. no GH1 result root, terminal receipt, result merge, or adoption record has appeared;
4. the authoritative hosting verification object for `GH1_ACTIVATION_MERGE_SHA` has `verification.verified=true`, `verification.reason=valid`, `verification.signature` non-null source text, and `verification.payload` non-null source text;
5. cumulative repair delta is exactly four new governance files under `execution-preflight-1-gh1-result-binding-repair-1/`;
6. no source/runtime/test/dependency/workflow/model/frozen Repair-2 path changes;
7. exact-head CI PASS;
8. exact-head CodeQL PASS;
9. fresh independent exact-head governance review = no blocking finding;
10. unresolved blocking review threads = 0.

After Draft gates, mark Ready only if explicitly authorized, then perform fresh post-Ready exact-head reconciliation. Merge only with exact `expected_head_sha`.

Immediately after any permitted repair merge, recognize repair authority only if **all** of the following hold in one fresh post-merge snapshot:

1. canonical `main` equals the returned repair merge SHA;
2. the merge tree and ordered parents are exact;
3. the path delta is exactly the reviewed four repair files and reviewed bytes match canonical bytes;
4. complete open + closed/merged PR replay under normative `acceptance.md` Section B returns exactly `GH1_SELECTED_ACTIVATION_PRS = 1`, `GH1_SELECTED_RESULT_PRS = 0`, and `GH1_RESERVED_RESULT_NAMESPACE_CONFLICTS = 0`;
5. `GH1_RESULT_ROOT_ON_MAIN = ABSENT`;
6. `GH1_TERMINAL_RECEIPT_ON_MAIN = ABSENT`;
7. `GH1_RESULT_MERGE = ABSENT`;
8. `GH1_ADOPTION_RECORD = ABSENT`;
9. the authoritative hosting verification object for the repair merge satisfies exactly:

```text
verification.verified = true
verification.reason = valid
verification.signature = NON_NULL_SOURCE_TEXT
verification.payload = NON_NULL_SOURCE_TEXT
```

Any failure above blocks repair authority and forbids GH2 activation.

Any new commit invalidates all stale exact-head evidence.

## Absolute prohibitions

This repair, GH2 authorization, and GH2 preflight do not authorize:

```text
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
GENERATION = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
MODEL_RETRIEVAL = NOT_AUTHORIZED
RANKING = NOT_AUTHORIZED
WINNER_SELECTION = NOT_AUTHORIZED
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
PHI_OR_REAL_PATIENT_DATA = NOT_AUTHORIZED
```

Even `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` would require a later separate Founder execution authorization.
