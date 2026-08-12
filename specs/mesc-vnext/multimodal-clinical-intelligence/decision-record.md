# MESC vNext Decision Record

## MESC-VNEXT-1 — Multimodal by Architecture

Multimodality is a first-class MESC capability rather than an attachment
feature. Supported future modality classes include text, documents, images,
medical imaging, audio, video, physiological signals, and longitudinal
structured data. This decision does not authorize implementation of every
modality immediately.

## MESC-VNEXT-2 — Dual-Speed Clinical Intelligence

Separate fast conversational interaction from deeper clinical planning /
reasoning and continuous modality perception where latency or safety requires
separation. Do not mandate separate agents when a simpler component is
sufficient.

## MESC-VNEXT-3 — Typed Clinical Observations

Perceptual or model-derived observations must not exist only as hidden model
context. Introduce a future typed ClinicalObservation contract containing at
minimum: observation identity, modality, clinical concept/value,
source/provenance, confidence/uncertainty, temporal binding, supporting
evidence reference, contradiction state.

## MESC-VNEXT-4 — FHIR-native Longitudinal State

Longitudinal clinical state is a first-class reasoning input. FHIR remains the
canonical interoperability boundary. Multimodal perception does not replace
structured longitudinal clinical state.

## MESC-VNEXT-5 — Active Information Acquisition

MESC may reason about what information is missing and propose the next useful
clinical information action. Future InformationNeed / NextBestClinicalAction
objects may represent: follow-up question, physical observation, image request,
audio request, video examination, laboratory test, imaging study,
guideline/evidence lookup, clinician escalation. The planner must represent
expected value, uncertainty reduction, risk, cost, latency, authority
requirements.

## MESC-VNEXT-6 — Explicit Uncertainty and Abstention

Every clinical intelligence layer must preserve uncertainty. MESC must support
known, uncertain, conflicting, insufficient evidence, out-of-domain, and
requires-human-review states. Abstention is a valid clinical action.

## MESC-VNEXT-7 — Clinician Authority

MESC does not obtain autonomous clinical authority merely because the system
becomes multimodal. Clinician oversight remains a first-class contract. The
system must distinguish observation, suggestion, recommendation, authorization,
and execution.

## MESC-VNEXT-8 — Evaluation-First Multimodal Development

New clinical modalities are not considered mature because a model accepts them.
Each modality/capability requires explicit evaluation. Future benchmark families
should include: text clinical reasoning, active history taking, medical image
interpretation, audio consultation, real-time video consultation, longitudinal
disease management, information-seeking quality, evidence grounding, FHIR
reasoning, uncertainty calibration, abstention, clinician oversight,
communication/rapport, cost, latency, worst-case safety.

## MESC-VNEXT-9 — Model Agnosticism

No single model family defines MESC architecture. MedGemma, MedASR,
Gemini-derived research systems, or other permitted models may serve as
reference or optional backends. Backends remain replaceable. Existing MESC model
restrictions remain unchanged.

## MESC-VNEXT-10 — Agent Minimalism

Do not use multiple agents merely because multi-agent architecture is
fashionable. Create separate agents/processes only when justified by at least
one of: latency isolation, modality specialization, authority separation,
security boundary, independent verification, measured quality improvement,
measured reliability improvement. Prefer the simplest architecture that
preserves the required clinical contract.