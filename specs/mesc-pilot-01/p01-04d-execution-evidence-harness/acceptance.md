# P-A1 External Execution-Evidence Contract — Acceptance

Status: **documentation acceptance criteria — no implementation, no execution
authorized**

This document defines acceptance for the P-A1 documentation package itself. It
does not accept an implementation, and it does not close XD-EXEC-1.

## 1. Scope of this acceptance

```text
in scope:
the four P-A1 documentation paths and their internal consistency

out of scope:
P-A2 implementation acceptance
harness behaviour
real execution
XD-EXEC-1 closure
```

Implementation acceptance is deferred to a separate
`implementation-acceptance.md` delivered with P-A2, which requires a separate
founder authorization that has not been issued.

## 2. Package identity under test

```text
Canonical baseline:
035392831c6218b5302b04ca7e392eff8724ff52

Canonical tree:
ee409f9dbb57492514b384e2332487a923bf01f9

Package class:
DOCUMENTATION AND CONTRACT ONLY

Added paths:
4

Modified paths:
0
```

## 3. Acceptance criteria

### A-1 — Exactly four added documentation paths

The package adds exactly `README.md`, `founder-authorization.md`,
`evidence-contract.md` and `acceptance.md` under
`specs/mesc-pilot-01/p01-04d-execution-evidence-harness/`. There is no fifth
path.

Verification: changed-path enumeration of the candidate commit.

```text
SATISFIED
```

### A-2 — Zero existing-file modifications

No existing repository file is modified, renamed or deleted. Every changed path
is an addition.

Verification: name-status enumeration of the candidate commit.

```text
SATISFIED
```

### A-3 — Architecture A stated exactly

The package records `ARCHITECTURE A` as the controlling architecture: a separate
repository-controlled evidence harness wraps the canonical operator.

Verification: `founder-authorization.md` §1 and §3; `evidence-contract.md` §2;
`README.md` §5.

```text
SATISFIED
```

### A-4 — MODEL E2′ stated exactly

The package records `MODEL E2′` as per-stage append-only evidence with a
write-once episode core and a write-once terminal manifest, and records the
rejection of a shared cross-generation journal and of a single mutable execution
document.

Verification: `founder-authorization.md` §1 and `PA1-FD-1`;
`evidence-contract.md` §2.

```text
SATISFIED
```

### A-5 — Six-command future harness surface

The future harness command surface is recorded as exactly `open`, `generate`,
`compare`, `verify`, `invalidate`, `finalize`, with command count six.

Verification: `founder-authorization.md` `PA1-FD-6`; `evidence-contract.md` §4;
`README.md` §7.

```text
SATISFIED
```

### A-6 — No record-freeze command

No `record-freeze` command exists in the P-A surface, in any document, in any
inventory or in any lifecycle description.

Verification: `PA1-FD-2`, `PA1-FD-6`, `evidence-contract.md` §4 and §12.

```text
SATISFIED
```

### A-7 — MODEL A′ evidence interface remains out of scope

MODEL A′ activation-verification evidence is recorded as out of P-A scope. No
activation-evidence filename, schema, directory or owner is defined, and the
episode core carries no activation field, not even as a null field.

Verification: `PA1-FD-3`; `evidence-contract.md` §14 and §26.

```text
SATISFIED
```

### A-8 — P01-04F obligations 11 and 12 preserved and deferred

Obligations `11` and `12` are recorded as P01-04F stage obligations, explicitly
not removed, weakened or satisfied by P-A. Only the stable-identity interface is
defined, and the future P01-04F filename, schema and owner are not invented.

Verification: `PA1-FD-2`; `evidence-contract.md` §3 and §26; `README.md` §6.

```text
SATISFIED
```

### A-9 — State-dependent inventory

The successful inventory and the failed, refused or invalidated inventory are
recorded separately. Fabricating an execution record for a stage that never
executed is prohibited, and every failed or refused episode that can safely reach
finalize still receives a terminal identity.

Verification: `PA1-FD-13`; `evidence-contract.md` §13.

```text
SATISFIED
```

### A-10 — Finalize is the last mutation

The package records that finalize is the last P-A mutation to an execution
episode, and that after seal no file may be rewritten, appended, deleted or
added.

Verification: `PA1-FD-12`; `evidence-contract.md` §22.

```text
SATISFIED
```

### A-11 — Evidence containment mode

The package records the controlling distinction between scientific continuation
and evidence containment, including the exact permitted and prohibited
containment actions and the prohibition of automatic re-pin.

Verification: reconciliation `R1`; `evidence-contract.md` §5.2.

