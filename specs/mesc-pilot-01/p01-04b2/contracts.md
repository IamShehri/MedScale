# MESC Pilot-01 — P01-04B2 Contracts

Status: **founder-ratified design contracts — implementation and execution not authorized**

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

This document records the founder-ratified design contracts for P01-04B2
tooling. No Python implementation is authorized. Types are proposed for later
review and implementation after separate founder authorization.

B2 defines an extended versioned leakage schema that wraps the frozen B1 contracts at the boundary; it does not mutate or silently reinterpret B1 fields.

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
| `partitions` | array of strings | Partition names | Must be subset of `["train", "validation", "test"]` |
| `target_counts` | object | partition -> integer | Must sum to total dataset size |
| `target_ratios` | object | partition -> float | Informative only; not used for computation |
| `holdout_included` | boolean | Holdout flag | `false` for version 1 per D8 |
| `minimum_sizes` | object | partition -> integer | Per D7 minimums |
| `rank_key_schema` | object | Ranking key definition | Must match D6 canonical key schema |
| `serialization_rules` | object | Encoding and formatting | Must match D6 serialization rules |
| `apportionment_method` | string | Algorithm description | Must describe constrained minimum-deviation apportionment |

Promotable: yes
Prohibited fields: `ratified_at`, `generated_at`, local paths, usernames, hostnames, timestamps
Canonical ordering: recursive key sort; UTF-8; `ensure_ascii=False`; `allow_nan=False`; separators `(",", ":")`; no BOM; LF lines.

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
Canonical JSON: sorted keys, UTF-8, no BOM, LF lines, no indentation.

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
Canonical JSON: sorted keys, UTF-8, no BOM, LF lines, no indentation.

### `SplitSummary`

Aggregate summary in `split-summary.json`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `record_count` | integer | Total examples | Must equal canonical total |
| `group_count` | integer | Total groups | Must equal canonical group count |
| `partition_counts` | object | partition -> integer | Must sum to `record_count` |
| `label_distributions_by_partition` | object | partition -> {label -> count} | Must match D4 ratified target matrix within integer rounding |
| `algorithm_version` | string | Algorithm version | Must match SplitPolicy |
| `split_hash` | string | 16-hex SHA-256 digest | Truncated from canonical payload; B1 compatibility only; never authoritative |
| `split_fingerprint` | string | 64-hex SHA-256 digest | Full fingerprint of complete canonical payload; sole authoritative identity |

Promotable: yes
Prohibited fields: local paths, usernames, hostnames, execution durations, command logs, timestamps

Note: `split_hash` is the B1 truncated digest (16 hex). `split_fingerprint` is the authoritative B2 full digest (64 hex). They are not interchangeable.

### `SplitFingerprint`

Full fingerprint in `split-fingerprint.json`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `fingerprint_payload_sha256` | string | 64-hex SHA-256 | Full digest of canonical payload |
| `payload_size` | integer | Byte size | Must match actual payload bytes |
| `sha_method` | string | Hash method | Must equal `SHA-256` |
| `schema_version` | string | Schema version | Future-proofing |
| `canonical_manifest_reference` | string | Manifest reference | Stable reference, not local path |
| `input_artifact_sha256s` | object | stable id -> SHA-256 | Only for non-repository inputs; repository paths excluded |

Promotable: yes
Prohibited fields: local paths, hostnames, usernames, command logs, workspace locations, timestamps

The `input_artifact_sha256s` field must not expose repository-internal paths. Only external input artifacts may be recorded by stable identifier.

### `SplitFingerprintBundle`

Canonical bundle manifest bound into the authoritative fingerprint.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `bundle_schema_version` | string | Bundle schema version | Stable version |
| `policy_id` | string | Policy identifier | Must match SplitPolicy |
| `algorithm_version` | string | Algorithm version | Must match SplitPolicy |
| `split_seed` | string | Domain-separation value | Not an RNG seed |
| `canonical_artifact_role` | string | Role identifier | Stable role |
| `artifact_sha256` | string | 64-hex SHA-256 | Exact canonical artifact bytes |
| `artifact_byte_size` | integer | Byte size | Exact byte length |
| `schema_version` | string | Artifact schema version | Stable schema version |

Promotable: yes
Binding requirement: The bundle binds the exact canonical bytes of the group-registry artifact, example-split-registry artifact, split-summary identity core, excluded-or-unassigned ledger, and any other ratified formal split artifact. Artifact entries are ordered by stable artifact role.

