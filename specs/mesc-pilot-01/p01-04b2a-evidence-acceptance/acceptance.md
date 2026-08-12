# P01-04B2A Evidence Acceptance — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-PV-19:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN
```

Two layers. Satisfying the first never satisfies the second.

---

## 1. This governance documentation gate

| Criterion | Requirement |
|---|---|
| Canonical baseline | Exactly `e3478da94e62ad9af5858a69e28de7e5d5fc04f4`, tree `e64e57a1c6c94703a7f20ef6598256fa77600b31`, ordered parents `69f16455...` then `626a23f0...`, subject `docs(mesc): authorize B2A portability evidence production (#65)` |
| PR #65 truth | Recorded as MERGED / CLOSED / NOT DRAFT, merged head `626a23f0...`, merged `2026-08-01T01:19:29Z`, scope 5 files / +909 / -1 |
| Unused identifiers | `FD-PV-19` and `P01-T03B10` verified unused on canonical main before this package |
| Run identity | Run `30678040133`, run number 8, `event: workflow_dispatch`, `run_attempt: 1`, `head_branch: main`, `head_sha` equal to the canonical baseline, actor `IamShehri`, created `2026-08-01T01:30:04Z`, completed / success |
| One dispatch, zero reruns | Workflow history: 8 total runs, 7 `pull_request`, exactly 1 `workflow_dispatch`, 0 runs with `run_attempt > 1` |
| Job topology | 6 generation jobs plus 1 aggregate job, all success; pull-request aggregation skipped; dispatch aggregation executed; evidence upload executed exactly once |
| Artifact inventory | Exactly 7 artifacts — 6 cell artifacts and 1 `b2a-portability-evidence`; 0 duplicates, 0 missing, 0 unexpected, 0 expired at inspection and at review |
| Artifact identity | Every artifact ID, archive byte size and archive SHA-256 recorded exactly, and every artifact bound to run `30678040133` |
| Payload identity | `canonical.json` 228 bytes, `canonical.jsonl` 79 bytes, `manifest.json` 308 bytes, with their exact SHA-256 digests, byte-identical across all six cells |
| Schemas | Manifest `mesc-pilot-01-b2a-portability-manifest/1`; evidence `mesc-pilot-01-b2a-portability-evidence/1`; `result: pass`; `canonical_sha` equal to the canonical baseline |
| NB3 checks | `NB3-A`, `NB3-B` and `NB3-C` each recorded as PASS |
| Content boundary | Recorded as PASS, with GitHub artifact API metadata distinguished from prohibited runtime-derived evidence content |
| Independent review | Recorded verdict `APPROVE WITH NON-BLOCKING NOTES` |
| No blocking findings | Recorded as NONE |
| Non-blocking observations | `NB-01` and `NB-02` recorded with their dispositions; neither requires a correction, new run, rerun, replacement artifact, or implementation change |
| Path scope | Only this package's four documents plus `specs/mesc-pilot-01/tasks.md` |
| No implementation change | No `.github/**`, `tests/**`, `src/**`, `pyproject.toml`, `uv.lock`, dataset, model, contract, serializer, or public-API path changed |
| No workflow action | No dispatch, rerun, cancellation, or replacement run during this package; run `30678040133` untouched |
| No artifact action | No artifact edited, deleted, downloaded, recommitted, published, or mirrored; no artifact bytes embedded |
| No B2A claim | No B2A acceptance, no `N-12` discharge, no platform-obligation closure, no B2B authorization |
| No execution claim | No real Pilot-01 split, B0, model access, dataset access, inference, retrieval, training, or fine-tuning |
| Adoption boundary | `FD-PV-19` classified as issued but NOT YET ADOPTED while the pull request is Draft or unmerged; five adoption conditions stated and no subset sufficient |
| Ledger integrity | Historical snapshots preserved; superseding truth appended, not rewritten; exactly one live `Current controlling state` block |
| No duplication | Prior history linked, not restated |
| Internal links | All relative links resolve |
| No placeholders | Every value concrete; no deferred-work marker, stub token, or unfilled substitution slot |
| Exact-head verification | CI and CodeQL succeed on this package's exact head |
| Independent review of this package | A genuinely independent clean-room exact-head review, required before Ready |
| Ready and merge | Each a separate founder decision, after that review |

### Stop conditions

Do not treat this gate as satisfied if any document accepts B2A; discharges
binding `N-12`; closes the Windows or macOS obligation; authorizes B2B;
completes P01-04B acceptance; dispatches, reruns, cancels or replaces any
workflow run; edits, deletes or embeds any artifact; treats a pull-request
artifact as admissible evidence; claims `FD-PV-19` is adopted while the pull
request is Draft or unmerged; revives consumed `FD-PV-18`; rewrites or deletes a
historical governance snapshot; leaves two blocks simultaneously claiming to be
the current controlling state; or modifies any path outside the authorized five.

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later B2A acceptance decision

Not made by this package and not authorized by it.

| Criterion | Requirement |
|---|---|
| Prerequisite | This package independently reviewed, marked Ready, merged, and mechanically verified on canonical `main` |
| Scope | A separate founder decision addressing B2A acceptance on its own governing criteria |
| Binding `N-12` | A separate disposition decision |
| Platform obligations | Separate closure decisions for Windows and macOS |
| B2B | A separate authorization decision |
| P01-04B | A separate acceptance decision |

Accepting the portability evidence establishes deterministic six-cell canonical
serialization at `e3478da94e62ad9af5858a69e28de7e5d5fc04f4` and nothing further.
It does **not** accept B2A, discharge binding `N-12`, close the Windows or macOS
obligations, complete P01-04B acceptance, or authorize B2B.

---

## 3. Standing prohibition

At no point does this package permit execution against real data, the real
Pilot-01 split, B0, benchmark execution, model training or fine-tuning, P01-03G
or dataset access, model access, inference, retrieval, publication, or clinical
use.
