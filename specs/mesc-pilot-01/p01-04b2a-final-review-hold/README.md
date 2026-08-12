# P01-04B2A Final Review Hold

```text
Status:
FINAL REVIEW HOLD RECORDED — DISPOSITION ISSUED

Accepted verdict on PR #61:
GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT

FD-PV-17:
RECORDED BUT NOT ACTIVE

Activation:
OPERATIVE ONLY AFTER ALL FIVE FD-PV-17 ACTIVATION CONDITIONS ARE SATISFIED

PR #61:
OPEN / DRAFT / NOT MERGED — HELD

Infrastructure adoption:
NOT ACHIEVED

Admissible evidence production:
NOT AUTHORIZED

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
`02d0aafb61fa62de414c0e8e5d61187c03b650bd`

Governed pull request:
`PR #61` — exact head `f68f8be8799c0ec67b26c319a4a06789f2ea1a7e`, exact tree
`1caa8f9ae4031ff17ddcd33ffc0a32a4e7cc855e`, 8 commits, 3 files, +3829 / −0

---

## Purpose

This package records the final independent exact-head review verdict on PR #61
and prospectively authorizes exactly one ninth correction commit. It implements
no correction.

Prior governance history — the authority-record disposition, the canonical-main
incident, the preventive controls, and `FD-PV-16` — is adopted at
[`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/) and is **not**
restated here.

## What holds PR #61

| Finding | Substance |
|---|---|
| **F1** | Large unexpected-artifact responses can bypass the guard: `comm … \| grep -q .` under `pipefail` yields status 141 when `grep` exits early, so the `if` reads false |
| **F2** | B2 tests supply pre-rendered TSV and never exercise the real `--paginate` / `--jq` `.artifacts[]` projection |
| **F3** | Dispatch tests cover one of two guard copies and do not prove malformed-SHA rejection precedes `git rev-parse HEAD` |
| **F4** | Archive-cardinality behaviour is asserted structurally only, with no real execution for valid or invalid counts |

Two taxonomy mappings were **accepted** by the review and are settled:

```text
expired expected artifact:              missing_matrix_cell
post-validation archive-count mismatch: aggregate_verifier_internal_error
```

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-disposition.md`](founder-disposition.md) | **Controlling**: accepted verdict, F1–F4, settled mappings, `FD-PV-17` and its five-condition gate, and the authorized body correction |
| [`implementation-task.md`](implementation-task.md) | Prospective correction brief — not executable |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for this gate and for the future commit 9 |

On any conflict, [`founder-disposition.md`](founder-disposition.md) controls.

## Three states

**Current — while this package is Draft.** Nothing is activated. No PR #61
mutation, no ninth commit, no branch update, no body change, no rerun, no
dispatch, no Ready, no merge, no evidence.

**After the complete five-condition gate.** `FD-PV-17` authorizes exactly one
additive ninth commit on PR #61, its normal non-force push, the workflows that
push triggers, a metadata-only PR #61 body correction, and commissioning a new
independent exact-head review.

**Always.** Ready and merge for either pull request remain separate founder
acts, available only after a successful independent review of the relevant exact
head.

## Relationship to adopted decisions

`FD-PV-1` through `FD-PV-16`, `FD-B2A-1` through `FD-B2A-8`, binding `N-12`,
`D1`–`D10`, and `FD-B2-1` through `FD-B2-8` are **unamended**. The four
`FD-PV-6` values and their axes, the `FD-PV-13` permission boundary, the
`FD-PV-14` canonical-SHA rules, the exact implementation paths, and the
twenty-one-category taxonomy are unchanged. `FD-PV-17` adds a new, narrowly
bounded correction authority and amends nothing.

## What this package does not do

It does not correct any finding, adopt the infrastructure, execute any workflow,
produce or accept admissible evidence, accept B2A, discharge binding `N-12`,
close the Windows or macOS obligations, authorize B2B, execute the real split,
run B0, train any model, change any repository setting, or authorize a Ready
transition or merge for either pull request.
