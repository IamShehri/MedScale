# MESC Pilot-01 — P01-03 Research Findings

Status: **research record**
Authorization: P01-03 planning authorized; execution not authorized
Freeze date: 2026-07-17

---

## Repository inspection scope

Read-only inspection was performed on the following repository paths:

```text
specs/mesc-pilot-01/README.md
specs/mesc-pilot-01/spec.md
specs/mesc-pilot-01/plan.md
specs/mesc-pilot-01/tasks.md
specs/mesc-pilot-01/data-contract.md
specs/mesc-pilot-01/evaluation-contract.md
specs/mesc-pilot-01/dataset-selection.md
specs/mesc-pilot-01/revision-lock.md
specs/mesc-pilot-01/risk-register.md
specs/mesc-pilot-01/acceptance.md

src/medscale/mesc/contracts.py
src/medscale/mesc/evaluation.py
src/medscale/mesc/manifests.py
src/medscale/mesc/split.py

src/medscale/dataset/
src/medscale/reproducibility.py
src/medscale/_layout.py
.gitignore
pyproject.toml
uv.lock

tests/test_mesc_contracts.py
tests/test_mesc_evaluation.py
tests/test_mesc_manifests.py
tests/test_mesc_split.py
tests/fixtures/mesc/pilot_smoke.jsonl
```

No modifications were made outside the P01-03 planning documentation allowlist.

---

## P01-02 terminology reconciliation

### Historical wording

P01-02 was titled "Dataset acquisition and immutable revision."

### Actual completed work

```text
Dataset selection: complete
Rights and license review: complete
Immutable repository revision lock: complete
Dataset acquisition: not performed
Dataset content retrieved: no
```

### Reconciled interpretation

```text
P01-02 CLOSED: Dataset identity, rights boundary, and immutable revision lock.

P01-03 PLANNING: Future acquisition, transformation, and validation execution protocol.

P01-T04 ACQUISITION: Still NOT AUTHORIZED.

P01-T05 TRANSFORMATION: Still NOT AUTHORIZED.
```

P01-02 did not download data, did not retrieve artifacts, and did not execute any dataset loading code. The "acquisition" wording in P01-02 referred to future protocol design, not completed acquisition.

---

## Source-to-contract field gap analysis

The following table compares native PubMedQA fields against the current `PilotRecord` contract.

| Pilot field | PubMedQA source | Native, derived, manually annotated, or unavailable |
|---|---|---|
| `dataset_id` | fixed repository identity | native metadata |
| `dataset_revision` | revision lock | native metadata |
| `configuration` | `pqa_labeled` | native metadata |
| `original_example_id` | must be resolved | unresolved until protocol decision |
| `source_document_id` | likely derived from `pubid` | requires uniqueness policy |
| `question` | `question` | native |
| `evidence` | `context` | native but normalization required |
| `decision` | `final_decision` | native gold label |
| `answer` | `long_answer` | native |
| `claims` | none | unavailable until annotation |
| `evidence_sufficiency` | none | unavailable |
| `uncertainty` | none | unavailable |
| `abstain` | none | unavailable as native gold |
| `abstention_reason` | none | unavailable |
| transformation provenance | transformation process | derived |
| annotation provenance | native/manual status | mixed |

### Non-fabrication findings

The following fields cannot be derived from native PubMedQA without explicit later authorization:

- Atomic gold claims from `long_answer`
- Sentence-level gold evidence rationales from `context`
- Native abstention labels
- Native gold evidence-sufficiency labels
- Native gold uncertainty labels

The current mandatory `evidence_sufficiency` and `uncertainty` fields in `PilotTarget` create a real schema gap for unannotated PubMedQA rows. Any transformation that fills these fields without explicit annotation authorization would fabricate scientific metadata.

---

## Licensing and rights constraints

- PubMedQA repository license: MIT (repository/package metadata)
- MIT package metadata does not transfer copyright in underlying PubMed abstracts
- Raw abstracts must not be committed to MedScale
- Raw abstracts must not be republished or redistributed by MedScale
- Local research acquisition requires later explicit authorization
- SciFact: CC BY-NC 2.0, commercial use prohibited, remote-code execution required

---

## Source-identity risks

- `pubid` may be missing or malformed in unknown rows
- One `pubid` may map to multiple source documents in edge cases
- `original_example_id` must not be an unpinned dataframe index
- No runtime UUID may be used in identity fields
- Identity must be reproducible across environments and transformation versions

---

## Alternative transformation strategies

Three options were evaluated:

### Option A — Schema-v2 explicit unannotated state

Plan a later separately authorized schema revision adding explicit values such as `not_annotated` for `evidence_sufficiency` and `uncertainty`.

- Requires schema version increment
- Requires migration/compatibility policy
- No silent reinterpretation of v1
- No implementation in this task

### Option B — Two-stage record model

Plan an internal normalized PubMedQA source-record representation for Layer 1, followed by conversion to full `PilotRecord` only after manual annotation supplies required grounding fields.

- No duplicate public contract root
- Source-record type remains internal
- Exact boundary between native labels and research annotations
- No implementation in this task

### Option C — Restrict full `PilotRecord` transformation

Transform only the manually reviewed grounding subset into full `PilotRecord`; retain the rest of PQA-L in an external/native Layer-1 format.

- Clear Layer-1 runner implications
- No misleading claim that all rows are fully grounded records
- No implementation in this task

### Selected recommendation

**Option B** is recommended. It preserves the single public `PilotRecord` contract, maintains a clear internal boundary for unannotated native records, and does not require silent schema version inflation or misleading completeness claims.
