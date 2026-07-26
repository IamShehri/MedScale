# P01-04B2A Cross-Platform Portability Validation Infrastructure — Implementation Task

```text
THIS TASK IS NOT EXECUTABLE WITHOUT A SEPARATE FOUNDER IMPLEMENTATION AUTHORIZATION.
```

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

This document is a brief describing what a future, separately authorized builder
would do. It records a design; it instructs no one to act now. Reading it grants
nothing.

---

## Preconditions before this brief becomes actionable

1. PD-PV-1 through PD-PV-10 decided by the founder.
2. A separate infrastructure-implementation authorization naming an exact
   canonical baseline.
3. The B2A implementation already present on that canonical baseline, merged in
   a state recorded as `IMPLEMENTED BUT NOT ACCEPTED`.

If any precondition is absent, stop without mutation.

## Proposed exact paths

Create exactly:

```text
.github/workflows/mesc-b2a-portability.yml
tests/_mesc_b2a_portability.py
tests/test_mesc_b2a_portability.py
```

Do not modify `.github/workflows/ci.yml`, `src/**`, the four ratified B2A
implementation and test paths, `pyproject.toml`, `uv.lock`, or any B2A contract,
decision, acceptance, plan or founder-ratification document.

## Matrix

Six cells, `fail-fast: false`, explicit timeouts, locked dependency
synchronization, no exclusions:

| OS runner | Python |
|---|---|
| `ubuntu-latest` | `3.11` |
| `ubuntu-latest` | `3.12` |
| `windows-latest` | `3.11` |
| `windows-latest` | `3.12` |
| `macos-latest` | `3.11` |
| `macos-latest` | `3.12` |

An authorized cell that cannot run is a failure, never a silent downgrade.

## Artifact generation

Each cell generates, from fixed synthetic inputs only, exactly:

```text
canonical.json
canonical.jsonl
manifest.json
```

The bytes must carry no timestamps, dates, local paths, usernames, hostnames, OS
name, Python version, runtime version, run metadata, command logs, or
environment-specific metadata, and no BOM. `manifest.json` is itself canonical
and carries only deterministic schema identifiers, file names, SHA-256 values,
and byte sizes.

Upload per-cell artifacts named:

```text
b2a-portability-linux-py3.11
b2a-portability-linux-py3.12
b2a-portability-windows-py3.11
b2a-portability-windows-py3.12
b2a-portability-macos-py3.11
b2a-portability-macos-py3.12
```

Retention 14 days unless the founder selected another period.

## Aggregation

A separate aggregate job requires all six matrix jobs, downloads exactly six
artifacts, and enforces the fifteen checks in `spec.md` §9 — artifact
cardinality, file cardinality, recomputed SHA-256 values, recomputed byte sizes,
canonical manifest validation, and byte-for-byte equality of all three compared
files across all six cells — failing closed with typed categories and emitting
`portability-evidence.json` only after every comparison passes.

## Negative tests

`tests/test_mesc_b2a_portability.py` must cover every proposed failure category
with a deterministic negative test: `missing_matrix_cell`,
`duplicate_matrix_cell`, `unexpected_matrix_cell`, `missing_evidence_file`,
`unexpected_evidence_file`, `manifest_schema_mismatch`, `invalid_sha256`,
`byte_size_mismatch`, `content_hash_mismatch`, `cross_platform_byte_mismatch`,
`forbidden_runtime_metadata`, `noncanonical_manifest`,
`evidence_generation_failure`.

Negative tests use synthetic in-memory fixtures and must not require a real
multi-platform run.

## Security controls

`contents: read` only. No secrets, no write permissions, no OIDC, no
publication, no releases, no evidence-bearing cache. Third-party actions pinned
to immutable full commit SHAs. Dependencies only from the locked `uv`
environment. No dataset, model, network, or external corpus access.

## Stop conditions

Stop without mutation if authorization is absent or withdrawn; if canonical main
differs from the authorized baseline; if the B2A implementation is not present
on that baseline; if any path outside the three proposed paths would change; if
`ci.yml` would change; if secrets, write permissions, OIDC or data/model access
would be required; or if any document would claim B2A acceptance.

## Verification commands

```bash
git status --short
git diff --check
git diff --name-only <authorized-baseline>
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest -q
```

## Required report format

A future builder report must state: the authorized baseline; the exact three
changed paths; the six matrix cell results; artifact and file cardinality; the
recomputed hashes and byte sizes; the aggregate comparison result; negative-test
results; local gate results; exact-head CI and CodeQL conclusions; commit,
parent, tree and branch identities; and an explicit statement that infrastructure
success is not B2A acceptance.

## One-commit and one-PR rule

Exactly one atomic commit and exactly one Draft pull request. No force-push. No
Ready transition, no merge, no auto-merge. B2A implementation must never be
combined with this infrastructure work.
