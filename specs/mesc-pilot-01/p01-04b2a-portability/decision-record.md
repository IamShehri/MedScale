# P01-04B2A Cross-Platform Portability Validation Infrastructure — Decision Record

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

## Controlling authority

D1–D10 (P01-04A) remain ratified policy and control on conflict. FD-B2-1
through FD-B2-8 and FD-B2A-1 through FD-B2A-8 remain the controlling design and
contract authority; this package neither amends nor reinterprets them. Binding
N-12 remains in force exactly as ratified.

Every decision below was ratified by the founder on 2026-07-27 and adopted as
`FD-PV-1` through `FD-PV-10`; the canonical record is `founder-ratification.md`.
Ratification freezes these design decisions only. It grants no
infrastructure-implementation, B2A-implementation, execution, or
evidence-production authority, and merging this package grants no authority.

---

## PD-PV-1 — Dedicated workflow boundary

A new dedicated portability workflow is proposed at
`.github/workflows/mesc-b2a-portability.yml`. The existing general workflow
`.github/workflows/ci.yml` is **not** modified and keeps its current
`ubuntu-latest` / Python 3.11 and 3.12 scope. Separating the workflows keeps the
fast general gate unchanged and confines six-cell cost and failure modes to the
portability gate.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-1
```

## PD-PV-2 — Exact six-cell matrix

The required matrix is exactly three operating systems by two Python versions:
`ubuntu-latest`, `windows-latest` and `macos-latest`, each with Python 3.11 and
3.12. `fail-fast: false` applies. No cell may be silently skipped; if an
authorized cell cannot run, the workflow fails rather than reporting success on
partial coverage.

FD-B2A-8's phrase "Python 3.12 where supported by the authorized validation
infrastructure" does **not** authorize dropping a matrix cell. This proposed
infrastructure defines all six cells as supported requirements. At the time of
this gate's review, the proposed hosted-runner matrix is available; availability
must be reverified at implementation time and is not asserted as permanent fact.
Once ratified, inability to execute one cell is a workflow failure, not
permission to exclude it, and any future removal, exclusion, or downgrade of a
cell requires a new founder decision.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-2
```

## PD-PV-3 — Least privilege and immutable dependencies

The workflow runs with `contents: read` only, no secrets, no write permissions,
no OIDC, no publication and no release creation. **All GitHub Actions, including
GitHub-owned actions such as checkout, upload-artifact, and download-artifact,
must be pinned to immutable full commit SHAs**; no tag-only reference such as
`@v4` is permitted, and the rule applies to every `uses:` entry. Dependencies
come only from the repository's locked `uv` environment. No cache may carry
generated evidence between runs.

Total network isolation is not achievable on a hosted runner and is not claimed.
The boundary is defined on two planes.

**Permitted infrastructure plane:** only the network activity required for
GitHub Actions orchestration, repository checkout, immutable GitHub Action
retrieval, Python installation where performed by the authorized runner setup,
and locked dependency resolution from the repository-configured package index.
This activity is bounded to infrastructure setup and must not supply evidence
inputs.

**Prohibited data plane:** no access to P01-03G, any dataset, model weights,
model APIs, medical or biomedical corpora, inference endpoints, retrieval
endpoints, training services, benchmark services, external evidence sources,
arbitrary URLs, or user-supplied network locations; no secrets, credentials,
OIDC tokens, or write-capable repository tokens; and no downloaded network
content may enter `canonical.json`, `canonical.jsonl`, `manifest.json`,
`portability-evidence.json`, or any hash or comparison input.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-3
```

## PD-PV-4 — Exact future repository paths

Infrastructure implementation is limited to exactly:

```text
.github/workflows/mesc-b2a-portability.yml
tests/_mesc_b2a_portability.py
tests/test_mesc_b2a_portability.py
```

No other path may be created or modified by the infrastructure pull request.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-4
```

## PD-PV-5 — Synthetic deterministic evidence set

Each cell emits exactly `canonical.json`, `canonical.jsonl` and `manifest.json`
from identical fixed synthetic inputs. The compared bytes carry no timestamps,
dates, paths, usernames, hostnames, OS name, Python version, runtime version,
run metadata, command logs or environment-specific metadata. OS and Python
identity live only in the matrix cell, the artifact name and the evidence
envelope.

