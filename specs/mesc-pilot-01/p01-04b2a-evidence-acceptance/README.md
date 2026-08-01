# P01-04B2A Evidence Acceptance

```text
Status:
FOUNDER EVIDENCE-ACCEPTANCE DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

FD-PV-18:
ACTIVATED AND CONSUMED

Evidence run:
30678040133 — COMPLETED / SUCCESS

Mechanical evidence verification:
PASSED

Independent evidence review:
COMPLETED — APPROVE WITH NON-BLOCKING NOTES

FD-PV-19:
RECORDED BUT NOT YET ADOPTED

Canonical portability evidence:
FOUNDER-ACCEPTED IN SUBSTANCE

B2A acceptance:
NOT ACHIEVED

N-12:
BINDING AND UNDISCHARGED

Windows and macOS obligations:
OPEN

B2B:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

Canonical baseline:
`e3478da94e62ad9af5858a69e28de7e5d5fc04f4`

Adopted authorization:
`PR #65` — merge `e3478da94e62ad9af5858a69e28de7e5d5fc04f4`, tree
`e64e57a1c6c94703a7f20ef6598256fa77600b31`, merged head
`626a23f01db978d43d51cdbae2c4378d2cf1733f`, 2 commits, 5 files, +909 / -1,
merged `2026-08-01T01:19:29Z`

---

## Purpose

This package records the founder's acceptance of the canonical portability
evidence produced by the single `FD-PV-18`-authorized dispatch. It records a
decision about **evidence**. It does not accept B2A.

The package dispatches nothing, reruns nothing, downloads nothing, and changes
no implementation path. Prior governance history is adopted at
[`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/),
[`../p01-04b2a-final-review-hold/`](../p01-04b2a-final-review-hold/) and
[`../p01-04b2a-evidence-production-gate/`](../p01-04b2a-evidence-production-gate/)
and is **not** restated here.

## Run and review identity

```text
Workflow:      MESC B2A Portability (323476626)
Run ID:        30678040133
Run number:    8
Event:         workflow_dispatch
Run attempt:   1
Head branch:   main
Head SHA:      e3478da94e62ad9af5858a69e28de7e5d5fc04f4
Actor:         IamShehri
Created:       2026-08-01T01:30:04Z
Status:        completed
Conclusion:    success
```

`FD-PV-18` authorized exactly one dispatch request and was consumed when GitHub
accepted it. The workflow history holds 8 runs total — 7 `pull_request`
infrastructure-validation runs and this single `workflow_dispatch` run — with
zero reruns. No retry, rerun, second dispatch, or replacement run is authorized.

The independent clean-room evidence review of that run returned:

```text
APPROVE WITH NON-BLOCKING NOTES — CANONICAL PORTABILITY EVIDENCE
ELIGIBLE FOR A SEPARATE FOUNDER EVIDENCE-ACCEPTANCE DECISION

Blocking findings:
NONE
```

## Accepted evidence summary

Seven artifacts, all bound to run `30678040133`, all non-expired at inspection
and at review:

```text
b2a-portability-evidence         509 bytes
b2a-portability-linux-py3.11     855 bytes
b2a-portability-linux-py3.12     855 bytes
b2a-portability-macos-py3.11     855 bytes
b2a-portability-macos-py3.12     855 bytes
b2a-portability-windows-py3.11   855 bytes
b2a-portability-windows-py3.12   855 bytes
```

Each of the six cell artifacts carries the exact canonical file set, byte-identical
across every OS and Python cell:

```text
canonical.json    228 bytes
canonical.jsonl    79 bytes
manifest.json     308 bytes
```

```text
Cross-cell byte identity:  PASSED ACROSS ALL SIX CELLS
Manifest schema:           mesc-pilot-01-b2a-portability-manifest/1
Evidence schema:           mesc-pilot-01-b2a-portability-evidence/1
Evidence result:           pass
Evidence canonical_sha:    e3478da94e62ad9af5858a69e28de7e5d5fc04f4
NB3-A / NB3-B / NB3-C:     PASS / PASS / PASS
```

The full ledger, including artifact IDs, archive digests, job topology and step
conclusions, is recorded in
[`evidence-ledger.md`](evidence-ledger.md).

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-disposition.md`](founder-disposition.md) | **Controlling**: `FD-PV-19`, its prerequisites, the accepted non-blocking observations, the adoption conditions, and the acts that remain separate |
| [`evidence-ledger.md`](evidence-ledger.md) | Immutable record of the run, its jobs, its seven artifacts, their digests and the verified payload identities |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for this governance package |

On any conflict, [`founder-disposition.md`](founder-disposition.md) controls.

## Evidence acceptance is not B2A acceptance

These are two different decisions and this package makes only the first.

| Decision | State after this package |
|---|---|
| Canonical portability evidence accepted | **Yes, in substance** — pending adoption of this package |
| B2A accepted | **No** |
| Binding `N-12` discharged | **No** |
| Windows and macOS obligations closed | **No** |
| B2B authorized | **No** |
| P01-04B complete | **No** |

Accepting the evidence establishes that the six-cell canonical serialization is
byte-identical across Linux, macOS and Windows on Python 3.11 and 3.12 at
`e3478da9...`. It establishes nothing else. B2A acceptance, the binding `N-12`
disposition, closure of the platform obligations, and B2B authorization each
remain separate later founder decisions with their own gates.

## Adoption boundary

While this package's pull request is Draft or unmerged, `FD-PV-19` is a
**recorded founder decision that is not yet canonically adopted**. Adoption
requires, in order: a genuinely independent clean-room exact-head review of this
package, a separate founder Ready decision, a separate founder merge decision,
merge into canonical `main`, and mechanical post-merge verification.

## What this package does not do

It does not accept B2A, discharge binding `N-12`, close the Windows or macOS
obligations, authorize B2B, complete P01-04B acceptance, dispatch or rerun any
workflow, cancel or replace run `30678040133`, edit or delete any artifact,
download or embed evidence bytes, change any implementation path, execute the
real Pilot-01 split, run B0, access model weights or the real dataset, run
inference, retrieval, training or fine-tuning, or authorize a Ready transition
or merge.
