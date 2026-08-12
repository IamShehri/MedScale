# P01-04B2A Acceptance

```text
Status:
FOUNDER IMPLEMENTATION-ACCEPTANCE DECISION ISSUED — NOT YET ADOPTED ON
CANONICAL MAIN

FD-B2A-9:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2A:
FOUNDER-ACCEPTED IN SUBSTANCE; NOT YET CANONICALLY ADOPTED

N-12:
FOUNDER DISCHARGE DECISION ISSUED;
CANONICALLY BINDING UNTIL THIS PACKAGE IS ADOPTED

Windows portability obligation:
FOUNDER CLOSURE DECISION ISSUED;
CANONICALLY OPEN UNTIL THIS PACKAGE IS ADOPTED

macOS portability obligation:
FOUNDER CLOSURE DECISION ISSUED;
CANONICALLY OPEN UNTIL THIS PACKAGE IS ADOPTED

P01-04B as a whole:
INCOMPLETE / NOT ACCEPTED

B2B:
NOT AUTHORIZED
```

Canonical baseline:
`1f2d9152281f3136d212dcf7729063f7b1c64ad1`

---

## Purpose

This package records the founder's acceptance of the **P01-04B2A
implementation**, the discharge of the binding `N-12` sequencing obligation for
P01-04B2A, and the closure of the Windows and macOS portability obligations for
P01-04B2A.

It is documentation only. It dispatches nothing, reruns nothing, downloads
nothing, and changes no implementation, test, workflow, dependency or artifact
path.

Prior governance history is adopted at
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/),
[`../p01-04b2a-final-review-hold/`](../p01-04b2a-final-review-hold/),
[`../p01-04b2a-evidence-production-gate/`](../p01-04b2a-evidence-production-gate/)
and
[`../p01-04b2a-evidence-acceptance/`](../p01-04b2a-evidence-acceptance/)
and is **not** restated here.

## Canonical baseline

```text
Merge SHA:
1f2d9152281f3136d212dcf7729063f7b1c64ad1

Tree:
83de598c69c5ab963f400f9f69d1d0b2a3b0ac81

Ordered parent 1:
e3478da94e62ad9af5858a69e28de7e5d5fc04f4

Ordered parent 2:
bf26351ff84c7ed6d30f0ad054109309af64b04b

Subject:
docs(mesc): record B2A portability evidence acceptance (#66)
```

## Accepted implementation identity

```text
Contract authority:
PR #55 — merge 5c083a0c5f23d0f9837e7543c444633a68524e67
FD-B2A-1 through FD-B2A-8 ratified 2026-07-26

Implementation:
PR #59 — merge 5736b1171f1aa467105d931713f5749fb81acd5b
merged head 7307fcf9085d3d15114984731b49d484523f09eb
tree 575fcf124792cd38b546a58a6845ad2ecd317281
2 commits / 4 files / +2559 / -0
```

Exactly four implementation paths, all private and non-executable:

```text
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
tests/test_mesc_canonical_json_v1.py
tests/test_mesc_split_artifacts_v1.py
```

The acceptance decision applies to **this exact implementation identity** under
**these exact ratified contracts**, and to nothing else.

## Evidence and FD-PV-19 adoption identity

```text
Portability infrastructure:
PR #61 — merge 69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3
reviewed head 7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae

Evidence run:
MESC B2A Portability (323476626) run 30678040133, run number 8,
event workflow_dispatch, run_attempt 1, head_branch main,
evidence canonical SHA e3478da94e62ad9af5858a69e28de7e5d5fc04f4,
completed / success

Independent evidence review:
APPROVE WITH NON-BLOCKING NOTES — no blocking findings

FD-PV-19:
ACCEPT — CANONICAL PORTABILITY EVIDENCE
ADOPTED ON CANONICAL MAIN at 1f2d9152281f3136d212dcf7729063f7b1c64ad1
```

The complete artifact ledger is adopted by reference at
[`../p01-04b2a-evidence-acceptance/evidence-ledger.md`](../p01-04b2a-evidence-acceptance/evidence-ledger.md)
and is not duplicated here. No artifact bytes are embedded, downloaded,
recommitted, mirrored or republished.

## N-12 satisfaction summary

The ratified `N-12` sequencing decision requires deterministic golden-vector
bytes and hashes demonstrated identical across Linux, Windows, macOS, Python
3.11 and Python 3.12, produced and independently reviewed, before B2A may be
declared accepted.

```text
Linux identity                    SATISFIED
Windows identity                  SATISFIED
macOS identity                    SATISFIED
Python 3.11 identity              SATISFIED
Python 3.12 identity              SATISFIED
Cross-cell byte and hash equality SATISFIED
Independent evidence review       SATISFIED
Founder acceptance and adoption   SATISFIED

N-12:  SATISFIED IN SUBSTANCE
```

The full requirement-to-evidence mapping is in
[`decision-basis.md`](decision-basis.md).

`N-12`'s ratified scope is P01-04B2A deterministic portability evidence. It is
**not** a requirement for model execution, real-data execution, split execution,
retrieval, training or benchmark results, and is not reinterpreted as such here.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-disposition.md`](founder-disposition.md) | **Controlling**: `FD-B2A-9`, the acceptance decision, the `N-12` discharge, the Windows and macOS closures, the adoption conditions, and the continuing separation |
| [`decision-basis.md`](decision-basis.md) | The immutable basis — contracts, implementation, infrastructure, evidence, review, `FD-PV-19`, and the `N-12` mapping |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for this governance package |

On any conflict, [`founder-disposition.md`](founder-disposition.md) controls.

## Adoption boundary

While this package's pull request is Draft, Ready-but-unmerged, or
merged-but-not-mechanically-verified, every decision it records is **issued but
not canonically adopted**. Adoption requires all five conditions: a genuinely
independent clean-room exact-head review of this package, a separate founder
Ready decision, a separate founder merge decision, merge into canonical `main`,
and mechanical post-merge verification.

```text
No subset adopts FD-B2A-9.
```

## Continuing separation

Even after canonical adoption:

```text
P01-04B2A:                          ACCEPTED
P01-04B as a whole:                 INCOMPLETE / NOT ACCEPTED
B2B:                                NOT AUTHORIZED
B2C:                                NOT AUTHORIZED
B2D:                                NOT AUTHORIZED
P01-04C through P01-04G:            NOT AUTHORIZED
Real Pilot-01 split:                NOT AUTHORIZED
P01-03G or real dataset access:     NOT AUTHORIZED
B0/B1 execution:                    NOT AUTHORIZED
Model access:                       NOT AUTHORIZED
Inference:                          NOT AUTHORIZED
Retrieval:                          NOT AUTHORIZED
Metrics or benchmark execution:     NOT AUTHORIZED
Training or fine-tuning:            NOT AUTHORIZED
Publication:                        NOT AUTHORIZED
Clinical use:                       NOT AUTHORIZED
```

B2A acceptance makes a later B2B authorization decision **eligible for
consideration**. It does not itself authorize B2B, and this package contains no
prospective B2B implementation authority.

## What this package does not do

It does not authorize B2B, accept P01-04B as a whole, execute the real Pilot-01
split, authorize B0 or B1 execution, authorize dataset or model access,
authorize inference, retrieval, metrics, benchmark execution, training or
fine-tuning, dispatch or rerun any workflow, modify implementation, tests,
workflows, dependencies or artifacts, modify any prior governance package, or
authorize a Ready transition or merge.
