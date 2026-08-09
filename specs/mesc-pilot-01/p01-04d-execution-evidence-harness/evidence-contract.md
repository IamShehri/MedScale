# P01-04D External Execution-Evidence Contract

Status: **normative contract — no implementation, no execution authorized**

This document is the technical contract for the future P01-04D external
execution-evidence harness. It is governed by
[`founder-authorization.md`](founder-authorization.md), which controls on any
conflict.

Nothing here authorizes P-A2 implementation or P01-04D execution.

## 1. Scope

The harness records the runtime facts of one P01-04D execution episode into an
external evidence location. It wraps the canonical formal operator and adds no
scientific authority.

```text
harness owns:
EXECUTION-EPISODE EVIDENCE ONLY

harness does not own:
the split policy
the allocation
the seven candidate payloads
the authoritative split fingerprint
the freeze stage
activation verification
```

## 2. Architecture

```text
ARCHITECTURE A
A separate repository-controlled evidence harness wraps the canonical operator
and invokes it as a separate child process.

MODEL E2′
PER-STAGE APPEND-ONLY EVIDENCE
WITH WRITE-ONCE EPISODE CORE
AND WRITE-ONCE TERMINAL MANIFEST
```

Rejected as the current architecture:

```text
shared cross-generation journal:
REJECTED — one shared writer couples the two generations that the protocol
requires to execute without knowledge of each other's outputs

single mutable execution JSON:
REJECTED — in-place rewriting is indistinguishable from tampering and conflicts
with the canonical invalidation rules
```

## 3. Ownership of the canonical required-reporting obligations

| # | Canonical obligation | Owner | Where recorded |
|---|----------------------|-------|----------------|
| 1 | Complete Generation A and B command lines | P-A | `stage_opened.argv` |
| 2 | Process IDs | P-A | `child_started.pid` |
| 3 | Start timestamps | P-A | `child_started.started_at` |
| 4 | End timestamps | P-A | `child_exited.exited_at` |
| 5 | Exit codes | P-A | `child_exited.exit_code` |
| 6 | Input SHA-256 digests at execution time | P-A | `inputs_hashed.inputs[]` |
| 7 | Output artifact byte hashes | P-A | `outputs_hashed.outputs[]` |
| 8 | Generation A/B byte-equality disposition | P-A | `comparison_derived` |
| 9 | Invalidation events | P-A (pre-seal) | `episode-invalidation.jsonl` |
| 10 | Root-cause analysis where applicable | P-A (pre-seal) | structured fields in `episode-invalidation.jsonl` |
| 11 | Freeze timestamp | **P01-04F** | outside P-A |
| 12 | Evidence-root identity | **P01-04F** | outside P-A |
| 13 | Verification-rerun results | P-A | `stage-verify.jsonl` |

Obligations `11` and `12` are deferred, not waived. Obligations `9` and `10` are
owned by P-A only while the episode is unsealed; after seal they belong to the
separately governed stage that discovers the later fact.

## 4. Future harness command surface

```text
open
generate
compare
verify
invalidate
finalize

command count:
6

record-freeze:
DOES NOT EXIST
```

| Command | Child process | Mutation |
|---------|---------------|----------|
| `open` | none | creates `episode-core.json` once |
| `generate` | exactly one operator `generate` | appends one stage record |
| `compare` | exactly one operator `compare` | appends one stage record |
| `verify` | exactly one operator `compare`, read-only rerun | appends one stage record |
| `invalidate` | none | appends to the pre-seal invalidation record |
| `finalize` | none | creates `episode-manifest.json` once |

`verify` is P01-04D episode self-verification only. It is not P01-04F
independent verification and does not authorize P01-04F.

A successful episode therefore intentionally performs canonical compare twice:
once during `compare` and once during `verify`.

Defining these commands creates no authority to invoke any of them over real
inputs.

## 5. Canonical repository identity gate

Every relevant command performs a read-only canonical repository identity
observation and records it as a `repository_identity_observed` event.

```text
observation points:
before open
before every generate stage
immediately before every generate child launch
before compare
immediately before the compare child launch
before verify
before invalidate where repository identity is material
before finalize
```

### 5.1 Scientific continuation

