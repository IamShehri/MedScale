# P01-04D Entry Authorization — Founder Decision

This is the controlling document of the P01-04D entry-authorization package.

## 1. Decision

```text
Decision:
P01-04D ENTRY AUTHORIZED

Decision date:
2026-08-05

Decision class:
ENTRY / PRE-EXECUTION GOVERNANCE ONLY

Canonical decision baseline:
9229fea8c208021d3bbdb3767e71c3e3f790262e

Entry-readiness re-evaluation:
READY FOR FOUNDER P01-04D ENTRY DISPOSITION

P01-04D control state:
ENTERED — PRE-EXECUTION GOVERNANCE ONLY

P01-04D execution:
NOT AUTHORIZED
```

## 2. Basis of the decision

```text
Original entry-readiness verdict:
NOT READY — HISTORICAL AND PRESERVED

B-1 implementation-level status:
CLOSED

B-2 implementation-level status:
CLOSED

New blocking findings:
0

Formal executor findings:
F1 CLOSED
F2 CLOSED
F3 CLOSED

Formal operator implementation code:
CANONICALLY ADOPTED

Formal-executor adoption truth:
CANONICALLY RECONCILED
```

The evidence supporting each line is recorded in
[`entry-readiness-re-evaluation.md`](entry-readiness-re-evaluation.md). That
record reports a readiness disposition. It does not itself grant entry. Entry is
granted by this document.

## 3. What this decision means

P01-04D may enter its controlled pre-execution governance state. The phase may
be planned, and a future execution-authorization request may be prepared and
reviewed.

```text
Entry authorization is not execution authorization.

Entry authorization does not grant access to any input.

Entry authorization does not permit a formal generation workspace to be
created.

Entry authorization does not permit `generate` or `compare` to be invoked.

A separate founder execution authorization is required before any protected
input may be opened or any generation command may run.
```

## 4. Prohibition boundary

Every line below remains in force after this decision.

```text
P01-03G registry access:
NOT AUTHORIZED

external source-record access:
NOT AUTHORIZED

real dataset access:
NOT AUTHORIZED

Generation A:
NOT AUTHORIZED

Generation B:
NOT AUTHORIZED

real split generation:
NOT AUTHORIZED

real partition membership:
NOT AUTHORIZED

canonical leakage execution:
NOT AUTHORIZED

evidence publication:
NOT AUTHORIZED

model execution:
NOT AUTHORIZED

training:
NOT AUTHORIZED

fine-tuning:
NOT AUTHORIZED

P01-04E through P01-04G execution:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

## 5. Scope and non-authority

```text
records an entry decision only
creates no execution authority
grants no input access
creates no generation workspace
generates no artifact
creates no partition membership
executes no leakage analysis
publishes nothing
unlocks no later stage
```

This decision amends no earlier founder decision. It does not alter
`FD-DREADY-1` through `FD-DREADY-12`, the formal operator contract, the
seven-file candidate artifact inventory, the artifact-name supersession map, the
P01-04D/E/F/G stage separation or the ratified scientific decisions D1 through
D10. On any conflict, D1 through D10 control.
