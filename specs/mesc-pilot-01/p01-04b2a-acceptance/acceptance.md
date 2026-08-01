# P01-04B2A Acceptance — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-B2A-9:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN
```

Two layers. Satisfying the first never satisfies the second.

---

## 1. This governance documentation gate

| Criterion | Requirement |
|---|---|
| Canonical baseline | Exactly `1f2d9152281f3136d212dcf7729063f7b1c64ad1`, tree `83de598c69c5ab963f400f9f69d1d0b2a3b0ac81`, ordered parents `e3478da9...` then `bf26351f...`, subject `docs(mesc): record B2A portability evidence acceptance (#66)` |
| PR #66 truth | Recorded as CLOSED / MERGED / NOT DRAFT, merged head `bf26351f...`, merged `2026-08-01T02:37:09Z`, 1 commit / 5 files / +1056 / -1; reviewed-head-to-merge and synthetic-to-merge deltas both zero files |
| Unused identifiers | `FD-B2A-9` and `P01-T03B11` verified unused across the complete canonical tree, task ledgers, founder dispositions and adopted decision packages |
| New directory | `specs/mesc-pilot-01/p01-04b2a-acceptance/` did not exist on canonical main |
| Contract identity | PR #55 merge `5c083a0c...`, ratification head `edc09743...`, `FD-B2A-1` through `FD-B2A-8` recorded, `FD-B2A-5` including the `PD-B2A-5.1` non-circular clarification |
| N-12 fidelity | The ratified `N-12` text reproduced without alteration and not reinterpreted as requiring model, real-data, split, retrieval, training or benchmark execution |
| Implementation identity | PR #59 merge `5736b117...`, merged head `7307fcf9...`, reviewed tree `575fcf12...`, 2 commits / 4 files / +2559 / -0, and the exact four-path scope |
| Implementation observations | `NB-01` and `NB-02` recorded accurately, not claimed corrected, not upgraded into accepted public behaviour, not used to expand scope |
| Infrastructure identity | PR #61 merge `69f16455...`, reviewed head `7c1522eb...`; independently reviewed and adopted before `FD-PV-18` activation; six matrix cells preserved; evidence-only |
| Evidence identity | Run `30678040133`, run number 8, `event: workflow_dispatch`, `run_attempt: 1`, `head_branch: main`, evidence canonical SHA `e3478da9...`, completed / success |
| Evidence history | 8 total runs — 7 `pull_request`, 1 `workflow_dispatch`, 0 reruns |
| Evidence topology | 6 generation jobs and 1 aggregate job, all success |
| Artifact inventory | 6 cell artifacts and 1 evidence artifact = 7; 0 duplicates, 0 missing, 0 unexpected, 0 expired at inspection and at independent review |
| Payload identities | `canonical.json` 228 B, `canonical.jsonl` 79 B, `manifest.json` 308 B, with their exact SHA-256 digests, byte-identical across all six cells |
| Verification conclusions | Cross-cell byte identity PASSED; manifest and evidence schemas recorded; evidence `result: pass`; `NB3-A`, `NB3-B`, `NB3-C` and content boundary all PASS |
| Ledger by reference | The complete artifact ledger linked, not duplicated; no artifact bytes embedded, downloaded, recommitted, mirrored or republished |
| Evidence review | Verdict `APPROVE WITH NON-BLOCKING NOTES`, blocking findings `NONE`; evidence `NB-01` and `NB-02` recorded with dispositions |
| FD-PV-19 | Recorded as ACCEPT and as adopted on canonical main at `1f2d9152...` |
| N-12 mapping complete | All eight prerequisites individually mapped to evidence and each marked SATISFIED |
| Founder decisions bounded | `FD-B2A-9` accepts the P01-04B2A implementation, discharges `N-12` for P01-04B2A, and closes the Windows and macOS obligations for P01-04B2A — and nothing wider |
| Decisions actually made | The package makes these founder decisions; it does not merely state that they are technically eligible |
| No B2B authorization | No B2B authorization and no prospective B2B implementation authority anywhere in the package |
| No whole-phase acceptance | P01-04B recorded as INCOMPLETE / NOT ACCEPTED |
| No execution authority | No real split, B0/B1, model access, dataset access, inference, retrieval, metrics, benchmark, training, fine-tuning, publication or clinical claim |
| Pre-adoption classification | While Draft, Ready-but-unmerged, or merged-but-unverified: `FD-B2A-9` issued but not adopted; B2A accepted in substance only; `N-12` canonically binding; both platform obligations canonically open |
| Adoption conditions | All five stated, with `No subset adopts FD-B2A-9.` |
| Path scope | Only this package's four documents plus `specs/mesc-pilot-01/tasks.md` |
| No implementation change | No `.github/**`, `src/**`, `tests/**`, `pyproject.toml`, `uv.lock`, dataset, model, contract, serializer, public-API, repository-setting or artifact change |
| Historical packages preserved | No prior governance package modified; prior pre-adoption language superseded additively, never rewritten |
| Ledger integrity | Historical snapshots preserved; the previous live block annotated as superseded using the established additive pattern; exactly one unannotated live `Current controlling state` block remains |
| Terminology | The seventeen governed concepts kept distinct; none substituted for another |
| Internal links | All relative links resolve |
| No unresolved markers | Every value concrete; no unresolved drafting marker, stub token, unfilled substitution slot, provisional-value token, or working-directory reference appears anywhere in the package |
| Exact-head verification | CI and CodeQL succeed on this package's exact head |
| Independent review | A genuinely independent clean-room exact-head review of this package, required before Ready |
| Ready and merge | Each a separate founder decision, after that review |

### Stop conditions

Do not treat this gate as satisfied if any document authorizes B2B, B2C or B2D;
accepts P01-04B as a whole; authorizes the real Pilot-01 split, B0 or B1,
dataset or model access, inference, retrieval, metrics, benchmark execution,
training or fine-tuning; dispatches, reruns or cancels a workflow; mutates,
downloads or republishes artifacts; revives consumed `FD-PV-18`; claims
`FD-B2A-9` is adopted while the pull request is Draft or unmerged; claims the
implementation observations were corrected; reinterprets `N-12` beyond
deterministic portability evidence; rewrites or deletes a historical governance
assertion; modifies any prior governance package; leaves two blocks
simultaneously claiming to be the current controlling state; or modifies any
path outside the authorized five.

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later decisions this package does not make

| Decision | State |
|---|---|
| Canonical adoption of `FD-B2A-9` | Requires the five adoption conditions |
| B2B authorization | **NOT AUTHORIZED** — a separate later decision, merely eligible for consideration once B2A is adopted |
| B2C, B2D | **NOT AUTHORIZED** |
| P01-04C through P01-04G | **NOT AUTHORIZED** |
| P01-04B whole-phase acceptance | **NOT ACHIEVED** |
| Real Pilot-01 split, B0/B1 | **NOT AUTHORIZED** |
| Model access, real dataset access, P01-03G | **NOT AUTHORIZED** |
| Inference, retrieval, metrics, benchmark execution | **NOT AUTHORIZED** |
| Training, fine-tuning | **NOT AUTHORIZED** |
| Publication, clinical use | **NOT AUTHORIZED** |

---

## 3. Standing prohibition

At no point does this package permit execution against real data, the real
Pilot-01 split, B0 or B1, benchmark execution, model training or fine-tuning,
P01-03G or dataset access, model access, inference, retrieval, publication, or
clinical use.
