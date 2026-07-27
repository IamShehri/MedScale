# P01-04B2A Cross-Platform Portability Validation Infrastructure — Acceptance

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

Acceptance is defined in three separate layers. Satisfying an earlier layer
never satisfies a later one.

---

## 1. Documentation-gate acceptance

Applies to this documentation pull request only.

| Criterion | Requirement |
|---|---|
| Path scope | Exactly eight authorized documentation paths |
| Decisions visible | PD-PV-1 through PD-PV-10 all present and all pending |
| No implementation authority | No document authorizes infrastructure or B2A implementation |
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
record, or modifies a path outside the eight authorized paths.

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
| Permissions | `contents: read` only; no secrets, no write, no OIDC |
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
