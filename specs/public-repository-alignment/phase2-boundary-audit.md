# Public Repository Alignment — Phase 2 Evidence/Dataset Boundary Audit

## 1. Executive decision
- Status: GO conditionally
- Decision: The minimum dependency-complete slice is a small contract-and-fingerprint-only subset under `src/medscale/dataset/builder` and `src/medscale/dataset/schema`.
- Boundary: No implementation, imports, tests, or capability PR is authorized by this audit. ALIGN-13 remains pending explicit founder approval.

## 2. Canonical baseline
- Current `origin/main`: `0f9a2d3`
- History includes merged PRs: `#4`, `#5`, `#6`
- Governance documents read from current `origin/main`:
  - `specs/public-repository-alignment/spec.md`
  - `specs/public-repository-alignment/plan.md`
  - `specs/public-repository-alignment/tasks.md`
- Stale baseline note: merged governance docs still reference older baseline SHAs; this audit uses the canonical `0f9a2d3` only.

## 3. Original workspace preservation evidence
- Path: `C:\Users\Shehr\OneDrive\Desktop\MedScale`
- Branch: `main`
- Local HEAD: `d2e651a55c92f2218aca49acaa5b7bd18a75f096`
- Modified tracked files: 6
- Untracked files: 228
- Deleted tracked files: 0
- Renamed tracked files: 0
- Mutating commands used: none
- Status: preserved as read-only evidence only.

## 4. Audit method
- Read-only Git and filesystem evidence from original workspace and canonical `origin/main`
- Static path and text inspection of candidate files; no module execution
- No candidate imports
- No file copies into a capability branch

## 5. Canonical public inventory
Canonical `main` already contains the foundation layer needed for the recommended slice:
- `src/medscale/reproducibility.py`: `canonical_json`, `content_hash`, `set_global_seed`
- canonical `dataset` surface: `__init__.py`, `compat.py`, `generate.py`, `licenses.py`, `manifest.py`, `schema.py`, `snapshot.py`, `split.py`, `validate.py`
- canonical `evidence` surface: `__init__.py`, `grading.py`, `models.py`, `protocol.py`

The proposed minimum slice can import only canonical deterministic primitives and remain additive.

## 6. Local candidate inventory
Candidate directories/files from the original workspace:
- `src/medscale/evidence/contract.py`
- `src/medscale/dataset/builder/*`
- `src/medscale/dataset/connectors/*`
- `src/medscale/dataset/governance/*`
- `src/medscale/validation/*`
- related tests: `tests/test_evidence_*.py`, `tests/test_dataset_*.py`, `tests/test_validation_*.py`

Tracked-only delta relevant as evidence:
- `src/medscale/evidence/__init__.py` public-export expansion from untracked `evidence/contract.py`

Canonical status check confirms:
- `src/medscale/dataset/schema.py`: exists on canonical `main`
- `src/medscale/dataset/manifest.py`: exists on canonical `main`
- `src/medscale/reproducibility.py`: exists on canonical `main`
- `src/medscale/dataset/builder/*`: not on canonical `main`
- `src/medscale/evidence/contract.py`: not on canonical `main`
- `src/medscale/validation/*`: not on canonical `main`

## 7. Dependency graph findings
Minimum dependency-complete component:
- `src/medscale/dataset/builder/contracts.py`
- `src/medscale/dataset/builder/manifest.py`
- `src/medscale/dataset/builder/fingerprint.py`
- supported by canonical `src/medscale/dataset/schema.py`
- supported by canonical `src/medscale/reproducibility.py`

Key constraints found from static inspection:
- `dataset/builder/*` may depend on canonical reproducibility utilities; those are already public and stable
- `dataset/builder/pipeline.py`, `release_packager.py`, and `export_artifacts.py` introduce ordering, packaging/runtime concerns and are excluded from the minimum slice
- `dataset/connectors/*` introduces external-source dependencies and is excluded
- `validation/*`, `evidence/contract.py`, and `dataset/governance/*` expand the governance surface and are excluded from the initial PR

No confirmed dependency on:
- `medscale.evaluation`
- `medscale.models`
- model execution
- evaluation execution
- training
- cloud SDKs
- schedulers
- HTTP/network clients
- external APIs

## 8. Duplicate-contract analysis
Duplicate or competing contract surfaces:
- `src/medscale/dataset/builder/contracts.py`
- `src/medscale/dataset/governance/contracts.py`
- `src/medscale/evidence/contract.py`
- tracked local export expansion in `src/medscale/evidence/__init__.py`

Recommendation: one public contract root for the first PR at `dataset.builder.contracts`. Do not expose `dataset.governance` or `evidence/contract.py` publicly in the initial capability-import PR.

