# AI Model Strategy

- **Status:** Strategy (governed by [ADR-0006](../adr/0006-model-access-strategy.md), Proposed;
  final base selection remains the empirical T4 decision, reserved ADR-0002)
- **Date:** 2026-07-10
- **Related:** [ecosystem analysis §2](ecosystem_analysis.md#2-medical-foundation-models),
  Rules R3/R7, [RQ1–RQ2](../research/research_questions.md),
  [Strategic Blueprint §10](../vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md)

## Invariants (unchanged, restated)

**Adapt, don't pretrain.** MedScale consumes open models and adds value through
constrained decoding, cheap adaptation (QLoRA), and validator-grounded verification. The
compute ceiling (~1 GPU-week) stands. Nothing below reopens that.

## The licence-first candidate registry

Candidates enter a *registry document* (not code) in two tiers, filtered by licence
before capability is even considered:

| Tier | Criterion | Current members (evidence: 2026-07-10) | Permitted roles |
|---|---|---|---|
| **1 — clean-permissive** | OSI-style licence permitting derivatives + commercial use with no terms passthrough | BioMistral-7B (Apache-2.0); other Apache/MIT-family open models to be enumerated at T4 | Base for released MESC adapters; benchmark subject; extraction model |
| **2 — conditional terms** | Derivatives + commercial permitted, but with passthrough obligations / use policies (e.g. HAI-DEF) | MedGemma 1.5-4B / 4B / 27B, MedSigLIP | Benchmark/comparison subject; reasoning reference. Adapter base **only** via explicit ADR accepting the passthrough |

Rationale for the tiers: a Tier-2-derived released adapter would impose the upstream
terms on every MedScale consumer, silently narrowing the Apache-2.0 promise (Rule R3's
spirit, not just its letter).

### Model role is a second axis (orthogonal to licence tier)

Licence tier says whether a model may ship in an artifact; **role** says what job it can
do. The two are independent, and conflating them is a common error (an encoder is not a
smaller generator). MedScale's core task — generating FHIR JSON under a grammar — is
**generative**, so only generative (decoder/seq2seq) models can be MESC bases. Encoders
(BERT-family) cannot generate; their value is as deterministic **extraction/NER baselines
and span tooling** (RQ5), the same role as OpenMed's models.

| Role | What it does in MedScale | Eligible model kind |
|---|---|---|
| **Generative base** | MESC adapter base; constrained-decoding subject | Decoder / seq2seq LLMs (Tier 1 for release) |
| **Reasoning reference** | Benchmark comparison only | Generative, any tier (eval-only) |
| **Extraction / NER baseline** | T-EXTRACT non-LLM baseline; span fixtures for RQ5 | Encoder token-classifiers |
| **Embedding / retrieval** | Deferred (no v0 RAG); only where provenance is checkable | Encoders — H2+ |

### Registry entries (verified 2026-07-10; extends the tier table)

| Model | Kind | Licence (tier) | Role | Provenance note |
|---|---|---|---|---|
| BioMistral-7B | Generative (Mistral) | Apache-2.0 (T1) | Generative base candidate; comparison | Trained on PMC-OA |
| MedGemma 4B/27B, MedSigLIP | Generative / multimodal | HAI-DEF (T2) | Eval/comparison only; base only via ADR | Google HAI-DEF terms |
| Bio_ClinicalBERT | **Encoder** | MIT (T1) | Extraction/NER baseline | Trained on **MIMIC-III** (de-identified, credentialed). Weights are MIT and are a *released artifact* — using them as a baseline does **not** put MIMIC data into MedScale (R2 unbroken); provenance stated for transparency |
| PubMedBERT / BiomedBERT | **Encoder** | MIT (T1) | Extraction/NER baseline; embedding (H2+) | Pretrained on public PubMed + PMC |
| OpenMed NER models | **Encoder** | Apache-2.0 (T1) | Extraction/NER baseline (ADR-0007) | On-device; pinned by revision + SHA |

The registry stays a documentation artifact under ADR-0006 until T4 needs it structured
([ADR-0012](../adr/0012-layered-architecture-model.md) confirms: no `models/` package is
created merely because it is common). Every future row records licence, tier, role, and a
verified source before it informs any decision.

## Answers to the standing questions

**RAG, fine-tuning, agents, multiple models?**

- **Constrained decoding first.** It is the thesis (RQ1) and it is free. Everything else
  is measured against it.
- **Fine-tuning (QLoRA): yes, but only as the RQ2 experiment** — its *marginal value over
  the constrained base* is the question, not an assumption. If the adapter adds nothing
  beyond seed variance, that null result ships.
- **RAG: not a v0 platform feature.** Retrieval enters only where provenance is
  checkable — the litdb citation machinery (verified ids, `verified_at`) is the
  MedScale-grade form of "retrieval." Fluent-context RAG with unauditable grounding is
  the OpenEvidence pattern we differentiate *against*.
- **Agents: Horizon-2+, validator-gated only.** An agent step that cannot be checked by
  an executable oracle does not ship (RQ3/RQ4 territory).
- **Multiple models: yes, in evaluation; no, in production surface.** The benchmark
  compares many; the platform releases few.

**When does training start?** After, and only after:

1. T2 fhirkit is green (validator + grammar exist);
2. T3 benchmark v0 is green (there is something exact to measure against);
3. T4's 2×2 establishes the constrained-base baselines on the Tier-1 pool.

That is the existing T5→T6 gate; this analysis found no reason to accelerate it, and one
more reason not to: **medical-QA leaderboard scores (the evidence models are marketed on)
are weak proxies for grammar-constrained FHIR generation**, MedScale's actual task.

## Roles, mapped

| Role | Policy |
|---|---|
| Base model (MESC adapters) | Tier-1 only; selected empirically at T4 (ADR-0002) |
| Reasoning model | Tier 1 or 2 as *benchmark subjects*; none endorsed |
| Extraction model | Tier-1 constrained LLM vs OpenMed encoder baselines — measured in T3/T7 |
| Benchmark models | Any tier (evaluation-only use imposes no passthrough on consumers) |
| Future fine-tuning targets | Tier-1 pool at T4; multimodal (MedSigLIP-class) is Horizon-3+, gated on an executable ground truth existing |

## Data requirements before any training (T5 gate, restated)

Synthetic-only (Synthea + fixtures), validator-labeled, per-class corruptions (RQ4),
fixed splits with build-time contamination assertion, per-directory `LICENSE.md`. No new
data source enters without an R3 licence check.
