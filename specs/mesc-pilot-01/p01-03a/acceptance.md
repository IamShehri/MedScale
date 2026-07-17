# MESC Pilot-01 -- P01-03A Acceptance Criteria

Freeze date: 2026-07-17

## Readiness-package acceptance

All of the following must be true for the P01-03A readiness package to pass:

- [x] All required readiness documents are present and non-empty.
- [x] Dataset identity is frozen to `qiaojin/PubMedQA`, configuration `pqa_labeled`, revision `9001f2853fb87cab8d220904e0de81ac6973b318`.
- [x] Rights and redistribution boundaries are explicitly recorded and match committed authority documents.
- [x] `.gitignore` gap is recorded as a readiness issue without being masked as acceptable.
- [x] Task-registry finding is recorded without altering the registry.
- [x] Proposed storage boundary is documented with read-only evidence only.
- [x] Directory creation was not performed during readiness turn.
- [x] No remote dataset access, remote metadata query, hugging face API call, or dataset file enumeration occurred.
- [x] Artifact allowlist distinguishes frozen identity from unverified remote filenames.
- [x] Acquisition protocol is non-executable and separated from later stages.
- [x] Risk register covers revision, configuration, artifact selection, remote code, storage, rights, and governance misinterpretation risks.
- [x] No placeholder, invented hash, invented filename, or invented authorization date remains.
- [x] Repository quality gates pass on the readiness worktree.

## Acquisition-authorization readiness

The readiness package may pass documentation acceptance while actual acquisition remains blocked.

Readiness conclusion:

```text
NOT READY FOR ACQUISITION AUTHORIZATION -- BLOCKERS RECORDED
```

The package is ready for founder review of the recorded blockers and proposed remediation sequence. It is not ready for authorization of P01-03B acquisition.

Acquisition-authorization readiness is blocked by:

* `pending storage-boundary permission verification`
* `retention and cleanup policy unresolved`

Resolved blockers:

* `exact remote filename allowlist` -- verified via metadata API in separate authorized turn
* `metadata-only remote verification authorization` -- authorized and completed
* `.gitignore` guardrail implementation -- merged as PR #26

## Planning checklist

- [x] `specs/mesc-pilot-01/p01-03a/README.md` present and non-empty.
- [x] `specs/mesc-pilot-01/p01-03a/research.md` present and non-empty.
- [x] `specs/mesc-pilot-01/p01-03a/authorization-request.md` present and non-empty.
- [x] `specs/mesc-pilot-01/p01-03a/storage-boundary.md` present and non-empty.
- [x] `specs/mesc-pilot-01/p01-03a/artifact-allowlist.md` present and non-empty.
- [x] `specs/mesc-pilot-01/p01-03a/acquisition-protocol.md` present and non-empty.
- [x] `specs/mesc-pilot-01/p01-03a/risk-register.md` present and non-empty.
- [x] `specs/mesc-pilot-01/p01-03a/decision-record.md` present and non-empty.
- [x] Frozen dataset identity documented and consistent across package.
- [x] Rights boundaries documented and consistent with committed authority.
- [x] Storage path documented as external to all worktrees, repositories, and synchronized trees.
- [x] Acquisition protocol fail-closed at every boundary.
- [x] No execution activity authorized or performed.
- [x] No dataset download, transformation, inference, retrieval, baseline, or training occurred.
- [x] No directory creation under proposed raw-data root.
- [x] No Parquet file opened or schema inspected.
- [x] Repository quality gates pass.

## Governance record

```text
Governance decision: P01-03A READINESS PACKAGE IN REVIEW
Execution authorization: NOT AUTHORIZED
Acquisition authorization: NOT AUTHORIZED
P01-03B authorization: NOT AUTHORIZED
P01-03C and later authorization: NOT AUTHORIZED
Authorization record: NO EXECUTION OR ACQUISITION AUTHORIZATION RECORDED
Authorization authority: REQUIRES A SEPARATE EXPLICIT GOVERNANCE DECISION
Effective acquisition date: NOT APPLICABLE -- ACQUISITION NOT AUTHORIZED
Dataset acquisition: NOT AUTHORIZED
Model or embedding-model download: NOT AUTHORIZED
Remote code: NOT AUTHORIZED
Inference, retrieval, baselines, and annotation: NOT AUTHORIZED
QLoRA, training, and adapter merge: NOT AUTHORIZED
Release, publication, production, clinical use, and Afia integration: NOT AUTHORIZED
```

Acceptance of this readiness package records documentation readiness only. It grants no acquisition or execution authority. Every future dataset acquisition, transformation, experiment, training, or release stage requires a separate explicit governance decision.

Founder-frozen model selection authority is recorded in `model-selection.md`. Hermes authority is repository implementation and verification only.
