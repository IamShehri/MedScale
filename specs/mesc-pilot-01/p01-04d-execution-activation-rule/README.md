# MESC Pilot-01 — P01-04D Execution-Authorization Activation Rule

This package records one founder decision: the activation rule that a future
P01-04D execution-authorization package must follow.

```text
records an activation-governance decision only
opens no protected input
creates no generation workspace
performs no generation
authorizes no execution
drafts no execution authorization
```

## 1. How this point was reached

The founder-authorized P01-04D execution-authorization readiness re-evaluation
was rerun against canonical main and returned:

```text
NOT READY FOR FOUNDER P01-04D EXECUTION-AUTHORIZATION DISPOSITION
```

It identified four execution-readiness blockers:

```text
XD-EXEC-1   external execution-evidence recording
XD-EXEC-2   external source-record custody and binding
XD-EXEC-3   independently recorded formal input identities
XD-EXEC-4   execution-authorization activation baseline
```

The founder issued a disposition for each. This package encodes the XD-EXEC-4
disposition and nothing else. It does not encode, satisfy or close XD-EXEC-1,
XD-EXEC-2 or XD-EXEC-3.

## 2. The defect XD-EXEC-4 resolves

The adopted formal operator requires an exact expected canonical commit and
verifies the repository checkout against it twice: once when the request is
constructed, and again immediately before the first filesystem mutation.

A future execution-authorization package, once canonically adopted, itself moves
canonical main. The authorization therefore cannot name the commit that its own
adoption will produce.

Two apparent remedies both fail:

```text
naming a pre-adoption commit
->
leaves the execution checkout behind canonical main

adding a second canonical commit to record the resolved identity
->
moves canonical main again and reproduces the same problem one step later
```

That is the execution-authorization activation self-reference defect.

## 3. The decided rule

```text
XD-EXEC-4:
MODEL A′ — CANONICAL POST-ADOPTION ACTIVATION RULE
```

The accepted mechanism is exactly:

```text
CANONICAL AUTHORIZATION RULE
->
CANONICAL AUTHORIZATION ADOPTION
->
READ-ONLY POST-MERGE ACTIVATION VERIFICATION
->
VERIFIED MERGE COMMIT BECOMES --expected-canonical-commit
```

No additional canonical commit follows merely to bind that identity.

The authorization package defines the rule against its reviewed pre-adoption
baseline and its exact candidate tree. It never predicts, fabricates, reserves or
embeds the merge identity its own adoption will produce. After adoption, one
read-only verification resolves the actual merge commit and proves every
activation prerequisite. Only a passing verification supplies the exact value of
`--expected-canonical-commit`.

[`founder-authorization.md`](founder-authorization.md) is the controlling record
of the rule and states it in full.

## 4. What this package does not do

```text
P01-04D execution:
NOT AUTHORIZED

execution-authorization drafting:
NOT AUTHORIZED

P01-03G content access:
NOT AUTHORIZED

external source-record access:
NOT AUTHORIZED

real dataset access:
NOT AUTHORIZED

Generation A:
NOT AUTHORIZED

Generation B:
NOT AUTHORIZED

compare:
NOT AUTHORIZED

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

MODEL A′ is an activation mechanism. Recording it moves no blocker other than
XD-EXEC-4, and it moves that one only at the governance-mechanism level.

## 5. Package documents

- [`founder-authorization.md`](founder-authorization.md) — the controlling
  document: the exact founder XD-EXEC-4 decision, the activation rule, the
  canonical-main-movement rule and the prohibition boundary.
- [`acceptance.md`](acceptance.md) — the acceptance criteria for this
  documentation gate.

This package deliberately contains no canonical-adoption record. Adoption
identity does not exist before merge, and a candidate cannot carry the identity
of its own adoption. That is the same constraint MODEL A′ exists to govern.

## 6. Related canonical records

- [`../p01-04/execution-protocol.md`](../p01-04/execution-protocol.md) — the
  execution-safety protocol, including the stop condition for canonical-main
  movement.
- [`../p01-04d-entry-authorization/founder-authorization.md`](../p01-04d-entry-authorization/founder-authorization.md)
  — the founder P01-04D entry decision.
- [`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md)
  — formal-executor implementation canonical adoption.
- [`../p01-04d-entry-readiness-remediation/founder-authorization.md`](../p01-04d-entry-readiness-remediation/founder-authorization.md)
  — `FD-DREADY-1` through `FD-DREADY-12`.

## 7. Authority

This package amends no founder decision and alters no ratified scientific
decision. It does not change the seven-file candidate inventory, the
artifact-name supersession map, the P01-04D/E/F/G stage separation or the
ratified decisions D1 through D10. On any conflict, D1 through D10 control, and
[`founder-authorization.md`](founder-authorization.md) controls this package.
