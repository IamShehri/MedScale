# MESC Pilot-01 — P01-03 Plan

Status: **future gated execution plan**
Authorization: P01-03 planning authorized; execution not authorized
Freeze date: 2026-07-17

---

## Stage registry

Each stage requires separate explicit authorization before execution begins. Carrying a future stage authorization does not authorize prior stages.

```text
P01-03A — acquisition authorization
P01-03B — immutable artifact acquisition
P01-03C — native schema inspection and decision confirmation
P01-03D — schema-gap resolution
P01-03E — deterministic transformation
P01-03F — validation
P01-03G — closeout and P01-04 handoff
```

---

## P01-03A — acquisition authorization

Prerequisites:
- P01-03 planning package accepted.
- Founder authorization for dataset acquisition recorded.
- Raw-data storage boundary confirmed.
- `.gitignore` entries confirmed.

Outputs:
- Acquisition authorization record.
- Approved artifact allowlist.
- Storage boundary confirmation.

Acceptance:
- Authorization record present and signed.
- Allowlist matches pinned revision and configuration.
- No raw-data path is inside tracked source directories.

Stop conditions:
- Acquisition authorized without storage boundary confirmation.
- Allowlist includes mutable branch names or arbitrary loading scripts.
- `trust_remote_code` is required or permitted by the proposed acquisition path.</text>

---

## P01-03B — immutable artifact acquisition

Prerequisites:
- P01-03A authorization recorded.

Outputs:
- Acquisition manifest.
- Downloaded Parquet artifacts in approved local raw-data location.
- Artifact SHA256 digests.

Acceptance:
- Manifest revision equals pinned revision.
- Manifest configuration equals `pqa_labeled`.
- Only approved Parquet and metadata files are present.
- Computed SHA256 digests match recorded manifest hashes.
- No raw content is inside Git tracking.

Stop conditions:
- Revision mismatch.
- Configuration missing.
- Unexpected Python scripts required.
- File allowlist violation.
- Hash computation failure.
- Rights metadata change detected.
- Raw content placed inside tracked directory.

---

## P01-03C — native schema inspection and decision confirmation

Prerequisites:
- P01-03B acquisition manifest accepted.

Outputs:
- Native schema validation report.
- Column presence and type confirmation.
- `final_decision` value audit.
- `pubid` presence and type audit.
- Context shape audit.
- Row count and split identity confirmation.
- Source-document uniqueness check.

Acceptance:
- All required columns present.
- All `final_decision` values are `yes`, `no`, or `maybe`.
- No unexpected nulls in required fields.
- No empty questions in answerable records.
- Row count matches expected PQA-L count.
- Source-document uniqueness assumptions are documented.

Stop conditions:
- Required columns missing.
- Unexpected `final_decision` values.
- `pubid` missing or malformed at scale.
- Source-document uniqueness violated.
- Row count or configuration identity differs from approved values.

---

## P01-03D — schema-gap resolution

Prerequisites:
- P01-03C native schema confirmed.
- Approved schema-gap strategy selected.

Outputs:
- `PilotPubMedQASourceRecord` normalized representation defined.
- Unavailable annotation fields explicitly marked.
- Schema version policy confirmed.

Acceptance:
- No synthetic gold annotations are produced.
- Native labels remain distinguishable from derived or manual labels.
- Schema version policy is explicit.
- No silent reinterpretation of v1 occurs.

Stop conditions:
- Atomic claims derived from `long_answer` and labeled gold.
- `maybe` mapped to `abstain` without annotation protocol.
- Evidence sufficiency or uncertainty inferred from context presence.
- Sentence-level rationale labels fabricated from context entries.

---

## P01-03E — deterministic transformation

Prerequisites:
- P01-03D schema-gap resolution approved.
- Source-document identity policy approved.
- Example-ID policy approved.
- Evidence-mapping policy approved.
- Text-normalization policy approved.

Outputs:
- Layer-1 `PilotPubMedQASourceRecord` instances.
- Full `PilotRecord` instances for annotated subset.
- Transformation report.
- Example-ID registry.
- Source-document-ID registry.

Acceptance:
- Identical input bytes and transformation version produce byte-identical canonical output.
- Different source revision changes source and record identity.
- Record ordering is deterministic.
- Canonical serialization is stable.
- `content_hash` is reproducible.
- No raw abstracts are included in output.

Stop conditions:
- Runtime UUID used in identity.
- Unpinned dataframe index used as identity.
- Timestamps, paths, or hostnames included in identity.
- Context order non-deterministic.
- Abstraction rewriting or summarization applied to evidence text.
- Raw abstracts committed or prepared for redistribution.

---

## P01-03F — validation

Prerequisites:
- P01-03E transformation output accepted.

Outputs:
- Validation report.
- Validation status per record and per category.
- Excluded-record ledger.

Acceptance:
- All required identity validations pass.
- All required schema validations pass.
- All content-boundary validations pass.
- All determinism validations pass.
- All rights and provenance validations pass.
- All honesty validations pass.
- No `fail` status without explicit reason.
- No silent conversion of warnings to success.

Stop conditions:
- Duplicate `example_id` values.
- Invalid `source_document_id` values.
- Content hash mismatch.
- Unapproved field values present.
- Raw content found in output.
- Unavailable metrics reported as computed values.
- Layer 2 metrics claimed without gold subset.

---

## P01-03G — closeout and P01-04 handoff

Prerequisites:
- P01-03F validation report accepted.

Outputs:
- P01-03 closeout record.
- P01-04 handoff package containing:
  - validated transformed dataset identity;
  - ordered example-ID registry;
  - source-document-ID registry;
  - dataset fingerprint;
  - schema version;
  - transformation version;
  - validation report;
  - excluded-record ledger;
  - rights/provenance record.

Acceptance:
- All handoff artifacts present and non-empty.
- Handoff package does not include train, validation, test, or holdout assignments.
- P01-04 explicitly acknowledges its responsibilities for grouped split assignment and leakage audit.

Stop conditions:
- Handoff package includes split assignments.
- Leakage audit findings suppressed.
- Claims exceed executed phases.
