# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** Implemented / Merged / Closed

## Evidence inventory

Documents inspected for ALIGN-14 selection:
- `ROADMAP.md`
- `specs/public-repository-alignment/spec.md`
- `specs/public-repository-alignment/phase2-boundary-audit.md`
- `docs/execution/v0.2/final_release_audit.md`
- `docs/execution/v0.2/milestone_tracker.md`
- `docs/architecture/openmed_capability_analysis.md`
- `docs/execution/v0.2/dataset_v1.md`
- `docs/adr/0031-deterministic-dataset-contract-boundary.md`
- `src/medscale/dataset/__init__.py`
- `src/medscale/dataset/split.py`

Key findings:
- ALIGN-13 closed a deterministic dataset-builder contract boundary without defining split-assignment freeze semantics.
- `tests/test_dataset_builder.py` exists and covers ALIGN-13 contract/manifest/fingerprint behavior.
- `src/medscale/dataset/split.py` already provides deterministic split computation.
- `medscale.dataset.builder.DatasetReleaseManifest` already records immutable release metadata.
- No `ALIGN-14` identifier or authorized successor exists in repository documents.

## Candidate scoring — corrected

### C1 — Dataset split-assignment freeze contract

| Criterion | Weight | Score | Rationale |
|---|---|---:|---|
| Direct dependency on ALIGN-13 | 20 | 18 | Uses ALIGN-13 contracts/manifest/fingerprint; splitter already exists |
| Research and publication value | 20 | 18 | Freeze identity enables citation-stable dataset releases |
| Reproducibility value | 15 | 15 | Deterministic identity from explicit inputs only |
| Architectural necessity | 15 | 14 | Fills the gap between mutable generation and immutable release |
| Narrow implementable scope | 15 | 14 | Two production files + one test file |
| Low compatibility risk | 10 | 9 | Additive facade delta only |
| Low infrastructure cost | 5 | 5 | No runtime, storage, or network additions |
| **Total** | **100** | **93** | |

### C2 — Evidence contract boundary

| Criterion | Weight | Score | Rationale |
|---|---|---:|---|
| Direct dependency on ALIGN-13 | 20 | 5 | Independent of dataset-builder contracts |
| Research and publication value | 20 | 16 | Evidence contracts are publication-relevant |
| Reproducibility value | 15 | 14 | Adds determinism to evidence layer |
| Architectural necessity | 15 | 12 | Useful but not blocking downstream capability |
| Narrow implementable scope | 15 | 10 | Duplicate-contract ownership risk |
| Low compatibility risk | 10 | 7 | Facade risk from competing roots |
| Low infrastructure cost | 5 | 4 | Duplicate resolution required first |
| **Total** | **100** | **68** | |

### C3 — v0.2 release-hygiene ADR/documentation package

| Criterion | Weight | Score | Rationale |
|---|---|---:|---|
| Direct dependency on ALIGN-13 | 20 | 0 | Orthogonal governance cleanup |
| Research and publication value | 20 | 8 | Improves auditability and citation |
| Reproducibility value | 15 | 6 | No new determinism semantics |
| Architectural necessity | 15 | 6 | Hygiene, not capability delivery |
| Narrow implementable scope | 15 | 14 | Documentation-only changes |
| Low compatibility risk | 10 | 10 | No runtime surface touched |
| Low infrastructure cost | 5 | 5 | Docs changes only |
| **Total** | **100** | **49** | |

### C4 — FHIR grammar/validation expansion

| Criterion | Weight | Score | Rationale |
|---|---|---:|---|
| Direct dependency on ALIGN-13 | 20 | 4 | Weak dependency; FHIR path largely independent |
| Research and publication value | 20 | 14 | T2 roadmap item |
| Reproducibility value | 15 | 13 | Validation reports are frozen |
| Architectural necessity | 15 | 13 | Needed eventually |
| Narrow implementable scope | 15 | 6 | Blocked by JRE + HL7 validator |
| Low compatibility risk | 10 | 7 | External validator optional |
| Low infrastructure cost | 5 | 2 | Blocked; infrastructure cost high |
| **Total** | **100** | **59** | |

### C5 — Reproducibility namespace consolidation

| Criterion | Weight | Score | Rationale |
|---|---|---:|---|
| Direct dependency on ALIGN-13 | 20 | 6 | Indirect; ADR-0014 already proposed |
| Research and publication value | 20 | 12 | Improves reproducibility narrative |
| Reproducibility value | 15 | 14 | High on principle |
| Architectural necessity | 15 | 12 | UX improvement, not capability blocker |
| Narrow implementable scope | 15 | 8 | Wider blast radius |
| Low compatibility risk | 10 | 7 | Backward-compat aliases reduce risk |
| Low infrastructure cost | 5 | 2 | Requires broad refactor |
| **Total** | **100** | **59** | |

## Overlap analysis

- Existing `DeterministicSplitter` computes assignments. ALIGN-14 does not reimplement this.
- Existing `SplitResult` carries computed assignments. ALIGN-14 does not replace it.
- Existing `DatasetReleaseManifest` records release metadata. ALIGN-14 does not duplicate it.
- The remaining gap is a deterministic, immutable freeze record that identifies exact assignments for release reference.

## Assumptions

- The freeze contract can rely on `medscale.reproducibility` primitives only.
- No additional storage, export, publication, or CLI surface is needed.
- Formal release-manifest integration is deferred to a later capability or ADR.

## Implementation evidence required later

- None in planning scope; ADR-0032 resolves the schema version, empty-assignment semantics, and release-integration boundary.
