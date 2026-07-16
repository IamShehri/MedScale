# Public Repository Alignment — Plan

## Verified baseline
- Current `origin/main` is `ce7db4342f01bdcbc15240f1dcf8384ea22ff308` (PR #16 merge).
- This baseline includes:
  - PR #10 — ALIGN-13 capability foundation;
  - PR #12 — ALIGN-14 deterministic split assignment freeze;
  - PR #13 — ALIGN-14 governance closeout;
  - PR #14 — ALIGN-15 evaluation engine boundary audit;
  - PR #15 — ALIGN-16 model runtime and governance boundary audit;
  - PR #16 — ALIGN-17 ModelKit public surface and runtime governance ADR.

## Phase 0 — Truth capture
1. Complete divergence audit.
2. Capture README/ROADMAP/CHANGELOG/RELEASES/CITATION drift against current code/tests.
3. Classify uncommitted work by capability group and review risk.
4. Capture public API surface and classify stability.
5. Record PR2 hygiene audit outcome as `Not Applicable` when no tracked behavior-preserving candidates exist.

## Phase 1 — Repository formatting and typing hygiene
- Status: Not Applicable / NO-GO
- Verified Group A eligible tracked files: 0
- Modified tracked files audited: 6
- Untracked files audited: 228
- Reason: every tracked candidate is a functional, contract, CLI, export, or architecture-test change; every untracked candidate is new implementation or governance material
- Result: no PR2 hygiene branch should be created
- Governance rule: empty or mislabeled implementation PRs are prohibited
- Next authorized action: Phase 2 dependency and boundary audit only

## Phase 2 — Evidence/dataset foundations
- Status: Complete / Conditional GO implemented
- ALIGN-12: done
- ALIGN-13: done (PR #10)
- ALIGN-14: done (PR #12, PR #13)
6. Audit the minimum dependency-complete evidence/dataset foundation slice.
7. Determine which files are new versus already public.
8. Classify public / experimental / internal surface.
9. Identify required tests, dependency graph, serialization and schema compatibility, facade impact, and ADR need.
10. Confirm the slice can be imported without model execution, cloud, scheduler, or external API assumptions.
11. Capability implementation remains blocked until this audit is reviewed and explicitly approved.

## Phase 2.5 — ALIGN-14 implementation complete
- Deterministic split assignment freeze contract (`medscale.dataset.SplitAssignmentFreeze`) frozen and merged to `main` via PR #12.
- Governance closeout documents updated and merged via PR #13.
- Branch cleanup and selection of the next ALIGN task remain separately gated.

## Phase 3 — Evaluation engine boundary audit

- Status: Complete / ADR NOT REQUIRED
- ALIGN-15: done via PR #14
- Canonical evaluation boundary:
  - `medscale.bench`;
  - `Benchmark`;
  - `BenchmarkRunArtifact`.
- No separate `EvaluationResult`, `EvaluationReport`, or `EvaluationEngine` was authorized.
- Evaluation implementation remains separately gated.

## Phase 4 — Model runtime and governance boundary audit

- Status: Complete / Conditional GO / ADR required
- ALIGN-16: merged via PR #15
- Merge commit: `1d60f00826f7029c83706b7f97e2409b40f57d57`
- Post-merge CI, CodeQL, and Optional Extras / Backends: green
- Audit findings:
  - provider-neutral protocol contracts exist;
  - optional backend adapters remain dependency-isolated;
  - current Transformers and llama.cpp adapters provide deterministic synthetic contract behavior, not real inference;
  - `_runtime.py` and workspace orchestration remain internal;
  - `REGISTRY` is an immutable governed model fact registry, not a mutable runtime registry;
  - recipes and experiment manifests are schemas, not execution systems;
  - the wider `modelkit.__all__` compatibility status is unresolved;
  - model promotion, model lineage, training-run, checkpoint, adapter-artifact, deployment, and infrastructure contracts do not exist;
  - ADR-0033 accepted by founder on 2026-07-15 after full semantic review.
- Decision: `ALIGN-16 AUDIT DECISION: CONDITIONAL GO`
- ADR decision: `ADR REQUIRED BEFORE IMPLEMENTATION` → `ADR-0033 ACCEPTED`
- Model runtime, routing, training, promotion, lineage, export changes, and real inference remain blocked.

Future governed sequence:

1. Merge the documentation-only ALIGN-16 audit.
2. Authorize a separate ADR-only task.
3. Review and accept or reject the ADR.
4. Authorize a separate exact implementation allowlist.
5. Implement only the approved slice in a later PR.

ADR acceptance does not automatically authorize implementation.

## Phase 4.5 — ModelKit public surface and runtime governance ADR

- ADR WORK: COMPLETE
- MERGE STATUS: COMPLETE — PR #16 merged via `ce7db4342f01bdcbc15240f1dcf8384ea22ff308`
- POST-MERGE WORKFLOWS: CI PASS / CodeQL PASS / Optional Extras / Backends PASS
- TRUTH-CLOSEOUT DOCUMENTATION: VALIDATED WORKING DRAFT
- IMPLEMENTATION AUTHORIZATION: NOT GRANTED

`specs/align-17/README.md` and `specs/align-17/acceptance.md` record this post-merge truth package.

This closeout branch is not yet committed, pushed, merged, or cleaned up.

No implementation authorization was granted, and no source, test, or runtime change occurred as part of ALIGN-17.

ALIGN-10 remains pending. Phases 5–7 remain not started. The release gate remains unchanged. Feature-branch and worktree cleanup remain separately gated.

ADR acceptance does not automatically authorize implementation.


## Phase 5 — Public documentation truth sync
- Status: Not started
22. Update README status, ROADMAP, CHANGELOG, RELEASES, CITATION, docs index, ADR index.
23. Only after PR2–PR4 lands and tests remain green.

## Phase 6 — Executable golden path
- Status: Not started
24. Add deterministic offline smoke command proving fixture/release artifact → evidence → evaluation → uncertainty → report bundle.
25. Capture Example output for README/release notes.

## Phase 7 — CI, packaging, contributor hardening
- Status: Not started
26. Pin GitHub Actions SHAs.
27. Add coverage enforcement artifact/failure gates.
28. Add sdist/wheel install + `medscale --version` smoke test.
29. Add TestPyPI dry-run job.
30. Add CODEOWNERS, issue/PR templates.

## Release gate
- Do not tag, release, or publish until all PRs are merged, CI green, and founder approves.

## Deliverables
- `specs/public-repository-alignment/spec.md`
- `specs/public-repository-alignment/plan.md`
- `specs/public-repository-alignment/tasks.md`
- Final audit report with exact file lists and fresh verification evidence.
