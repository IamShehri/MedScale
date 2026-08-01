# P01-04B2A Evidence Production Gate — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-PV-18:
RECORDED BUT NOT ACTIVE
```

Two layers. Satisfying the first never satisfies the second.

---

## 1. This governance documentation gate

| Criterion | Requirement |
|---|---|
| Canonical baseline | Exactly `69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3` |
| Merge identity | Merge SHA, tree `ebbb61b905bde4773d48b40b9f667ceb0d558566`, ordered parents `63c6e320...` then `7c1522eb...`, subject `ci(mesc): add B2A portability infrastructure (#61)`, and merged timestamp `2026-07-31T22:00:34Z` all recorded exactly |
| PR final state | `PR #61` recorded as MERGED / CLOSED / NOT DRAFT with merged head `7c1522eb...` and 9 commits, all ancestors of the merge |
| First-parent delta | Exactly three added paths, `3 files changed, 4411 insertions(+), 0 deletions(-)` |
| No commit 10 | Recorded as not authorized and not created; branch tip still `7c1522eb...` |
| Taxonomy | Exactly twenty-one categories, unchanged |
| Settled mappings | `expired expected artifact` → `missing_matrix_cell` and `post-validation archive-count inconsistency` → `aggregate_verifier_internal_error`, both recorded and marked unchangeable |
| Path scope | Only this package's four documents plus `specs/mesc-pilot-01/tasks.md` |
| No implementation change | No `.github/**`, `tests/**`, `src/**`, `pyproject.toml`, `uv.lock`, dataset, model, contract, serializer, or public-API path changed |
| Actions truth | Post-merge runs recorded by exact head SHA and event, not filtered to `pull_request`; the absence of a post-merge portability run recorded as expected, not as a failure |
| No dispatch | No workflow dispatched or rerun during this package |
| No evidence | No admissible evidence produced, downloaded, accepted, or interpreted during this package |
| No false satisfaction | No claim that any existing pull-request artifact satisfies the canonical-main obligation |
| Activation gate | `FD-PV-18` carries five conditions and no subset activates it |
| No live authority | Nothing authorizes a dispatch while this package is Draft or unadopted |
| Future dispatch defined | Exact workflow, ref, event, input rule, one-attempt limit, consumption rule, and prohibitions stated |
| No hard-coded input | The future `expected_sha` is defined as the post-merge canonical SHA, never `69f16455...` |
| No downstream claim | No B2A acceptance, no `N-12` discharge, no platform closure, no B2B authorization |
| No execution claim | No real Pilot-01 split, B0, model access, dataset access, inference, retrieval, training, or fine-tuning |
| Ledger integrity | Historical snapshots preserved; superseding truth appended, not rewritten |
| No duplication | Prior history linked, not restated |
| Internal links | All relative links resolve |
| No placeholders | Every value is concrete; no deferred-work marker, stub token, or unfilled substitution slot appears anywhere in the package |
| Exact-head verification | CI and CodeQL succeed on this package's exact head |
| Independent review | A genuinely independent clean-room exact-head review of this package |
| Ready and merge | Each a separate founder decision, after that review |

### Stop conditions

Do not treat this gate as satisfied if any document dispatches or authorizes an
immediate dispatch; claims evidence exists, was produced, or was accepted;
treats a pull-request artifact as admissible; hard-codes
`69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3` as the future dispatch input; changes
either settled taxonomy mapping or the category count; claims B2A acceptance,
`N-12` discharge, platform closure, or B2B; rewrites or deletes a historical
governance snapshot; or modifies any path outside the authorized five.

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The future canonical-main evidence run

Applies only after `FD-PV-18` activation.

| Criterion | Requirement |
|---|---|
| Activation | All five conditions satisfied and mechanically verified |
| Dispatch count | Exactly one accepted request; no retry, rerun, or replacement |
| Run identity | `event: workflow_dispatch`, `run_attempt: 1`, `head_branch: main`, `head_sha` equal to the activated canonical SHA |
| Input fidelity | `expected_sha` exactly equal to `head_sha` |
| Matrix | All six cells succeed |
| Aggregate | Aggregate verification succeeds |
| Dispatch guards | Both copies execute and pass |
| Path selection | Pull-request aggregation skipped; dispatch aggregation executed |
| Upload | Evidence upload step executes exactly once |
| Artifacts | Exactly 7 — 6 cell artifacts and 1 `b2a-portability-evidence`; 0 duplicates, 0 unexpected, 0 expired at inspection |
| Envelope | Schema `mesc-pilot-01-b2a-portability-evidence/1`, `result: pass`, `canonical_sha` exactly the dispatch head SHA |
| Envelope scope | All six ratified cells and the exact canonical file set identified |
| Content boundary | No real dataset content, model weights, inference outputs, patient data, training artifacts, runtime-derived timestamps, hostnames, usernames, runner identifiers, secrets, environment paths, or unratified metadata |
| Verification | Offline byte-identity and digest verification across all six cells |
| No mutation | No repository, workflow, test, source, dependency, or lockfile change |
| Independent review | A genuinely independent clean-room evidence review |
| Acceptance | A separate founder evidence-acceptance decision |

Meeting every row still does **not** accept B2A, discharge binding `N-12`, close
the Windows or macOS obligations, complete P01-04B acceptance, or authorize B2B.
Those follow only from a separate founder evidence-acceptance decision taken
after an independent evidence review.

---

## 3. Standing prohibition

At no point does this package permit execution against real data, the real
Pilot-01 split, B0, benchmark execution, model training or fine-tuning, P01-03G
or dataset access, model access, inference, retrieval, publication, or clinical
use.
