# P01-04D External Execution-Evidence Harness — P-A1 Contract Package

Status: **contract and governance documentation only — no implementation, no
execution authorized**

This package records the XD-EXEC-1 external execution-evidence contract for MESC
Pilot-01 P01-04D. It defines what a future repository-controlled execution-evidence
harness must record, how it must record it, and what it must never record.

It contains no implementation. It authorizes no execution.

## 1. Package identity

```text
Package:
P-A1 — P01-04D EXTERNAL EXECUTION-EVIDENCE CONTRACT

Blocker:
XD-EXEC-1 — external execution-evidence recording

Blocker state:
DECIDED — CLOSED FOR P01-04D EXECUTION READINESS (§8E)

Selected architecture:
ARCHITECTURE A

Evidence model:
MODEL E2′

Package class:
DOCUMENTATION AND CONTRACT ONLY

Implementation clarification:
PIC-1 .. PIC-9 RECORDED

Implementation corrections:
PIC-CORR-1 .. PIC-CORR-15 RECORDED

P-A2 implementation:
NOT AUTHORIZED BY THIS PACKAGE

P01-04D execution:
NOT AUTHORIZED
```

## 2. Canonical baseline

```text
Canonical main:
035392831c6218b5302b04ca7e392eff8724ff52

Canonical tree:
ee409f9dbb57492514b384e2332487a923bf01f9

P-D governance mechanism:
CANONICALLY ADOPTED

MODEL A′:
CANONICAL GOVERNING ACTIVATION RULE

P01-04D entry:
AUTHORIZED

P01-04D control state:
ENTERED — PRE-EXECUTION GOVERNANCE ONLY
```

The P-A1 contract package was canonically adopted at that baseline. The
implementation clarification `PIC-1` .. `PIC-9` was recorded on top of it at:

```text
Canonical main:
ddd9766e7362a43e79cd8b0728b0eb0d00830441

Canonical tree:
bc3b1a1db5dbca3daf09c13f46631d290de0e692

Clarification class:
DOCUMENTATION CORRECTION ONLY

P-A2 implementation:
STILL NOT AUTHORIZED

XD-EXEC-1:
STILL DECIDED / OPEN
```

The implementation corrections `PIC-CORR-1` .. `PIC-CORR-6` were recorded on the
same clarification candidate, after an independent full-content review returned
`CHANGES REQUIRED`. They fix the exact `STAGE_REFUSED` / `STAGE_FAILED`
boundary, the deterministic `failure_class` → `root_cause_class` →
`remediation_disposition` mapping, the `CHILD_NONZERO_EXIT` derivation, the
post-failed-stage `finalize` progression, the historical scope of acceptance
criteria `A-1` and `A-2`, and several deterministic safety details.

The final implementation corrections `PIC-CORR-7` .. `PIC-CORR-13` were recorded
on the same candidate after a second independent full-content review again
returned `CHANGES REQUIRED`. They close the destination-unwritable case in which
an opened stage's journal bytes remain well formed but a required append can no
longer be durably written — the stage is then structurally unsealed, nothing is
fabricated, continuation stops, and terminal finalization selects
`EPISODE_EVIDENCE_CORRUPT`. They also fix the exact stderr logical-line
algorithm so LF and CRLF classify identically, the `CHILD_LAUNCH_FAILURE`
lifecycle, the separation of semantic derivation from durable destination, the
completeness of the controlling `CHILD_NONZERO_EXIT` table, the historical scope
of `PA1-FD-18`, and the literal canonical exception-module anchor.

The closing implementation corrections `PIC-CORR-14` and `PIC-CORR-15` were
recorded on the same candidate after a third independent full-content review
returned `CHANGES REQUIRED` on one blocking finding, `PIC-FFR1`: partial
terminal-manifest creation was undefined. `PIC-CORR-14` records one deterministic
three-state model for `episode-manifest.json` — `TM-0` absent, `TM-1` present but
invalid or incomplete, `TM-2` complete valid canonical — separates the physical
path state from manifest validity, ties terminal identity and the durable
terminal disposition to `TM-2` alone, preserves the exact bytes of a partial
manifest while prohibiting every retry, repair and overwrite, and closes the
crash-after-valid-write case as still sealed. `PIC-CORR-15` corrects wording that
could have been read as granting additional formal test imports;
`resolve_repository_commit` remains the sole formal test-scope import.

