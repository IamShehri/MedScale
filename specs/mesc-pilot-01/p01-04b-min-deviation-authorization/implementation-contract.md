# P01-04B Minimum-Deviation Correction — Implementation Contract

```text
Status:
FUTURE IMPLEMENTATION CONTRACT — INACTIVE

Implementation authority:
RECORDED BUT INACTIVE until FD-BMD-14 activation completes
```

This document defines, criterion by criterion, what the future bounded
implementation must satisfy. It creates no authority.
[`founder-authorization.md`](founder-authorization.md) controls on any conflict.

Nothing in this document may be started before all five FD-BMD-14 activation
conditions have passed.

---

## 1. Exact implementation identity

| Criterion | Requirement |
|---|---|
| C-1 branch | Exactly one branch named `fix/mesc-p01-04b-minimum-deviation`, cut from the canonical main that adopts this package |
| C-2 commit | Exactly one normal commit; one parent; subject `fix(mesc): implement P01-04B minimum-deviation allocation`; one-line message with no body, no trailer and no `Co-Authored-By` |
| C-3 scope | Exactly four modified paths; no fifth path; zero additions of new modules; zero deletions |
| C-4 no amend | No amend, rebase, squash, reset, cherry-pick, merge or force-push; a defect after commit requires `STOP / REPORT / NO AMEND / NO SECOND COMMIT / SEPARATE FOUNDER CORRECTION AUTHORIZATION` |

The exact four paths:

```text
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_fixture_split_v1.py
tests/test_mesc_split_v1.py
tests/test_mesc_p01_04b2d_qualification_v1.py
```

Paths explicitly **outside** the allowlist, which must remain byte-identical:

```text
tests/_mesc_p01_04b2d_fixtures_v1.py
.github/workflows/mesc-p01-04b2d-qualification.yml
src/medscale/mesc/split.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/mesc/_leakage_v1.py
tests/test_mesc_fixture_split_v1.py
pyproject.toml
uv.lock
every specs/ path
```

## 2. Private boundaries

| Criterion | Requirement |
|---|---|
| C-5 private resolver | The resolver and the typed boundary-failure subclass are module-private in `_split_v1.py`; neither appears in any `__all__`, any package `__init__`, any public re-export or any documented surface |
| C-6 no public export | `medscale`, `medscale.mesc` and every public module expose no new name |
| C-7 no CLI | No console entry point, no argument parser, no subcommand, no `medscale` CLI surface references the resolver |
| C-8 no I/O | The resolver performs no filesystem read or write, no environment read, no network, no subprocess, no clock read, no randomness, no locale or timezone dependence, no logging side effect and no temp file |
| C-9 no dependency change | `pyproject.toml` and `uv.lock` are unchanged; the resolver uses only the standard library already imported or importable without a new dependency |

## 3. Public splitter fail-closed invariant

| Criterion | Requirement |
|---|---|
| C-10 | `SourceDocumentGroupedSplitter.assign` continues to raise `PilotSplitNotAuthorizedError` unconditionally, on every call, for every argument value, with no conditional branch, flag, environment switch or partial path that permits execution |
| C-11 | A dedicated test asserts C-10 and fails if any execution path is introduced |

## 4. Preservation of the accepted exact allocator

| Criterion | Requirement |
|---|---|
| C-12 name and signature | `allocate_indivisible_groups(examples, targets)` keeps its name, parameters, return type and module |
| C-13 exact semantics | Its exact-target behaviour, validation order and target-total checks are unchanged |
| C-14 returned ordering | Its returned tuple keeps the accepted final ordering: partition order (`train`, `validation`, `test`), then decision order (`yes`, `no`, `maybe`), then `partition_key`, then `source_document_id`, then `min(row_ordinals)` |
| C-15 message stability | The ranked-boundary crossing message text is preserved verbatim, so that existing assertions matching `would cross` continue to hold |

The only permitted change to this function is that its ranked-boundary crossing
raise now constructs the private typed subclass instead of the base
`SplitAllocationError`. Because the subclass is a `SplitAllocationError`, every
existing `except` and `pytest.raises` clause keyed to the base class continues to
behave identically.

## 5. Typed fallback trigger