## 9. Recommended minimum slice
Implementation allowlist:
- `src/medscale/dataset/__init__.py`
- `src/medscale/dataset/schema.py`
- `src/medscale/dataset/builder/__init__.py`
- `src/medscale/dataset/builder/contracts.py`
- `src/medscale/dataset/builder/manifest.py`
- `src/medscale/dataset/builder/fingerprint.py`

Test allowlist:
- `tests/test_dataset_builder.py`
- `tests/test_evidence_contract.py`

Exact exclusions:
- `src/medscale/dataset/builder/pipeline.py`
- `src/medscale/dataset/builder/release_packager.py`
- `src/medscale/dataset/builder/export_artifacts.py`
- `src/medscale/dataset/builder/audit.py`
- `src/medscale/dataset/builder/layout.py`
- `src/medscale/dataset/builder/errors.py`
- `src/medscale/dataset/connectors/**`
- `src/medscale/dataset/governance/**`
- `src/medscale/validation/**`
- `src/medscale/evidence/contract.py`
- `src/medscale/evidence/grading.py`
- `src/medscale/evidence/models.py`
- `src/medscale/evidence/protocol.py`
- evaluation, model, training, orchestration, MESC, strategy, and execution files

## 10. Public / experimental / internal matrix
- Public: `DatasetBinding`, `ManifestRecord`, `FingerprintInput`, schema version constant, stable factory helpers in `dataset.builder`
- Experimental: none in the minimum slice
- Internal: schema helpers, normalization helpers, internal hashing details not re-exported at top-level facade

## 11. Schema and serialization analysis
- Schema uses deterministic field order and JSON-compatible structures
- Serialization targets canonical JSON stable output
- No timestamps, environment paths, or runtime metadata are embedded in the minimum slice implementation scope
- Deterministic outputs are expected when implementations rely on canonical reproducibility utilities and sorted artifacts
- Validation before PR is required to confirm identical inputs yield identical outputs

## 12. Facade and packaging impact
- No top-level `medscale.__all__` expansion required
- No new runtime dependencies declared
- No new console scripts
- Wheel impact: new package files only
- Clean-wheel import verification required after implementation

## 13. Required tests
Exact proposed tests:
- `tests/test_dataset_builder.py::test_manifest_round_trip_is_deterministic`
- `tests/test_dataset_builder.py::test_fingerprint_stability`
- `tests/test_evidence_contract.py::test_dataset_binding_schema_version`
- `tests/test_evidence_contract.py::test_public_imports_only_allowlist`

Clean-wheel smoke and schema freeze tests remain required.

## 14. ADR decision
Result: ADR REQUIRED BEFORE IMPLEMENTATION
Rationale:
- The slice creates a new public dataset-contract surface within an existing package
- It establishes fingerprint/manifest ownership and compatibility policy
- It affects how later dataset/governance PRs may expand exports
- This aligns with existing ADR governance in canonical `main`

## 15. Risk register
| Risk | Severity | Evidence | Mitigation | Blocks capability PR |
|:---|:---|:---|:---|:---|
| Duplicate contract roots | High | multiple `contracts.py` files | freeze one public root only | Yes |
| Hidden execution assumptions | High | large execution layer nearby | exclude connectors and pipeline | Yes |
| Schema churn later | Medium | neighboring uncleared development files | ADR + schema freeze audit | No |
| Packaging expansion | Medium | new files only | no dependency/version changes | No |
| Public export drift | Medium | tracked `evidence/__init__.py` adds new exports | explicit allowlist tests | No |
| Provenance risk | Medium | dirty workspace is evidence only | static audit, no imports | No |

## 16. Capability PR GO/NO-GO
Result: GO conditionally
- The minimum slice is finite, dependency-complete, deterministic, offline, and separable from execution
- It remains blocked until:
  - an approved ADR is merged
  - explicit founder approval is recorded
  - ALIGN-12 audit is reviewed
  - exact file/test allowlist above is confirmed

Proposed branch name: `chore/phase2-dataset-contract-foundation`
Proposed PR title: `feat(dataset): add evidence/dataset foundation contracts`
Proposed commit structure: one commit if inseparable; two commits if formatting and contract freeze are separable

## 17. Proposed implementation sequence
1. Merge this audit PR.
2. Create and approve the required ADR.
3. Obtain explicit founder approval for the exact allowlist above.
4. Implement only `dataset.__init__`, `schema.py`, `builder` contract/manifest/fingerprint files.
5. Implement the four exact proposed tests.
6. Run full canonical verification.
7. Stop; do not proceed to connectors, governance, validation, evaluation, models, or execution in the same PR.

## 18. Explicit non-authorization statement
This audit does not authorize capability implementation. ALIGN-13 remains pending. No capability-import branch may be created until this audit PR is reviewed, CI-green, merged, ADR approved, and founder approval is recorded.
