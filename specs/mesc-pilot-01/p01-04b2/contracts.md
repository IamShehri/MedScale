# MESC Pilot-01 — P01-04B2 Contracts

Status: **specification and entry-gate proposal only — implementation and execution not authorized**

This document defines proposed type contracts for P01-04B2 tooling. No Python implementation is authorized. Types are proposed for later review and implementation after separate founder authorization.

All types exclude raw question, context, answer, or per-example label content from promotable artifacts, per P01-04A decision D9.

---

## Stable type definitions

### `SplitPolicy`

Stable identifier for a complete split policy configuration.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `policy_id` | string | Stable identifier | Format: `mesc-pilot-01-split-policy/<version>` |
| `algorithm_version` | string | Algorithm version | Must match D10 versioning scheme |
| `grouping_key` | string | Grouping unit | Must equal `source_document_id` unless founder amendment |
| `stratification_field` | string | Stratification field | Must equal `decision` unless founder amendment |
| `partitions` | array of strings | Partition names | Must be subset of `["train", "validation", "test", "holdout"]` |
| `target_counts` | object | partition -> integer | Must sum to total dataset size |
| `target_ratios` | object | partition -> float | Informative only; not used for computation |
| `holdout_included` | boolean | Holdout flag | `false` for version 1 per D8 |
| `minimum_sizes` | object | partition -> integer | Per D7 minimums |
| `rank_key_schema` | object | Ranking key definition | Must match D6 canonical key schema |
| `serialization_rules` | object | Encoding and formatting | Must match D6 serialization rules |
| `apportionment_method` | string | Algorithm description | Must describe constrained minimum-deviation apportionment |
| `ratified_at` | string | ISO date only | No timestamp; no runtime generation |

Promotable: yes
Prohibited fields: `generated_at` (use `ratified_at`), local paths, usernames, hostnames, timestamps

Canonical ordering: recursive key sort; UTF-8; `ensure_ascii=False`; `allow_nan=False`; separators `(",", ":"`; no BOM; LF lines.

### `GroupRegistryEntry`

One JSON object per source-document group in `group-registry.jsonl`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `group_id` | string | Stable group identifier | Deterministic from group content |
| `source_document_id` | string | Source document identifier | Must match canonical registry |
| `example_count` | integer | Examples in group | Non-negative integer |
| `row_ordinals` | array of integers | Row ordinals in group | Sorted ascending |
| `assigned_split` | string | Assigned partition | Must be `train`, `validation`, or `test` |
| `partition_key` | string | Deterministic key | Computed from rank key schema |

Promotable: yes
Prohibited content: question text, context text, labels, local paths, usernames, hostnames, timestamps

Serialization order: `(assigned_split, group_id)` ascending within file.
Canonical JSON: sorted keys, UTF-8, no BOM, LF lines.

### `ExampleSplitRegistryEntry`

One JSON object per example in `example-split-registry.jsonl`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `example_id` | string | Stable example identifier | Must match canonical registry |
| `source_document_id` | string | Source document identifier | Must match canonical registry |
| `row_ordinal` | integer | Row ordinal in ordered registry | Non-negative integer |
| `assigned_split` | string | Assigned partition | Must be `train`, `validation`, or `test` |
| `partition_key` | string | Deterministic key | Computed from rank key schema |

Promotable: yes
Prohibited content: question text, context text, labels, local paths, usernames, hostnames, timestamps

Serialization order: `(assigned_split, row_ordinal)` ascending within file.
Canonical JSON: sorted keys, UTF-8, no BOM, LF lines.

### `SplitSummary`

Aggregate summary in `split-summary.json`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `record_count` | integer | Total examples | Must equal canonical total |
| `group_count` | integer | Total groups | Must equal canonical group count |
| `partition_counts` | object | partition -> integer | Must sum to `record_count` |
| `label_distributions_by_partition` | object | partition -> {label -> count} | Must match D4 ratified target matrix within integer rounding |
| `algorithm_version` | string | Algorithm version | Must match SplitPolicy |
| `split_hash` | string | 16-hex SHA-256 digest | Truncated from canonical payload; for in-memory integrity only |
| `split_fingerprint` | string | 64-hex SHA-256 digest | Full fingerprint of complete canonical payload |
| `generated_at` | string | ISO date only | No timestamp; no runtime generation |

Promotable: yes
Prohibited fields: local paths, usernames, hostnames, execution durations, command logs

Note: `split_hash` is the B1 truncated digest (16 hex). `split_fingerprint` is the proposed B2 full digest (64 hex). They are not interchangeable. See `decision-record.md` for pending founder decision on authoritative identity.

### `SplitFingerprint`

