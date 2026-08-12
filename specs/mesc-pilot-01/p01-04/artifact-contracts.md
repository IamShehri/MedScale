# MESC Pilot-01 — P01-04 Artifact Contracts

Status: **specification and policy only — no execution authorized**

This document defines the proposed stable artifact schemas and external-evidence-only records for P01-04. No real split artifacts are created during P01-04A. No real partition membership is created or disclosed.

## Stable promotable artifacts

### HISTORICAL P01-04A PROPOSED INVENTORY — SUPERSEDED FOR CURRENT FORMAL STAGE CONTRACTING

Subsections 1 through 8 below are the original P01-04A **proposed** artifact
schemas. They are preserved unrewritten as a truthful historical record of the
proposal they describe. No field, name or table in them has been edited.

They are superseded for current formal stage contracting by
[Current formal stage contracts](#current-formal-stage-contracts) at the end of
this document. Where the two differ, the current formal stage contracts control
for P01-04D, P01-04E, P01-04F and P01-04G.

In particular, this historical inventory must not be read as the formal P01-04D
generation inventory: it proposes eight undifferentiated artifacts spanning four
stages, uses three artifact names that are now superseded, and omits
`generation-manifest.json` entirely.

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

**Historical name note.** The "Split manifest canonical payload" row above cites
`split-fingerprint.json` as the referencing artifact. That is the historical
P01-04A proposed name and it is preserved unrewritten. Under the `FD-DREADY-7`
supersession map recorded below, `split-fingerprint.json` maps to **no standalone
file**; for formal P01-04D the authoritative full lowercase 64-hex
`split_fingerprint` is carried and verified through `split-summary.json` and
`generation-manifest.json`, and any such external-evidence reference is made from
those artifacts instead.

---

## Current formal stage contracts

These contracts supersede the historical P01-04A proposed inventory above for
current formal stage contracting. They are recorded under `FD-DREADY-6`,
`FD-DREADY-7`, `FD-DREADY-8`, `FD-DREADY-9` and `FD-DREADY-10` in
[`../p01-04d-entry-readiness-remediation/founder-authorization.md`](../p01-04d-entry-readiness-remediation/founder-authorization.md),
which controls.

**Historical as of the remediation-design baseline.** Nothing below is produced
at this baseline.

```text
P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED
```

**Historical as of the remediation-design baseline.** The single supported
prospective operator surface is `scripts/mesc_p01_04d_operator.py` with exactly
the two commands `generate` and `compare`; it does not exist at this baseline.

**Current truth.** The two statements above describe the remediation-design
baseline and are preserved verbatim for it. The operator surface
`scripts/mesc_p01_04d_operator.py` and the private formal implementation modules
now exist on canonical main. The implementation code was adopted through PR #90,
and the adoption truth was reconciled through PR #91, so the
`P01-04D implementation: NOT AUTHORIZED` line above is superseded for current
implementation status by
[`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md).

No formal P01-04D artifact has been generated. The line
`P01-04D execution: NOT AUTHORIZED` remains current and in force, and P01-03G
registry access, external source-record access and real dataset access all
remain unauthorized. Under the founder decision recorded in
[`../p01-04d-entry-authorization/founder-authorization.md`](../p01-04d-entry-authorization/founder-authorization.md),
P01-04D entry is authorized and the control state is pre-execution governance
only. Entry authorizes no execution and opens no input.

The artifact names, schemas, descriptors, fingerprint rules, stage ownership and
scientific contracts recorded below are unchanged by this note.

### Artifact-name supersession map

```text
example-split-registry.jsonl
->
example-registry.jsonl
```

```text
excluded-or-unassigned-ledger.json
->
excluded-ledger.json
```

```text
split-fingerprint.json
->
no standalone file
```

```text
standalone fingerprint file:
none
```

The authoritative full lowercase 64-hex `split_fingerprint` is carried and
verified through `split-summary.json` and `generation-manifest.json`. The 16-hex
`split_hash` remains compatibility/display-only and never substitutes for the
64-hex value in any verification.

The following are **not** P01-04D generation outputs:

```text
leakage-audit-report.json
leakage-audit.json
p01-04-closeout-record.json
publication-manifest.json
```

### P01-04D candidate artifacts

Each Generation A and Generation B workspace contains exactly these seven
P01-04D candidate artifacts:

```text
split-policy.json

group-registry.jsonl

example-registry.jsonl

excluded-ledger.json

split-summary-identity-core.json

split-summary.json

generation-manifest.json
```

```text
P01-04D artifact count:
7
```

No eighth artifact. No log, receipt, lock, marker, PID file, timestamp file or
sidecar is part of the deterministic generation bundle. All seven files are
compared byte-for-byte between Generation A and Generation B.

`split-policy.json` is deterministic and carries no runtime or ratification
date. It binds exactly the versioned scientific policy needed for generation:
schema version, algorithm version, partition order, exact target counts,
grouping key, stratification field, label order, seed/domain separator,
ranking-key schema, apportionment method, minimum partition sizes, canonical
serialization rules and holdout policy. It contains no float where an exact
integer or rational representation is available, and no timestamp, local path,
username, hostname, command or environment value.

`generation-manifest.json` is non-circular and deterministic. It binds schema
version, algorithm version, generation-bundle filenames, surface identifiers,
schema versions, SHA-256 digests, byte sizes, the authoritative split
fingerprint and the input identity digests. It carries no generation identity
`A` or `B`, no workspace path, no process ID, no timestamp, no hostname, no
username, no command line and no external-evidence path, and neither its own
digest nor its own byte size. Generation A and Generation B therefore produce
identical manifest bytes when all scientific inputs and code are identical.

### P01-04E leakage artifact

```text
leakage-audit.json
```

Stage: canonical leakage audit and finding resolution. This is a P01-04E output,
not a P01-04D output. The filename is exactly `leakage-audit.json`; a `-report`
infix variant of that filename is not the current name.

### P01-04F closeout artifact

```text
p01-04-closeout-record.json
```

Stage: freeze, independent verification and closeout record. This is a P01-04F
output, not a P01-04D output.

### P01-04G promotion boundary

Stage: separately authorized repository promotion. P01-04G produces no new
scientific artifact. It is a promotion boundary only, and it requires its own
separate promotion authorization.

No stage may mutate an immutable artifact from an earlier stage. Later stages
reference earlier artifacts by stable identity.

### Fixture-only publication inventory

The accepted fixture-only publication inventory is a **different** inventory,
belonging to private, fixture-only, synthetic-only, non-evidence tooling:

```text
group-registry.jsonl
example-registry.jsonl
excluded-ledger.json
split-summary-identity-core.json
split-summary.json
leakage-audit.json
publication-manifest.json
```

This fixture inventory is **not** the formal P01-04D inventory. The two differ:

| Filename | Formal P01-04D bundle | Fixture-only publication |
|---|---|---|
| `split-policy.json` | yes | no |
| `group-registry.jsonl` | yes | yes |
| `example-registry.jsonl` | yes | yes |
| `excluded-ledger.json` | yes | yes |
| `split-summary-identity-core.json` | yes | yes |
| `split-summary.json` | yes | yes |
| `generation-manifest.json` | yes | no |
| `leakage-audit.json` | no | yes |
| `publication-manifest.json` | no | yes |

`publication-manifest.json` is the existing fixture-only publication artifact and
is never the formal P01-04D generation manifest. The formal P01-04D
candidate-bundle manifest is `generation-manifest.json`.

The fixture-only tooling — `FixtureSplitFacade` and `_fixture_publication_v1` —
remains private, fixture-only, synthetic-only, non-evidence, unexported and
unchanged. Its execution authority is never reused for formal P01-04D execution.
