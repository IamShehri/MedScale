# MESC Backbone Tournament — GH1 Result-Binding Repair 1

Status: **DRAFT GOVERNANCE REPAIR — NO EXECUTION AUTHORITY**

Date: 2026-08-21

Repair decision ID: `FD-MESC-BT-EXEC-1-PREFLIGHT-GH1-RESULT-BINDING-REPAIR-1`

Replacement episode if canonically adopted: `FD-MESC-BT-EXEC-1-PREFLIGHT-GH2`

## Why this repair exists

Canonical GH1 was validly activated at merge `4e259767a86c74a26967e0f19598a1f84a987df4` after PR #134. Bounded frozen Repair-2 content inspection then began under that activation. During deterministic GH1 result-package construction, the worker reached the **historical GH1 hosting-repair** `acceptance.md` Section J.2 and found that `frozen_input_digest_map` is required to preserve an "exact unchanged old Section E key/value object", while the canonical inherited old Section E never defines any literal JSON keyset/object for that map.

This is not a digest mismatch and not a scientific-audit failure. It is a result-binding determinism defect: multiple JSON objects could encode the same frozen constants, and the contract provides no canonical way to choose one.

The historical GH1 hosting-repair acceptance blob is:

```text
HISTORICAL_GH1_HOSTING_REPAIR_ACCEPTANCE_BLOB_SHA = 2d0c9765d22b435cd8e57d13e7d5972e9a095b40
```

The inherited old preflight acceptance blob is:

```text
INHERITED_ACCEPTANCE_BLOB_SHA = 7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
```

Neither historical blob contains a literal canonical `frozen_input_digest_map` object.

The acceptance blob of **this current result-binding-repair PR** is a different identity: it is the Git blob SHA of `execution-preflight-1-gh1-result-binding-repair-1/acceptance.md` at the exact reviewed PR head. It is observed and recorded externally at each exact-head gate and is intentionally not embedded in its own file bytes.

## Why GH1 cannot be repaired in place

Historical GH1 hosting-repair Section I requires the first GH1 result commit to have parent exactly `GH1_ACTIVATION_MERGE_SHA` and permits changes only to the GH1 result-root allowlist. Section L requires the final premerge-main to reviewed-result-head diff to contain only those allowlisted result paths.

Therefore:

- merging a clarification to canonical `main` before a GH1 result would make that clarification appear as an out-of-result-root difference when comparing the advanced `main` to a result head rooted at the activation merge; and
- placing the clarification inside the GH1 result lineage would itself violate Section I.

GH1 cannot be made deterministic without violating its already-canonical graph/path contract. It must fail closed and become nonreusable.

## Current GH1 state recorded by this repair candidate

```text
PRE_REPAIR_MAIN_SHA = 4e259767a86c74a26967e0f19598a1f84a987df4
PRE_REPAIR_MAIN_TREE = c487c5a70abf865b364c96de1aa8c18da7bf6602
GH1_REPAIR_AUTHORIZATION_MERGE_SHA = 9d66538b96794429e29b7baa0c58dfa60a408cb7
GH1_REPAIR_AUTHORIZATION_MERGE_TREE = b80aceddcb7082fa8af8c40c34e4228c6e8f6a35
GH1_ACTIVATION_RECEIPT_ID = 6c3bb9a5e8b55c4bd3b9be81e59629dd9e257d4a1eb3a6d0e99dcaf00be9947c
GH1_ACTIVATION_HEAD_SHA = 8d525730705351afffc8ca67940e2cc50df9632a
GH1_ACTIVATION_MERGE_SHA = 4e259767a86c74a26967e0f19598a1f84a987df4
GH1_ACTIVATION_MERGE_TREE = c487c5a70abf865b364c96de1aa8c18da7bf6602
GH1_SELECTED_ACTIVATION_PRS = 1
GH1_SELECTED_RESULT_PRS = 0
GH1_RESERVED_RESULT_NAMESPACE_CONFLICTS = 0
GH1_RESULT_PR = ABSENT
GH1_RESULT_ROOT_ON_MAIN = ABSENT
GH1_TERMINAL_RECEIPT = ABSENT
GH1_CANONICAL_TERMINAL_STATE = NONE
GH1_FROZEN_REPAIR2_CONTENT_ACCESS = PERFORMED_AFTER_VALID_ACTIVATION
GH1_MODEL_ACCESS = NOT_PERFORMED
GH1_TOURNAMENT_EXECUTION = NOT_PERFORMED
```

Before this repair may become Ready and again immediately before merge, canonical `main` must still equal the exact pre-repair SHA/tree above, complete PR replay must reproduce the selected/conflict counts above using the exact selector in normative `acceptance.md` Section B, and the authoritative hosting verification object for `GH1_ACTIVATION_MERGE_SHA` must satisfy exactly:

```text
verification.verified = true
verification.reason = valid
verification.signature = NON_NULL_SOURCE_TEXT
verification.payload = NON_NULL_SOURCE_TEXT
```

Any failure is `BLOCKED`.

No GH1 result branch, result PR, terminal-content commit, terminal receipt, result merge, or adoption record may be fabricated from the underdefined binding.

## Canonical effect if this repair merges and is mechanically verified

```text
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = SUPERSEDED_NONREUSABLE_POST_ACTIVATION_CONTRACT_DEFECT
GH1_RESULT_CREATION = PERMANENTLY_FORBIDDEN
GH1_RETRY = PERMANENTLY_FORBIDDEN
FD-MESC-BT-EXEC-1-PREFLIGHT-GH2 = AUTHORIZED_NOT_STARTED
```

The existing GH1 activation files remain immutable historical evidence. They are not deleted, rewritten, or reclassified as a successful result.

## GH2 design

GH2 retains the same no-model scientific scope and GitHub-native one-shot lifecycle, but its result binding is defined independently and completely. It inherits only original preflight `acceptance.md` Sections A-D for frozen Repair-2 scientific/content predicates and canonical JSON serialization.

GH2 does **not** inherit old Section E, historical GH1 hosting-repair Section J, or any implicit "digest map" representation.

Instead GH2 defines one literal versioned `frozen_input_bindings` object containing exactly the 15 frozen Repair-2 binding fields and values. The exact object and all GH2 result/receipt identities are normative in this repair's `acceptance.md`.

## Absolute exclusions

This repair and any GH2 preflight do not authorize:

- model-weight access/download/load;
- gated-access request or terms acceptance;
- prompt serialization to a model/provider;
- inference or generation;
- training or fine-tuning;
- model-executing retrieval;
- candidate ranking or winner selection;
- backbone tournament execution;
- PHI or real patient/clinician data;
- mutation/regeneration/substitution of frozen Repair-2 artifacts;
- force-push or destructive history rewriting.

A future GH2 terminal state `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` remains only a candidate for a separate Founder execution authorization.