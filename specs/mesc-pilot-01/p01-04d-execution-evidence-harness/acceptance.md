# P-A1 External Execution-Evidence Contract — Acceptance

Status: **documentation acceptance criteria — no implementation, no execution
authorized**

This document defines acceptance for the P-A1 documentation package itself. It
does not accept an implementation, and it does not close XD-EXEC-1.

## 1. Scope of this acceptance

```text
in scope:
the four P-A1 documentation paths and their internal consistency
the P-A1 implementation clarification PIC-1 .. PIC-9 and the associated
deterministic implementation decisions
the P-A1 implementation corrections PIC-CORR-1 .. PIC-CORR-6
the P-A1 final implementation corrections PIC-CORR-7 .. PIC-CORR-13
the P-A1 closing implementation corrections PIC-CORR-14 .. PIC-CORR-15

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

The P-A1 package as originally built and canonically adopted:

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

The P-A1 implementation clarification recorded on top of that adoption:

```text
Canonical baseline:
ddd9766e7362a43e79cd8b0728b0eb0d00830441

Canonical tree:
bc3b1a1db5dbca3daf09c13f46631d290de0e692

Clarification class:
DOCUMENTATION CORRECTION ONLY

Added paths:
0

Modified paths:
4

Deleted paths:
0

Renamed paths:
0
```

The four modified paths are exactly `README.md`, `founder-authorization.md`,
`evidence-contract.md` and `acceptance.md` in this directory. No implementation
path, test path, script, workflow, dependency or lockfile is touched.

## 3. Acceptance criteria

### A-1 — Exactly four added documentation paths *(historical — original package)*

**Scope: the ORIGINAL P-A1 package canonically adopted through PR #95**
(`PIC-CORR-5`). This criterion is historical and does not describe the current
clarification commit.

That package added exactly `README.md`, `founder-authorization.md`,
`evidence-contract.md` and `acceptance.md` under
`specs/mesc-pilot-01/p01-04d-execution-evidence-harness/`. There was no fifth
path.

Verification: changed-path enumeration of the **original adopted P-A1 commit**.

```text
SATISFIED — HISTORICAL
```

### A-2 — Zero existing-file modifications *(historical — original package)*

**Scope: the ORIGINAL P-A1 package canonically adopted through PR #95**
(`PIC-CORR-5`). This criterion is historical and does not describe the current
clarification commit.

In that package no existing repository file was modified, renamed or deleted,
and every changed path was an addition.

Verification: name-status enumeration of the **original adopted P-A1 commit**.

```text
SATISFIED — HISTORICAL
```

### A-2A — Current clarification candidate changed-path truth

The current clarification candidate modifies the same four documentation paths
and adds none. It touches no implementation path, test path, script, workflow,
dependency or lockfile, and creates no fifth path.

```text
modified:  4
added:     0
deleted:   0
renamed:   0
```

Verification: name-status enumeration of the current candidate commit; §2 above.

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
finalize still receives a terminal identity — which by `PIC-CORR-14` means
exactly that `finalize` durably created a `TM-2` terminal manifest (A-58).

Verification: `PA1-FD-13`; `evidence-contract.md` §13 and §18.8.

```text
SATISFIED
```

### A-10 — Finalize is the last mutation

The package records that finalize is the last P-A mutation to an execution
episode, and that after seal no file may be rewritten, appended, deleted or
added. That rule holds in every terminal-manifest creation state: under `TM-1`
the partial or invalid creation attempt is itself the last mutation and no
cleanup mutation follows, and under `TM-2` successful manifest creation is the
last mutation (`PIC-CORR-14`, A-58).

Verification: `PA1-FD-12`; `evidence-contract.md` §18.8.8 and §22.

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

The package additionally records the exact authorized differential divergence:
exact equality with `resolve_repository_commit` for every supported non-reparse
shape, with the harness refusing symlink, junction and reparse-point shapes even
where the oracle resolves them, and no other divergence permitted.

Verification: `PA1-FD-4`; `evidence-contract.md` §5.3 and §5.3.1.

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
`record_integrity`, `comparison_disposition`, `terminal_disposition`,
`operator_error_class`, `stage_disposition` and `path_role` are recorded as
exact, case-sensitive closed enumerations, with values outside them rejected and
no arbitrary extension permitted without a founder disposition.

```text
closed enumerations:
10

total closed enumeration values:
77

