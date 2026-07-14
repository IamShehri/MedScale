# Public Repository Alignment — Plan

## Verified baseline
- Current `origin/main` is `13629fabb9d18645eac1c68bd9e529cb6ff4bbd0`, which includes the merged PR #5 quality-gate repair.
- Commits ahead of current `origin/main` after rebase: 1 specification commit.
- Verification from current canonical baseline:
  - `uv run ruff check .`: PASS
  - `uv run ruff format --check .`: PASS
  - `uv run mypy`: PASS — 136 source files
  - `uv run pytest -q --no-header --tb=short`: 349 passed, 2 skipped
  - `uv run pytest --cov --cov-report=term-missing`: 349 passed, 2 skipped, coverage 78.11%, required threshold 77.0%
  - `uv run medscale check`: CLEAN
  - `uv build`: PASS — `medscale-0.2.0.tar.gz`, `medscale-0.2.0-py3-none-any.whl`
  - clean-wheel smoke test: imported package resolves from temporary `site-packages`, `medscale.cli.fhir` imports successfully, `medscale --help` and `medscale check` both pass
- PR #5 remains the source of that baseline; this PR is specification-only on top of it.

## Phase 0 — Truth capture
1. Complete divergence audit.
2. Capture README/ROADMAP/CHANGELOG/RELEASES/CITATION drift against current code/tests.
3. Classify uncommitted work by capability group and review risk.
4. Capture public API surface and classify stability.
5. Document mypy/ruff-format drift as separate hygiene PRs.

## Phase 1 — Repository formatting and typing hygiene
6. Run `ruff format` across tests and source where needed.
7. Add explicit type annotations for untyped helpers/fixtures/paths in tests and evaluation modules.
8. Fix remaining `attr-defined`, `arg-type`, `union-attr`, `index`, and `name-defined` mypy errors in M17/M18 modules.
9. Gate format/type repairs on pytest remaining green.

## Phase 2 — Evidence/dataset foundations
10. Consolidate dataset/governance/validation contracts if duplicate `DatasetBinding`/contract roots remain.
11. Freeze `dataset.builder` and `dataset.governance` public symbols and add tests proving imports.
12. Bind dataset fingerprint/manifest/release_packager to CLI surface without execution logic.

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