For `open`, `generate`, `compare` and `verify`, the observed canonical commit
must equal `expected_canonical_commit` before scientific continuation.

A mismatch prohibits:

```text
child launch
new protected-input hashing
new scientific-output derivation
compare execution
verify execution
any new generation activity
```

### 5.2 Evidence containment mode

For `invalidate` and `finalize`, the identity check is still mandatory, but a
mismatch does not require abandoning already-created evidence. A mismatch enters
evidence containment mode.

Containment mode may only:

```text
record the safe canonical-main-movement fact
record expected and observed commit identities
invalidate the episode
seal already-existing evidence
produce a terminal identity selected by the §20.7 precedence
```

Under containment the terminal disposition is normally `EPISODE_INVALIDATED` or
`EPISODE_FAILED`, and is `EPISODE_EVIDENCE_CORRUPT` where a record that must be
bound at seal is `MALFORMED_PRESERVED`. Containment never reaches
`EPISODE_COMPLETE_EQUAL`.

Containment mode must not:

```text
launch a child process
access a new protected input
hash new protected input bytes
derive new scientific outputs
mutate a generation workspace
run operator generate
run operator compare
run verify
silently re-pin to the moved canonical main
```

```text
automatic continuation after canonical-main movement:
DOES NOT EXIST

automatic re-pin:
PROHIBITED
```

### 5.3 Independent harness resolver

The harness implements its own read-only expected-canonical-commit gate, because
the canonical operator compare command has no expected-commit argument.

The resolver must cover at least:

```text
detached HEAD
normal .git directory
.git file gitdir pointer
commondir
packed-refs
```

and must fail closed on an unsupported or ambiguous repository shape.

For `generate`, the operator's existing internal double repository-identity
checks remain an additional enforcement layer and are not replaced.

## 6. Child-process contract

```text
operator invocation:
SEPARATE CHILD PROCESS

direct call into formal generation internals:
PROHIBITED

interpreter:
THE EXACT CONFIGURED PYTHON EXECUTABLE

children per stage invocation:
EXACTLY ONE

generation workspace pre-creation by the harness:
PROHIBITED
```

The adopted operator creates the generation workspace itself and refuses any
pre-existing destination. A harness that pre-created the workspace would cause
every generation to fail closed.

## 7. Runtime identity binding

The episode core binds the runtime by exactly these five fields:

```text
resolved_python_executable_path
python_executable_sha256
python_executable_byte_size
python_version
python_implementation
```

```text
The executable SHA-256 binds the configured executable artifact.
It does not claim to cryptographically bind the interpreter's complete dynamic
dependency closure.
```

No additional runtime dependency fields are required by this contract. The
operator's existing interpreter-version refusal remains additional enforcement.

## 8. Command-line recording

Complete argv is recorded as an ordered UTF-8 string array. The array is
authoritative, so no shell quoting ambiguity can arise. A rendered display string
is optional and never authoritative.

Path arguments are recorded in full. Required absolute path values must not be
sanitized or redacted merely because a path may incidentally contain a
username-like component.

```text
permitted, as a required path value:
C:\Users\<account>\...\python.exe

prohibited:
a dedicated username field
a dedicated hostname field
deriving a username from a path
deriving a hostname from a path
environment dumps
tokens
credentials
```

Incidental identity-like text inside a required path is part of that required
path value. It is not a separate identity field, and removing it would break both
the complete-command-line obligation and the runtime binding.

## 9. Input evidence

For each accepted formal input surface the harness may persist at most:

```text
logical surface
SHA-256
byte size
safe path role
```

```text
input bytes:
NEVER PERSISTED

labels:
NEVER PERSISTED

partition membership:
NEVER PERSISTED

question, context, answer, annotation text:
NEVER PERSISTED
```

No accepted digest that XD-EXEC-3 has not canonically bound may be invented here.
P-A evidence records what bytes were actually presented at execution time. After
XD-EXEC-3 closes, the future execution-input manifest remains the authority for
accepted input identity.

## 10. Output evidence

Generation output evidence covers exactly the seven canonical P01-04D candidate
filenames and nothing else:

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

For every file the harness records exactly:

```text
filename
SHA-256
byte size
```