Full fingerprint in `split-fingerprint.json`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `fingerprint_payload_sha256` | string | 64-hex SHA-256 | Full digest of canonical payload |
| `payload_size` | integer | Byte size | Must match actual payload bytes |
| `sha_method` | string | Hash method | Must equal `SHA-256` |
| `schema_version` | string | Schema version | Future-proofing |
| `canonical_manifest_reference` | string | Manifest reference | Stable reference, not local path |
| `input_artifact_sha256s` | object | path -> SHA-256 | Only for non-repository inputs; repository paths excluded |
| `generated_at` | string | ISO date only | No timestamp |

Promotable: yes
Prohibited fields: local paths, hostnames, usernames, command logs, workspace locations

The `input_artifact_sha256s` field must not expose repository-internal paths. Only external input artifacts (e.g., `source-records.jsonl` identity reference) may be recorded by stable identifier.

### `ExcludedOrUnassignedLedger`

Ledger of examples excluded or unassigned from the split.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `count` | integer | Excluded count | Non-negative |
| `reason` | string | Exclusion reason | Must be documented in decision record |
| `excluded_ids` | array of strings | Excluded identifiers | Must match canonical registry |
| `generated_at` | string | ISO date only | No timestamp |

Promotable: yes
Prohibited fields: local paths, usernames, hostnames, timestamps beyond ISO date

### `LeakageFinding`

Single leakage finding in `leakage-audit-report.json`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `finding_id` | string | Stable identifier | Deterministic across reruns |
| `finding_type` | string | One of: `exact_example`, `source_document`, `exact_question`, `normalized_question`, `near_duplicate_question`, `context_overlap` | Enumerated |
| `example_ids` | array of strings | Examples involved | Must match canonical registry |
| `source_document_ids` | array of strings | Source documents involved | Must match canonical registry |
| `partitions` | array of strings | Partitions involved | Must be subset of canonical partitions |
| `score` | float or null | Similarity score | Jaccard for near-duplicate; null for exact matches |
| `shared_surface` | array of strings | What was shared | Must not contain raw text |
| `classification` | string | `unresolved`, `false_positive`, `confirmed_leakage` | Must not be suppressed |
| `evidence_reference` | string or null | Supporting evidence | Stable reference, not local path |
| `suppressed` | boolean | Suppression flag | Must be `false`; suppression is prohibited |

Promotable: yes, if and only if raw text is absent from all fields
Prohibited content: raw question text, context text, answer text, local paths, usernames, hostnames, timestamps

### `LeakageAuditReport`

Aggregate leakage audit result.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `findings` | array of `LeakageFinding` | All findings | Must include all findings; suppression prohibited |
| `leaked` | boolean | True if unresolved findings | Computed from findings |
| `finding_count` | integer | Total findings | Count of `findings` array |
| `detection_methods` | array of strings | Methods applied | Ordered list |
| `generated_at` | string | ISO date only | No timestamp |

Promotable: yes, if and only if no finding contains raw text
Prohibited content: raw question text, context text, answer text, local paths, usernames, hostnames, timestamps

### Fixture-only execution request/result types

Proposed request type (design only, not implemented):

- `fixture_rows`: injected synthetic rows only
- `fixture_source_document_ids`: corresponding source-document IDs
- `policy_override`: optional policy reference (must be ratified)
- `seed`: domain-separation value (not RNG seed)
- `request_id`: stable request identifier

Proposed result type (design only, not implemented):

- `split_manifest`: `PilotSplitManifest` equivalent
- `summary`: `SplitSummary`
- `fingerprint`: `SplitFingerprint`
- `audit_report`: `LeakageAuditReport` (always empty for fixture input)
- `execution_evidence_ref`: stable reference to external evidence (not path)

### Authorization and path-safety errors

Proposed error enumerations (design only, not implemented):

- `PilotSplitNotAuthorizedError(NotImplementedError)`: real split not authorized (already implemented in B1)
- `FixtureOnlyModeError(RuntimeError)`: attempted real-registry invocation
- `PathSafetyViolation(ValueError)`: output path outside designated workspace
- `ConcurrencyViolation(RuntimeError)`: concurrent writer detected
- `InvalidInputError(ValueError)`: input fails identity verification
- `ArtifactOverwriteError(PermissionError)`: write would overwrite existing artifact

---

## Type promotion rules

| Type | Promotable | External-evidence-only |
|---|---|---|
| `SplitPolicy` | Yes | No |
| `GroupRegistryEntry` | Yes | No |
| `ExampleSplitRegistryEntry` | Yes | No |
| `SplitSummary` | Yes | No |
| `SplitFingerprint` | Yes | No |
| `ExcludedOrUnassignedLedger` | Yes | No |
| `LeakageFinding` | Yes, if no raw text | No |
| `LeakageAuditReport` | Yes, if no raw text | No |
| Fixture request/result | No | Yes |

Promotable types must pass the promotable-artifact scan: no runtime metadata, no local paths, no timestamps beyond ISO date, no usernames, no hostnames, no command logs, no workspace locations.

External-evidence-only types must remain outside the repository and outside the evidence root, referenced by stable identity only.
