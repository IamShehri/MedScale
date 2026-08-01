# P01-04B2A Acceptance — Decision Basis

```text
Status:
IMMUTABLE BASIS RECORD

Canonical baseline:
1f2d9152281f3136d212dcf7729063f7b1c64ad1
```

Every fact below was verified from GitHub and immutable Git objects. No artifact
bytes are embedded, duplicated, downloaded, mirrored or republished.

---

## 1. Contract authority — PR #55

```text
PR:                        #55
Title:                     docs(mesc): define P01-04B2A authorization gate
State:                     CLOSED / MERGED / NOT DRAFT
Canonical merge:           5c083a0c5f23d0f9837e7543c444633a68524e67
Founder-ratification head: edc09743a1aa9478c2accbe9debb8fcc5bcbe268
Ratification date:         2026-07-26
```

Ratified contracts:

```text
FD-B2A-1 — Private module boundary
FD-B2A-2 — Canonical value domain
FD-B2A-3 — Canonical JSON and JSONL
FD-B2A-4 — Artifact descriptors
FD-B2A-5 — Non-circular fingerprint model
FD-B2A-6 — Split-summary identity core
FD-B2A-7 — Fail-closed validation
FD-B2A-8 — Determinism evidence
```

`FD-B2A-5` incorporates the non-circular fingerprint clarification and
validation sequence recorded under the historical proposal label `PD-B2A-5.1`.
That clarification is part of the ratified contract, not a later amendment.

The canonical record is at
[`../p01-04b2a/founder-ratification.md`](../p01-04b2a/founder-ratification.md).

## 2. The ratified N-12 sequencing decision

Reproduced from the canonical record without alteration:

```text
B2A implementation acceptance must not be declared while the Windows and macOS
portability obligation remains open.

Linux evidence on Python 3.11 and Python 3.12 is partial evidence only.

Before B2A may be declared accepted, deterministic golden-vector bytes and
hashes must be demonstrated as identical across:

- Linux;
- Windows;
- macOS;
- Python 3.11;
- Python 3.12 where supported by the authorized validation infrastructure.

Until that evidence is produced and independently reviewed:

- B2A remains not accepted;
- the portability obligation remains open;
- B2B authorization must not be granted;
- no artifact may be promoted on the claim of completed cross-platform
  determinism.

Any workflow or validation-infrastructure change requires separate founder
authorization.
```

`N-12`'s ratified scope is **P01-04B2A deterministic portability evidence**. It
does not require model execution, real-data execution, split execution,
retrieval, training or benchmark results, and it is not reinterpreted here.

## 3. Implementation identity — PR #59

```text
PR:                    #59
Title:                 feat(mesc): implement B2A canonical artifact contracts
State:                 CLOSED / MERGED / NOT DRAFT
Canonical merge:       5736b1171f1aa467105d931713f5749fb81acd5b
Final merged PR head:  7307fcf9085d3d15114984731b49d484523f09eb
Final reviewed tree:   575fcf124792cd38b546a58a6845ad2ecd317281
Commits:               2
Changed files:         4
Statistics:            +2559 / -0
```

Exact scope:

| Path | Lines |
|---|---:|
| `src/medscale/mesc/_canonical_json_v1.py` | +183 |
| `src/medscale/mesc/_split_artifacts_v1.py` | +490 |
| `tests/test_mesc_canonical_json_v1.py` | +792 |
| `tests/test_mesc_split_artifacts_v1.py` | +1094 |

The implementation provides:

```text
private immutable artifact types
strict canonical JSON and JSONL bytes
exact primitive-type and fail-closed validation
deterministic mapping snapshots
SHA-256 descriptors and byte-size binding
immutable split-summary identity state
non-circular split-fingerprint construction
split-summary descriptor rebinding
typed deterministic errors
synthetic tests and literal committed golden vectors
no public export or execution entry point
```

## 4. Accepted implementation observations

Recorded accurately; neither was corrected, and neither is upgraded into
accepted public behaviour or used to expand scope.

```text
Implementation NB-01:
A deliberately malformed low-level object that omits the required
split_summary descriptor may produce an untyped StopIteration.

Disposition:
NON-BLOCKING.

Supported construction paths guarantee all four descriptor roles and fail
closed. This observation does not affect the ratified public authority boundary,
canonical serialization result or accepted construction path.
```

```text
Implementation NB-02:
Some descriptor/core field validators may accept primitive subclasses before
canonical serialization rejects them.

Disposition:
NON-BLOCKING.

Such values cannot reach an authoritative canonical hash and fail closed during
the canonical serialization boundary.
```

