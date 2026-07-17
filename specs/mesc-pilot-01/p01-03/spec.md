# MESC Pilot-01 — P01-03 Spec

Status: **planning specification**
Authorization: P01-03 planning authorized; execution not authorized
Freeze date: 2026-07-17

---

## Problem

P01-02 locked the PubMedQA dataset identity, rights boundary, and immutable revision. The dataset remains unacquired and untransformed. A deterministic, rights-preserving, schema-honest acquisition and transformation protocol is required before any execution can occur.

The core problem is not data access; it is defining a protocol that:
- respects the immutable revision and MIT package-rules boundary;
- does not fabricate annotations that PubMedQA does not provide;
- produces reproducible `PilotRecord` outputs;
- preserves scientific identity across transformation versions; and
- stops execution whenever a fail-closed condition is met.

## Objectives

1. Define a deterministic future acquisition protocol for the pinned PubMedQA `pqa_labeled` Parquet artifacts.
2. Define a deterministic future transformation from native PubMedQA schema to `PilotRecord` without fabricating unavailable annotations.
3. Define validation rules that catch schema drift, rights violations, identity collisions, and nondeterminism before any record is considered accepted.
4. Define the handoff package for P01-04 split assignment and leakage audit.
5. Record the schema-gap resolution strategy so that future execution is honest about what is native, derived, and unavailable.

## Scope

In scope:
- Future acquisition of the pinned PubMedQA Parquet artifacts under separate authorization.
- Future deterministic transformation of acquired Parquet rows into normalized Layer-1 source records and, after annotation, full `PilotRecord` records.
- Future validation of native schema, derived identity, evidence mapping, and serialization determinism.
- Future P01-04 handoff package specification.
- Documentation of schema-gap options and selected resolution.

Out of scope:
- Any dataset download, inspection, or transformation in this turn.
- Any model access, inference, retrieval, baseline execution, or training.
- Any annotation tooling implementation or gold-subset creation.
- Any modification to protected source, test, workflow, or dependency files.
- Any commit, push, PR, merge, tag, or release.

## Non-goals

- Do not reopen model selection or dataset selection.
- Do not replace PubMedQA with another dataset.
- Do not promote SciFact to the primary dataset.
- Do not add runtime dependencies or modify `uv.lock`.
- Do not claim that PubMedQA `context` entries are sentence-level gold rationales.
- Do not derive atomic claims from `long_answer` and label them as gold.
- Do not map `maybe` to `abstain` without an explicit later annotation protocol.
- Do not execute B0, B1, B2, or B3.
- Do not run an Evidence Judge.

## Invariants

- The immutable revision `9001f2853fb87cab8d220904e0de81ac6973b318` is fixed for P01-03 planning and future P01-03 execution.
- Raw PubMed abstracts must not be committed to MedScale, republished, or redistributed.
- Scientific identity fields must never contain timestamps, local paths, hostnames, runtime durations, hardware identifiers, or split assignments.
- `content_hash` must be computed only over scientific identity fields.
- Split assignment must remain external to `PilotRecord` scientific identity.
- Every unavailable metric or annotation must be represented explicitly as `not_applicable`, not silently omitted.
- Layer 2 metrics remain `not_applicable` until the manually reviewed gold subset is complete.

## Outputs

Documentation-only outputs produced in this turn:
- `specs/mesc-pilot-01/p01-03/README.md`
- `specs/mesc-pilot-01/p01-03/research.md`
- `specs/mesc-pilot-01/p01-03/spec.md`
- `specs/mesc-pilot-01/p01-03/plan.md`
- `specs/mesc-pilot-01/p01-03/data-model.md`
- `specs/mesc-pilot-01/p01-03/execution-protocol.md`
- `specs/mesc-pilot-01/p01-03/decision-record.md`
- `specs/mesc-pilot-01/p01-03/acceptance.md`

Top-level reconciliation outputs:
- `specs/mesc-pilot-01/README.md` — document map updated
- `specs/mesc-pilot-01/plan.md` — P01-02 and P01-03 statuses reconciled
- `specs/mesc-pilot-01/tasks.md` — P01-T04 and P01-T05 statuses reconciled

Future execution outputs (not produced in this turn):
- Acquisition manifest
- Parquet artifact hashes
- Native schema validation report
- Transformation report
- Validation report
- P01-04 handoff package

## Future prerequisites

Before P01-03 execution may begin:
- Separate founder authorization for dataset acquisition.
- Separate founder authorization for transformation execution.
- Confirmation that the pinned revision, configuration, and artifact allowlist are unchanged.
- Confirmation that the schema-gap resolution strategy is approved.
- Confirmation that raw-data storage boundary and `.gitignore` entries are in place.
- Confirmation that the gold-subset annotation protocol is defined and authorized.

## Success criteria

Planning success:
- All required planning documents are present and non-empty.
- All execution protocols are fail-closed at documented boundaries.
- No fabricated annotations or unsupported claims appear in the planning package.
- The schema-gap resolution is explicitly selected and justified.
- Top-level registry documents are reconciled without altering protected authority documents.
- Repository quality gates pass on the planning worktree.

Execution success (future, not assessed in this turn):
- Acquisition manifest matches approved identity.
- Transformation determinism is reproducible.
- Validation report has no `fail` statuses without explicit reasons.
- P01-04 handoff package is complete.

## Stop conditions

Halt P01-03 planning and record `P01-03 EXECUTION READINESS: BLOCKED` if:
- A protected authority document would need modification to resolve a conflict.
- The repository quality baseline changes materially without explanation.

## Historical planning prerequisites

The following facts justified the planning package at its creation time:

- PR #19 established the immutable revision lock for Pilot-01 datasets and models.
- The canonical planning base was `origin/main` at SHA `ea4c0b1798d92b2560184f35a3a7a4d2b27db15e`.

These are historical planning prerequisites, not runtime dataset-acquisition checks. Future execution must use the then-current separately authorized canonical repository state.

Halt P01-03 execution and record `BLOCKED` if:</text>
- The acquired revision differs from the pinned revision.
- The configuration is missing from the acquired artifacts.
- Unexpected Python loading scripts are required.
- Parquet files differ from the approved allowlist.
- Artifact hashes cannot be computed.
- Rights metadata changes.
- Raw content would be placed inside Git tracking.
- Source schema differs materially from the approved transformation protocol.