Evidence files must be written as raw bytes using binary mode. The harness must
not use platform text-mode newline translation; LF (`0x0A`) is the only
permitted line terminator in the emitted bytes, and LF must never be transformed
into CRLF on Windows. The B2A canonical serializers produce the authoritative
bytes, and the portability harness must preserve those exact bytes when writing
them.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-5
```

## PD-PV-6 — Fail-closed aggregate verifier

A separate aggregate job requires all six matrix jobs, downloads exactly six
artifacts, and verifies exact artifact cardinality, exact file cardinality,
canonical manifests, recomputed SHA-256 values, recomputed byte sizes, and
byte-for-byte equality of all three compared files across all six cells. It
fails closed with typed, human-readable categories and emits evidence only after
every comparison passes.

The verifier compares the extracted evidence-file bytes only. It must never
compare ZIP archives, artifact-container bytes, archive metadata, file
permissions, executable bits, timestamps, or platform-specific extraction
metadata, and it must not normalize line endings, whitespace, encoding, Unicode,
JSON key ordering, or any other byte representation before comparison. Any byte
difference fails closed; normalization during comparison is prohibited because
it could conceal a genuine B2A determinism defect. Comparison measures B2A
output bytes, not GitHub artifact packaging behavior; archive extraction is
transport handling only.

Extraction is fail-closed: exactly six artifacts and exactly three regular files
per artifact, with rejection of absolute paths, `..` parent traversal, paths
escaping the extraction root, symbolic links, hard links, device files, FIFOs,
sockets, nested archives, unexpected directories or files, duplicate output
paths, and case-colliding names where the extraction platform could alias them,
under bounded memory and disk consumption.

```text
Exact numeric limits, founder-ratified 2026-07-27:

Maximum compressed size per matrix-cell artifact:
1048576 bytes (1 MiB)

Maximum total extracted size per matrix-cell artifact:
4194304 bytes (4 MiB)

Derived maximum compressed across exactly six artifacts:
6291456 bytes (6 MiB)

Derived maximum extracted across exactly six artifacts:
25165824 bytes (24 MiB)
```

Limits must be enforced before or during bounded extraction, never only after an
artifact has been fully written to disk. A violation at artifact, file, or
aggregate level fails closed with `artifact_size_limit_exceeded`. No artifact,
file, or aggregate may silently exceed these limits. Changing any of these limits
requires a new founder decision.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-6
```

## PD-PV-7 — Evidence-envelope separation

`portability-evidence.json` is validation evidence only. It never enters
`split_fingerprint`, never becomes a promoted B2A artifact, never alters the
four required split artifact roles, and never implies B2A acceptance by its
existence alone.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-7
```

## PD-PV-8 — Controlled triggers and retention

Proposed triggers are `pull_request` for exact-head review evidence and
`workflow_dispatch` for canonical-main acceptance evidence, with path filtering
limited to the B2A and portability paths. No schedules, webhooks, secrets or
automatic data/model execution. Proposed artifact retention is 14 days unless
the founder selects another period.

The `pull_request` path filter must include at least all seven executable or
measured paths: `.github/workflows/mesc-b2a-portability.yml`,
`tests/_mesc_b2a_portability.py`, `tests/test_mesc_b2a_portability.py`,
`src/medscale/mesc/_canonical_json_v1.py`,
`src/medscale/mesc/_split_artifacts_v1.py`,
`tests/test_mesc_canonical_json_v1.py` and
`tests/test_mesc_split_artifacts_v1.py`. It may additionally include the
portability documentation paths but must omit none of the above.

A `workflow_dispatch` run used for acceptance evidence must execute against an
exact canonical-main commit SHA, record that SHA in the workflow-run metadata
and in the validation-evidence envelope, be rejected for acceptance if initiated
from a noncanonical ref, not rely only on a mutable branch name, and not imply
acceptance merely because it succeeded. The exact canonical SHA belongs in the
non-promoted evidence envelope only; it never enters the compared golden-vector
bytes and never enters `split_fingerprint`.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-8
```

