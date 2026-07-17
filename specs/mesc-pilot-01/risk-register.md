# MESC Pilot-01 — Risk Register

Status: **foundation risk register**
Authorization: Foundation *** only
Freeze date: 2026-07-17

---

## Risk record format

Each risk record includes:

- ID
- description
- severity
- likelihood
- mitigation
- verification
- stop condition
- owner
- status

---

## RSK-01 — Dataset-package licensing

- description: PubMedQA package license may not cover all downstream uses or redistribution contexts.
- severity: medium
- likelihood: low
- mitigation: record exact package license and dataset README terms before execution.
- verification: inspect dataset card and license metadata; record findings in `dataset-selection.md`.
- stop condition: unresolved license review before acquisition.
- owner: Hermes verification
- status: OPEN

---

## RSK-02 — Underlying abstract rights

- description: PubMed abstracts may carry publisher-specific restrictions beyond the dataset package license.
- severity: medium
- likelihood: medium
- mitigation: use abstracts only; do not assert full-text rights; consult PubMed/NIH policies.
- verification: add explicit rights caveat to `data-contract.md` and foundation documentation.
- stop condition: full-text use without documented rights.
- owner: Hermes verification
- status: DOCUMENTED

---

## RSK-03 — Benchmark contamination

- description: PubMedQA questions or abstracts may appear in training data or public benchmarks, inflating scores.
- severity: high
- likelihood: medium
- mitigation: treat PubMedQA as a labeled benchmark; do not claim held-out generalization beyond documented scope.
- verification: document PubMedQA role and split provenance in acceptance criteria.
- stop condition: held-out generalization claimed without contamination analysis.
- owner: Hermes verification
- status: DOCUMENTED

---

## RSK-04 — Source-document leakage

- description: records sharing source documents may leak across splits if grouping is ignored.
- severity: high
- likelihood: medium
- mitigation: enforce source-document-grouped deterministic splitting; leakage audit before evaluation.
- verification: leakage audit reports findings; split enforcement tests pass.
- stop condition: evaluation runs without leakage audit.
- owner: implementation and verification
- status: OPEN

---

## RSK-05 — Near-duplicate leakage

- description: character or semantic near-duplicates may bleed across splits regardless of source-document grouping.
- severity: high
- likelihood: medium
- mitigation: character 3-gram Jaccard near-duplicate detection with threshold 0.6; cross-split findings reported.
- verification: leakage audit includes near-duplicate findings; threshold documented.
- stop condition: near-duplicate evidence ignored in audit output.
- owner: implementation and verification
- status: OPEN

---

## RSK-06 — Weak claim annotations

- description: weak or inconsistent claim annotations undermine Layer 2 metric reliability.
- severity: high
- likelihood: high
- mitigation: manual review protocol for gold subset; annotation status field distinguishes gold from derived.
- verification: gold-subset protocol present; Layer 2 metrics gated.
- stop condition: Layer 2 metrics without gold subset.
- owner: manual review process
- status: OPEN

---

## RSK-07 — Synthetic-example bias

- description: synthetic smoke fixtures may encode assumptions that do not generalize to real data.
- severity: medium
- likelihood: medium
- mitigation: keep synthetic fixtures small and explicitly test-only; never claim synthetic metrics as production evidence.
- verification: synthetic provenance explicit; no experimental results claimed from fixtures.
- stop condition: synthetic fixture used as benchmark evidence.
- owner: implementation and verification
- status: DOCUMENTED

---

## RSK-08 — Citation errors

- description: predicted evidence IDs may reference nonexistent or mismatched evidence objects.
- severity: medium
- likelihood: medium
- mitigation: evidence-reference validity metric; claim-to-evidence references validated in fixtures and tests.
- verification: contract tests enforce valid references; metric reports invalid rate.
- stop condition: citation errors ignored in evaluation output.
- owner: implementation and verification
- status: OPEN

---

## RSK-09 — Unsupported claims

- description: predicted claims may lack supporting evidence, leading to false precision.
- severity: medium
- likelihood: medium
- mitigation: supported-claim metrics; unsupported-claim rate reported explicitly.
- verification: evaluation contract defines unsupported-claim rate; tests cover empty evidence cases.
- stop condition: unsupported claims treated as supported.
- owner: implementation and verification
- status: OPEN

---

## RSK-10 — Abstention-label quality

