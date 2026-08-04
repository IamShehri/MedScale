# MESC Pilot-01 — P01-04C Synthetic Fixture Qualification Candidate

This document records a **synthetic qualification candidate**. It is not
canonical evidence, not research evidence and not real split evidence.

## Status

```text
Founder qualification authorization:
ISSUED ON 2026-08-04

Qualification candidate:
BUILT AND EXECUTED LOCALLY

P01-04C acceptance:
NOT YET ISSUED

Canonical adoption:
NOT ACHIEVED

Real dataset execution:
NOT AUTHORIZED

P01-04D:
NOT AUTHORIZED
```

## Authorized and prohibited scope

Authorized by the founder disposition:

```text
synthetic fixture construction
in-memory fixture execution
fixture-only deterministic qualification
local qualification evidence
the tests and documentation listed in this record
```

Not authorized:

```text
P01-04C acceptance
real dataset access
P01-03G registry access
real partition generation
real partition membership
canonical leakage execution
evidence publication
P01-04D through P01-04G
model access
inference
retrieval
training
fine-tuning
clinical use
```

## Canonical baseline

```text
commit:
78cb1004b15c4ff4daa25895e4bbec99c4bb4eae

tree:
f01a6b44b85f5e8964e26b3c8940b1de369cc1b8

subject:
Merge pull request #84 from IamShehri/docs/mesc-p01-04b-acceptance-closeout

body:
docs(mesc): record P01-04B acceptance closeout

parent[0]:
d5a6ac1654cabd33b6a795756d2796bceaf1652a

parent[1]:
e2d4308e4fdc99c206f62cf6b6a78ea6ed14c60b
```

## Branch and candidate commit identity

```text
branch:
test/mesc-p01-04c-fixture-qualification

commits above canonical baseline:
1

parent:
78cb1004b15c4ff4daa25895e4bbec99c4bb4eae

subject:
test(mesc): qualify P01-04C synthetic fixtures

body:
empty

trailers:
none
```

The candidate commit SHA and tree SHA are reported in the build report and in
the independent review request. They are deliberately not written into this
file, because this file is part of the tree those identities hash over and a
self-reference would be circular.

## Exact four-path scope

```text
A tests/test_mesc_p01_04c_fixture_qualification_v1.py
A specs/mesc-pilot-01/p01-04c-fixture-qualification/qualification-record.md
M specs/mesc-pilot-01/plan.md
M specs/mesc-pilot-01/tasks.md
```

No fifth path. No source file, existing test, workflow, dependency, lockfile,
execution-protocol document or P01-03 artifact was changed.

## Fixture definitions

All identities are synthetic and deterministic. Identifiers follow
`p01-04c-example-<two-digit ordinal>` and
`p01-04c-document-<two-digit ordinal>`, and each `source_record_hash` is a
64-lowercase-hex digest derived only from the row ordinal.

```text
p01-04c-small-20-v1
  examples: 20
  source documents: 20 (one example each)
  decisions by row ordinal: 00-07 yes, 08-14 no, 15-19 maybe
  decision distribution: yes 8, no 7, maybe 5
  partition totals: train 14, validation 3, test 3

p01-04c-single-example-v1
  examples: 1
  source documents: 1
  decision: yes
  partition totals: train 1, validation 0, test 0

p01-04c-all-one-label-20-v1
  examples: 20
  source documents: 20 (one example each)
  decision for every example: yes
  partition totals: train 14, validation 3, test 3

empty input
  ordered rows: 0
  source labels: 0
  partition totals: train 0, validation 0, test 0
```

## Ratified edge-case semantics

`pass` does not mean every edge case produces a successful split.

```text
empty input:
EXPECTED FAIL-CLOSED

single-example input:
EXPECTED SUCCESS

all-one-label input:
EXPECTED SUCCESS
```

The empty case is required to fail deterministically with the accepted typed
request-validation error:

```text
exception type:
InvalidFixtureRequestError

taxonomy code:
invalid_fixture_request

sanitized message:
ordered_rows must be a non-empty exact tuple

artifacts emitted:
0

filesystem writes:
0

state mutation:
0
```

The empty case was executed three times with an identical exception type, an
identical taxonomy code and an identical sanitized message. The accepted
non-empty request invariant was not weakened.

## Literal qualification vectors

Every value below is compared against a literal constant in the committed test
module. No expectation is derived from the result under test, and no test
regenerates a golden automatically.

### p01-04c-small-20-v1

