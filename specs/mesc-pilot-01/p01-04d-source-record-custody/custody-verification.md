# P01-04D External Source-Record Custody — Verification Record

The measurement evidence satisfying the XD-EXEC-2 closure condition of
[`founder-authorization.md`](founder-authorization.md), which controls on any
conflict.

```text
Canonical baseline:
97a67560430b428759d6121bc5bdf1c0f3f8a317

Verification class:
READ-ONLY CUSTODY MEASUREMENT — NO EXECUTION

Authority:
the founder disposition authorizing narrowly bounded read-only access solely to
locate the artifact, inspect filesystem metadata for path separation, determine
byte size, and sequentially read bytes to compute SHA-256
```

## 1. Expected identity

Taken from the accepted P01-03G transformed-dataset identity
(`specs/mesc-pilot-01/p01-03g/transformed-dataset-identity.json`) and recited
identically by `specs/mesc-pilot-01/p01-04/execution-protocol.md`,
`specs/mesc-pilot-01/p01-03g/dataset-fingerprint.json` and
`specs/mesc-pilot-01/p01-03e/transformation-report.json` — four independent
recitals, zero divergence.

```text
sha256     22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce
byte_size  2770193
```

## 2. Evidence record

Exactly the five permitted fields. No absolute path and no source-record
content of any kind.

```text
surface_name   source-records.jsonl
sha256         22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce
byte_size      2770193
match_result   MATCH
path_role      FORMAL_INPUT_SOURCE_RECORDS
```

`path_role` is the existing closed-enumeration value from
`p01-04d-execution-evidence-harness/evidence-contract.md` §20.10. No
enumeration, value or field is added by this record.

## 3. What was and was not done

```text
artifact located:                       YES
filesystem metadata inspected:          YES — for path separation only
byte size determined:                   YES
bytes read sequentially for SHA-256:    YES

JSONL records parsed:                   NO
record contents inspected or reported:  NO
labels or final_decision values read:   NO
artifact copied:                        NO
artifact transformed or moved:          NO
artifact used as an execution input:    NO
execution workspace created:            NO
```

## 4. Path separation

```text
outside the repository root:
VERIFIED — component-based comparison, not string prefix

copies of the artifact inside the repository root:
NONE — recursive search returned zero results

reparse point on any custody path component:
NONE — every component scanned

outside the external evidence root, Generation A workspace, Generation B
workspace and the future P01-04D evidence root:
SATISFIED — none of these four roots exists at this baseline, so none can
contain the custody location. Recorded as the structural fact it is, not as a
containment measurement. The obligation carries forward: each must be declared
disjoint from the custody location at execution time.
```

## 5. Result

```text
condition 1 — identity match:        SATISFIED
condition 2 — path separation:       SATISFIED
condition 3 — evidence record form:  SATISFIED

XD-EXEC-2:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-3:
OPEN

P01-04D execution:
NOT AUTHORIZED
```
