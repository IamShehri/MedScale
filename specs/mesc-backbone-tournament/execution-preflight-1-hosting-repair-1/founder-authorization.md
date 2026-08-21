# Founder Authorization — FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1

Status: **DRAFT FOUNDER AUTHORIZATION CANDIDATE — NO EXECUTION AUTHORITY UNTIL CANONICAL MERGE + VERIFICATION**

Date: 2026-08-21

## Decision identity

Repair decision: `FD-MESC-BT-EXEC-1-PREFLIGHT-HOSTING-REPAIR-1`

Replacement bounded episode after canonical activation: `FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`

## Founder decision

Authorize a hosting-compatibility repair for the already-canonical but unstarted `FD-MESC-BT-EXEC-1-PREFLIGHT` contract. The repair exists only because the original storage-boundary ref-protection predicates cannot be mechanically satisfied on the current GitHub.com hosting surface without either weakening the exact-target requirement or introducing a provider capability that is not present.

No original failed predicate is reclassified as PASS. The old authorization remains fail-closed and unstarted until this repair is canonically adopted.

## Preconditions for canonical activation

This repair activates only if all are true on one unchanged exact head:

1. canonical `main` contains PR #131 merge `d1c33ed61f69cd996453e1b50a6dfd8ce14509e6` with tree `6104a8a95f0a688ff30b3ca8bd45a18b601eab70` in ancestry;
2. PR #131's original four package blobs equal the immutable identities recorded in this repair;
3. no historical `CLAIM_REF` descendant exists for the old decision;
4. no historical `RESULT_REF` descendant exists for the old decision;
5. no structurally selected old-decision result PR or conflicting reserved-namespace PR exists;
6. no old-decision activation or consumption receipt is reachable from canonical `main` or selected hosting evidence;
7. no frozen Repair-2 content was read/hashed/parsed/decompressed under the old episode;
8. `FD-MESC-BT-READINESS-REPAIR-2 = CONSUMED / REUSABLE = NO` remains canonical;
9. `BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE` remains canonical;
10. exact-head CI and CodeQL pass;
11. fresh independent exact-head governance review reports no blocking finding;
12. unresolved blocking review threads = 0;
13. the PR is Ready only after Draft gates pass;
14. any post-Ready required review passes on the unchanged exact head;
15. merge uses exact expected-head protection; and
16. post-merge canonical SHA/tree/ordered-parent/signature verification passes.

Any contrary evidence means this repair MUST NOT merge.

## Supersession after canonical merge

A verified canonical merge of this repair has exactly these governance effects:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT = SUPERSEDED_UNSTARTED
OLD_CLAIM_REF_CREATION = PERMANENTLY_FORBIDDEN
OLD_RESULT_REF_CREATION = PERMANENTLY_FORBIDDEN
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = AUTHORIZED_NOT_STARTED
```

The old authorization is not marked consumed because no claim was created. It is retired by explicit canonical supersession. Any later appearance of an old claim/result ref or old episode result PR is conflicting governance evidence and blocks the GH1 episode.

## Authorized action after repair activation

Exactly one bounded **no-model-access execution preflight / corpus audit episode** under `FD-MESC-BT-EXEC-1-PREFLIGHT-GH1`.

Authority proceeds in two canonical GitHub merge phases:

### Phase 1 — claim + activation merge

Before the claim/activation PR is merged, authority remains metadata-only. The worker may inspect only Git/repository/PR metadata and non-Repair-2 governance evidence needed to prove replay state and construct the deterministic claim/activation candidate.

The deterministic claim/activation PR:

- is same-repository;
- targets canonical `main`;
- has one deterministic reserved head name derived from the repair authorization merge SHA and replacement activation receipt ID;
- changes exactly two new paths under the GH1 activation root: `claim-record.json` and `activation-receipt.json`;
- changes no pre-existing path;
- contains no Repair-2 content or derived Repair-2 content;
- grants no frozen-content read authority merely by branch creation, PR opening, CI, approval, or Ready state.

Only the exact-head merge into unchanged canonical `main`, followed by successful post-merge SHA/tree/ordered-parent/signature/path verification, simultaneously establishes the one-shot claim and activates frozen-content read authority.

A failed/stale merge, conflicting reserved PR, changed `main`, changed head, extra path, replacement of an existing path, failed post-merge verification, or inability to prove complete PR/ref replay state => `BLOCKED` and no frozen-content read.

### Phase 2 — bounded audit + terminal result merge

After Phase 1 activation is canonically verified, the worker may perform only the inherited no-model Repair-2 content audits and package construction.

The deterministic result PR is staging only. It grants no canonical terminal authority until its exact reviewed terminal-receipt head is merged into canonical `main` with expected-head protection and the merge is post-verified.

No result-branch force-push or history rewriting is permitted. If its head moves after a review, every exact-head review/gate is stale and must be repeated. Any unexpected branch or PR namespace conflict is fail-closed.

## Scientific and serialization inheritance

The replacement episode inherits, without relaxation, the exact frozen Repair-2 input bindings, content verification requirements, canonical JSON serialization rule, R2 provenance audit, corpus-conformance audit, result-package binding, successor-candidate rules, no-PHI boundary, and no-model boundary from PR #131's exact `acceptance.md` blob:

```text
7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf
```

Only the original ref-protection/CAS lifecycle and any fields that necessarily self-bind to that lifecycle are replaced by the GitHub-native canonical-merge lifecycle in this repair's `acceptance.md`.

## Absolute prohibitions

This authorization does not permit, at any time during this repair or the GH1 preflight:

- model-weight access, download, or load;
- gated model access request or terms acceptance;
- prompts sent or serialized to models/provider APIs;
- inference or generation;
- training/fine-tuning;
- retrieval involving model execution or external clinical data;
- ranking/selecting a backbone winner;
- backbone tournament execution;
- PHI/real patient/clinician data;
- alteration or regeneration of frozen Repair-2 artifacts;
- force-push or destructive Git history rewriting.

If GH1 later reaches `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, that state is only a candidate for a separate Founder execution authorization. It is not tournament authority.
