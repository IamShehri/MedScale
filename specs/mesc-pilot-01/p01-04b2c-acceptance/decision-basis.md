# P01-04B2C Acceptance — Decision Basis

```text
Status:
IMMUTABLE EVIDENCE LEDGER

FD-B2C-ACT-1 and FD-B2C-13:
RECORDED — NOT YET ADOPTED ON CANONICAL MAIN
```

This document is the evidence ledger for
[`founder-disposition.md`](founder-disposition.md), which controls on any
conflict. Every value here was verified mechanically against the repository and
against GitHub at the canonical baseline
`9d4b9ed0bada16455781240bb074ffd852397988`.

All identity values in this ledger derived from the B2C fixtures are
**synthetic unit-fixture identities**. None is dataset evidence, scientific
evidence, or a real split artifact.

---

## 1. Authorization identity

```text
Authorization package:
PR #74 — MERGED / CLOSED / NOT DRAFT

Authorization package head:
89a708587ef28b4e19f6225ce86181715a680805

Authorization package tree:
c5afa12e85ef4e0c7f9fcbf71c673da211e1ef2a

Authorization package parent:
3c4d7f153522128533fa9aba26209426b248b4f1

Authorization commit subject:
docs(mesc): authorize P01-04B2C implementation

Canonical authorization merge:
fb17439e6c9f0f28b31689c82567cd9c97312085

Merged at:
2026-08-02T02:32:49Z

Adopted authority:
FD-B2C-1 through FD-B2C-12
```

The adopted authorization documents are
[`../p01-04b2c-authorization/README.md`](../p01-04b2c-authorization/README.md),
[`../p01-04b2c-authorization/founder-authorization.md`](../p01-04b2c-authorization/founder-authorization.md),
[`../p01-04b2c-authorization/implementation-contract.md`](../p01-04b2c-authorization/implementation-contract.md)
and
[`../p01-04b2c-authorization/acceptance.md`](../p01-04b2c-authorization/acceptance.md).

## 2. FD-B2C-ACT-1 sequencing evidence

The implementation commit was created **after** the authorization was merged
into canonical main. The interval is established by two independently observable
timestamps:

```text
Authorization merge (PR #74 -> fb17439e...):
2026-08-02T02:32:49Z

Implementation commit 17c7478... authored and committed:
2026-08-02T08:25:25+03:00  (= 2026-08-02T05:25:25Z)

Elapsed before implementation began:
approximately 2 hours 52 minutes
```

```text
Condition 1 — independent clean-room exact-head review of the authorization
package
SATISFIED — founder-confirmed under FD-B2C-ACT-1

Condition 2 — separate Founder Ready decision
SATISFIED — founder-confirmed under FD-B2C-ACT-1;
PR #74 observed state isDraft = false

Condition 3 — separate Founder Merge decision
SATISFIED — founder-confirmed under FD-B2C-ACT-1

Condition 4 — merge into canonical main
SATISFIED — mechanically verified: PR #74 state MERGED,
merge commit fb17439e6c9f0f28b31689c82567cd9c97312085,
which is the first ordered parent of the canonical baseline

Condition 5 — mechanical post-merge verification
SATISFIED — founder-confirmed under FD-B2C-ACT-1
```

Conditions 1, 2, 3 and 5 are founder-level governance events recorded by
FD-B2C-ACT-1 rather than by repository artifacts. Condition 4 is mechanically
verifiable and was verified. This ledger does not assert repository-mechanical
proof for conditions 1, 2, 3 and 5; it records the founder confirmation as the
governing evidence for them.

FD-B2C-ACT-1 confirms sequencing only. It creates no new implementation
authority, does not accept the implementation, and does not authorize
P01-04B2D.

## 3. Implementation commit, tree and parent

```text
Implementation commit:
17c7478f4e052ac331505d3fcfe4dfde825db898

Implementation tree:
2fc26581ceb1b09216b2bf51de10fcbece68a62b

Implementation parent (single):
fb17439e6c9f0f28b31689c82567cd9c97312085

Commit subject:
feat(mesc): implement P01-04B2C fixture facade

Commit count above the authorization baseline:
1
```

The single parent equals the canonical authorization merge, so the
implementation sits exactly one commit above the adopted authority with no
intervening commit and no rebase.

