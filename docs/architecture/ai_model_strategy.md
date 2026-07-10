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

Candidates are filtered on two independent axes — **licence tier** (may it ship?) and
**role** (what job can it do?) — before capability is compared. The canonical registry,
with verified entries and the `medscale.registry` design, is a single source of truth:

> **→ [docs/models/model_registry.md](../models/model_registry.md)** (governed by
> ADR-0006; structured-artifact design under ADR-0012).

The load-bearing rule, restated here because it drives the whole model strategy: a
Tier-2-derived *released* adapter would impose upstream terms on every MedScale consumer,
silently narrowing the Apache-2.0 promise — so released adapter bases are Tier-1
generative models only, while any model may be an *evaluation* subject. Encoders
(ClinicalBERT, PubMedBERT, OpenMed) are extraction/NER baselines, never MESC bases.

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
