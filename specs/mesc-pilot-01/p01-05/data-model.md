# MESC Pilot-01 — P01-05 Data Model

Status: **prospective deterministic contracts**

Authorization: Entry *** defined — real execution not authorized

---

## Purpose

Define deterministic prospective contracts for B0/B1 runner outputs.

Preserve existing B0 structures where they are already equivalent. Do not create duplicate contracts solely for naming symmetry. Document equivalence where appropriate.

---

## B0 contracts

The existing B0 implementation already defines the following contracts in `src/medscale/mesc/_b0.py`:

- `B0Config`
- `B0RuntimeManifest`
- `B0Prediction`
- `B0ExampleScore`
- `B0Aggregate`
- `B0Report`

These are reconciled, not redefined, in this phase. P01-05 adopts them as the canonical B0 data-model truth.

### B0Config

Deterministic experiment configuration for B0.

Fields:

- `experiment_version`
- `model_id`
- `model_revision`
- `tokenizer_revision`
- `max_new_tokens`
- `seed`
- `experiment_id`
- `prompt_template_version`
- `evidence_condition`

Validation enforces:

- approved model allowlist
- immutable 40-hex commit SHAs for model and tokenizer revisions
- fixed prompt template version
- fixed evidence condition (`"none"`)
- positive `max_new_tokens`
- non-negative `seed`

### B0RuntimeManifest

Reproducibility manifest. Every field enters the canonical digest.

Fields:

- `code_commit`
- `python_version`
- `medscale_version`
- `transformers_version`
- `torch_version`
- `tokenizers_version`
- `huggingface_hub_version`
- `safetensors_version`
- `model_revision`
- `tokenizer_revision`
- `device`
- `dtype`
- `quantization`
- `seed`
- `prompt_template_version`
- `evidence_condition`

### B0Prediction

One example-level prediction record.

Fields:

- `example_id`
- `row_ordinal`
- `prompt_sha256`
- `raw_output`
- `raw_output_sha256`
- `predicted_decision`
- `parse_state`

`parse_state` is one of:

- `parsed`
- `unparseable`
- `ambiguous`
- `generation_failed`

### B0ExampleScore

One example-level score record, used for evaluation only.

Fields:

- `example_id`
- `gold_decision`
- `predicted_decision`
- `parse_state`
- `correct`

The gold decision is retained structurally separate from the prompt-facing fields and is used for scoring only.

### B0Aggregate

Dataset-level aggregate.

Fields:

- `total`
- `parsed_count`
- `unparseable_count`
- `ambiguous_count`
- `generation_failed_count`
- `correct_count`
- `predicted_distribution`
- `gold_distribution`

Derived properties:

- `accuracy`
- `coverage`

### B0Report

Full run output.

Fields:

- `run_id`
- `run_digest`
- `config`
- `manifest`
- `input_sha256`
- `input_size`
- `predictions`
- `scores`
- `aggregate`

---

## B1 prospective contracts

B1 uses the same deterministic execution discipline as B0. The same base-model family, frozen split, example identities, gold-decision isolation, abstention policy, and deterministic execution discipline apply.

B1 differs from B0 ONLY by an explicit additional evidence input channel.

### B1Config prospective contract

B1Config is the counterpart of B0Config. It reuses the same base fields and binds an immutable run-level evidence-pack identity.

Because a B1 run consumes a multi-example evidence pack, the earlier prospective singular `evidence_reference` wording is reconciled to a run-level evidence-pack identity. The reconciled fields are:

- All B0Config fields
- `evidence_pack_sha256`: `str`
- `evidence_pack_size`: `int`
- `evidence_schema_version`: `"mesc-pilot-01-b1-evidence-pack/1"`
- `annotation_protocol_version`: `"mesc-pilot-01-b1-annotation/1"`
- `subset_digest`: `str`

Validation must enforce that the evidence condition reflects the presence of a valid supplied evidence pack, and that no retrieval channel is smuggled in. The ratified per-cue record contract `mesc-pilot-01-b1-evidence-cue/1` (FD-P01-05-B1-EVIDENCE-1) supersedes the earlier prospective `SuppliedEvidenceReference` shape below for cue-level identity.

### B1RuntimeManifest prospective contract

B1RuntimeManifest reuses the B0RuntimeManifest shape and adds an explicit evidence-condition field that records the supplied evidence-pack identity rather than `"none"`.

### B1Prediction prospective contract

B1Prediction reuses the B0Prediction shape. The prompt builder includes the supplied evidence reference content/reference according to the B1 prompt contract. Parse states are unchanged.

### B1ExampleScore prospective contract

B1ExampleScore reuses the B0ExampleScore shape. Gold-decision isolation is unchanged.

### B1Aggregate prospective contract

B1Aggregate reuses the B0Aggregate shape.

### B1Report prospective contract

B1Report reuses the B0Report shape.

---

## SuppliedEvidenceReference

A minimal supplied-evidence object suitable for B1 is a versioned private contract conceptually containing:

- `schema_version`
- `evidence_id`
- `example_id`
- `source_document_id`
- `evidence_type`
- `content_reference`
- `content_sha256`
- `provenance`
- `availability`

Do NOT persist copyrighted raw scientific content merely to satisfy this schema. The exact contract may use stable references to already-authorized content.

No fabricated evidence. No teacher-generated evidence. No LLM-generated gold. No retrieval-generated evidence in B1.

---

## Equivalence notes

Where B1 contracts reuse B0 shapes, document the equivalence rather than duplicating the contract.

- B1Config ≡ B0Config + run-level evidence-pack identity
- B1RuntimeManifest ≡ B0RuntimeManifest + evidence-condition recording
- B1Prediction ≡ B0Prediction
- B1ExampleScore ≡ B0ExampleScore
- B1Aggregate ≡ B0Aggregate
- B1Report ≡ B0Report

---

## Gold-decision isolation

The gold/final decision must remain structurally separate from the prompt-facing fields for both B0 and B1. It is used for scoring only and must never leak into a model prompt.

---

## Input identity

The input dataset contract is defined by `B0InputDataset` and `B0InputRecord` in `src/medscale/mesc/_pilot_loader.py`. The input SHA-256 and input size are recorded on `B0InputDataset` and propagated through `B0Report`; they are NOT fields on `B0RuntimeManifest`. B1 reuses the same frozen split and example identities.

---

## Serialization

B0 reports are written as deterministic JSON via `write_b0_report`. The canonical payload is hashed to produce the run digest. B1 must preserve the same deterministic serialization discipline.