No artifact bytes are copied into external evidence. No eighth
generation-workspace artifact may be created, and no log, receipt, lock, marker,
process-identifier file, timestamp file or sidecar may be written into a
generation workspace.

## 11. Byte-equality contract

Harness-derived seven-file digest equality is the structured equality source. The
canonical operator compare outcome is corroborating enforcement.

| Harness ledger | Operator exit | `comparison_disposition` |
|----------------|---------------|--------------------------|
| EQUAL | zero | `EQUAL_VERIFIED` |
| EQUAL | nonzero | `INTEGRITY_FAILURE` |
| UNEQUAL | nonzero | `BYTE_INEQUALITY` |
| UNEQUAL | zero | `CONTRADICTION` |

`CONTRADICTION` is a hard stop requiring founder disposition.

The harness-derived ledger is required because the operator compare command
cannot express an unequal result: it raises a typed byte-equality failure, and a
returned comparison result is always an equal result. The operator also verifies
workspace self-consistency, manifest contract and fingerprint reconstruction,
which the harness does not replicate, so an `INTEGRITY_FAILURE` remains visible
and distinct.

```text
repair:
PROHIBITED

workspace mutation:
PROHIBITED

suppression of an inequality:
PROHIBITED
```

Any inequality remains visible in the evidence and invalidates both candidates
under the canonical invalidation rules.

## 12. Evidence inventory

All paths are relative to:

```text
<external-evidence-root>/<episode_id>/
```

| Filename | Purpose | Creation point | Mutation rule |
|----------|---------|----------------|---------------|
| `episode-core.json` | Episode identity anchor | `open` | **write-once** |
| `stage-generate-a.jsonl` | Generation A stage record | generate A, before child launch | **append-only** |
| `stage-generate-b.jsonl` | Generation B stage record | generate B, before child launch | **append-only** |
| `stage-compare.jsonl` | Comparison stage record | compare, before child launch | **append-only** |
| `stage-verify.jsonl` | Verification rerun record | verify, before child launch | **append-only** |
| `episode-invalidation.jsonl` | Pre-seal invalidation and structured root cause | first `invalidate` | **append-only, pre-seal only** |
| `episode-manifest.json` | Terminal seal | `finalize` | **write-once, terminal** |

```text
P01-04F file:
NONE

MODEL A′ activation-evidence file:
NONE

generation-workspace sidecar:
NONE
```

## 13. State-dependent inventory

Evidence is never required for a stage that never executed, and no execution
record may be fabricated for an unexecuted stage.

### 13.1 Successful episode

Terminal disposition `EPISODE_COMPLETE_EQUAL` requires:

```text
episode-core.json
stage-generate-a.jsonl
stage-generate-b.jsonl
stage-compare.jsonl
stage-verify.jsonl
episode-manifest.json
```

and no unresolved evidence-corruption condition.

### 13.2 Failed, refused or invalidated episode

```text
required:
episode-core.json where the episode was opened
only the stage records actually opened or started
episode-manifest.json where safe finalization remains possible

present only when a pre-seal invalidation exists:
episode-invalidation.jsonl
```

Every failed or refused episode that can safely reach finalize receives a
terminal manifest and a terminal identity. Evidence of failure is evidence.

### 13.3 Pre-open refusal

If a refusal occurs before `episode-core.json` has been successfully created, no
P-A execution episode exists.

```text
episode directory:           NOT FABRICATED
episode-core.json:           NOT FABRICATED
stage journal:               NOT FABRICATED
episode-invalidation.jsonl:  NOT FABRICATED
episode-manifest.json:       NOT FABRICATED
terminal episode identity:   NOT FABRICATED
```

None of these may be created merely to record that refusal. A pre-open refusal is
a harness or process refusal outside a sealed P-A episode, and it produces no
terminal episode identity.

This follows the same rule as §13: evidence is never required for a stage that
never executed, and no record may be fabricated for one. Evidence containment
(§5.2) does not apply, because containment operates only on an already-open
episode whose existing evidence can be sealed. `EPISODE_REFUSED` therefore
describes a refusal after successful episode open, never a pre-open refusal.

## 14. Episode identity

```text
episode_id
A founder-supplied external episode identifier, constrained to lowercase
alphanumeric and hyphen, three to sixty-four characters, beginning with an
alphanumeric character.

episode_identity
The SHA-256 of the canonical bytes of episode-core.json.
```

