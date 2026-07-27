# P01-04B2A Cross-Platform Portability Validation Infrastructure — Decision Record

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

## Controlling authority

D1–D10 (P01-04A) remain ratified policy and control on conflict. FD-B2-1
through FD-B2-8 and FD-B2A-1 through FD-B2A-8 remain the controlling design and
contract authority; this package neither amends nor reinterprets them. Binding
N-12 remains in force exactly as ratified.

Every decision below is a proposal awaiting an explicit founder decision. None
is ratified. Recording them grants no authority, and merging this package grants
no authority.

---

## PD-PV-1 — Dedicated workflow boundary

A new dedicated portability workflow is proposed at
`.github/workflows/mesc-b2a-portability.yml`. The existing general workflow
`.github/workflows/ci.yml` is **not** modified and keeps its current
`ubuntu-latest` / Python 3.11 and 3.12 scope. Separating the workflows keeps the
fast general gate unchanged and confines six-cell cost and failure modes to the
portability gate.

```text
PENDING FOUNDER DECISION
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
PENDING FOUNDER DECISION
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
PENDING FOUNDER DECISION
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
PENDING FOUNDER DECISION
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
PENDING FOUNDER DECISION
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
Proposed default:
A small bounded limit sufficient for the three synthetic evidence files.

Exact numeric compressed and extracted byte limits:
PENDING FOUNDER DECISION
```

```text
PENDING FOUNDER DECISION
```

## PD-PV-7 — Evidence-envelope separation

`portability-evidence.json` is validation evidence only. It never enters
`split_fingerprint`, never becomes a promoted B2A artifact, never alters the
four required split artifact roles, and never implies B2A acceptance by its
existence alone.

```text
PENDING FOUNDER DECISION
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
PENDING FOUNDER DECISION
```

## PD-PV-9 — Implementation and merge sequencing

B2A code is implemented and reviewed under its own separate authorization,
limited to its four already-ratified implementation and test paths, and may be
merged only in a state recorded explicitly as `IMPLEMENTED BUT NOT ACCEPTED`.
The portability infrastructure is implemented afterwards, on a canonical main
that already contains the B2A implementation. B2A implementation and
infrastructure implementation must never be combined into one pull request.

```text
PENDING FOUNDER DECISION
```

## PD-PV-10 — Acceptance remains a separate authority act

Passing the portability workflow does not automatically accept B2A. B2A
acceptance requires canonical-main evidence produced by `workflow_dispatch`,
independent Opus review of that evidence, and a separate founder/ChatGPT
acceptance decision. Only after B2A acceptance may B2B authorization be
considered.

```text
PENDING FOUNDER DECISION
```

---

## Requested founder action

The founder is asked to decide PD-PV-1 through PD-PV-10. A decision on these
contracts does not by itself authorize infrastructure implementation, B2A
implementation, execution, evidence production, or B2A acceptance; each remains
a separate act.
