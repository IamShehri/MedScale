# MedScale v0.2 — Release Readiness Checklist

Stability: public release artifact.
Use this checklist as the acceptance gate before tagging M4 or any v0.2 release candidate.

## Quality Gates

- [x] `uv run ruff check .` passes
- [x] `uv run mypy src tests` passes
- [x] `uv run pytest -q --no-header` passes
- [ ] `pytest --cov=src/medscale` branch coverage ≥90%
- [x] `tests/test_architecture.py` passes
- [ ] Performance baseline documented (`docs/execution/v0.2/performance_baseline.md`)

## Documentation

- [x] README updated
- [x] ADR registry reviewed
- [ ] milestone tracker updated
- [ ] roadmap updated for M4-M6
- [ ] release notes draft started for v0.2-alpha
- [ ] Dataset v1 docs exist and are consistent (`docs/execution/v0.2/dataset_v1.md`)
- [ ] Architecture audit exists (`docs/execution/v0.2/architecture_audit.md`)
- [ ] Technical debt register exists (`docs/execution/v0.2/technical_debt.md`)

## Reproducibility

- [x] Deterministic benchmarks verified (`bench replay` passes on committed artifacts)
- [x] Dataset manifests validated (`dataset validate` succeeds on generated artifacts)
- [x] Dataset checksums verified by sibling `.sha256` files
- [x] Replay contracts verified by `tests/test_bench_replay.py`
- [ ] Content-hash primitive audit completed and frozen
- [ ] Snapshot contract reviewed for M4 compatibility

## Packaging

- [x] `pyproject.toml` validates
- [x] `pyproject.toml` optional dependencies reviewed
- [x] Version strategy confirmed single-source in `src/medscale/__about__.py`
- [ ] Release workflow tested manually or in CI
- [ ] `RELEASES.md` initialized
- [ ] `CHANGELOG.md` updated

## Security / Safety

- [x] No secrets committed
- [x] No network-dependent core behavior in `src/medscale`
- [x] No uncontrolled downloads in core
- [x] No hidden mutation in public dataclasses
- [ ] Secret-scanning tool run against entire history
- [ ] Supply-chain audit of pyproject dependencies complete

## Architecture Boundaries

- [x] `dataset` does not depend on `research`
- [x] `dataset` does not depend on `modelkit`, `litdb`, `evidence`
- [x] `bench` does not depend on optional backends (`transformers`, `llama.cpp`, `hf`)
- [x] `evidence` package does not import `litdb`
- [ ] New DATASET_V1_PLAN.md superseded or archived
- [ ] All TODOs/FIXMEs inventoried and triaged

## M4 Readiness

- [ ] M4 milestone plan approved
- [ ] Modelkit interfaces reviewed for breaking changes
- [ ] Modelkit registry contract frozen
- [ ] Test fixtures for model backends established
- [ ] Deployment targets for M4 decided
