# Founder Authorization Candidate — FD-MESC-BT-READINESS-1

Status: **RECORDED IN DRAFT PACKAGE — INACTIVE UNTIL CANONICALLY ADOPTED**

Date: 2026-08-19

## Decision identity

`FD-MESC-BT-READINESS-1`

## Proposed authorized action

`MESC BACKBONE TOURNAMENT — BOUNDED READ-ONLY READINESS AND PROTOCOL FREEZE`

## Preconditions

This authorization may activate only after all of the following are mechanically satisfied:

1. the separate Pilot-01 closeout disposition is proven adopted by merged PR #125 at merge commit `c0a9acfc678149736bd9054f7fadae1c31b488a1`;
2. that closeout merge verifies to tree `71f36f2e49932f82a6ee733833b93306ab5f1f41`, ordered parents `f69a1b2f1c050aad6fe77eb6273016c764c109f5` then `1e52fa581af8f7894e2cfe3dbd1b07683ae0de72`, with GitHub verification `verified=true / reason=valid`;
3. then-current canonical `main` is equal to or a descendant of `c0a9acfc678149736bd9054f7fadae1c31b488a1`;
4. this exact readiness-package head passes exact-head CI;
5. this exact readiness-package head passes exact-head CodeQL;
6. fresh independent exact-head review reports no unresolved blocking findings;
7. there are zero unresolved or undispositioned review threads;
8. the founder exercises a separate Founder Ready decision;
9. the founder exercises a separate Founder Merge decision using an exact expected-head guard;
10. post-merge mechanical verification proves canonical `main`, merge tree, and ordered parents for this readiness package;
11. after package merge, canonical `main` is reverified to contain the Pilot-01 closeout merge in its ancestry.

Historical status text, strategy intent, or the mere presence of closeout files is not sufficient evidence for items 1–3 and 11.

## Authority if activated

One bounded readiness episode may:

- inspect canonical repository/governance history read-only;
- inspect authoritative public documentation, public metadata, model cards, licenses, technical reports, and official registry metadata for candidate models;
- resolve exact candidate repository IDs and immutable revisions without downloading/opening model weights;
- resolve tokenizer/processor identities and revisions without runtime model execution;
- classify license/access/hardware/runtime/admissibility constraints;
- fill or leave empty the single challenger slot before any model execution;
- design and freeze a synthetic/hand-authored R2-compatible evaluation corpus contract;
- create hand-authored/synthetic fixture specifications, but not run models against them;
- freeze prompts, decoding, parsing, metrics, selection thresholds, compute accounting, and report schemas;
- produce documentation artifacts: candidate manifest, protocol-freeze report, readiness verdict, execution plan, and a separate inactive tournament-execution authorization candidate.

## Explicit exclusions

This authorization does **not** permit:

- model-weight download, opening, loading, or access;
- gated-weight access acceptance/request;
- inference/generation;
- benchmark/tournament execution;
- B0 rerun/replication;
- B1/B2/B3;
- P01-06+;
- Pilot-01 test access or scientific-content inspection;
- external non-R2-compatible benchmark data;
- patient/product/telemetry/PHI data;
- training/fine-tuning/continued pretraining/SFT/QLoRA/adapters/preference optimization/RL;
- retrieval;
- fallback substitution;
- quantization changes;
- DeepSeek or other excluded model-family admission;
- MCRL/AMGE/audio/biosignal/donor-runtime implementation;
- publication, release, clinical, safety, efficacy, or production claims.

## Consumption rule

If activated, `FD-MESC-BT-READINESS-1` may be consumed by **one** bounded readiness/protocol-freeze episode only.

The episode ends when it produces either:

- `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`, or
- `BLOCKED` with explicit unresolved evidence/constraints.

It cannot be reused to refresh candidate versions, add candidates after outputs are observed, or execute the tournament.

## Fail-closed rule

If the Pilot-01 closeout adoption proof or ancestry check fails, canonical state moves materially, an authoritative source cannot be resolved, a license/access fact remains unclear, R2 compatibility is uncertain, or equal-treatment cannot be frozen without seeing model outputs, stop and report `BLOCKED`.

No scientific or runtime action may be used to resolve a readiness ambiguity.