## 4. PR and merge identity

```text
Implementation PR:
#75 — MERGED / CLOSED / NOT DRAFT

PR title:
feat(mesc): implement P01-04B2C fixture facade

Head ref:
feat/mesc-p01-04b2c-fixture-facade

Head SHA:
17c7478f4e052ac331505d3fcfe4dfde825db898

Base ref:
main

Merged at:
2026-08-02T06:38:16Z

Canonical merge:
9d4b9ed0bada16455781240bb074ffd852397988

Canonical merge tree:
2fc26581ceb1b09216b2bf51de10fcbece68a62b

Ordered parent 1:
fb17439e6c9f0f28b31689c82567cd9c97312085

Ordered parent 2:
17c7478f4e052ac331505d3fcfe4dfde825db898

Canonical merge subject:
Merge pull request #75 from IamShehri/feat/mesc-p01-04b2c-fixture-facade
```

The canonical merge tree equals the reviewed implementation tree exactly, so the
merge introduced no content of its own.

## 5. Path and blob identity

```text
src/medscale/mesc/_fixture_split_v1.py
blob 6511861b41b2276948a6903292f07c3735317177

tests/test_mesc_fixture_split_v1.py
blob 5a2c1d5a19afa4ebee63ffacee5c4b9a7aabafd9
```

Both blobs were verified present on canonical main at
`9d4b9ed0bada16455781240bb074ffd852397988` by direct tree lookup. They are the
same blob identifiers that the independent review verified at the reviewed head.

Accepted modules verified unchanged across the implementation:

```text
src/medscale/mesc/__init__.py
src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/mesc/_leakage_v1.py
```

## 6. Diff statistics

```text
Canonical base-to-merge delta
fb17439e6c9f0f28b31689c82567cd9c97312085 -> 9d4b9ed0bada16455781240bb074ffd852397988

A  src/medscale/mesc/_fixture_split_v1.py    947 additions   0 deletions
A  tests/test_mesc_fixture_split_v1.py      1319 additions   0 deletions

Total:
2 files
2266 additions
0 deletions
```

```text
Reviewed-head-to-merge delta
17c7478f4e052ac331505d3fcfe4dfde825db898 -> 9d4b9ed0bada16455781240bb074ffd852397988

zero changed files
```

```text
PR #75 reported statistics:
changedFiles 2 / additions 2266 / deletions 0
```

The repository delta, the reviewed-head delta and the PR-reported statistics
agree. No rename, no copy, no binary file and no deletion appears in the change.

## 7. Independent review evidence

```text
Independent implementation review:
APPROVE WITH NON-BLOCKING NOTES

Independence:
SATISFIED

Blocking findings:
NONE

Reviewed head:
17c7478f4e052ac331505d3fcfe4dfde825db898

Reviewed tree:
2fc26581ceb1b09216b2bf51de10fcbece68a62b
```

The review:

```text
used a separate session and reviewer role
used a clean detached exact-head worktree
did not author or debug the implementation
performed no repository mutation
independently inspected the contract and predecessor APIs
independently re-derived the synthetic golden identities
```

The independent review occurred outside the GitHub pull-request
review-submission mechanism. The observed PR #75 state carried no submitted
GitHub review, no review decision, no PR comment and no inline review thread.
This ledger therefore makes no claim that any such review interaction existed.

The review independently reconstructed the fixture identity document, the
request identity document, the group identity payload, the compatibility
manifest, all six canonical byte surfaces and the authoritative fingerprint from
the contract text using only the accepted predecessor serializers, and compared
those reconstructions against both the implementation output and the committed
literal golden vectors. Every value matched.

## 8. CI and CodeQL evidence — exact head

```text
CI run:
30736118968

Name:
CI

Status / conclusion:
completed / success

Head SHA:
17c7478f4e052ac331505d3fcfe4dfde825db898

Event:
pull_request

Run attempt:
1

Created / updated:
2026-08-02T06:33:03Z / 2026-08-02T06:33:46Z
```

```text
CI jobs:

quality (py3.11)
completed / success

quality (py3.12)
completed / success
```

Both quality jobs completed the same step sequence, every step `success`:

