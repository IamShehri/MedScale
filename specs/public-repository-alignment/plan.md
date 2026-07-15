# Public Repository Alignment — Plan

## Verified baseline
- Current `origin/main` is `99b024aaf6831ad15296cb85210b8ae7f8df6998`, which includes merged PR #10 (ALIGN-13 capability foundation), PR #12 (ALIGN-14 implementation), and PR #13 (ALIGN-14 governance closeout).
- This amendment is documented from a clean worktree based on current canonical `origin/main`.

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

## Phase 3 — Evaluation engine boundary audit (current governed phase)
- Status: Complete / ADR NOT REQUIRED
- ALIGN-15: done (documentation-only audit)
12. Audit the evaluation surface on current `main`.
13. Discover actual modules, symbols, tests, exports, CLI commands, and dependencies.
14. Classify every evaluation-adjacent symbol as public / experimental / internal.
15. Determine the minimum dependency-complete future slice with production/test allowlists.
16. Resolve the `evaluation.pipeline.execution` vs `BenchmarkRunArtifact` naming question.
17. Determine ADR requirement (ADR NOT REQUIRED for current boundary).
18. Preserve implementation blocking until any future ADR is separately approved.

## Phase 4 — Model runtime and governance
- Status: Not started
19. Freeze M18 contracts: promotion, lineage, training artifacts, infrastructure.
20. Keep `models.execution`, `models.routing`, `models.registry` internal; do not export them publicly.
21. Document evaluation vs execution boundary in README/docs.

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
