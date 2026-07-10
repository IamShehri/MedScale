# MedScale Research Vision

- **Status:** Foundational (governs scope; changes require an ADR)
- **Date:** 2026-07-09
- **Horizon:** 2026–2036
- **Owner:** Operator (solo founder)

This document defines what MedScale is, what it is not, and where it is going. It is the
top of the scope hierarchy: when a proposed piece of work cannot be traced to a research
question in `docs/research/research_questions.md` and a horizon below, it is out of
scope until this document is amended.

---

## 1. Mission

Make clinical AI **verifiable**. MedScale builds systems that produce healthcare data
and reasoning whose correctness can be *checked mechanically* — against FHIR
StructureDefinitions, against terminology value sets, and against executable queries —
rather than merely *judged plausibly*. The bet is that in medicine, form that can be
validated and content that can be traced to a source are worth more than fluent prose
that cannot be checked.

## 2. What MedScale IS

- A **FHIR-native clinical reasoning system**: QLoRA adapters over an open, permissively
  licensed base model + grammar-constrained decoding against FHIR StructureDefinitions +
  a validation layer.
- A **research engine**: a literature database, reproducible benchmarks
  (MedScale-Bench), synthetic datasets, trained adapters, and scientific publications.
- **FHIR intelligence**: structural, terminology, and profile validation; grammar
  emission; note↔bundle transformation; FHIRPath query and repair.
- An **open-source platform** intended to be consumed by products (Afia first) and by
  the wider research community.
- **Verification-first**: every claim is backed by a reproducible script and a committed
  result artifact (Rule R7); every metric that headlines is deterministic and executable.

## 3. What MedScale is NOT

- **NOT a from-scratch pretrained foundation model.** MedScale is adapters +
  constrained decoding + validation over an *existing* open base model. This phrase is
  banned from all MedScale documentation and communication.
- **NOT a medical device, and NOT a clinical decision-making tool.** Outputs are not
  validated on real patient data and must never be used for diagnosis, treatment, or
  triage. This constraint is restated in every model card.
- **NOT trained or evaluated on PHI.** Synthetic data only (Synthea, hand-authored
  fixtures). See the PHI boundary in §5.
- **NOT the Afia product.** MedScale does not own user workflows, UI, scheduling,
  storage, or clinical applications. It has no dependency on Afia.
- **NOT a leaderboard-chasing "state of the art" effort.** No superlative performance
  claims; only reported numbers with seeds and confidence intervals. Honest negative
  results are first-class deliverables.

## 4. Guiding scientific hypothesis

**Grammar guarantees FORM; training only teaches CONTENT.** If grammar-constrained
decoding against FHIR StructureDefinitions can guarantee structural validity for free,
then a small, cheap QLoRA adapter needs only to learn *what to say*, not *how to shape
it* — making a clinically useful FHIR model buildable on a solo founder's compute budget.
This hypothesis is the reason MedScale is affordable, and it is designed to be
*falsified*, not assumed (see `docs/research/research_questions.md`, RQ1–RQ2, and
`docs/research/constrained_decoding_hypothesis.md` when T2 lands).

## 5. Relationship to Afia

**Afia consumes MedScale. MedScale must never depend on Afia.** (Formalized in
ADR-0003.)

| | MedScale (research engine) | Afia (product layer) |
|---|---|---|
| Owns | FHIR intelligence, benchmarks, datasets, models, publications | Healthcare OS, Studio, AI Lab, clinical workflows, UI |
| Data | Synthetic only (Synthea, fixtures) | Real clinical data / PHI in production |
| Released as | Open-source package + model weights + FHIR schemas | Product |
| Depends on | Nothing in Afia | Pinned MedScale releases |

**Consumption contract (outbound only).** Afia consumes MedScale through *published,
versioned artifacts*, never by importing MedScale source:
1. a Python package (`medscale` / `fhirkit`) — validation, grammar, FHIRPath;
2. released model weights (adapters + base reference);
3. released FHIR schemas / GBNF grammars.
Afia pins a MedScale version; MedScale never pins Afia.