Split-summary identity core exclusion: The artifact bound as the split-summary identity core must exclude `split_fingerprint` itself, provenance dates, local/runtime metadata, and command evidence.

Any mismatch in fingerprint, artifact hash, or artifact byte size is fail-closed.

### `ExcludedOrUnassignedLedger`

Ledger of examples excluded or unassigned from the split.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `count` | integer | Excluded count | Non-negative |
| `reason` | string | Exclusion reason | Must be documented in decision record |
| `excluded_ids` | array of strings | Excluded identifiers | Must match canonical registry |

Promotable: yes
Prohibited fields: local paths, usernames, hostnames, timestamps

---

## Leakage contracts

B2 leakage contracts extend and wrap the frozen B1 contracts at the boundary;
they do not mutate or silently reinterpret B1 fields.
`PilotSplitAssignment`, `PilotSplitManifest`, `PilotLeakageFinding`, and
`PilotLeakageAuditReport` remain frozen in B1.

### `LeakageFinding`

Single leakage finding in `leakage-audit-report.json`.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `finding_id` | string | Stable identifier | Deterministic over finding schema version, finding type, sorted example IDs, sorted source-document IDs, sorted partitions, and normalized score representation |
| `finding_type` | string | One of: `exact_example`, `source_document`, `exact_question`, `normalized_question`, `near_duplicate_question`, `context_overlap`, `empty_normalized_question` | Enumerated |
| `example_ids` | array of strings | Examples involved | Must match canonical registry |
| `source_document_ids` | array of strings | Source documents involved | Must match canonical registry |
| `partitions` | array of strings | Partitions involved | Must be subset of canonical partitions |
| `score` | float or null | Similarity score | Jaccard for near-duplicate; null for exact matches; never fabricated |
| `shared_surface` | array of strings | What was shared | Must not contain raw text |
| `classification` | string | `unresolved`, `false_positive`, `confirmed_leakage` | Must not be suppressed |
| `evidence_reference` | string or null | Supporting evidence | Stable reference, not local path |
| `suppressed` | boolean | Suppression flag | Must be `false`; suppression is prohibited |

Promotable: yes, if and only if no finding contains raw text
Prohibited content: raw question text, context text, answer text, local paths, usernames, hostnames, timestamps

### `LeakageAuditReport`

Aggregate leakage audit result.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `findings` | array of `LeakageFinding` | All findings | Must include all findings; suppression prohibited; report must not be empty for leakage-positive qualification fixtures |
| `leaked` | boolean | True if unresolved findings | Computed from findings |
| `finding_count` | integer | Total findings | Count of `findings` array |
| `detection_methods` | array of strings | Methods applied | Ordered list |
| `normalization_record` | object | Normalization steps applied | Records NFKC, case folding, whitespace collapse |

Promotable: yes, if and only if no finding contains raw text
Prohibited content: raw question text, context text, answer text, local paths, usernames, hostnames, timestamps

Note: The audit report is expected to be non-empty for leakage-positive qualification fixtures. A vacuous empty audit report is not an acceptable qualification outcome.

### `CanonicalJsonBytes`

Canonical JSON serialization contract shared by all promotable types.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `encoding` | string | Text encoding | Must equal `UTF-8` |
| `bom` | boolean | BOM presence | Must be `false` |
| `key_ordering` | string | Key sort order | Must equal `recursive_lexicographic` |
| `ensure_ascii` | boolean | ASCII escaping | Must be `false` |
| `allow_nan` | boolean | NaN allowance | Must be `false` |
| `separators` | string | JSON separators | Must equal `(",", ":")` |
| `indentation` | integer | Indent width | Must equal `0` |
| `line_ending` | string | Line ending | Must equal `LF` |
| `terminal_newline` | boolean | Final LF | Must be `true` for multi-line JSONL; single-object JSON ends with exactly one LF |

Promotable: yes as a schema definition artifact
Binding: identical inputs must produce byte-identical outputs across supported Python 3.11 and 3.12; Windows, Linux and macOS; locale settings; time zones.

### `CanonicalJsonlBytes`

