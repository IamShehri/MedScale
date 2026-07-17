# MESC Pilot-01 -- P01-03 Acceptance Criteria

Status: **planning acceptance record**
Authorization: P01-03 documentation-planning only. Execution not authorized.
Freeze date: 2026-07-17

---

## Planning acceptance

All of the following must be true for P01-03 planning to pass:

- All required planning documents are present and non-empty.
- The schema-gap resolution strategy is explicitly selected and justified.
- No fabricated annotations or unsupported claims appear in the planning package.
- The acquisition protocol is fail-closed at every documented boundary.
- The transformation protocol preserves scientific identity and does not introduce unavailable annotation fields.
- The validation protocol reports unavailable metrics as `not_applicable`.
- Top-level registry documents are reconciled without altering protected authority documents.
- Repository quality gates pass on the planning worktree.

## Execution readiness

Planning acceptance does not imply execution authorization.

The planning package passes while execution remains blocked if:

- Separate founder authorization for acquisition has not been recorded.
- Separate founder instruction for transformation has not been recorded.
- The schema-gap annotation protocol has not been authorized.
- The raw-data storage boundary has not been confirmed in the repository.

## Separate execution readiness assessment

```text
READY FOR DOCUMENTATION REVIEW ONLY -- EXECUTION IS NOT AUTHORIZED.

Documentation completeness: READY FOR DOCUMENTATION REVIEW
Semantic consistency: READY FOR DOCUMENTATION REVIEW
Execution readiness: NOT ASSESSED OR AUTHORIZED
Dataset acquisition authorization: NOT AUTHORIZED
Experiment execution authorization: NOT AUTHORIZED
Training authorization: NOT AUTHORIZED
Release or publication authorization: NOT AUTHORIZED

Passing this acceptance review, opening the documentation pull request, or merging the documentation pull request does not authorize dataset acquisition or any execution activity. A separate explicit governance decision is required before each execution stage.
```

---

## Planning checklist

- [ ] `specs/mesc-pilot-01/p01-03/README.md` present and non-empty.
- [ ] `specs/mesc-pilot-01/p01-03/research.md` present and non-empty.
- [ ] `specs/mesc-pilot-01/p01-03/spec.md` present and non-empty.
- [ ] `specs/mesc-pilot-01/p01-03/plan.md` present and non-empty.
- [ ] `specs/mesc-pilot-01/p01-03/data-model.md` present and non-empty.
- [ ] `specs/mesc-pilot-01/p01-03/execution-protocol.md` present and non-empty.
- [ ] `specs/mesc-pilot-01/p01-03/decision-record.md` present and non-empty.
- [ ] `specs/mesc-pilot-01/p01-03/acceptance.md` present and non-empty.
- [ ] Schema-gap resolution explicitly selected and documented.
- [ ] Acquisition mechanism fail-closed at every boundary.
- [ ] Source identity policy deterministic and fail-closed.
- [ ] Example-ID policy deterministic and collision-safe.
- [ ] Evidence mapping preserves original text and does not fabricate gold rationales.
- [ ] Validation protocol reports unavailable fields as `not_applicable`.
- [ ] No dataset download, transformation, inference, retrieval, baseline, or training occurred.
- [ ] Documentation commit, push, and PR creation are separately authorized and recorded; PR #23 remains open and unmerged, auto-merge remains disabled, and no tag, release, or execution activity occurred.
- [ ] Top-level registry documents reconciled.
- [ ] Repository quality gates pass.

---

## Governance record

```text
Governance decision: DOCUMENTATION REVIEW ONLY
Execution authorization: NOT AUTHORIZED
Authorization record: NO EXECUTION AUTHORIZATION RECORDED
Authorization authority: REQUIRES A SEPARATE EXPLICIT GOVERNANCE DECISION
Effective execution date: NOT APPLICABLE -- EXECUTION NOT AUTHORIZED
Dataset acquisition: NOT AUTHORIZED
Model or embedding-model download: NOT AUTHORIZED
Remote code: NOT AUTHORIZED
Inference, retrieval, baselines, and annotation: NOT AUTHORIZED
QLoRA, training, and adapter merge: NOT AUTHORIZED
Release, publication, production, clinical use, and Afia integration: NOT AUTHORIZED
```

Acceptance of this documentation package records documentation readiness only. It grants no execution authority. Every future execution stage requires a separate explicit governance decision after this package is reviewed and merged.

Founder-frozen model selection authority is recorded in `model-selection.md`. Hermes authority is repository implementation and verification only.
