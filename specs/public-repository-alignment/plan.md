# Public Repository Alignment — Plan

## Verified baseline
- Current `origin/main` is `0f9a2d3b68546e5475946a582be1496d8ac40ad3`, which includes merged PR #4, PR #5, and PR #6 governance and quality-gate repairs.
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
- Status: Conditional GO / documentation complete
- Audit recommendation: conditional GO; ADR required before capability implementation
- Next governed action: ADR-only PR; capability implementation remains blocked
- ALIGN-12: done
- ALIGN-13: pending
6. Audit the minimum dependency-complete evidence/dataset foundation slice.
7. Determine which files are new versus already public.
8. Classify public / experimental / internal surface.
9. Identify required tests, dependency graph, serialization and schema compatibility, facade impact, and ADR need.
10. Confirm the slice can be imported without model execution, cloud, scheduler, or external API assumptions.
11. Capability implementation remains blocked until this audit is reviewed and explicitly approved.

## Phase 3 — Evaluation engine
13. Audit `evaluation.pipeline.execution` naming vs `EvaluationReport`/`EvaluationResult` mismatch.
14. Stabilize evaluation harness contracts and mark runner as experimental/internal until execution charter exists.
15. Add public import test for stable evaluation subset.

## Phase 4 — Model runtime and governance
16. Freeze M18 contracts: promotion, lineage, training artifacts, infrastructure.
17. Keep `models.execution`, `models.routing`, `models.registry` internal; do not export them publicly.
18. Document evaluation vs execution boundary in README/docs.

## Phase 5 — Public documentation truth sync
19. Update README status, ROADMAP, CHANGELOG, RELEASES, CITATION, docs index, ADR index.
20. Only after PR2–PR4 lands and tests remain green.

## Phase 6 — Executable golden path
21. Add deterministic offline smoke command proving fixture/release artifact → evidence → evaluation → uncertainty → report bundle.
22. Capture Example output for README/release notes.

## Phase 7 — CI, packaging, contributor hardening
23. Pin GitHub Actions SHAs.
24. Add coverage enforcement artifact/failure gates.
25. Add sdist/wheel install + `medscale --version` smoke test.
26. Add TestPyPI dry-run job.
27. Add CODEOWNERS, issue/PR templates.

## Release gate
- Do not tag, release, or publish until all PRs are merged, CI green, and founder approves.

## Deliverables
- `specs/public-repository-alignment/spec.md`
- `specs/public-repository-alignment/plan.md`
- `specs/public-repository-alignment/tasks.md`
- Final audit report with exact file lists and fresh verification evidence.
