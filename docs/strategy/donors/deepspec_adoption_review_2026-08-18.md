# DeepSpec Adoption Review for MESC

Date: 2026-08-18
Status: STRATEGIC DONOR REVIEW — NO IMPLEMENTATION AUTHORIZED

## Source

Repository: `deepseek-ai/DeepSpec`

Reviewed live upstream state:

- default branch: `main`
- reviewed recent head: `005e03b81cec38b7da6399833d609ee89a2587f2`
- license: MIT, subject to third-party notices for adapted components
- purpose: training/evaluating draft models for speculative decoding
- supported draft families in the current repository include DSpark, DFlash, and Eagle3

## Decision

Classification: `HIGH_VALUE_LATE_STAGE_SERVING_DONOR`

DeepSpec is **not** a MESC medical backbone candidate and is **not** part of the current Pilot-01 execution path.

Its value to MESC is inference efficiency after a Compact/Flagship target model has been selected and scientifically frozen.

This review does not authorize:

- DeepSpec installation;
- speculative-decoding training;
- draft-model generation;
- use of Qwen or another excluded model family in MESC;
- changes to Pilot-01;
- training or serving implementation.

## Why it matters

Speculative decoding separates a smaller draft model from the authoritative target model. The draft proposes future tokens and the target model verifies them. This creates a path to reduce latency and increase serving efficiency without turning the draft model into the source of medical truth.

The DSpark work associated with DeepSpec reports large serving gains in production DeepSeek-V4 settings. The exact speedup for MESC must be measured independently on the eventual MESC target model, medical workloads, hardware, batch sizes, generation settings, and safety constraints.

## MESC role

DeepSpec belongs in a future layer:

```text
MESC-Compact / MESC-Reasoner
        │
        ▼
Authoritative target model
        │
        ├── normal decoding baseline
        │
        └── speculative decoding
              ├── MESC draft model
              ├── target verification
              └── serving telemetry
```

The target model remains authoritative.

## Required MESC invariants

Any future speculative-decoding adoption must prove:

1. **Quality preservation** — outputs satisfy the selected exact-verification semantics and do not silently change clinical decisions relative to the canonical decoding baseline.
2. **Safety preservation** — abstention, emergency escalation, tool calls, evidence citations, and MCRL control states are not weakened by acceleration.
3. **Determinism characterization** — any changes caused by kernels, sampling, batching, precision, or scheduler behavior are measured and documented.
4. **Target identity pinning** — each draft model is bound to an exact target-model identity/revision and training recipe.
5. **Domain-aware draft training** — if medical-domain draft adaptation is used, the training data receives the same provenance, licensing, decontamination, split, and safety controls as other MESC training data.
6. **No evaluation leakage** — target-cache or draft-training generation must never consume quarantined MESC-Eval/test scientific content.
7. **Performance proof** — latency, throughput, memory, energy/cost, accepted-token length, and tail latency are measured on representative MESC workloads.
8. **Fallback** — MESC can always disable speculative decoding and return to the canonical target-only path.

## Important upstream constraints

The current DeepSpec data pipeline can generate extremely large target caches; its README warns that a default example setting can require tens of terabytes. MESC must not reproduce that pipeline blindly.

The current repository includes target configurations and released checkpoints for model families that are not permitted in the MESC core model stack. Code/algorithm research must remain separated from model-family admission.

## Recommended adoption phase

Do not evaluate DeepSpec during Pilot-01 or initial backbone selection.

Recommended sequence:

1. close Pilot-01;
2. run MESC Backbone Tournament;
3. choose and freeze MESC-Compact and MESC-Reasoner;
4. complete canonical target-only quality/safety evaluation;
5. profile real serving bottlenecks;
6. only then open `MESC SPECULATIVE DECODING ADMISSION`;
7. compare DSpark, DFlash, Eagle3, and any newer strong open alternatives against a no-speculation baseline.

## Recommendation

Priority for medical quality: `LOW NOW`

Priority for eventual Hugging Face/product serving quality: `HIGH LATER`

Direct dependency: `NOT APPROVED`

DeepSeek model use: `NOT APPROVED`

Use as algorithm/runtime donor after model freeze: `RECOMMENDED FOR FUTURE EVALUATION`.
