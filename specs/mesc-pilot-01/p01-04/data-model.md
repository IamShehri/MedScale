# MESC Pilot-01 — P01-04 Data Model

Status: **specification and policy only — no execution authorized**

This document defines the canonical data structures for P01-04 split and audit outputs. No instance data is created during P01-04A.

---

## Group identity

```text
Group
  source_document_id: str        # Primary key; derived from normalized pubid
  example_count: int             # Number of examples in this group (currently always 1)
  row_ordinals: [int]            # Stable ordinals from ordered registry
  group_id: str                  # Stable derived identifier
  assigned_split: str | null     # train | validation | test | null (before allocation)
```

A group is the minimum indivisible allocation unit. All `row_ordinals` in a group must receive the same `assigned_split`.

## Example identity

```text
ExampleIdentity
  example_id: str                # Stable derived identifier
  source_document_id: str        # Source document this example belongs to
  row_ordinal: int               # Stable ordinal in ordered registry
  decision: str                  # yes | no | maybe
  assigned_split: str | null     # train | validation | test | null (before allocation)
  partition_key: str | null      # Deterministic partition key (before allocation: null)
```

`example_id` is derived from a deterministic payload including `dataset_id`, `dataset_revision`, `configuration`, `original_example_id`, `source_document_id`, `transformation_version`. The derivation is SHA-256 based and is fully reproducible.

## Label stratum

```text
LabelStratum
  decision: str                  # yes | no | maybe
  example_count: int             # Count of examples in this stratum
  target_train: int              # Target examples for train
  target_validation: int         # Target examples for validation
  target_test: int               # Target examples for test
```

The target counts for each stratum are derived from the apportionment algorithm and must sum exactly to the stratum's example count.

## Partition assignment

```text
PartitionAssignment
  partition: str                 # train | validation | test
  group_ids: [str]               # Groups assigned to this partition
  example_count: int             # Total examples in this partition
  label_distribution: {str: int} # decision -> count
  split_key: str                 # Deterministic ranking key used for this partition
```

## Split fingerprint payload

```text
SplitFingerprintPayload
  algorithm_version: str         # e.g. "mesc-pilot-01-split-algorithm/1"
  seed: str                      # "mesc-pilot-01-split-v1"
  record_count: int              # Total examples
  group_count: int               # Total groups
  partition_counts: {str: int}   # partition -> count
  label_distributions: {str: {str: int}}  # partition -> {decision -> count}
  assignment_payload_sha256: str # SHA-256 over canonical assignment artifact
  serialization: {
    encoding: str,               # "utf-8"
    ensure_ascii: bool,
    allow_nan: bool,
    separators: [str, str],      # [",", ":"]
    sort_keys: bool,             # true
    indent: null                 # no indentation
  }
```

The fingerprint is computed as the first 16 hex characters of `SHA-256(canonical_json(payload))`.

## Finding model

```text
LeakageFinding
  finding_id: str                # Stable derived identifier
  finding_type: str              # exact_example | source_document | exact_question |
                                 # normalized_question | near_duplicate_question |
                                 # context_overlap
  example_ids: [str]             # Examples involved (length N >= 2)
  source_document_ids: [str]     # Source documents involved
  partitions: [str]              # Partitions involved (length >= 2)
  score: float | null            # Similarity score (e.g., Jaccard) when applicable
  shared_surface: [str]          # What was shared
  classification: str            # unresolved | false_positive | confirmed_leakage
  evidence_reference: str | null # Stable reference to supporting evidence
  suppressed: bool               # Must be false for all findings in accepted report
```

## Split manifest

```text
SplitManifest
  algorithm_version: str
  seed: str
  assignments: [PartitionAssignment]
  group_assignments: [GroupAssignment]  # one per group, ordered by (partition, group_id)
  example_assignments: [ExampleAssignment]  # one per example, ordered by (partition, row_ordinal)
  split_hash: str                # 16-char hex split fingerprint
  generated_at: str | null       # ISO date only; null for specification-only artifacts
```

## Finding audit report

```text
LeakageAuditReport
  findings: [LeakageFinding]
  leaked: bool                   # true if any unresolved finding
  finding_count: int             # len(findings)
  detection_methods: [str]       # Ordered list of methods applied
  generated_at: str | null       # ISO date only; null for specification-only artifacts
```

## Stable versus runtime metadata

| Metadata type | Examples | Included in promotable artifacts | Included in external evidence |
|---|---|---|---|
| Stable identity | `example_id`, `source_document_id`, `group_id`, `split_hash` | Yes | No |
| Schema version | `algorithm_version`, `schema_version` | Yes | No |
| Input artifact identity | `input_artifact_sha256s` | Yes (as digests) | Yes (as digests) |
| Ratification record | `authorization_record`, `ratified_at` | Yes (ISO date only) | Yes |
| Runtime metadata | timestamps, process IDs, durations, hostnames, usernames | No | Yes |
| Workspace identity | generation workspace paths | No | Yes |
| Command log | exact command lines with paths | No | Yes |
| Forensic review | independent review output | No | Yes |
