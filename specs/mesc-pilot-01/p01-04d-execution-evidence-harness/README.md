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
DECIDED / OPEN

Selected architecture:
ARCHITECTURE A

Evidence model:
MODEL E2′

Package class:
DOCUMENTATION AND CONTRACT ONLY

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

## 3. Documents in this package

| Document | Role |
|----------|------|
| [`founder-authorization.md`](founder-authorization.md) | **Controlling document.** Records the founder disposition `PA1-FD-1` .. `PA1-FD-20`, amendments `A1`–`A5`, reconciliations `R1`–`R5` and corrections `PA1-C1`–`PA1-C5`. |
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
inputs. Their implementation is P-A2, which requires a separate founder
authorization that has not been issued.

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
DECIDED / OPEN

XD-EXEC-2:
OPEN

XD-EXEC-3:
OPEN

XD-EXEC-4 governance mechanism:
CANONICALLY ADOPTED

P-A2 implementation:
NOT AUTHORIZED

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```