```text
SATISFIED
```

### A-12 — Independent harness repository-identity gate

The package requires the future harness to implement its own read-only
expected-canonical-commit gate covering detached HEAD, a normal `.git`
directory, a `.git` file gitdir pointer, `commondir` and `packed-refs`, failing
closed on unsupported or ambiguous repository shape, and records that this is
mandatory because the canonical compare surface has no expected-commit argument.

Verification: `PA1-FD-4`; `evidence-contract.md` §5.3.

```text
SATISFIED
```

### A-13 — Production and test import distinction

The package prohibits production harness imports of the adopted formal
generation and formal split modules for execution or repository-identity
enforcement, and permits a test-scope differential import of
`resolve_repository_commit` as a reference oracle over synthetic repository
shapes only.

Production serialization reuse is bounded exactly to pure canonical serialization
and digest primitives from `medscale.mesc._canonical_json_v1`, and grants no
shortcut into the formal executor.

Verification: `PA1-FD-5`; reconciliation `R4`; correction `PA1-C3`;
`evidence-contract.md` §27.

```text
SATISFIED
```

### A-14 — Exact runtime five-field binding

The runtime binding is exactly the resolved executable path, executable SHA-256,
executable byte size, Python version and Python implementation, with the recorded
limitation that the executable digest does not claim to bind the interpreter's
complete dynamic dependency closure.

Verification: `PA1-FD-10`; reconciliation `R3`; `evidence-contract.md` §7 and
§15.1.

```text
SATISFIED
```

### A-15 — Complete argv and required path rule

Complete argv is recorded as an ordered UTF-8 string array. Required absolute
path values are not sanitized or redacted for incidental username-like
components, while dedicated username and hostname fields, derivation of either
from a path, environment dumps, tokens and credentials remain prohibited.

Verification: `PA1-FD-8`; reconciliation `R5`; `evidence-contract.md` §8.

```text
SATISFIED
```

### A-16 — Raw stdout and stderr non-persistence

Raw child standard output and standard error are never persisted. Only SHA-256,
byte size and exactly one closed `operator_error_class` value persist, extraction
happens in memory, and the durable evidence contains no raw error message and no
raw exception class text.

Verification: `PA1-FD-8`; correction `PA1-C4`; `evidence-contract.md` §19, §20.8
and §24.

```text
SATISFIED
```

### A-17 — Exact seven-file output ledger

Generation output evidence covers exactly the seven canonical candidate
filenames, recording only filename, SHA-256 and byte size, with no artifact bytes
copied and no eighth generation-workspace artifact.

Verification: `PA1-FD-11`; `evidence-contract.md` §10.

```text
SATISFIED
```

### A-18 — Closed vocabularies

`root_cause_class`, `causal_stage`, `failure_class`, `remediation_disposition`,
`record_integrity`, `comparison_disposition`, `terminal_disposition` and
`operator_error_class` are recorded as exact, case-sensitive closed enumerations,
with values outside them rejected and no arbitrary extension permitted without a
founder disposition.

```text
closed enumerations:
8

total closed enumeration values:
69
```

Verification: `PA1-FD-15`; correction `PA1-C4`; `evidence-contract.md` §20.

```text
SATISFIED
```

### A-19 — Partial-write preservation

A partial record write is never repaired. Malformed bytes are preserved exactly,
no fabricated seal event is appended after them, the record is classified
`MALFORMED_PRESERVED`, `event_count` is omitted rather than invented, and a
successful terminal disposition is prevented. A malformed record bound at seal
selects `EPISODE_EVIDENCE_CORRUPT` under the terminal-disposition precedence.

Verification: `PA1-FD-14`; correction `PA1-C2`; `evidence-contract.md` §18 and
§20.7.

```text
SATISFIED
```

### A-20 — No P-A2 authority

No document in this package authorizes P-A2 implementation, and the future P-A2
path direction is recorded as expected scope requiring separate founder
disposition. No clause in any of the four documents asserts that P-A2
authorization already exists.

Verification: `PA1-FD-19`; correction `PA1-C1`; `evidence-contract.md` §28;
`README.md` §9.

```text
SATISFIED
```

### A-21 — Six adopted formal-executor paths unchanged

The six adopted formal-executor paths are not modified by this package, and their
expected blob identities were verified read-only at the canonical baseline before
any mutation.

```text
scripts/mesc_p01_04d_operator.py
src/medscale/mesc/_formal_generation_v1.py
src/medscale/mesc/_formal_split_v1.py
tests/test_mesc_formal_generation_v1.py
tests/test_mesc_formal_split_v1.py
tests/test_mesc_p01_04d_operator.py
```

