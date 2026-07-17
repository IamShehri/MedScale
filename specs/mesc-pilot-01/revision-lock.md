# MESC Pilot-01 — Immutable Revision Lock

Status: **founder-and-ChatGPT approved metadata lock**
Execution authorization: **not granted**
Verification date: 2026-07-17
Authorized scope: documentation-only reconciliation

This file records the immutable revisions for every external,
founder-approved artifact in MESC Pilot-01.

Founder-and-ChatGPT approval is required before any execution boundary
is crossed. Presence in this file does not authorize download,
execution, inference, retrieval, baseline, annotation, training,
adapter creation, production deployment, or clinical use.

Remote metadata retrieval was performed via `git ls-remote refs/heads/main`.
Model weight files, tokenizer files, dataset files, Git LFS objects,
and Xet pods were not retrieved.

Gated repositories that refused anonymous metadata access were
resolved using the founder-approved revisions below. Those revisions
are preserved and marked `FOUNDER-APPROVED`.

---

## Execution-path locks

These are the planned Pilot-01 primary artifacts.
Their presence in this file does not authorize download or execution.

| Role | Repository ID | Immutable revision | License or terms | Gated | Execution status |
|---|---|---|---|---|---|
| Pilot-01 primary training target | `meta-llama/Llama-3.2-3B-Instruct` | `0cb88a4f764b7a12671c53f0838cd831a0843b95` | Llama 3.2 Community License | Yes — HF access request | NOT AUTHORIZED |
| Primary dataset / configuration | `qiaojin/PubMedQA` / `pqa_labeled` | `9001f2853fb87cab8d220904e0de81ac6973b318` | MIT (repository/package metadata) | No (dataset repository) | NOT AUTHORIZED |

Boundaries for execution-path locks:
- The pinned Hugging Face repository commit pins the complete repository
  snapshot, not only `README.md`.
- The pinned snapshot contains the `pqa_labeled` configuration.
- No arbitrary Python dataset loading script is required by the current
  Parquet repository representation.
- The dataset remains undownloaded.
- Raw abstracts must not be committed to MedScale.
- Raw abstracts must not be republished or redistributed by MedScale.
- The MIT repository/package metadata does not transfer publisher
  copyright in underlying abstracts.
- Local research acquisition requires a later explicit authorization.

---

## Reference and fallback locks

These revisions preserve research identity only.
They do not authorize execution or change frozen MESC roles.

| Role | Repository ID | Immutable revision | License or terms | Gated | Execution status |
|---|---|---|---|---|---|
| Low-memory fallback | `meta-llama/Llama-3.2-1B-Instruct` | `9213176726f574b556790deb65791e0c5aa438b6` | Llama 3.2 Community License | Yes — HF access request | NOT AUTHORIZED |
| Clinical specialist | `google/medgemma-1.5-4b-it` | `91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b` | HAI-DEF Terms of Use | Yes — auto-approval after terms acceptance | NOT AUTHORIZED |
| Biomedical specialist | `BioMistral/BioMistral-7B` | `9a11e1ffa817c211cbb52ee1fb312dc6b61b40a5` | Apache-2.0 | No | NOT AUTHORIZED |
| Retrieval | `BAAI/bge-m3` | `5617a9f61b028005a4858fdac845db406aefb181` | MIT | No | NOT AUTHORIZED |
| General external baseline | `Qwen/Qwen3-4B-Instruct-2507` | `cdbee75f17c01a7cc42f958dc650907174af0554` | Apache-2.0 | No | NOT AUTHORIZED |
| Reasoning external baseline | `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` | `ad9f0ae0864d7fbcd1cd905e3c6c5b069cc8b562` | MIT | No | NOT AUTHORIZED |
| Arabic/multilingual comparator | `CohereLabs/aya-expanse-8b` | `5062468bf9bc0c6035fd64e06274333ec127d980` | CC-BY-NC-4.0 | Yes — gated form acceptance | NOT AUTHORIZED |
| Auxiliary validation | `allenai/scifact` / `claims` | `1fe54665deee011033b2dd98db5752e0d586fdfb` | CC BY-NC 2.0 | No (dataset repository) | NOT AUTHORIZED |

Boundaries for SciFact:
- Repository requires arbitrary Python loading-script execution.
- Non-commercial use only.
- This is an auxiliary Evidence Judge validation dataset only.
- It is not promoted to the primary dataset.

---

## Metadata corrections

The following factual corrections were applied to aligned documentation
during this reconciliation pass:

- `BAAI/bge-m3` license corrected to MIT.
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` context length recorded as
  131072 tokens / 128K; parameter size described as 1.5B checkpoint family.
- `google/medgemma-1.5-4b-it` parameter wording normalized to 4.3B reported.
- `CohereLabs/aya-expanse-8b` license normalized to CC-BY-NC-4.0.
- `qiaojin/PubMedQA` immutable revision set to full returned SHA.
- `allenai/scifact` immutable revision set to full returned SHA
  and remote-code-execution / non-commercial boundaries recorded.

---

## Execution boundaries

```text
DATASET DOWNLOADED: NO
MODEL WEIGHTS DOWNLOADED: NO
MODEL INFERENCE EXECUTED: NO
RETRIEVAL EXECUTED: NO
BASELINE EXECUTED: NO
QLORA TRAINING EXECUTED: NO
ADAPTER CREATED: NO
EXECUTION AUTHORIZED: NO
```
