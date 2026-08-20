# Founder Authorization — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **FOUNDER APPROVED FOR CANONICAL ADOPTION / INACTIVE UNTIL MERGED AND VERIFIED**

Date: 2026-08-20

## Decision identity

`FD-MESC-BT-EXEC-1-PREFLIGHT`

## Authorized action after canonical activation

`MESC BACKBONE TOURNAMENT — ONE BOUNDED NO-MODEL-ACCESS EXECUTION PREFLIGHT / CORPUS AUDIT EPISODE`

## Activation preconditions

This authorization activates only when all are true:

1. this exact package is reviewed against then-current canonical `main`;
2. PR #130 remains in canonical ancestry;
3. `FD-MESC-BT-READINESS-REPAIR-2 = CONSUMED / REUSABLE = NO` remains canonical;
4. `BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE` remains canonical;
5. exact-head CI passes;
6. exact-head CodeQL passes;
7. a fresh independent exact-head governance review reports no unresolved blocking findings;
8. all review threads are resolved or explicitly dispositioned with evidence;
9. the package is marked Ready only after those gates pass;
10. merge uses exact expected-head protection;
11. post-merge canonical main/tree/ordered parents/signature are mechanically verified.

## Authority if activated

One episode may:

- inspect canonical repository/governance history read-only;
- read the exact committed Repair-2 corpus, corpus specification, manifest, scoring keys, prompts, parser/scoring/report contracts, and their Git objects;
- decompress the exact committed corpus locally and compute deterministic byte lengths and SHA-256 values;
- run deterministic local validation over all 240 committed corpus records and all 240 scoring-key records;
- verify exact item-ID membership/order, six 40-item axes, archetype/difficulty assignment, task-template bindings, answer-state/scoring-key compatibility, evidence-reference integrity, payload/gold separation, and frozen R2 source prohibitions;
- generate deterministic `R2_PROVENANCE_AUDIT` and `CORPUS_SPEC_MANIFEST_CONFORMANCE_AUDIT` artifacts under the exact canonical serialization rule in `acceptance.md`;
- generate a fully hash-bound preflight result manifest, verdict, execution-binding inventory, activation receipt, and consumption receipt;
- record negative audit findings as first-class evidence and terminate `BLOCKED` on any mismatch;
- inspect public, ungated candidate/runtime metadata read-only only when needed to inventory remaining execution bindings;
- record exact hardware/provider/runtime facts only when they are actually observed and independently identifiable;
- propose, but not activate, a candidate subset of at least two previously admitted candidates;
- create exactly one uniquely identified successor inactive candidate, `FD-MESC-BT-EXEC-1-CANDIDATE-V2`, at `specs/mesc-backbone-tournament/execution-preflight-1-result/execution-authorization-candidate.md` only if all acceptance sections pass.

The existing `readiness-repair-2-result/execution-authorization-candidate.md` is immutable historical seed evidence. It is superseded only if the V2 successor is later canonically merged and post-merge verified; until then it remains the only canonical candidate record.

## Explicit exclusions

This authorization does **not** permit:

- downloading, opening, loading, inspecting, or accessing model weights;
- requesting or accepting gated model access;
- accepting gated-access terms or model-access agreements;
- serializing any tournament prompt to any model endpoint/runtime;
- inference or generation;
- benchmark/tournament execution;
- scoring or ranking model outputs;
- selecting a Compact or Flagship/Reasoner winner;
- B0/B1/B2/B3 execution or P01-06+;
- Pilot-01 test-content access or scientific-content inspection;
- real patient data, PHI, product telemetry, or other R2-prohibited data;
- external benchmark ingestion;
- training, continued pretraining, SFT, fine-tuning, QLoRA, adapters, preference optimization, RL, verifier training, or distillation;
- retrieval activation;
- fallback substitution;
- quantization changes or derivative quantized entries;
- challenger population;
- excluded model-family admission;
- clinical, safety, efficacy, publication, release, or production claims.

## Fail-closed rules

Any mismatch in committed corpus/storage/logical/scoring-key identity, any missing frozen protocol-contract binding, any non-canonical item ID, any prohibited source indication, any gold leakage into model-visible payload, any unresolved evidence-reference mismatch, any result-package hash mismatch, any missing/mismatched activation or consumption receipt, or any inability to reproduce a required audit deterministically => `BLOCKED`.

Gated candidates remain non-accessible during this episode. No wording in this authorization constitutes acceptance of Apertus or MedGemma gated terms.

## Single-use receipt and consumption rule

This decision is single-use and must be replay-resistant.

1. After this authorization package is canonically merged and post-merge verified, derive `ACTIVATION_RECEIPT_ID` exactly as specified in `acceptance.md`, bound to this decision ID, the canonical authorization merge SHA/tree, and the four authorization-package Git blob SHAs.
2. Before any audit begins, canonical history and any existing/open/closed result PR for this decision must be checked for that receipt. An already-consumed receipt, a mismatched receipt for the same authorization merge, or an existing completed/blocked episode => `BLOCKED`; this authorization cannot be replayed.
3. The result branch must carry the matching `activation-receipt.json` before audit-result publication.
4. Every terminal episode, successful or blocked, preserves its receipt and evidence. A successful result additionally carries `consumption-receipt.json` bound to the exact final result-manifest SHA-256.
5. Canonical merge of the result package is the durable `CONSUMED` state. After that state exists, reuse is rejected fail-closed.
6. A failed or blocked episode may not restart under this decision. A new attempt requires a new separately reviewed founder authorization.

Terminal outcomes are only:

- `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, or
- `BLOCKED`.

Even `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` grants no execution authority.

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
