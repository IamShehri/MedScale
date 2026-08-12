# MESC Pilot-01 — P01-04D Entry Authorization

This package records the founder decision that P01-04D may enter its controlled
pre-execution governance state.

```text
records an entry decision only
opens no protected input
creates no generation workspace
performs no real generation
authorizes no execution
```

## 1. How this point was reached

The founder-authorized P01-04D entry-readiness review returned **NOT READY** on
two blockers:

```text
B-1:
No controlled formal operator invocation path existed for Generation A and
Generation B.

B-2:
The P01-04A/E policy artifact inventory was not reconciled with the accepted
fixture-only implementation inventory.
```

That verdict is historical and preserved. It is not rewritten by this package.

B-1 and B-2 were then resolved in two stages. The remediation design closed both
at the design and contract level under `FD-DREADY-1` through `FD-DREADY-12`. The
formal executor implementation subsequently closed both at the implementation
level: the controlled operator surface now exists as repository-controlled code,
and the exact seven-file candidate inventory is enforced by the implementation
itself.

The formal executor was independently reviewed and canonically adopted, and its
adoption truth was then canonically reconciled so that canonical status text
matches canonical code.

An independent entry-readiness re-evaluation against canonical main returned:

```text
READY FOR FOUNDER P01-04D ENTRY DISPOSITION
```

with B-1 and B-2 closed at the implementation level, zero new blocking findings,
and `F1`, `F2` and `F3` closed.

On that basis the founder issued P01-04D entry authorization on **2026-08-05**.

## 2. What entry is, and what it is not

Entry moves P01-04D into a controlled pre-execution governance state. It is a
governance transition, not an operation over data.

```text
entry is not execution
entry opens no protected data
entry authorizes no Generation A
entry authorizes no Generation B
```

Entry does not permit a formal generation workspace to be created, and it does
not permit `generate` or `compare` to be invoked. A separate founder execution
authorization is required before any protected input may be opened or any
generation command may run.

No formal P01-04D artifact has been generated.

## 3. Package documents

- [`founder-authorization.md`](founder-authorization.md) — the controlling
  document: the exact founder entry decision and its prohibition boundary.
- [`entry-readiness-re-evaluation.md`](entry-readiness-re-evaluation.md) — the
  exact external re-evaluation result and its evidence.
- [`acceptance.md`](acceptance.md) — the acceptance criteria for this
  documentation gate.

## 4. Existing canonical adoption records

- [`../p01-04d-entry-readiness-remediation/canonical-adoption-record.md`](../p01-04d-entry-readiness-remediation/canonical-adoption-record.md)
  — remediation-design canonical adoption.
- [`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md)
  — formal-executor implementation canonical adoption.

## 5. Authority

This package amends no founder decision and alters no ratified scientific
decision. It does not change the seven-file candidate inventory, the
artifact-name supersession map, the P01-04D/E/F/G stage separation or the
ratified decisions D1 through D10. On any conflict, D1 through D10 control.