Verification: read-only blob identity comparison at the canonical baseline, plus
changed-path enumeration of the candidate commit.

```text
SATISFIED
```

### A-22 — No protected-data access

Building this package accessed no P01-03G content, no external source records, no
real dataset bytes, no generation workspace and no evidence contents. No search
for a lost source record was performed. The operator was not invoked.

Verification: build report access attestation.

```text
SATISFIED
```

### A-23 — Execution authority unchanged

No document in this package asserts authorization for P01-04D execution, and no
document asserts authorization for P01-03G access, source-record access, real
dataset access, workspace creation, Generation A, Generation B, compare, verify
over real inputs, or any P01-04E through P01-04G stage.

Verification: prohibition boundary in `founder-authorization.md` §10; authority
boundary in `evidence-contract.md` §29 and `README.md` §9.

```text
SATISFIED
```

### A-24 — Terminal-disposition precedence

Exactly one terminal disposition is selected by a fixed precedence in which
evidence integrity outranks causal outcome: a `MALFORMED_PRESERVED` bound record
or unresolved evidence-integrity corruption selects `EPISODE_EVIDENCE_CORRUPT`
above `EPISODE_INVALIDATED`, `EPISODE_REFUSED` and `EPISODE_FAILED`, while the
causal facts remain independently recorded. `EPISODE_COMPLETE_EQUAL` requires all
success prerequisites and every bound record `WELL_FORMED`. No
terminal-disposition value is added.

Verification: correction `PA1-C2`; `evidence-contract.md` §20.7, §5.2 and §18.

```text
SATISFIED
```

### A-25 — Closed operator error classification

`operator_error_class` is recorded as a closed enumeration of eleven exact
case-sensitive values. Exit code zero requires `NO_ERROR`, nonzero failures map
in memory from an allowlisted exception-class token, unmatched nonzero failures
map to `UNCLASSIFIED`, values outside the enumeration are rejected, and
`child_exited.error_class` carries exactly one such value. No free-form error
field is created.

Verification: correction `PA1-C4`; `evidence-contract.md` §15.2, §20.8 and §24.

```text
SATISFIED
```

### A-26 — Pre-open refusal

A refusal occurring before `episode-core.json` has been successfully created
means no P-A execution episode exists, and no episode directory, episode core,
stage journal, invalidation record, terminal manifest or terminal episode
identity may be fabricated to record it. The rule is consistent with the
state-dependent inventory, with the prohibition on fabricating a record for an
unexecuted stage, and with evidence containment, which applies only to an
already-open episode.

Verification: correction `PA1-C5`; `evidence-contract.md` §13.3.

```text
SATISFIED
```

## 4. Acceptance summary

```text
criteria:
26

satisfied:
26

unsatisfied:
0

package disposition:
READY FOR INDEPENDENT LOCAL P-A1 REVIEW
```

Independent review and canonical adoption remain separate gates. This document
records criteria satisfaction, not adoption.

## 5. What acceptance of this package would not mean

```text
would not accept an implementation
would not close XD-EXEC-1
would not authorize P-A2
would not authorize execution
would not authorize P01-04F
would not satisfy obligations 11 and 12
would not grant protected input access
```

## 6. XD-EXEC-1 closure criteria

XD-EXEC-1 may be marked `CLOSED FOR P01-04D EXECUTION READINESS` only after all
of the following, per `PA1-FD-20`:

```text
1.  Architecture A recorded
2.  P-A1 independently reviewed
3.  P-A1 canonically adopted
4.  a separate founder authorization for P-A2 issued
5.  P-A2 implementation independently reviewed
6.  P-A2 canonically adopted
7.  fixture-only synthetic tests green on canonical main
8.  all required commands including verify implemented and tested
9.  the six frozen formal-executor paths still byte-identical
10. the seven-file deterministic artifact contract unchanged
```

Real execution is not required and must not be required, because execution is
itself unauthorized. Requiring it would make XD-EXEC-1 unclosable by
construction.

Closure of XD-EXEC-1 concerns the execution-evidence mechanism only. XD-EXEC-2
and XD-EXEC-3 remain open, and execution additionally requires a separate founder
execution authorization together with a passing MODEL A′ post-merge activation
verification.

## 7. Governance state

```text
P-A1 package:
BUILT LOCALLY — NOT REVIEWED, NOT ADOPTED

P-A2 implementation:
NOT AUTHORIZED

XD-EXEC-1:
DECIDED / OPEN

P01-04D entry:
AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-04:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```
