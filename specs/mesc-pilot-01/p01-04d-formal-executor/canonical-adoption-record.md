# MESC Pilot-01 — P01-04D Formal Executor Canonical Adoption Record

## 1. Purpose

This document reconciles canonical truth following the merge of PR #90, which
adopted the independently reviewed six-path P01-04D formal-executor
implementation into canonical `main`.

```text
records implementation adoption only
creates no entry authority
creates no execution authority
opens no protected input
performs no real generation
```

Every earlier canonical statement that the formal executor was prospective,
absent, unimplemented or unauthorized to exist describes the state before PR #90
and remains truthful for the baseline it describes. Those statements are
superseded for current implementation-status purposes by this record.

## 2. Canonical implementation adoption

```text
PR:
90

implementation head:
962a5ef432c14aa74940e018373168f46a299669

implementation tree:
d5b51ee1569c30b0866e24c65fd15a77836787e5

canonical merge:
e924027f1c8ea08ac4e5e4281fdcf75e5b419693

canonical merge tree:
d5b51ee1569c30b0866e24c65fd15a77836787e5

formal operator implementation code:
CANONICALLY ADOPTED
```

The implementation tree and the canonical merge tree are the same object. That
identity establishes that canonical `main` contains the exact independently
reviewed implementation tree, with no post-review modification.

## 3. Reviewed implementation identity

The three-commit correction history is preserved in order and is not collapsed:

```text
9ceff9ff0ddb894dbede65f8042a47d20dea6d1c
feat(mesc): implement P01-04D formal executor

93a0b0af1f45f2e38a5361053885721d79882d6d
fix(mesc): close formal executor verification gaps

962a5ef432c14aa74940e018373168f46a299669
fix(mesc): enforce formal manifest contract
```

Each commit has exactly one parent, chaining from canonical baseline
`4828a314f0c8f1fb4d1db8a5740a8d5d94afcd8b` to the reviewed head.

Final cumulative scope against that baseline:

```text
6 files changed
4705 insertions
0 deletions
```

## 4. Correction history

```text
F1:
independent workspace verification and fingerprint/descriptor recomputation
CLOSED

F2:
second repository-identity verification immediately before first mutation
CLOSED

F3:
exact generation-manifest schema, semantic and canonical-byte validation
CLOSED
```

F1 closed the gap where comparison accepted two identically corrupted
workspaces because it proved only carrier consistency and A/B byte equality.
F2 closed the gap where repository commit identity was verified at request
construction but not re-read immediately before the first filesystem mutation.
F3 closed the gap where the generation manifest was validated only against its
non-prohibited fields, so two byte-identical workspaces were accepted when both
manifests carried a modified `algorithm_version` or an extra top-level key.

No F1, F2 or F3 correction expanded execution authority. Each narrowed what the
executor accepts; none widened what it is permitted to do.

## 5. Exact six-path scope

```text
A scripts/mesc_p01_04d_operator.py
blob c1010c8ec227312e5b86e2599b1365ae4f2be4f4
+143 -0

A src/medscale/mesc/_formal_generation_v1.py
blob cc23fbffbce4ccb87a36136c1cd13ee0b6f42fb4
+997 -0

A src/medscale/mesc/_formal_split_v1.py
blob 7b921f915282d4d970af1ad8adff61ef6ca5be7a
+1104 -0

A tests/test_mesc_formal_generation_v1.py
blob 3db877fb123c895c0bf3c196f39cdb05f8c15ac2
+1385 -0

A tests/test_mesc_formal_split_v1.py
blob e1c190a965a68c45cb587392447eb6a500bfbd47
+671 -0

A tests/test_mesc_p01_04d_operator.py
blob d1045fcf946a78fa4f989c48600116c49cab14c1
+405 -0
```

No seventh path. No source, test, script, workflow, dependency, lockfile,
documentation or governance path outside this list was changed by PR #90, and
the accepted P01-04 primitives remained byte-identical across the merge.

## 6. Independent review disposition

```text
final disposition:
APPROVE WITH NON-BLOCKING NOTES

blocking findings:
0

F1:
CLOSED

F2:
CLOSED

F3:
CLOSED
```

Non-blocking notes, recorded as notes and not as unresolved blockers:

```text
1. The top-level-key-set comment overstates derivation from the model; the
   literal remains fail-closed through canonical-byte equality and tests.
2. The nine-key identity-core tuple is hand-maintained but protected by
   canonical-byte equality.
3. The 54 pre-existing portability failures remain outside this branch.
4. The algorithm-version guard is intentionally redundant defense in depth.
```