## PD-PV-9 — Implementation and merge sequencing

B2A code is implemented and reviewed under its own separate authorization,
limited to its four already-ratified implementation and test paths, and may be
merged only in a state recorded explicitly as `IMPLEMENTED BUT NOT ACCEPTED`.
The portability infrastructure is implemented afterwards, on a canonical main
that already contains the B2A implementation. B2A implementation and
infrastructure implementation must never be combined into one pull request.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-9
```

## PD-PV-10 — Acceptance remains a separate authority act

Passing the portability workflow does not automatically accept B2A. B2A
acceptance requires canonical-main evidence produced by `workflow_dispatch`,
independent Opus review of that evidence, and a separate founder/ChatGPT
acceptance decision. Only after B2A acceptance may B2B authorization be
considered.

```text
FOUNDER-RATIFIED 2026-07-27 AS FD-PV-10
```

---

## Founder action taken

The founder decided PD-PV-1 through PD-PV-10 on 2026-07-27, adopting them as
`FD-PV-1` through `FD-PV-10`, and selected the exact `FD-PV-6` numeric limits.
That decision does not by itself authorize infrastructure implementation, B2A
implementation, execution, evidence production, or B2A acceptance; each remains
a separate act.

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

## FD-PV-11 — Historical truth and prospective remediation authorization

Recorded 2026-07-30. The PR #61 implementation work predates any canonical
infrastructure-implementation authorization. This record does not retroactively
authorize it. Remediation and further review are authorized prospectively, only
after this package is adopted. PR #61 remains Draft until adoption,
non-rewriting synchronization, correction, passing exact-head workflows, a
genuinely independent exact-head review, and a separate Ready-transition
decision have all occurred.

```text
FOUNDER-RATIFIED 2026-07-30 AS FD-PV-11
```

## FD-PV-12 — Preserve FD-PV-6 through bounded artifact handling

The four `FD-PV-6` limits are unchanged. Compressed limits are measured against
artifact archive bytes and enforced before or during download; extracted limits
are measured against extracted regular-file bytes and enforced during bounded
extraction. Archive structure is inspected before extraction.
Post-extraction-only enforcement is prohibited. `1048576` is a compressed
per-artifact limit and must not be reinterpreted as an extracted per-file limit;
no general per-file 1 MiB extracted limit is ratified, and any such invented
limit is removed during remediation.

```text
FOUNDER-RATIFIED 2026-07-30 AS FD-PV-12
```

## FD-PV-13 — Narrow read-only Actions permission

`permissions: contents: read` is amended to `contents: read` plus
`actions: read`, solely for enumerating the current run's artifacts, reading
artifact metadata including archive byte size, and downloading the exact
expected artifacts through the documented GitHub Actions API. No other expansion
is authorized. The helper remains network-free.

```text
FOUNDER-RATIFIED 2026-07-30 AS FD-PV-13
```

## FD-PV-14 — Canonical SHA binding in the evidence envelope

`canonical_sha` is added to the evidence envelope for canonical-main
`workflow_dispatch` runs only, absent from pull-request envelopes, validated as
exactly 40 lowercase hexadecimal characters, passed explicitly from the guarded
dispatch input, never inferred from the environment, failing closed through
`evidence_generation_failure`. `mesc-pilot-01-b2a-portability-evidence/1` is
corrected in place; no version 2 is created.

```text
FOUNDER-RATIFIED 2026-07-30 AS FD-PV-14
```

## FD-PV-15 — Remediation and sequencing authority

A non-force merge commit synchronizes canonical main into the PR #61 branch,
preserving both existing commit identities, followed by exactly two additive
correction commits — Correction A for `FD-PV-14`, Correction B for `FD-PV-12`
and `FD-PV-13` — each confined to the three implementation paths.

```text
FOUNDER-RATIFIED 2026-07-30 AS FD-PV-15
```

The full text of `FD-PV-11` through `FD-PV-15` is canonical in
`founder-ratification.md`. This file records them for continuity only; on any
conflict the founder-ratification record controls.
