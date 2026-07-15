# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** Implemented / Merged / Closed

## Implementation boundary

- Selected boundary: Option A — Standalone freeze contract.
- Minimum slice: a standalone deterministic split-assignment freeze contract.
- Formal release-manifest integration is deferred.
- Preparation of an implementation task is authorized.
- Implementation itself remains unauthorized until the next explicit founder authorization.

## Planning phases

1. Accept or amend Proposed ADR-0032.
2. Freeze exact field and identity semantics under ADR approval.
3. Implement the minimum pure contract in `src/medscale/dataset/builder/freeze.py`.
4. Add focused positive and negative tests in `tests/test_dataset_freeze.py`.
5. Update the builder facade additively in `src/medscale/dataset/builder/__init__.py`.
6. Run focused validation on the new contract and tests.
7. Run repository-wide validation: ruff, format, mypy, pytest, coverage, `medscale check`, `uv build`, clean-wheel imports, `git diff --check`.
8. Conduct exact cumulative scope audit against the three-file allowlist.
9. Create a dedicated implementation PR after a separate founder authorization.
10. Require a separate founder merge authorization.
11. Verify post-merge CI, CodeQL, and Optional Extras / Backends.

## Governance sequence

- ALIGN-14 planning and ADR-0032 acceptance are complete.
- Preparation of an implementation task for ALIGN-14 is authorized.
- Implementation is not authorized.
- Any scope expansion beyond the three-file boundary requires a new founder decision.