On the reviewed Windows host, 54 pre-existing `test_mesc_b2a_portability.py`
failures were observed, and the identical 54-failure set reproduced on the
canonical parent under the same environment. The reviewed-host full suite was
therefore **not** green, and that host's result establishes non-regression only.
GitHub CI passed on Python 3.11 and Python 3.12.

## 7. Merge identity

```text
canonical merge:
e924027f1c8ea08ac4e5e4281fdcf75e5b419693

tree:
d5b51ee1569c30b0866e24c65fd15a77836787e5

parent[0]:
4828a314f0c8f1fb4d1db8a5740a8d5d94afcd8b

parent[1]:
962a5ef432c14aa74940e018373168f46a299669

parent count:
2

subject:
Merge pull request #90 from IamShehri/feat/mesc-p01-04d-formal-executor

body:
feat(mesc): add P01-04D formal executor

merged at:
2026-08-05T04:24:18Z

merged by:
IamShehri

merge method:
MERGE COMMIT
```

Parents appear in exactly that order. The first-parent delta of the canonical
merge is exactly the six paths above, 4705 insertions and 0 deletions.

## 8. Post-merge workflow evidence

All workflows below were triggered automatically by the merge push to `main` at
canonical commit `e924027f1c8ea08ac4e5e4281fdcf75e5b419693`.

```text
CI:
run 30975038139
run number 274
attempt 1
SUCCESS

quality (py3.11):
SUCCESS
job 92207193199

quality (py3.12):
SUCCESS
job 92207193187
```

```text
CodeQL:
run 30975038120
run number 278
attempt 1
SUCCESS

analyze (python):
SUCCESS
job 92207192974
```

```text
Optional Extras / Backends:
run 30975038141
run number 92
attempt 1
SUCCESS

core-without-backends:
SUCCESS
job 92207192939

backends-transformers:
SUCCESS
job 92207192957

backends-llamacpp:
SUCCESS
job 92207192962
```

```text
workflow runs:
3

jobs:
6

non-success:
0

reruns:
0

dispatches:
0

cancellations:
0
```

Workflows whose current `push` configuration does not match the changed paths
did not run, and their absence is correct rather than a missing check.

## 9. Meaning of implementation adoption

The repository now contains the canonically adopted implementation of the
ratified formal-operator design.

This proves that the formal executor exists as repository code.

It does not prove that protected inputs are authorized for use.

It does not authorize P01-04D entry or execution.

It does not retroactively change the original entry-readiness verdict.

A separately authorized entry-readiness re-evaluation is required before any
entry decision.

The executor has been exercised only against freshly generated synthetic
fixtures under temporary directories. No P01-03G registry content, no external
real source-record file and no real dataset artifact has been read by it.

## 10. Authorization boundary

```text
P01-04D entry:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-04D entry-readiness re-evaluation:
NOT YET AUTHORIZED

P01-04E through P01-04G:
NOT AUTHORIZED

P01-03G registry access:
NOT AUTHORIZED

external real source-record access:
NOT AUTHORIZED

real dataset access:
NOT AUTHORIZED

real split generation:
NOT AUTHORIZED

real Generation A:
NOT AUTHORIZED

real Generation B:
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

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

Canonical adoption of executor code is not P01-04D readiness, not P01-04D entry
authorization, not P01-04D execution authorization, not protected-input
authorization, not Generation A authorization and not Generation B
authorization.

## 11. Current next gate

```text
NEXT GATE:

P01-04D ENTRY-READINESS RE-EVALUATION AUTHORIZATION DISPOSITION

NOT ENTRY
NOT EXECUTION
NOT DATA ACCESS
```

This record does not itself authorize that re-evaluation. It records only that
the implementation code is now canonical, which is one input a later
re-evaluation may consider.

## 12. Scope and non-authority

```text
reconciles canonical truth only
records implementation adoption only
creates no implementation authority beyond what is already adopted
creates no entry authority
creates no execution authority
accesses no protected input
generates no artifact
creates no partition membership
executes no leakage analysis
unlocks no later stage
```

This record amends no founder decision. It does not alter `FD-DREADY-1` through
`FD-DREADY-12`, the prospective-to-adopted operator contract, the seven-file
artifact inventory, the artifact-name supersession map, the P01-04D/E/F/G stage
separation or the ratified scientific decisions D1 through D10. On any conflict,
D1 through D10 control.

## 13. Reconciliation commit identity

The identity of the commit that introduces this record is reported externally —
in its build report and in its independent review record — and is never written
inside the content it would have to hash.
