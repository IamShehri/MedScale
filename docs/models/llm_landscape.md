# Open LLM Landscape Analysis (Model Research Program, step 1–2)

- **Status:** Analysis — licence axis **verified**; capability axis **deliberately
  unverified until T4** (empirical, on MedScale-Bench tasks, not exam QA)
- **Date:** 2026-07-10
- **Related:** [model registry](model_registry.md) (canonical entries),
  [AI model strategy](../architecture/ai_model_strategy.md) (tiers + roles),
  [experiment framework](../research/experiment_framework.md), ADR-0006, reserved ADR-0002

The objective is **not** to choose the strongest model. It is to identify the best
foundation for a long-term open medical model family — where "best" is a joint property
of licence cleanliness, adaptability on the compute ceiling (~1 GPU-week, Colab-class
QLoRA), constrained-decoding compatibility, and community longevity. Capability numbers
published on medical-QA leaderboards are recorded as context only; they are **not
selection evidence** for FHIR-grammar generation (ADR-0006 §3).

## 1. Candidate pool (licences verified 2026-07-10, primary sources)

| Candidate | Kind | Licence (verified) | Tier | Compute fit (QLoRA ≤ 1 GPU-week) | Notes |
|---|---|---|---|---|---|
| **Qwen3** (0.6B–32B; 8B ref) | Generative decoder | **Apache-2.0** | **1** | ✅ 4B/8B ideal | 32K ctx native; active family, strong JSON/instruct reputation — verify empirically |
| **Mistral-7B-Instruct-v0.3** | Generative decoder | **Apache-2.0** | **1** | ✅ | ⚠️ *Per-model check required*: newer Mistral releases may use the Mistral Research License — each model verified individually, never family-wide |
| **DeepSeek-R1** | Generative MoE (671B/37B act.) | **MIT** (weights + code; distillation explicitly permitted) | **1** (licence) | ❌ far beyond ceiling | Practical entries are the **R1-Distill** variants — but each inherits its *base* licence (Qwen2.5 → Apache-2.0 = Tier 1; Llama → Tier 2) |
| **BioMistral-7B** | Generative decoder | **Apache-2.0** | **1** | ✅ | Medical continued-pretrain of Mistral-7B-v0.1 (Feb 2024, aging); authors warn against clinical use |
| **Llama 3.1** (8B ref) | Generative decoder | **Llama 3.1 Community License** — not OSI: licence passthrough, "Built with Llama" branding, derivative name-prefix rule, 700M-MAU clause, AUP | **2** | ✅ technically | Eval/comparison only; releasing a Llama-based adapter would impose Meta's terms + naming on every consumer |
| **MedGemma** (4B/27B) | Generative/multimodal | HAI-DEF terms (passthrough) | **2** | 4B ✅ | Eval/comparison only (ADR-0006); strongest medical-domain signal in the pool |
| **Meditron-7B** | Generative decoder | **Llama 2 Community License** (inherited) | **2** | ✅ | Sept-2023 era; PubMed+guidelines pretrain; authors advise against deployment; historically important, practically dated |

## 2. What the licence axis already decides

- **The Tier-1 generative pool for T4 is real and sufficient:** Qwen3 (4B/8B),
  Mistral-7B-v0.3, BioMistral-7B, and (licence-wise) R1-Distill-Qwen variants. No
  capability argument can promote a Tier-2 model into a release path — only a dedicated
  ADR can.
- **Tier 2 is still scientifically valuable:** Llama 3.1, MedGemma, and Meditron enter
  the T4 comparison as evaluation subjects, strengthening Papers 1–3 without touching
  the release chain.
- **Family ≠ licence:** Mistral and DeepSeek prove that licence must be verified
  *per model, per revision* — the registry records model-level facts, never
  family-level assumptions.

## 3. What is deliberately NOT decided here

- **No capability ranking.** RQ1's whole point is that unconstrained FHIR competence
  may not predict constrained performance. The T4 2×2 (unconstrained/constrained ×
  zero/few-shot) on MedScale-Bench tasks is the only admissible capability evidence,
  run under the [experiment framework](../research/experiment_framework.md).
- **No default winner.** Reserved **ADR-0002** records the empirical selection when T4
  produces manifests, not before.
- **No medical-domain preference.** Whether medical continued-pretraining (BioMistral,
  Meditron, MedGemma) helps *grammar-constrained FHIR generation* is exactly the kind
  of assumption MedScale tests rather than inherits.

## 4. Longevity considerations (10-year lens)

Model families die; the registry must outlive them. Signals recorded per family —
release cadence, organizational backing, licence stability across versions (Mistral's
drift is a caution), ecosystem tooling — inform *shortlisting*, not selection. The
architecture guarantee stands regardless: models are replaceable behind the
constrained-decoding + validation interface; if the 2029 best open model is none of the
above, MedScale swaps the base and re-runs the manifests. **That property — not any
row in this table — is the long-term asset.**

## 5. Feeding T4 (when its gate opens)

Shortlist rule: Tier-1 generative, ≤ 14B params (QLoRA on Colab-class hardware),
instruct-tuned, tokenizer-compatible with the grammar engine chosen in ADR-0001.
Current shortlist by that rule: **Qwen3-4B, Qwen3-8B, Mistral-7B-Instruct-v0.3,
BioMistral-7B** (+ R1-Distill-Qwen-7B pending grammar-engine compatibility check).
Tier-2 comparison set: MedGemma-4B, Llama-3.1-8B, Meditron-7B. Every run produces the
experiment manifest; no training (T5/T6) until the T4 baselines exist.