## 5. Portability infrastructure identity — PR #61

```text
Infrastructure adoption PR:            #61
Canonical infrastructure merge:        69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3
Final reviewed infrastructure head:    7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae
```

The infrastructure was independently reviewed (`APPROVE WITH NON-BLOCKING NOTES`,
no blocking findings) and adopted on canonical `main` **before** the
evidence-production authority `FD-PV-18` was activated. Adoption of the
infrastructure is not evidence production; the two are distinct acts.

The workflow preserves exactly six matrix cells:

```text
linux-py3.11    linux-py3.12
macos-py3.11    macos-py3.12
windows-py3.11  windows-py3.12
```

It is evidence-only. It performs no model, dataset, split, retrieval, inference,
training or real-data execution. It is byte-identical between its adoption merge
`69f16455...` and canonical baseline `1f2d9152...` — unmodified and not rerun.

## 6. Evidence run identity

```text
Workflow:                MESC B2A Portability
Workflow ID:             323476626
Run ID:                  30678040133
Run number:              8
Event:                   workflow_dispatch
Run attempt:             1
Head branch:             main
Evidence canonical SHA:  e3478da94e62ad9af5858a69e28de7e5d5fc04f4
Status:                  completed
Conclusion:              success
```

```text
Total portability runs:     8
pull_request runs:          7   — infrastructure validation only, non-admissible
workflow_dispatch runs:     1   — the sole authorized evidence dispatch
Runs with run_attempt > 1:  0
```

```text
Topology:   6 generation jobs and 1 aggregate job, all success
Artifacts:  6 cell artifacts and 1 evidence artifact = 7 total;
            0 duplicates, 0 missing, 0 unexpected,
            0 expired at inspection and at independent review
```

## 7. Payload identities

Byte-identical and hash-identical across all six OS/Python cells:

| File | Bytes | SHA-256 |
|---|---:|---|
| `canonical.json` | 228 | `7c5668f7b90c5c4cbe62bb0b073c97ed8e8084419d34cad41bc245d98f3873b8` |
| `canonical.jsonl` | 79 | `bb1dcc82390f4168ba2a644c0bf4d40313d735c9a59db97d90a383dfa3a7b266` |
| `manifest.json` | 308 | `da30b9ad0ba9d30547075ecb4ab7e7798b9e354d6d3f068e27c702eba6f5244d` |

```text
Cross-cell byte identity:  PASSED ACROSS ALL SIX CELLS
Manifest schema:           mesc-pilot-01-b2a-portability-manifest/1
Evidence schema:           mesc-pilot-01-b2a-portability-evidence/1
Evidence result:           pass
NB3-A:                     PASS
NB3-B:                     PASS
NB3-C:                     PASS
Content boundary:          PASS
```

The complete artifact ledger — artifact IDs, archive byte sizes, archive
SHA-256 digests, job topology and step conclusions — is adopted by reference at
[`../p01-04b2a-evidence-acceptance/evidence-ledger.md`](../p01-04b2a-evidence-acceptance/evidence-ledger.md)
and is deliberately not duplicated.

## 8. Independent evidence review and FD-PV-19

```text
Independent clean-room evidence review verdict:
APPROVE WITH NON-BLOCKING NOTES — CANONICAL PORTABILITY EVIDENCE
ELIGIBLE FOR A SEPARATE FOUNDER EVIDENCE-ACCEPTANCE DECISION

Blocking findings:
NONE
```

```text
Evidence NB-01:
ZIP Unix permission metadata differs by producer:
0644 on Linux/macOS and 0666 on Windows.

Disposition:
NON-BLOCKING — archive metadata only; payload bytes and identities are
unchanged.
```

```text
Evidence NB-02:
Broad substring scans initially produced false positives from "decomposed"
and "windows-py3.11".

Disposition:
NON-BLOCKING — methodology observation only; precise inspection found no
prohibited provenance or runtime content.
```

```text
FD-PV-19:
Decision:              ACCEPT — CANONICAL PORTABILITY EVIDENCE
Adopted on canonical main: YES
ADOPTED_SHA:           1f2d9152281f3136d212dcf7729063f7b1c64ad1
```

`FD-PV-19` adoption verification:

