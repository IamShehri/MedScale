# MESC Pilot-01 — P01-03 Execution Protocol

Status: **future execution protocol — not executed**
Authorization: P01-03 planning authorized; execution not authorized
Freeze date: 2026-07-17

---

## General rule

All commands, code blocks, and procedures in this document are **future examples only**.
No acquisition, transformation, validation, or dataset-access action may be executed
under the current authorization.

Every example block is labeled:

```text
EXAMPLE ONLY — DO NOT EXECUTE UNDER CURRENT AUTHORIZATION
```

---

## A0 — Verify acquisition manifest

Before any Parquet file is opened, the future acquisition manifest must be verified.

Checks:
- `dataset_id` equals `qiaojin/PubMedQA`.
- `dataset_revision` equals `9001f2853fb87cab8d220904e0de81ac6973b318`.
- `configuration` equals `pqa_labeled`.
- `artifact_path` entries are inside the approved raw-data location and outside Git tracking.
- Computed `sha256` matches recorded manifest hash for every file.
- `license_id` matches approved license metadata.
- No unknown fields are present that would indicate schema drift.

Fail-closed behavior:
- Any mismatch stops execution.
- The manifest itself is treated as untrusted until all checks pass.

---

## A1 — Read approved Parquet artifacts locally

After A0 passes, read only approved Parquet files from the local raw-data location.

Allowed file extensions:
- `.parquet`
- `.json` metadata files explicitly listed in the manifest

Prohibited:
- Python loading scripts
- Loading-cache directories with unknown contents
- Arbitrary pickle or joblib files
- Network access during read

Fail-closed behavior:
- Absence of an approved `.parquet` file stops execution.
- Presence of an unexpected file type stops execution.

---

## A2 — Validate native schema

Verify, do not assume, the following:

- Required columns `pubid`, `question`, `context`, `long_answer`, `final_decision` are present.
- `context` is a struct with members `contexts`, `labels`, `meshes`, `reasoning_required_pred`, and `reasoning_free_pred`.
- `context.contexts` is a list of strings.
- `context.labels` is a list of strings.
- `context.meshes` is a list of strings.
- `context.reasoning_required_pred` is a list of strings.
- `context.reasoning_free_pred` is a list of strings.
- Column types match expectations: `pubid` is string-like or integer; `final_decision` is string-like.
- `final_decision` values are only `yes`, `no`, or `maybe`.
- `pubid` is present and non-empty for every row.
- `context.contexts` list lengths are between 1 and 9.
- No unexpected nulls in required fields.
- No empty `question` values in records treated as answerable.
- Row count matches expected PQA-L count from approved metadata.
- Configuration identity matches `pqa_labeled`.
- File and revision provenance are recorded.

Fail-closed behavior:
- Missing required column stops execution.
- Missing `context` struct member stops execution.
- Unexpected `final_decision` value stops execution.
- `pubid` missing or malformed at scale stops execution.
- Row count deviation without documented explanation stops execution.
- `labels` / `contexts` cardinality mismatch stops execution.

---

## A3 — Normalize source identity

Apply deterministic policy to derive `original_example_id` and `source_document_id`.

Decision tree:
1. If a stable native example identifier exists and is verified, use it.
2. Otherwise use the deterministic revision-bound source locator:
   - `dataset_id`
   - `dataset_revision`
   - `configuration`
   - artifact identity
   - row ordinal
   - `pubid`
3. Never use an unpinned dataframe index without source artifact identity.
4. Never use a runtime UUID.

`source_document_id` policy:
- Start from normalized `pubid`.
- Fail closed if `pubid` is missing or malformed.
- Fail closed if one `pubid` maps to multiple incompatible source documents.
- Fail closed if uniqueness assumptions are violated.

---

## A4 — Normalize question, context, answer, and decision

Normalization rules:
- `question`: strip surrounding whitespace only; preserve all other characters.
- `long_answer`: strip surrounding whitespace only; preserve all other characters.
- `final_decision`: map `yes` -> `yes`, `no` -> `no`, `maybe` -> `maybe`; no other mappings.
- `context.contexts`: preserve exact text, source order, and every entry in `NativeContextSegment` records; do not deduplicate or rewrite.
- `context.labels`: preserve exact source values and positional alignment with `context.contexts`; enforce `len(labels) == len(contexts)` in P01-03E.
- `context.meshes`: preserve exact values and source order in `mesh_terms`.
- `context.reasoning_required_pred` and `context.reasoning_free_pred`: preserve exact source values and multiplicity in `native_annotation_trace`.

Prohibited normalizations:
- Lowercasing.
- Collapsing clinically meaningful punctuation.
- Removing Unicode.
- Normalizing away negation.
- Reordering context.
- Removing citations.
- Paraphrasing abstracts.
- Summarizing context segments.
- Collapsing reasoning_* lists to a scalar without a verified cardinality rule.

---

## A5 — Populate internal source-record structures

Populate the internal `context_segments`, `mesh_terms`, and
`native_annotation_trace` structures deterministically. Only
`context.contexts` entries are candidates for later `PilotEvidence` mapping.
MeSH terms and reasoning annotation traces remain internal source metadata.

Map `context.contexts`, `context.labels`, `context.meshes`, `context.reasoning_required_pred`, and `context.reasoning_free_pred` records deterministically.

