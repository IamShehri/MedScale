# P01-04B2A Cross-Platform Portability Validation Infrastructure — Acceptance

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

Acceptance is defined in three separate layers. Satisfying an earlier layer
never satisfies a later one.

---

## 1. Documentation-gate acceptance

Applies to this documentation pull request only.

| Criterion | Requirement |
|---|---|
| Path scope | Exactly eight authorized documentation paths |
| Decisions visible | PD-PV-1 through PD-PV-10 all present, adopted as FD-PV-1 through FD-PV-10 |
| Numeric limits | The FD-PV-6 compressed and extracted byte limits recorded exactly |
| No pre-adoption implementation authority | No pre-adoption remediation implementation authority. `FD-PV-15` activates only after canonical adoption and mechanical verification |
| No workflow change | No `.github/**` path changed |
| No source or test change | No `src/**` or `tests/**` path changed |
| No evidence claims | No document claims portability evidence exists or has passed |
| No acceptance claims | No document claims B2A is accepted |
| Internal links | All cross-references resolve |
| Canonical identities | Exact current base, PR #55 and PR #56 identities recorded |
| Local gates | Locked sync, Ruff lint, Ruff format, Mypy and Pytest pass |
| Exact-head verification | CI and CodeQL succeed on the exact head |
| Independent review | Independent Opus exact-head review |
| Merge | A separate merge decision |

### Documentation-gate stop conditions

Do not treat this gate as satisfied if any document authorizes implementation or
execution, claims Windows or macOS evidence exists, claims B2A is accepted,
claims P01-04B is complete, modifies a B2A contract or the founder-ratification
record, or modifies a path outside the nine authorized paths.

---

## 2. Future infrastructure-implementation acceptance

Applies only to a later, separately authorized infrastructure pull request.

| Criterion | Requirement |
|---|---|
| Path scope | Exactly the three proposed implementation paths, and no others |
| Base state | The B2A implementation is already present on its canonical base |
| `ci.yml` | Unmodified |
| Matrix | All six cells complete successfully |
| Artifacts | Exactly six artifacts exist |
| Files | Exactly three files per artifact |
| Bytes | All compared bytes identical across all six cells |
| Hashes and sizes | All recomputed SHA-256 values and byte sizes identical |
| Negative tests | Fail-closed tests exist for every proposed failure category |
| Permissions | Exactly `contents: read` and `actions: read`; no secrets, no write, no OIDC. `FD-PV-13` narrowly supersedes the original `contents: read` only criterion |
| Action pinning | Every `uses:` entry pinned to an immutable full commit SHA, including GitHub-owned actions; no tag-only reference such as `@v4` |
| Network boundary | Infrastructure-plane activity only (see below); no data-plane access |
| Binary writes | Evidence files written as raw bytes in binary mode |
| LF-only output | LF (`0x0A`) is the only line terminator in the emitted bytes |
| No CRLF translation | No platform text-mode newline translation on any runner |
| No comparison normalization | The verifier normalizes nothing — not line endings, whitespace, encoding, Unicode, or key ordering — before comparison |
| Extracted bytes only | Comparison targets extracted regular-file bytes; never archives, container bytes, archive metadata, permissions, executable bits, or extraction metadata |
| Safe extraction | Fail-closed rejection of absolute paths, `..` traversal, escapes from the extraction root, symlinks, hard links, device files, FIFOs, sockets, nested archives, unexpected entries, duplicate output paths, and case-colliding names; bounded memory and disk |
| Gates | CI and CodeQL green |
| Review | Independent Opus exact-head review |

### Network boundary detail

Total network isolation is not achievable on a hosted runner and is not claimed.

**Permitted — infrastructure plane.** Only the network activity required for
GitHub Actions orchestration, repository checkout, immutable GitHub Action
retrieval, Python installation where performed by the authorized runner setup,
and locked dependency resolution from the repository-configured package index.
This activity is bounded to infrastructure setup and must not supply evidence
inputs.

