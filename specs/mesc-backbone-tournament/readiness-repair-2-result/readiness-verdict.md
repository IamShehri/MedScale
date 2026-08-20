# MESC Backbone Tournament — Repair-2 Readiness Verdict

Status: **TERMINAL VERDICT CANDIDATE — EFFECTIVE ONLY AFTER CANONICAL MERGE AND POST-MERGE VERIFICATION**

Authority: `FD-MESC-BT-READINESS-REPAIR-2`

Canonical episode snapshot:

```text
main = 53f517e57602b1b721fce6edae71d6f9e64d3bc6
tree = aff1c0ba76cd9959141c7208d8efb14b37228f16
```

## Required evidence disposition

### Apertus blocker

```text
BT-RDY-BLK-APERTUS-AUP-001 = RESOLVED
AUP_BYTE_LENGTH = 53794
AUP_SHA256 = 424b0a0d24ee1369f9a8614d9e4c7eb0fc3ee8a9ad7ece39baea3a83f0d4ba76
AUP_COMPUTED_GIT_BLOB = 8ddd8e25b6672340dd4f921ba623578571a65526
AUP_AUTHORITATIVE_GIT_BLOB = 8ddd8e25b6672340dd4f921ba623578571a65526
AUP_BINDING = EXACT_MATCH
```

The exact v1.5 PDF was interpreted only after byte identity was proven. No gated model access or terms acceptance occurred.

### Candidate roster

```text
openai/gpt-oss-20b = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
swiss-ai/Apertus-v1.5-8B = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
microsoft/Phi-4-multimodal-instruct = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
google/medgemma-1.5-4b-it = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
challenger = EMPTY
BLOCKED_NON_EMPTY_CANDIDATES = 0
ADMITTED_DISTINCT_CANDIDATES = 4
MINIMUM_REQUIRED = 2
ROSTER_GATE = PASS
```

Every non-empty candidate was refreshed from then-current authoritative sources during repair-2. Historical repair-1 dispositions were not treated as current proof.

### Program rules

```text
R2_SYNTHETIC_ONLY = PRESERVED
R3_DERIVATIVE_AND_COMMERCIAL_USE = PROVEN_COMPATIBLE_FOR_ADMITTED_CANDIDATES
R5_VERIFICATION_IS_A_RUN = PRESERVED
R6_EXPENSIVE_DECISION_ADR = SATISFIED_BY_ADR_0034_CANDIDATE
R7_NO_RESULT_WITHOUT_ARTIFACT = PRESERVED
```

### Six-axis freeze

`MESC-BT-PROTOCOL-V1` freezes all six mandatory axes with a 240-item R2-only future corpus design, equal-treatment rules, deterministic decoding, parser/error/abstention semantics, visible scoring weights, Compact/Flagship thresholds, tie-breaks, and `NO_SELECTION` behavior.

```text
PROTOCOL_CONFIG_SHA256 = 30e9402ef10739da040a741938a7bcac1405d81d97884e08bfbd88f0b0446baa
SYSTEM_PROMPT_SHA256 = 02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867
ALL_SIX_AXES_FROZEN = YES
```

The exact materialized corpus hash is correctly deferred to the separate execution authorization because readiness is authorized to freeze the corpus specification/provenance contract, not fabricate uncreated corpus bytes.

## Terminal verdict candidate

If and only if this exact result package passes exact-head CI/CodeQL, fresh independent exact-head review, zero unresolved blocking threads, expected-head merge protection, and post-merge canonical verification, record:

```text
FD-MESC-BT-READINESS-REPAIR-2 = CONSUMED
REUSABLE = NO
BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
```

`FD-MESC-BT-EXEC-1` exists only as an inactive candidate and cannot inherit execution authority from readiness.

## Negative authority statement

No model was downloaded, opened, loaded, queried, or ranked in repair-2. No gated access was requested or accepted. No synthetic tournament corpus was executed. No B0/B1/B2/B3, P01-06+, Pilot-01 test inspection, PHI/patient/product/telemetry access, training, retrieval, fallback substitution, quantization change, challenger addition, or downstream runtime implementation occurred.

Until canonical adoption of this exact result, repair-2 remains active/non-terminal and the prior canonical readiness state remains the source of truth.
