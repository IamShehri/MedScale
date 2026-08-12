# P01-04B2A Evidence Production Gate

```text
Status:
EVIDENCE-PRODUCTION AUTHORIZATION GATE RECORDED — DISPOSITION ISSUED

PR #61:
MERGED / CLOSED — 69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3

Infrastructure adoption:
ACHIEVED ON CANONICAL MAIN

FD-PV-17:
ACTIVATED AND CONSUMED

FD-PV-18:
RECORDED BUT NOT ACTIVE

Activation:
OPERATIVE ONLY AFTER ALL FIVE FD-PV-18 ACTIVATION CONDITIONS ARE SATISFIED

Admissible evidence production:
NOT YET AUTHORIZED

Admissible evidence:
NOT PRODUCED

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
`69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3`

Adopted infrastructure:
`PR #61` — merge `69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3`, tree
`ebbb61b905bde4773d48b40b9f667ceb0d558566`, merged head
`7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae`, 9 commits, 3 files, +4411 / -0

---

## Purpose

This package records the verified post-merge truth of PR #61 and prospectively
authorizes exactly **one** canonical-main portability evidence-production
workflow dispatch. It dispatches nothing and produces no evidence.

Prior governance history — the authority-record disposition, the canonical-main
incident, the preventive controls, `FD-PV-16`, and the final review hold with
`FD-PV-17` — is adopted at
[`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/) and
[`../p01-04b2a-final-review-hold/`](../p01-04b2a-final-review-hold/) and is
**not** restated here.

## What changed

The four blocking findings that held PR #61 are closed, reviewed, and adopted:

| Finding | Disposition |
|---|---|
| **F1** | Both artifact-set comparisons materialize their output and test it with `[ -s ]`; no guard depends on a `SIGPIPE`-prone pipeline |
| **F2** | The `gh` stub serves raw artifact API JSON and fails closed unless the workflow passes `--paginate` and the exact `--jq` projection |
| **F3** | Both dispatch-guard bodies are proven byte-identical, then the shared body is executed against a strict git stub that permits only `rev-parse HEAD` |
| **F4** | The real archive-cardinality step executes for 6, 5, 7, 0 and 12 archives with the exact category asserted for every invalid count |

The independent clean-room exact-head review of
`7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae` returned
`APPROVE WITH NON-BLOCKING NOTES` with **no blocking findings**. Its nine
non-blocking notes neither authorize nor require a tenth commit; none was
created.

The two settled taxonomy mappings are unchanged and remain unchangeable:

```text
expired expected artifact:              missing_matrix_cell
post-validation archive-count mismatch: aggregate_verifier_internal_error
```

The taxonomy remains exactly twenty-one categories.

## What is still missing

Adoption of the infrastructure is **not** portability evidence. Every run so far
was a `pull_request` infrastructure-validation run on the feature branch. None
produced an evidence envelope artifact, and none executed against canonical
`main`. Binding `N-12` therefore remains undischarged and the Windows and macOS
obligations remain open.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-disposition.md`](founder-disposition.md) | **Controlling**: verified post-merge truth, `FD-PV-18` and its five-condition gate, the exact one-dispatch authority, and the acts that remain separate |
| [`implementation-task.md`](implementation-task.md) | Prospective dispatch and verification brief — not executable |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for this gate and for the future evidence run |

On any conflict, [`founder-disposition.md`](founder-disposition.md) controls.

## Three states

**Current — while this package is Draft.** Nothing is activated. No dispatch, no
rerun, no evidence production, no artifact download as evidence, no acceptance,
no `N-12` disposition, no platform closure, no B2B.

**After the complete five-condition gate.** `FD-PV-18` authorizes exactly one
`workflow_dispatch` request against `.github/workflows/mesc-b2a-portability.yml`
on `main`, with `expected_sha` equal to the mechanically verified canonical-main
SHA produced by merging this package, plus read-only inspection and offline
verification of that one run's seven artifacts.

**Always.** Successful evidence production does not itself accept B2A. Mechanical
verification, a genuinely independent clean-room evidence review, and a separate
founder evidence-acceptance decision each remain required, in that order.

## Relationship to adopted decisions

`FD-PV-1` through `FD-PV-17`, `FD-B2A-1` through `FD-B2A-8`, binding `N-12`,
`D1`–`D10`, and `FD-B2-1` through `FD-B2-8` are **unamended**. The four
`FD-PV-6` values and their axes, the `FD-PV-13` permission boundary, the
`FD-PV-14` canonical-SHA rules, the adopted implementation paths, and the
twenty-one-category taxonomy are unchanged. `FD-PV-18` adds a new, narrowly
bounded evidence-production authority and amends nothing.

## What this package does not do

It does not dispatch any workflow, rerun any check, produce or download
admissible evidence, treat any existing pull-request artifact as satisfying the
canonical-main obligation, accept B2A, discharge binding `N-12`, close the
Windows or macOS obligations, authorize B2B, complete P01-04B acceptance,
execute the real Pilot-01 split, run B0, access model weights or the real
dataset, run inference, retrieval, training or fine-tuning, change any
repository setting, or authorize a Ready transition or merge.