Rules:
- Preserve original context text, labels, MeSH terms, reasoning annotations exactly in raw local artifacts.
- No LLM rewriting.
- No summarization.
- No semantic sentence splitter requiring external models.
- Deterministic ordering: use row ordinal as stable index.
- Deterministic `evidence_id` payload excludes timestamps, paths, hostnames, runtime metadata, and split assignments.
- Explicit handling of empty context lists: produce zero context segments and mark unavailable in Layer 1.
- Duplicate text entries remain separate segments with distinct ordinals.
- `len(labels) == len(contexts)` is enforced in P01-03E; fail closed on mismatch.
- `meshes` are retained as document metadata, not evidence objects.
- `reasoning_required_pred` and `reasoning_free_pred` are retained as annotation traces, not model inputs.
- Source-document linkage is owned by the parent `PilotPubMedQASourceRecord`. `NativeContextSegment` and `NativeAnnotationTrace` do not duplicate `source_document_id`.

Do not assert that context elements are gold rationales. Record them as source-provided context segments.

---

## A6 — Apply honest target-field policy

For native Layer-1 records:

```text
decision: native final_decision
answer: native long_answer
claims: []
evidence_sufficiency: "not_annotated"
uncertainty: "not_annotated"
abstain: false
abstention_reason: null
```

`maybe` is not mapped to `abstain`. Abstention requires an explicit later annotation protocol.

Any future automatically derived claims must carry a non-gold annotation status and must not activate Layer-2 metrics.

---

## A7 — Construct provenance

Every transformed record must carry:

```text
transformation_version: approved transformation version string
annotation_method: "native" for native labels, "derived" for derived fields,
                    "manual" for manually annotated fields
annotation_revision: annotation protocol version or empty string
synthetic: false for real data
```

Operational provenance belongs in the acquisition manifest and transformation report, not in `PilotRecord`.

---

## A8 — Derive example IDs

Derivation payload (scientific identity only):

```text
dataset_id
dataset_revision
configuration
original_example_id
source_document_id
transformation_version
```

Excluded from identity:
- timestamps
- local paths
- hostname
- runtime duration
- hardware
- split assignment
- annotation UI state

Digest policy:
- Use full SHA-256 digest or an explicitly justified collision-safe representation.
- Do not silently continue using an arbitrary shortened digest without collision analysis.

---

## A9 — Construct or defer PilotRecord

For native unannotated rows:
- Construct `PilotPubMedQASourceRecord` Layer-1 representation.
- Populate `context_segments`, `mesh_terms`, and `native_annotation_trace` from the resolved P01-03D mapping.
- Compute `source_record_hash` from scientific identity fields only; exclude operational provenance, timestamps, local paths, hostnames, hardware, runtime durations, split assignments, and annotation UI state.
- Defer full `PilotRecord` construction until annotation authorization is granted.

For manually annotated rows:
- Construct full `PilotRecord` with annotated fields populated.
- Record annotation revision.

No silent upgrade from Layer 1 to full `PilotRecord` occurs without explicit authorization.

---

## A10 — Validate records

Run deterministic validation against every transformed record.

Required checks:
- `example_id` uniqueness within the dataset.
- Stable repeated derivation produces identical `example_id`.
- Valid `source_document_id` values.
- Revision and configuration match approved values.
- No runtime metadata in identity fields.
- Required source fields present.
- Allowed decision values only.
- Valid target semantics.
- Evidence IDs unique within record.
- Evidence references resolve.
- Schema version explicit.
- No raw-full-text or PDF content present.
- No raw content committed to Git.
- Unavailable fields are explicitly marked `not_annotated` or empty.
- Layer-2 metrics remain `not_applicable`.

Validation statuses:
```text
pass
fail
not_applicable
blocked
```

Every non-pass must include an explicit reason. No warning may be silently converted to success.

---

## A11 — Serialize canonical JSONL

- Output path: approved transformed-data location outside Git tracking.
- Format: one JSON object per line, deterministic key ordering, UTF-8, no pretty-printing.
- Byte-identical output for identical inputs and transformation version.
- No raw abstracts included.
- No backup to public artifact store.

---

## A12 — Generate transformation report

Report contents:
- acquisition manifest reference
- native schema validation results
- per-record validation statuses and reasons
- excluded-record ledger
- evidence-mapping statistics
- example-ID registry
- source-document-ID registry
- transformation version
- tool and environment identity
- timestamp for operational provenance only

---

## Storage boundary

Raw external data location:
- Outside tracked source directories.
- Listed in `.gitignore`.
- Local-only raw artifact policy.
- No raw abstract commitment.
- No raw abstract release.
- No inclusion in wheel or sdist.
- No backup to public artifact store.
- Cleanup and retention policy defined in future authorization.

## Acquisition manifest

Future immutable manifest fields:

| Field | Category |
|---|---|
| `dataset_id` | scientific identity |
| `repository_revision` | scientific identity |
| `configuration` | scientific identity |
| `artifact_path` | operational provenance |
| `artifact_size` | operational provenance |
| `sha256` | operational provenance |
| `acquisition_method` | operational provenance |
| `acquired_at` | operational provenance |
| `source_url` | operational provenance |
| `license_id` | scientific identity |
| `rights_notice_version` | scientific identity |
| `tool_version` | operational provenance |
| `environment_identity` | operational provenance |

Scientific identity fields must never change after acquisition. Operational provenance fields may be appended but not silently altered.

## Fail-closed checks

Execution must stop if:
- returned revision differs from pinned revision;
- configuration is missing;
- unexpected Python scripts are required;
- Parquet files differ from the approved allowlist;
- artifact hashes cannot be computed;
- rights metadata changes;
- raw content would be placed inside Git tracking;
- source schema differs materially from the approved transformation protocol.
