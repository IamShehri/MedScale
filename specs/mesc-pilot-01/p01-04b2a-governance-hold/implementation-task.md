# P01-04B2A Governance Hold — Prospective Correction Brief

```text
THIS BRIEF IS NOT EXECUTABLE.
IT BECOMES EXECUTABLE ONLY AFTER ALL FIVE FD-PV-16 ACTIVATION CONDITIONS ARE
SATISFIED AND MECHANICALLY VERIFIED. RECORDING IT IN A DRAFT PULL REQUEST
ACTIVATES NOTHING.
```

```text
Status:
RECORDED — NOT EXECUTABLE

FD-PV-16:
RECORDED BUT NOT ACTIVE

PR #61:
OPEN / DRAFT / NOT MERGED — HELD
```

Canonical authority: [`founder-disposition.md`](founder-disposition.md) §3.
Findings being closed: [`review-findings.md`](review-findings.md).

## Exact commit identity

```text
Required parent:
2260fa540c440ce3584535f30e74323381568b98

Recommended subject:
fix(mesc): close portability governance-hold findings

Count:
exactly one additive commit
```

No ninth PR #61 commit may be created without another separate founder decision.
No amendment, rebase, squash, reset, cherry-pick, or force-push is authorized.

## Exact paths

```text
.github/workflows/mesc-b2a-portability.yml
tests/test_mesc_b2a_portability.py
```

`tests/_mesc_b2a_portability.py` may change **only** if the correction analysis
proves a helper change is strictly necessary, and the necessity must be stated
explicitly in the commit record. Otherwise it remains byte-identical. No `src`,
`specs`, `docs`, dependency, lockfile, dataset, model, public-API, B2A-contract,
or `ci.yml` change is authorized.

## B2 — full artifact-set equality

The complete current-run API response must be validated **without filtering away
expired unexpected entries**.

Require, before any download:

- exactly **six total** artifacts in the relevant current-run response;
- exactly the six ratified names;
- every artifact **non-expired**;
- **no unexpected artifact, expired or otherwise**;
- no duplicate artifact;
- no missing expected artifact.

Ratified names:

```text
b2a-portability-linux-py3.11
b2a-portability-linux-py3.12
b2a-portability-macos-py3.11
b2a-portability-macos-py3.12
b2a-portability-windows-py3.11
b2a-portability-windows-py3.12
```

The state **six valid expected artifacts plus one expired unexpected artifact
must fail before download**. The existing test that asserts success for that
state encodes the wrong expectation and must be reversed, not deleted and not
weakened.

## B3 — exact taxonomy propagation

The defect is confined to the **shell/workflow execution layer**. The Python
helper already raises the correct typed category for every guard it owns, and
those mappings are compliant. What is missing is category emission from the
workflow-side guards, which currently fail closed with prose only.

### Required category behaviour by failure path

| Failure path | Execution layer | Current state | Required category |
|---|---|---|---|
| Malformed canonical SHA dispatch input | Workflow guard step | **Absent** — prose only | `evidence_generation_failure` |
| Workflow-side artifact size violation (declared or transferred compressed bytes, aggregate compressed) | Workflow download step | **Absent** — prose only | `artifact_size_limit_exceeded` |
| Workflow-side unsafe archive condition, where applicable | Workflow steps | **Absent** — prose only | `unsafe_archive_entry` |
| Matrix or artifact-set cardinality failure | Workflow set-equality step | **Absent** — prose only | the applicable existing matrix or evidence-file category |
| Helper-side extraction, size, structure, encoding, manifest and comparison guards | Python helper | **Present and compliant** | unchanged — preserve exactly |

Constraints:

- **no twenty-second category** may be added; the ratified twenty-one are exact;
- the category must be **machine-verifiable** — emitted in a fixed, parseable
  position that a test can assert against, not merely mentioned in prose;
- the existing compliant helper-side mappings must be **preserved unchanged**;
  this finding does not authorize helper modification, and the helper path
  remains conditional under `FD-PV-16`.

## B4 — test-quality closure

Replace or correct:

- the tautological string-literal test that asserts a property of its own
  literals and never invokes the implementation;
- any guard or failure category whose runtime behaviour is claimed but proved
  only by a static source or wiring assertion;
- assertions that accept several unrelated categories where one deterministic
  category applies — the four multi-category sites identified in the findings;
- the expired-unexpected-artifact test that currently expects success.

Where runtime behaviour is claimed, the test must **execute the actual guard or
helper path** and assert **one exact intended outcome**. A test that would pass
for an unrelated early failure does not satisfy this requirement.

Static source and wiring assertions are **not** prohibited. They may remain as
**supplemental** checks that pin structure a runtime test cannot reach — such as
workflow permission blocks or action pinning — but they may not be the sole
proof that a guard fires or that a failure category is emitted.

## N1 — optional, non-blocking

The same commit may strengthen the consumer-failure test to use a payload large
enough that broken-pipe behaviour is observable, record both producer and
consumer statuses, and assert that the consumer status remains the controlling
diagnostic. This is permitted because it touches the same authorized test path.
It is not required and its absence does not block.

## Preservation requirements

The correction must preserve, and its tests must continue to prove:

- exactly-at-limit transfer succeeds; one byte over fails and removes partial
  output;
- declared oversize fails before download; declared and actual size mismatch
  fails;
- the exact six-artifact set passes;
- missing, duplicate and unexpected artifacts fail before download;
- permissions remain exactly `contents: read` and `actions: read`;
- the four `FD-PV-6` values — `1048576`, `4194304`, `6291456`, `25165824` — and
  their axes are unchanged;
- the twenty-one-category taxonomy is unchanged;
- Correction A's `canonical_sha` behaviour is unchanged, including complete
  omission from pull-request envelopes;
- schema `mesc-pilot-01-b2a-portability-evidence/1` is unchanged;
- every `uses:` entry stays pinned to an immutable full commit SHA;
- the six-cell matrix, `fail-fast: false`, timeouts, locked sync, 14-day
  retention, and the non-admissible pull-request output are unchanged.

## Required validation before the commit

```bash
git status --short
git diff --check
git diff --name-only
git diff --stat
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest -q tests/test_mesc_b2a_portability.py
uv run pytest -q
uv run medscale check
```

The changed path set must equal the authorized paths exactly.

## After the commit

Authorized: a normal non-force push, the automatically triggered pull-request
workflows, a PR #61 body update through the pull-request metadata endpoint, and
commissioning a new genuinely independent clean-room exact-head review.

Not authorized: marking PR #61 Ready, merging PR #61, auto-merge, manual
workflow rerun or dispatch, admissible evidence production or acceptance, B2A
acceptance, discharge of `N-12`, closure of the Windows or macOS obligations,
B2B, branch deletion, or any further commit.