| Criterion | Requirement |
|---|---|
| C-16 subclass | Exactly one new private exception class, a direct subclass of `SplitAllocationError` |
| C-17 single raise site | It is raised **only** at the ranked-boundary crossing site |
| C-18 other sites unchanged | The observed/expected label-total mismatch raise, the "allocation did not exhaust targets" raise, and the controlled-rounding raise continue to raise the base `SplitAllocationError` |
| C-19 class-based dispatch | The exact-first wrapper discriminates by `except <PrivateSubclass>` only |
| C-20 no message parsing | No `str(error)`, `error.args` inspection, `in`, `startswith`, `re` match or any other message-derived condition participates in fallback selection |
| C-21 negative tests | Dedicated tests prove the resolver is **not** invoked for malformed input, duplicate identity, inconsistent dataset identity, invalid target keys, negative totals, label/partition grand-total mismatch, observed/expected label-total mismatch, internal invariant failure and unknown exception |

## 6. Complete global optimizer

| Criterion | Requirement |
|---|---|
| C-22 architecture | Dynamic programming over reachable integer count states; per-decision reachable matrices; global combination enforcing exact partition totals; canonical predecessor and tie-break retention |
| C-23 completeness | The reachable-state set is complete for the bounded problem; the implementation must be able to state why no assignment is excluded |
| C-24 prohibited techniques | No greedy approximation presented as global, no random search, no beam search, no local search, no external solver, no platform-native optimizer, no subprocess, no network operation, no `3**group_count` brute-force enumeration, no floating-point optimization |
| C-25 integer arithmetic | Every score, comparison, accumulation and tie-break uses Python integers only; no `float`, no `Decimal`-as-float, no `math.isclose`, no tolerance, no epsilon |
| C-26 bounded resources | At most 1000 examples, 1000 source-document groups, 3 decisions, 3 partitions; an input beyond the boundary fails closed with a private typed allocation error and is never approximated |
| C-27 determinism | Two invocations on the same input in the same process, in different processes, and on different operating systems produce identical assignments |

Memory or predecessor-storage optimization is permitted; reducing the state set
or weakening the tie-break is not.

## 7. Constraints

| Criterion | Requirement |
|---|---|
| C-28 | Every ranked source-document group is assigned exactly once to exactly one partition |
| C-29 | Groups remain indivisible; no group is split across partitions |
| C-30 | Zero cross-partition group overlap |
| C-31 | Every example is assigned exactly once |
| C-32 | Exact label row totals are preserved |
| C-33 | Exact overall partition totals are preserved |
| C-34 | No excluded examples, no duplicated examples, no omitted groups |
| C-35 | A cell deviates from its target only because indivisible-group constraints make the exact target unavailable |

## 8. Integer score, matrix order and tie-breaks

| Criterion | Requirement |
|---|---|
| C-36 matrix order | The nine cells are ordered exactly `yes/train`, `yes/validation`, `yes/test`, `no/train`, `no/validation`, `no/test`, `maybe/train`, `maybe/validation`, `maybe/test` |
| C-37 objective | `sum((actual_cell - target_cell) ** 2 for all nine cells)`, integer arithmetic only |
| C-38 global minimum | The selected matrix is a proven global minimum, not a best-found value |
| C-39 matrix tie-break | Among equal-minimum matrices, the lexicographically smallest nine-cell vector in C-36 order is selected |
| C-40 assignment tie-break | Among assignments producing the selected matrix, the lexicographically smallest partition-code vector is selected, ordered by decision (`yes`, `no`, `maybe`), then the existing `rank_groups` ordering within each decision, with codes `train = 0`, `validation = 1`, `test = 2` |
| C-41 order independence | No dictionary insertion order, set iteration order, filesystem order, process scheduling, platform behaviour or random source affects the selection |

`rank_groups` ordering is the accepted deterministic rank: `partition_key`, then
`source_document_id`, then `min(row_ordinals)`.

## 9. Facade integration

| Criterion | Requirement |
|---|---|
| C-42 single call site | `FixtureSplitFacade.run()` changes only where it calls the allocator, so that it uses the authorized exact-first/minimum-deviation path |
| C-43 validation order | The accepted twelve-step order is unchanged; fixture-identity and request-identity verification continue to execute **before** allocation |
| C-44 frozen result | The twelve-field `FixtureSplitResult` gains, loses and renames no field |
| C-45 no schema change | No B2A, B2B or B2C artifact schema, serialization version or leakage schema changes |
| C-46 facade properties | The facade remains private, unexported, stateless, in-memory, fixture-only, non-evidence, with no path inputs, no path outputs, no I/O, no environment reads, no network, no subprocess and no publication |
| C-47 derived values | The actual matrix, per-cell deviations and score may be derived and asserted by the qualification suite without being added to `FixtureSplitResult` |

