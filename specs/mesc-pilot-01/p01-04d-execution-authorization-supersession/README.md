# MESC Pilot-01 — Superseding P01-04D Execution Authorization

This package records the separate superseding founder execution authorization
required before a fresh P01-04D execution episode (Episode #2) may begin,
following the canonical real-input contract correction (PR #104) and the
XD-EXEC-3 re-verification and re-closure (PR #105).

It is conditional: it becomes active only after

```text
1. this superseding-authorization package is canonically adopted on main; and
2. the required MODEL A′ read-only post-merge activation verification returns
   PASS against the actual superseding-authorization merge identity and the
   corrected canonical runtime; and
3. the separate read-only Episode #1 custody reconciliation returns PASS.
```

If any activation condition fails, Episode #2 remains NOT AUTHORIZED.

```text
records an execution-authorization supersession decision only
opens no protected input
creates no generation workspace
performs no real generation
authorizes nothing until MODEL A′ PASS and Episode #1 custody reconciliation PASS
does not execute P01-04D
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
— re-verified and re-closed on corrected canonical inputs,
  PR #105 merge 636540c761aba65d569af3d40b321616497aeb7c
```

The earlier execution authorization (specs/mesc-pilot-01/
p01-04d-execution-authorization/) bound the superseded execution-input-manifest
identity

```text
execution-input-manifest SHA-256:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939

execution-input-manifest byte_size:
973
```

That earlier authorization and its binding remain historical evidence and are
not rewritten. It governed the first fail-closed execution attempt (Episode #1).
For all future P01-04D execution episodes it is superseded by the corrected
canonical identity independently re-measured on canonical main:

```text
execution-input-manifest SHA-256:
b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004

execution-input-manifest byte_size:
820
```

## 2. What this authorization is

A conditional superseding founder execution authorization for exactly one fresh
bounded P01-04D execution episode under the corrected canonical formal executor
and the canonically adopted P01-04D execution protocol, using exactly the five
accepted formal input surfaces bound by the exact execution-input-manifest
identity above.

## 3. Package documents

- [`founder-authorization.md`](founder-authorization.md) — the controlling
  document: the exact superseding founder execution-authorization decision,
  its bound identities, its activation conditions and its prohibition
  boundary.
- [`README.md`](README.md) — this index.

The `MODEL A′` activation verification result is not recorded inside this
package: by `MODEL A′` §6 the post-merge verification is evidence only and is
recorded outside the canonical commit history.

## 4. Authority

This package supersedes the earlier execution authorization for all future
P01-04D execution episodes. It amends no other founder decision and alters no
ratified scientific decision. It does not change the seven-file candidate
inventory, the artifact-name supersession map, the P01-04D/E/F/G stage
separation or the ratified decisions D1 through D10. On any conflict, D1
through D10 control.