The constrained identifier prevents path traversal into the evidence root and
prevents protected content from being carried in a directory name.

`episode_identity` is not stored inside `episode-core.json`; every other record
carries it as a binding reference.

Episode identity binds the canonical commit, the operator identity, the harness
identity and the runtime identity. It does not depend on protected content.

```text
execution-input-manifest identity:
ABSENT UNTIL XD-EXEC-3 CLOSES

activation-verification identity:
OUT OF SCOPE — NO FIELD, NOT EVEN A NULL FIELD
```

A null field would be a schema claim of ownership over a decision that has not
been made.

## 15. Record schemas

### 15.1 `episode-core.json`

```text
schema_version
episode_id
expected_canonical_commit
repository_root
external_evidence_root
operator_relative_path
operator_sha256
operator_byte_size
harness_sha256
harness_byte_size
resolved_python_executable_path
python_executable_sha256
python_executable_byte_size
python_version
python_implementation
```

### 15.2 Stage record events

Every event line carries `schema_version`, `episode_identity`, `stage`, `event`
and `event_ordinal`.

| Event | Additional fields |
|-------|-------------------|
| `stage_opened` | `generation_identity` where applicable, `argv` |
| `repository_identity_observed` | `expected_canonical_commit`, `observed_canonical_commit`, `identity_match`, `mode` |
| `inputs_hashed` | `inputs[]` of `surface`, `sha256`, `byte_size`, `path_role` |
| `child_started` | `pid`, `started_at` |
| `child_exited` | `exited_at`, `exit_code`, `elapsed_ms`, `stdout_sha256`, `stdout_byte_size`, `stderr_sha256`, `stderr_byte_size`, `error_class` |
| `outputs_hashed` | `outputs[]` of `filename`, `sha256`, `byte_size`, exactly seven entries |
| `split_fingerprint_observed` | `split_fingerprint` |
| `comparison_derived` | `byte_equality`, `unequal_filenames[]`, `operator_exit_code`, `comparison_disposition` |
| `stage_sealed` | `stage_disposition` |

`mode` is `CONTINUATION` or `CONTAINMENT`. `elapsed_ms` is a non-authoritative
diagnostic. `unequal_filenames[]` may contain only canonical candidate
filenames. `error_class` is exactly one `operator_error_class` value (§20.8) and
is never free-form text.

### 15.3 `episode-invalidation.jsonl`

```text
schema_version
episode_identity
event_ordinal
root_cause_class
causal_stage
failure_class
remediation_disposition
affected_candidates[]      filename, sha256, byte_size
originating_episode_identity
new_episode_required
canonical_main_movement    expected and observed commit, where applicable
recorded_at
```

### 15.4 `episode-manifest.json`

```text
schema_version
episode_identity
episode_core              filename, sha256, byte_size, record_integrity
records[]                 filename, sha256, byte_size, record_integrity,
                          event_count when countable
terminal_disposition
manifest_sealed_at
```

```text
manifest_sealed_at is the evidence-seal time of this manifest.
It is NOT the P01-04F freeze timestamp, and it does not satisfy obligation 11.
```

The terminal manifest must not embed its own SHA-256.

## 16. Serialization

```text
encoding:            UTF-8
line terminator:     LF
object keys:         sorted
separators:          tight
non-finite numbers:  rejected
JSON documents:      one terminal LF
record lines:        one canonical JSON object plus LF per event
```

Runtime evidence values are not scientifically deterministic across executions.
Their serialization is deterministic.

## 17. Append-only and write-once semantics

```text
may be appended:
stage records, and the pre-seal invalidation record

may be created exactly once:
episode-core.json, episode-manifest.json

may never be rewritten:
any evidence record, once written

truncation:
PROHIBITED

overwrite:
PROHIBITED

seek-and-patch:
PROHIBITED

silent in-place repair:
PROHIBITED
```

Refusal to overwrite is a hard error, never a warning. Write-once records are
created with exclusive creation so that a second attempt fails rather than
replaces.

## 18. Partial-write semantics

If a canonical event append fails and malformed bytes remain:

