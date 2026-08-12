# P01-04D Execution Authorization — Acceptance

```text
Gate type:
DOCUMENTATION AND GOVERNANCE ONLY

P01-04D execution:
NOT AUTHORIZED — INACTIVE UNTIL MODEL A′ PASS
```

These criteria govern this documentation gate only. Satisfying every criterion
records a conditional founder execution authorization. It opens no protected
input, creates no generation workspace, produces no artifact and activates no
execution.

```text
A PASSING EXECUTION-AUTHORIZATION DOCUMENTATION GATE IS NOT ACTIVATION.
ACTIVATION REQUIRES THE SEPARATE MODEL A′ POST-MERGE ACTIVATION VERIFICATION.
```

[`founder-authorization.md`](founder-authorization.md) controls. Where this
document would conflict with it, the founder authorization controls.

---

## 1. Exact change scope

```text
A specs/mesc-pilot-01/p01-04d-execution-authorization/README.md
A specs/mesc-pilot-01/p01-04d-execution-authorization/founder-authorization.md
A specs/mesc-pilot-01/p01-04d-execution-authorization/acceptance.md
```

```text
Total:
3 documentation paths
```

No fourth path. No modification of any existing repository file. No source,
test, script, workflow, dependency, lockfile, scientific-policy or
artifact-schema change. `src/`, `tests/` and `scripts/` are untouched, and the
P-C1b implementation and the execution-input manifest are untouched.

---

## 2. Acceptance criteria

### 1. Conditional, not premature

The authorization is expressed as CONDITIONAL / INACTIVE UNTIL MODEL A′ PASS.
No document asserts that execution is authorized before the `MODEL A′`
post-merge activation verification returns PASS.

### 2. Exact execution-input-manifest identity bound

Every occurrence of the execution-input-manifest identity is exactly:

```text
SHA-256:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939

byte_size:
973
```

No path substitutes for the identity, and no other digest appears in its
place.

### 3. Accepted source-record identity bound

```text
SHA-256:
22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce

byte_size:
2770193
```

No absolute custody path is persisted, and no physical copy is designated
authoritative. Authority remains the accepted identity.

### 4. XD-EXEC-1, XD-EXEC-2 and XD-EXEC-3 CLOSED

All three blockers are recited as CLOSED FOR P01-04D EXECUTION READINESS, each
with its canonical closure authority:

```text
XD-EXEC-1:  CLOSED — evidence-harness package (P-A2 adoption, PR #97)
XD-EXEC-2:  CLOSED — PR #99 merge 0941e84
XD-EXEC-3:  CLOSED — PR #102 merge e8cd1f5
```

### 5. MODEL A′ prerequisite intact

`MODEL A′` is named exactly. The activation rule it defines is recorded
unchanged: canonical adoption, then read-only post-merge activation
verification, then — only on PASS — the verified merge becomes
`--expected-canonical-commit`. No second canonical activation commit is
required or permitted for that purpose.

### 6. No self-reference

No future merge identity of this package is predicted, fabricated, reserved or
embedded in any form. The identity is resolved only after adoption through the
`MODEL A′` verification.

### 7. No authority beyond P01-04D

The package authorizes only the exact P01-04D execution workflow of the
adopted governing protocol. It does not authorize training, fine-tuning,
unrelated model experiments, unrelated datasets, expansion of the execution
input set, publication beyond the protocol, P01-04E through P01-04G, or any
subsequent MESC phase.

### 8. Governing protocol identities bound

The execution protocol, the ratified decision record and the activation rule
are bound by their exact canonical blob identities as recorded in
`founder-authorization.md` §4.5.

### 9. No production/test/script change

```text
src/**:          UNCHANGED
tests/**:        UNCHANGED
scripts/**:      UNCHANGED
.github/workflows/**: UNCHANGED
pyproject.toml:  UNCHANGED
uv.lock:         UNCHANGED
```

The six adopted formal-executor paths remain byte-identical, and the exact
seven-file P01-04D candidate artifact inventory is unchanged.

### 10. Document integrity

No unresolved marker of any of the following categories appears in any of the
three paths:

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

### 11. Cross-document consistency

The following values are identical wherever they appear across the three
paths:

```text
canonical baseline:
e8cd1f516efa4f9dde0281cbd07d1d47250d1c58

execution-input-manifest SHA-256:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939

execution-input-manifest byte_size:
973

source-record SHA-256:
22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce

source-record byte_size:
2770193

P01-04D execution authorization:
CONDITIONAL — INACTIVE UNTIL MODEL A′ PASS
```

Any mismatch is a blocker.

---

## 3. Stop conditions

Stop without mutation if:

```text
canonical main is not e8cd1f516efa4f9dde0281cbd07d1d47250d1c58
the tracked worktree or the staged index is not clean
the package directory already exists
the selected local branch name already exists
a fourth path appears in the change set
any existing repository file is modified
a protected path is accessed
a document asserts unconditional execution authorization
a document presents a future merge identity of this package as a real value
a document names MODEL A as the activation mechanism
a document asserts activation without a passing MODEL A′ verification
a required document integrity scan returns a non-zero count
a cross-document value mismatch is found
more than one commit exists above the canonical baseline
```

---

## 4. Protected paths

```text
src/**
tests/**
scripts/**
.github/workflows/**
pyproject.toml
uv.lock
specs/mesc-pilot-01/p01-03g/**
specs/mesc-pilot-01/p01-04/**
specs/mesc-pilot-01/p01-04b**
specs/mesc-pilot-01/p01-04c**
specs/mesc-pilot-01/p01-04d-entry-readiness-remediation/**
specs/mesc-pilot-01/p01-04d-formal-executor/**
specs/mesc-pilot-01/p01-04d-entry-authorization/**
specs/mesc-pilot-01/p01-04d-execution-activation-rule/**
specs/mesc-pilot-01/p01-04d-execution-evidence-harness/**
specs/mesc-pilot-01/p01-04d-source-record-custody/**
specs/mesc-pilot-01/p01-04d-execution-input-identity/**
specs/mesc-pilot-01/plan.md
specs/mesc-pilot-01/tasks.md
every prior governance package
```

Historical accepted records are never rewritten. They are preserved and,
where their current status has moved on, explicitly labelled as superseded
without altering their recorded facts. This package rewrites none of them and
modifies none of them.

---

## 5. What passing this gate does not do

```text
does not activate P01-04D execution
does not supply --expected-canonical-commit
does not authorize P01-03G registry access
does not authorize external source-record access
does not authorize real dataset access
does not authorize real split generation
does not create a generation workspace or any split artifact
does not invoke generate or compare
does not reopen or alter XD-EXEC-1, XD-EXEC-2 or XD-EXEC-3
does not modify P-C1b or the execution-input manifest
does not amend D1 through D10
does not complete P01-04
does not unlock P01-05
```

```text
A PASSING DOCUMENTATION GATE IS NOT ACTIVATION.
ACTIVATION REQUIRES A PASSING MODEL A′ POST-MERGE ACTIVATION VERIFICATION.
```
