# P01-04B2A Final Review Hold — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-PV-17:
RECORDED BUT NOT ACTIVE
```

Two layers. Satisfying the first never satisfies the second.

---

## 1. This governance documentation gate

| Criterion | Requirement |
|---|---|
| Path scope | Only this package's four documents plus `specs/mesc-pilot-01/tasks.md` |
| No implementation change | No `.github/**`, `tests/**`, `src/**`, `pyproject.toml`, `uv.lock`, dataset, model, public-API, or B2A-contract path changed |
| Verdict fidelity | `GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT` quoted exactly |
| Findings | F1–F4 recorded, neither minimized nor exaggerated, each with its concrete mechanism |
| Settled mappings | The two accepted taxonomy mappings recorded and marked unchangeable |
| Activation gate | `FD-PV-17` carries five conditions and no subset activates it |
| No live authority | Nothing authorizes a PR #61 mutation while this package is Draft or unadopted |
| Future commit defined | Exact parent, subject, paths, conditional helper rule, and prohibitions stated |
| Canonical identities | Canonical main, PR #61 exact head, tree, and scope recorded exactly |
| No duplication | Prior history linked, not restated |
| Internal links | All relative links resolve |
| Exact-head verification | Automatically triggered checks succeed on the exact head |
| Independent review | A genuinely independent exact-head review of this package |
| Ready and merge | Each a separate founder decision, after that review |

### Stop conditions

Do not treat this gate as satisfied if any document authorizes a PR #61
mutation before `FD-PV-17` activation; authorizes execution or admissible
evidence production; claims any of F1–F4 is already corrected; changes either
settled taxonomy mapping; claims B2A acceptance, `N-12` discharge, platform
closure, or B2B; or modifies any path outside the authorized set.

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The future PR #61 commit 9

Applies only after `FD-PV-17` activation.

| Criterion | Requirement |
|---|---|
| Activation | All five conditions satisfied and mechanically verified |
| Commit count | Exactly one, parent `f68f8be8799c0ec67b26c319a4a06789f2ea1a7e` |
| Path scope | The two primary paths; the helper only on proven, recorded necessity |
| F1 closed | No guard depends on a `SIGPIPE`-prone pipeline; the large-response regression fails against `f68f8be879…` and passes after |
| F2 closed | The stub serves raw API JSON through the real `--paginate` and `--jq` projection; all three mutation proofs hold |
| F3 closed | Both guard copies covered behaviourally or proven byte-equivalent; malformed SHA rejected before `git rev-parse`; git stub rejects unexpected commands; whitespace and newline cases included; ref and HEAD-mismatch tested separately |
| F4 closed | The real cardinality step executes for 6, 5 and 7 archives with the exact category asserted for the failing counts |
| Mappings unchanged | Both settled mappings intact |
| Preservation | Permissions, limits, axes, taxonomy at twenty-one, `canonical_sha`, schema, pins and matrix properties unchanged |
| Gates | Lock check, Ruff lint and format, Mypy, focused and full Pytest, `medscale check` all pass |
| Exact-head checks | CI, CodeQL and the portability workflow succeed, automatically triggered, attempt 1 |
| Artifacts | Exactly six cell artifacts, no seventh evidence artifact, dispatch path skipped |
| Independent review | A genuinely independent clean-room exact-head review approves the final head |
| Ready | A separate founder decision after that review |

Meeting every row still does **not** accept B2A, produce admissible evidence,
discharge `N-12`, close the Windows or macOS obligations, or authorize B2B.

---

## 3. Standing prohibition

At no point does this package permit execution against real data, the real
split, B0, benchmark execution, model training or fine-tuning, P01-03G or
dataset access, model access, inference, retrieval, publication, or clinical
use.
