# MESC Pilot-01 — Specification

Status: **foundation spec**
Authorization: Foundation implementation only
Freeze date: 2026-07-17

---

## Pilot purpose

MESC Pilot-01 defines the deterministic foundation for a multi-model experimental ecosystem that evaluates biomedical question answering with explicit evidence grounding, abstention, and provenance controls.

The primary research question is whether bounded evidence-grounded generation improves decision accuracy and abstention quality for PubMed-style biomedical QA without weakening scientific identity or leakage controls.

The Pilot-01 package is a bounded component of the larger MESC ecosystem. It does not define the full ecosystem; it provides the contracts, splits, manifests, metrics, and frozen selection needed to execute later phases under separate authorization.

---

## Multi-model ecosystem constraint

The MESC ecosystem is multi-model by design. The Pilot model is only one bounded component. Future phases may compare core reasoning, clinical specialists, biomedical specialists, retrieval rerankers, external baselines, and judges. Collapsing this package to a single-model path is not permitted.

---

## Frozen architecture boundaries

These boundaries are not open to reinterpretation in this turn.

```text
MESC GENERAL REASONING CORE FAMILY: LLAMA

PILOT-01 PRIMARY TRAINING TARGET: meta-llama/Llama-3.2-3B-Instruct
LOW-MEMORY FALLBACK: meta-llama/Llama-3.2-1B-Instruct
CLINICAL SPECIALIST: google/medgemma-1.5-4b-it
BIOMEDICAL AND LITERATURE SPECIALIST: BioMistral/BioMistral-7B
RETRIEVAL: BAAI/bge-m3
EVIDENCE VERIFICATION: MedScale-native Evidence Judge
GENERAL EXTERNAL BASELINE: Qwen/Qwen3-4B-Instruct-2507
REASONING EXTERNAL BASELINE: deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
MULTILINGUAL AND ARABIC FUTURE COMPARATOR: CohereLabs/aya-expanse-8b
```

Model selection authority is recorded in `model-selection.md`. Hermes authority is repository implementation and verification only.

---

## Dataset boundaries

Primary dataset: `qiaojin/PubMedQA`, configuration `pqa_labeled`, subset PQA-L.

SciFact is documented as optional auxiliary Evidence Judge validation data. It is not the primary dataset.

```text
DATASET DOWNLOADED: NO
MODEL WEIGHTS DOWNLOADED: NO
```

---

## B0–B3 definitions

```text
B0 — Llama 3.2 3B without supplied evidence
B1 — Llama 3.2 3B with supplied evidence
B2 — QLoRA-adapted Llama 3.2 3B without supplied evidence
B3 — QLoRA-adapted Llama 3.2 3B with supplied evidence
```

B0–B3 are definitions only. Definitions do not imply execution.

---

## Evidence-grounding subset

A manually reviewed 100-example gold subset is required before claim-support metrics are treated as gold. Missing gold annotations must produce `status: not_applicable` for Layer 2 metrics. No gold annotations were created in this turn.

---

## Success criteria

- All required foundation files present and non-empty.
- All required contracts implemented and type-checked.
- Architecture registration complete and enforcement preserved.
- Deterministic serialization, hashing, and split reproducibility verified.
- Leakage audit report contract present and serializable.
- Smoke fixture covers required answer classes and abstention semantics.
- Full Pytest passes.
- Mypy passes.
- Ruff passes.
- Format check passes.
- `git diff --check` passes.
- Staging remains empty.
- No dataset, weights, inference, baseline, training, publication, clinical use, or production use occurs.

## Exclusions

- Clinical use is excluded.
- Production use is excluded.
- No experimental result claims are made in the foundation package.
- Do not modify frozen model selections.
- Do not execute inference, retrieval, baselines, or training without separate authorization.
