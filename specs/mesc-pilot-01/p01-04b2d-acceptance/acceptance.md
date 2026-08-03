# P01-04B2D Acceptance — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-B2D-15:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED
```

This document defines the gate for **this governance package only**. Satisfying
it does not adopt FD-B2D-15, does not canonically accept P01-04B2D, does not
accept P01-04B, does not grant production correction authority, and does not
authorize any downstream phase.
[`founder-disposition.md`](founder-disposition.md) controls on any conflict.

---

## 1. This governance documentation gate

| Criterion | Requirement |
|---|---|
| Exact baseline | Branch created from exactly `faf58c3fbfa9a83e7d392630e3ad1f322c616259`, tree `3d27b9c43462ef9880d5fab1ea45b675d5ff55c1`, ordered parents `63cefe04...` then `6e586782...`; `origin/main` equal to that SHA; no rebase onto a later `main` |
| Exact five paths | Exactly `README.md`, `founder-disposition.md`, `decision-basis.md` and `acceptance.md` added under `specs/mesc-pilot-01/p01-04b2d-acceptance/`, plus `specs/mesc-pilot-01/tasks.md` modified. No sixth path |
| Documentation only | No change to `src/**`, `tests/**`, `.github/**`, `docs/**`, `pyproject.toml`, `uv.lock`; no prior governance package modified; no repository setting changed |
| One local commit | Exactly one normal commit with subject `docs(mesc): record P01-04B2D qualification acceptance`; one parent; one-line message with no body, no trailer and no `Co-Authored-By`; no amend, rebase, squash, reset, cherry-pick, merge or force-push; no push and no pull request |
| Unused identifiers | `FD-B2D-15`, `P01-T03B17` and `specs/mesc-pilot-01/p01-04b2d-acceptance/` verified unused on the exact baseline before creation |
| FD-B2D-15 present in full | The complete founder decision stated verbatim in `founder-disposition.md`, with founder identity, decision date, and every disposition line; no clause weakened, reinterpreted, aggregated away or silently overridden |
| Exact implementation identity | Authorization PR #77 with head `096f6667...`, tree `30b4cb54...` and merge `63cefe04...`; implementation PR #78 with branch `test/mesc-p01-04b2d-qualification`, reviewed head `6e586782...`, tree `3d27b9c4...`, parent `63cefe04...`, canonical merge `faf58c3f...`, 1 commit, 3 files, 3223 additions, 0 deletions; the three exact paths with blobs `b45811a2...`, `f35b4443...` and `ad215f71...` |
| Exact review identity | `APPROVE WITH NON-BLOCKING NOTES`; blocking findings `NONE`; reviewed head `6e586782...`; reviewed tree `3d27b9c4...` |
| Complete non-blocking-note ledger | All nine observations carried forward with identifier, observed behavior, scope, founder disposition, why non-blocking, and whether correction is authorized; none invented, merged, omitted or materially paraphrased; aggregate disposition `ACCEPTED AS NON-BLOCKING`, correction authorization `NOT ISSUED`, deferred obligation `NONE CREATED BY THIS PACKAGE` |
| Exact workflow evidence | Pull-request-triggered CI run `30780440275` with `quality (py3.11)` and `quality (py3.12)`, CodeQL run `30780440276` with `analyze (python)`, and qualification run `30780440318` — all completed / success; post-merge push-triggered CI `SUCCESS — 2/2`, CodeQL `SUCCESS — 1/1` and qualification `SUCCESS — 6/6`, with run identifiers queried from the repository and never invented |
| Exact six-cell evidence | All six qualification jobs recorded by exact name — ubuntu, windows and macos on Python 3.11 and 3.12 — each completed / success, against one set of committed literal golden vectors with no operating-system-specific expected value |
| Exact fixture dispositions | `exact-reference-1000-v1` 1000 rows / 89 groups / 700-150-150 / 552-338-110 / matrix REPRODUCED / placement CONFORMING / cross-platform literals SATISFIED; `constraint-stress-1000-v1` 1000 rows / 500 groups of size 2 / target PROVABLY INFEASIBLE / minimum score 6 / exactly 2 score-6 matrices / selected `386,82,84,238,50,50,76,18,16` / runner-up `386,84,82,236,50,52,78,16,16` / fallback ABSENT / TYPED FAIL-CLOSED / capability UNSATISFIED; `leakage-positive-v1` 1000 rows / 999 groups / 1 two-example group / 998 singletons / 9 findings / 3 `false_positive` / 6 `unresolved` / `leaked` true / 0 suppressed, with the same-partition synthetic control boundary preserved explicitly |
| Thirteen-criterion mapping | All thirteen criteria recorded with one result class each; criteria 1-10 `SATISFIED`; criteria 11 and 12 `NOT APPLICABLE TO B2D` and `NOT SATISFIED FOR P01-04B OVERALL`; criterion 13 `NOT APPLICABLE TO B2D OUTPUT PROMOTION` with the date-free canonical-byte invariant `SATISFIED` and non-promotability stated |
| UNSATISFIED minimum-deviation result | The indivisible-group global minimum-deviation allocation capability recorded `UNSATISFIED`, separately from the thirteen numbered criteria, with the typed fail-closed behaviour never described as conformance |
| P01-04B non-acceptance | `P01-04B acceptance eligibility: FALSE`; `P01-04B: CHANGES REQUIRED / NOT ACCEPTED`; a green qualification workflow explicitly does not equal P01-04B acceptance; `NOT APPLICABLE` never converted to `SATISFIED`; no aggregate ignores an `UNSATISFIED` or `BLOCKED` criterion |
| Zero correction authority | No production correction, no minimum-deviation implementation, no atomic-publication implementation, no write-path implementation, no test, workflow or contract change authorized; no deferred obligation created |
| Five adoption conditions | All five stated, with no subset sufficient |
| `tasks.md` integrity | `P01-T03B17` added chronologically; `P01-T03B16` and every earlier entry neither rewritten nor deleted; the completion of `P01-T03B16` recorded chronologically; prior controlling-state snapshots preserved and superseded only additively; exactly one unannotated live `Current controlling state` block |
| Internal-link integrity | Every relative Markdown link in the four new documents resolves at the package commit |
| No placeholders | Every value concrete; no `TODO`, `TBD`, `FIXME`, `XXX`, `PLACEHOLDER`, `<insert>`, `<replace>`, conflict marker, template variable, unfilled value, working-directory path, temporary path, local username, hostname or session identifier; no embedded logs, artifacts, synthetic raw question text or synthetic raw context text |
| No downstream authorization | Nothing authorizes P01-04C through P01-04G, P01-05 or later, P01-04B whole-phase acceptance, real execution, dataset or model access, or a production correction of the minimum-deviation gap |
| Independent review | A genuinely independent clean-room exact-head review of **this package**, in a different session and role, required before Ready |
| Separate Ready decision | A distinct founder decision taken after that review |
| Separate merge decision | A distinct founder decision taken after Ready |
| Mechanical post-merge verification | Performed after merge; canonical adoption is not achieved without it |

### Stop conditions

Do not treat this gate as satisfied if the package states or implies that:

```text
P01-04B is accepted
P01-04B acceptance eligibility is true
minimum-deviation allocation is satisfied
the typed allocation failure satisfies the missing capability
atomic publication is satisfied
write-path protections are satisfied
a NOT APPLICABLE disposition is SATISFIED
B2D outputs, registries, summaries or fixture helpers are promotable
the synthetic fixtures constitute real split evidence
the leakage fixture proves the real dataset is leak-free
either same-partition control is cross-partition leakage, duplicate split
  membership, source-document overlap or canonical leakage evidence
the ratified target matrix has five odd cells
a second score-6 matrix exists without its exact vector being recorded
a green qualification workflow equals P01-04B acceptance
workflow success is scientific, clinical, dataset or real-split evidence
P01-04C through P01-04G are authorized
P01-05 or later is authorized
production correction is authorized
model, data, training, publication or clinical authority exists
```

Also do not treat this gate as satisfied if the package:

```text
modifies any source, test or workflow path
modifies pyproject.toml, uv.lock or any prior governance package
adds a sixth path
carries a second commit, an amend or a force operation
invents a workflow run identifier
omits, merges or materially paraphrases an independent-review note
omits any of the six qualification cells
rewrites or deletes a historical ledger assertion
leaves more than one live Current controlling state
claims premature adoption of FD-B2D-15
```

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later decisions this package does not make

| Decision | State |
|---|---|
| Canonical adoption of FD-B2D-15 | Requires the five adoption conditions |
| Canonical acceptance of P01-04B2D | Requires the five adoption conditions |
| P01-04B whole-phase acceptance | **NOT ACHIEVED** — one criterion UNSATISFIED, two NOT SATISFIED for P01-04B overall |
| Production correction of minimum-deviation allocation | **NOT AUTHORIZED** — requires separate founder correction authorization |
| Atomic-publication component | **NOT AUTHORIZED** — separately governed |
| Write-path-protection component | **NOT AUTHORIZED** — separately governed |
| Promotion of any B2D output | **NOT AUTHORIZED** |
| P01-04C through P01-04G | **NOT AUTHORIZED** |
| P01-05 or later | **NOT AUTHORIZED** |
| Real split generation, real or canonical leakage audit | **NOT AUTHORIZED** |
| Dataset or registry scanning, record-pair discovery | **NOT AUTHORIZED** |
| CLI, filesystem publication, public export | **NOT AUTHORIZED** |
| Model access, real dataset access, P01-03G | **NOT AUTHORIZED** |
| Inference, retrieval, metrics, benchmark execution | **NOT AUTHORIZED** |
| Training, fine-tuning, adapter creation | **NOT AUTHORIZED** |
| Publication, clinical use | **NOT AUTHORIZED** |

A later, separately governed correction decision or remaining-tooling decision
is **eligible for founder consideration**. Eligibility is never authority, and
this package authorizes none of that work.

---

## 3. Standing prohibition

At no point does this package permit execution against real data, real split
generation, a real or canonical leakage audit, B0 or B1 execution, benchmark
execution, model training or fine-tuning, P01-03G or dataset access, model
access, inference, retrieval, publication, or clinical use.
