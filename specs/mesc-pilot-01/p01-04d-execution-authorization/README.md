# MESC Pilot-01 — P01-04D Execution Authorization

This package records the separate founder execution authorization required
before P01-04D execution may begin. It is conditional: it becomes active only
after the required `MODEL A′` read-only post-merge activation verification
returns PASS against the actual canonical merge of this package and the exact
canonically bound execution-input-manifest identity.

```text
records an execution-authorization decision only
opens no protected input
creates no generation workspace
performs no real generation
authorizes nothing until MODEL A′ PASS
```

## 1. How this point was reached

All execution-readiness blockers are closed:

```text
XD-EXEC-1   external execution-evidence recording
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-2   external source-record custody and binding
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-3   independently recorded formal input identities
CLOSED FOR P01-04D EXECUTION READINESS
```

The P-C1a contract and the P-C1b implementation are canonically adopted, the
formal executor and the P-A2 evidence harness are canonically adopted, P01-04D
entry is authorized, and the `MODEL A′` activation rule is canonically adopted.

The canonically recorded P-C1b verification established the exact
execution-input-manifest identity this package binds:

```text
execution-input-manifest SHA-256:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939

execution-input-manifest byte_size:
973
```

## 2. What this authorization is

A conditional founder execution authorization for the bounded P01-04D
execution workflow already defined by the canonically adopted P01-04D
governing protocol, using exactly the canonically bound execution-input
manifest identity above.

```text
this authorization is inactive until:
1. this execution-authorization package is canonically adopted on main; and
2. the required MODEL A′ read-only post-merge activation verification
   returns PASS against the actual execution-authorization merge identity
   and the exact execution-input-manifest identity above.

if MODEL A′ does not PASS:
P01-04D execution remains NOT AUTHORIZED
```

## 3. Package documents

- [`founder-authorization.md`](founder-authorization.md) — the controlling
  document: the exact founder execution-authorization decision, its bound
  identities and its prohibition boundary.
- [`acceptance.md`](acceptance.md) — the acceptance criteria for this
  documentation gate.

The `MODEL A′` activation verification result is not recorded inside this
package: by `MODEL A′` §6 the post-merge verification is evidence only and is
recorded outside the canonical commit history.

## 4. Authority

This package amends no founder decision and alters no ratified scientific
decision. It does not change the seven-file candidate inventory, the
artifact-name supersession map, the P01-04D/E/F/G stage separation or the
ratified decisions D1 through D10. On any conflict, D1 through D10 control.
