# MESC Pilot-01 — Data Contract

Status: **foundation data contract**
Authorization: Foundation *** only
Freeze date: 2026-07-17

---

## Record identity

The Pilot-01 record schema defines scientific identity through `PilotSourceIdentity`, `PilotEvidence`, `PilotClaim`, `PilotTarget`, `PilotProvenance`, and `PilotRecord`. These objects must remain stable across split assignments and runtime environments.

---

## `PilotSourceIdentity`

Fields:

- `dataset_id`
- `dataset_revision`
- `configuration`
- `original_example_id`
- `source_document_id`
- `license_id`

`dataset_revision` must be pinned to an immutable revision identifier before execution. `source_document_id` links the record to its source document for deterministic grouping.

---

## `PilotEvidence`

Fields:

- `evidence_id`
- `sentence_index`
- `text`
- `source_document_id`

Evidence objects are short, synthetic, or extracted abstracts. They must not contain full copyrighted article passages in foundation documentation or fixtures.

---

## `PilotClaim`

Fields:

- `claim_id`
- `text`
- `evidence_ids`
- `annotation_status`

`annotation_status` distinguishes gold annotations from derived or predicted annotations. Manual gold annotations are required before Layer 2 metrics are treated as ground truth.

---

## `PilotTarget`

Fields:

- `decision`
- `answer`
- `claims`
- `evidence_sufficiency`
- `uncertainty`
- `abstain`
- `abstention_reason`

`decision` enum values: `yes`, `no`, `maybe`, `abstain`.

`evidence_sufficiency` enum values: `sufficient`, `insufficient`, `ambiguous`.

`uncertainty` enum values: `low`, `medium`, `high`.

`abstain` is true when evidence is insufficient or ambiguous. `abstention_reason` must be non-empty when `abstain` is true.

---

## `PilotProvenance`

Fields:

- `transformation_version`
- `annotation_method`
- `annotation_revision`
- `synthetic`

`synthetic` indicates test-only provenance. Synthetic provenance does not automatically imply abstention in answerable examples.

---

## `PilotRecord`

Fields:

- `schema_version`
- `example_id`
- `source`
- `question`
- `evidence`
- `target`
- `provenance`

`schema_version` is immutable across the foundation. `example_id` is derived from dataset identity, original example ID, transformation version, and source document ID. `content_hash` is computed over scientific identity fields only.

---

## `example_id`

`example_id` must be unique within a pinned dataset revision. `example_id` must be re-derived when the pinned revision changes.

---

## `content_hash`

`content_hash` is computed over scientific identity fields excluding runtime timestamps, local paths, hardware identifiers, and execution duration. It is deterministic and stable under repeated evaluation.

---

## Split manifest separation

Split assignment is external to `PilotRecord` scientific identity. Changing split assignment must not affect `PilotRecord.content_hash`. Split metadata lives in `PilotSplitManifest` and `PilotSplitAssignment`.

---

## Abstention consistency

Abstention requires explicit evidence conditions. Synthetic provenance alone does not force abstention. Missing abstention reasons or invalid sufficiency states are contract violations.

---

## Enum values

Allowed enum values are explicit and typed. Invalid enum values must be rejected at construction time when runtime validation is enforced.

---

## Failure behavior

Invalid records must fail fast with explicit errors when runtime validation is enabled. Fallback defaults must not silently corrupt scientific identity.

---

## Schema versioning

Schema version changes require explicit authorization. Version increments must propagate to serialization, hashing, and fixture validation.
