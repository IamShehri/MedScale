# P01-04B2A Cross-Platform Portability Validation Infrastructure — Specification

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

---

## 1. Problem

FD-B2A-8 and binding N-12 require deterministic golden-vector byte and hash
identity across Linux, Windows and macOS, and across Python 3.11 and 3.12. The
repository's general workflow runs only `ubuntu-latest` with Python 3.11 and
3.12, so the required Windows and macOS evidence cannot be produced today and
does not exist.

This specification proposes the contract for infrastructure that could produce
that evidence, so the contract can be frozen by founder decision before any code
is written.

## 2. Proposed future implementation paths

If, and only if, infrastructure implementation is separately authorized, exactly
these three paths may be created:

```text
.github/workflows/mesc-b2a-portability.yml
tests/_mesc_b2a_portability.py
tests/test_mesc_b2a_portability.py
```

These are proposals. This task creates none of them and modifies none of them.

The future infrastructure pull request **must not modify**
`.github/workflows/ci.yml`. The general CI workflow remains exactly as it is
today: `ubuntu-latest`, Python 3.11 and 3.12. The portability workflow is a
separate, dedicated workflow.

The future infrastructure pull request must also not modify `src/**`, the four
ratified B2A implementation and test paths, `pyproject.toml`, `uv.lock`, or any
B2A contract, decision, acceptance, plan or founder-ratification document.

## 3. Required operating-system and Python matrix

Exactly six cells:

| OS runner | Python |
|---|---|
| `ubuntu-latest` | `3.11` |
| `ubuntu-latest` | `3.12` |
| `windows-latest` | `3.11` |
| `windows-latest` | `3.12` |
| `macos-latest` | `3.11` |
| `macos-latest` | `3.12` |

Matrix rules:

- `fail-fast: false`, so every cell reports independently and a single failure
  never hides the state of the others;
- explicit per-job timeouts;
- locked dependency synchronization only;
- no matrix exclusions unless separately founder-authorized;
- if an authorized cell cannot run, the workflow **fails**; it must never
  silently downgrade to a smaller matrix or report success on partial coverage.

## 4. Proposed triggers

Proposed:

- `pull_request` — produces exact-head evidence for review of an infrastructure
  or B2A change;
- `workflow_dispatch` — produces canonical-main evidence, which is the only
  evidence admissible for a B2A acceptance decision.

Explicitly **not** proposed: schedules, external webhooks, automatic model or
dataset execution, secrets, or write permissions.

Path filtering should limit runs to the future B2A implementation and test paths
and the portability paths, so unrelated documentation changes do not consume
runners.

## 5. Permissions and supply-chain controls

- `permissions: contents: read` only.
- No secrets of any kind.
- No write permissions.
- No OIDC.
- No package publication.
- No release creation.
- No cache that could carry generated evidence between runs.
- Third-party GitHub Actions pinned to immutable full commit SHAs, never to
  mutable tags or branches.
- Dependency installation only through the repository's locked `uv` environment.

## 6. Synthetic-only inputs

All inputs are fixed synthetic fixtures authored inside the repository.

The workflow must not access P01-03G, load datasets, access models, perform
inference, perform retrieval, perform training, calculate clinical or benchmark
metrics, access external medical corpora, perform formal split generation, or
use secrets.

## 7. Per-cell deterministic evidence

Each of the six cells produces exactly three files:

```text
canonical.json
canonical.jsonl
manifest.json
```

The compared contents must:

- be UTF-8 bytes;
- contain no BOM;
- use the ratified canonical serialization (FD-B2A-3);
- contain no timestamps;
- contain no dates;
- contain no local paths;
- contain no usernames;
- contain no hostnames;
- contain no OS name;
- contain no Python version;
- contain no runtime version;
- contain no GitHub run metadata;
- contain no command logs;
- contain no environment-specific metadata;
- be generated from exactly the same synthetic inputs in every cell.

`manifest.json` must itself be canonical and must contain only deterministic
schema identifiers, file names, SHA-256 values, and byte sizes.

**Identity separation.** Operating-system and Python identity is carried only in
the GitHub matrix cell, the uploaded artifact name, and the later
validation-evidence envelope. It must never be written into the compared
golden-vector files — doing so would make the bytes differ by construction and
destroy the very property under test.

## 8. Artifact names and retention

Proposed deterministic artifact names:

```text
b2a-portability-linux-py3.11
b2a-portability-linux-py3.12
b2a-portability-windows-py3.11
b2a-portability-windows-py3.12
b2a-portability-macos-py3.11
b2a-portability-macos-py3.12
```

Artifact names identify cells; the deterministic bytes they contain must be
identical across all six.

Proposed retention: **14 days**, unless the founder selects another period.

## 9. Aggregate verification

A separate aggregate job must:

1. require all six matrix jobs to have succeeded;
2. download exactly six artifacts;
3. reject missing artifacts;
4. reject duplicate artifacts;
5. reject unexpected artifacts;
6. reject missing files within any artifact;
7. reject extra files within any artifact;
8. recompute every SHA-256;
9. recompute every byte size;
10. validate every canonical manifest;
11. compare `canonical.json` byte-for-byte across all six cells;
12. compare `canonical.jsonl` byte-for-byte across all six cells;
13. compare `manifest.json` byte-for-byte across all six cells;
14. fail on the first or accumulated mismatch using typed, human-readable
    failure categories;
15. produce the validation-evidence envelope **only after** every comparison
    passes.

## 10. Validation-evidence envelope

Proposed non-promoted file:

```text
portability-evidence.json
```

It may record: a schema identifier; the six expected cell identifiers; each
compared file name; the authoritative SHA-256; the authoritative byte size; and
the overall result.

It must not contain timestamps, mutable URLs, local paths, hostnames,
usernames, command logs, or secrets.

It is a validation record only. It must never become an input to
`split_fingerprint`, never be represented as a promoted B2A artifact, never
alter the four required split artifact roles, and never imply B2A acceptance by
its existence alone.

## 11. Failure taxonomy

Proposed fail-closed categories:

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
```

These categories are **proposed**. None of them exists in repository code today,
and this document does not claim otherwise.

## 12. Relationship to B2A implementation

This infrastructure exercises the private B2A implementation; it does not
contain it. The two are separate pull requests under separate authorizations,
and must never be combined. The infrastructure is implemented only on a
canonical main that already contains the B2A implementation it must exercise.
