# P01-04B2A Cross-Platform Portability Validation Infrastructure — Acceptance

```text
Status:
PROPOSED AUTHORIZATION GATE — FOUNDER DECISION PENDING

Infrastructure implementation:
NOT AUTHORIZED

B2A implementation:
NOT AUTHORIZED

Execution:
NOT AUTHORIZED

Evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED
```

Canonical planning baseline:
`0884971f68619be8f25c3b905a3dcad7c5212101`

Acceptance is defined in three separate layers. Satisfying an earlier layer
never satisfies a later one.

---

## 1. Documentation-gate acceptance

Applies to this documentation pull request only.

| Criterion | Requirement |
|---|---|
| Path scope | Exactly eight authorized documentation paths |
| Decisions visible | PD-PV-1 through PD-PV-10 all present and all pending |
| No implementation authority | No document authorizes infrastructure or B2A implementation |
| No workflow change | No `.github/**` path changed |
| No source or test change | No `src/**` or `tests/**` path changed |
| No evidence claims | No document claims portability evidence exists or has passed |
| No acceptance claims | No document claims B2A is accepted |
| Internal links | All cross-references resolve |
| Canonical identities | Exact current base, PR #55 and PR #56 identities recorded |
| Local gates | Locked sync, Ruff lint, Ruff format, Mypy and Pytest pass |
| Exact-head verification | CI and CodeQL succeed on the exact head |
| Independent review | Independent Opus exact-head review |
| Merge | A separate merge decision |

### Documentation-gate stop conditions

Do not treat this gate as satisfied if any document authorizes implementation or
execution, claims Windows or macOS evidence exists, claims B2A is accepted,
claims P01-04B is complete, modifies a B2A contract or the founder-ratification
record, or modifies a path outside the eight authorized paths.

---

## 2. Future infrastructure-implementation acceptance

Applies only to a later, separately authorized infrastructure pull request.

| Criterion | Requirement |
|---|---|
| Path scope | Exactly the three proposed implementation paths, and no others |
| Base state | The B2A implementation is already present on its canonical base |
| `ci.yml` | Unmodified |
| Matrix | All six cells complete successfully |
| Artifacts | Exactly six artifacts exist |
| Files | Exactly three files per artifact |
| Bytes | All compared bytes identical across all six cells |
| Hashes and sizes | All recomputed SHA-256 values and byte sizes identical |
| Negative tests | Fail-closed tests exist for every proposed failure category |
| Permissions | `contents: read` only; no secrets, no write, no OIDC |
| Isolation | No dataset, model, network, or secret access |
| Gates | CI and CodeQL green |
| Review | Independent Opus exact-head review |

---

## 3. Future B2A acceptance

**Infrastructure acceptance is not B2A acceptance.** Merging a working
portability workflow accepts the workflow, not the increment it measures.

B2A acceptance requires all of:

1. the validation infrastructure merged on canonical main;
2. a canonical-main `workflow_dispatch` evidence run;
3. the exact canonical-main SHA recorded;
4. all six cells successful;
5. the aggregate verifier successful;
6. the evidence artifact inspected;
7. an independent Opus review of that evidence;
8. a separate founder/ChatGPT acceptance decision.

Only after B2A acceptance may B2B authorization be considered.

## 4. Standing prohibition

None of these layers authorizes execution against real data. At no point does
this package permit formal split generation, P01-03G or dataset access, model
access, inference, retrieval, training, metrics or benchmark execution,
publication, or clinical use.

Until a separate founder acceptance decision is recorded, B2A remains **not
accepted**, P01-04B remains **incomplete and not accepted**, and B2B remains
**not authorized**.
