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
- generate a deterministic `R2_PROVENANCE_AUDIT` artifact and SHA-256;
- generate a deterministic `CORPUS_SPEC_MANIFEST_CONFORMANCE_AUDIT` artifact and SHA-256;
- record negative audit findings as first-class evidence and terminate `BLOCKED` on any mismatch;
- inspect public, ungated candidate/runtime metadata read-only only when needed to inventory remaining execution bindings;
- record exact hardware/provider/runtime facts only when they are actually observed and independently identifiable;
- propose, but not activate, a candidate subset of at least two previously admitted candidates;
- create an inactive `FD-MESC-BT-EXEC-1` activation candidate only if both audits pass and every remaining unbound requirement is explicitly listed.

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

Any mismatch in committed corpus/storage/logical/scoring-key identity, any non-canonical item ID, any prohibited source indication, any gold leakage into model-visible payload, any unresolved evidence-reference mismatch, or any inability to reproduce a required audit deterministically => `BLOCKED`.

Gated candidates remain non-accessible during this episode. No wording in this authorization constitutes acceptance of Apertus or MedGemma gated terms.

## Consumption rule

If activated, this decision is consumed by exactly one bounded preflight episode and cannot be reused for execution.

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
