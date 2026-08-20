# MESC Backbone Tournament — Readiness Repair-2 Result

Status: **RESULT CANDIDATE — EFFECTIVE ONLY AFTER CANONICAL MERGE AND POST-MERGE VERIFICATION**

Date: 2026-08-20

Authority: `FD-MESC-BT-READINESS-REPAIR-2`

Canonical snapshot inspected:

```text
main = 53f517e57602b1b721fce6edae71d6f9e64d3bc6
tree = aff1c0ba76cd9959141c7208d8efb14b37228f16
```

This package records the terminal evidence candidate for the one bounded read-only repair-2 episode. It does not execute the tournament and does not access model weights.

## Result summary

The previously unresolved Apertus 1.5 AUP artifact was reconstructed from authoritative public GitHub Base64 content and mechanically bound to the repository object before interpretation:

```text
path = apertus_1.5/USAGE_POLICY.pdf
byte_length = 53794
sha256 = 424b0a0d24ee1369f9a8614d9e4c7eb0fc3ee8a9ad7ece39baea3a83f0d4ba76
git_blob_sha1 = 8ddd8e25b6672340dd4f921ba623578571a65526
authoritative_git_blob_sha1 = 8ddd8e25b6672340dd4f921ba623578571a65526
binding = EXACT_MATCH
```

The exact bound PDF rendered successfully and identified itself as Apertus LLM Acceptable Use Policy v1.5 dated 2026-07-14. Material restrictions were assessed against canonical MESC Program Rules before candidate disposition.

All four non-empty roster slots were independently refreshed from then-current authoritative sources. Historical repair-1 dispositions were not carried forward as evidence.

## Candidate disposition candidate

| Slot | Exact candidate | Exact revision | Disposition |
|---|---|---|---|
| 1 | `openai/gpt-oss-20b` | `6cee5e81ee83917806bbde320786a8fb61efebee` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 2 | `swiss-ai/Apertus-v1.5-8B` | `a411d838600baf0e3635a3daf66fb7c55fc97bb6` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 3 | `microsoft/Phi-4-multimodal-instruct` | `93f923e1a7727d1c4f446756212d9d3e8fcc5d81` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 4 | `google/medgemma-1.5-4b-it` | `91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 5 | Challenger | n/a | `EMPTY` |

No non-empty slot remains `BLOCKED`. At least two distinct candidates are admitted, so the protocol-freeze phase is permitted by the controlling readiness contract.

## Acceptance-artifact reconciliation

The readiness corpus and future execution materialization are explicitly separated. The readiness artifact freezes the 240 item identities/archetypes/difficulty/target-state/provenance/template bindings; the later execution artifact supplies concrete synthetic/hand-authored case payloads and receives its own distinct SHA-256.

```text
READINESS_CORPUS_SPEC_ID = MESC-BT-CORPUS-SPEC-V1
READINESS_CORPUS_ITEM_COUNT = 240
READINESS_CORPUS_SPEC_SHA256 = 73a236db0fe4a7ab9064d87b70d8dac98b3a7f1bf15132ac239f2393072d65c3
MATERIALIZED_CORPUS_SHA256 = REQUIRED_LATER_FOR_EXECUTION

PROMPT_BUNDLE_ID = MESC-BT-PROMPTS-V1
SYSTEM_PROMPT_SHA256 = 02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867
TASK_PROMPT_BUNDLE_SHA256 = fb0b24fbc55f81e3fc3b828fe9b7c291df883e82c8f9362f2cf2d8afeedca777
PROTOCOL_CONFIG_SHA256 = 30e9402ef10739da040a741938a7bcac1405d81d97884e08bfbd88f0b0446baa
PROMPT_PROTOCOL_SHA256 = 0928585636fc3ea2e3b1066ac0cf19a30b38bb69ffad6a1b240247bb2f566ef1

REPORT_SCHEMA_ID = MESC-BT-REPORT-V1
REPORT_SCHEMA_SHA256 = 64962cd417e5b0816ec1a3078a506f9a5509367ed573168f9c152151035a80d1
```

See `acceptance-reconciliation.md` for the normative mapping to repair-2 acceptance items 16–23.

## Package files

- `apertus-aup-resolution.md` — exact legal-artifact binding and disposition evidence.
- `candidate-manifest.md` — refreshed exact candidate identities, revisions, licensing/access/runtime evidence, and dispositions.
- `corpus-specification.json` — canonical 240-slot readiness corpus specification and R2 materialization contract.
- `task-prompts.json` — exact system prompt, six task templates, formatting policy, and answer-state envelope.
- `protocol-freeze.md` — six-axis equal-treatment/decoding/scoring/resource freeze and digest bindings.
- `report-schema.json` — canonical future aggregate-report JSON Schema.
- `reproducibility-schema.md` — required future run/artifact identity contract.
- `acceptance-reconciliation.md` — explicit readiness-spec versus later materialized-corpus distinction and acceptance mapping.
- `execution-authorization-candidate.md` — `FD-MESC-BT-EXEC-1` candidate, explicitly inactive.
- `readiness-verdict.md` — terminal repair-2 verdict candidate.
- `docs/adr/0034-backbone-tournament-protocol-freeze.md` — R6 decision record for experiment-defining protocol choices.

## Non-authority

This result package grants none of the following:

- model-weight download, opening, loading, or access;
- gated model access request or acceptance;
- gated terms acceptance;
- inference or generation;
- tournament or benchmark execution;
- B0/B1/B2/B3 or P01-06+ work;
- Pilot-01 test-content access;
- PHI, patient, product, telemetry, or credentialed clinical data;
- training, SFT, QLoRA, RL, retrieval, fallback substitution, or quantization change;
- challenger population;
- MCRL, AMGE, audio, biosignal, or donor runtime implementation;
- publication, clinical, or production claims.

Until this exact package passes exact-head review/checks, is merged with expected-head protection, and is post-merge mechanically verified, the prior canonical state remains controlling and repair-2 must not be described as terminally consumed.