**Prohibited — data plane.** No access to P01-03G, any dataset, model weights,
model APIs, medical or biomedical corpora, inference endpoints, retrieval
endpoints, training services, benchmark services, external evidence sources,
arbitrary URLs, or user-supplied network locations. No secrets, credentials,
OIDC tokens, or write-capable repository tokens. No downloaded network content
may enter `canonical.json`, `canonical.jsonl`, `manifest.json`,
`portability-evidence.json`, or any hash or comparison input.

---

## 3. Future B2A acceptance

**Infrastructure acceptance is not B2A acceptance.** Merging a working
portability workflow accepts the workflow, not the increment it measures.

B2A acceptance requires all of:

1. the validation infrastructure merged on canonical main;
2. a canonical-main `workflow_dispatch` evidence run;
3. the exact canonical-main SHA recorded;
4. all six cells successful;
5. the aggregate verifier successful;
6. the evidence artifact inspected;
7. an independent Opus review of that evidence;
8. a separate founder/ChatGPT acceptance decision.

Only after B2A acceptance may B2B authorization be considered.

## 4. Standing prohibition

None of these layers authorizes execution against real data. At no point does
this package permit formal split generation, P01-03G or dataset access, model
access, inference, retrieval, training, metrics or benchmark execution,
publication, or clinical use.

Until a separate founder acceptance decision is recorded, B2A remains **not
accepted**, P01-04B remains **incomplete and not accepted**, and B2B remains
**not authorized**.

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

## Remediation acceptance criteria (FD-PV-11 through FD-PV-15)

Earlier criteria remain controlling except where `FD-PV-11` through `FD-PV-15`
expressly supersede them. The express supersessions are limited to the PR #62
documentation path count, pre-adoption versus post-adoption remediation
authority, the narrow addition of `actions: read`, and the remediation commit
sequence.

Nothing here weakens any evidence, data, model, execution, review, Ready, merge,
B2A, or B2B gate. Satisfying these criteria does not satisfy infrastructure
adoption and does not accept B2A.

| Criterion | Requirement |
|---|---|
| Governance adoption | This package adopted on canonical main before any correction commit |
| History preservation | Both PR #61 commits retain their exact object identities; no rebase, amend, squash, reset, cherry-pick, or force-push |
| Synchronization | Canonical main merged into the branch by a normal non-force merge commit |
| Correction scope | Exactly the three implementation paths; no dependency, lockfile, `src/**`, dataset, model, or public-API change |
| Compressed limits | Measured against artifact archive bytes and enforced before or during download |
| Extracted limits | Measured against extracted regular-file bytes and enforced during bounded extraction |
| Pre-extraction inspection | Archive structure inspected before any entry is written |
| Invented limit removed | No general per-file 1 MiB extracted limit remains |
| Resource safety | An oversized download or ZIP bomb is stopped before runner-disk exhaustion |
| Permission scope | Exactly `contents: read` and `actions: read`; no further expansion |
| Helper network boundary | The helper performs no network access |
| Envelope binding | `canonical_sha` present on canonical-main dispatch envelopes only, absent on pull-request envelopes, validated as 40 lowercase hex, failing closed via `evidence_generation_failure` |
| Schema | `mesc-pilot-01-b2a-portability-evidence/1` corrected in place; no version 2 |
| Taxonomy | The twenty-one ratified categories are preserved exactly, unrenamed and unextended |
| Test effectiveness | Every safe-extraction guard has a negative test that invokes the helper, reaches the guard, and asserts the exact category; no tautological or non-executing safety test remains; tests do not accept unrelated error categories |
| Exact-head verification | Exact-head workflows pass after correction |
| Independent review | A genuinely independent exact-head review, by a reviewer that did not author the work, approves the corrected head |
| Ready transition | A separate founder decision, issued after all of the above |

Meeting every row above still does **not** accept B2A, does not produce
admissible evidence, does not discharge binding `N-12`, does not close the
Windows or macOS obligations, and does not authorize B2B.
