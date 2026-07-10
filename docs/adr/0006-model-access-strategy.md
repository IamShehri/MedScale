# ADR-0006 — Licence-First Model Registry with Two Eligibility Tiers

- **Status:** Proposed (awaiting operator approval)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none (reserved ADR-0002 — empirical base selection at T4 — remains open and is *narrowed*, not replaced, by this ADR)
- **Related:** [AI model strategy](../architecture/ai_model_strategy.md),
  [ecosystem analysis §2](../architecture/ecosystem_analysis.md#2-medical-foundation-models), Rule R3

## Context

Ecosystem evidence (2026-07-10) shows the open medical-model landscape splits on licence,
not capability: BioMistral-7B is Apache-2.0 (clean, but dated, and its authors warn
against clinical deployment); MedGemma (1.5-4B/4B/27B, MedSigLIP) is capable and permits
commercial use and fine-tuning — but under Health AI Developer Foundations terms that
impose terms-passthrough on distribution plus a prohibited-use policy. A MedGemma-derived
released adapter would therefore impose HAI-DEF terms on every downstream MedScale
consumer, silently narrowing the platform's Apache-2.0 promise. Rule R3's letter
(derivatives + commercial permitted) would be satisfied while its spirit (a permissive
platform others build on freely) would not.

## Decision (proposed)

1. **Candidate models are recorded in a registry document with two tiers**, filtered by
   licence before capability:
   - **Tier 1 (clean-permissive):** OSI-style terms, no passthrough → eligible as base
     for *released* MESC adapters, and for all evaluation roles.
   - **Tier 2 (conditional-terms, e.g. HAI-DEF):** eligible for *evaluation-only* roles
     (benchmark subject, comparison, reference). Use as a released-adapter base requires
     a dedicated ADR explicitly accepting the passthrough consequences.
2. **Evaluation-only use of Tier-2 models is pre-approved** (it imposes nothing on
   consumers of MedScale artifacts).
3. **Final base-model selection stays empirical at T4** (reserved ADR-0002): the
   constrained-decoding 2×2 runs on the Tier-1 pool; medical-QA leaderboard scores are
   explicitly *not* selection evidence, because MedScale's task is grammar-constrained
   FHIR generation, not exam QA.
4. **No training before the existing T5 gate.** This ADR changes eligibility, not
   schedule.

## Consequences

**Positive:** the R3 invariant becomes mechanically checkable at model level; MedGemma
remains usable where it is safe (evaluation) without contaminating releases; T4 has a
defined, smaller search space.

**Negative / costs:** Tier 1 currently excludes the most capable medical model
(MedGemma) from release paths — accepted deliberately; the registry document must be
maintained as licences and model versions evolve.

## Alternatives considered

- **Capability-first selection.** Rejected: risks a release whose licence poisons the
  platform promise (R3 spirit).
- **Ban Tier-2 models entirely.** Rejected: evaluation-only use is harmless and
  scientifically valuable (stronger comparisons in Papers 1–3).

## Compliance

The registry lives as a documentation table (extends the
[model strategy](../architecture/ai_model_strategy.md)) until T4 needs it in structured
form. Every registry row records: licence name, passthrough (y/n), derivative +
commercial rights, verification date, source URL.
