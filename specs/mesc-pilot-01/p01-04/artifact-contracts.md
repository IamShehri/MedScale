# MESC Pilot-01 — P01-04 Artifact Contracts

Status: **specification and policy only — no execution authorized**

This document defines the proposed stable artifact schemas and external-evidence-only records for P01-04. No real split artifacts are created during P01-04A. No real partition membership is created or disclosed.

## Stable promotable artifacts

The following artifacts are candidates for repository promotion after successful formal execution and separate promotion authorization:

### 1. `split-policy.json`

| Field | Type | Purpose |
|-------|------|---------|
| `policy_id` | string | Stable identifier |
| `algorithm_version` | string | e.g. `mesc-pilot-01-split-algorithm/1` |
| `grouping_key` | string | `source_document_id` |
| `stratification_field` | string | `decision` |
| `partitions` | array of strings | e.g. `["train", "validation", "test"]` |
| `target_counts` | object | partition name -> integer count |
| `target_ratios` | object | partition name -> float ratio (informative) |
| `holdout_included` | boolean | false for version 1 |
| `minimum_sizes` | object | partition name -> minimum count |
| `rank_key_schema` | object | canonical ranking key definition |
| `serialization_rules` | object | encoding, separators, ensure_ascii, allow_nan |
| `apportionment_method` | string | description of constrained apportionment |
| `ratified_at` | string | ISO date of ratification (no timestamp) |

Promotable. Must not contain runtime timestamps, local paths, usernames, hostnames, or command logs.

### 2. `group-registry.jsonl`

One JSON object per source-document group, one line per object. Fields:

| Field | Type | Purpose |
|-------|------|---------|
| `group_id` | string | Stable group identifier |
| `source_document_id` | string | Source document identifier |
| `example_count` | integer | Number of examples in this group |
| `row_ordinals` | array of integers | Row ordinals in this group |
| `assigned_split` | string | `train`, `validation`, or `test` |
| `partition_key` | string | Deterministic partition key |

Serialized in order: `(assigned_split, group_id)` ascending. Sorted keys. UTF-8. No BOM.

Promotable. Must not contain question text, context text, or labels.

### 3. `example-split-registry.jsonl`

One JSON object per example, one line per object. Fields:

| Field | Type | Purpose |
|-------|------|---------|
| `example_id` | string | Stable example identifier |
| `source_document_id` | string | Source document identifier |
| `row_ordinal` | integer | Row ordinal in ordered registry |
| `assigned_split` | string | `train`, `validation`, or `test` |
| `partition_key` | string | Deterministic partition key |

Serialized in order: `(assigned_split, row_ordinal)` ascending. Sorted keys. UTF-8. No BOM.

Promotable. Must not contain question text, context text, or labels.

### 4. `split-summary.json`

| Field | Type | Purpose |
|-------|------|---------|
| `record_count` | integer | Total examples |
| `group_count` | integer | Total groups |
| `partition_counts` | object | partition name -> integer count |
| `label_distributions_by_partition` | object | partition name -> { label -> count } |
| `algorithm_version` | string | Algorithm version used |
| `split_hash` | string | SHA-256 split fingerprint (16 hex chars) |
| `generated_at` | string | ISO date only (no timestamp) |

Promotable. Must not contain local paths, hostnames, usernames, or execution durations.

### 5. `split-fingerprint.json`

| Field | Type | Purpose |
|-------|------|---------|
| `fingerprint_payload_sha256` | string | SHA-256 hex digest |
| `payload_size` | integer | Byte size of canonical payload |
| `sha_method` | string | `SHA-256` |
| `schema_version` | string | Schema version identifier |
| `canonical_manifest_reference` | string | Stable reference to canonical manifest |
| `input_artifact_sha256s` | object | input file path -> SHA-256 |
| `generated_at` | string | ISO date only (no timestamp) |

Promotable. Must not contain local paths, hostnames, or usernames.

### 6. `leakage-audit-report.json`

| Field | Type | Purpose |
|-------|------|---------|
| `findings` | array | List of leakage findings |
| `leaked` | boolean | `true` if any unresolved finding |
| `finding_count` | integer | Total findings |
| `detection_methods` | array of strings | Ordered list of methods applied |
| `generated_at` | string | ISO date only (no timestamp) |

Each finding:

| Field | Type | Purpose |
|-------|------|---------|
| `finding_id` | string | Stable finding identifier |
| `finding_type` | string | One of: exact_example, source_document, exact_question, normalized_question, near_duplicate_question, context_overlap |
| `example_ids` | array of strings | Examples involved |
| `source_document_ids` | array of strings | Source documents involved |
| `partitions` | array of strings | Partitions involved |
| `score` | float or null | Similarity score (Jaccard, etc.) |
| `shared_surface` | array of strings | What was shared |
| `classification` | string | `unresolved`, `false_positive`, `confirmed_leakage` |
| `evidence_reference` | string or null | Stable reference to supporting evidence |
| `suppressed` | boolean | Must be `false` for all findings |

Promotable. Must not contain raw question text, context text, or labels.

### 7. `excluded-or-unassigned-ledger.json`

| Field | Type | Purpose |
|-------|------|---------|
| `count` | integer | Number of excluded examples |
| `reason` | string | Why examples were excluded |
| `excluded_ids` | array of strings | Excluded example identifiers |
| `generated_at` | string | ISO date only (no timestamp) |

Promotable.

### 8. `p01-04-closeout-record.json`

| Field | Type | Purpose |
|-------|------|---------|
| `status` | string | `pass` or `fail` |
| `authorization_record` | string | Stable reference to authorization |
| `split_hash` | string | Canonical split fingerprint |
| `validation_references` | array of strings | References to validation outputs |
| `external_evidence_references` | array of strings | References to external evidence only |
| `ratified_at` | string | ISO date only (no timestamp) |

Promotable.

---

## External-evidence-only records

The following must remain outside the repository and outside the evidence root. They are referenced by stable identity only.

| Record | Purpose | Storage |
|--------|---------|---------|
| Command log | Complete command lines for Generation A and Generation B | External evidence location |
| Process access log | Process IDs, start/end timestamps, exit codes | External evidence location |
| Generation workspace identity | Paths to Generation A and Generation B work directories | External evidence location |
| Pre-freeze and post-freeze inventories | Byte-level file listings before and after freeze | External evidence location |
| Copy/finalization log | Copy commands and verification results | External evidence location |
| Forensic review output | Independent review conclusions | External evidence location |
| Invalidation record | Details of any invalidated candidates | External evidence location |
| Execution evidence record | Complete execution provenance | External evidence location |
| Split manifest canonical payload | Exact byte payload used for fingerprint computation | External evidence location (referenced by `split-fingerprint.json`) |

A promotable record may reference an external-evidence record using a stable identifier (e.g., a SHA-256 digest or UUID), but must not include local paths, workspace paths, timestamps beyond ISO date, usernames, or hostnames.
