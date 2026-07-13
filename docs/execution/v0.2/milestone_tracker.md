# Milestone Tracker

## M0 Foundation
- Status: complete
- Verification: ruff/mypy/pytest PASS

## M1 Patient Domain
- Status: complete
- Verification: ruff/mypy/pytest PASS

## M2 Evidence/Extractor
- Status: complete
- Verification: ruff/mypy/pytest PASS

## M3 Benchmark Framework
- Status: complete
- Verification: ruff/mypy/pytest PASS

## M4 ModelKit Backends
- Status: complete
- Deliverables:
  - `src/medscale/backends/common.py`
  - `src/medscale/backends/__init__.py`
  - `src/medscale/backends/transformers/`
  - `src/medscale/backends/llamacpp/`
  - `pyproject.toml` optional extras:
    - `backends-transformers`
    - `backends-llamacpp`
- Verification: ruff/mypy/pytest GREEN
- Known limitations: optional ML deps are not installed in core; full remote-model runs are out of scope.

## M5 FHIR Boundary
- Status: pending

## M6 Collaboration Workflow
- Status: pending
