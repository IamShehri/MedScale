# Founder Authorization — FD-MESC-BT-READINESS-REPAIR-2

Status: **FOUNDER APPROVED FOR CANONICAL ADOPTION / INACTIVE UNTIL MERGED AND VERIFIED**

Date: 2026-08-20

## Decision identity

`FD-MESC-BT-READINESS-REPAIR-2`

## Authorized action after canonical activation

`MESC BACKBONE TOURNAMENT — ONE BOUNDED READ-ONLY APERTUS AUP REMEDIATION AND READINESS/PROTOCOL-FREEZE EPISODE`

## Activation preconditions

This authorization activates only when all are true:

1. this exact package is reviewed against then-current canonical `main`;
2. PR #128 / terminal repair-1 result remains in canonical ancestry;
3. `FD-MESC-BT-READINESS-REPAIR-1 = CONSUMED / REUSABLE = NO` remains canonical;
4. exact-head CI passes;
5. exact-head CodeQL passes;
6. a fresh independent exact-head governance review reports no unresolved blocking findings;
7. all review threads are resolved or explicitly dispositioned with evidence;
8. the package is marked Ready only after those gates pass;
9. merge uses exact expected-head protection;
10. post-merge canonical main/tree/ordered parents/signature are mechanically verified.

## Authority if activated

One episode may:

- inspect canonical repository/governance history read-only;
- inspect authoritative public model metadata, model cards, licenses, policy pages, technical reports, and registry metadata;
- retrieve the exact public `swiss-ai/apertus-legal` Apertus 1.5 AUP binary through a binary-safe public transport such as the repository raw-content endpoint;
- compute byte length, SHA-256, and Git blob SHA-1 locally and require the computed Git blob identity to equal the authoritative repository blob before interpreting the PDF;
- render the verified PDF to page images and extract its text locally for legal/use-restriction evidence;
- inspect only the public legal document; no model repository gated file may be requested to accomplish this;
- record material use restrictions and R2/R3 compatibility conclusions with primary-evidence binding;
- refresh all four non-empty roster candidates from then-current authoritative public sources;
- assign only `BLOCKED`, `NOT_ADMITTED`, or `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`;
- keep challenger `EMPTY`;
- if and only if all non-empty candidates are conclusively dispositioned with none `BLOCKED` and at least two admitted, complete the six-axis synthetic/hand-authored R2-compatible corpus and protocol freeze;
- create deterministic corpus/protocol/report-schema digests and a non-authoritative future execution plan;
- create a separate inactive `FD-MESC-BT-EXEC-1` candidate only if the terminal readiness result is `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`.

## Apertus evidence rule

For `swiss-ai/Apertus-v1.5-8B`:

- the exact authoritative AUP binary must be bound to the official Git blob identity before its text is used;
- any byte mismatch, unreadable/ambiguous material term, contradictory source, or inability to bind exact text to the official artifact => `BLOCKED`;
- authoritative exact terms conclusively incompatible with MESC policy => `NOT_ADMITTED`;
- authoritative exact terms conclusively compatible, with all other admission evidence proven => normal admission analysis may yield `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`.

## Mandatory candidate refresh

No prior model revision, tokenizer/processor revision, access condition, or license observation may be silently carried forward. Every non-empty roster slot must be refreshed from then-current authoritative public sources during this episode.

## Explicit exclusions

This authorization does **not** permit:

- downloading, opening, loading, inspecting, or accessing model weights;
- requesting or accepting gated model access;
- accepting gated-access terms or model-access agreements for any purpose;
- inference or generation;
- benchmark/tournament execution;
- B0 rerun or B1/B2/B3 execution;
- P01-06+;
- Pilot-01 test-content access or scientific-content inspection;
- real patient data, PHI, product telemetry, or other R2-prohibited data;
- external benchmark ingestion unless separately proven R2-compatible within this episode;
- training, continued pretraining, SFT, fine-tuning, QLoRA, adapters, preference optimization, RL, verifier training, or distillation;
- retrieval activation;
- fallback substitution;
- quantization changes or derivative quantized entries;
- challenger population;
- excluded model-family admission;
- MCRL/AMGE/audio/biosignal/donor-runtime implementation;
- clinical, safety, efficacy, publication, release, or production claims.

## Consumption rule

If activated, this decision is consumed by exactly one bounded episode. It cannot be reused for later refreshes or execution.

Terminal outcomes are only:

- `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`, or
- `BLOCKED`.

Any non-empty `BLOCKED` candidate forces overall `BLOCKED`. Fewer than two admitted candidates also forces `BLOCKED`.

## Execution boundary

Even a successful episode grants no execution authority.

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