```text
Correction class:
DOCUMENTATION CORRECTION ONLY

New enumerations or enumeration values:
NONE

New evidence record class or manifest field:
NONE

New terminal-disposition value:
NONE

Recovery sidecar, repair marker or retry marker:
NONE

P-A2 implementation:
STILL NOT AUTHORIZED

XD-EXEC-1:
STILL DECIDED / OPEN
```

## 3. Documents in this package

| Document | Role |
|----------|------|
| [`founder-authorization.md`](founder-authorization.md) | **Controlling document.** Records the founder disposition `PA1-FD-1` .. `PA1-FD-20`, amendments `A1`–`A5`, reconciliations `R1`–`R5`, corrections `PA1-C1`–`PA1-C5`, implementation clarifications `PIC-1`–`PIC-9` with the associated deterministic implementation decisions, implementation corrections `PIC-CORR-1`–`PIC-CORR-6`, final implementation corrections `PIC-CORR-7`–`PIC-CORR-13`, and closing implementation corrections `PIC-CORR-14`–`PIC-CORR-15`. |
| [`evidence-contract.md`](evidence-contract.md) | The normative technical contract: architecture, obligations, inventory, schemas, lifecycle, closed vocabularies, serialization, path safety and minimization. |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for **this documentation package**, and the deferral of implementation acceptance to P-A2. |

On any conflict, `founder-authorization.md` controls, and the ratified
scientific decisions D1 through D10 control over everything in this package.

## 4. Why this package exists

The canonical P01-04 execution protocol requires every formal execution to
produce external evidence, stored outside the repository and outside the
evidence root, and referenced by stable identity only.

The adopted P01-04D formal operator does not produce that evidence. It reports a
compact completion summary and returns. Its `--external-evidence-root` argument
is used solely to refuse a generation workspace that is or lies inside that root;
the operator never writes there.

ARCHITECTURE A resolves this by wrapping the canonical operator in a separate
repository-controlled evidence harness rather than by changing the operator.

## 5. Architecture summary

```text
ARCHITECTURE A:
A separate repository-controlled evidence harness wraps the canonical operator
and invokes it as a separate child process.

MODEL E2′:
PER-STAGE APPEND-ONLY EVIDENCE
WITH WRITE-ONCE EPISODE CORE
AND WRITE-ONCE TERMINAL MANIFEST

Rejected as the current architecture:
shared cross-generation journal
single mutable execution JSON
```

The six adopted formal-executor implementation blobs remain byte-identical. The
exact seven-file deterministic P01-04D candidate bundle remains unchanged.
Runtime evidence remains scientifically non-authoritative and never enters a
generation workspace, `generation-manifest.json`, the authoritative split
fingerprint, the repository or the future evidence root.

## 6. Stage ownership summary

```text
P-A owns canonical required-reporting obligations:
1 through 10, and 13

P01-04F later owns:
11 — freeze timestamp
12 — evidence-root identity
```

Obligations 11 and 12 are **not** removed, weakened or satisfied here. P-A
defines only the stable-identity interface by which a future, separately
authorized P01-04F record may reference a sealed P01-04D execution episode.

```text
record-freeze command:
DOES NOT EXIST IN P-A

MODEL A′ activation-verification evidence:
OUT OF P-A SCOPE — INTERFACE STILL OPEN

P01-04F:
NOT AUTHORIZED BY THIS PACKAGE
```

## 7. Future harness command surface

```text
open
generate
compare
verify
invalidate
finalize

command count:
6
```

Defining these commands creates no authority to invoke any of them over real
inputs. Their implementation is P-A2, which required a separate founder
authorization; that authorization was issued and recorded in
`founder-authorization.md` §8E, and P-A2 was canonically adopted at `13add97d`.
Adoption of the implementation still confers no authority to invoke any command
over real inputs — that remains a separate founder execution authorization.

## 8. What this package is not

This package is not an implementation, not an execution authorization, not an
input-access authorization and not a P01-04F authorization. It creates no
generation workspace, opens no protected input, derives no partition membership,
produces no artifact and publishes nothing.

No document in this package asserts authorization for P01-04D execution.

## 9. Authority boundary

```text
P01-04D entry:
AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

XD-EXEC-1:
DECIDED — CLOSED FOR P01-04D EXECUTION READINESS
(founder-authorization.md §8E, at canonical main 13add97d)

XD-EXEC-2:
OPEN

XD-EXEC-3:
OPEN

XD-EXEC-4 governance mechanism:
CANONICALLY ADOPTED

P-A2 implementation:
AUTHORIZED AND CANONICALLY ADOPTED — PR #97, merge 13add97d

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```