```text
fixture_sha256
3b95e70f2b82129556d81f6a8b9ece80d01c314ded57d6cfa2e7c176d452d821

request_id
mesc-pilot-01-fixture-request/1:sha256:65a4f736763287b34334e44516c03f495d2f005c3849472b82082c1861c19e27

split_hash
d451adc740e54b28

split_fingerprint
6c8ca75dbccaf92a4501bd86d1b3c1150ded22cf28cf39696e7f864f2073ef54

group registry
sha256 d68f1e4d4e4e0457d992cdfaa49e2d26fdeef2f123279120eb7da3cabfffcbf7
bytes  6962

example registry
sha256 5d5250261593d82158a3fde480d0025bf9f549b4106b06eac625f7b6bfbeefee
bytes  6322

excluded ledger
sha256 786ba24fd619636052cfb3bd42b49f7bcaeb481e3745a8becb626dc064d80050
bytes  97

summary identity core
sha256 d8f2c264c2952e066661f64107ff6ed0282cb4068f31c3c910c83b4f9b385655
bytes  492

summary document
sha256 3373f5676dcae0c9fda8315bb9334340f141e6e489846e2bfe8330177e4f7365
bytes  597

audit report
sha256 cfbd0134bc007b69603d6178dd06b3410af57823ac3261d00e4206b2e2ebfd58
bytes  351

example count 20
group count   20
partition counts train 14, validation 3, test 3
group counts     train 14, validation 3, test 3
label totals     yes 8, no 7, maybe 5
label matrix     train yes 6 no 5 maybe 3;
                 validation yes 1 no 1 maybe 1;
                 test yes 1 no 1 maybe 1
finding count 0
leaked        false
```

### p01-04c-single-example-v1

```text
fixture_sha256
2d52d8dd9ce964e69d8dc49cfa9239e583352c854cdc1cf77399db20a849b65f

request_id
mesc-pilot-01-fixture-request/1:sha256:4fca9992942ee903f0e36bc2b0676d04a928cdac3c8553ef1babcb7553401013

split_hash
fed2add59657a094

split_fingerprint
5094ece610c3a5e6ed3da9b707f074e2101b31e61b2c6950e2ca2c7e8017659d

group registry
sha256 c0b401c74f2edc215a1c8b0b6c15b8f717ef74cc3f05b3f590560394c710b459
bytes  347

example registry
sha256 9ea7fbdb2cbf09c2957c43f8aaa30bdc6aadfbc43da930ac73580a1cd752e598
bytes  315

excluded ledger
sha256 786ba24fd619636052cfb3bd42b49f7bcaeb481e3745a8becb626dc064d80050
bytes  97

summary identity core
sha256 8110bc21939ec6ad34433ac650582176131dfd27abd75bde6130ecf09e532aad
bytes  488

summary document
sha256 7e28dacd31cb1773d0646e709311cb6003b19649cec34d057195e838e8ab9634
bytes  593

audit report
sha256 cfbd0134bc007b69603d6178dd06b3410af57823ac3261d00e4206b2e2ebfd58
bytes  351

example count 1
group count   1
partition counts train 1, validation 0, test 0
group counts     train 1, validation 0, test 0
label totals     yes 1, no 0, maybe 0
label matrix     train yes 1 no 0 maybe 0;
                 validation yes 0 no 0 maybe 0;
                 test yes 0 no 0 maybe 0
finding count 0
leaked        false

assigned exactly once  yes
assigned partition     train
split_fingerprint      64 lowercase hexadecimal characters
split_hash             16 lowercase hexadecimal characters
```

### p01-04c-all-one-label-20-v1

```text
fixture_sha256
d0c505a39712632f20df8a80bb2c5931481f99ce1180d5b30df0513b3d6f6719

request_id
mesc-pilot-01-fixture-request/1:sha256:3607e24fd5478043606445b150912e775ea655325687988931247eb6dcdf973b

split_hash
7a6e06cfb1b71aa3

split_fingerprint
7aba158a3ddffbbfb230fe7e72acf633cbf1c5b67f41805643a2796812ed64d9

group registry
sha256 4c9dcffa75f9ea1ce2c0192120ea3ba7834bbafc6389b3ef14155cd95fdd44e6
bytes  6962

example registry
sha256 fb2bc6060a6961cd5683df23e5c7441a83496e7544de402ca7ca8455110bddce
bytes  6322

excluded ledger
sha256 786ba24fd619636052cfb3bd42b49f7bcaeb481e3745a8becb626dc064d80050
bytes  97

summary identity core
sha256 7ef665533ba2eaf958b033ab62f01a7e97a1dceeed0bf88ba58bd03508f46f2d
bytes  494

summary document
sha256 78a30c42a27252b67d7cbb100972b0338df1bb19cf3f4ab5995b355678197d0e
bytes  599

audit report
sha256 cfbd0134bc007b69603d6178dd06b3410af57823ac3261d00e4206b2e2ebfd58
bytes  351

example count 20
group count   20
partition counts train 14, validation 3, test 3
group counts     train 14, validation 3, test 3
label totals     yes 20, no 0, maybe 0
label matrix     train yes 14 no 0 maybe 0;
                 validation yes 3 no 0 maybe 0;
                 test yes 3 no 0 maybe 0
finding count 0
leaked        false

group indivisibility  satisfied; each of the twenty source documents lands in
                      exactly one partition
```

