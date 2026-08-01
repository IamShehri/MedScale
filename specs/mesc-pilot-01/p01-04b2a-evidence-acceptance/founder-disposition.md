# P01-04B2A Evidence Acceptance — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Decision:
ACCEPT — CANONICAL PORTABILITY EVIDENCE

FD-PV-19:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

FD-PV-18:
ACTIVATED AND CONSUMED

Evidence run:
30678040133 — COMPLETED / SUCCESS

Independent evidence review:
COMPLETED — APPROVE WITH NON-BLOCKING NOTES

Blocking findings:
NONE

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

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-01

Required canonical baseline:
`e3478da94e62ad9af5858a69e28de7e5d5fc04f4`

This document is controlling for this package. Prior governance history is
adopted at [`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/),
[`../p01-04b2a-final-review-hold/`](../p01-04b2a-final-review-hold/) and
[`../p01-04b2a-evidence-production-gate/`](../p01-04b2a-evidence-production-gate/)
and is not restated here.

---

## 1. Verified canonical baseline

```text
Merge SHA:
e3478da94e62ad9af5858a69e28de7e5d5fc04f4

Tree:
e64e57a1c6c94703a7f20ef6598256fa77600b31

Ordered parent 1:
69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3

Ordered parent 2:
626a23f01db978d43d51cdbae2c4378d2cf1733f

Subject:
docs(mesc): authorize B2A portability evidence production (#65)
```

```text
PR #65:
MERGED / CLOSED / NOT DRAFT

Merged head:
626a23f01db978d43d51cdbae2c4378d2cf1733f

Merged at:
2026-08-01T01:19:29Z

Scope:
2 commits / 5 files / +909 / -1
```

## 2. FD-PV-18 disposition

```text
FD-PV-18:
ACTIVATED AND CONSUMED

Authorized dispatch requests:
EXACTLY ONE — accepted 2026-08-01T01:30:04Z

Retry:
NOT AUTHORIZED

Rerun:
NOT AUTHORIZED

Second dispatch:
NOT AUTHORIZED

Replacement run:
NOT AUTHORIZED
```

All five `FD-PV-18` activation conditions were satisfied and mechanically
verified before the dispatch. The authority was consumed when GitHub accepted
the single request, and it is not revived by this disposition or by any later
decision.

Complete workflow history for `MESC B2A Portability` (workflow `323476626`):

```text
Total runs:                8
pull_request runs:         7   — infrastructure validation only, non-admissible
workflow_dispatch runs:    1   — run 30678040133, the sole authorized dispatch
Runs with run_attempt > 1: 0
```

## 3. FD-PV-19 — Canonical Portability Evidence Acceptance Disposition

```text
FD-PV-19 — Canonical Portability Evidence Acceptance Disposition

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-01

Decision:
ACCEPT

Accepted evidence:
The seven-artifact canonical portability evidence set produced by
MESC B2A Portability run 30678040133 against canonical main
e3478da94e62ad9af5858a69e28de7e5d5fc04f4.

Basis:
1. FD-PV-18 was validly activated.
2. Exactly one authorized dispatch was accepted.
3. FD-PV-18 was consumed.
4. Run 30678040133 completed successfully at attempt 1.
5. Six generation jobs and one aggregate job succeeded.
6. Exactly seven expected, non-expired artifacts were produced.
7. Mechanical verification passed.
8. NB3-A, NB3-B and NB3-C passed.
9. A genuinely independent clean-room evidence review found no blocking
   findings.
```

### Classification while this package is Draft or unmerged

```text
FD-PV-19:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN
```

Issuing a founder decision is not canonical adoption. Recording it in a Draft
pull request adopts nothing and changes no repository state.

### Adoption conditions — all five required

1. a genuinely independent clean-room exact-head review of **this governance
   package**;
2. a separate founder Ready decision for this package's pull request;
3. a separate founder merge decision for that pull request;
4. merge into canonical `main`;
5. mechanical post-merge verification of the resulting merge SHA, its ordered
   parents, its tree, its path scope, and the final canonical-main identity.

**No subset adopts `FD-PV-19`.** Draft creation adopts nothing. Review approval
alone, Ready alone, merge alone, review plus merge, and merge without mechanical
verification are each insufficient. Only after all five may the repository
classify the disposition as adopted.

## 4. Accepted independent evidence review

```text
Verdict:
APPROVE WITH NON-BLOCKING NOTES — CANONICAL PORTABILITY EVIDENCE
ELIGIBLE FOR A SEPARATE FOUNDER EVIDENCE-ACCEPTANCE DECISION

Blocking findings:
NONE
```

### Accepted non-blocking observations

```text
NB-01:
ZIP Unix permission metadata differs by producer:
0644 on Linux/macOS and 0666 on Windows.

Disposition:
NON-BLOCKING — archive metadata only; payload bytes, names, sizes,
serialization and cross-cell identities are unchanged.

NB-02:
Broad substring scans initially produced false positives from the key
"decomposed" and the ratified cell identifier "windows-py3.11".

Disposition:
NON-BLOCKING — methodology observation only; precise inspection found no
prohibited provenance or runtime content.
```

Neither observation authorizes or requires an evidence correction, a new
workflow run, a rerun, a replacement artifact, or any repository implementation
change. None is authorized and none is required.

## 5. What this disposition accepts

It accepts that the evidence set recorded in
[`evidence-ledger.md`](evidence-ledger.md) is a faithful, mechanically verified
record of deterministic six-cell canonical serialization at
`e3478da94e62ad9af5858a69e28de7e5d5fc04f4`.

```text
Canonical portability evidence:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED UNTIL THIS PACKAGE IS MERGED AND VERIFIED
```

## 6. What this disposition does not accept

```text
Evidence acceptance is not interchangeable with B2A acceptance.
```

```text
B2A acceptance:            NOT ACHIEVED
N-12:                      BINDING AND UNDISCHARGED
Windows/macOS obligations: OPEN
B2B:                       NOT AUTHORIZED
P01-04B:                   INCOMPLETE / NOT ACCEPTED
Real Pilot-01 split:       NOT AUTHORIZED
B0:                        NOT AUTHORIZED
Model access:              NOT AUTHORIZED
Real dataset access:       NOT AUTHORIZED
Inference/retrieval:       NOT AUTHORIZED
Training/fine-tuning:      NOT AUTHORIZED
```

`FD-PV-19` does not authorize, before or after adoption: a B2A acceptance
decision; discharge of binding `N-12`; closure of the Windows or macOS
obligations; B2B authorization; P01-04B acceptance; any workflow dispatch,
rerun, cancellation or replacement run; editing or deleting any artifact;
downloading, recommitting, publishing or mirroring evidence bytes; a second
commit on this governance package; amendment, rebase, squash, reset,
cherry-pick, or force-push; any path outside those named in
[`acceptance.md`](acceptance.md); marking this package's pull request Ready;
merging it; auto-merge; the real Pilot-01 split; B0; model or real-dataset
access; inference, retrieval, training or fine-tuning; publication; clinical
use; or deleting any branch.

## 7. Artifact durability

The seven artifacts were non-expired at inspection and at the completed
independent review. Their later expiry under the GitHub retention window does
**not** retroactively invalidate the recorded review, the recorded digests, or
this disposition. The ledger in [`evidence-ledger.md`](evidence-ledger.md) is
the durable governance record of what was produced and verified.

## 8. Standing status

Nothing in this disposition accepts B2A, discharges `N-12`, closes the Windows
or macOS obligations, authorizes B2B, or completes P01-04B. P01-04B remains
incomplete and not accepted.
