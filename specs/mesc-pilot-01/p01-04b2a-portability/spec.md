# P01-04B2A Cross-Platform Portability Validation Infrastructure — Specification

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

### Reconciliation with "where supported"

FD-B2A-8 requires Python 3.12 identity "where supported by the authorized
validation infrastructure". That phrase does **not** authorize dropping a matrix
cell. This proposed infrastructure defines all six cells as supported
requirements.

At the time of this gate's review, the proposed hosted-runner matrix is
available: GitHub-hosted `ubuntu-latest`, `windows-latest` and `macos-latest`
provide Python 3.11 and 3.12. Availability must be reverified at implementation
time and is not asserted here as permanent fact.

Once ratified, inability to execute one cell is a **workflow failure**, not
permission to exclude that cell. Any future removal, exclusion, or downgrade of
a cell requires a new founder decision.

## 4. Proposed triggers

Proposed:

- `pull_request` — produces exact-head evidence for review of an infrastructure
  or B2A change;
- `workflow_dispatch` — produces canonical-main evidence, which is the only
  evidence admissible for a B2A acceptance decision.

Explicitly **not** proposed: schedules, external webhooks, automatic model or
dataset execution, secrets, or write permissions.

Path filtering should limit runs so unrelated documentation changes do not
consume runners. The `pull_request` filter must include at least all seven
executable or measured paths:

```text
.github/workflows/mesc-b2a-portability.yml
tests/_mesc_b2a_portability.py
tests/test_mesc_b2a_portability.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
tests/test_mesc_canonical_json_v1.py
tests/test_mesc_split_artifacts_v1.py
```

The filter may additionally include the portability documentation paths, but it
must omit none of the paths above. Omitting the workflow file itself, or any B2A
implementation path, would let a change to the measured code or to the measuring
harness escape validation.

### Canonical-main dispatch binding

A `workflow_dispatch` run used for acceptance evidence must:

- execute against an exact canonical-main commit SHA;
- record that SHA in the workflow-run metadata and in the validation-evidence
  envelope;
- be rejected for acceptance if it was initiated from a noncanonical ref;
- not rely only on a mutable branch name;
- not imply acceptance merely because the run succeeded.

The exact canonical SHA belongs in the non-promoted evidence envelope only. It
must never enter the compared golden-vector bytes and must never enter
`split_fingerprint`.

## 5. Permissions and supply-chain controls

- `permissions: contents: read` only.
- No secrets of any kind.
- No write permissions.
- No OIDC.
- No package publication.
- No release creation.
- No cache that could carry generated evidence between runs.
- **All GitHub Actions, including GitHub-owned actions such as checkout,
  upload-artifact, and download-artifact, must be pinned to immutable full
  commit SHAs.** No tag-only reference such as `@v4` is permitted. This rule
  applies to every `uses:` entry in the workflow, without exception.
- Dependency installation only through the repository's locked `uv` environment.

### Network boundary

Total network isolation is not achievable on a hosted runner and is not claimed
here. The boundary is defined on two planes.

**Permitted infrastructure-plane network activity.** Only the network activity
required for:

- GitHub Actions orchestration;
- repository checkout;
- immutable GitHub Action retrieval;
- Python installation where performed by the authorized runner setup;
- locked dependency resolution from the repository-configured package index.

This activity is bounded to infrastructure setup and must not supply evidence
inputs of any kind.

**Prohibited data-plane network activity.** The workflow must not access
P01-03G, any dataset, model weights, model APIs, medical or biomedical corpora,
inference endpoints, retrieval endpoints, training services, benchmark services,
external evidence sources, arbitrary URLs, or user-supplied network locations.

No secrets, credentials, OIDC tokens, or write-capable repository tokens may be
used.

No downloaded network content may enter `canonical.json`, `canonical.jsonl`,
`manifest.json`, `portability-evidence.json`, or any hash or comparison input.

## 6. Synthetic-only inputs

All inputs are fixed synthetic fixtures authored inside the repository.

The workflow must not perform inference, perform retrieval, perform training,
calculate clinical or benchmark metrics, or perform formal split generation.

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

### Binary byte-write discipline

This rule is controlling for both evidence generation and comparison.

- Evidence files must be written as raw bytes using **binary mode**.
- The validation harness must not use platform text-mode newline translation.
- LF (`0x0A`) is the only permitted line terminator in the emitted canonical
  JSON and JSONL bytes.
- The harness must not transform LF into CRLF on Windows.
- The aggregate verifier compares the extracted evidence-file bytes only.
- It must never compare ZIP archives, artifact-container bytes, archive
  metadata, file permissions, executable bits, timestamps, or platform-specific
  extraction metadata.
- The verifier must not normalize line endings, whitespace, encoding, Unicode,
  JSON key ordering, or any other byte representation before comparison.
- Any byte difference must fail closed. Normalization during comparison is
  prohibited because it could conceal a genuine B2A determinism defect.

Division of responsibility:

- the B2A canonical serializers produce the **authoritative bytes**;
- the portability harness must **preserve those exact bytes** when writing them
  to disk;
- comparison measures **B2A output bytes**, not GitHub artifact packaging
  behavior;
- archive extraction is only transport handling and is never part of the
  deterministic value being compared.

Without this rule, a default text-mode write would translate LF to CRLF on
Windows, producing a false failure that looks like a B2A determinism defect; and
repairing that by normalizing during comparison would produce a false success
that conceals real defects.

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

### Safe extraction and resource bounds

