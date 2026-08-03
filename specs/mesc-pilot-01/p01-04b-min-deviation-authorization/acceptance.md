# P01-04B Minimum-Deviation Correction — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-BR-1:
FOUNDER DECISION ISSUED;
NOT YET ADOPTED ON CANONICAL MAIN

FD-BMD-1 THROUGH FD-BMD-14:
FOUNDER DECISIONS ISSUED;
NOT YET ADOPTED ON CANONICAL MAIN

MINIMUM-DEVIATION IMPLEMENTATION AUTHORITY:
RECORDED BUT INACTIVE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED
```

This document defines the gate for **this governance package only**. Satisfying
it does not adopt FD-BR-1 or FD-BMD-1 through FD-BMD-14, does not activate
implementation authority, does not accept P01-04B, does not authorize
publication, and does not authorize any downstream phase.
[`founder-authorization.md`](founder-authorization.md) controls on any conflict.

---

## 1. This governance documentation gate

| Criterion | Requirement |
|---|---|
| Exact baseline | Branch created from exactly `3513d66bc36650363a6368bb4e42901119419802`, tree `e08393388f4684b39ef9226a3a90b719ea1ba494`, ordered parents `faf58c3f...` then `c38473d6...`; `origin/main` equal to that SHA; no rebase onto a later `main` |
| Exact five paths | Exactly `README.md`, `acceptance.md`, `founder-authorization.md` and `implementation-contract.md` added under `specs/mesc-pilot-01/p01-04b-min-deviation-authorization/`, plus `specs/mesc-pilot-01/tasks.md` modified. No sixth path |
| Documentation only | No change to `src/**`, `tests/**`, `.github/**`, `docs/**`, `pyproject.toml`, `uv.lock`; no prior governance package modified; no repository setting changed |
| One local commit | Exactly one normal commit with subject `docs(mesc): authorize P01-04B minimum-deviation correction`; one parent; one-line message with no body, no trailer and no `Co-Authored-By`; no amend, rebase, squash, reset, cherry-pick, merge or force-push; no push and no pull request |
| Unused identifiers | `FD-BR-1`, `FD-BMD-1` through `FD-BMD-14`, `P01-T03B18` and `specs/mesc-pilot-01/p01-04b-min-deviation-authorization/` verified unused on the exact baseline before creation |
| FD-BR-1 present in full | The complete recovery-architecture decision stated verbatim, with founder identity, decision date, the three-increment sequence, the separate-governance requirement, the publication-ordering constraints and the naming rationale for omitting `P01-04B2E` |
| FD-BMD-1 through FD-BMD-14 present in full | All fourteen decisions stated verbatim, each with its operative constraints; none merged, abbreviated, reordered away or silently weakened |
| Exact recovery sequence | Allocation correction, then publication boundary, then integrated requalification — with acceptance of each required before the next may be authorized |
| Exact four-path future allowlist | `src/medscale/mesc/_split_v1.py`, `src/medscale/mesc/_fixture_split_v1.py`, `tests/test_mesc_split_v1.py`, `tests/test_mesc_p01_04b2d_qualification_v1.py`; no fifth path; the excluded paths named explicitly |
| Exact future branch and subject | Branch `fix/mesc-p01-04b-minimum-deviation`; subject `fix(mesc): implement P01-04B minimum-deviation allocation` |
| Global objective unambiguous | `sum((actual_cell - target_cell) ** 2 for all nine cells)`, integer arithmetic only, proven global minimum, no tolerance and no heuristic |
| Matrix order unambiguous | The nine cells stated in exactly one order: `yes/train`, `yes/validation`, `yes/test`, `no/train`, `no/validation`, `no/test`, `maybe/train`, `maybe/validation`, `maybe/test` |
| Both tie-breaks unambiguous | Matrix tie-break by lexicographically smallest nine-cell vector; assignment tie-break by lexicographically smallest partition-code vector with decision order `yes, no, maybe`, existing `rank_groups` ordering within a decision, and codes `train = 0`, `validation = 1`, `test = 2` |
| Constraint-stress values exact | 1000 rows, 500 groups, size 2, target `386,83,83,237,50,51,77,17,16`, exact target `INFEASIBLE`, minimum score `6`, exactly `2` minimum-score matrices, selected `386,82,84,238,50,50,76,18,16`, runner-up `386,84,82,236,50,52,78,16,16` |
| Exact-feasible byte preservation | `exact-reference-1000-v1` and `leakage-positive-v1` byte-identical in every listed value; `ALGORITHM_VERSION`, `SPLIT_SEED` and every schema version unchanged |
| Public splitter remains fail-closed | `SourceDocumentGroupedSplitter.assign` remains unconditionally fail-closed |
| Publication remains unauthorized | Atomic publication and write-path implementation are `NOT AUTHORIZED` before and after adoption |
| P01-04B remains not accepted | `P01-04B acceptance eligibility: FALSE` and `P01-04B: CHANGES REQUIRED / NOT ACCEPTED` in both the pre-adoption and post-adoption states |
| Five activation conditions | All five stated, with no subset sufficient |
| One bounded attempt | One branch, one normal commit, four paths, one attempt; authority spent at commit creation; defect handling requires a separate founder correction authorization |
| `tasks.md` integrity | `P01-T03B18` added chronologically exactly once; `P01-T03B17` and every earlier entry preserved byte-for-byte except additive supersession annotations; zero removed lines; exactly one unannotated live `Current controlling state` block; every earlier snapshot marked `HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED` |
| Internal-link integrity | Every relative Markdown link in the four new documents resolves at the package commit |
| Zero placeholders | Every value concrete; no `TODO`, `TBD`, `FIXME`, `XXX`, `PLACEHOLDER`, conflict marker, template variable, unfilled value, local username, hostname, local absolute path, temporary path, working-directory path or session identifier; no embedded workflow logs, artifact bytes, raw synthetic questions, raw synthetic contexts, real data or model output |
| Independent package review | A genuinely independent clean-room exact-head review of **this package**, in a different session and role, required before Ready |
| Separate Founder Ready | A distinct founder decision taken after that review |
| Separate Founder Merge | A distinct founder decision taken after Ready |
| Mechanical post-merge verification | Performed after merge; canonical adoption is not achieved without it |

### Stop conditions

Do not treat this gate as satisfied if the package states or implies that:

```text
the correction is already implemented
implementation authority is active before adoption
the existing exact allocator may be replaced
SourceDocumentGroupedSplitter.assign may execute
floating point may select the optimum
a heuristic is globally optimal
matrix order is unspecified
tie-breaking may depend on runtime order
constraint-stress has any score other than 6
the runner-up matrix may be omitted
exact-reference bytes may change
leakage-positive bytes may change
artifact schemas may change
publication is authorized
filesystem I/O is authorized
P01-04B is accepted
P01-04C through P01-04G are authorized
real data or real split execution is authorized
```

Also do not treat this gate as satisfied if the package:

```text
modifies any source, test or workflow path
modifies pyproject.toml, uv.lock or any prior governance package
adds a sixth path
carries a second commit, an amend or a force operation
authorizes a fifth future implementation path
authorizes a workflow edit
rewrites or deletes a historical ledger assertion
leaves more than one live Current controlling state
claims premature adoption of FD-BR-1 or any FD-BMD decision
treats eligibility for a later decision as authority
```

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later decisions this package does not make

| Decision | State |
|---|---|
| Canonical adoption of FD-BR-1 and FD-BMD-1 through FD-BMD-14 | Requires the five activation conditions |
| Activation of minimum-deviation implementation authority | Requires the five activation conditions |
| The minimum-deviation implementation itself | **NOT AUTHORIZED TO BEGIN** before adoption |
| Acceptance of the future implementation | **NOT ACHIEVED** — requires its own separate disposition |
| Atomic-publication component | **NOT AUTHORIZED** — separately governed, and only after the correction is accepted |
| Write-path-protection component | **NOT AUTHORIZED** — separately governed |
| P01-04B whole-phase acceptance | **NOT ACHIEVED** — three gaps outstanding |
| Integrated P01-04B requalification | **NOT AUTHORIZED** — increment 3, after increment 2 acceptance |
| P01-04C through P01-04G | **NOT AUTHORIZED** |
| P01-05 or later | **NOT AUTHORIZED** |
| Real split generation, real or canonical leakage audit | **NOT AUTHORIZED** |
| Dataset or registry scanning, record-pair discovery | **NOT AUTHORIZED** |
| CLI, filesystem publication, public export | **NOT AUTHORIZED** |
| Model access, real dataset access, P01-03G | **NOT AUTHORIZED** |
| Inference, retrieval, metrics, benchmark execution | **NOT AUTHORIZED** |
| Training, fine-tuning, adapter creation | **NOT AUTHORIZED** |
| Publication, clinical use | **NOT AUTHORIZED** |

A later, separately governed decision is **eligible for founder consideration**.
Eligibility is never authority, and this package authorizes none of that work.

---

## 3. Standing prohibition

At no point does this package permit execution against real data, real split
generation, a real or canonical leakage audit, B0 or B1 execution, fixture or
facade execution, benchmark execution, model training or fine-tuning, P01-03G or
dataset access, model access, inference, retrieval, publication, or clinical use.