```text
preserve the exact malformed bytes
do not truncate
do not seek-and-patch
do not append a fabricated stage_sealed event after malformed bytes
classify the record MALFORMED_PRESERVED
prevent EPISODE_COMPLETE_EQUAL
permit failed or evidence-corrupt terminal sealing only where the manifest can
safely bind the preserved bytes
```

A record classified `MALFORMED_PRESERVED` omits `event_count`, because an event
count cannot be derived from malformed bytes and must not be invented.

A malformed record that must be bound at seal selects `EPISODE_EVIDENCE_CORRUPT`
under the §20.7 terminal-disposition precedence, above any invalidation, refusal
or failure label, while the causal fact remains separately recorded.

## 19. Structured root-cause analysis

Free-form root-cause prose is prohibited from the safe P-A evidence bundle. Only
closed-vocabulary structured fields are persisted.

This follows directly from the operator's typed error behaviour: registry and
source-record parse failures embed identifier values in their messages, so
durable narrative diagnostics are a protected-content vector.

The required failure fact is preserved without the message, because the
byte-equality disposition is derived independently and the failure is classified
by type rather than by text. Operator failure classification is itself closed:
the durable value is exactly one `operator_error_class` value (§20.8).

## 20. Closed vocabularies

Values outside these enumerations are rejected. All values are case-sensitive and
exact. No arbitrary extension is permitted without a founder disposition.

```text
closed enumerations:
8

total closed enumeration values:
69

root_cause_class           15
causal_stage                8
failure_class              20
remediation_disposition     4
record_integrity            2
comparison_disposition      4
terminal_disposition        5
operator_error_class       11
```

### 20.1 `root_cause_class`

```text
CANONICAL_MAIN_MOVEMENT
HARNESS_IDENTITY_MISMATCH
OPERATOR_IDENTITY_MISMATCH
RUNTIME_IDENTITY_MISMATCH
INPUT_IDENTITY_FAILURE
INPUT_SCHEMA_FAILURE
PATH_SAFETY_FAILURE
WORKSPACE_STATE_FAILURE
OUTPUT_INVENTORY_FAILURE
BYTE_INEQUALITY
FINGERPRINT_FAILURE
EVIDENCE_INTEGRITY_FAILURE
EVIDENCE_CONFIGURATION_FAILURE
CHILD_PROCESS_FAILURE
UNDETERMINED
```

### 20.2 `causal_stage`

```text
PREFLIGHT
OPEN
GENERATE_A
GENERATE_B
COMPARE
VERIFY
INVALIDATE
FINALIZE
```

### 20.3 `failure_class`

```text
ARGUMENT_REFUSAL
CANONICAL_MAIN_MISMATCH
PATH_SEPARATION_REFUSAL
REPARSE_POINT_REFUSAL
HARNESS_IDENTITY_MISMATCH
OPERATOR_IDENTITY_MISMATCH
RUNTIME_IDENTITY_MISMATCH
INPUT_HASH_FAILURE
INPUT_IDENTITY_MISMATCH
CHILD_LAUNCH_FAILURE
CHILD_NONZERO_EXIT
OUTPUT_INVENTORY_MISMATCH
OUTPUT_HASH_FAILURE
BYTE_INEQUALITY
COMPARE_CONTRADICTION
FINGERPRINT_MISMATCH
EVIDENCE_WRITE_FAILURE
EVIDENCE_MALFORMED_PRESERVED
VERIFY_FAILURE
UNCLASSIFIED
```

### 20.4 `remediation_disposition`

```text
NO_REMEDIATION_AUTHORIZED
NEW_EPISODE_REQUIRED
FOUNDER_DISPOSITION_REQUIRED
LATER_STAGE_GOVERNANCE_REQUIRED
```

### 20.5 `record_integrity`

```text
WELL_FORMED
MALFORMED_PRESERVED
```

### 20.6 `comparison_disposition`

```text
EQUAL_VERIFIED
INTEGRITY_FAILURE
BYTE_INEQUALITY
CONTRADICTION
```

### 20.7 `terminal_disposition`

```text
EPISODE_COMPLETE_EQUAL
EPISODE_FAILED
EPISODE_INVALIDATED
EPISODE_REFUSED
EPISODE_EVIDENCE_CORRUPT
```