```text
Sync (locked)                      -> locked dependency sync
Ruff (lint)                        -> Ruff lint
Ruff (format)                      -> Ruff format
Mypy (strict)                      -> Mypy strict
Pytest                             -> Pytest
litdb integrity (medscale check)   -> medscale check
```

```text
CodeQL run:
30736118959

Name:
CodeQL

Status / conclusion:
completed / success

Head SHA:
17c7478f4e052ac331505d3fcfe4dfde825db898

Event:
pull_request

Run attempt:
1

Created / updated:
2026-08-02T06:33:03Z / 2026-08-02T06:34:00Z

CodeQL job:
analyze (python)
completed / success
```

Exactly two workflow runs exist for head
`17c7478f4e052ac331505d3fcfe4dfde825db898`, both at run attempt 1. No rerun, no
retry, no replacement workflow and no manual dispatch is claimed, and none is
evidenced.

### 8.1 Observed push-event runs at the canonical merge commit

Recorded for completeness and factual accuracy. These runs are **not** part of
the mechanical post-merge verification defined in §11, and the acceptance basis
of [`founder-disposition.md`](founder-disposition.md) §3 does not rest on them.

```text
Head SHA:
9d4b9ed0bada16455781240bb074ffd852397988

Event:
push

Run attempt:
1

CI                          run 30736276703   completed / success
CodeQL                      run 30736276690   completed / success
Optional Extras / Backends  run 30736276688   completed / success

Created:
2026-08-02T06:38:18Z
```

These are the ordinary push-triggered workflows that GitHub started when the
merge landed on `main`. They are recorded because GitHub evidence proves them.
Criterion 8 of the decision basis is satisfied by the exact-head
`pull_request` runs of §8, not by these.

## 9. Independent validation evidence

Independently reproduced by the reviewer in a clean detached worktree at exact
head `17c7478f4e052ac331505d3fcfe4dfde825db898`:

```text
Focused B2C tests:
145 passed

Full Pytest:
1579 passed
2 skipped

Focused Ruff:
PASS

Focused Ruff format:
PASS

Source Mypy:
PASS

Test Mypy:
PASS

Project-wide Mypy:
PASS — 175 files

Project-wide Ruff:
PASS

medscale check:
CLEAN
```

The two full-suite skips are pre-existing and environmental — symlink creation
not permitted on the platform, and the `transformers` extra not installed — and
are unrelated to P01-04B2C.

```text
These are implementation-review results at exact head 17c7478..., not new
execution evidence against a real dataset.

All golden values are synthetic unit-fixture identities, not scientific or
dataset evidence.
```

No real split was generated, no real or canonical leakage audit was executed, no
dataset was read, and no model was accessed at any point.

## 10. Ready and merge evidence

```text
Ready:
PR #75 observed isDraft = false

Ready decision:
SEPARATELY FOUNDER-AUTHORIZED AND EXECUTED

Merge decision:
SEPARATELY FOUNDER-AUTHORIZED AND EXECUTED

Merged at:
2026-08-02T06:38:16Z

Merged from:
17c7478f4e052ac331505d3fcfe4dfde825db898

Merged into:
main

Resulting canonical merge:
9d4b9ed0bada16455781240bb074ffd852397988
```

The Ready and Merge decisions are distinct founder decisions. Neither is
inferred from the other, and neither is inferred from the existence of the merge
commit.

## 11. Mechanical post-merge verification

The mechanical post-merge verification is defined as, and limited to, these
repository facts. All were verified:

```text
origin/main
= 9d4b9ed0bada16455781240bb074ffd852397988
VERIFIED

origin/main tree
= 2fc26581ceb1b09216b2bf51de10fcbece68a62b
= the reviewed implementation tree
VERIFIED

ordered parents
= fb17439e... THEN 17c7478f...
VERIFIED

merge subject
= "Merge pull request #75 from IamShehri/feat/mesc-p01-04b2c-fixture-facade"
VERIFIED

canonical base-to-merge delta
= exactly the two implementation paths, +2266 / -0
VERIFIED

reviewed-head-to-merge delta
= zero changed files
VERIFIED

both expected blobs present on canonical main
VERIFIED

source branch feat/mesc-p01-04b2c-fixture-facade
= retained at 17c7478f4e052ac331505d3fcfe4dfde825db898
VERIFIED
```

