# P01-04B2A Acceptance — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Decision:
ACCEPT P01-04B2A IMPLEMENTATION

FD-B2A-9:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

N-12:
FOUNDER DISCHARGE DECISION ISSUED

Windows portability obligation:
FOUNDER CLOSURE DECISION ISSUED

macOS portability obligation:
FOUNDER CLOSURE DECISION ISSUED

P01-04B as a whole:
INCOMPLETE / NOT ACCEPTED

B2B:
NOT AUTHORIZED
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-01

Required canonical baseline:
`1f2d9152281f3136d212dcf7729063f7b1c64ad1`

This document is controlling for this package. Prior governance history is
adopted at [`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/),
[`../p01-04b2a-final-review-hold/`](../p01-04b2a-final-review-hold/),
[`../p01-04b2a-evidence-production-gate/`](../p01-04b2a-evidence-production-gate/)
and
[`../p01-04b2a-evidence-acceptance/`](../p01-04b2a-evidence-acceptance/)
and is not restated here.

---

## 1. FD-B2A-9 — P01-04B2A Implementation Acceptance Disposition

```text
FD-B2A-9 — P01-04B2A Implementation Acceptance Disposition

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-01

Decision:
ACCEPT P01-04B2A IMPLEMENTATION

Accepted implementation:
The private deterministic P01-04B2A canonical-artifact and canonical-
serialization implementation introduced through PR #59 and canonically merged
as 5736b1171f1aa467105d931713f5749fb81acd5b, under the ratified FD-B2A-1
through FD-B2A-8 contracts.

Accepted portability basis:
The seven-artifact canonical portability evidence produced by run 30678040133,
independently reviewed, founder-accepted through FD-PV-19, and canonically
adopted at 1f2d9152281f3136d212dcf7729063f7b1c64ad1.

N-12 disposition:
SATISFIED AND DISCHARGED FOR P01-04B2A

Windows portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A

macOS portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A

P01-04B2A:
ACCEPTED
```

## 2. Exact implementation accepted

```text
Contract authority:
PR #55 — docs(mesc): define P01-04B2A authorization gate
MERGED / CLOSED / NOT DRAFT
canonical merge 5c083a0c5f23d0f9837e7543c444633a68524e67
founder-ratification head edc09743a1aa9478c2accbe9debb8fcc5bcbe268
FD-B2A-1 through FD-B2A-8 ratified 2026-07-26

Implementation:
PR #59 — feat(mesc): implement B2A canonical artifact contracts
MERGED / CLOSED / NOT DRAFT
canonical merge 5736b1171f1aa467105d931713f5749fb81acd5b
merged head 7307fcf9085d3d15114984731b49d484523f09eb
reviewed tree 575fcf124792cd38b546a58a6845ad2ecd317281
2 commits / 4 files / +2559 / -0
```

Exactly four paths:

```text
src/medscale/mesc/_canonical_json_v1.py       +183
src/medscale/mesc/_split_artifacts_v1.py      +490
tests/test_mesc_canonical_json_v1.py          +792
tests/test_mesc_split_artifacts_v1.py        +1094
```

The acceptance is bounded to this exact implementation identity. It does not
extend to any later or unmerged implementation, to any public surface, or to any
execution entry point — none of which exists in this increment.

## 3. Exact evidence basis

```text
Portability infrastructure:
PR #61 — canonical merge 69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3
reviewed head 7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae
independently reviewed and adopted BEFORE the evidence-production authority
was activated

Evidence-production authority:
FD-PV-18 — activated, exercised exactly once, and CONSUMED

Evidence run:
MESC B2A Portability (workflow 323476626)
run 30678040133, run number 8, event workflow_dispatch, run_attempt 1,
head_branch main, evidence canonical SHA
e3478da94e62ad9af5858a69e28de7e5d5fc04f4, completed / success

Run history:
8 total — 7 pull_request, 1 workflow_dispatch, 0 reruns

Topology:
6 generation jobs and 1 aggregate job, all success

Artifacts:
7 total — 6 cell artifacts and 1 evidence artifact;
0 duplicates, 0 missing, 0 unexpected, 0 expired at inspection and at
independent review

Payload identities, byte-identical across all six cells:
canonical.json   228 bytes
canonical.jsonl   79 bytes
manifest.json    308 bytes

Verification:
cross-cell byte identity PASSED ACROSS ALL SIX CELLS;
NB3-A PASS; NB3-B PASS; NB3-C PASS; content boundary PASS

Independent evidence review:
APPROVE WITH NON-BLOCKING NOTES — CANONICAL PORTABILITY EVIDENCE
ELIGIBLE FOR A SEPARATE FOUNDER EVIDENCE-ACCEPTANCE DECISION
Blocking findings: NONE

FD-PV-19:
ACCEPT — CANONICAL PORTABILITY EVIDENCE
ADOPTED ON CANONICAL MAIN
ADOPTED_SHA 1f2d9152281f3136d212dcf7729063f7b1c64ad1
```

The complete ledger is adopted by reference at
[`../p01-04b2a-evidence-acceptance/evidence-ledger.md`](../p01-04b2a-evidence-acceptance/evidence-ledger.md).

## 4. Accepted non-blocking observations

Carried forward accurately. None was corrected, and none is upgraded into
accepted public behaviour or used to expand scope.

### Implementation observations

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

### Evidence observations

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

No new evidence correction, workflow run, rerun or replacement artifact is
required or authorized.

## 5. N-12 discharge decision

The ratified `N-12` sequencing decision is reproduced and mapped to evidence in
[`decision-basis.md`](decision-basis.md). Every prerequisite is satisfied.

```text
N-12:
SATISFIED AND DISCHARGED FOR P01-04B2A
```

The discharge is scoped to P01-04B2A. `N-12` is a portability-evidence
sequencing obligation; it is not reinterpreted as requiring model execution,
real-data execution, split execution, retrieval, training or benchmark results,
and its discharge grants none of those.

## 6. Windows and macOS closure decisions

```text
Windows portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A

macOS portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A
```

Basis: the `windows-py3.11`, `windows-py3.12`, `macos-py3.11` and
`macos-py3.12` cells of run `30678040133` each succeeded and each produced
`canonical.json`, `canonical.jsonl` and `manifest.json` byte-identical and
hash-identical to the Linux cells.

Both closures are scoped to P01-04B2A. Any later increment carrying its own
platform obligation must satisfy it on its own evidence.

## 7. Adoption conditions — all five required

1. a genuinely independent clean-room exact-head review of **this package**;
2. a separate founder Ready decision;
3. a separate founder merge decision;
4. merge into canonical `main`;
5. mechanical post-merge verification of the resulting merge SHA, tree, ordered
   parents, path scope and final `main` identity.

```text
No subset adopts FD-B2A-9.
```

Draft creation adopts nothing. Review approval alone, Ready alone, merge alone,
review plus merge, and merge without mechanical verification are each
insufficient.

## 8. Classification before canonical adoption

While this package is Draft, Ready-but-unmerged, or merged-but-not-mechanically-
verified:

```text
FD-B2A-9:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2A acceptance:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

N-12:
FOUNDER DISCHARGE DECISION ISSUED;
CANONICALLY BINDING UNTIL THIS PACKAGE IS ADOPTED

Windows portability obligation:
FOUNDER CLOSURE DECISION ISSUED;
CANONICALLY OPEN UNTIL THIS PACKAGE IS ADOPTED

macOS portability obligation:
FOUNDER CLOSURE DECISION ISSUED;
CANONICALLY OPEN UNTIL THIS PACKAGE IS ADOPTED
```

B2A is **not** canonically accepted merely because this decision appears in a
branch or a Draft pull request.

## 9. Classification after canonical adoption

Only after all five adoption conditions pass:

```text
FD-B2A-9:
ADOPTED ON CANONICAL MAIN

P01-04B2A:
ACCEPTED

N-12:
SATISFIED AND DISCHARGED FOR P01-04B2A

Windows portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A

macOS portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A
```

## 10. Continuing downstream separation

Even after canonical adoption:

```text
P01-04B as a whole:              INCOMPLETE / NOT ACCEPTED
B2B:                             NOT AUTHORIZED
B2C:                             NOT AUTHORIZED
B2D:                             NOT AUTHORIZED
P01-04C through P01-04G:         NOT AUTHORIZED
Real Pilot-01 split:             NOT AUTHORIZED
P01-03G or real dataset access:  NOT AUTHORIZED
B0/B1 execution:                 NOT AUTHORIZED
Model access:                    NOT AUTHORIZED
Inference:                       NOT AUTHORIZED
Retrieval:                       NOT AUTHORIZED
Metrics or benchmark execution:  NOT AUTHORIZED
Training or fine-tuning:         NOT AUTHORIZED
Publication:                     NOT AUTHORIZED
Clinical use:                    NOT AUTHORIZED
```

B2A acceptance makes a later B2B authorization decision **eligible for
consideration**. It does not itself authorize B2B. This disposition contains no
prospective B2B implementation authority.

`FD-B2A-9` does not authorize, before or after adoption: B2B, B2C or B2D; any
P01-04C through P01-04G work; P01-04B whole-phase acceptance; the real Pilot-01
split; B0 or B1 execution; model or real-dataset access; inference, retrieval,
metrics, benchmark execution, training or fine-tuning; any workflow dispatch,
rerun or cancellation; any artifact mutation, download or republication;
modification of any prior governance package; any implementation, test, workflow
or dependency change; a second commit on this package; amendment, rebase,
squash, reset, cherry-pick or force-push; marking this package's pull request
Ready; merging it; auto-merge; publication; clinical use; or deleting any
branch.

## 11. Standing status

P01-04B remains incomplete and not accepted. B2B remains unauthorized. No
execution authority of any kind is created by this disposition.