Artifact download and extraction is transport handling only. The aggregate
verifier must, fail-closed:

- expect exactly six artifacts;
- impose the ratified maximum compressed size per artifact;
- impose the ratified maximum total extraction size;
- permit exactly three regular files per artifact;
- reject absolute paths;
- reject `..` parent traversal;
- reject paths escaping the intended extraction root;
- reject symbolic links;
- reject hard links;
- reject device files;
- reject FIFOs;
- reject sockets;
- reject nested archives;
- reject unexpected directories or files;
- reject duplicate output paths;
- reject case-colliding names where the extraction platform could alias them;
- use bounded memory and disk consumption;
- compare extracted regular-file bytes only.

### Founder-ratified size limits

`FD-PV-6` fixes the exact limits:

| Limit | Bytes | Equivalent |
|---|---|---|
| Maximum compressed size per matrix-cell artifact | `1048576` | 1 MiB |
| Maximum total extracted size per matrix-cell artifact | `4194304` | 4 MiB |
| Derived maximum compressed across exactly six artifacts | `6291456` | 6 MiB |
| Derived maximum extracted across exactly six artifacts | `25165824` | 24 MiB |

The derived aggregate values are exactly six times the corresponding per-artifact
limits, so an aggregate total can never silently exceed the per-artifact
contract.

Limits must be enforced **before or during** bounded extraction, never only after
an artifact has been fully written to disk; enforcing only after the fact would
defeat the resource bound the limit exists to impose. A violation at artifact,
file, or aggregate level fails closed with `artifact_size_limit_exceeded`. No
artifact, file, or aggregate may silently exceed these limits. Changing any of
these limits requires a new founder decision.

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
bom_present
malformed_utf8
invalid_json
invalid_jsonl
duplicate_json_object_key
aggregate_verifier_internal_error
unsafe_archive_entry
artifact_size_limit_exceeded
```

These are **proposed names only**. No implementation exists in repository code
today, and this document does not claim otherwise.

Every category fails closed. In particular:

- `duplicate_json_object_key` — duplicate keys must be **rejected**, never
  silently resolved by a parser's last-wins behavior, because silent resolution
  would hide a nondeterministic serializer;
- `aggregate_verifier_internal_error` — an internal verifier error can **never**
  produce a passing result; it always fails the run;
- `bom_present`, `malformed_utf8`, `invalid_json`, `invalid_jsonl` — encoding
  and parse defects are reported under their own categories rather than folded
  into a generic failure, so a real defect stays diagnosable;
- `unsafe_archive_entry`, `artifact_size_limit_exceeded` — extraction-safety and
  resource-bound violations abort the run before any comparison occurs.

## 12. Relationship to B2A implementation

This infrastructure exercises the private B2A implementation; it does not
contain it. The two are separate pull requests under separate authorizations,
and must never be combined. The infrastructure is implemented only on a
canonical main that already contains the B2A implementation it must exercise.

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

## Amendments recorded 2026-07-30 (FD-PV-12, FD-PV-13, FD-PV-14)

These amendments control on conflict with any earlier section of this
specification. Earlier text is retained above as the ratified contract as it
stood before 2026-07-30.

### Size limits — measurement axis and enforcement timing (FD-PV-12)

The four `FD-PV-6` byte values are unchanged. Their axes are now explicit:

| Limit | Bytes | Axis | Scope | Enforced |
|---|---|---|---|---|
| Max compressed per artifact | `1048576` | Compressed archive bytes | Per artifact | Before or during download |
| Max extracted per artifact | `4194304` | Extracted regular-file bytes | Per artifact | During bounded extraction |
| Max compressed across six | `6291456` | Compressed archive bytes | Aggregate | Before or during download |
| Max extracted across six | `25165824` | Extracted regular-file bytes | Aggregate | During bounded extraction |

`1048576` is a **compressed per-artifact** limit. It must not be applied as an
extracted per-file limit, and no general per-file extracted limit is ratified.
Archive structure must be inspected before extraction. Post-extraction-only
enforcement is prohibited. An oversized download or ZIP bomb must be stopped
before it can exhaust runner disk.

### Permissions (FD-PV-13)

Section 5's `permissions: contents: read` only rule is amended to:

```yaml
permissions:
  contents: read
  actions: read
```

`actions: read` is confined to enumerating the current run's artifacts, reading
artifact metadata including archive byte size, and downloading the exact
expected artifacts through the documented GitHub Actions API. It authorizes no
mutation, rerun, cancellation, dispatch, deletion, write scope, secret, OIDC,
publication, cache, or cross-run or cross-repository access. The workflow
performs metadata lookup and capped transport; the helper remains network-free
and reads only bounded local ZIP files.

### Evidence envelope (FD-PV-14)

The canonical-main dispatch binding in section 4 is satisfied by an explicit
envelope field:

```json
"canonical_sha": "<40 lowercase hexadecimal commit SHA>"
```

Present only for canonical-main `workflow_dispatch` envelopes; absent from
pull-request envelopes; equal to the guarded checked-out HEAD; passed explicitly
from the validated dispatch input and never inferred from the environment;
validated as exactly 40 lowercase hexadecimal characters, with uppercase, empty,
short, long, non-hex, ref, branch, and tag values failing closed through
`evidence_generation_failure`. It never enters the three compared files and
never enters `split_fingerprint`. Schema
`mesc-pilot-01-b2a-portability-evidence/1` is corrected in place; no version 2
is created.
