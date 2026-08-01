# P01-04B2B Implementation Authorization — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

P01-04B2B implementation authority:
RECORDED BUT INACTIVE
```

Two layers. Satisfying the first never satisfies the second.

---

## 1. This documentation package

| Criterion | Requirement |
|---|---|
| Canonical baseline | Exactly `bfc4254b6a028ea7ec5969b505d73e7d66751272`, tree `4208ea672a01ac942a1caeee764167d530cc8f1e`, ordered parents `1f2d9152...` then `c59e4e16...`, subject `docs(mesc): record P01-04B2A acceptance (#67)` |
| PR #67 adoption verified | CLOSED / MERGED / NOT DRAFT, merged head `c59e4e16...`, merged `2026-08-01T03:32:26Z`, 1 commit / 5 files / +1259 / -1; first-parent scope exactly the five B2A-acceptance paths; reviewed-head-to-merge and synthetic-to-merge deltas both zero files |
| B2A state recorded | `FD-B2A-9` adopted at `bfc4254b...`; P01-04B2A accepted; `N-12` discharged; Windows and macOS obligations closed — all scoped to P01-04B2A |
| Post-merge workflows verified | Every automatic run at `bfc4254b...` recorded by name, ID, event, branch, head SHA, attempt, status and conclusion; all `push`, branch `main`, attempt 1, conclusion success; no rerun, retry, cancellation or manual dispatch; portability workflow not dispatched again; run `30678040133` remains the sole portability `workflow_dispatch`; `FD-PV-18` remains consumed |
| Identifiers unused | `FD-B2B-1` … `FD-B2B-10` and `P01-T03B12` verified unused across the complete canonical tree, task ledgers, founder records and adopted packages |
| New directory | `specs/mesc-pilot-01/p01-04b2b-authorization/` did not exist on canonical main |
| Dependency DAG satisfied | The adopted plan's `B2B requires B2A acceptance` prerequisite is recorded as satisfied, and the package states that this makes a B2B decision *eligible* rather than automatic |
| Design authority grounded | B2B recorded as the leakage primitive library with its nine adopted deliverables, and the seven excluded B2C/B2D concerns recorded as excluded |
| Ten decisions complete | `FD-B2B-1` through `FD-B2B-10` each recorded in full and mutually consistent |
| No senior conflict | Recorded as subordinate to `D1`–`D10`, `FD-B2-1`–`FD-B2-8`, `FD-B2A-1`–`FD-B2A-8` and the accepted B2A implementation, amending none of them; the `leaked` rule and the rational score form are labelled clarifications |
| Exact future allowlist | Exactly `src/medscale/mesc/_leakage_v1.py` and `tests/test_mesc_leakage_v1.py`, both status `A`, with the named prohibited paths listed and expansion forbidden |
| No implementation performed | No `_leakage_v1.py`, no `tests/test_mesc_leakage_v1.py`, no code, test, workflow, dependency or configuration change in this package |
| Inactive authority | While Draft or unmerged: decisions issued but not adopted; authority recorded but inactive; implementation not authorized to begin |
| Activation conditions | All five stated, with `No subset activates P01-04B2B implementation authority.` |
| No B2C/B2D or execution authority | No B2C, B2D, P01-04B acceptance, real split, P01-03G or real-dataset access, real leakage-audit execution, fixture facade, CLI, filesystem publication, B0/B1, model access, inference, retrieval, metrics, benchmark execution, training, fine-tuning, publication or clinical use |
| Acceptance separation | Recorded that completing the implementation will not accept B2B, and that B2C stays blocked until B2B is accepted rather than merely implemented |
| Path scope | Only this package's four documents plus `specs/mesc-pilot-01/tasks.md` |
| Prior packages untouched | No previous governance package modified; superseded state recorded additively |
| Task-ledger integrity | Every historical block preserved; the previous live block annotated as a superseded historical snapshot using the established additive pattern; exactly one unannotated live `Current controlling state` block remains; no prior statement silently rewritten |
| Terminology | The sixteen governed concepts kept distinct; none substituted for another |
| Internal links | All relative links resolve |
| No unresolved markers | Every value concrete; no unresolved drafting marker, stub token, unfilled substitution slot, provisional-value token or working-directory reference |
| Exact-head verification | CI and CodeQL succeed on this package's exact head |
| Independent review | A genuinely independent clean-room exact-head review of this package, required before Ready |
| Ready and merge | Each a separate founder decision, after that review |

### Stop conditions

Do not treat this gate as satisfied if any document implements B2B; creates the
future implementation or test file; modifies B1 or B2A implementation, public
exports, a CLI, workflows, dependencies or repository settings; inspects or
loads real dataset records; runs a leakage audit, fixture facade or split;
dispatches, reruns or cancels a workflow; mutates artifacts; authorizes B2C or
B2D; accepts P01-04B; claims the authority is active while the pull request is
Draft or unmerged; expands the two-path allowlist; amends `D1`–`D10`,
`FD-B2-1`–`FD-B2-8` or `FD-B2A-1`–`FD-B2A-8`; rewrites or deletes a historical
governance assertion; leaves two blocks simultaneously claiming to be the
current controlling state; or modifies any path outside the authorized five.

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later B2B implementation gate

Not satisfied by this package. Defined in
[`implementation-contract.md`](implementation-contract.md) §15 and reachable
only after all five activation conditions pass.

| Criterion | Requirement |
|---|---|
| Activation | All five conditions satisfied and mechanically verified |
| Path scope | Exactly the two allowlisted paths, both added |
| Contract conformance | Every §1–§14 requirement of the implementation contract satisfied |
| Test coverage | Every §15 test group present and passing |
| Independent review | A genuinely independent clean-room exact-head implementation review |
| Ready and merge | Separate founder decisions |
| Acceptance | A later, separate B2B implementation-acceptance decision |

Meeting every row still does not accept B2B, authorize B2C or B2D, complete
P01-04B, or authorize any execution.

---

## 3. Standing prohibition

At no point does this package permit B2B implementation before adoption,
execution against real data, the real Pilot-01 split, a real leakage audit, B0
or B1, benchmark execution, model training or fine-tuning, P01-03G or dataset
access, model access, inference, retrieval, publication, or clinical use.