Exactly one terminal disposition is selected, by this fixed precedence. Evidence
integrity outranks causal outcome.

```text
1. any record that must be bound at seal is MALFORMED_PRESERVED,
   or any unresolved evidence-integrity corruption exists:
   EPISODE_EVIDENCE_CORRUPT

2. otherwise, explicit invalidation:
   EPISODE_INVALIDATED

3. otherwise, refusal after successful episode open:
   EPISODE_REFUSED

4. otherwise, terminal failure:
   EPISODE_FAILED

5. otherwise, success:
   EPISODE_COMPLETE_EQUAL
```

`EPISODE_EVIDENCE_CORRUPT` takes precedence over `EPISODE_INVALIDATED`,
`EPISODE_FAILED` and `EPISODE_REFUSED`.

Precedence governs the terminal label only. The underlying causal facts remain
independently recorded in the structured failure and invalidation evidence, so an
evidence-corrupt seal never erases the invalidation, refusal or failure that
caused it.

`EPISODE_COMPLETE_EQUAL` requires every success prerequisite of §13.1 and every
bound record `WELL_FORMED`.

This precedence adds no terminal-disposition value.

### 20.8 `operator_error_class`

```text
NO_ERROR
BYTE_EQUALITY_ERROR
INPUT_IDENTITY_ERROR
INPUT_SCHEMA_ERROR
INVENTORY_ERROR
FINGERPRINT_ERROR
METADATA_ERROR
WORKSPACE_SAFETY_ERROR
EVIDENCE_CONFIGURATION_ERROR
GENERATION_ERROR
UNCLASSIFIED
```

This enumeration closes the durable classification of a canonical operator child
failure.

```text
exit_code == 0:
requires NO_ERROR

nonzero operator failure:
mapped in memory from an allowlisted exception-class token to exactly one
semantic value above

unmatched nonzero failure:
UNCLASSIFIED

raw exception class text:
NEED NOT BE DURABLE

raw exception message:
PROHIBITED

value outside this enumeration:
REJECTED
```

`child_exited.error_class` carries exactly one of these values. No free-form error
field exists, and this classification never carries operator message text.

## 21. Episode lifecycle and failure ordering

Each stage follows a fixed fail-closed order:

```text
1.  validate harness arguments
2.  validate the external evidence location
3.  verify path separation
4.  observe canonical repository identity and record it
5.  verify harness, operator and runtime identities
6.  verify episode-core agreement for stages after open
7.  hash permitted inputs, digests and sizes only
8.  open the stage record and append the opening events
9.  launch exactly one child process
10. record child completion
11. hash completed outputs where applicable
12. seal or continue the stage according to the stage
```

Evidence exists before the child does, so a failure before child creation is
recorded with no child and no workspace. A failure after child creation records
the child's outcome first and unconditionally; any later harness-side failure is
a separate appended event and never erases what preceded it.

## 22. Terminal identity and sealing

```text
stable terminal evidence identity exists only after finalize
```

```text
terminal evidence identity:
SHA-256 plus byte size of episode-manifest.json
```

The manifest binds every evidence record present at seal by filename, SHA-256,
byte size, `record_integrity` and `event_count` where countable.

```text
FINALIZE IS THE LAST P-A MUTATION TO AN EXECUTION EPISODE.
```

After successful manifest creation, no existing episode file may be rewritten, no
journal may be appended, no invalidation record may be appended, no file may be
deleted and no new file may be created inside that sealed episode.

The terminal identity cannot be written inside the manifest it hashes. It is
emitted by the harness at finalize and recorded externally, in the build report
and in the independent review record. This is the same constraint MODEL A′
governs at the scale of a canonical merge.

## 23. Path safety

```text
external evidence root must be:
absolute
resolved
existing before episode open
writable
outside the repository root
outside the Generation A workspace
outside the Generation B workspace
outside the future evidence root
```

The episode directory may be created under that validated root.

```text
symlinks, junctions and other reparse-point redirects:
FAIL CLOSED
```

Path containment is evaluated on resolved path components, never on string
prefixes, so a sibling directory whose name shares a prefix with a protected root
is not treated as being inside it.

The harness must not pre-create a generation workspace.

