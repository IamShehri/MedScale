# P01-04D Entry-Readiness Remediation — Acceptance Criteria

```text
Gate type:
DOCUMENTATION AND CONTRACTS ONLY

P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED
```

This document is the acceptance gate for **this remediation documentation
package only**. It does not accept P01-04D, does not accept a future
implementation and does not accept any execution.

[`founder-authorization.md`](founder-authorization.md) controls.

---

## Exact change scope

```text
A specs/mesc-pilot-01/p01-04d-entry-readiness-remediation/README.md
A specs/mesc-pilot-01/p01-04d-entry-readiness-remediation/founder-authorization.md
A specs/mesc-pilot-01/p01-04d-entry-readiness-remediation/implementation-contract.md
A specs/mesc-pilot-01/p01-04d-entry-readiness-remediation/acceptance.md
M specs/mesc-pilot-01/p01-04/plan.md
M specs/mesc-pilot-01/p01-04/artifact-contracts.md
M specs/mesc-pilot-01/p01-04/execution-protocol.md
M specs/mesc-pilot-01/p01-04/decision-record.md
M specs/mesc-pilot-01/tasks.md
```

```text
Total:
9 documentation paths
```

No tenth path. No source change, no test change, no script change, no workflow
change, no dependency change and no lockfile change.

---

## The fourteen acceptance criteria

The remediation documentation passes only when all fourteen criteria hold.

### 1. Founder decisions complete and ordered

`FD-DREADY-1` through `FD-DREADY-12` appear exactly once and in order.

Mechanical form: in
[`founder-authorization.md`](founder-authorization.md) each identifier
`FD-DREADY-1` … `FD-DREADY-12` occurs exactly once as a numbered decision
heading, the twelve headings appear in ascending order, no identifier is
duplicated, no identifier is skipped, and no identifier beyond `FD-DREADY-12`
exists anywhere in the package.

### 2. Single formal operator surface

A single formal operator surface is defined:

```text
scripts/mesc_p01_04d_operator.py
```

No alternative operator path, improvised script, CLI subcommand, public console
script or environment-variable activation switch is defined anywhere in the nine
changed paths.

### 3. Exactly two operator commands

The operator has exactly `generate` and `compare` commands.

```text
operator command count:
2
```

No third command, alias, hidden command, debug command, repair command or
promotion command appears.

### 4. Exact seven-file P01-04D inventory

The exact seven-file P01-04D inventory is defined consistently:

```text
split-policy.json
group-registry.jsonl
example-registry.jsonl
excluded-ledger.json
split-summary-identity-core.json
split-summary.json
generation-manifest.json
```

```text
P01-04D artifact count:
7
```

Every occurrence of the inventory across the nine changed paths lists the same
seven filenames with no eighth artifact and no sidecar, log, receipt, lock,
marker, PID file or timestamp file.

### 5. Complete supersession mapping

Every superseded artifact name has an explicit mapping:

```text
example-split-registry.jsonl       ->  example-registry.jsonl
excluded-or-unassigned-ledger.json ->  excluded-ledger.json
split-fingerprint.json             ->  no standalone file
```

```text
standalone fingerprint file:
none
```

The authoritative full lowercase 64-hex `split_fingerprint` is carried and
verified through `split-summary.json` and `generation-manifest.json`, and the
16-hex `split_hash` is recorded as compatibility/display-only.

### 6. Stage separation

P01-04D, P01-04E, P01-04F and P01-04G outputs are stage-separated:

```text
P01-04D   formal split generation candidate bundle
P01-04E   canonical leakage audit and finding resolution
P01-04F   freeze, independent verification and closeout record
P01-04G   separately authorized repository promotion
```

```text
leakage-audit.json            P01-04E, not P01-04D
p01-04-closeout-record.json   P01-04F, not P01-04D
publication-manifest.json     fixture-only publication artifact
generation-manifest.json      formal P01-04D candidate-bundle manifest
```

No document presents an earlier-stage artifact as a P01-04D generation output,
and no document permits a later stage to mutate an earlier stage's immutable
artifact.

### 7. Fixture tooling explicitly unchanged

Existing fixture-only tooling remains explicitly unchanged:

```text
FixtureSplitFacade
_fixture_publication_v1
```

Both remain private, fixture-only, synthetic-only, non-evidence, unexported and
unchanged. No document re-scopes, widens, promotes or reuses the fixture-only
execution authority for formal P01-04D execution.

### 8. Scientific identity preserved

D1–D10 remain unchanged.

`specs/mesc-pilot-01/p01-04/decision-record.md` carries no edit to the text of
D1 through D10; the remediation appears only as an appended appendix. On any
conflict, D1–D10 control.

### 9. No implementation-started claim

