# MedScale v0.2 — Release Checklist

Stability: public release artifact.
Use this checklist before tagging `v0.2.0`.

## Code quality

- [x] `uv run ruff check .`
- [x] `uv run mypy src tests`
- [x] `uv run pytest -q --no-header`
- [x] `uv run pytest tests/test_architecture.py -q --no-header`
- [ ] `uv build` produces installable wheel + sdist
- [ ] Fresh venv smoke test: `import medscale` succeeds after wheel install

## Reproducibility

- [x] Benchmark replay verified against committed artifacts
- [x] Dataset validation verified (`dataset validate` passes)
- [x] Dataset checksums verified by sibling `.sha256` files
- [x] Content-hash primitive audit completed and frozen
- [x] Snapshot contract reviewed for backward compatibility
- [x] Reviewer merge deterministic replay test green

## Grammar / interoperability

- [x] FHIR ValidationReport deterministic serialization verified
- [x] `medscale fhir validate` local-only path verified
- [x] No PHI leakage paths in FHIR boundary
- [x] No hidden network dependency in deterministic paths

## Governance

- [x] ADR-0022 implemented
- [x] ADR-0029 implemented
- [x] ADR-0030 implemented
- [x] ADR-0026 implemented (M6)
- [x] ADR-0027 implemented (M4)
- [x] ADR-0028 implemented (M5)
- [ ] ADR-0023/0024/0025 registry status documented as post-v0.2 items or short formal records
- [ ] `docs/execution/v0.2/adr_implementation_tracker.md` updated for v0.2 final
- [ ] `docs/execution/v0.2/milestone_tracker.md` updated to M6 complete

## Documentation

- [x] `docs/execution/v0.2/architecture_audit.md`
- [x] `docs/execution/v0.2/dataset_v1.md`
- [x] `docs/execution/v0.2/M2-evidence-infrastructure.md`
- [x] `docs/execution/v0.2/M3-README.md`
- [x] `docs/execution/v0.2/M4-README.md`
- [x] `docs/execution/v0.2/M5-README.md`
- [x] `docs/execution/v0.2/M6-README.md`
- [x] `docs/execution/v0.2/technical_debt.md`
- [x] `docs/execution/v0.2/final_release_audit.md`
- [ ] `README.md` updated from T0 status to v0.2 final
- [ ] `CHANGELOG.md` v0.2 section filled
- [ ] `RELEASES.md` v0.2.0 section added
- [ ] `ROADMAP.md` maturity labels reviewed

## Release

- [ ] Version bump reviewed in `src/medscale/__about__.py`
- [ ] `CITATION.cff` version + date bumped to v0.2.0
- [ ] Release workflow added: `.github/workflows/release.yml`
- [ ] Tag strategy documented in `RELEASES.md`
- [ ] No automatic publish from `main`; publish only from tag gate
- [ ] GitHub Release created with CHANGELOG excerpt + manifest
- [ ] Optional dependencies confirmed optional in CI and docs

## Post-release

- [ ] Coverage threshold added to `pyproject.toml` or CI
- [ ] ADR-0023/0024/0025 formalized in v0.3 spike or governance doc
- [ ] `release_readiness.md` complete-state snapshot archived
