# P01-04B2A Governance Hold — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-PV-16:
RECORDED BUT NOT ACTIVE
```

Acceptance is defined in two layers. Satisfying the first never satisfies the
second.

---

## 1. This governance documentation gate

Applies to this Draft pull request only.

| Criterion | Requirement |
|---|---|
| Path scope | Only the authorized documentation paths of this package plus `specs/mesc-pilot-01/tasks.md` |
| No implementation change | No `.github/**`, `tests/**`, `src/**`, `pyproject.toml`, `uv.lock`, dataset, model, public-API, or B2A-contract path changed |
| Verdict fidelity | The independent verdict `GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT` is quoted exactly and not softened |
| Findings recorded | B1, B2, B3 and B4 are recorded without minimizing them, with the concrete defect stated in each case |
| Authority gap | The B1 record acknowledges the gap and does not claim records existed that did not |
| Incident recorded | The accidental commit, its identities, and the non-fast-forward rewind are recorded explicitly |
| Prevention | The preventive control decision is explicit and prospective |
| Activation gate | `FD-PV-16` carries a five-condition activation gate and no subset activates it |
| No live authority | Nothing in this package authorizes implementation while it is Draft or unadopted |
| Future commit defined | Exact parent, subject, paths, scope, and prohibitions for the single future PR #61 commit are stated |
| Canonical identities | Canonical main, PR #61 exact head and tree, and both covered commit SHAs recorded exactly |
| Internal links | All cross-references resolve |
| Exact-head verification | Automatically triggered checks succeed on the exact head |
| Independent review | A genuinely independent exact-head review of this governance pull request |
| Ready and merge | Each a separate founder decision, after that review |

### Documentation-gate stop conditions

Do not treat this gate as satisfied if:

- any document authorizes a PR #61 mutation before `FD-PV-16` activation;
- any document authorizes execution or admissible evidence production;
- any document claims a blocking finding is already corrected;
- any document claims Windows or macOS evidence exists;
- any document claims B2A is accepted, `N-12` discharged, or B2B authorized;
- any document claims the pre-existing recordkeeping process was compliant;
- any path outside the authorized documentation set is modified;
- any B2A contract path under `../p01-04b2a/**` or the portability package under
  `../p01-04b2a-portability/**` is modified.

Modifying `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The future PR #61 correction

Applies only after `FD-PV-16` activation. Recorded here so the criteria exist
before the work does.

| Criterion | Requirement |
|---|---|
| Activation | All five `FD-PV-16` conditions satisfied and mechanically verified |
| Commit count | Exactly one additive commit, parent `2260fa540c440ce3584535f30e74323381568b98` |
| Path scope | `.github/workflows/mesc-b2a-portability.yml` and `tests/test_mesc_b2a_portability.py`; the helper only on proven necessity |
| B2 closed | Six total artifacts required; an unexpected artifact fails whether expired or not; the reversed test proves it |
| B3 closed | Each workflow-side guard emits its exact ratified category in a machine-verifiable form; still exactly twenty-one categories |
| B4 closed | No tautological test, no source-token-only safety test, no multi-category assertion where one category applies; every required test executes the real path and asserts one exact outcome |
| Preservation | All limits, axes, permissions, taxonomy, `canonical_sha` behaviour, schema, pins and matrix properties unchanged |
| Gates | Lock check, Ruff lint and format, Mypy, focused and full Pytest, and `medscale check` all pass |
| Exact-head checks | CI, CodeQL and the portability workflow succeed on the final head, automatically triggered, attempt 1 |
| Artifacts | Exactly six cell artifacts, no seventh evidence artifact, dispatch path skipped |
| Independent review | A genuinely independent clean-room exact-head review approves the final head |
| Ready | A separate founder decision, issued after that review |

Meeting every row above still does **not** accept B2A, does not produce
admissible evidence, does not discharge binding `N-12`, does not close the
Windows or macOS obligations, and does not authorize B2B.

---

## 3. Standing prohibition

At no point does this package permit execution against real data, formal split
generation, P01-03G or dataset access, model access, inference, retrieval,
training, metrics or benchmark execution, publication, or clinical use.
