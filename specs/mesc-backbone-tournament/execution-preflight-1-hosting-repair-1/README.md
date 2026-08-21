# MESC Backbone Tournament — Execution Preflight 1 Hosting Repair 1

Status: **DRAFT HOSTING-COMPATIBILITY REPAIR — NO EXECUTION AUTHORITY**

Date: 2026-08-21

Decision ID: `FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1`

Replacement episode ID if this package is canonically adopted: `FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`

## Why this repair exists

PR #131 canonically adopted `FD-MESC-BT-EXEC-1-PREFLIGHT` at:

```text
AUTHORIZATION_MERGE_SHA = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6
AUTHORIZATION_MERGE_TREE = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70
ACTIVATION_RECEIPT_ID = 5d544ddb1406992c703c4ae9274daba6701089b3fdb994a080207af107256634
```

The episode did not start. No claim ref, result ref, activation receipt, frozen Repair-2 content read, model access, inference, generation, training, retrieval, ranking, winner selection, or tournament execution occurred.

The pre-claim protocol then failed closed because its storage-protection contract requires a server-enforced mechanism that, among other properties, permits initial `RESULT_REF` creation **only** at one exact authorization SHA while denying unauthorized mutation and configured bypass. GitHub.com native branch/tag rulesets can restrict *who* may create/update/delete a matching ref, but the native creation rule does not constrain the created ref to one exact target OID. Custom pre-receive hooks that can enforce old/new/ref predicates are a GitHub Enterprise Server capability, not a GitHub.com repository capability.

This repair does not reinterpret that failed proof as PASS. It replaces the unexecutable ref-level lifecycle with a GitHub.com-native canonical-merge lifecycle.

## Supersession rule

Until this repair is canonically merged and post-merge verified, PR #131 remains the active canonical contract and remains fail-closed before claim creation.

If this repair is canonically merged and verified:

- `FD-MESC-BT-EXEC-1-PREFLIGHT` becomes **SUPERSEDED_UNSTARTED**;
- its historical `CLAIM_REF` and `RESULT_REF` MUST NEVER be created;
- its historical activation receipt ID remains historical evidence only;
- the replacement episode is `FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`;
- the replacement receives a new receipt identity derived from the repair authorization merge and exact repair-package blob identities.

Supersession is valid only because the old episode has no claim, no result ref, no activation receipt, no result PR, and no frozen-content access. Any contrary live evidence blocks this repair.

## GitHub-native one-shot lifecycle

The replacement protocol uses GitHub records whose authority begins only at canonical `main` merge boundaries:

1. **Replay/preclaim:** enumerate the complete PR population and exact reserved branch namespaces; inspect only repository/PR metadata and non-Repair-2 governance evidence. No frozen Repair-2 content may be read.
2. **Claim + activation candidate PR:** create one deterministic same-repository PR whose delta is exactly two new governance files: `claim-record.json` and `activation-receipt.json`. Opening the PR creates durable hosting evidence but grants no content-read authority.
3. **Atomic canonical claim + activation:** immediately before merge, repeat replay checks; require the exact reviewed head, unchanged canonical `main`, all required CI/security/review gates, and merge with `expected_head_sha`. Only the verified merge to canonical `main` creates the one-shot claim and activates content-read authority.
4. **Bounded no-model audit:** after canonical activation verification only, reproduce the frozen Repair-2 content checks inherited from the original contract. No model/provider operation is permitted.
5. **Result PR:** publish the deterministic result package on one result branch/PR. The branch is staging only and is never authority by itself.
6. **Terminal exact-head adoption:** final result PR head is the terminal receipt commit, reviewed at exact head, CI/security gates pass, and merge uses `expected_head_sha`. Only the verified canonical result merge adopts the terminal state.
7. **Adoption verification:** publish one create-only canonical adoption record under a merge-SHA-qualified path, preserving the original non-self-referential adoption pattern.

Concurrency is fail-closed: the reserved PR namespaces are deterministic; any sibling/conflicting PR blocks; and `expected_head_sha` plus exact premerge `main` binding prevents a stale concurrent merge from silently claiming the episode.

## Inherited scientific/content contract

This repair does not weaken or redesign the Repair-2 scientific audit. It inherits the exact frozen input identities, post-activation content verification, canonical JSON rules, R2 provenance audit, corpus-conformance audit, result-package binding, no-model-access boundary, and successor-candidate semantics from the exact PR #131 authorization package at merge `d1c33ed61f69cd996453e1b50a6dfd8ce14509e6`, with the lifecycle substitutions defined in `acceptance.md` here.

The exact inherited PR #131 package blob identities are:

```text
README.md                 e801fb6d66c2f24e6a0294f7e7c80b35cac99a86
acceptance.md             7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
founder-authorization.md  9656fe06d791d86a960787c9451a0ee970e84c3a
plan.md                   b741fb1b7888a2ac861832390ce6586246818814
```

Those blobs are immutable inheritance anchors. This repair does not edit them.

## Absolute exclusions

This repair does **not** authorize:

- backbone tournament execution;
- model-weight access/download/load;
- gated-access requests or terms acceptance;
- prompt serialization to any model/provider;
- inference or generation;
- training or fine-tuning;
- retrieval against a model or external clinical source;
- candidate ranking or winner selection;
- PHI or real patient/clinician data;
- any mutation to frozen Repair-2 artifacts.

A later execution authorization remains separately required even if the replacement preflight reaches `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`.
