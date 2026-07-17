# MESC Pilot-01 — P01-03 Data Model

Status: **planning data model**
Authorization: P01-03 planning authorized; execution not authorized
Freeze date: 2026-07-17

---

## Native PubMedQA field model

The native `qiaojin/PubMedQA` `pqa_labeled` Parquet representation exposes at least the following columns:

| Native field | Meaning | Notes |
|---|---|---|
| `pubid` | PubMed publication identifier | Used as source-document anchor; must be present and well-formed |
| `question` | Research question | Native gold text |
| `context` | JSON-formatted list of abstract snippets | Native evidence proxy; not sentence-level gold rationale |
| `long_answer` | Full explanatory answer | Native gold answer text |
| `final_decision` | Categorical label | Native gold label; allowed values: `yes`, `no`, `maybe` |

### Native limitations

- No atomic gold claims.
- No sentence-level gold evidence rationales.
- No native abstention labels.
- No native gold evidence-sufficiency labels.
- No native gold uncertainty labels.

Any downstream field that depends on these missing annotations must be marked unavailable or explicitly deferred to manual annotation.

---

## Proposed normalized source record — `PilotPubMedQASourceRecord`

This internal representation is not a public contract root. It exists to keep native labels separate from derived or manual annotations.

```text
schema_version: "mesc-pilot-01/1"
dataset_id: str
dataset_revision: str
configuration: str
original_example_id: str
source_document_id: str
pubid: str
question: str
context: tuple[str, ...]
long_answer: str
final_decision: str
license_id: str
```

Fields `dataset_id`, `dataset_revision`, `configuration`, `original_example_id`, `source_document_id`, `pubid`, `question`, `context`, `long_answer`, `final_decision`, and `license_id` are populated from native data or revision metadata only. No annotation fields are present.

---

## PilotRecord mapping

Full `PilotRecord` construction requires manual annotation for unavailable fields. The mapping below records the boundary precisely.

| PilotRecord field | Source | Status |
|---|---|---|
| `schema_version` | fixed to `mesc-pilot-01/1` | native metadata |
| `example_id` | derived payload (see `execution-protocol.md`) | derived |
| `source.dataset_id` | `qiaojin/PubMedQA` | native metadata |
| `source.dataset_revision` | pinned revision | native metadata |
| `source.configuration` | `pqa_labeled` | native metadata |
| `source.original_example_id` | stable native identifier or fallback locator | derived |
| `source.source_document_id` | normalized `pubid` | derived |
| `source.license_id` | `PubMedQA-PQA-L` | derived |
| `question` | native `question` | native |
| `evidence[].text` | native `context` entries | native but normalized |
| `evidence[].evidence_id` | deterministic derivation | derived |
| `evidence[].sentence_index` | ordinal in normalized context list | derived |
| `evidence[].source_document_id` | same as `source.source_document_id` | derived |
| `target.decision` | native `final_decision` | native gold |
| `target.answer` | native `long_answer` | native |
| `target.claims` | unavailable until manual annotation | unavailable |
| `target.evidence_sufficiency` | unavailable until manual annotation | unavailable |
| `target.uncertainty` | unavailable until manual annotation | unavailable |
| `target.abstain` | unavailable as native gold; false in Layer 1 | unavailable |
| `target.abstention_reason` | unavailable until manual annotation | unavailable |
| `provenance.transformation_version` | transformation protocol version | derived |
| `provenance.annotation_method` | `native`, `derived`, or `manual` | mixed |
| `provenance.annotation_revision` | annotation protocol version or empty | derived |
| `provenance.synthetic` | false for real data | derived |

---

## Scientific identity fields

These fields define record identity and appear in `content_hash`:

```text
schema_version
example_id
source.dataset_id
source.dataset_revision
source.configuration
source.original_example_id
source.source_document_id
source.license_id
question
evidence[].evidence_id
evidence[].sentence_index
evidence[].text
evidence[].source_document_id
target.decision
target.answer
target.claims
target.evidence_sufficiency
target.uncertainty
target.abstain
target.abstention_reason
provenance.transformation_version
provenance.annotation_method
provenance.annotation_revision
provenance.synthetic
```

## Operational provenance fields

Operational provenance supports auditability but does not change scientific identity:

```text
acquired_at
source_url
artifact_path
artifact_size
sha256
acquisition_method
tool_version
environment_identity
```

These fields are recorded in the acquisition manifest and transformation report, not in `content_hash`.

---

## Unavailable annotation fields

The following fields are unavailable for native PubMedQA rows until a separately authorized annotation protocol supplies them:

```text
claims: []
evidence_sufficiency: "not_annotated"
uncertainty: "not_annotated"
abstain: false
abstention_reason: null
```

When manual annotation is later authorized, these fields transition from `not_annotated` / empty to annotated values under a documented annotation revision.

---

## Excluded fields

The following must never appear in `PilotRecord` or normalized source records:

```text
runtime timestamps
local filesystem paths
hostnames
runtime durations
hardware identifiers
split assignments
annotation UI state
raw abstract redistribution payloads
full article text
```

---

## Serialization shapes

- Canonical serialization: JSON with deterministic key ordering, UTF-8 encoding, no pretty-printing.
- External storage format: JSONL, one `PilotRecord` per line.
- Acquisition manifest: JSON with explicit schema version.
- Transformation report: JSON with per-record validation status.
- All serialized forms must be byte-identical when inputs and transformation version are identical.

---

## Versioning policy

- `schema_version` increments require explicit authorization and must propagate to serialization, hashing, and fixture validation.
- `transformation_version` increments require explicit authorization and must trigger re-derivation of `example_id` and `content_hash`.
- Annotation revisions track manual annotation protocol versions; they do not change `example_id` or `content_hash` unless the transformation version also changes.