root_cause_class           15
causal_stage                8
failure_class              20
remediation_disposition     4
record_integrity            2
comparison_disposition      4
terminal_disposition        5
operator_error_class       11
stage_disposition           3
path_role                   5
```

No statement anywhere in this package asserts eight enumerations or sixty-nine
values.

Verification: `PA1-FD-15`; correction `PA1-C4`; clarifications `PIC-7` and
`PIC-8`; `evidence-contract.md` §20, §20.9 and §20.10.

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

Verification: prohibition boundary in `founder-authorization.md` §11; authority
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

The exact allowlist of ten tokens and their durable mappings are recorded, along
with the fixed extraction mechanism and the prohibition on production import of
the formal modules to perform the mapping.

Verification: correction `PA1-C4`; clarification `PIC-9`;
`evidence-contract.md` §15.2, §20.8, §20.8.1, §20.8.2 and §24.

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

A canonical repository identity mismatch observed before `open` is recorded as
exactly such a refusal, consistent with the mandatory non-durable pre-open
observation.

Verification: correction `PA1-C5`; clarification `PIC-2`;
`evidence-contract.md` §5.1 and §13.3.

```text
SATISFIED
```

### A-27 — Evidence inventory exact and closed

The evidence inventory is recorded as exact and closed rather than a minimum,
with seven record classes and an eighth prohibited. `episode-control.jsonl`,
`repository-observation.jsonl`, `preflight.jsonl` and `failure.jsonl` are named
and prohibited explicitly, and state dependence is recorded as governing which of
the seven must exist, never whether an eighth may be created.

Verification: clarification `PIC-1`; `evidence-contract.md` §12 and §12.1.

```text
SATISFIED
```

### A-28 — Non-durable open observation

The pre-open repository observation is recorded as mandatory and non-durable,
producing no `repository_identity_observed` event. A mismatch refuses `open` and
creates no episode directory, episode core, stage journal, invalidation record,
manifest or terminal identity. `observed_canonical_commit` and `identity_match`
are prohibited in `episode-core.json`. The prior unqualified statement that every
command persists a `repository_identity_observed` event is explicitly withdrawn
and replaced by an observation-versus-durability matrix.

Verification: clarification `PIC-2`; `evidence-contract.md` §5, §5.1, §13.3 and
§15.1.

```text
SATISFIED
```

### A-29 — Explicit invalidate before finalize under containment

The pre-finalize observation is recorded as mandatory, with a matching
observation non-durable. On mismatch, `finalize` may neither silently append
invalidation evidence nor seal unless a prior explicit `invalidate` has already
recorded canonical-main movement for the same episode and the exact
expected/observed pair. The required sequence — invalidate, durable
`canonical_main_movement`, finalize retry, re-observe, confirm equality with the
recorded movement, seal in containment — is recorded exactly, together with the
refusal on a further movement and the requirement of a new explicit `invalidate`
before another attempt. No repository-observation field is added to
`episode-manifest.json`.

Verification: clarification `PIC-3`; `evidence-contract.md` §5, §5.2.1 and
§15.4.

```text
SATISFIED
```

### A-30 — Invalidate repository-identity materiality

Repository identity is recorded as material to `invalidate` exactly when
`root_cause_class` is `CANONICAL_MAIN_MOVEMENT` or `failure_class` is
`CANONICAL_MAIN_MISMATCH`, in which case the observation is mandatory,
`expected != observed` is mandatory, and both commit values persist under
`canonical_main_movement`. For every other cause the observation is not required
and a matching observation is never persisted. `identity_match` and a
stage-event structure are prohibited in `episode-invalidation.jsonl`.

Verification: clarification `PIC-4`; `evidence-contract.md` §5, §15.3 and
§15.3.1.

```text
SATISFIED
```

### A-31 — Pre-stage and opened-stage boundary

The ambiguous single lifecycle is replaced by two explicit phases for
`generate`, `compare` and `verify`: a four-step PRE-STAGE and a nine-step OPENED
STAGE beginning with exclusive stage-journal creation and `stage_opened`. A
PRE-STAGE failure is recorded as a harness or process refusal that creates no
stage journal, fabricates no stage and implies no automatic invalidation. The
corrected boundary statement reads that evidence exists before the child once
`stage_opened` has been durably appended, and the claim that failures before
stage creation are stage evidence is explicitly withdrawn.

Verification: clarification `PIC-5`; `evidence-contract.md` §21, §21.1, §21.2
and §21.3.

```text
SATISFIED
```

### A-32 — `stage_failed` and invalidation ownership

One stage-event type `stage_failed` is added, carrying exactly `failure_class`,
`root_cause_class` and `remediation_disposition`, all drawn from existing closed
vocabularies with no free-form text. It is recorded as technical stage evidence
and explicitly not an episode invalidation. Only the explicit `invalidate`
command may create or append `episode-invalidation.jsonl`, and automatic append
by `generate`, `compare`, `verify` or `finalize` is prohibited.

Verification: clarification `PIC-6`; `evidence-contract.md` §15.2 and §17.1.

```text
SATISFIED
```

### A-33 — No continuation after a failed or refused stage

When an opened stage seals `STAGE_REFUSED` or `STAGE_FAILED`, further
`generate`, `compare` or `verify` continuation in that episode is prohibited, no
retry of the failed or refused scientific stage is permitted inside the same
episode, and a fresh scientific attempt requires a new episode.

Explicit `invalidate` is not universally mandatory before `finalize`
(`PIC-CORR-4`, `A-48`); the earlier "invalidate, then finalize" progression
wording is superseded.

Verification: clarification `PIC-6`; correction `PIC-CORR-4`;
`evidence-contract.md` §17.2.

```text
SATISFIED
```

### A-34 — `stage_disposition` exact three values

`stage_disposition` is recorded as a closed enumeration of exactly
`STAGE_COMPLETE`, `STAGE_REFUSED` and `STAGE_FAILED`, each defined, with
`stage_sealed.stage_disposition` carrying exactly one value from the set.

Verification: clarification `PIC-7`; `evidence-contract.md` §15.2 and §20.9.

```text
SATISFIED
```

### A-35 — `path_role` exact five values

`path_role` is recorded as a closed enumeration of exactly
`FORMAL_INPUT_ORDERED_EXAMPLE_REGISTRY`,
`FORMAL_INPUT_SOURCE_DOCUMENT_REGISTRY`,
`FORMAL_INPUT_TRANSFORMED_DATASET_IDENTITY`, `FORMAL_INPUT_SOURCE_RECORDS` and
`FORMAL_INPUT_DECISION_RECORD`, carrying semantic role only, with absolute path,
relative path, locally derived filename, username, hostname and protected
identifier all prohibited.

Verification: clarification `PIC-8`; `evidence-contract.md` §9 and §20.10.

```text
SATISFIED
```

### A-36 — Exact schema versions

The four record kinds carry exact schema versions:

```text
episode-core:         mesc-p01-04d-execution-evidence/episode-core/v1
stage events:         mesc-p01-04d-execution-evidence/stage-event/v1
invalidation events:  mesc-p01-04d-execution-evidence/invalidation-event/v1
episode manifest:     mesc-p01-04d-execution-evidence/episode-manifest/v1
```

Verification: `evidence-contract.md` §15.1, §15.2, §15.3 and §15.4;
`founder-authorization.md` §8.

```text
SATISFIED
```

### A-37 — One-based per-file event ordinal

`event_ordinal` is recorded as starting at one, scoped independently to each
physical JSONL file, increasing by exactly one for every successfully appended
complete canonical event, and never invented after malformed bytes.

Verification: `evidence-contract.md` §15.2; `founder-authorization.md` §8.

```text
SATISFIED
```

### A-38 — Exact UTC timestamp form

Every timestamp field uses the exact UTC RFC3339 form
`YYYY-MM-DDTHH:MM:SS.ffffffZ`, recorded as a string rather than a number,
consistent with the canonical serializer's rejection of binary floating-point
values.

Verification: `evidence-contract.md` §16; `founder-authorization.md` §8.

```text
SATISFIED
```

### A-39 — `byte_equality` and the `comparison_derived` omission rule

`byte_equality` is recorded with the exact representation `EQUAL` or `UNEQUAL`.
`comparison_derived` must not be emitted when a complete seven-file equality
ledger cannot be derived; the stage instead records `stage_failed` and seals
failed or refused as applicable.

Verification: `evidence-contract.md` §11 and §15.2; `founder-authorization.md`
§8.

```text
SATISFIED
```

### A-40 — Split-fingerprint source

`split_fingerprint_observed` is recorded as never derived from persisted stdout.
Generation A and Generation B read `generation-manifest.json` read-only after
successful child completion; `compare` and `verify` read both manifests
read-only and require their authoritative `split_fingerprint` values to agree
before one observed value is recorded.

Verification: `evidence-contract.md` §10.1; `founder-authorization.md` §8.

```text
SATISFIED
```

### A-41 — Harness self-identity and POSIX operator path

`harness_sha256` and `harness_byte_size` cover the exact bytes of
`<repository-root>/scripts/mesc_p01_04d_evidence_harness.py`, whose resolved
target must equal the running script's resolved `__file__` path.
`operator_relative_path` carries the exact value
`scripts/mesc_p01_04d_operator.py` using POSIX `/` separators regardless of host
OS.

Verification: `evidence-contract.md` §15.1; `founder-authorization.md` §8.

```text
SATISFIED
```

### A-42 — Input-surface literals and test-helper import boundary

The five logical input surfaces are recorded as production string literals
obtained without importing the formal split or formal generation modules. The
test-scope formal import permission remains `resolve_repository_commit` only and
is explicitly not broadened to `make_environment`, `SYNTHETIC_COMMIT` or any
other helper from a frozen formal test; the P-A2 test constructs its own
synthetic repositories and fixture inputs.

Verification: `evidence-contract.md` §9 and §27; `founder-authorization.md` §8.

```text
SATISFIED
```

### A-43 — Adopted boundaries unchanged by the clarification

The clarification changes none of `ARCHITECTURE A`, `MODEL E2′`, the six-command
harness surface, the absence of `record-freeze`, the seven scientific artifacts,
the terminal-manifest identity, the P01-04F boundary, the MODEL A′ boundary,
post-seal immutability, the five-field runtime identity, raw stdout and stderr
non-persistence, the six frozen formal-executor paths or the expected
three-path P-A2 scope.

The terminal-manifest identity formula — the SHA-256 and byte size of the
terminal manifest's exact bytes — remains unchanged throughout. `PIC-CORR-14`
qualifies only the state in which that identity exists (`TM-2` alone) and adds
no field, enumeration or value to it (A-58).

Verification: `founder-authorization.md` §8; `evidence-contract.md` §2, §4, §7,
§22, §24, §26 and §28; `README.md` §5 and §7.

```text
SATISFIED
```

### A-44 — Clarification creates no authority

No clarification in this package authorizes P-A2 implementation, asserts that a
P-A2 implementation exists, or closes XD-EXEC-1. The expected future P-A2
additive paths remain exactly three and remain future-only.

Verification: correction `PA1-C1`; `founder-authorization.md` §8, §9 and §10;
`evidence-contract.md` §28 and §29; `README.md` §9.

```text
SATISFIED
```

### A-45 — Exact stage-disposition boundary

`stage_disposition` is decided by an exact three-condition test rather than by
judgement. `STAGE_REFUSED` requires `stage_opened` durably appended,
`child_started` absent, and a `failure_class` drawn from exactly
`CANONICAL_MAIN_MISMATCH`, `HARNESS_IDENTITY_MISMATCH`,
`OPERATOR_IDENTITY_MISMATCH`, `RUNTIME_IDENTITY_MISMATCH` and
`INPUT_IDENTITY_MISMATCH`; every other safely recordable post-`stage_opened`
failure is `STAGE_FAILED`. `INPUT_HASH_FAILURE` and a clean pre-child
`EVIDENCE_WRITE_FAILURE` are recorded explicitly as `STAGE_FAILED`. The phrase
"before child execution or completion" is withdrawn as a definition of
`STAGE_REFUSED`, and no overlap remains.

Verification: correction `PIC-CORR-1`; `founder-authorization.md` §8A;
`evidence-contract.md` §20.9 and §11.

```text
SATISFIED
```

### A-46 — Universal failure triad mapping

`failure_class` is observed and `root_cause_class` and
`remediation_disposition` are derived from it by an exact table total over all
twenty `failure_class` values, applying wherever those closed fields coexist,
including `stage_failed` and episode invalidation evidence. Substitution of
another root cause or remediation value is prohibited, and
`LATER_STAGE_GOVERNANCE_REQUIRED` is recorded as never emitted by a P-A2
`stage_failed`.

Verification: correction `PIC-CORR-2`; `founder-authorization.md` §8A;
`evidence-contract.md` §19.1 and §15.2.

```text
SATISFIED
```

### A-47 — `CHILD_NONZERO_EXIT` derivation

For `CHILD_NONZERO_EXIT` the triad derives from the `operator_error_class`
already recorded on `child_exited`, with a mapping total over all eleven
`operator_error_class` values. The `NO_ERROR` combination is recorded as a
contract contradiction deriving `UNDETERMINED` and
`FOUNDER_DISPOSITION_REQUIRED`, and failing closed.

Verification: correction `PIC-CORR-3`; `founder-authorization.md` §8A;
`evidence-contract.md` §19.2.

```text
SATISFIED
```

### A-48 — Post-failed-stage progression

Continuation, retry and fresh scientific attempts remain governed exactly as
before, while explicit `invalidate` is recorded as **not** universally mandatory
before `finalize`. Where no separate pre-seal invalidation fact exists,
`finalize` may seal directly and `EPISODE_REFUSED` and `EPISODE_FAILED` remain
reachable under the existing precedence. Where canonical-main movement exists,
the `PIC-3` explicit invalidate-before-finalize containment sequence remains
mandatory and is not weakened.

Verification: correction `PIC-CORR-4`; `founder-authorization.md` §8A;
`evidence-contract.md` §17.2, §5.2.1 and §20.7.

```text
SATISFIED
```

### A-49 — Acceptance historical scoping

`A-1` and `A-2` are explicitly scoped to the original P-A1 package canonically
adopted through PR #95 and no longer describe the current clarification commit
as though its four paths were additions. The current candidate truth — four
modified, zero added, zero deleted, zero renamed — is recorded separately.

Verification: correction `PIC-CORR-5`; §2 above; `A-1`, `A-2` and `A-2A`.

```text
SATISFIED
```

### A-50 — Explicit deterministic safety details

Stderr inspection is recorded as operating on bytes in memory without requiring
successful decoding of the full stream, inspecting only the final non-empty line
and accepting only an exact ASCII canonical module-plus-allowlisted-token form,
with empty stderr, non-ASCII or non-UTF-8 bytes, a malformed final line, an
unexpected exception module, a non-allowlisted token and message text merely
containing an allowlisted token all resolving to `UNCLASSIFIED` with no raw class
text or message persisted.

The §20 ten-enumeration seventy-seven-value count is recorded as the named
closed-enumeration ledger, with `mode`, `stage`, `generation_identity` and
`byte_equality` remaining fixed closed domains outside that arithmetic.

Coexisting non-main stage failure and canonical-main movement are recorded as
separately preserved, with the movement requiring its own explicit `invalidate`
record before containment `finalize` may proceed.

Stage failure-event ordering is explicit: `stage_failed` precedes
`stage_sealed`; a nonzero child records `child_started`, `child_exited`,
`stage_failed`, `stage_sealed`; a post-child integrity failure records
`child_exited`, any fully derivable outputs or comparison event, `stage_failed`,
`stage_sealed`; non-derivable outputs or comparison events are omitted rather
than truncated; and malformed journal bytes forbid fabricating any later event
including `stage_sealed`.

Verification: correction `PIC-CORR-6`; `founder-authorization.md` §8A;
`evidence-contract.md` §20.8.2, §20, §15.3.2, §21.2.1 and §18.

```text
SATISFIED
```

### A-51 — Evidence-write cases A, B and C, and structural unseal

The three evidence-write outcomes for an opened stage are recorded as disjoint
and exhaustive. Case A — a zero-byte write failure leaving the journal
syntactically `WELL_FORMED` with a later safe append still possible — carries
`EVIDENCE_WRITE_FAILURE` / `EVIDENCE_INTEGRITY_FAILURE` /
`NO_REMEDIATION_AUTHORIZED` and seals `stage_failed` → `stage_sealed` with
`STAGE_FAILED`. Case B — partial or malformed bytes — preserves the exact bytes
as `MALFORMED_PRESERVED` and fabricates no `stage_failed`, no `stage_sealed` and
no `stage_disposition`. Case C — bytes well formed but a required append no
longer safely recordable — fabricates nothing, prohibits repair and prohibits
later backfill, and leaves the stage `STRUCTURALLY UNSEALED`.

`STRUCTURALLY UNSEALED` is recorded as a structural condition only: not an
enumeration, not an enumeration value, not a durable field, and never written.
A stage is structurally unsealed exactly when `stage_opened` exists and the
journal does not end in exactly one valid `stage_sealed` event.

`safely recordable` is recorded as a defined term — the required canonical event
can be appended atomically and durably, without altering prior bytes and without
leaving malformed or partial bytes — and never as an undefined escape clause.
The prior unqualified §21.2 claim that every post-`stage_opened` failure is
durably representable is explicitly withdrawn and replaced by the qualified
rule.

Verification: correction `PIC-CORR-7`; `founder-authorization.md` §8B;
`evidence-contract.md` §18, §18.0, §18.1, §18.2, §18.3, §18.4, §20.9 and §21.2.

```text
SATISFIED
```

### A-52 — Continuation, finalize and success after structural unseal

Continuation is prohibited immediately on detection, without waiting for a seal
that will never occur: `generate`, `compare`, `verify`, same-stage retry, any
new scientific stage, child launch, new protected-input access, new
protected-input hashing, generation-workspace mutation, automatic re-pin,
journal repair and journal backfill after storage recovery are all recorded as
prohibited, and the episode enters evidence-preserving containment only, with no
new enumeration or record representing that fact.

At `finalize`, a structurally unsealed opened stage is recorded as an unresolved
evidence-integrity corruption condition regardless of syntactic parse success,
selecting `EPISODE_EVIDENCE_CORRUPT` at precedence rank 1 and explicitly not
falling through to `EPISODE_INVALIDATED`, `EPISODE_REFUSED`, `EPISODE_FAILED` or
`EPISODE_COMPLETE_EQUAL`. `finalize` binds the exact existing bytes without
appending or repairing, records `record_integrity` `WELL_FORMED` where those
bytes are syntactically canonical and countable, and records the actual
`event_count` — the structural condition is explicitly not encoded by falsely
changing `record_integrity` to `MALFORMED_PRESERVED`, because syntactic record
integrity and lifecycle completeness are separate properties.

A `finalize` retry is recorded as permitted only after storage becomes writable
and only while `episode-manifest.json` is `TM-0` — physically absent (§18.8,
`PIC-CORR-14`); after successful manifest creation post-seal immutability applies
absolutely, and a physically existing but invalid or incomplete manifest is
`TM-1`, where no retry is permitted at all. Where `finalize` itself cannot
durably create a valid manifest, no valid manifest, no terminal identity, no
success or adoption claim and no scientific continuation exist.

The general abrupt-stop rule is recorded: at `finalize` any opened stage journal
not ending in exactly one valid `stage_sealed` event is an unresolved
evidence-integrity corruption condition, whatever the cause — evidence
destination failure, process termination, harness crash or abrupt host
interruption — and no causal event that was never durably recorded may be
invented.

`EPISODE_COMPLETE_EQUAL` is recorded as additionally requiring every required
opened stage journal to end in exactly one valid `stage_sealed` event carrying
`STAGE_COMPLETE` for every scientifically successful required stage, so an
opened but structurally unsealed stage can never satisfy the successful-episode
prerequisites.

Verification: correction `PIC-CORR-7`; `founder-authorization.md` §8B;
`evidence-contract.md` §13.1, §17.2, §18.5, §18.6, §18.7, §20.7 and §22.

```text
SATISFIED
```

### A-53 — Exact stderr logical-line algorithm

The byte-level scan is recorded exactly: split the exact stderr bytes only on
`b"\n"`; remove exactly one trailing `b"\r"` from a segment if and only if it is
that segment's final byte; treat a bare `b"\r"` not immediately before a `b"\n"`
as **not** a line separator; discard zero-length logical lines after that
normalization; inspect only the final non-empty normalized segment. stderr
remains exact bytes in memory and no full Unicode decode is required.

The recognized prefix is recorded as required at byte offset 0 and as exactly
`b"medscale.mesc._formal_split_v1."`, followed by exactly one allowlisted ASCII
formal exception class token, followed by either the end of the logical line or
one ASCII colon byte, after which all bytes are untrusted message content that
is ignored, need not decode and is never persisted.

The recorded fail-closed set resolving to `UNCLASSIFIED` covers empty stderr, no
final non-empty logical line, a nonmatching or unexpected module prefix, a token
that is not exactly allowlisted, non-ASCII bytes inside the required syntax,
malformed required syntax, an allowlisted token appearing away from byte offset
zero, and any bare-CR layout not satisfying the exact syntax. The rule is
recorded as producing identical classification for LF and CRLF traceback output,
and raw stderr, raw class text and raw messages remain non-persisted.

Verification: correction `PIC-CORR-8`; `founder-authorization.md` §8B;
`evidence-contract.md` §20.8.2, §20.8.2.1, §20.8.2.2 and §20.8.2.3.

```text
SATISFIED
```

### A-54 — `CHILD_LAUNCH_FAILURE` lifecycle

Where process creation itself fails, the package records that no child process
exists, that `child_started` and `child_exited` must both be absent, and that
`pid`, `started_at` and an end timestamp must not be fabricated as child
evidence. The triad is recorded as `CHILD_LAUNCH_FAILURE` /
`CHILD_PROCESS_FAILURE` / `NEW_EPISODE_REQUIRED`, sealing `stage_failed` →
`stage_sealed` with `STAGE_FAILED` where the journal remains safely recordable,
and deferring to `PIC-CORR-7` where it does not. The ordering is named
explicitly in the failure-event ordering list.

Verification: correction `PIC-CORR-9`; `founder-authorization.md` §8B;
`evidence-contract.md` §21.2.1 and §21.2.1.1.

```text
SATISFIED
```

### A-55 — Derivation versus durable destination

Derivation and durability are recorded as separate obligations: the triad may be
deterministically derived without thereby authorizing or requiring a fabricated
durable record, and it is persisted only where an authorized record schema
contains those fields, the authorized destination exists, and the event is
safely recordable. The three worked cases — PRE-STAGE, `MALFORMED_PRESERVED` and
`PIC-CORR-7` case C — are recorded explicitly, together with the rule that the
terminal structural-corruption treatment still applies in each.

Verification: correction `PIC-CORR-10`; `founder-authorization.md` §8B;
`evidence-contract.md` §19.3, §12.1 and §21.1.

```text
SATISFIED
```

### A-56 — Controlling `CHILD_NONZERO_EXIT` table completeness

The controlling table in `founder-authorization.md` contains all eleven
`operator_error_class` values, with `NO_ERROR` present as an actual eleventh row
deriving `UNDETERMINED` and `FOUNDER_DISPOSITION_REQUIRED` and marked
`CONTRACT CONTRADICTION / FAIL CLOSED`. No branch remains table-external, and no
mapping value changes.

Verification: correction `PIC-CORR-11`; `founder-authorization.md` §8A
`PIC-CORR-3` table and §8B; `evidence-contract.md` §19.2.

```text
SATISFIED
```

### A-57 — Historical additive wording and the exact module anchor

`PA1-FD-18`'s phrase "four additive documents" is explicitly scoped to the
original P-A1 documentation package canonically adopted through PR #95, where
all four paths were additions, while the current clarification candidate is
recorded as modifying those same four documents and adding zero documentation
paths. History is not rewritten and the original package is not implied to have
been non-additive.

The literal canonical formal exception module is recorded as exactly
`medscale.mesc._formal_split_v1`, as the only accepted module prefix for the
`PIC-9` / `PIC-CORR-8` extraction mechanism, carried in production as a
classification constant, with production import of the formal module to perform
classification still prohibited.

Verification: corrections `PIC-CORR-12` and `PIC-CORR-13`;
`founder-authorization.md` `PA1-FD-18` and §8B; `evidence-contract.md`
§20.8.2.2 and §27.

```text
SATISFIED
```

### A-58 — Terminal-manifest creation semantics

Partial terminal-manifest creation is defined. `episode-manifest.json` has
exactly three creation states, recorded as mutually exclusive, exhaustive,
observable and deterministic, with no fourth state, and the physical path state
is recorded as distinct from manifest validity.

```text
TM-0   path absent
TM-1   path present, exact bytes NOT a complete canonical schema-valid manifest
TM-2   path present, exact bytes ARE a complete canonical schema-valid manifest
```

State classification is recorded exactly:

```text
path absent:                                        TM-0
existing zero-byte manifest path:                   TM-1
partial or truncated manifest:                      TM-1
malformed JSON manifest:                            TM-1
syntactically valid but schema-incomplete manifest: TM-1
noncanonical or wrong-schema_version manifest:      TM-1
complete canonical valid manifest:                  TM-2
```

`TM-0`: no valid manifest, no canonical seal, no terminal identity and no durably
established terminal disposition. A later `finalize` retry is recorded as
permitted **only** as evidence-preserving containment — only while the path is
still physically absent, only where no successful seal previously occurred, with
no scientific continuation, no journal repair or backfill, and all existing
pre-finalize evidence read-only.

`TM-1`: the exact existing bytes are preserved; truncation, deletion, overwrite,
replacement, rename, repair, seek-and-patch, appending to complete it, re-running
manifest creation and creating a second terminal manifest are all recorded as
prohibited; `finalize` retry is prohibited; there is no valid seal, no terminal
identity and no durably established terminal disposition; scientific success,
scientific continuation, `generate`, `compare`, `verify`, protected-input access,
protected-input hashing and workspace mutation are all prohibited. The episode is
recorded as an irrecoverably failed terminalization attempt — a governance
condition only, with no enumeration, value, field, evidence record, marker or
sidecar created for it — and any fresh scientific attempt is recorded as
requiring a separate new episode that remains subject to all existing
authorization and is neither created nor authorized here.

`TM-2`: the canonical seal and terminal identity are established; terminal
identity is exactly the SHA-256 of the complete valid exact manifest bytes plus
the byte size of those same exact bytes; post-seal immutability is absolute; and
`finalize` retry and rewrite are prohibited.

Path existence alone is recorded as insufficient: terminal identity exists if and
only if the manifest is `TM-2`, `TM-0` and `TM-1` have no terminal identity, and
computing or reporting a terminal identity over invalid, partial or incomplete
bytes is prohibited.

The crash cases are closed. Where the complete valid canonical `TM-2` bytes were
durably created and the harness then crashed before reporting the terminal
identity, the episode is recorded as still canonically sealed, with the identity
recomputable read-only from those exact bytes and rewriting, mutating rerun,
disposition change and second-manifest creation all prohibited. Where a crash
leaves a directory entry whose bytes are not `TM-2`, `TM-1` controls, and intent
is never inferred from how many bytes the harness expected to write.

Exclusive creation is preserved: on entry to `finalize` an existing path is
validated read-only, `TM-2` is recognized as already sealed and `TM-1` as
irrecoverably failed, and neither branch is recorded as a permitted `finalize`
retry. `finalize` remains the last P-A mutation in both — under `TM-1` the
partial or invalid creation attempt is itself the last mutation and no cleanup
mutation follows.

`EPISODE_EVIDENCE_CORRUPT` must not be falsely claimed durable under `TM-1`.
`PIC-CORR-7` is preserved: a structurally unsealed stage ordinarily causes a
valid `TM-2` manifest to carry `EPISODE_EVIDENCE_CORRUPT`, but where
terminal-manifest creation itself reaches `TM-1` no terminal disposition is
durably established at all. The same holds for canonical-main movement: validly
persisted invalidation evidence remains preserved, but `EPISODE_INVALIDATED` must
not be claimed without a valid `TM-2` manifest carrying it.

No `record_integrity` field is invented for the manifest: `WELL_FORMED` and
`MALFORMED_PRESERVED` remain defined only for the bound evidence records, and
manifest validity is decided by the `TM-0` / `TM-1` / `TM-2` semantics alone,
persisting nothing.

Verification: correction `PIC-CORR-14`; `founder-authorization.md` §8C;
`evidence-contract.md` §5.2.1, §13.2, §15.4, §17, §18.6, §18.8, §18.8.1 through
§18.8.11, §20.7 and §22.

```text
SATISFIED
```

### A-59 — Test-authority wording correction

The §27 sentence that could be read as granting additional formal test imports is
removed and replaced. `resolve_repository_commit` is recorded as the **only**
formal execution-module import permitted at test scope, and no other formal
module import is authorized.

```text
test import of medscale.mesc._formal_split_v1:      NOT PERMITTED
test import of medscale.mesc._formal_generation_v1: NOT PERMITTED