No post-merge workflow result is asserted as part of this verification. The
push-event runs observed at the merge commit are recorded separately in §8.1 and
are outside this definition.

## 12. Criterion-by-criterion mapping to the adopted implementation contract

Every section of
[`../p01-04b2c-authorization/implementation-contract.md`](../p01-04b2c-authorization/implementation-contract.md)
is represented. Section titles are quoted as they appear in the canonical
contract.

| § | Canonical section title | Requirement | Observed conformance basis | Result |
|---|---|---|---|---|
| 1 | Allowed imports | Standard library plus exactly the listed B1, B2A, B2B and compatibility names; no new dependency; the B1 LF-free serializer never used for a B2C byte surface; `rank_groups` and `derive_example_id` reached only transitively | Import list is a strict subset of the allowlist; `medscale.mesc._split_v1.canonical_json_bytes` is not imported; no `rank_groups` or `derive_example_id` reference; runtime inspection found zero module objects bound in the module namespace; `uv.lock` unchanged | CONFORMS |
| 2 | Exact classes | Four authorized private classes and no others; no `__all__` entry; not imported by `medscale/mesc/__init__.py`; adds no public name | Exactly nine classes exist — request, result, facade and the six-member error hierarchy; `__all__` absent; `medscale/mesc/__init__.py` byte-identical; no authorized name reachable from `medscale.mesc` | CONFORMS |
| 3 | `FixtureSplitRequest` — exact fields | Seventeen fields in the specified order with exact-type contracts; path and external-resource rejection; snapshot obligation; duplicate rejection without silent deduplication | Seventeen fields in contract order; `type(...) is` enforcement throughout; `str`, `int` and `tuple` subclasses and accepted-row subclasses all rejected; `bool` never satisfies an integer count; caller mapping read exactly once and stored as a read-only proxy before validation; all five duplicate rules reject rather than collapse | CONFORMS — see NB-5 |
| 4 | Validation order — controlling | The twelve-step order is controlling and the earliest applicable rule always controls | Reconstructed from source and confirmed by eleven multi-violation precedence probes; markers precede schema and namespace, which precede primitive and collection types, which precede path rejection, which precedes snapshot and duplicate checks, which precede fixture identity, which precedes request identity. Collection exact-type checks precede content inspection exactly as §3.2 requires | CONFORMS |
| 5 | Exact fixture identity payload | Exactly sixteen members; specified element shapes; canonical array ordering before serialization; digest over the canonical bytes; recomputed and compared | Sixteen members with `fixture_sha256` and `request_id` structurally absent; element member sets exact; arrays pre-ordered and object keys left to the serializer; digest independently re-derived and matched | CONFORMS |
| 6 | Exact request identity payload | Exactly four members with the fixed schema and domain; binds the recomputed fixture digest; recomputed and compared | Four members; `request_id` structurally absent from its own payload; the recomputed digest is the value bound, never the caller-supplied one; derived identifier independently re-derived and matched | CONFORMS |
| 7 | Exact integration pipeline | The eleven-step composition using the accepted B1 functions; complete zero-filled label totals; `SourceDocumentGroupedSplitter.assign()` never called | The three accepted B1 functions are called in the specified order with verified signatures; label totals carry every decision explicitly including zero; no reimplementation of join, apportionment, ranking or allocation; the public splitter is never called and remains fail-closed | CONFORMS |
| 8 | Compatibility manifest — exact rules | One assignment per example; the train, validation, test then row-ordinal then example-id ordering; empty `split_hash`; explicit `split_seed`; no holdout; the 16-hex value never authoritative | One assignment per member of `example_ids`; explicit example-to-ordinal mapping that fails closed on duplicate and missing keys; manifest constructed with `split_hash=""` and the B1 seed passed explicitly; 16-hex value obtained from `computed_split_hash` and independently re-derived; never conflated with the 64-hex fingerprint | CONFORMS |
| 9 | Canonical artifact byte surfaces — exact schemas and ordering | Six surfaces with exact schemas, member sets and ordering; six-member group identity payload; constant zero-exclusion ledger; complete summary identity core; the four-role descriptor boundary | All six surfaces independently re-derived byte-for-byte; registry ordering is lexicographic on assigned split as required and is not replaced by canonical partition order; group identity payload has exactly six members; excluded ledger is the exact constant document; summary core carries complete zero-filled domains; the two B2C-level surfaces receive no descriptor role | CONFORMS |
| 10 | Fingerprint construction — exact and non-circular | The three B2A calls in order; the `split_summary` descriptor derived from the core itself; the other three descriptors independently verified against the exact constructed bytes; the final summary built only after the fingerprint exists and never re-entering the payload | The three B2A calls appear in the specified order; all four descriptors are verified with `verify_descriptor_against_bytes` against the exact constructed bytes and completeness of the verified role set is asserted; the final summary is built after the record and is never an input to it | CONFORMS — see NB-4 |
| 11 | `FixtureSplitResult` — exact fields | Twelve fields; every byte field exact `bytes`; every accepted object checked against its exact class | Twelve fields in contract order; frozen and slotted; construction-time exact-type enforcement verified by probe for byte, string and object fields | CONFORMS |
| 12 | Final cross-object invariants | All verified before return; any failure raises the integration-invariant error | The invariant routine runs inside the facade before the result is returned, using the validated request, the joined examples, the assignments and the constructed result; identity agreement, exactly-once assignment, ordinal uniqueness, group indivisibility, partition, label and group reconciliation, zero exclusion, all four descriptor bindings, fingerprint verification, audit-byte equality and fingerprint presence are each checked | CONFORMS — see NB-2, NB-3, NB-4 |
| 13 | Errors and codes | The six-member hierarchy with exact stable codes; the private base not exported; B1, B2A and B2B typed exceptions propagate as themselves; message hygiene | All six classes present with codes exactly as specified and all descending from the private base; a B1 input error and a B2B report-invariant error were each observed propagating as themselves; error messages carry no raw text, path, username, hostname, environment value, timestamp, duration, command or PID | CONFORMS — see NB-1 |
| 14 | Side-effect boundary | No filesystem, network, database, subprocess, environment, clock, locale, timezone, logging, telemetry, cache, randomness, temporary file, publication or dispatch; no global mutable state; no public export, CLI, entry point, capability token, authentication, path-safety layer, overwrite or concurrency handling | Static inspection found no I/O-capable import and no module-level mutable state — every constant is a `Final` scalar, frozenset, tuple or read-only mapping proxy; the committed test poisons the filesystem, socket, subprocess, clock, randomness and environment channels and runs the complete pipeline to a golden fingerprint; no public export, CLI or entry point exists | CONFORMS |
| 15 | Required tests | The complete matrix — request boundary, deterministic integration, compatibility manifest, canonical artifacts with literal golden vectors, leakage integration, side-effect boundary and scope proof; the three B2D fixtures neither implemented nor qualified | 106 test functions and 145 collected cases, all passing; every required group maps to concrete tests whose assertions reach the claimed layer; literal golden vectors for every canonical byte surface were confirmed independent of the implementation's own helpers; the three B2D fixture names appear only in the test asserting their absence | CONFORMS — see NB-1, NB-2, NB-5 |
| 16 | Path scope for the future implementation | Exactly the two authorized paths | Mechanically verified: exactly two added paths, no third path, no rename, no binary file, no deletion, and every protected path and subtree byte-identical | CONFORMS |

```text
Sections represented:
16 of 16

Blocking conformance gap:
NONE
```

## 13. Ledger integrity

This ledger records only facts observed at the canonical baseline
`9d4b9ed0bada16455781240bb074ffd852397988` and from GitHub metadata queried
against the same identities. It does not claim:

```text
a separate post-merge workflow result as part of the mechanical verification
a submitted GitHub pull-request review
a pull-request review decision
a pull-request comment
an inline review thread
a rerun, retry, replacement workflow or manual dispatch
```

The observed PR #75 state carried none of those review interactions, and the
push-event runs at the merge commit are recorded in §8.1 strictly as an
observation outside the verification definition.

No prior governance package was modified in the course of assembling this
ledger. No source file, test file, workflow, dependency or lockfile was
modified. No implementation correction is authorized by any entry recorded here.
