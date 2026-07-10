# Ecosystem Analysis

- **Status:** Analysis (evidence for Proposed ADRs 0005–0008; no implementation authorized)
- **Date:** 2026-07-10
- **Related:** [reference architecture](medscale_reference_architecture.md),
  [ADR-0005](../adr/0005-research-intelligence-scope.md) · [ADR-0006](../adr/0006-model-access-strategy.md) ·
  [ADR-0007](../adr/0007-openmed-adapter.md) · [ADR-0008](../adr/0008-interoperability-fhir-canonical.md)

Evidence-based assessment of the external ecosystem MedScale operates in. All facts below
were verified against the cited primary sources on **2026-07-10** (grey-tier evidence per
the [paper taxonomy](../research/paper_taxonomy.md): citable for facts, not for
performance claims). Nothing here authorizes integration; decisions live in the ADRs.

---

## 1. OpenMed

**Sources:** [github.com/maziyarpanahi/openmed](https://github.com/maziyarpanahi/openmed) ·
[huggingface.co/OpenMed](https://huggingface.co/OpenMed) (accessed 2026-07-10)

| Facet | Finding |
|---|---|
| Purpose | Local-first clinical NLP: medical NER + PII detection / de-identification |
| Scale | 1,511+ models on HF; 110M–1B param encoder models (BioClinicalBERT-family etc.) |
| Maturity | 4.4k stars, 531 forks, 2,119 commits, 36 releases (v1.8.0, July 2026) — active and healthy |
| Licence | **Apache-2.0** (repo and models) — clean pass under Rule R3 |
| Architecture | Python core; local inference (PyTorch CPU/CUDA, MLX, Transformers.js); also REST/Docker/mobile |
| Privacy | On-device by design; claims all 18 HIPAA Safe Harbor identifiers for de-id |

**Fit assessment.** OpenMed solves *clinical NLP over real text* — exactly the territory
MedScale deliberately does not own. Two subtleties matter:

1. **MedScale does not need de-identification for itself.** MedScale is synthetic-only
   (R2); there is no PHI to de-identify. Adopting OpenMed "because healthcare" would be
   scope creep.
2. **MedScale does need deterministic entity spans at evaluation time.** The T-EXTRACT
   hallucination metric (RQ5) is a *deterministic span-alignment scorer*. OpenMed's
   encoder NER models are deterministic per fixed weights, Apache-2.0, and local — a
   credible *optional assist* and *baseline family* for that scorer, and nothing more.

**Verdict → (C) optional adapter + (D) reference architecture.** Not a dependency, not a
service. Details and the avoid-list: [OpenMed strategy](openmed_integration_strategy.md);
decision: [ADR-0007](../adr/0007-openmed-adapter.md).

## 2. Medical foundation models

**Sources:** [MedGemma collection](https://huggingface.co/collections/google/medgemma-release) ·
[medgemma-27b-it card](https://huggingface.co/google/medgemma-27b-it) ·
[HAI-DEF terms](https://developers.google.com/health-ai-developer-foundations/terms) ·
[BioMistral-7B card](https://huggingface.co/BioMistral/BioMistral-7B) (accessed 2026-07-10)

| | MedGemma (1.5-4B / 4B / 27B, + MedSigLIP) | BioMistral-7B |
|---|---|---|
| Capability | Strong medical text + multimodal (radiology, dermatology, pathology, ophthalmology) | Dated (Feb 2024); 57.3% avg over 10 medical-QA sets (below GPT-3.5-turbo's 66.0%) |
| Licence | **Health AI Developer Foundations terms** — commercial use and fine-tuning permitted, **but** terms passthrough on distribution + prohibited-use policy; not OSI-open | **Apache-2.0** — clean R3 pass |
| Deployment | 4B runs on modest hardware; 27B needs serious VRAM | 7B, QLoRA-friendly |
| Clinical caveat | "Not intended to directly inform clinical diagnosis…" | Authors explicitly warn against clinical deployment |

**The licence asymmetry is the finding.** BioMistral is licence-clean but
capability-dated; MedGemma is capable but carries a passthrough obligation: a
MedGemma-derived MESC adapter would force HAI-DEF terms onto every downstream consumer,
layering non-permissive conditions inside MedScale's Apache-2.0 promise. That does not
disqualify MedGemma — HAI-DEF permits both derivative models and commercial use, so it
*passes R3's letter* — but it creates a two-tier candidate pool:

- **Tier 1 (clean-permissive):** eligible as base for released MESC adapters.
- **Tier 2 (conditional terms, e.g. HAI-DEF):** eligible as *benchmark/comparison*
  models; eligible as adapter base **only** by explicit ADR accepting the passthrough.

**No model is selected today.** Selection remains the empirical T4 decision (reserved
ADR-0002), made by running the constrained-decoding 2×2 on the licence-eligible pool.
Note that medical-QA scores are weak evidence for MedScale's actual task (FHIR-JSON
generation under grammar constraint) — another reason to decide at T4, not now.
Strategy: [AI model strategy](ai_model_strategy.md); decision:
[ADR-0006](../adr/0006-model-access-strategy.md).

## 3. FHIR (and the EHR Functional Model)

**Source:** [build.fhir.org/ehr-fm.html](https://build.fhir.org/ehr-fm.html) (accessed 2026-07-10)

The EHR-S Functional Model is an informative mapping from EHR *system* capabilities
(audit, attestation, security, storage) to FHIR resources. Its lesson for MedScale is a
boundary lesson: **FHIR-the-exchange-standard is MedScale's territory;
EHR-system-functionality is not.** MedScale validates, generates, and repairs FHIR
*resources*; it does not implement EHR functions (workflow, business rules — gaps the
EHR-FM itself acknowledges in FHIR). The fhirkit module (T2) remains exactly as
architected: validation, grammar emission, FHIRPath.
Strategy: [interoperability strategy](interoperability_strategy.md).

## 4. openEHR bridge

**Source:** [github.com/cistec-com/openEHR2FHIRquestionnaire](https://github.com/cistec-com/openEHR2FHIRquestionnaire) (accessed 2026-07-10)

MIT-licensed Python utility (Cistec AG): openEHR web templates → FHIR Questionnaire, and
QuestionnaireResponse → openEHR FLAT composition. Maturity is low (10 stars, no releases),
but that is beside the point — its value to MedScale is **existence proof of the boundary
pattern**: openEHR interop is achievable by *conversion at the edge*, with FHIR remaining
the single canonical representation inside the platform. MedScale should never carry a
dual-model core. openEHR (and DICOM) are Horizon-3 adapter candidates, not architecture.
Decision: [ADR-0008](../adr/0008-interoperability-fhir-canonical.md).

## 5. Market references (not dependencies)

**Sources:** [OpenEvidence coverage](https://aimagazine.com/news/how-openevidence-ai-is-transforming-clinical-decision-making) ·
[openevidence.com/about](https://www.openevidence.com/about) ·
[medwise.ai](https://medwise.ai) (accessed 2026-07-10; openevidence.com blocks direct fetch)

| | OpenEvidence (US) | Medwise (UK) |
|---|---|---|
| Model | AI copilot; answers grounded in literature with inline citations | Search-first answers from "trusted sources"; drug/tariff modes |
| Adoption | Reported >40% of US physicians daily; 10k+ hospitals; $210M Series B at $3.5B; NEJM/JAMA/Cochrane partnerships | 2,000+ NHS organisations; NHSmail auth; freemium |
| Access | Free for verified US clinicians | Freemium, UK-focused |
| Transparency | **Closed**: proprietary pipeline, unauditable retrieval/citation process | **Closed**; verification burden pushed to user ("always visit the source") |

**What the market proves:** massive validated demand for evidence-grounded clinical
answers — and a uniform blind spot. Both products ask users to *trust* citations they
cannot audit; neither publishes retrieval corpora, ranking, prompts, or failure rates;
neither is reproducible. That blind spot is precisely MedScale's thesis applied to
literature: **citation-grounding without verification is plausibility, not evidence.**

**Differentiation (MedScale does not compete for clinician eyeballs):**

1. **Infrastructure, not product.** MedScale is the open, Apache-2.0 substrate such
   products *should* be built on — the "HAPI FHIR of verifiable medical AI," not another
   answer box.
2. **Verifiable provenance as a first-class artifact.** R1-style citations (resolvable id
   + `verified_at` + `source_api`) and deterministic span-support scoring make "is this
   claim actually supported?" a *checkable* property, not a promise.
3. **Published evaluation.** MedScale ships the benchmark and its own failure numbers;
   closed products publish neither.
4. **Reproducibility.** Anyone can re-run the pipeline from committed artifacts.

## Summary table

| External element | Role in MedScale | Decision record |
|---|---|---|
| OpenMed | Optional eval-time adapter + reference architecture | ADR-0007 (Proposed) |
| MedGemma | Tier-2 candidate (benchmark/comparison; adapter base only by explicit ADR) | ADR-0006 (Proposed); selection at T4 (reserved ADR-0002) |
| BioMistral-7B | Tier-1 licence-clean candidate for the T4 landscape; likely comparison, not winner | ADR-0006 (Proposed) |
| FHIR | Canonical representation (unchanged); fhirkit at T2 | ADR-0008 (Proposed) reaffirms |
| openEHR bridge | Horizon-3 boundary adapter pattern; never a dual-model core | ADR-0008 (Proposed) |
| OpenEvidence / Medwise | Market references defining the differentiation axis: verifiability + openness | none (no decision) |
| "Research Intelligence" mission | Scope amendment — operator decision required | **ADR-0005 (Proposed)** |