## 24. Sensitive-data minimization

Never persisted:

```text
input bytes
labels
partition membership
question text
context text
answer text
annotation text
raw stdout
raw stderr
environment variables
tokens
credentials
dedicated username
dedicated hostname
raw process memory
generation artifact bytes
```

For child output streams the harness persists only:

```text
SHA-256
byte size
one operator_error_class value
```

Error-class extraction happens in memory, from the typed exception class token
only, and is mapped to the closed `operator_error_class` enumeration (§20.8)
before anything durable is written. The durable evidence contains no raw error
message and no raw exception class text.

The canonical stop condition prohibiting runtime metadata, local paths, usernames
and hostnames is scoped to the generation artifacts. External evidence is
separately and explicitly required to carry command lines, process identifiers
and timestamps. The two rules partition by surface and do not conflict.

## 25. Scientific artifact isolation

The harness cannot alter the scientific result, because:

```text
it writes only inside the external evidence root, which is proved disjoint from
every workspace, the repository and the future evidence root;

it opens workspace files read-only, and only after the child has exited;

it passes no argument that reaches a scientific value;

the generation manifest by construction carries no generation identity, path,
process identifier, timestamp, host name, user name, command line or
environment value.
```

```text
the seven-file bundle:
UNCHANGED

generation-manifest.json contents:
UNCHANGED

the authoritative split fingerprint:
UNCHANGED

A/B byte-equality semantics:
UNCHANGED

D1 through D10:
UNCHANGED

runtime evidence:
SCIENTIFICALLY NON-AUTHORITATIVE
```

## 26. Interface boundaries deliberately left open

Three boundaries are defined by interface only. P-A invents no filename, schema,
directory, owner or storage mechanism for any of them.

```text
1. P01-04F freeze record
   May reference the sealed P01-04D episode by terminal evidence identity.
   Obligations 11 and 12 remain P01-04F obligations and are not waived.

2. MODEL A′ activation-verification evidence
   Out of P-A scope. The episode records only the expected_canonical_commit
   value actually supplied for execution.

3. Post-seal invalidation evidence
   Belongs to the separately governed stage that discovers the later fact, and
   references the prior terminal episode identity.
```

## 27. Production and test import boundary

```text
production harness imports of
medscale.mesc._formal_generation_v1 and medscale.mesc._formal_split_v1
for execution or repository-identity enforcement:
PROHIBITED

test-scope import of resolve_repository_commit by
tests/test_mesc_p01_04d_evidence_harness.py
solely as a differential reference oracle:
PERMITTED
```

The test permission covers synthetic repository shapes only and grants no access
to real P01-03G or source-record bytes. It exists to bound the drift risk created
by the harness carrying its own independent resolver.

```text
production reuse of pure canonical serialization and digest primitives from
medscale.mesc._canonical_json_v1, for evidence serialization and digest
construction:
PERMITTED — subject to later P-A2 identity verification and fixture-only testing
```

That permission is exact and exhaustive. It does not authorize production import
from `medscale.mesc._formal_generation_v1` or `medscale.mesc._formal_split_v1`
for formal execution, generation, comparison, repository-identity enforcement or
any other shortcut into the formal executor. `_canonical_json_v1.py` is not
modified by P-A1.

## 28. Future P-A2 direction

P-A2 is not authorized by this contract. Its expected future additive paths are:

```text
scripts/mesc_p01_04d_evidence_harness.py
tests/test_mesc_p01_04d_evidence_harness.py
specs/mesc-pilot-01/p01-04d-execution-evidence-harness/implementation-acceptance.md
```

Any additional implementation path requires a separate founder scope
disposition. The six adopted formal-executor paths remain immutable under P-A2
unless the founder separately changes that rule.

No test may use real P01-03G bytes or real source-record bytes. Synthetic
fixtures only.

## 29. Authority boundary

```text
P-A2 implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-03G access:
NOT AUTHORIZED

source-record access:
NOT AUTHORIZED

generation workspace creation:
NOT AUTHORIZED

Generation A, Generation B, compare, verify over real inputs:
NOT AUTHORIZED

P01-04E through P01-04G:
NOT AUTHORIZED

XD-EXEC-1:
DECIDED / OPEN

P01-04:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```
