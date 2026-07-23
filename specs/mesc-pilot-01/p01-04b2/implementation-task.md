# MESC Pilot-01 — P01-04B2 Implementation Task

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

Status: **NOT AUTHORIZED FOR EXECUTION**

This document is a future Hermes implementation brief. It describes what implementation would look like after separate founder authorization for each increment. It does not authorize any implementation action.

---
Reconcile to:
- separate `FixtureSplitFacade`; keep `SourceDocumentGroupedSplitter.assign()` fail-closed;
- library-only B2; no CLI;
- three-fixture qualification suite;
- non-empty positive leakage audit;
- canonical fingerprint bundle;
- date-free promotable artifacts;
- atomic publication requirements.

## Task overview

Implement P01-04B2 increments B2A–B2D after founder authorization. Each increment requires:

- explicit founder authorization for that increment;
- an atomic PR with independent Opus review;
- canonical main at exact `ce1272235cb48dbacdb18f20e1ae8db695b01328` at authorization time;
- no real P01-03G registry execution;
- no automatic authorization of the next increment.

## B2A — Artifact types and canonical serialization

**Objective:** Add stable dataclasses and canonical JSON serialization for all split-artifact types.

**Not authorized in this task:**

- Any Python source modification
- Any test modification
- Any import or dataclass addition to `src/`

**Future implementation scope:**

1. Add `SplitPolicy` dataclass in a new file under `src/medscale/mesc/` (exact path to be determined at authorization time).
2. Add `GroupRegistryEntry` dataclass with `to_jsonl_line()` method using D6 canonical rules.
3. Add `ExampleSplitRegistryEntry` dataclass with `to_jsonl_line()` method.
4. Add `SplitSummary` dataclass with `split_hash` (16-hex, compatibility-only) and `split_fingerprint` (64-hex, authoritative).
5. Add `SplitFingerprint` dataclass with full 64-hex SHA-256 digest.
6. Add `SplitFingerprintBundle` dataclass binding `bundle_schema_version`, `policy_id`, `algorithm_version`, `split_seed`, canonical artifact role, SHA-256, byte size, and stable schema version for each artifact.
7. Add `ExcludedOrUnassignedLedger` dataclass.
8. Add `LeakageFinding` dataclass with raw-text prohibition enforced by field validation.
9. Add `LeakageAuditReport` dataclass. The report is expected to be non-empty for leakage-positive qualification fixtures.
10. Add `FixtureSplitRequest` and `FixtureSplitResult` types.
11. Add authorization and path-safety error enumerations.

**Acceptance criteria (future):**

- All types match `contracts.md` field definitions exactly.
- All serialization matches `spec.md` canonical JSONL rules.
- `mypy` strict passes on new types.
- `ruff check` and `ruff format` pass.
- No modification to existing B1 data contracts.
- Promotable artifacts contain no runtime timestamps, local paths, usernames, or hostnames.

## B2B — Leakage primitive library

**Objective:** Implement leakage-detection functions consistent with `research.md` and `contracts.md`.

**Not authorized in this task:**

- Any Python source modification
- Any access to real question, context, or answer text

**Future implementation scope:**

1. Add `exact_example_identity(a, b) -> bool`.
2. Add `exact_source_document_identity(a, b) -> bool`.
3. Add `exact_question_equality(a, b) -> bool`.
4. Add `normalized_question_equality(a, b) -> bool` using NFKC, case folding, whitespace collapse.
5. Add `token_set_jaccard(a, b, threshold=0.90) -> float | None`.
6. Add `context_equality(a, b) -> bool`.
7. Add deterministic finding identifier generator.
8. Add false-positive classification rules.
9. Enforce suppression prohibition via explicit error on suppression attempt.

**Acceptance criteria (future):**

- All functions are deterministic on identical inputs.
- Edge cases (empty token sets, Unicode edge cases) produce explicit, documented results.
- No raw text is exposed in any finding field.
- All functions pass synthetic fixture tests without real data access.
- Leakage-positive fixture produces a non-empty `LeakageAuditReport`.

## B2C — Fixture-only public facade and integration entry point

**Objective:** Implement a separate fixture-only facade. Keep `SourceDocumentGroupedSplitter.assign()` fail-closed.

**Not authorized in this task:**

- Any modification to `src/medscale/mesc/split.py`
- Any modification to `SourceDocumentGroupedSplitter` in its current form

**Future implementation scope:**

1. Implement private `_FixtureOnlySplitter` in a new module.
2. Implement public `FixtureSplitFacade` that:
   - accepts `FixtureSplitRequest` only;
   - raises `FixtureOnlyModeError` on any real-registry invocation attempt;
   - produces `FixtureSplitResult` with deterministic output.
3. Add path-safety checks: `PathSafetyViolation` on output outside designated workspace.
4. Add concurrency checks: `ConcurrencyViolation` on concurrent writer detection.
5. Add overwrite protection: `ArtifactOverwriteError` on write to existing artifact.
6. Add CLI boundary design (no CLI code in this task; design only).

**Acceptance criteria (future):**

- `SourceDocumentGroupedSplitter.assign()` remains unconditionally fail-closed.
- `FixtureSplitFacade` is the only supported execution surface for B2.
- Synthetic fixture injection is the only supported input path.
- All error types are distinct and documented.
- No real execution is possible through the facade.
- Existing private core (`_split_v1.py`) is unchanged.

## B2D — Integrated synthetic qualification and P01-04B acceptance review

**Objective:** Define and execute integrated synthetic qualification tests and P01-04B acceptance review.

**Not authorized in this task:**

- Any test execution
- Any 1,000-row fixture generation
- Any acceptance review execution

**Future implementation scope:**

1. Generate synthetic 1,000-row fixture with label totals 552/338/110 and targets 700/150/150.
2. Execute `PilotSplitManifest` computation on synthetic fixture.
3. Verify byte-identical output on repeated runs.
4. Verify split fingerprint reproducibility from promoted artifacts.
5. Verify zero group overlaps.
6. Execute leakage-detection primitives on synthetic fixture.
7. Produce `LeakageAuditReport` (expected non-empty for leakage-positive fixture).
8. Execute P01-04B acceptance review per `acceptance.md`.
9. Produce external execution evidence repository (outside Git).

**Acceptance criteria (future):**

- All P01-04B acceptance criteria in `acceptance.md` are demonstrably satisfied.
- No P01-03G membership is generated during qualification.
- P01-04B acceptance review produces independent review conclusions.
- External execution evidence is stored outside repository and evidence root.
- Promotable artifacts contain no timestamps; provenance records remain external.

---
## Atomic PR strategy

Each increment (B2A, B2B, B2C, B2D) must ship in a separate atomic PR:

- PR title: `feat(mesc): P01-04B2X — <increment name>`
- PR description: exact canonical baseline, authorization reference, scope, acceptance criteria, execution prohibitions.
- Independent Opus review required before merge.
- No automatic merge, no auto-merge, no squash-merge unless explicitly authorized.

## Stop conditions for any future implementation

Stop implementation without mutation if:

- canonical main SHA does not match recorded authorization baseline;
- any proposed change conflicts with P01-04A decisions D1–D10;
- any proposed change modifies `src/medscale/mesc/split.py` data contracts without founder decision;
- any proposed change exposes raw question, context, or answer text in promotable artifacts;
- any proposed change authorizes P01-04C–G;
- any proposed change modifies `pyproject.toml`, `uv.lock`, `tests/**`, `scripts/**`, `.github/**`, or `specs/mesc-pilot-01/p01-03g/**`.
