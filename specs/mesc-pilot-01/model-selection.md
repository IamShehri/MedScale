# MESC Pilot-01 — Model Selection

Status: **founder-frozen**
Authorized by: Founder and ChatGPT
Hermes authority: repository implementation and verification only
Freeze date: 2026-07-16

---

## Frozen selection

```text
MESC GENERAL REASONING CORE FAMILY: LLAMA

PILOT-01 PRIMARY TRAINING TARGET: meta-llama/Llama-3.2-3B-Instruct

LOW-MEMORY FALLBACK: meta-llama/Llama-3.2-1B-Instruct

CLINICAL SPECIALIST: google/medgemma-1.5-4b-it

BIOMEDICAL AND LITERATURE SPECIALIST: BioMistral/BioMistral-7B

RETRIEVAL: BAAI/bge-m3

EVIDENCE VERIFICATION: MedScale-native Evidence Judge

GENERAL EXTERNAL BASELINE: Qwen/Qwen3-4B-Instruct-2507

REASONING EXTERNAL BASELINE: deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B

MULTILINGUAL AND ARABIC FUTURE COMPARATOR: CohereLabs/aya-expanse-8b
```

```text
SELECTION AUTHORITY: FOUNDER AND CHATGPT

HERMES AUTHORITY: REPOSITORY IMPLEMENTATION AND VERIFICATION ONLY
```

---

## Verification notes

- Llama 3.2 Instruct models are gated on Hugging Face; acceptance of the Llama 3.2 Community License is required.
  Commercial-use threshold: >700 million monthly active users requires a separate Meta commercial license.
- MedGemma requires acceptance of the Health AI Developer Foundation Terms of Use.
- BioMistral-7B is Apache-2.0 and publicly accessible.
- BGE-M3 is Apache-2.0 and publicly accessible.
- Qwen3-4B-Instruct-2507 is publicly accessible.
- DeepSeek-R1-Distill-Qwen-1.5B is MIT licensed.
- Aya Expanse 8B requires CC-BY-NC acceptance and Cohere Labs Acceptable Use Policy compliance.
- No model weights were downloaded in this turn.
- No inference was executed in this turn.

---

## Non-negotiable constraints

- Do not replace Llama as the general MESC core.
- Do not select Qwen as the primary training target.
- Do not select MedGemma as the primary training target.
- Do not substitute the low-memory fallback without a separately authorized feasibility test.
- Do not narrow the architecture to a single model.
- Do not hard-code any named model into stable scientific data contracts.

## P01-05 entry contract — current model authority

The controlling current execution authority for MESC Pilot-01 is recorded in
`specs/mesc-pilot-01/p01-05/decision-record.md` and the supersession section of
`model-landscape.md`.

Chinese model families are NOT permitted for MESC execution:
Qwen, DeepSeek, Yi, GLM, InternLM.

Historical external baseline selections for Qwen and DeepSeek, and the
historical retrieval selection for BAAI/bge-m3, are SUPERSEDED FOR EXECUTION
under the current founder constraint. The historical records are preserved;
they are not removed.

Current permitted execution targets:

- `meta-llama/Llama-3.2-3B-Instruct`: PERMITTED PRIMARY PILOT TARGET —
  execution still separately gated.
- `meta-llama/Llama-3.2-1B-Instruct`: PERMITTED LOW-MEMORY FALLBACK —
  substitution separately gated.
- `google/medgemma-1.5-4b-it`: PERMITTED FUTURE CLINICAL SPECIALIST /
  COMPARATOR — separate authorization required.
- `BioMistral/BioMistral-7B`: PERMITTED FUTURE BIOMEDICAL SPECIALIST —
  separate authorization required.
- `CohereLabs/aya-expanse-8b`: FUTURE COMPARATOR ONLY — license/non-commercial
  constraints remain — separate authorization required.
