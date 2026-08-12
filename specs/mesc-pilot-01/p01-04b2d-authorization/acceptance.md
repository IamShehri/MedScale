# P01-04B2D Authorization — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-B2D-1 through FD-B2D-14:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D implementation authority:
RECORDED BUT INACTIVE

P01-04B2D implementation:
NOT AUTHORIZED TO BEGIN
```

This document defines the gate for **this governance package only**. Satisfying
it does not adopt FD-B2D-1 through FD-B2D-14, does not activate implementation
authority, and does not authorize any qualification run.
[`founder-authorization.md`](founder-authorization.md) controls on any conflict.

---

## 1. This governance documentation gate

| Criterion | Requirement |
|---|---|
| Exact canonical baseline | Branch created from exactly `a0c623aa08354a343fccc1d066a7a6acaa5b8576`, tree `6e766deb531a9d7332942c3a524be0b3de698af3`, ordered parents `9d4b9ed0...` then `3edcc476...`; `origin/main` equal to that SHA; no rebase onto a later `main` |
| Exact five documentation paths | Exactly `README.md`, `acceptance.md`, `founder-authorization.md` and `implementation-contract.md` added under `specs/mesc-pilot-01/p01-04b2d-authorization/`, plus `specs/mesc-pilot-01/tasks.md` modified. No sixth path |
| Documentation only | No change to `src/**`, `tests/**`, `.github/**`, `docs/**`, `pyproject.toml`, `uv.lock`; no prior governance package modified |
| One local commit | Exactly one commit with subject `docs(mesc): authorize P01-04B2D qualification`; no amend, rebase, squash, reset, cherry-pick, merge or force-push; no push and no pull request |
| Unused identifiers | `FD-B2D-1` through `FD-B2D-14`, `P01-T03B16` and `specs/mesc-pilot-01/p01-04b2d-authorization/` verified unused on the exact baseline before creation |
| All fourteen founder decisions present | FD-B2D-1 through FD-B2D-14 each stated in full in `founder-authorization.md` with no gap, no merge and no contradiction |
| FD-B2-7 conformance | The package conforms to ratified FD-B2-7 Fixture A, B and C without amending, superseding or narrowing it; the four withdrawn conflicting requirements are recorded as withdrawn |
| Exact future three-path allowlist | Exactly `tests/_mesc_p01_04b2d_fixtures_v1.py`, `tests/test_mesc_p01_04b2d_qualification_v1.py` and `.github/workflows/mesc-p01-04b2d-qualification.yml`; zero production source changes; zero new dependencies; no public export, CLI or entry point |
| Exact three fixture names | `exact-reference-1000-v1`, `constraint-stress-1000-v1`, `leakage-positive-v1`; no generic alias; no fourth fixture; derived negative mutations never granted fixture status |
| Exact 1000-row requirement | Every fixture exactly 1,000 `OrderedExampleRow` and 1,000 `SourceLabelRow` values |
| Exact target totals and label matrix | Partitions 700 / 150 / 150; labels 552 / 338 / 110; the ratified 3x3 matrix stated exactly |
| Exact reference-fixture contract | 89 groups; group-size vectors exactly as frozen; all six sizes 1, 2, 3, 5, 8, 13 present; multi-example groups mandatory; every partition holds multiple multi-example groups; exact matrix feasible; independent D6 construction without `rank_groups`, `allocate_indivisible_groups` or `FixtureSplitFacade` |
| Exact constraint-stress contract | 500 groups of size exactly 2; the ratified target matrix has exactly **six** odd-valued cells comprising **five** distinct odd values because `83` occurs twice, so the exact matrix is provably **infeasible**; global minimum-deviation oracle over non-negative even cells; minimum squared-deviation score **6**; exactly **two** score-6 matrices frozen — selected Matrix A `386,82,84,238,50,50,76,18,16` and runner-up Matrix B `386,84,82,236,50,52,78,16,16` — with the lexicographic tie-break (label order `yes, no, maybe`; partition order `train, validation, test`) selecting Matrix A; expected typed `SplitAllocationError` fail-closed from the accepted implementation; criterion recorded **UNSATISFIED** |
| Exact leakage-positive contract | The founder-frozen structure stated as a requirement and not as an inference: 1,000 rows; exactly **999** source-document groups; exactly one homogeneous two-example source-document group whose members share a decision, remain in one actual partition and never straddle a partition boundary; exactly 998 singleton groups; no other multi-example group. Nine deterministic scenarios covering every ratified FD-B2-7 Fixture C case; `finding_count` 9; `leaked` true; at least three supported `false_positive` findings each with a stable evidence reference; at least one `unresolved`; zero suppressed; raw-text exclusion from every promotable surface |
| Same-partition synthetic control boundary | The exact-example control uses one actual fixture example; the source-document control uses one actual two-example homogeneous group; the pair remains in one actual partition; the pair never straddles a partition boundary; both are explicitly classified as same-partition synthetic controls; neither is represented as cross-partition leakage. The distinction is explicit — not merely implied — in all four authorization documents |
| Exact workflow matrix | One new workflow only; name `MESC P01-04B2D Qualification`; triggers `pull_request` and `push` to `main`; `permissions: contents: read`; `fail-fast: false`; all six OS/Python cells present; locked sync; no `workflow_dispatch`, schedule, secret, artifact upload or cache publication; required path filters present; no existing workflow modified |
| Anti-circularity | Generator-spec proof binds the specification, never facade output; no private `_fixture_split_v1.py` helper used for expected values; expected values are literal constants; no golden regeneration command, `--update-goldens` option, automatic rewrite or self-approval routine |
| No pre-authorization qualification execution | No fixture constructed, no 1,000-row batch instantiated, no `FixtureSplitFacade` invocation, no oracle run, and no B2D digest, request identifier, split hash, fingerprint or finding identifier calculated during this documentation task |
| Activation gate | All five activation conditions stated, with no subset sufficient |
| One bounded implementation | One branch, one commit, three paths, one attempt; authority spent at that commit; correction requires a separate founder decision |
| Separate implementation acceptance | Nine post-implementation gates stated; no implementation merge accepts B2D or P01-04B; no B2D acceptance authorizes P01-04C |
| Complete acceptance mapping | The mapping covers **13 unique criteria** — the ten P01-04B tooling-acceptance criteria plus three additional non-duplicative future-code criteria from `p01-04b2/acceptance.md` (atomic publication, write-path protections, date-free promotable artifacts). No document claims the ten tooling rows alone represent every canonical criterion. Criteria 11 and 12 are NOT APPLICABLE to B2D and NOT SATISFIED for P01-04B overall; criterion 13 is NOT APPLICABLE to B2D output promotion with the date-free canonical-byte invariant testable |
| P01-04B non-acceptance | The package states P01-04B is INCOMPLETE / NOT ACCEPTED, that the minimum-deviation criterion is UNSATISFIED, and that green B2D CI does not equal P01-04B acceptance. No aggregate acceptance algorithm may ignore an `UNSATISFIED` or `BLOCKED` criterion, and `NOT APPLICABLE` never converts to `SATISFIED` |
| `tasks.md` integrity | `P01-T03B16` added; `P01-T03B13`, `P01-T03B14` and `P01-T03B15` neither rewritten nor deleted; the completion of P01-T03B15 recorded chronologically; prior controlling-state snapshots preserved and superseded only additively; exactly one unannotated live `Current controlling state` block |
| Internal-link integrity | Every relative Markdown link in the four new documents resolves at the package commit |
| No placeholders | Every value concrete; no `TODO`, `TBD`, `FIXME`, `XXX`, `PLACEHOLDER`, `<insert>`, `<replace>`, conflict marker, template variable, unfilled value, working-directory path, temporary path, local username, hostname or session identifier |
| No downstream authorization | Nothing authorizes P01-04C through P01-04G, P01-05 or later, P01-04B whole-phase acceptance, real execution, dataset or model access, or a production correction of the minimum-deviation gap |
| Independent review | A genuinely independent clean-room exact-head review of **this package**, required before Ready |
| Separate Ready decision | A distinct founder decision taken after that review |
| Separate merge decision | A distinct founder decision taken after Ready |
| Mechanical post-merge verification | Performed after merge; canonical adoption is not achieved without it |

### Same-partition synthetic control boundary

This statement is normative for this package and is required by FD-B2D-6 to be
explicit in all four authorization documents.

```text
The exact-example self-identity scenario and the exact-source-document
same-group scenario are same-partition synthetic controls.

They qualify primitive behavior, finding construction, canonical identity,
classification and evidence-reference enforcement only.

They are not cross-partition leakage findings, do not establish duplicate
partition membership, do not establish source-document overlap, and do not
constitute a real or canonical leakage audit.
```

The leakage-positive acceptance criterion is satisfied only when all of the
following are verified:

```text
the exact-example control uses one actual fixture example
the source-document control uses one actual two-example homogeneous group
the pair remains in one actual partition
the pair never straddles a partition boundary
both are explicitly classified as same-partition synthetic controls
neither is represented as cross-partition leakage
```

### Stop conditions

Do not treat this gate as satisfied if the package:

```text
modifies any source, test or workflow path
constructs any B2D fixture
invokes FixtureSplitFacade for B2D
calculates any B2D output fingerprint, hash or identifier
accesses any real data
introduces a fourth fixture
substitutes a generic fixture for the three named fixtures
introduces a public API or CLI
modifies an existing workflow
omits any operating-system cell from the six-cell matrix
permits dynamic golden regeneration
amends, supersedes or narrows FD-B2-7
claims 1000 singleton groups for exact-reference-1000-v1
claims 88 groups for exact-reference-1000-v1
claims constraint-stress proves exact targets or zero deviation
claims five leakage findings or that all findings are unresolved
claims a leakage-positive group count other than 999
claims more than one multi-example group in leakage-positive-v1
describes the leakage-positive 999-group structure as an inference or note
rather than as a founder-frozen requirement
describes either same-partition control as a cross-partition finding, real
leakage, canonical leakage evidence, duplicate split membership or
source-document overlap
states or implies that the ratified target matrix has five odd cells
records that a second score-6 matrix exists without freezing its exact vector
claims the ten tooling criteria alone represent every canonical criterion
omits the atomic-publication, write-path-protection or date-free
promotable-artifact criterion from the mapping
converts a NOT APPLICABLE disposition into SATISFIED, or aggregates acceptance
while any criterion is UNSATISFIED or BLOCKED
claims premature implementation authority
claims P01-04B acceptance or P01-04B acceptance eligibility
claims any P01-04C through P01-04G authority
adds a sixth documentation path
rewrites or deletes a historical ledger assertion
leaves more than one live Current controlling state
```

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later decisions this package does not make

| Decision | State |
|---|---|
| Canonical adoption of FD-B2D-1 through FD-B2D-14 | Requires the five activation conditions |
| P01-04B2D implementation | **NOT AUTHORIZED TO BEGIN** |
| P01-04B2D qualification execution | **NOT EXECUTED** |
| P01-04B2D harness acceptance | Requires a separate founder disposition |
| P01-04B whole-phase acceptance | **NOT ACHIEVED** — one criterion UNSATISFIED |
| Production correction of minimum-deviation allocation | **NOT AUTHORIZED** — requires separate founder correction authorization |
| P01-04C through P01-04G | **NOT AUTHORIZED** |
| P01-05 or later | **NOT AUTHORIZED** |
| Real split generation, real or canonical leakage audit | **NOT AUTHORIZED** |
| Dataset or registry scanning, record-pair discovery | **NOT AUTHORIZED** |
| CLI, filesystem publication, public export | **NOT AUTHORIZED** |
| Model access, real dataset access, P01-03G | **NOT AUTHORIZED** |
| Inference, retrieval, metrics, benchmark execution | **NOT AUTHORIZED** |
| Training, fine-tuning, adapter creation | **NOT AUTHORIZED** |
| Publication, clinical use | **NOT AUTHORIZED** |

After canonical adoption, P01-04B2D implementation becomes **authorized to begin
once, within the three-path allowlist**, and nothing more.

---

## 3. Standing prohibition

At no point does this package permit execution against real data, real split
generation, a real or canonical leakage audit, B0 or B1 execution, benchmark
execution, model training or fine-tuning, P01-03G or dataset access, model
access, inference, retrieval, publication, or clinical use.
