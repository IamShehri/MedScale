# P01-04B2A Final Review Hold — Prospective Correction Brief

```text
THIS BRIEF IS NOT EXECUTABLE.
IT BECOMES EXECUTABLE ONLY AFTER ALL FIVE FD-PV-17 ACTIVATION CONDITIONS ARE
SATISFIED AND MECHANICALLY VERIFIED. RECORDING IT IN A DRAFT PULL REQUEST
ACTIVATES NOTHING.
```

Canonical authority: [`founder-disposition.md`](founder-disposition.md).

## Exact commit identity

```text
Required parent:
f68f8be8799c0ec67b26c319a4a06789f2ea1a7e

Recommended subject:
fix(mesc): close final portability review findings

Count:
exactly one additive commit
```

No tenth commit. No amendment, rebase, squash, reset, cherry-pick, or
force-push. Canonical `main` must not be synchronized into the branch.

## Exact paths

Primary: `.github/workflows/mesc-b2a-portability.yml`,
`tests/test_mesc_b2a_portability.py`. Conditional:
`tests/_mesc_b2a_portability.py`, only on proven necessity recorded in the
commit. Nothing else.

## F1 — large-response category stability

Replace every guard pipeline of the form `comm -23 … | grep -q .` with a
pipefail-safe design:

1. materialize the `comm` output into a file;
2. test that file with `-s`;
3. emit exactly `unexpected_matrix_cell` for the unexpected-artifact case, and
   the existing category for each other case;
4. add a large-response regression whose artifact set contains **many long
   unexpected names**, sized so the old pipeline would have taken the `SIGPIPE`
   path;
5. prove no download starts and no archive output survives.

The regression must **fail against head `f68f8be8799c0ec67b26c319a4a06789f2ea1a7e`**.

## F2 — real projection and pagination boundary

The stub must serve **raw GitHub artifact API JSON** and must exercise the real
projection the workflow passes:

```text
--paginate
--jq
.artifacts[]
name
size_in_bytes
expired
id
```

The stub must not return pre-rendered TSV while ignoring the projection
arguments. Required mutation proofs:

- restoring the old `select(.expired == false)` projection **fails** tests;
- dropping later pages **fails** tests;
- an expired unexpected artifact **on a later page** fails before download.

## F3 — dispatch guards

Either execute **both** dispatch-guard copies behaviourally, or prove their
executable bodies are byte-equivalent and execute the shared body behaviourally.

For malformed SHA inputs:

- assert the precise rejection diagnostic;
- assert `git rev-parse HEAD` was **not** called;
- make the git stub **reject unexpected commands**, so a fall-through is
  detectable;
- include whitespace and newline contamination in the dispatch-script corpus;
- test noncanonical ref and HEAD mismatch **separately**.

A test must not pass merely because a malformed SHA falls through to a later
failure carrying the same category.

## F4 — archive-cardinality behaviour

Execute the **actual** archive-cardinality step:

```text
6 archives — pass
5 archives — fail
7 archives — fail
```

For the failing counts assert exactly:

```text
MESC_PORTABILITY_FAILURE_CATEGORY=aggregate_verifier_internal_error
```

Also assert that exactly one category is emitted, that no downstream aggregation
or evidence output occurs, and that the test fails if the category is removed or
remapped.

## Settled mappings — do not change

```text
expired expected artifact:              missing_matrix_cell
post-validation archive-count mismatch: aggregate_verifier_internal_error
```

## Preservation

Preserve `permissions: contents: read` and `actions: read`; the six-cell matrix
and six ratified artifact names; the four `FD-PV-6` limits and axes; bounded
limit-plus-one transport; producer and consumer status checks; partial-file
cleanup; declared-versus-actual verification; bounded network-free ZIP
inspection and extraction; every archive-safety protection; `canonical_sha`
behaviour; schema `mesc-pilot-01-b2a-portability-evidence/1`; every immutable
action pin; exactly twenty-one taxonomy categories; no evidence upload on
pull-request validation; and no model, dataset, inference, training, benchmark,
or real split execution.

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

Authorized: a normal non-force push, the automatically triggered workflows, a
metadata-only PR #61 body correction through the pull-request metadata endpoint,
and commissioning a new genuinely independent exact-head review. Nothing else.
