# MESC Pilot-01 — P01-03 Decision Record

Status: **planning decisions**
Authorization: P01-03 authorized; execution not authorized
Freeze date: 2026-07-17

---

## Selected acquisition mechanism

**Selected:** revision-pinned Hugging Face Hub file download restricted to approved Parquet and metadata files.

Rationale:
- Supports immutable revision pinning.
- No remote code execution.
- Exact file allowlisting possible.
- Resume and integrity behavior supported via SHA256 verification.
- No need to add unnecessary repository dependencies beyond existing `huggingface_hub` if already present; if absent, acquisition command must be run in an explicitly authorized separate environment outside the MedScale locked dependency set.

Invariant:
- `trust_remote_code=True` is prohibited.
- PubMedQA acquisition must use the pinned Parquet repository representation without executing arbitrary remote dataset loading code.

Rejected alternatives:
- `datasets.load_dataset` with `trust_remote_code=True`: rejected because it executes arbitrary Python loading scripts and violates the no-remote-code boundary.
- `snapshot_download` without file allowlisting: rejected because it may retrieve unknown repository contents.
- Direct mutable-branch download: rejected because mutable branch names do not provide immutable revision guarantees.

---

## Selected schema-gap strategy

**Selected:** Option B — Two-stage record model.

Rationale:
- Preserves a single public `PilotRecord` contract.
- Maintains an explicit internal boundary between native PubMedQA labels and research annotations.
- Does not require silent schema version inflation.
- Does not mislead consumers into believing all rows are fully grounded records.
- Native unannotated rows remain in an internal `PilotPubMedQASourceRecord` representation until manual annotation is separately authorized.

Rejected alternatives:
- Option A — Schema-v2 explicit unannotated state: rejected because it would require a schema version increment and silent reinterpretation risk before annotation is actually performed.
- Option C — Restrict full `PilotRecord` transformation: rejected because it would create two public contract roots and complicate the deterministic runner contract.

---

## Selected source identity policy

**Selected:** deterministic normalization of `pubid` to `source_document_id`, with fail-closed rules.

Rules:
- `pubid` must be present and well-formed.
- One `pubid` maps to exactly one source document.
- Uniqueness violations stop execution.
- No random suffixes appended silently.
- Fallback example locator includes immutable revision, configuration, source artifact identity, row ordinal, and `pubid`.

---

## Selected example-ID policy

**Selected:** deterministic derivation payload over full SHA-256 digest, with explicit collision-safe representation requirement.

Payload:
```text
dataset_id
dataset_revision
configuration
original_example_id
source_document_id
transformation_version
```

Excluded:
- timestamps
- local paths
- hostname
- runtime duration
- hardware
- split assignment
- annotation UI state

Shortened digests are not permitted without an explicit collision analysis documented in a separately authorized amendment.

---

## Selected native-context mapping decision

**Selected:** positional ordered segment mapping for `context.contexts`, `context.labels`, `context.meshes`, `context.reasoning_required_pred`, and `context.reasoning_free_pred`.

Rationale:
- All five members are present in all `1000` rows in the merged P01-03C verified report.
- `context.contexts` contains the structured abstract excluding its conclusion.
- `long_answer` contains the abstract conclusion.
- `final_decision` is the only native consensus target decision.
- `meshes` are document-topic metadata derived from Medical Subject Headings.
- `reasoning_required_pred` preserves the annotation made using question and context.
- `reasoning_free_pred` preserves the annotation made using question, context, and long_answer.
- No field may be silently discarded or semantically reinterpreted.

Rules:
- `contexts` entries map to ordered `NativeContextSegment` objects with `ordinal`, `text`, and `section_label`.
- Preserve every entry, preserve source order, preserve exact text, do not summarize, rewrite, split, merge, or deduplicate.
- Duplicate text entries remain separate segments with distinct ordinals.
- `labels[i]` maps to `context_segments[i].section_label`.
- Require `len(labels) == len(contexts)` during P01-03E; any cardinality mismatch must fail closed.
- `meshes` map to `mesh_terms: tuple[str, ...]` and are excluded from default model input.
- `reasoning_required_pred` and `reasoning_free_pred` map to `native_annotation_trace` and are not used as model inputs, targets, or scoring signals.
- `final_decision` remains the only native consensus target; `maybe` is not converted to abstain.
- This decision supersedes the prior generic deduplication assumption for PubMedQA context entries.

---

## Selected raw-data storage boundary

**Selected:** raw artifacts stored outside tracked source directories, listed in `.gitignore`, local-only, excluded from wheel and sdist, with cleanup and retention policy defined in future acquisition authorization.

Prohibited actions:
- Committing raw abstracts to MedScale.
- Republishing or redistributing raw abstracts.
- Backing up raw artifacts to public artifact stores.
- Including raw artifacts in distribution packages.

---

## Rejected alternatives summary

| Decision | Rejected alternative | Reason |
|---|---|---|
| Acquisition mechanism | `datasets.load_dataset` with remote code | Violates no-remote-code boundary |
| Acquisition mechanism | `snapshot_download` without allowlist | May retrieve unknown contents |
| Schema-gap strategy | Option A schema-v2 explicit values | Requires premature version inflation |
| Schema-gap strategy | Option C two public contracts | Complicates runner contract |
| Evidence mapping | LLM-derived atomic claims | Fabricates gold annotations |
| Evidence mapping | sentence splitters | Requires external models |
| Data reuse | promote SciFact to primary | Violates frozen primary decision |
| Abstention mapping | map `maybe` to `abstain` | Fabricates abstention labels |

---

## Consequences

- P01-03 execution remains blocked pending separate founder authorization for acquisition and transformation.
- The two-stage record model requires an explicit annotation authorization before any Layer-2 metric is treated as ground truth.
- The source-document identity policy may surface `pubid` uniqueness violations that require dataset-level exclusion rules in a future authorization.
- The full-digest example-ID policy increases identifier length but eliminates collision risk.
- SciFact remains auxiliary only; it does not acquire, transform, or execute under this planning package.

---

## Exact future authorization gates

P01-03A PLANNING AUTHORIZATION: GRANTED
P01-03A EXECUTION AUTHORIZATION: NOT AUTHORIZED — requires a separate explicit governance decision.

P01-03B PLANNING AUTHORIZATION: GRANTED
P01-03B EXECUTION AUTHORIZATION: NOT AUTHORIZED — requires a separate explicit governance decision.

P01-03C PLANNING AUTHORIZATION: GRANTED
P01-03C EXECUTION AUTHORIZATION: NOT AUTHORIZED — requires a separate explicit governance decision.

P01-03D PLANNING AUTHORIZATION: GRANTED
P01-03D EXECUTION AUTHORIZATION: NOT AUTHORIZED — requires a separate explicit governance decision.

P01-03E PLANNING AUTHORIZATION: GRANTED
P01-03E EXECUTION AUTHORIZATION: NOT AUTHORIZED — requires a separate explicit governance decision.

P01-03F PLANNING AUTHORIZATION: GRANTED
P01-03F EXECUTION AUTHORIZATION: NOT AUTHORIZED — requires a separate explicit governance decision.

P01-03G PLANNING AUTHORIZATION: GRANTED
P01-03G EXECUTION AUTHORIZATION: NOT AUTHORIZED — requires a separate explicit governance decision.

No gate is opened automatically by documentation acceptance, pull-request creation, pull-request merge, technical readiness, passing validation, or completion of an earlier Pilot-01 stage.