## 10. Constraint-stress exact result

| Criterion | Requirement |
|---|---|
| C-48 | `constraint-stress-1000-v1` produces a successful deterministic in-memory `FixtureSplitResult` |
| C-49 | Target matrix `386,83,83,237,50,51,77,17,16`; exact target `INFEASIBLE` |
| C-50 | Global minimum squared-deviation score exactly `6` |
| C-51 | Exactly `2` minimum-score matrices |
| C-52 | Selected matrix `386,82,84,238,50,50,76,18,16` |
| C-53 | Runner-up matrix `386,84,82,236,50,52,78,16,16`, recorded explicitly and never omitted |
| C-54 | 1000 rows, 500 groups, every group size 2 |

Frozen literal goldens required for the constraint-stress result:

```text
request identity
split_hash
split_fingerprint
group_registry_bytes            SHA-256 and byte size
example_registry_bytes          SHA-256 and byte size
excluded_ledger_bytes           SHA-256 and byte size
split_summary_identity_core_bytes  SHA-256 and byte size
split_summary_document_bytes    SHA-256 and byte size
audit_report_bytes              SHA-256 and byte size
partition counts
group counts
actual label matrix
target label matrix
per-cell deviations
minimum score
selected matrix
runner-up matrix
```

| Criterion | Requirement |
|---|---|
| C-55 no auto-goldens | No regeneration command, no `--update-goldens` flag, no snapshot-approval mechanism, no self-approval from the result under test |
| C-56 fail-closed goldens | Mutating any single frozen literal causes at least one test to fail |

## 11. Exact-feasible byte non-regression

| Criterion | Requirement |
|---|---|
| C-57 | `exact-reference-1000-v1` remains byte-identical in every listed value |
| C-58 | `leakage-positive-v1` remains byte-identical in every listed value |
| C-59 | `ALGORITHM_VERSION` and `SPLIT_SEED` are unchanged |
| C-60 | Canonical serialization versions, artifact schema versions, leakage schema versions, fixture identity schema and request identity schema are unchanged |

Values required unchanged for both fixtures:

```text
fixture SHA-256                 request ID
split_hash                      split_fingerprint
every canonical byte surface    every canonical byte-surface digest
every canonical byte size       partition counts
label matrix                    group counts
ordered leakage finding IDs     audit classifications
```

The correction completes the existing ratified split-algorithm version. Because
the constraint-stress fixture has no prior successful artifact identity, freezing
its first successful result creates no identity conflict.

## 12. Independent-oracle placement

The accepted fixture helper `tests/_mesc_p01_04b2d_fixtures_v1.py` is **not** in
the four-path allowlist and must remain byte-identical. This constrains where new
oracle code may live, and the implementation must respect the following division:

| Criterion | Requirement |
|---|---|
| C-61 helper untouched | The helper is not modified; its `independent_partition_by_row` remains the exact-target oracle and stays correct for `exact-reference-1000-v1` and `leakage-positive-v1` |
| C-62 reuse matrix oracle | The helper's existing independent minimum-deviation **matrix** oracle is reused unchanged as the source of the minimum score, the selected matrix and the runner-up |
| C-63 new placement oracle | Any new independent minimum-deviation **placement** oracle — deriving which ranked group lands in which partition — lives in `tests/test_mesc_p01_04b2d_qualification_v1.py`, which is in the allowlist |
| C-64 oracle independence | The independent oracle must not call the new resolver, the facade or the accepted allocator to compute its own expected values |

`independent_partition_by_row` must simply cease to be the constraint-stress
expectation source; it is not deleted, not reinterpreted and not modified.

## 13. Qualification-status transition

