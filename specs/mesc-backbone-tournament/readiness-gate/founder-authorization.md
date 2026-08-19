# Founder Authorization Candidate — FD-MESC-BT-READINESS-1

Status: **RECORDED IN DRAFT PACKAGE — INACTIVE UNTIL CANONICALLY ADOPTED**

Date: 2026-08-19

## Decision identity

`FD-MESC-BT-READINESS-1`

## Proposed authorized action

`MESC BACKBONE TOURNAMENT — BOUNDED READ-ONLY READINESS AND PROTOCOL FREEZE`

## Preconditions

This authorization may activate only after this exact package passes:

1. exact-head CI;
2. exact-head CodeQL;
3. fresh independent exact-head review with no unresolved blocking findings;
4. zero unresolved or undispositioned review threads;
5. separate Founder Ready decision;
6. separate Founder Merge decision using an exact expected-head guard;
7. post-merge mechanical verification of canonical `main`, merge tree, and ordered parents.

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

If canonical state moves materially, an authoritative source cannot be resolved, a license/access fact remains unclear, R2 compatibility is uncertain, or equal-treatment cannot be frozen without seeing model outputs, stop and report `BLOCKED`.

No scientific or runtime action may be used to resolve a readiness ambiguity.
