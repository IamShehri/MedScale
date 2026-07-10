# MedScale Research Blueprint v1.0

> ⚠️ **SUPERSEDED — historical record, do not use.** This early working draft has been
> replaced by the [Strategic Blueprint v1.0](../vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md)
> and the [Research Vision](../vision/MEDSCALE_RESEARCH_VISION.md), and is kept only for
> history. In particular, its "foundation model" framing is **obsolete**: MedScale's
> position is *adapt, don't pretrain* (see [ADR-0004](../adr/0004-t0-foundation-scope.md)
> and the Research Vision). Nothing in this file is authoritative.

> Working Draft

## Vision
Build the world's leading open-source clinical foundation model for FHIR-native reasoning, validation, and healthcare interoperability. MedScale is a long-term research initiative whose AI engine (MESC) will ultimately power the Afia platform.

## Mission
- Develop open foundation models for healthcare.
- Advance clinical reasoning beyond question answering.
- Make FHIR a native reasoning representation.
- Publish open datasets, benchmarks, papers, and tooling.

## Long-Term Objectives
1. MESC Foundation Models
2. MedScale Datasets
3. MedScale Benchmarks
4. FHIR Intelligence Engine
5. Clinical Reasoning Engine
6. Medical Agents
7. Knowledge Graph
8. Afia AI Engine

# Research Program

## Phase 0 – Vision
- Vision
- Mission
- Principles
- Research philosophy
- Branding
- Governance

## Phase 1 – Literature Review
Study:
- Foundation Models
- Medical LLMs
- Reasoning (CoT, ToT, GoT, Reflexion, ReAct, Self-Refine)
- FHIR
- Clinical NLP
- Knowledge Graphs
- Agents
- RAG
- Training (LoRA, QLoRA, DPO, RLHF, MoE)
- Evaluation

Target: 100–150 papers.

## Phase 2 – Model Landscape
Evaluate:
- Llama
- Gemma
- MedGemma
- Qwen
- Mistral
- BioMistral
- Meditron
- OpenBioLLM
- HuatuoGPT
- Phi
- Aya
- DeepSeek

For each:
- Architecture
- License
- Context
- Reasoning
- Clinical capability
- JSON/FHIR support
- Fine-tuning suitability
- Compute requirements

## Phase 3 – Dataset Landscape
Catalog:
- PubMed
- PubMedQA
- MedQA
- MedMCQA
- MIMIC (license permitting)
- SNOMED CT
- LOINC
- RxNorm
- ICD
- UMLS
- FHIR examples
- Clinical notes
- Synthetic data

## Phase 4 – Architecture Research
Compare multiple architectures before implementation.

## Phase 5 – Research Questions
Examples:
- Can an LLM become FHIR-native instead of text-native?
- Can validation be integrated into reasoning?
- Can structured clinical reasoning outperform text-only reasoning?

## Phase 6 – MESC Architecture
Core layers:
- General reasoning
- Biomedical knowledge
- Clinical reasoning
- FHIR reasoning
- Validation
- Evidence retrieval
- Confidence estimation
- Explainability

## Phase 7 – Training
- QLoRA
- PEFT
- Curriculum learning
- Continual learning
- Preference optimization
- Model merging (future)
- Mixture of Experts (future)

## Phase 8 – Evaluation
Measure:
- Clinical correctness
- FHIR validity
- Hallucination
- Explainability
- Benchmark performance
- Human clinician review

## Phase 9 – Publications
Potential papers:
1. MESC: FHIR-Native Clinical Foundation Model
2. MedScale-Bench
3. FHIR Cognitive Reasoning
4. Multi-Agent Clinical Intelligence

## Phase 10 – Open Source
Publish:
- Hugging Face organization
- GitHub organization
- Datasets
- Benchmarks
- Documentation
- Community governance

## Phase 11 – Afia Integration
MESC becomes the AI engine powering:
- Studio
- Nota
- AI Lab
- FHIR Gate
- Clinical workflows

# Deliverables
- Foundation Models
- Datasets
- Benchmarks
- Papers
- Documentation
- APIs
- Training pipelines
- Evaluation framework

# Guiding Principles
- Open science
- Reproducibility
- Clinical safety
- Standards-first (FHIR)
- Evidence-driven design
- Long-term sustainability

# Immediate Next Steps
1. Produce a complete documentation system.
2. Build a literature database.
3. Gather papers using Elicit, SciSpace, Perplexity, Semantic Scholar, and Google Scholar.
4. Review and categorize every paper.
5. Select the base model scientifically.
6. Design MESC before training.
7. Begin experiments on Google Colab with QLoRA.