| Criterion | Requirement |
|---|---|
| C-65 | The obsolete expected typed-failure assertion for `constraint-stress-1000-v1` is removed and replaced by the successful literal-golden qualification |
| C-66 | The revised qualification reports the minimum-deviation capability as `SATISFIED` |
| C-67 | Atomic publication remains `NOT SATISFIED FOR P01-04B OVERALL` |
| C-68 | Write-path protections remain `NOT SATISFIED FOR P01-04B OVERALL` |
| C-69 | `P01-04B acceptance eligibility` remains `FALSE` |
| C-70 | `P01-04B` remains `CHANGES REQUIRED / NOT ACCEPTED` |
| C-71 | No aggregate treats `NOT APPLICABLE TO THIS CORRECTION` as satisfaction of the two remaining requirements |
| C-72 | No historical governance document is rewritten; the pre-correction `UNSATISFIED` record remains truthful history |

## 14. Six-cell workflow requirement

| Criterion | Requirement |
|---|---|
| C-73 | The existing `MESC P01-04B2D Qualification` workflow runs automatically through its **existing** path filters |
| C-74 | No workflow edit is authorized |
| C-75 | All six cells — ubuntu, windows and macos on Python 3.11 and 3.12 — must succeed against one set of committed literal golden vectors, with no operating-system-specific expected value |

This is satisfiable without any workflow change: three of the four authorized
implementation paths — `src/medscale/mesc/_split_v1.py`,
`src/medscale/mesc/_fixture_split_v1.py` and
`tests/test_mesc_p01_04b2d_qualification_v1.py` — are already listed in both the
`pull_request` and `push` path filters, so a commit touching them triggers the
workflow automatically. `tests/test_mesc_split_v1.py` is not listed, and does not
need to be.

## 15. Quality gates

Required before the implementation commit:

```bash
git status --short
git diff --check
git diff --cached --name-status
git diff --cached --numstat
```

Required validation:

```text
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run python -m mypy
uv run pytest tests/test_mesc_split_v1.py
uv run pytest tests/test_mesc_fixture_split_v1.py
uv run pytest tests/test_mesc_p01_04b2d_qualification_v1.py
uv run pytest -q
uv run medscale check
six-cell B2D GitHub qualification
standard CI
CodeQL
```

| Criterion | Requirement |
|---|---|
| C-76 | Every gate passes at the exact implementation head |
| C-77 | `uv lock --check` reports no lockfile change |
| C-78 | The full suite passes with no new failure and no new skip |
| C-79 | No workflow is dispatched, rerun or cancelled to obtain a green result |

## 16. Implementation review

| Criterion | Requirement |
|---|---|
| C-80 independence | A genuinely independent clean-room exact-head implementation review, in a different session and role, with no authorship of the implementation |
| C-81 rederivation | The reviewer must rederive the feasible lattice, both score-6 matrices, the score calculation and the selected tie-break **without using the new optimizer as their oracle** |
| C-82 non-regression proof | The reviewer must independently confirm that `exact-reference-1000-v1` and `leakage-positive-v1` byte surfaces are unchanged |
| C-83 boundary proof | The reviewer must confirm class-based fallback dispatch, absence of message parsing, and that the resolver is unreachable for every non-boundary error |
| C-84 read-only | The review performs zero repository mutation |

An independent reviewer may reproduce the lattice by the complete-cover argument:
any feasible matrix scoring at most 6 has every cell deviation bounded by
`|d| <= 2`, because `3 ** 2 = 9 > 6`, and a deviation matrix has zero row and
column sums.

## 17. Implementation acceptance

| Criterion | Requirement |
|---|---|
| C-85 | Implementation merge does not equal implementation acceptance |
| C-86 | A separate implementation-acceptance disposition and its own canonical adoption are required |
| C-87 | Only after that acceptance may the atomic-publication/write-path-protection authorization package be considered |
| C-88 | P01-04B remains `CHANGES REQUIRED / NOT ACCEPTED` throughout |

## 18. Continuing non-authority

The future implementation authorized here does not permit:

```text
public export                      CLI
filesystem publication             atomic publisher implementation
write-path implementation          real registry access
real source-record access          real split generation
real partition membership          real or canonical leakage audit
record-pair discovery              dataset or model download
model access                       inference
retrieval                          metrics
benchmark execution                training
fine-tuning                        adapter creation
publication                        clinical use
P01-04C through P01-04G            P01-05 or later
```

```text
ELIGIBILITY IS NOT AUTHORITY.
```
