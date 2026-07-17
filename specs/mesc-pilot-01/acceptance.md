# MESC Pilot-01 — Acceptance Criteria

Status: **foundation acceptance record**
Authorization: Foundation *** only
Freeze date: 2026-07-17

---

## Foundation acceptance criteria

All criteria below are required. No criterion may be marked satisfied by inference or fabrication.

### Artifacts

- Every required foundation file is present and non-empty.
- All required source contracts are implemented and importable.
- Architecture layer registration is present and enforcement is preserved.
- Deterministic serialization and content hashing are defined and stable.
- Source-document-grouped deterministic split is implemented.
- Leakage audit report contract is present and tested.
- Unavailable metrics are represented as `not_applicable`.

### Quality gates

- Full Pytest passes with 0 failures.
- Mypy passes with 0 errors.
- Ruff check passes.
- Ruff format check passes.
- `git diff --check` passes.
- Exact scope: only approved Pilot-01 foundation paths are present.
- Staging is empty.

### Conduct boundaries

- No dataset download in this turn.
- No model weight download in this turn.
- No inference execution in this turn.
- No retrieval execution in this turn.
- No baseline execution in this turn.
- No QLoRA training in this turn.
- No adapter creation in this turn.
- No clinical use in this turn.
- No production use in this turn.
- No release or publication in this turn.
- No Afia integration in this turn.
- No ALIGN modification in this turn.

---

## Governance record

```text
FOUNDATION IMPLEMENTATION AUTHORIZATION: GRANTED
BASELINE EXECUTION AUTHORIZATION: NOT GRANTED
QLORA TRAINING AUTHORIZATION: NOT GRANTED
CLINICAL USE: NOT AUTHORIZED
PRODUCTION USE: NOT AUTHORIZED
RELEASE: NOT AUTHORIZED
```

Founder-frozen model selection authority is recorded in `model-selection.md`. Hermes authority is repository implementation and verification only.

---

## Scope record

Approved foundation scope:

```text
tests/test_architecture.py
specs/mesc-pilot-01/README.md
specs/mesc-pilot-01/spec.md
specs/mesc-pilot-01/plan.md
specs/mesc-pilot-01/tasks.md
specs/mesc-pilot-01/acceptance.md
specs/mesc-pilot-01/data-contract.md
specs/mesc-pilot-01/evaluation-contract.md
specs/mesc-pilot-01/model-landscape.md
specs/mesc-pilot-01/model-selection.md
specs/mesc-pilot-01/dataset-selection.md
specs/mesc-pilot-01/risk-register.md
src/medscale/mesc/__init__.py
src/medscale/mesc/contracts.py
src/medscale/mesc/split.py
src/medscale/mesc/manifests.py
src/medscale/mesc/evaluation.py
tests/test_mesc_contracts.py
tests/test_mesc_split.py
tests/test_mesc_manifests.py
tests/test_mesc_evaluation.py
tests/fixtures/mesc/pilot_smoke.jsonl
```

Any path outside the approved set blocks acceptance.

---

## Final acceptance checklist

- [ ] All required files present and non-empty.
- [ ] All required contracts present or proven equivalent.
- [ ] Architecture registration present and enforcement preserved.
- [ ] Deterministic serialization and hashing verified.
- [ ] Leakage audit report present and serializable.
- [ ] Missing metrics represented as `not_applicable`.
- [ ] Smoke fixture scenario coverage complete.
- [ ] Full Pytest passes.
- [ ] Mypy passes.
- [ ] Ruff passes.
- [ ] Format check passes.
- [ ] `git diff --check` passes.
- [ ] Scope exact.
- [ ] Staging empty.
- [ ] No datasets, weights, inference, training, or results claimed.
- [ ] No commit, push, PR, release, publication, production use, clinical use, or Afia integration.
