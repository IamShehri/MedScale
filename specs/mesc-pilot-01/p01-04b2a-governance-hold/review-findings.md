# P01-04B2A Governance Hold — Accepted Independent Review Findings

```text
Status:
INDEPENDENT EXACT-HEAD REVIEW VERDICT ACCEPTED

Governed pull request:
PR #61

Reviewed exact head:
2260fa540c440ce3584535f30e74323381568b98

Reviewed exact tree:
eb5cd1757f89bca2b42e1e9c61d3fcd1270a5e94

Canonical main at review time:
3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9
```

## Accepted verdict

A genuinely independent clean-room exact-head review of PR #61 returned:

```text
GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT
```

The founder accepts that verdict in full. It is recorded here verbatim and is
not paraphrased, softened, or partially adopted. PR #61 remains Draft.

## Blocking findings

Four blocking findings were returned. All four are accepted as stated. None is
treated as advisory, stylistic, or optional.

### B1 — Missing recoverable authorization for commits 6 and 7

The repository contains no canonical record authorizing PR #61 commits
`605536737a22db5a3abfe4243a1c528623a46ba5` and
`2260fa540c440ce3584535f30e74323381568b98`.

The adopted `FD-PV-15` record on canonical main authorizes exactly one
synchronization merge commit, Correction A, and Correction B, and lists "a
fourth implementation correction commit" among the acts that remain a separate
founder act. Commits 6 and 7 are the **fourth and fifth correction commits**,
and the **fifth and sixth implementation-path-changing commits**, on the PR #61
branch; the exact SHAs are controlling over any ordinal description. A reviewer
working only from the repository therefore cannot reconstruct any authority for
them.

The founder disposition for this finding is recorded in
[`founder-disposition.md`](founder-disposition.md).

### B2 — Expired unexpected seventh artifact is accepted

The workflow's artifact-set equality check filters the current-run API response
to non-expired entries **before** counting and comparing:

```bash
awk -F'\t' '$3 == "false" { print $1 }' artifacts.tsv | sort > live-names.txt
```

An unexpected artifact that is expired is therefore invisible to both the
`live_count` check and the `cmp` comparison, and the run proceeds. The state

```text
six valid expected artifacts + one expired unexpected artifact
```

currently **passes**. The corresponding test in
`tests/test_mesc_b2a_portability.py`,
`test_an_expired_extra_artifact_alone_does_not_pass_the_set_check`, asserts
`returncode == 0` for exactly that state, so the defect is pinned in place by a
test that encodes the wrong expectation.

This violates the exact-six-artifact requirement, which admits no unexpected
artifact in the relevant current-run response, expired or otherwise.

### B3 — Workflow failures bypass the ratified taxonomy

The workflow-side guards fail closed but emit prose only. No taxonomy category
string appears anywhere in `.github/workflows/mesc-b2a-portability.yml`. A
compressed-size violation, an artifact-set violation, or a malformed dispatch
input therefore terminates the run without surfacing
`artifact_size_limit_exceeded`, the applicable matrix or evidence-file category,
or `evidence_generation_failure`.

The ratified twenty-one-category taxonomy is the contract for fail-closed
reporting. A guard that fails without its category is not machine-verifiable and
cannot be audited against that contract.

### B4 — Correction B test-quality requirements remain unsatisfied

The following defects remain in `tests/test_mesc_b2a_portability.py` at the
reviewed head:

- a tautological test that asserts a property of its own string literals and
  never invokes the implementation:

  ```python
  def test_traversal_and_absolute_paths_are_rejected() -> None:
      for name in ("../escape.json", "/abs.json"):
          assert ".." in name or name.startswith("/")
  ```

- four assertions that accept one of several unrelated categories where a single
  deterministic category applies, at the `noncanonical_manifest` /
  `invalid_json`, `unsafe_archive_entry` / `unexpected_evidence_file` (twice),
  and `unsafe_archive_entry` / `aggregate_verifier_internal_error` sites;
- the expired-unexpected-artifact test described under B2, which asserts success
  for a state that must fail;
- source-token assertions that check workflow text without executing the guard
  they describe.

Correction B's ratified requirement is that every safe-extraction guard has a
negative test that invokes the implementation, reaches the guard, and asserts
the exact category, and that no tautological or non-executing safety test
remains. That requirement is not yet met.

## Non-blocking findings

### N1 — Consumer-failure test does not exercise broken-pipe behaviour

The consumer-failure test uses a payload small enough that the producer may
complete before the bounded consumer exits, so the test does not demonstrate
that the consumer status remains the controlling diagnostic when the producer
also observes a broken pipe. Non-blocking: the consumer branch is reached and
the correct message is asserted. Strengthening it is permitted but not required.

### N2 — The accidental canonical-main incident requires a durable governance record

Recorded in full in [`main-incident-record.md`](main-incident-record.md).

## What this record does not do

It does not correct any finding, authorize any implementation, approve any head,
authorize a Ready transition or merge for PR #61 or for this governance package,
produce or accept admissible evidence, accept B2A, discharge binding `N-12`,
close the Windows or macOS obligations, or authorize B2B.
