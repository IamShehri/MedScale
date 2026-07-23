# MESC Pilot-01 — P01-04B2 Data Model

Status: **specification and entry-gate proposal only — implementation and execution not authorized**

---

## Entity relationships

P01-04B2 defines the following entity relationships for future tooling. No real data is produced in this task.

### `OrderedExampleRow`

Represents one row in the ordered example registry (P01-03G output).

```
OrderedExampleRow
  +-- example_id: string (stable identifier)
  +-- source_document_id: string (grouping key)
  +-- row_ordinal: integer (position in ordered registry)
  +-- final_decision: string (yes/no/maybe/abstain)
  +-- split_assignment: string (train/validation/test/holdout) — future only
```

Constraints:
- `example_id` must be a full SHA-256 hex digest (64 characters) from the canonical identity derivation.
- `source_document_id` must be a full SHA-256 hex digest.
- `row_ordinal` must be a non-negative integer assigned by the ordered registry construction order.
- `final_decision` must come from the external `source-records.jsonl` join only; no fabrication.
- `split_assignment` must not be populated until P01-04D authorization.

### `SourceLabelRow`

Represents one row in the source-document registry (P01-03G output).

```
SourceLabelRow
  +-- source_document_id: string (stable identifier)
  +-- example_count: integer (number of examples in this group)
  +-- row_ordinals: list of integer (positions in ordered registry)
  +-- group_assignment: string (train/validation/test/holdout) — future only
```

Constraints:
- `source_document_id` must be a full SHA-256 hex digest.
- `example_count` must be non-negative.
- `row_ordinals` must be sorted ascending.
- `group_assignment` must not be populated until P01-04D authorization.

### `LabeledExample`

Represents one labeled example in memory during split computation.

```
LabeledExample
  +-- example_id: string
  +-- source_document_id: string
  +-- row_ordinal: integer
  +-- final_decision: string
  +-- stratum: string (derived from final_decision)
  +-- rank_key: bytes (canonical JSON bytes for ranking)
  +-- rank_digest: string (SHA-256 hex of rank_key)
```

Constraints:
- `stratum` must be derived from `final_decision` using D4 strata: `yes`, `no`, `maybe`, `abstain`.
- `rank_key` must be the canonical JSON serialization per D6 rules.
- `rank_digest` must be the lowercase SHA-256 hex digest of `rank_key`.
- `LabeledExample` instances are transient in-memory objects. They must not be serialized to promotable artifacts.

### `LabelTarget`

Represents one integer target in the apportionment matrix.

```
LabelTarget
  +-- decision: string (yes/no/maybe)
  +-- partition: string (train/validation/test)
  +-- target_count: integer
  +-- actual_count: integer — future only
  +-- deviation: float — future only
```

Constraints:
- `target_count` must sum across partitions to the D4 label totals (552/338/110).
- `actual_count` must equal `target_count` after apportionment.
- `deviation` must be minimized per D5 constrained apportionment rules.
- `LabelTarget` instances are transient in-memory objects.

### `RankedGroup`

Represents one ranked source-document group after deterministic ranking.

```
RankedGroup
  +-- source_document_id: string
  +-- rank_digest: string
  +-- row_ordinals: list of integer
  +-- stratum: string
  +-- assigned_partition: string — future only
  +-- partition_key: string — future only
```

Constraints:
- `rank_digest` determines group ordering within stratum.
- `source_document_id` is the collision tie-breaker.
- `row_ordinal` is the final defensive tie-breaker.
- `assigned_partition` must not be populated until P01-04D authorization.
- `partition_key` must not be populated until P01-04D authorization.

### `GroupAssignment`

Represents one group-to-partition assignment.

```
GroupAssignment
  +-- group_id: string
  +-- source_document_id: string
  +-- assigned_split: string
  +-- partition_key: string
  +-- example_ids: list of string
```

Constraints:
- `group_id` must be a stable deterministic identifier derived from group content.
- `assigned_split` must be one of `train`, `validation`, `test`.
- `partition_key` must be computable from the rank key schema.
- `example_ids` must contain all `example_id` values in the group.
- `GroupAssignment` instances appear only in `group-registry.jsonl` as promotable artifacts.

### Promotable split artifacts

The following artifacts are promotable after successful P01-04D execution and separate promotion authorization:

```
group-registry.jsonl
  content: GroupAssignment records (one per line)
  order: (assigned_split, group_id) ascending
  format: canonical JSON, sorted keys, UTF-8, no BOM, LF lines

example-split-registry.jsonl
  content: ExampleSplitRegistryEntry records (one per line)
  order: (assigned_split, row_ordinal) ascending
  format: canonical JSON, sorted keys, UTF-8, no BOM, LF lines

split-summary.json
  content: SplitSummary
  format: canonical JSON, sorted keys, UTF-8, no BOM

split-fingerprint.json
  content: SplitFingerprint
  format: canonical JSON, sorted keys, UTF-8, no BOM

excluded-or-unassigned-ledger.json
  content: ExcludedOrUnassignedLedger
  format: canonical JSON, sorted keys, UTF-8, no BOM
```

### Leakage findings

Leakage findings are transient in-memory objects during P01-04E execution. Promotable `LeakageAuditReport` must contain findings with stable identifiers and classifications but no raw text.

```
LeakageFinding (transient)
  +-- finding_id: string (deterministic)
  +-- finding_type: string (enumerated)
  +-- example_ids: list of string
  +-- source_document_ids: list of string
  +-- partitions: list of string
  +-- score: float or null
  +-- shared_surface: list of string (semantic labels only)
  +-- classification: string
  +-- evidence_reference: string or null

LeakageAuditReport (promotable)
  +-- findings: list of LeakageFinding sanitized for promotion
  +-- leaked: boolean
  +-- finding_count: integer
  +-- detection_methods: list of string
```

Note: The promotable `LeakageAuditReport` must not contain raw question text, context text, or answer text in any field.

### External execution evidence

External evidence remains outside the repository and outside the evidence root.

```
External Execution Evidence (not promotable)
  +-- command_log: complete command lines for Generation A and B
  +-- process_access_log: PIDs, timestamps, exit codes
  +-- generation_workspace_identity: stable workspace references
  +-- pre_freeze_inventory: byte-level file listing before freeze
  +-- post_freeze_inventory: byte-level file listing after freeze
  +-- copy_finalization_log: copy commands and verification results
  +-- forensic_review_output: independent review conclusions
  +-- invalidation_record: invalidated candidate details
  +-- execution_evidence_record: complete provenance
  +-- split_manifest_canonical_payload: exact byte payload used for fingerprint
```

Promotable records may reference external evidence using stable identifiers (SHA-256 digest or UUID) but must not include local paths, workspace paths, usernames, hostnames, or timestamps beyond ISO date.

---

## Identity and digest behavior

| Identity type | Format | Where used | Authoritative |
|---|---|---|---|
| `example_id` | 64-hex SHA-256 | Example registries, findings | Yes (canonical registry) |
| `source_document_id` | 64-hex SHA-256 | Group registries, findings | Yes (canonical registry) |
| `group_id` | Deterministic from group content | Group registries | Derived |
| `finding_id` | Deterministic string | Leakage findings | Derived |
| `split_hash` | 16-hex SHA-256 | In-memory manifest integrity | B1 only |
| `split_fingerprint` | 64-hex SHA-256 | `split-fingerprint.json` | Proposed B2 |

No truncated digest may be silently treated as equivalent to a full fingerprint in any formal artifact.