JSONL serialization contract for line-oriented artifact files.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `encoding` | string | Text encoding | Must equal `UTF-8` |
| `bom` | boolean | BOM presence | Must be `false` |
| `key_ordering` | string | Key sort order | Must equal `recursive_lexicographic` |
| `ensure_ascii` | boolean | ASCII escaping | Must be `false` |
| `allow_nan` | boolean | NaN allowance | Must be `false` |
| `separators` | string | JSON separators | Must equal `(",", ":")` |
| `indentation` | integer | Indent width | Must equal `0` |
| `line_ending` | string | Line ending | Must equal `LF` |
| `terminal_newline` | boolean | Final LF per object | Must be `true` |
| `blank_lines` | boolean | Blank-line allowance | Must be `false` |
| `empty_file_behavior` | string | Zero-record behavior | Must equal `zero_byte_file` |

Promotable: yes as a schema definition artifact

---

## Fixture-only execution types

B2 leakage contracts extend and wrap the frozen B1 contracts at the boundary;
they do not mutate or silently reinterpret B1 fields.
`PilotSplitAssignment`, `PilotSplitManifest`, `PilotLeakageFinding`, and
`PilotLeakageAuditReport` remain frozen in B1.

### `FixtureSplitRequest`

Structural fixture identity required for any B2 facade invocation.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `fixture_namespace` | string | Approved namespace | Must match `mesc-fixture/p01-04b2/<fixture-schema-version>/<fixture-id>` |
| `fixture_schema_version` | string | Schema version | Stable version |
| `fixture_id` | string | Fixture identifier | Approved fixture ID |
| `fixture_sha256` | string | 64-hex SHA-256 | Fingerprint of approved fixture bytes |
| `fixture_only` | boolean | Fixture-only marker | Must be `true` |
| `non_evidence` | boolean | Non-evidence marker | Must be `true` |
| `synthetic_identity_proof` | string | Proven synthetic batch | Approved synthetic batch reference |
| `request_id` | string | Stable request identifier | Deterministic request identity |
| `seed` | string | Domain-separation value | Not an RNG seed |

Promotable: no
External-evidence-only: no
Binding: No filename, directory name, or path heuristic may establish fixture identity. Synthetic identity must be proven by approved fixture namespace, fixture schema version, fixture fingerprint, and explicit `fixture_only=true` marker.

### `FixtureSplitResult`

Result of a fixture-only facade invocation.

| Field | Type | Purpose | Constraints |
|---|---|---|---|
| `split_manifest` | object | Manifest summary | Wraps B1 `PilotSplitManifest` at the boundary |
| `summary` | object | Split summary | `SplitSummary` |
| `fingerprint` | object | Full fingerprint | `SplitFingerprint` |
| `audit_report` | object | Leakage report | `LeakageAuditReport`; expected non-empty for leakage-positive qualification |
| `execution_evidence_ref` | string | External evidence reference | Stable reference, not local path |

Promotable: no
External-evidence-only: yes
Note: The `audit_report` is expected to be non-empty for leakage-positive qualification fixtures. A vacuous empty audit report is not an acceptable qualification outcome.

---

## Authorization and path-safety errors

Design enumerations (founder-ratified design only, not implemented):

| Error | Base | Meaning |
|---|---|---|
| `PilotSplitNotAuthorizedError` | `NotImplementedError` | Real split not authorized (already implemented in B1) |
| `FixtureOnlyModeError` | `RuntimeError` | Attempted real-registry invocation |
| `InvalidInputError` | `ValueError` | Input fails identity verification |

---

## Type promotion rules

| Type | Promotable | External-evidence-only |
|---|---|---|
| `SplitPolicy` | Yes | No |
| `GroupRegistryEntry` | Yes | No |
| `ExampleSplitRegistryEntry` | Yes | No |
| `SplitSummary` | Yes | No |
| `SplitFingerprint` | Yes | No |
| `SplitFingerprintBundle` | Yes | No |
| `ExcludedOrUnassignedLedger` | Yes | No |
| `CanonicalJsonBytes` | Yes | No |
| `CanonicalJsonlBytes` | Yes | No |
| `LeakageFinding` | Yes, if no raw text | No |
| `LeakageAuditReport` | Yes, if no raw text | No |
| Fixture request/result | No | Yes |

Promotable types must pass the promotable-artifact scan: no runtime metadata, no local paths, no timestamps, no usernames, no hostnames, no command logs, no workspace locations.
External-evidence-only types must remain outside the repository and outside the evidence root, referenced by stable identity only.