```text
PR #66:            CLOSED / MERGED / NOT DRAFT
Merge SHA:         1f2d9152281f3136d212dcf7729063f7b1c64ad1
Merged head:       bf26351ff84c7ed6d30f0ad054109309af64b04b
Merged at:         2026-08-01T02:37:09Z
Tree:              83de598c69c5ab963f400f9f69d1d0b2a3b0ac81
Ordered parents:   e3478da94e62ad9af5858a69e28de7e5d5fc04f4
                   bf26351ff84c7ed6d30f0ad054109309af64b04b
Scope:             1 commit / 5 files / +1056 / -1
Reviewed head -> final merge:    zero file delta
Synthetic merge a1e248e9... -> final merge:  zero file delta
```

## 9. N-12 requirement-to-evidence mapping

| # | N-12 prerequisite | Evidence | Result |
|---|---|---|---|
| 1 | Linux deterministic golden-vector identity | Cells `linux-py3.11` and `linux-py3.12` of run `30678040133` succeeded and produced the three canonical files at the recorded digests | **SATISFIED** |
| 2 | Windows deterministic golden-vector identity | Cells `windows-py3.11` and `windows-py3.12` succeeded and produced the same three files at the same digests | **SATISFIED** |
| 3 | macOS deterministic golden-vector identity | Cells `macos-py3.11` and `macos-py3.12` succeeded and produced the same three files at the same digests | **SATISFIED** |
| 4 | Python 3.11 identity | The `py3.11` cell of every one of the three operating systems succeeded with identical digests | **SATISFIED** |
| 5 | Python 3.12 identity | The `py3.12` cell of every one of the three operating systems succeeded with identical digests | **SATISFIED** |
| 6 | Cross-cell byte and hash equality | Cross-cell byte identity PASSED across all six cells; every cell resolves to `canonical.json` `7c5668f7…`, `canonical.jsonl` `bb1dcc82…`, `manifest.json` `da30b9ad…`; aggregate verification succeeded; `NB3-A`, `NB3-B` and `NB3-C` PASS | **SATISFIED** |
| 7 | Independent evidence review | Genuinely independent clean-room review returned `APPROVE WITH NON-BLOCKING NOTES` with no blocking findings | **SATISFIED** |
| 8 | Separate founder evidence acceptance and canonical adoption | `FD-PV-19` accepted the exact evidence and was canonically adopted at `1f2d9152281f3136d212dcf7729063f7b1c64ad1`, mechanically verified | **SATISFIED** |

```text
N-12:
SATISFIED IN SUBSTANCE

Binding sequencing block:
DISCHARGED FOR P01-04B2A BY FD-B2A-9

Windows portability obligation:
CLOSED FOR P01-04B2A BY FD-B2A-9

macOS portability obligation:
CLOSED FOR P01-04B2A BY FD-B2A-9
```

The N-12 clause "no artifact may be promoted on the claim of completed
cross-platform determinism" is also satisfied: the claim is now supported by
produced, verified, independently reviewed and canonically adopted evidence, and
no artifact is promoted beyond that.

## 10. Why this decision is limited to P01-04B2A

Each of the following is a distinct governed act, and none substitutes for
another:

```text
contract ratification              FD-B2A-1..8, PR #55
implementation adoption            PR #59 merge 5736b117...
portability-infrastructure adoption PR #61 merge 69f16455...
evidence production                run 30678040133 under FD-PV-18
mechanical evidence verification   digests, topology, NB3-A/B/C
independent evidence review        APPROVE WITH NON-BLOCKING NOTES
founder evidence acceptance        FD-PV-19 decision
canonical adoption of FD-PV-19     merge 1f2d9152...
B2A implementation acceptance      FD-B2A-9 — this package
canonical adoption of FD-B2A-9     a later, separate merge
N-12 discharge                     FD-B2A-9, scoped to P01-04B2A
Windows obligation closure         FD-B2A-9, scoped to P01-04B2A
macOS obligation closure           FD-B2A-9, scoped to P01-04B2A
B2B authorization                  a later, separate decision — NOT AUTHORIZED
P01-04B overall acceptance         a later, separate decision — NOT ACHIEVED
real split execution               NOT AUTHORIZED
model or dataset execution         NOT AUTHORIZED
```

The evidence establishes exactly one proposition: that the private canonical
serialization of PR #59 produces byte-identical and hash-identical output across
six ratified OS/Python cells at `e3478da94e62ad9af5858a69e28de7e5d5fc04f4`. That
proposition discharges the P01-04B2A portability obligation and no other.

It says nothing about the remaining P01-04B subphases, about any real dataset or
model, about split generation, or about benchmark, training or inference
behaviour — none of which was exercised, and none of which becomes authorized.
B2A acceptance therefore makes a later B2B authorization decision *eligible for
consideration* and nothing more.