**PHI boundary (one-way, absolute).** Real patient data, product telemetry, and clinical
content from Afia must **never** flow into MedScale training, evaluation, or benchmark
data (Rule R2). If a task appears to need real or credentialed data (MIMIC, etc.), work
stops and a licensing/PHI note is raised. Crossing this boundary would both violate R2
and invalidate every MedScale model card, which asserts the models are not validated on
real patient data.

## 6. Long-term research direction (2026–2036)

Staged into horizons. **Only Horizon 1 is committed work.** Everything beyond is
directional and explicitly gated: nothing advances a horizon until the prior horizon's
artifacts exist and the operator's compute budget (Rule: >1 GPU-week is out of scope)
still holds. This section is a *filter*, not a backlog.

### Horizon 1 — Foundations (2026–2027) · COMMITTED
- The technical core: `fhirkit` validation + grammar (T2).
- MedScale-Bench v0 — the crown artifact: deterministic, executable, PHI-free (T3).
- Empirical base-model landscape and the constrained-decoding 2×2 test (T4).
- Reproducible training-data pipeline and MESC-v0 QLoRA adapter (T5–T6).
- Honest evaluation + model card, including negative results (T7).
- A curated, citation-verified literature database (T1).
- **Success = a green benchmark, a published adapter or a published null result, and
  a reproducible pipeline — all on Colab-class compute.**

### Horizon 2 — Breadth and rigor (2027–2029) · DIRECTIONAL
- More FHIR resource types and profiles; deeper terminology grounding under proper
  licences (LOINC, RxNorm; SNOMED only via licensed, non-vendored interface).
- MedScale-Bench v1: harder tasks, external administration, held-out test set as a
  community leaderboard.
- Multi-adapter / task-specialized models; systematic ablations of the form-vs-content
  hypothesis across bases.

### Horizon 3 — Platform (2029–2032) · DIRECTIONAL
- MedScale as a cited, community-used open benchmark and toolkit for FHIR-native AI.
- Reproducibility infrastructure others can run; dataset and model cards as a standard.

### Horizon 4 — Ambition, gated on evidence (2032–2036) · ASPIRATIONAL
- Broader clinical reasoning under verification; interoperability beyond FHIR where
  evidence justifies it.
- **Explicitly not committed and not planned in detail.** Recorded so the near-term
  work is not mistaken for the whole ambition — and so the ambition is not mistaken for
  license to expand near-term scope.

### Permanently out of scope for v0 (restated so it is not re-litigated)
RLHF, DPO, MoE, model merging, and continual learning are out of scope for v0. There is
no evidence yet that they help MedScale's problem, and adding them now is how solo
projects die. Any reintroduction requires an ADR citing evidence.

## 7. Scope-drift guardrails

1. **Traceability.** New work must map to a research question (RQ) and a horizon. No
   RQ + horizon → out of scope until this document is amended.
2. **One ticket per session** (Rule R4). Finish, verify, commit; never start N+1.
3. **Compute ceiling** (operator rule). Any plan needing >1 GPU-week is flagged and not
   attempted.
4. **Verification is a run, not a claim** (Rules R5, R7). No "should work"; no number
   without a script and a committed artifact.
5. **The benchmark is not marketing.** MedScale-Bench integrity is firewalled from
   Afia's commercial interests; a result that does not flatter the product is published
   exactly as a result that does.

## 8. Open-source and licensing stance

MedScale is intended to be open source under a permissive licence (Apache-2.0 is the
working assumption, pending a licence ADR) so that Afia — and others — may build
commercial products on it. This makes a platform-wide invariant, broader than any single
ticket: **every** model, dataset, and value set MedScale ships or trains on must permit
*derivative models + commercial use*. Research-only or non-redistributable content is
excluded regardless of quality. SNOMED CT is the sharp edge and is handled by interface
only — license-gated, never vendored into the repository. Each `data/` directory carries
a `LICENSE.md` (Rule R3), enforced in CI from T0.

## 9. Change control

This document changes only by ADR. Amendments that expand scope, move a horizon forward,
or weaken the PHI boundary or the dependency direction require explicit operator
approval before implementation (Rule R6).
