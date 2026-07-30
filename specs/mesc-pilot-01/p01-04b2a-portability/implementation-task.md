# P01-04B2A Cross-Platform Portability Validation Infrastructure — Implementation Task

```text
THIS TASK IS NOT EXECUTABLE WITHOUT A SEPARATE FOUNDER IMPLEMENTATION AUTHORIZATION.
THE REMEDIATION BRIEF ADDED 2026-07-30 BECOMES EXECUTABLE ONLY AFTER THE
FD-PV-11 THROUGH FD-PV-15 GOVERNANCE PACKAGE IS ADOPTED ON CANONICAL MAIN.
```

```text
Status:
CONTRACTS FOUNDER RATIFIED;
REMEDIATION PROSPECTIVELY AUTHORIZED BY FD-PV-11 THROUGH FD-PV-15

Contracts:
FOUNDER RATIFIED

Historical initial implementation:
OCCURRED BEFORE CANONICAL AUTHORIZATION

Current remediation implementation:
PROSPECTIVELY AUTHORIZED AFTER THIS RECORD IS ADOPTED

Infrastructure adoption:
NOT ACHIEVED

Execution:
NOT AUTHORIZED

Admissible evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED

B2B:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

Canonical planning baseline:
`0884971f68619be8f25c3b905a3dcad7c5212101`

Founder ratification:
`FD-PV-1` through `FD-PV-10` ratified on 2026-07-27; see
`founder-ratification.md`.

This document is a brief describing what a future, separately authorized builder
would do. It records a design; it instructs no one to act now. Reading it grants
nothing.

---

## Preconditions before this brief becomes actionable

1. PD-PV-1 through PD-PV-10 decided by the founder. **Satisfied 2026-07-27**
   by `FD-PV-1` through `FD-PV-10`; see `founder-ratification.md`.
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

`tests/test_mesc_b2a_portability.py` must cover every failure category in
`spec.md` §11 with a deterministic negative test. All twenty-one categories:

```text
missing_matrix_cell
duplicate_matrix_cell
unexpected_matrix_cell
missing_evidence_file
unexpected_evidence_file
manifest_schema_mismatch
invalid_sha256
byte_size_mismatch
content_hash_mismatch
cross_platform_byte_mismatch
forbidden_runtime_metadata
noncanonical_manifest
evidence_generation_failure
bom_present
malformed_utf8
invalid_json
invalid_jsonl
duplicate_json_object_key
aggregate_verifier_internal_error
unsafe_archive_entry
artifact_size_limit_exceeded
```

Every category must fail closed. In particular, a negative test must prove that
duplicate JSON object keys are rejected rather than silently resolved by
last-wins parsing, and that an aggregate verifier internal error can never
produce a passing result.

Negative tests use synthetic in-memory fixtures and must not require a real
multi-platform run.

## Security controls

`contents: read` only. No secrets, no write permissions, no OIDC, no
publication, no releases, no evidence-bearing cache. **Every `uses:` entry,
including GitHub-owned actions such as checkout, upload-artifact and
download-artifact, must be pinned to an immutable full commit SHA**; no tag-only
reference such as `@v4` is permitted. Dependencies only from the locked `uv`
environment.

Network access follows the FD-PV-3 two-plane boundary. Total network isolation
is not achievable on a hosted runner and must not be claimed. Only
infrastructure-plane activity is permitted — GitHub Actions orchestration,
repository checkout, immutable Action retrieval, authorized Python setup, and
locked dependency resolution from the repository-configured index — and that
activity must never supply evidence inputs. The prohibited data plane covers
P01-03G, datasets, model weights, model APIs, medical and biomedical corpora,
inference, retrieval, training services, benchmark services, external evidence
sources, arbitrary URLs, and user-supplied network locations. No downloaded
network content may enter any evidence file, hash, or comparison input.

Artifact size limits are fixed by FD-PV-6 at `1048576` bytes compressed and
`4194304` bytes extracted per artifact, and `6291456` bytes compressed and
`25165824` bytes extracted across exactly six artifacts. Enforce them before or
during bounded extraction and fail closed with `artifact_size_limit_exceeded`.

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

## Historical chronology — status before FD-PV-11

This section preserves the status this document carried before founder decisions
`FD-PV-11` through `FD-PV-15` were recorded. It is retained as history. It is
**not** the current status, and it was **not** wrong when written: it accurately
described the period it covers.

```text
Status:
FOUNDER-RATIFIED CONTRACTS — IMPLEMENTATION NOT AUTHORIZED

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

Between the ratification of `FD-PV-1` through `FD-PV-10` on 2026-07-27 and the
adoption of this record, **no canonical infrastructure-implementation
authorization existed**. The implementation work now present in Draft PR #61 was
created during that period. `FD-PV-11` records that fact. It does not convert it
into retroactive authorization.

---

## Remediation brief (FD-PV-15)

This brief becomes executable only after this governance package is adopted on
canonical main, and only for the sequence recorded in `FD-PV-15`. It is not
executable at the time of writing.

Prerequisite: synchronize canonical main into
`feat/mesc-b2a-portability-infrastructure` with a normal non-force merge commit,
preserving both existing commit identities.

### Correction A — `fix(mesc): bind canonical SHA into portability evidence`

Implement `FD-PV-14`. Thread the already validated dispatch input explicitly
through the workflow into the aggregate invocation and into the envelope
builder. Validate exactly 40 lowercase hexadecimal characters. Fail closed via
`evidence_generation_failure` for uppercase, empty, short, long, non-hex, ref,
branch, and tag values. Omit the field entirely on pull-request runs. Never read
it from `GITHUB_SHA` or any other uncontrolled environment value. Preserve
deterministic canonical serialization and the twenty-one-category taxonomy.

### Correction B — `fix(mesc): enforce bounded portability artifact extraction`

Implement `FD-PV-12` and `FD-PV-13`. Replace automatic full extraction with
bounded artifact handling: enumerate the current run's artifacts and read their
archive byte sizes before download; enforce the `1048576` per-artifact and
`6291456` aggregate compressed limits before or during transport; cap download
bytes; inspect archive entries before extraction; extract through bounded
chunked reads; enforce the `4194304` per-artifact and `25165824` aggregate
extracted limits during extraction; and remove the invented per-file 1 MiB
extracted limit. Add real negative tests for every safe-extraction guard,
replace any tautological or non-executing safety test, and tighten tests that
accept multiple unrelated error categories.

Both corrections are confined to:

```text
.github/workflows/mesc-b2a-portability.yml
tests/_mesc_b2a_portability.py
tests/test_mesc_b2a_portability.py
```

No dependency, lockfile, `src/**`, dataset, model, or public-API change is
authorized. Neither existing commit may be amended or rewritten.

The size-limit sentence earlier in this document describing `1048576` bytes
compressed and `4194304` bytes extracted per artifact remains correct. The axes
are made explicit by `FD-PV-12`: compressed limits bind archive bytes, extracted
limits bind extracted regular-file bytes, and neither may be enforced only after
extraction has completed.
