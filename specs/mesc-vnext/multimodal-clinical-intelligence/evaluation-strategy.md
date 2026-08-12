# MESC vNext Evaluation Strategy

## Evaluation-first principle

New clinical modalities are not considered mature because a model accepts them.
Each modality and capability requires explicit evaluation before being
considered production-ready.

## Future benchmark families

| Family | Focus |
|--------|-------|
| Text clinical reasoning | Core clinical QA, differential reasoning, safety |
| Active history taking | Information-seeking quality, expected-value reasoning |
| Medical image interpretation | Radiology, pathology, multimodal image grounding |
| Audio consultation | Medical ASR, consultation quality, rapport |
| Real-time video consultation | Live multimodal interaction, latency, safety |
| Longitudinal disease management | FHIR-native state, temporal reasoning, care plans |
| Information-seeking quality | Next-best-action selection, cost-aware planning |
| Evidence grounding | Provenance, citation accuracy, contradiction detection |
| FHIR reasoning | Resource navigation, constraint satisfaction, interoperability |
| Uncertainty calibration | Confidence-accuracy correlation, abstention triggers |
| Abstention | Appropriate refusal, out-of-domain detection, safe handoff |
| Clinician oversight | Authority handoff, cockpit interaction, escalation |
| Communication / rapport | Patient-facing interaction quality, empathy, clarity |
| Cost | Token/compute budget, routing efficiency, modality cost |
| Latency | Response time budgets, fast-loop vs. deep-planning separation |
| Worst-case safety | Adversarial inputs, missing modalities, contradiction storms |

## Reproducibility

All evaluation results must be reproducible from canonical artifacts. The
MESC reproducibility contract from P01-04 extends to multimodal evaluation:
deterministic serialization, identity-bound artifacts, no runtime metadata in
promoted outputs.