for discovering or validating:
exception class names
the exception module literal
input-surface literals
any other contract constant
```

The harness is recorded as owning those exact contract literals locally, as
authorized by the documentation contract, and the P-A2 test as validating them
using literal expected values from the P-A1 contract, synthetic stderr byte
fixtures, synthetic repository fixtures and subprocess behaviour where
authorized, without broadening the formal import exception. The earlier
non-broadening to `make_environment`, `SYNTHETIC_COMMIT` or any other helper from
a frozen formal test is unchanged (A-13, A-42).

Verification: correction `PIC-CORR-15`; `founder-authorization.md` §8C;
`evidence-contract.md` §27.

```text
SATISFIED
```

## 4. Acceptance summary

```text
criteria:
60

satisfied:
60

unsatisfied:
0

original package criteria:
26

implementation-clarification criteria:
18

changed-path truth criterion:
1

implementation-correction criteria:
6

final implementation-correction criteria:
7

closing implementation-correction criteria:
2

new enumerations or enumeration values introduced by the corrections:
0

new evidence record classes introduced by the corrections:
0

new manifest fields introduced by the corrections:
0

new terminal-disposition values introduced by the corrections:
0

recovery sidecars, repair markers or retry markers introduced:
0

named closed enumerations:
10

named closed enumeration values:
77

package disposition:
READY FOR FINAL FRESH INDEPENDENT P-A1 IMPLEMENTATION-CLARIFICATION REVIEW
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
CANONICALLY ADOPTED

P-A1 implementation clarification PIC-1 .. PIC-9:
BUILT LOCALLY — NOT ADOPTED

P-A1 implementation corrections PIC-CORR-1 .. PIC-CORR-6:
BUILT LOCALLY — NOT ADOPTED

P-A1 final implementation corrections PIC-CORR-7 .. PIC-CORR-13:
BUILT LOCALLY — NOT ADOPTED

P-A1 closing implementation corrections PIC-CORR-14 .. PIC-CORR-15:
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
