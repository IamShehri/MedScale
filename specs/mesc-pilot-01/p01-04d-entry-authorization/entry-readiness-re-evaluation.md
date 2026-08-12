# P01-04D Entry-Readiness Re-Evaluation Record

This record reports the exact result of the independent, read-only P01-04D
entry-readiness re-evaluation performed against canonical main.

It reports a readiness disposition only. It does not grant entry. The founder
decision recorded in [`founder-authorization.md`](founder-authorization.md)
grants entry.

## 1. Verdict

```text
Verdict:
READY FOR FOUNDER P01-04D ENTRY DISPOSITION

B-1 implementation-level status:
CLOSED

B-2 implementation-level status:
CLOSED

New blocking findings:
0

F1 / F2 / F3:
CLOSED
```

## 2. Exact canonical identity

```text
canonical baseline:
9229fea8c208021d3bbdb3767e71c3e3f790262e

tree:
14ee0ffa80573b19c70948dd9db3b282ec5634af
```

## 3. Canonical implementation blobs

```text
scripts/mesc_p01_04d_operator.py
c1010c8ec227312e5b86e2599b1365ae4f2be4f4

src/medscale/mesc/_formal_generation_v1.py
cc23fbffbce4ccb87a36136c1cd13ee0b6f42fb4

src/medscale/mesc/_formal_split_v1.py
7b921f915282d4d970af1ad8adff61ef6ca5be7a

tests/test_mesc_formal_generation_v1.py
3db877fb123c895c0bf3c196f39cdb05f8c15ac2

tests/test_mesc_formal_split_v1.py
e1c190a965a68c45cb587392447eb6a500bfbd47

tests/test_mesc_p01_04d_operator.py
d1045fcf946a78fa4f989c48600116c49cab14c1
```

## 4. Merge identities

```text
PR #90 merge — formal-executor implementation adoption:
e924027f1c8ea08ac4e5e4281fdcf75e5b419693
tree d5b51ee1569c30b0866e24c65fd15a77836787e5
reviewed implementation head 962a5ef432c14aa74940e018373168f46a299669

PR #91 merge — formal-executor adoption-truth reconciliation:
9229fea8c208021d3bbdb3767e71c3e3f790262e
tree 14ee0ffa80573b19c70948dd9db3b282ec5634af
ordered parents e924027f1c8ea08ac4e5e4281fdcf75e5b419693 THEN
2e245e7eb06dd80cb2c9187fd55e907f5995743f
```

## 5. PR #91 post-merge workflow evidence

```text
CI:
run 30979151170
run number 276
attempt 1
SUCCESS

quality (py3.11):
job 92219644143
SUCCESS

quality (py3.12):
job 92219644193
SUCCESS

CodeQL:
run 30979151111
run number 280
attempt 1
SUCCESS

analyze (python):
job 92219643876
SUCCESS

Optional Extras / Backends:
run 30979151116
run number 93
attempt 1
SUCCESS

core-without-backends:
job 92219643906
SUCCESS

backends-transformers:
job 92219643930
SUCCESS

backends-llamacpp:
job 92219643926
SUCCESS

runs:
3

jobs:
6

non-success:
0

reruns:
0
```

## 6. Re-evaluation validation evidence

```text
Focused formal tests:
157 passed
1 skipped
0 failed

Full suite:
2091 passed
5 skipped
0 failed
1 warning

medscale check:
CLEAN

Protected-data accesses:
0

Manual generate invocations:
0

Manual compare invocations:
0
```

## 7. B-1 closure at implementation level

The controlled operator surface exists as repository-controlled code with
exactly the two commands `generate` and `compare` and no third command. Exactly
one generation identity is accepted per invocation, and one invocation never
performs both generations. Every contract-controlled input is required and
explicit, with no real-data default and no environment-based input discovery.

Every validation completes before the first filesystem mutation, including the
second canonical repository-identity re-read. The comparison path verifies each
completed workspace independently, recomputes descriptors from the actual bytes,
reconstructs the authoritative fingerprint, validates the exact manifest
contract, compares byte-for-byte only after both bundles are proved valid, and
writes nothing.

The formal execution modules are private. They are not exported from
`medscale.mesc`, not registered as a `medscale` CLI subcommand, not installed as
a console script and not reachable through an environment-variable activation
switch. The fixture-only execution authority is not reused for formal execution.

## 8. B-2 closure at implementation level

The implementation enforces exactly the seven-file P01-04D candidate inventory:

```text
split-policy.json
group-registry.jsonl
example-registry.jsonl
excluded-ledger.json
split-summary-identity-core.json
split-summary.json
generation-manifest.json

artifact count:
7
```

There is no eighth artifact and no standalone `split-fingerprint.json`. The
authoritative fingerprint is the full lowercase 64-hex SHA-256 carried and
verified through `split-summary.json` and `generation-manifest.json`; the 16-hex
`split_hash` remains compatibility and display only. The artifact-name
supersession map and the P01-04D/E/F/G stage separation are honoured by the
implementation, the contracts and the tests alike.

## 9. Harness artifact recorded truthfully

The first focused-test run reported one failure. Direct measurement established
that it was an artifact of the review harness, not of canonical code:

```text
constructed temporary fixture path length:
265 characters

Windows maximum path length:
260 characters

identical suite re-run with a short temporary root:
157 passed
1 skipped
0 failed
```

No repository file was changed to suppress the failure, and no file was edited
in response to it.

## 10. Observation N-1 — documentation currency

A single non-blocking observation was recorded. Two P01-04 contract documents
still carried wording written at the remediation-design baseline stating that
the operator did not exist and that nothing was produced at that baseline. That
wording became conservative rather than incorrect once the implementation was
adopted: it understates adopted capability and grants no entry or execution
authority.

N-1 was classified non-blocking because it does not affect correctness, safety,
determinism, authority separation or protected-data containment.

This eight-path package corrects N-1 by framing that wording as historical at
the remediation-design baseline and recording current truth alongside it. The
correction changes no artifact name, no schema, no descriptor, no fingerprint
rule, no stage ownership, no invocation parameter, no validation order and no
execution semantics.

## 11. Scientific-identity preservation

```text
partitions:
train, validation, test

targets:
700, 150, 150

total:
1000

decision order:
yes, no, maybe

grouping:
source_document_id

holdout:
none

accepted algorithm version:
unchanged

accepted split seed:
unchanged
```

The formal implementation imports the accepted algorithm version and split seed
rather than redefining them, so D1 through D10 remain unchanged.

## 12. Standing prohibitions at the time of this record

```text
P01-04D execution:
NOT AUTHORIZED

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
