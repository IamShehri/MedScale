# P01-04B2A Cross-Platform Portability Validation Infrastructure Gate

```text
Status:
FOUNDER-RATIFIED CONTRACTS — ADOPTED ON CANONICAL MAIN;
IMPLEMENTATION NOT AUTHORIZED

Infrastructure implementation:
NOT AUTHORIZED

B2A implementation:
ADOPTED THROUGH PR #59; NOT AUTHORIZED HERE

Execution:
NOT AUTHORIZED

Evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED
```

Canonical planning baseline:
`0884971f68619be8f25c3b905a3dcad7c5212101`

Canonical adoption:
`30f79b183a4fff6a08e30e1e43f5da549ce20c1a`

Adoption PR:
`#57 — MERGED`

Final merged PR head:
`b76420913c80bd54fd31e63ccffd5ed43a36a854`

Founder-ratified reviewed head:
`c555144b480b2334aeaaab0864cad59efe0a1e46`

Merged at:
`2026-07-27T02:53:00Z`

Source branch:
`docs/mesc-p01-04b2a-portability-gate` — deleted after verified post-merge cleanup.

Post-merge verification:
- CI `30233225446` — success
- CodeQL `30233225421` — success
- Optional Extras / Backends `30233225422` — success

Founder ratification:
`FD-PV-1` through `FD-PV-10` ratified on 2026-07-27; see
`founder-ratification.md`.

Adoption freezes and records `FD-PV-1` through `FD-PV-10`.

Adoption does not authorize infrastructure implementation.

No portability workflow was created.

No six-cell matrix was executed.

No portability evidence was produced.

B2A remains not accepted.

B2B remains not authorized.

P01-04B remains incomplete and not accepted.

---
## Purpose

This package designs a future, separately authorized cross-platform
portability-validation infrastructure for P01-04B2A. It exists so the founder
could decide the infrastructure contracts **before** any workflow file, test
file, or B2A implementation file is written. Those contracts were ratified on
2026-07-27 as `FD-PV-1` through `FD-PV-10`; implementation remains unauthorized.

This package designs infrastructure. It does not build it, run it, or produce
evidence with it.

The canonical B2A artifact implementation was adopted through PR #59.

Portability-infrastructure implementation remains unauthorized.

Portability evidence remains unauthorized and unproduced.

Windows and macOS evidence remain open.

## Binding relationship to FD-B2A-8 and N-12

FD-B2A-8 was founder-ratified on 2026-07-26 (adoption PR #55, canonical merge
`5c083a0c5f23d0f9837e7543c444633a68524e67`) and requires deterministic
golden-vector byte and hash identity across Linux, Windows and macOS, and across
Python 3.11 and Python 3.12 where supported by the authorized validation
infrastructure.

Binding N-12 makes the consequence explicit:

- Linux evidence on Python 3.11 and 3.12 is **partial evidence only**;
- B2A **cannot be accepted** while Windows and macOS evidence remains open;
- validation-infrastructure or workflow changes require **separate founder
  authorization**;
- B2B remains blocked until B2A acceptance;
- no artifact may be promoted on a claim of completed cross-platform
  determinism.

This package is the design gate for the infrastructure N-12 requires. It does
not discharge N-12, and it does not weaken it.

## Current CI limitation

The repository's general workflow `.github/workflows/ci.yml` runs only:

- runner `ubuntu-latest`;
- Python 3.11;
- Python 3.12.

There is therefore **no Windows or macOS byte-identity evidence in this
repository today**, and none is produced by this package. That obligation
remains open.

## Four distinct things, none authorized here

| Activity | Meaning | Status |
|---|---|---|
| **B2A implementation** | Writing the private canonical-serialization and artifact-identity modules and their tests, in the four already-ratified paths | **ADOPTED THROUGH PR #59; NOT AUTHORIZED BY THIS PORTABILITY PACKAGE** |
| **Validation-infrastructure implementation** | Writing the portability workflow and its helper/test modules in the three paths proposed here | **NOT AUTHORIZED** |
| **Portability evidence production** | Actually running the six-cell matrix and generating comparison evidence | **NOT AUTHORIZED** |
| **B2A acceptance** | Declaring B2A accepted, which unblocks B2B consideration | **NOT ACHIEVED** |

Each is a separate founder act. None is granted by this documentation package,
and none is granted by merging it.

## This package does not alter the B2A contracts

FD-B2A-1 through FD-B2A-8 and the canonical record at
`../p01-04b2a/founder-ratification.md` are unchanged by this package. The
canonical value domain, canonical JSON and JSONL rules, artifact descriptors,
the non-circular fingerprint model, the split-summary identity core, and the
fail-closed error taxonomy are all untouched.

The proposed `portability-evidence.json` envelope is a **validation record
only**. It never enters `split_fingerprint`, never becomes a promoted B2A
artifact, and never alters the four required split artifact roles
(`group_registry`, `example_registry`, `split_summary`, `excluded_ledger`).

## B2A may later be merged as implemented but not accepted

This package deliberately does **not** claim that portability infrastructure
must exist before B2A code exists. The proposed order is the reverse:

1. the infrastructure design is frozen first (this gate);
2. B2A code may later be implemented under its own separate authorization and
   merged in a state recorded explicitly as `IMPLEMENTED BUT NOT ACCEPTED`;
3. the portability workflow is implemented afterwards, on a canonical main that
   already contains the private B2A implementation it must exercise;
4. cross-platform evidence is required **before acceptance**, not before code
   authorship.

Merging B2A code does not accept B2A. Acceptance is a later, separate act.

## B2B remains blocked

B2B authorization may be considered only after a separate founder/ChatGPT B2A
acceptance decision, which itself requires canonical-main cross-platform
evidence and independent review. A passing workflow does not by itself accept
B2A and does not unblock B2B.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document: purpose, authority relationship, boundaries |
| `spec.md` | Proposed infrastructure contract: paths, matrix, evidence, aggregation, security |
| `decision-record.md` | PD-PV-1 through PD-PV-10, adopted as FD-PV-1 through FD-PV-10 |
| `founder-ratification.md` | Canonical founder record of FD-PV-1 through FD-PV-10 and the FD-PV-6 numeric limits |
| `plan.md` | The full controlled sequence and its prohibitions |
| `acceptance.md` | Documentation-gate, future-infrastructure, and future-B2A-acceptance criteria |
| `implementation-task.md` | Future builder brief; not executable without separate authorization |
