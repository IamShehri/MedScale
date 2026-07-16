# MESC Pilot-01 — Dataset Selection

Status: **frozen dataset decision**
Authorized by: Founder and ChatGPT
Hermes role: implementation and verification only
Verification date: 2026-07-16

---

## Primary dataset decision

```text
PubMedQA PQA-L
```

### Exact source and configuration

- Dataset: `qiaojin/PubMedQA`
- Configuration: `pqa_labeled`
- Primary split/task subset: PQA-L expert-labeled records
- Homepage: pubmedqa.github.io
- Paper: PubMedQA: A Dataset for Biomedical Research Question Answering, arXiv:1909.06146
- Official source for Hugging Face metadata: https://huggingface.co/datasets/qiaojin/PubMedQA

### Expert-labeled record count

Official Hugging Face dataset meta lists `pqa_labeled` as 1k rows.
The official test set documented on the dataset page and literature is the 500 manually labeled questions from `pqa_labeled` used for official benchmark evaluation.

### Package license

External primary source evidence: the `qiaojin/PubMedQA` dataset card metadata retrieved on 2026-07-16 lists `license: mit` in the dataset repository metadata.

### Underlying document-rights caveat

The dataset is constructed from PubMed abstracts.
PubMed abstracts are bibliographic metadata, not full article text.
Article-level PDF or full-text rights are not transferred by this dataset package.
Redistribution or use of extracted abstracts remains subject to the underlying PubMed/NIH data-access policies and any publisher-specific restrictions for the cited article body; this record does not assert full-text rights.
An immutable revision strategy must be adopted before execution to freeze the dataset revision as `pqa-labeled-immutable` or another exact pinned revision and to re-derive all `example_id` values when the pinned revision changes.

### Source identifiers

- `pubid`: PubMed publication identifier
- `original_example_id`: original example identifier from the dataset split
- `example_id` in scientific contracts is derived from dataset ID, dataset revision, configuration, original example ID, and transformation version

### Available evidence context

- `question`: research question
- `context`: JSON-formatted list of extracted abstract snippets from the corresponding PubMed paper
- `long_answer`: full explanatory answer derived from the paper abstract
- `final_decision`: categorical answer label `yes`, `no`, or `maybe`

The dataset does not natively provide atomic claims or sentence-level gold evidence rationales.
A manually reviewed evidence-grounding subset is required before claim-support metrics can be treated as gold.
No gold annotations were created in this turn.

### Answer-label structure

- Supported classes: `yes`, `no`, `maybe`
- `abstain` is added by the MESC Pilot-01 contract as a fifth target decision, gated by evidence sufficiency and abstention reason.

### Immutable revision strategy

- Pin dataset revision to `pqa-labeled-immutable` or another operator-assigned exact revision identifier.
- Record dataset revision in `PilotSourceIdentity.dataset_revision`.
- Recompute `example_id` and `content_hash` whenever the pinned revision changes.
- Do not download the dataset in this turn.

---

## SciFact auxiliary validation dataset

Exact dataset: `allenai/scifact`
Exact official page: https://huggingface.co/datasets/allenai/scifact
Role: optional auxiliary Evidence Judge validation dataset; not the primary dataset.
License: CC BY-NC 2.0
Restrictions: non-commercial use only; attribution required.
Size: 1.4k expert-written scientific claims paired with evidence-containing abstracts.
Splits: Claims 1261/450/300; Corpus 5183 train.
This turn status: not downloaded; used only for documentation and future validation planning.
Do not execute retrieval, baseline, evaluation, or training on SciFact in this turn without explicit authorization.

```text
SCIFACT AUXILIARY DATASET: NOT AUTHORIZED FOR EXECUTION IN THIS TURN
```

---

## Honesty limits

```text
DATASET DOWNLOADED: NO
MODEL WEIGHTS DOWNLOADED: NO
MODEL INFERENCE EXECUTED: NO
RETRIEVAL EXECUTED: NO
BASELINE EXECUTED: NO
QLORA TRAINING EXECUTED: NO
ADAPTER CREATED: NO
EXPERIMENTAL RESULTS CLAIMED: NO
```