- description: abstention labels may be noisy, inconsistent, or overused.
- severity: medium
- likelihood: medium
- mitigation: explicit abstention fields; abstention precision/recall metrics; abstention consistency rules in fixtures and contracts.
- verification: abstention tests enforce consistency; reports include precision/recall.
- stop condition: abstention used without evidence-condition checks.
- owner: implementation and verification
- status: OPEN

---

## RSK-11 — Uncertainty-calibration failure

- description: uncertainty labels may not reflect true decision confidence.
- severity: medium
- likelihood: medium
- mitigation: uncertainty field required; calibration analysis deferred to later phases with gold data.
- verification: contract includes uncertainty enum; calibration not claimed in foundation.
- stop condition: calibration claims made without gold-subject analysis.
- owner: future phase
- status: DEFERRED

---

## RSK-12 — Model-license restrictions

- description: Llama 3.2, MedGemma, and other models carry license or access restrictions.
- severity: high
- likelihood: medium
- mitigation: license terms documented in `model-selection.md`; gated access recorded before execution.
- verification: model-selection spec records exact terms; no execution without documented acceptance.
- stop condition: model access attempted without documented license acceptance.
- owner: Hermes verification
- status: DOCUMENTED

---

## RSK-13 — Gated-model access

- description: MedGemma and Llama 3.2 require gated Hugging Face access or Health AI terms acceptance.
- severity: high
- likelihood: medium
- mitigation: record exact access requirements; separate authorization for gated access.
- verification: access requirements documented; no download without explicit authorization.
- stop condition: gated access performed without authorization record.
- owner: Hermes verification
- status: DOCUMENTED

---

## RSK-14 — Colab OOM

- description: Colab runtime may run out of memory during feasibility smoke runs or QLoRA training.
- severity: high
- likelihood: medium
- mitigation: low-memory fallback documented; memory usage recorded; OOM stop condition explicit.
- verification: Colab feasibility plan records memory thresholds; fallback decision required.
- stop condition: OOM handled without fallback decision record.
- owner: future phase
- status: DEFERRED

---

## RSK-15 — Colab disconnection

- description: Colab runtime may disconnect during long-running experiments.
- severity: medium
- likelihood: medium
- mitigation: checkpoint and resume protocol; run manifests capture partial state.
- verification: Colab feasibility plan includes disconnection handling; no silent state loss accepted.
- stop condition: disconnected runs treated as complete without verification.
- owner: future phase
- status: DEFERRED

---

## RSK-16 — Dependency drift

- description: library updates may change behavior or break reproducibility.
- severity: medium
- likelihood: medium
- mitigation: lock dependency versions; record exact environment in manifests; avoid silent upgrades.
- verification: `uv.lock` and `pyproject.toml` recorded; no dependency changes without authorization.
- stop condition: dependency changed without manifest update.
- owner: Hermes verification
- status: DOCUMENTED

---

## RSK-17 — Revision drift

- description: dataset or model revisions may change after foundation contracts are frozen.
- severity: high
- likelihood: medium
- mitigation: immutable revision strategy; pin exact revisions before execution; re-derive identifiers on revision change.
- verification: revision fields present in contracts; split and content hashes recomputed on revision change.
- stop condition: revision change without recomputed identifiers.
- owner: implementation and verification
- status: OPEN

---

## RSK-18 — Judge bias

- description: Evidence Judge may inherit training or prompt bias that distorts citation correctness.
- severity: medium
- likelihood: medium
- mitigation: validate judge against manual gold annotations; document bias in judge validation report.
- verification: judge validation phase includes bias analysis; no judge treated as ground truth.
- stop condition: judge results replace manual review without bias analysis.
- owner: future phase
- status: DEFERRED

---

## RSK-19 — Overclaiming

- description: experimental results or model outputs may be overstated in documentation or claims.
- severity: high
- likelihood: medium
- mitigation: explicit authorization boundaries; publication and clinical-use restrictions; no experimental result claims in foundation.
- verification: acceptance criteria and governance statements explicitly limit claims.
- stop condition: foundation or documentation overstates capability or scope.
- owner: Hermes verification
- status: DOCUMENTED

---

## RSK-20 — Clinical misuse

- description: biomedical QA outputs may be misused for clinical decision support or patient care.
- severity: high
- likelihood: low
- mitigation: explicit non-clinical scope; non-production restriction; no clinical-use authorization.
- verification: acceptance criteria and all public docs state non-clinical and non-production scope.
- stop condition: any clinical-use authorization or implicit clinical routing.
- owner: Hermes verification
- status: DOCUMENTED
