# MESC Backbone Tournament — Execution Preflight 1 Hosting Repair 1

Status: **DRAFT HOSTING-COMPATIBILITY REPAIR — NO EXECUTION AUTHORITY**

Date: 2026-08-21

Repair decision ID: `FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1`

Replacement episode if canonically adopted: `FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`

## Canonical problem being repaired

PR #131 canonically adopted `FD-MESC-BT-EXEC-1-PREFLIGHT` at:

```text
OLD_AUTHORIZATION_MERGE_SHA = d1c33ed61f69cd996453e1b50a6dfd8ce14509e6
OLD_AUTHORIZATION_MERGE_TREE = 6104a8a95f0a688ff30b3ca8bd45a18b601eab70
OLD_ACTIVATION_RECEIPT_ID = 5d544ddb1406992c703c4ae9274daba6701089b3fdb994a080207af107256634
```

The bounded episode did not activate. No old claim ref, result ref, activation receipt publication, frozen Repair-2 content read/hash/parse, model access, inference, generation, training, retrieval, ranking, winner selection, or tournament execution was performed in the authorized workflow.

The old pre-claim protocol then failed closed because it required a server-enforced ref lifecycle that included an exact initial result-ref target OID. GitHub.com native rulesets can restrict matching ref creation/update/deletion by bypass eligibility, but their creation rule does not encode one exact required target OID. Programmable pre-receive hooks capable of old/new/ref predicate enforcement are a GitHub Enterprise Server capability, not the ordinary GitHub.com repository surface used here.

This repair never reclassifies that failed predicate as PASS.

## Canonical effect if this repair merges and verifies

Until this repair is merged and post-merge verified, PR #131 remains canonical and fail-closed before claim creation.

A verified canonical merge of this repair has exactly these governance effects:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT = SUPERSEDED_NONREUSABLE
OLD_CLAIM_REF_CREATION = PERMANENTLY_FORBIDDEN
OLD_RESULT_REF_CREATION = PERMANENTLY_FORBIDDEN
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = AUTHORIZED_NOT_STARTED
```

`SUPERSEDED_NONREUSABLE` is deliberately stronger and more robust than treating the old episode as reusable. GH1 is a distinct one-shot authorization and receives its own receipt identity from the canonical repair merge.

## Exact inheritance boundary

The old PR #131 package blobs are immutable anchors:

```text
README.md                 e801fb6d66c2f24e6a0294f7e7c80b35cac99a86
acceptance.md             7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
founder-authorization.md  9656fe06d791d86a960787c9451a0ee970e84c3a
plan.md                   b741fb1b7888a2ac861832390ce6586246818814
```

GH1 inherits only old `acceptance.md` Sections A–D:

- Repair-2 canonical ancestry/path/blob/digest and derived-prompt bindings;
- `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1`;
- R2 provenance audit predicates;
- corpus specification / manifest conformance audit predicates.

Old Section E result-package identity is **not inherited**. Old Sections F onward ref/CAS/result/adoption lifecycle is **not inherited**.

Active GH1 result identity is field-by-field defined in this repair's `acceptance.md` Sections J–M:

```text
decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT-GH1
authorization identity = canonical repair merge SHA/tree
activation identity = GH1_ACTIVATION_RECEIPT_ID + verified GH1 activation merge SHA
result root = GH1_RESULT_ROOT
manifest version = MESC-BT-PREFLIGHT-GH1-RESULT-MANIFEST-V1
successor id = FD-MESC-BT-EXEC-1-CANDIDATE-GH1-V1
consumption receipt version = MESC-BT-PREFLIGHT-GH1-CONSUMPTION-V1
adoption record version = MESC-BT-PREFLIGHT-GH1-CANONICAL-ADOPTION-V1
```

The old decision/authorization identity may appear in GH1 result data only inside the exact `inherited_contract` object defined by `acceptance.md` J.2. It is historical scientific-contract provenance, never the active GH1 result identity.

## GitHub-native one-shot lifecycle

GH1 uses durable PR records and verified canonical merges rather than mutable ref authority:

1. complete PR replay / reserved-namespace checks using metadata only;
2. deterministic same-repository activation PR adding exactly `claim-record.json` and `activation-receipt.json`;
3. no frozen Repair-2 content authority until exact reviewed activation head is merged with `expected_head_sha` and the canonical merge passes SHA/tree/ordered-parent/path/signature verification;
4. inherited no-model scientific/content audits from old Sections A–D only;
5. deterministic result lineage beginning exactly at the verified activation merge;
6. exact result-root allowlist and one-parent commit graph;
7. terminal-content commit freezes every manifest-bound non-receipt artifact;
8. direct-child terminal-receipt commit may only create `consumption-receipt.json`;
9. exact-head result PR review and `expected_head_sha` merge; canonical merge delta must contain no path outside the GH1 result allowlist;
10. one create-only canonical adoption record using the exact GH1 schema/version.

Branches are staging identities only. Branch creation, CI, review, or Ready state alone never creates canonical claim/result authority.

## Exact result path scope

The normative allowlist in `acceptance.md` Section I is exactly:

```text
<GH1_RESULT_ROOT>r2-provenance-audit.json
<GH1_RESULT_ROOT>corpus-conformance-audit.json
<GH1_RESULT_ROOT>execution-binding-inventory.md
<GH1_RESULT_ROOT>preflight-verdict.md
<GH1_RESULT_ROOT>preflight-result-manifest.json
<GH1_RESULT_ROOT>execution-authorization-candidate.md     # conditional
<GH1_RESULT_ROOT>consumption-receipt.json                # terminal-only
```

No GH1 result-lineage commit or final result merge may change a repository path outside this allowlist. The exact parent, create/update/delete, terminal immutability, and receipt-child rules are normative in `acceptance.md` Section I.

## Absolute exclusions

This repair and any GH1 preflight do **not** authorize:

- backbone tournament execution;
- model-weight access/download/load;
- gated-access requests or terms acceptance;
- prompt serialization to any model/provider;
- inference or generation;
- training or fine-tuning;
- retrieval involving model execution or external clinical data;
- candidate ranking or winner selection;
- PHI or real patient/clinician data;
- mutation/regeneration/substitution of frozen Repair-2 artifacts;
- force-push or destructive Git history rewriting.

A GH1 terminal state of `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` is only a candidate for a separate Founder execution authorization. It is not tournament authority.