No document claims implementation has started.

Every reference to the six prospective implementation paths, the five future
types and the ten future typed errors is marked prospective, and every one of
those paths remains absent or unchanged at this baseline.

### 10. No entry or execution claim

No document asserts authorization for P01-04D entry, and no document asserts
authorization for P01-04D execution.

Every governing-state block records P01-04D implementation, P01-04D execution
and P01-04D entry as `NOT AUTHORIZED`.

### 11. No protected data accessed

No protected data is accessed.

```text
P01-03G ordered-example registry:      NOT OPENED
P01-03G source-document registry:      NOT OPENED
P01-03G transformed-dataset identity:  NOT OPENED
external source-records.jsonl:         NOT OPENED, NOT LOCATED, NOT PROBED
```

No file under `specs/mesc-pilot-01/p01-03g/` was opened, read, hashed, stat-ed or
parsed; the external source-records location was not searched for and no
environment variable was queried for it. Naming an input role in a prospective
operator contract is not access.

### 12. Document integrity

No unresolved marker of any of the following categories remains in any of the
nine changed paths:

```text
category 1  git merge-conflict start, separator and end marker runs
category 2  unfinished-work markers of the "to-do" and
            "to-be-determined" forms
category 3  the uppercase substitution word used for a value
            not yet supplied
category 4  angle-bracket fill and replace prefixes
```

```text
Required count for every category:
0
```

### 13. Cross-document consistency

All nine changed paths are internally consistent. The following values are
identical wherever they appear:

```text
formal operator script:
scripts/mesc_p01_04d_operator.py

operator commands:
generate
compare

P01-04D artifact count:
7

P01-04D artifact filenames:
the exact seven names in FD-DREADY-6

standalone fingerprint file:
none

P01-04E audit filename:
leakage-audit.json

P01-04F closeout filename:
p01-04-closeout-record.json

fixture manifest:
publication-manifest.json

formal D manifest:
generation-manifest.json

implementation:
NOT AUTHORIZED

execution:
NOT AUTHORIZED
```

Any mismatch is a blocker.

### 14. Exactly one local commit

Exactly one local documentation commit exists.

```text
parent:              78bab082bde3b53cbdbd5f37109437b68ba2e5c5
parent count:        1
commits above main:  1
changed paths:       9
subject:             docs(mesc): resolve P01-04D entry-readiness design blockers
body:                empty
trailers:            none
amends:              0
pushes:              0
remote branch:       absent
PR mutations:        0
```

---

## Current-state topology

`specs/mesc-pilot-01/tasks.md` must contain exactly one live current-state
marker.

```text
live "--- Current controlling state ---" count:
1

blocking stale current-state claims:
0
```

Every other occurrence carries explicit historical supersession framing directly
beneath the marker, and every superseded block's fields are preserved
unrewritten.

---

## Stop conditions

Stop without mutation if:

```text
canonical origin/main is not 78bab082bde3b53cbdbd5f37109437b68ba2e5c5
the branch docs/mesc-p01-04d-entry-readiness-remediation already exists
a tenth path appears in the change set
a protected path is modified
a historical accepted record is rewritten
D1 through D10 are altered
more than one live current-state marker remains
a document asserts implementation, entry or execution authority
a document asserts access to protected registry or source-record content
a required document integrity scan returns a non-zero count
a cross-document value mismatch is found
more than one commit exists above canonical main
```

---

## Protected paths

```text
src/**
tests/**
scripts/**
.github/workflows/**
pyproject.toml
uv.lock
specs/mesc-pilot-01/plan.md
specs/mesc-pilot-01/p01-03/**
specs/mesc-pilot-01/p01-04/acceptance.md
specs/mesc-pilot-01/p01-04/data-model.md
specs/mesc-pilot-01/p01-04/spec.md
specs/mesc-pilot-01/p01-04/README.md
specs/mesc-pilot-01/p01-04c-fixture-qualification/**
every P01-04B and P01-04C historical package
```

Historical accepted records are never rewritten. They are preserved and, where
their current status has moved on, explicitly labelled as superseded without
altering their recorded facts.

---

## What passing this gate does not do

```text
does not authorize P01-04D entry
does not authorize P01-04D implementation
does not authorize P01-04D execution
does not authorize P01-03G registry access
does not authorize external source-record access
does not authorize real dataset access
does not authorize real split generation
does not authorize real partition membership
does not authorize canonical leakage execution
does not create the formal executor or the operator script
does not create a generation workspace or any split artifact
does not promote anything to an evidence root
does not amend D1 through D10
does not complete P01-04
does not unlock P01-05
```

```text
A PASSING DOCUMENTATION GATE IS NEVER EXECUTION AUTHORITY.
```