### Artifact descriptors — p01-04c-small-20-v1

Role-ascending canonical order.

```text
example_registry  mesc-pilot-01-example-registry/1
  sha256 5d5250261593d82158a3fde480d0025bf9f549b4106b06eac625f7b6bfbeefee
  bytes  6322

excluded_ledger  mesc-pilot-01-excluded-ledger/1
  sha256 786ba24fd619636052cfb3bd42b49f7bcaeb481e3745a8becb626dc064d80050
  bytes  97

group_registry  mesc-pilot-01-group-registry/1
  sha256 d68f1e4d4e4e0457d992cdfaa49e2d26fdeef2f123279120eb7da3cabfffcbf7
  bytes  6962

split_summary  mesc-pilot-01-split-summary-identity-core/1
  sha256 d8f2c264c2952e066661f64107ff6ed0282cb4068f31c3c910c83b4f9b385655
  bytes  492
```

## Repeated-run qualification

For each of the three successful fixtures, three fresh and semantically
identical requests were constructed and the private facade was run three times.
Equality held across all three runs for:

```text
request_id
fixture_sha256
split assignments
computed split_hash
split_fingerprint
group_registry_bytes
example_registry_bytes
excluded_ledger_bytes
split_summary_identity_core_bytes
split_summary_document_bytes
audit_report_bytes
artifact descriptor SHA-256 values
artifact descriptor byte sizes
```

Every successful byte surface ends with exactly one terminal LF where the
accepted serializer requires it, and no surface ends with a doubled LF.

## Side-effect attestation

Every successful fixture was executed with these channels disabled, and each
run still succeeded:

```text
filesystem open/write
socket creation
subprocess execution
clock access
environment reads
randomness
urandom
```

The guard itself is proven to block: a dedicated test asserts that each
prohibited channel raises while the boundary is active, and a further test
asserts every channel is restored afterwards. The empty-input case was also
executed inside the boundary and emitted no artifact and no write.

## No-real-membership attestation

```text
real dataset access            none
P01-03G registry access        none
real partition membership      none generated, none disclosed
real questions/contexts/answers  none — the accepted request type has no field
                                 that can carry payload text
real labels                    none; every decision is a synthetic literal
local paths                    none
usernames                      none
hostnames                      none
timestamps                     none
network URLs                   none
external-resource references   none
```

The accepted public `SourceDocumentGroupedSplitter.assign()` remains
unconditionally fail-closed and was verified to raise
`PilotSplitNotAuthorizedError` for empty, single and twenty-row inputs, both
before and after fixture execution.

## Validation results

Focused qualification suite:

```text
uv run pytest -q -p no:cacheprovider
  tests/test_mesc_p01_04c_fixture_qualification_v1.py

31 passed
0 skipped
0 xfail
0 warnings attributable to the new module
```

Accepted predecessor suites:

```text
uv run pytest -q -p no:cacheprovider
  tests/test_mesc_split_v1.py
  tests/test_mesc_split_artifacts_v1.py
  tests/test_mesc_leakage_v1.py
  tests/test_mesc_fixture_split_v1.py
  tests/test_mesc_p01_04b2d_qualification_v1.py
  tests/test_mesc_fixture_publication_v1.py
  tests/test_mesc_p01_04b_publication_qualification_v1.py

846 passed, 2 skipped
```

The two skips are the pre-existing environmental symlink-permission skips in
`tests/test_mesc_fixture_publication_v1.py`. No accepted predecessor regressed.

Repository gates:

```text
git diff --check          no whitespace errors
uv lock --check           47 packages, unchanged
uv run ruff check .       All checks passed
uv run ruff format --check .  181 files already formatted
uv run python -m mypy     Success: no issues found in 181 source files
uv run pytest -q -p no:cacheprovider   1934 passed, 4 skipped
medscale check            CLEAN
```

The four full-suite skips are the pre-existing environmental skips: three
symlink-permission skips and one absent `transformers` extra. The single
full-suite warning originates in a pre-existing test unrelated to this
candidate; the focused qualification suite produces no warning.

The `medscale check` gate was invoked through the library entry point rather
than the generated console shim, because Windows Application Control blocks a
freshly created virtual-environment console executable on this host. That is an
environmental constraint of the build machine, not a property of the candidate,
and the gate itself reports CLEAN.

## Governance

```text
P01-04B
ACCEPTED AND CANONICALLY ADOPTED

P01-04C qualification authorization
ISSUED

P01-04C qualification candidate
BUILT LOCALLY

P01-04C acceptance
NOT ISSUED

P01-04D
NOT AUTHORIZED

real dataset execution
NOT AUTHORIZED
```

A passing synthetic qualification candidate is not P01-04C acceptance. P01-04C
remains unaccepted until an independent review and a separate founder acceptance
disposition.
