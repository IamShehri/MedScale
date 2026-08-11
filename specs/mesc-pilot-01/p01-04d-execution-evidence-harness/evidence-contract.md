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

This section fixes the command **set**, each command's child-process relation and
each command's mutation. It does not fix per-command argument sets, and no other
section of this contract does (`PA3-DET-1`).

```text
command set:                 FIXED — exactly the six above
per-command argument sets:   NOT FIXED BY THIS CONTRACT
argv recording:              FIXED — §8
```

§21.1 requires harness arguments to be validated before any stage journal exists,
and §8 requires complete argv to be recorded as an ordered UTF-8 string array.
Neither enumerates the arguments a command accepts. An implementation that adds
an argument to an existing command therefore widens no stated contract, provided
the command set remains exactly six, the argument is recorded in `argv` under §8,
and it carries no content §24 prohibits. This is a statement of what the contract
already does and does not fix. It grants no authority and creates no argument.

Defining these commands creates no authority to invoke any of them over real
inputs.

## 5. Canonical repository identity gate

Every relevant command performs a read-only canonical repository identity
observation. **Observation and durability are separate obligations.** An
observation is durable only where an authorized record already exists to receive
it, and no observation may create, extend or invent a record in order to become
durable (`PIC-1`, `PIC-2`, `PIC-3`, `PIC-4`).

| Observation point | Observation | Durable record | Form |
|-------------------|-------------|----------------|------|
| before `open` | MANDATORY | **NONE** — non-durable (`PIC-2`) | — |
| before every `generate` stage | MANDATORY | `stage-generate-a.jsonl` / `stage-generate-b.jsonl` | `repository_identity_observed` |
| immediately before every `generate` child launch | MANDATORY | same stage journal | `repository_identity_observed` |
| before `compare` | MANDATORY | `stage-compare.jsonl` | `repository_identity_observed` |
| immediately before the `compare` child launch | MANDATORY | same stage journal | `repository_identity_observed` |
| before `verify` | MANDATORY | `stage-verify.jsonl` | `repository_identity_observed` |
| before `invalidate`, identity material (`PIC-4`) | MANDATORY | `episode-invalidation.jsonl` | `canonical_main_movement` only |
| before `invalidate`, identity not material | NOT REQUIRED | none — never persisted | — |
| before `finalize` | MANDATORY | **NONE** — non-durable (`PIC-3`) | — |

Every stage observation is durable because the stage journal already exists: the
`generate`, `compare` and `verify` observations occur inside the OPENED STAGE
phase, after `stage_opened` has been durably appended (§21).

```text
statement that every command persists a repository_identity_observed event:
WITHDRAWN — superseded by the matrix above
```

A non-durable observation is a fail-closed gate, not evidence. It is never
fabricated into a record, and its absence from the evidence bundle is correct
rather than missing.

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

For `open` specifically, a mismatch refuses before any episode exists and
creates nothing at all — no episode directory, no `episode-core.json`, no stage
journal, no invalidation record, no manifest and no terminal episode identity
(`PIC-2`, §13.3). On equality, `open` may continue, and `episode-core.json`
continues to carry `expected_canonical_commit` only.

```text
observed_canonical_commit in episode-core.json:  PROHIBITED
identity_match in episode-core.json:             PROHIBITED
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

Sealing and terminal identity remain conditional on the terminal-manifest
creation state of §18.8. Containment produces a terminal identity, and durably
establishes a terminal disposition at all, only where `finalize` creates a TM-2
manifest (`PIC-CORR-14`).

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

#### 5.2.1 Containment sequence at finalize

`finalize` never records canonical-main movement itself, because the terminal
manifest has no location for it and `finalize` may not append an invalidation
record (`PIC-3`, §15.4, §17). Containment at `finalize` therefore requires an
explicit `invalidate` first.

```text
required mismatch sequence:
invalidate
-> durable canonical_main_movement record
-> finalize retry
-> re-observe repository identity
-> confirm the current observed movement equals the recorded movement
-> seal in containment mode
```

`finalize` must not silently append invalidation evidence, and must not seal
unless a prior explicit `invalidate` has already recorded canonical-main
movement for the same episode and the exact expected/observed pair.

```text
canonical main moves again after invalidate:
finalize REFUSES

another finalize attempt:
requires a new explicit invalidate
```

The confirmation compares the identity observed at the `finalize` retry against
the pair already recorded by `invalidate`. Equality permits the seal; any
difference is a further movement and refuses.

This requirement is not weakened by the terminal-manifest creation states of
§18.8. If the movement record was validly persisted and terminal-manifest
creation then reaches TM-1, the invalidation evidence remains preserved, but no
canonical terminal disposition and no terminal identity exist, and
`EPISODE_INVALIDATED` must not be claimed without a valid TM-2 manifest carrying
it (`PIC-CORR-14`).

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

#### 5.3.1 Authorized differential divergence

The independent resolver is qualified by differential testing against
`resolve_repository_commit`, imported test-scope only (§27).

```text
every supported non-reparse repository shape:
EXACT EQUALITY WITH THE ORACLE REQUIRED

symlink, junction and other reparse-point shapes:
THE HARNESS MUST REFUSE, even where the oracle resolves them

any other divergence:
PROHIBITED
```

The stricter reparse refusal is the **only** authorized divergence. It follows
from the §23 path-safety rule, which the oracle does not implement because it
never had to. A differential test that observes any divergence outside this one
case has found a defect in the harness resolver.

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

The logical surface values are exactly these five, hardcoded in production as
string literals because production import of the formal split and formal
generation modules is prohibited (§27):

```text
ordered_example_registry
source_document_registry
transformed_dataset_identity
source_records
decision_record
```

The safe path role is the closed `path_role` enumeration (§20.10). It carries a
semantic role only, and never an absolute path, a relative path, a filename
derived from a local location, a username, a hostname or a protected identifier.

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

### 10.1 Source of `split_fingerprint_observed`

```text
derivation from persisted stdout:
PROHIBITED
```

Child standard output is never persisted, so it is never an evidence source.
The authoritative fingerprint is read from the artifacts themselves.

```text
Generation A and Generation B:
read generation-manifest.json read-only after successful child completion and
extract its authoritative split_fingerprint

compare and verify:
read both generation-manifest.json files read-only and require their
authoritative split_fingerprint values to agree before recording one observed
value
```

Every such read happens after the child has exited and opens workspace files
read-only, so it cannot alter a scientific artifact (§25). Disagreement between
the two manifests is a fingerprint failure and is recorded as a stage failure
(§15.2), never as an observed value. Its classification is fixed:

```text
failure_class:            FINGERPRINT_MISMATCH
root_cause_class:         FINGERPRINT_FAILURE
remediation_disposition:  FOUNDER_DISPOSITION_REQUIRED
stage_disposition:        STAGE_FAILED
```

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

The harness ledger is carried durably by `comparison_derived.byte_equality`,
whose exact representation is:

```text
EQUAL
UNEQUAL
```

The table is total over that two-value domain crossed with zero and nonzero exit,
so every derivable comparison has exactly one disposition. A comparison that is
not derivable has none:

```text
complete seven-file equality ledger cannot be derived:
comparison_derived MUST NOT BE EMITTED
```

Instead the stage appends `stage_failed` and seals `STAGE_FAILED` (§15.2,
§20.9). A ledger that cannot be built — because a workspace is absent, its
inventory is not exactly the seven candidate artifacts, or a candidate cannot be
read — is not an equality result and must never be forced into one.

The disposition is `STAGE_FAILED` rather than `STAGE_REFUSED` in every such
case, because comparison derivation is post-child harness work and none of its
failure classes appears in the closed five-value refusal set of §20.9. The
applicable `failure_class` is `OUTPUT_INVENTORY_MISMATCH`, `OUTPUT_HASH_FAILURE`
or `COMPARE_CONTRADICTION`, each carrying its §19.1 triad.

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

### 12.1 The inventory is exact and closed

This table is the complete evidence inventory. It is **exact and closed**, not a
minimum (`PIC-1`).

```text
evidence record classes:
7

eighth evidence record class:
PROHIBITED

episode-control.jsonl:         PROHIBITED
repository-observation.jsonl:  PROHIBITED
preflight.jsonl:               PROHIBITED
failure.jsonl:                 PROHIBITED
```

State dependence (§13) governs which of these seven records must exist in a
given episode. It never governs whether an eighth may be created. A durable
destination that does not appear in this table does not exist, and no obligation
elsewhere in this contract may be satisfied by inventing one.

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

It additionally requires, explicitly (`PIC-CORR-7`):

```text
every required opened stage journal ends in exactly one valid stage_sealed event

that stage_sealed event carries stage_disposition STAGE_COMPLETE for every
scientifically successful required stage
```

An opened but structurally unsealed stage (§18.4) can never satisfy the
successful-episode prerequisites, because its journal does not end in a valid
`stage_sealed` event. `EPISODE_COMPLETE_EQUAL` is therefore unreachable while
any opened stage remains structurally unsealed, whatever the syntactic
`record_integrity` of its bytes.

### 13.2 Failed, refused or invalidated episode

```text
required:
episode-core.json where the episode was opened
only the stage records actually opened or started
episode-manifest.json where safe finalization remains possible

present only when a pre-seal invalidation exists:
episode-invalidation.jsonl
```

Every failed or refused episode that can safely reach finalize receives a TM-2
terminal manifest and a terminal identity (§18.8). Evidence of failure is
evidence. Where terminal-manifest creation reaches only TM-0 or TM-1, neither a
valid manifest nor a terminal identity exists.

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

A canonical repository identity mismatch observed before `open` is exactly such
a refusal (`PIC-2`, §5.1). The observation is mandatory and non-durable, so the
refusal is correct and complete with no evidence produced. This is consistent
rather than contradictory: the pre-open observation has no authorized durable
destination (§5, §12.1), and inventing one to record it would violate both the
closed inventory and this section.

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

This field set is exact and closed. No repository-observation field may be added
(`PIC-2`).

```text
schema_version:
mesc-p01-04d-execution-evidence/episode-core/v1

operator_relative_path:
scripts/mesc_p01_04d_operator.py
POSIX "/" separators regardless of host OS

harness_sha256 and harness_byte_size cover the exact bytes of:
<repository-root>/scripts/mesc_p01_04d_evidence_harness.py
whose resolved target MUST equal the running script's resolved __file__ path
```

The harness digest is not self-referential: it is computed over the harness
script's own bytes and written into a different file, so no circularity arises.
Requiring the resolved target to equal the running script's resolved `__file__`
prevents a harness from attesting to bytes other than the ones executing.

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
| `stage_failed` | `failure_class`, `root_cause_class`, `remediation_disposition` |
| `stage_sealed` | `stage_disposition` |

`mode` is `CONTINUATION` or `CONTAINMENT`. `elapsed_ms` is a non-authoritative
diagnostic integer. `unequal_filenames[]` may contain only canonical candidate
filenames. `error_class` is exactly one `operator_error_class` value (§20.8) and
is never free-form text.

`stage_failed` (`PIC-6`) carries exactly three additional fields, each drawn
from an existing closed vocabulary: `failure_class` (§20.3), `root_cause_class`
(§20.1) and `remediation_disposition` (§20.4). No free-form text is permitted,
and no additional field may be added to it.

The three are not chosen independently. `failure_class` is observed from the
failure condition; `root_cause_class` and `remediation_disposition` are then
**derived from it by the exact tables of §19.1 and §19.2** (`PIC-CORR-2`,
`PIC-CORR-3`). No implementation may substitute another value.

```text
stage_failed is technical stage evidence.
It is NOT an episode invalidation.
```

Appending `stage_failed` never creates or appends `episode-invalidation.jsonl`,
and never implies that an invalidation occurred (§17.1).

The exact value domains of the common event fields are:

```text
stage:
GENERATE_A
GENERATE_B
COMPARE
VERIFY

generation_identity:
A
B
present only where applicable, and absent otherwise rather than null

schema_version:
mesc-p01-04d-execution-evidence/stage-event/v1

byte_equality:
EQUAL
UNEQUAL

stage_disposition:
exactly one value from the closed enumeration in §20.9

path_role:
exactly one value from the closed enumeration in §20.10

event_ordinal:
starts at 1
scoped independently to each physical JSONL file
increases by exactly one for every successfully appended complete canonical
event
never invented after malformed bytes
```

Because `event_ordinal` is per-file and one-based, the ordinal sequence of a
well-formed record is exactly `1 .. event_count`, which is what the terminal
manifest binds where countable (§15.4, §18).

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

```text
schema_version:
mesc-p01-04d-execution-evidence/invalidation-event/v1
```

This field set is exact and closed. No `identity_match` field and no stage-event
structure may be added to this record (`PIC-4`).

#### 15.3.1 When repository identity is material

Repository identity is material to `invalidate` exactly when:

```text
root_cause_class == CANONICAL_MAIN_MOVEMENT
or
failure_class == CANONICAL_MAIN_MISMATCH
```

For that case:

```text
repository observation:      MANDATORY
expected != observed:        MANDATORY
persisted under canonical_main_movement:
    expected_canonical_commit
    observed_canonical_commit
```

For every other invalidation cause the repository observation is not required
for invalidation evidence, and a matching observation is never persisted.

```text
canonical_main_movement when identity is not material:
ABSENT — not an empty object, not a null field
```

`canonical_main_movement` is therefore present exactly when the movement is real
and material, which is what "where applicable" means in the field list above.

#### 15.3.2 Coexisting stage failure and canonical-main movement

A non-main stage failure and canonical-main movement can both be true of the same
episode. They are recorded separately and neither displaces the other
(`PIC-CORR-6`):

```text
the stage failure:
preserved in stage_failed in its own stage journal, with the §19.1 triad

the canonical-main movement:
requires its OWN explicit invalidate record carrying canonical_main_movement

containment finalize:
may proceed only after that movement record satisfies PIC-3 (§5.2.1)
```

Materiality is evaluated per invalidation record, not per episode. An
invalidation record whose cause is not canonical-main movement therefore carries
no `canonical_main_movement` block even when main has in fact moved, and a
`finalize` retry will refuse until a movement record exists. Recording the
movement inside the non-main record instead is prohibited, because §15.3.1 binds
that block to the materiality of the record that carries it.

### 15.4 `episode-manifest.json`

```text
schema_version
episode_identity
episode_path_identity
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

```text
schema_version:
mesc-p01-04d-execution-evidence/episode-manifest/v1
```

This field set is exact and closed. It is closed at **seven** fields.
`episode_path_identity` was added by the P-A3 founder amendment (`PA3-AMD-2`),
and every earlier statement asserting a six-field manifest set is withdrawn.

```text
episode_path_identity
The digest of the episode directory's (st_dev, st_ino) pair, reduced through the
frozen canonical serializer (§16, §27), as measured at episode open and
re-confirmed at terminalization.
```

A verifier that recomputes the identity of the directory in which it found the
manifest MUST compare the result to this field, and MUST treat a mismatch as
terminal. The field binds the manifest to the directory object it was sealed in,
so a manifest read from anywhere else is detectably mislocated.

The `schema_version` literal above is **unchanged** by `PA3-AMD-2` and remains
`mesc-p01-04d-execution-evidence/episode-manifest/v1`. The seven-field set is
what that literal now denotes. A manifest carrying only the former six fields
fails the mandatory-field test of §18.8.3 and is TM-1.

```text
episode-manifest schema_version:
UNCHANGED — .../episode-manifest/v1

bumping it to v2 or any other value:
PROHIBITED WITHOUT A SEPARATE FOUNDER DISPOSITION
```

```text
repository-observation field in episode-manifest.json:
PROHIBITED
```

The pre-finalize observation is mandatory and non-durable (`PIC-3`). Where
canonical main has moved, the movement is recorded by the prior explicit
`invalidate` in `episode-invalidation.jsonl`, which the manifest then binds by
digest like any other record — so the movement remains bound at seal without the
manifest carrying an observation field of its own.

The terminal manifest must not embed its own SHA-256.

The manifest carries no `record_integrity` field of its own, and none is added
by `PIC-CORR-14`. `record_integrity` describes the bound evidence records only
(§20.5). Whether the terminal manifest itself is valid is decided entirely by
the TM-0 / TM-1 / TM-2 creation states of §18.8, which persist nothing.

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

Every timestamp field — `started_at`, `exited_at`, `recorded_at` and
`manifest_sealed_at` — uses one exact form:

```text
UTC RFC3339
YYYY-MM-DDTHH:MM:SS.ffffffZ
```

Timestamps are therefore strings, never numbers. This matters because the
canonical serializer rejects binary floating-point values outright, so an epoch
value carrying fractional seconds could not be serialized at all. For the same
reason `elapsed_ms` is an integer.

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

For `episode-manifest.json` the exclusive-creation rule is further governed by
§18.8 (`PIC-CORR-14`). An existing terminal-manifest path is validated read-only
and is never silently replaced, and neither a complete valid manifest nor a
partial or invalid one permits a mutating retry.

### 17.1 Invalidation ownership

```text
create or append episode-invalidation.jsonl:
EXPLICIT invalidate ONLY

automatic append by generate, compare, verify or finalize:
PROHIBITED
```

No command infers invalidation authority from a failure it observed. A stage
that fails records `stage_failed` in its own journal (§15.2) and seals; the
decision that the episode is invalid is a separate explicit act (`PIC-6`).

### 17.2 Episode progression after a failed or refused stage

When an opened stage seals `STAGE_REFUSED` or `STAGE_FAILED`:

```text
further generate, compare or verify continuation in that episode:
PROHIBITED

retry of the failed or refused scientific stage in the same episode:
PROHIBITED

fresh scientific attempt:
NEW EPISODE REQUIRED
```

A new episode is the only path to a fresh attempt at the scientific stage. This
preserves the append-only guarantee: an episode's stage journals record one
attempt each, so a sealed stage outcome can never be overwritten, retried into
ambiguity, or reinterpreted by a later success in the same episode.

Explicit `invalidate` is **not** universally mandatory before `finalize`
(`PIC-CORR-4`). The earlier wording that gave the permitted progression as
"explicit invalidate, then finalize" is corrected here, because read as a
requirement it would have made `EPISODE_REFUSED` and `EPISODE_FAILED`
unreachable — every failed episode would have become `EPISODE_INVALIDATED`, and
two of the five terminal dispositions would have been dead values.

```text
no separate pre-seal invalidation fact exists:
finalize MAY seal directly

terminal disposition then reachable as:
EPISODE_REFUSED or EPISODE_FAILED, by the §20.7 precedence

an explicit invalidation HAS been recorded:
EPISODE_INVALIDATED, unless evidence corruption takes higher precedence

canonical-main movement exists:
the PIC-3 explicit invalidate-before-finalize containment sequence of §5.2.1
REMAINS MANDATORY AND IS NOT WEAKENED
```

Invalidation stays a separate explicit act (§17.1). A stage failure is technical
stage evidence and does not by itself make the episode invalid, so sealing a
failed episode without an invalidation record is the correct default, not a
missing step.

The prohibitions above are triggered by a sealed `STAGE_REFUSED` or
`STAGE_FAILED` outcome. A stage that never sealed at all is governed separately
and at least as strictly: where required stage evidence can no longer be safely
appended, §18.5 prohibits every continuation immediately, without waiting for a
seal that will never occur.

## 18. Partial-write semantics and evidence-write outcomes

### 18.0 Definition — safely recordable

`safely recordable` is a defined term, never an undefined escape clause
(`PIC-CORR-7`). A required canonical event is **safely recordable** exactly
when:

```text
the required canonical event can be appended atomically and durably,
without altering any prior byte,
and without leaving malformed or partial bytes
```

Every clause in this contract that qualifies a rule with "safely recordable"
uses exactly this definition and no other.

### 18.1 The three evidence-write outcomes

For an opened stage whose journal already exists, an attempted required append
has exactly three outcomes. The three are disjoint and exhaustive.

| Case | Condition | Existing bytes | Controlling rule |
|---|---|---|---|
| **A** | append fails, no byte added or changed, a later required append is still safely recordable | syntactically `WELL_FORMED` | §18.2 |
| **B** | append leaves partial or malformed bytes | `MALFORMED_PRESERVED` | §18.3 |
| **C** | bytes remain syntactically well formed, but a required append is no longer safely recordable | syntactically well formed, lifecycle incomplete | §18.4 |

### 18.2 Case A — zero-byte write failure, later safe append possible

Conditions: the attempted required event append fails; no byte was added or
changed; the journal remains syntactically `WELL_FORMED`; and a subsequent
append can still be safely and durably completed (§18.0).

```text
failure_class:            EVIDENCE_WRITE_FAILURE
root_cause_class:         EVIDENCE_INTEGRITY_FAILURE
remediation_disposition:  NO_REMEDIATION_AUTHORIZED
```

Because durable recording remains possible, the stage records the failure and
seals it:

```text
stage_failed
-> stage_sealed

stage_disposition:
STAGE_FAILED
```

This is the case already required explicitly by §20.9 as a clean pre-child
`EVIDENCE_WRITE_FAILURE`.

### 18.3 Case B — partial or malformed bytes remain

If a canonical event append fails and malformed bytes remain:

```text
preserve the exact malformed bytes
do not truncate
do not repair
do not seek-and-patch
do not append a fabricated stage_failed event after malformed bytes
do not append a fabricated stage_sealed event after malformed bytes
do not fabricate a stage_disposition
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

### 18.4 Case C — structurally unsealed stage

Case C is an opened stage whose journal bytes remain syntactically well formed
but whose required remaining events are no longer safely recordable. Examples
include an evidence destination that becomes unwritable, storage that denies a
subsequent append, and a required event that cannot be durably appended even
though every prior byte remains intact.

```text
do NOT fabricate stage_failed
do NOT fabricate stage_sealed
do NOT repair the journal
do NOT backfill the journal later
```

The stage is then **STRUCTURALLY UNSEALED**.

```text
STRUCTURALLY UNSEALED is a structural condition.
It is NOT a new enumeration.
It is NOT a new enumeration value.
It is NOT a new durable field.
Nothing is written to record it.
```

A stage is structurally unsealed exactly when:

```text
stage_opened exists
and
the journal does not end in exactly one valid stage_sealed event
```

At `finalize`, a structurally unsealed opened stage **is by definition an
unresolved evidence-integrity corruption condition**, regardless of whether its
existing JSONL bytes parse correctly. Terminal-disposition precedence rank 1
therefore selects `EPISODE_EVIDENCE_CORRUPT` (§20.7).

```text
must NOT fall through to EPISODE_INVALIDATED:      PROHIBITED
must NOT fall through to EPISODE_REFUSED:          PROHIBITED
must NOT fall through to EPISODE_FAILED:           PROHIBITED
must NOT fall through to EPISODE_COMPLETE_EQUAL:   PROHIBITED
```

None of those four may be selected merely because the existing bytes parse
correctly. Syntactic record integrity and lifecycle completeness are separate
properties, and only the first is what `record_integrity` reports.

### 18.5 Continuation after structural unseal

Immediately after the harness detects that required stage evidence can no longer
be safely appended:

```text
generate:                              PROHIBITED
compare:                               PROHIBITED
verify:                                PROHIBITED
same-stage retry:                      PROHIBITED
any new scientific stage:              PROHIBITED
child launch:                          PROHIBITED
new protected-input access:            PROHIBITED
new protected-input hashing:           PROHIBITED
generation-workspace mutation:         PROHIBITED
automatic re-pin:                      PROHIBITED
journal repair:                        PROHIBITED
journal backfill after storage recovery: PROHIBITED
```

The episode enters evidence-preserving containment only. No new enumeration,
field or record is created to represent that containment fact.

### 18.6 Finalize after structural unseal

If `episode-manifest.json` does not yet exist and the evidence root later
permits the terminal manifest to be written, `finalize` may be invoked or
retried **only** as an evidence-preserving containment operation.

`finalize` must:

```text
not append to the structurally unsealed stage journal
not repair it
read and bind its exact existing bytes
compute its SHA-256 and byte size
record record_integrity = WELL_FORMED if those exact bytes are syntactically
    canonical and countable
record the actual event_count where countable
independently treat the absence of the required terminal stage_sealed event as
    an unresolved evidence-integrity corruption condition
select terminal_disposition = EPISODE_EVIDENCE_CORRUPT
```

The structural corruption condition is **not** encoded by falsely changing
`record_integrity` to `MALFORMED_PRESERVED`. `record_integrity` reports whether
the bytes are syntactically well formed; lifecycle completeness is reported by
the terminal disposition. Falsifying the first to express the second would
misdescribe the bytes the manifest binds.

If `finalize` itself cannot durably create a complete valid canonical
`episode-manifest.json`:

```text
valid manifest:            DOES NOT EXIST
terminal identity:         DOES NOT EXIST
success or adoption claim: PROHIBITED
scientific continuation:   PROHIBITED
```

Whether a later `finalize` retry is permitted at all depends on the exact
terminal-manifest creation state defined in §18.8 (`PIC-CORR-14`), not on
storage writability alone:

```text
TM-0 — the episode-manifest.json path is physically absent:
a later retry is PERMITTED, after storage becomes writable, as
evidence-preserving containment only

TM-1 — the path exists but its exact bytes are not a complete valid canonical
manifest, including a zero-byte path:
a later retry is PROHIBITED — terminalization has irrecoverably failed and the
exact existing bytes are preserved

TM-2 — a complete valid canonical manifest exists:
a later retry is PROHIBITED — post-seal immutability applies absolutely (§22)
```

After successful manifest creation, post-seal immutability applies absolutely
(§22), so no further `finalize` and no further mutation of that episode is
permitted.

### 18.7 General abrupt-stop rule

At `finalize`, **any** opened stage journal that does not end in exactly one
valid `stage_sealed` event is an unresolved evidence-integrity corruption
condition. This holds regardless of why the stage became unsealed, including:

```text
evidence destination failure
process termination
harness crash
abrupt host interruption
```

No causal event that was never durably recorded may be invented to explain the
gap. The observable structural incompleteness alone is sufficient to prevent
scientific success and to select `EPISODE_EVIDENCE_CORRUPT`.

### 18.8 Terminal-manifest creation semantics

Partial creation of the terminal manifest is defined here (`PIC-CORR-14`). The
physical **path state** of `episode-manifest.json` and the **validity** of its
bytes are distinct properties. Terminal authority follows validity, never mere
existence.

`episode-manifest.json` has exactly three creation states:

```text
TM-0   the path does not exist
TM-1   the path exists, but its exact bytes are NOT exactly one complete,
       canonical, schema-valid episode manifest
TM-2   the path exists, and its exact bytes ARE exactly one complete,
       canonical, schema-valid episode manifest
```

```text
TM-0, TM-1 and TM-2 are structural states.
They are NOT a new enumeration.
They are NOT new enumeration values.
They are NOT a new durable field.
Nothing is written to record which state holds.
```

The three states are mutually exclusive, exhaustive, observable and
deterministic. There is no fourth state.

#### 18.8.1 TM-0 — ABSENT

The filesystem path `episode-manifest.json` does not exist. No directory entry
exists at that path. This includes a `finalize` failure occurring before the
path is created at all.

```text
valid manifest:                           NO
canonical seal:                           NO
terminal identity:                        NO
terminal disposition durably established: NO
```

If storage later becomes usable, a later `finalize` retry MAY occur, but only
while all of the following hold:

```text
episode-manifest.json is still physically absent
no successful seal previously occurred
the retry remains evidence-preserving containment
no scientific continuation occurs
no stage journal is repaired or backfilled
all existing pre-finalize evidence is read-only
```

#### 18.8.2 TM-1 — PRESENT BUT INVALID OR INCOMPLETE

The filesystem path `episode-manifest.json` exists, but its exact bytes are not
exactly one complete, canonical, schema-valid episode manifest. This includes,
without limitation:

```text
zero-byte file
truncated bytes
partial JSON
malformed JSON
syntactically valid JSON missing mandatory fields
syntactically valid but noncanonical JSON
wrong schema_version
incomplete records[] binding
absent terminal_disposition
any bytes failing exact canonical-manifest validation
```

A zero-byte file that physically exists is TM-1, never TM-0.

The exact existing bytes are preserved:

```text
truncate:                          PROHIBITED
delete:                            PROHIBITED
overwrite:                         PROHIBITED
replace:                           PROHIBITED
rename:                            PROHIBITED
repair:                            PROHIBITED
seek-and-patch:                    PROHIBITED
append to complete it:             PROHIBITED
re-run manifest creation:          PROHIBITED
create a second terminal manifest: PROHIBITED
```

```text
finalize retry:                PROHIBITED
canonical seal:                FAILED / NOT ESTABLISHED
terminal identity:             NOT ESTABLISHED
terminal_disposition:          NOT DURABLY ESTABLISHED
scientific success:            PROHIBITED
scientific continuation:       PROHIBITED
generate:                      PROHIBITED
compare:                       PROHIBITED
verify:                        PROHIBITED
protected-input access:        PROHIBITED
protected-input hashing:       PROHIBITED
workspace mutation:            PROHIBITED
```

The episode is an irrecoverably failed terminalization attempt. That phrase is a
governance condition only: no enumeration, enumeration value, field, evidence
record, marker or sidecar is created for it.

Any fresh scientific attempt requires a **separate new episode**, and that new
episode remains subject to every existing execution and governance
authorization. Nothing here creates or authorizes such an episode.

##### 18.8.2.1 Corruption distinction

Under TM-1 the episode must be treated as unusable and evidence-corrupt for any
scientific or adoption claim.

It must **not** be claimed that `EPISODE_EVIDENCE_CORRUPT` was durably recorded
as `terminal_disposition`. That value exists only inside a complete valid
canonical terminal manifest.

```text
durable terminal_disposition:  ABSENT
terminal identity:             ABSENT
canonical seal:                ABSENT
```

This distinction is mandatory. Unusability is a governance conclusion drawn from
the observable TM-1 state; it is not a durably recorded terminal disposition.

#### 18.8.3 TM-2 — COMPLETE VALID CANONICAL MANIFEST

`episode-manifest.json` exists and its exact bytes satisfy all of:

```text
complete file
UTF-8
canonical JSON
exact episode-manifest schema_version
all mandatory fields
complete required record binding
valid record metadata
exactly one valid terminal_disposition
no extra prohibited fields
canonical serializer round-trip and exact-byte validation as required by §16
```

```text
canonical seal:         ESTABLISHED
terminal identity:      ESTABLISHED
post-seal immutability: ABSOLUTE
finalize retry:         PROHIBITED
rewrite:                PROHIBITED
```

Terminal identity is exactly the SHA-256 of the complete valid exact manifest
bytes together with the byte size of those same exact bytes.

#### 18.8.4 Manifest path existence is not terminal identity

Terminal identity exists **if and only if** `episode-manifest.json` is TM-2.
Filesystem path existence alone is insufficient.

```text
TM-0:  no terminal identity
TM-1:  no terminal identity
TM-2:  terminal identity exists
```

Computing or reporting a terminal identity over invalid, partial or incomplete
manifest bytes is prohibited.

#### 18.8.5 Crash after a complete valid write

If the complete valid canonical TM-2 bytes were durably created and the harness
then crashed or terminated before reporting the terminal identity, the episode
is still canonically sealed.

Terminal identity is a deterministic derived property of the exact valid
manifest bytes. It may be recomputed **read-only** from those exact bytes.

```text
rewrite manifest:               PROHIBITED
rerun finalize as a mutation:   PROHIBITED
change terminal disposition:    PROHIBITED
create another manifest:        PROHIBITED
```

A process failing to report the identity does not undo an already-valid terminal
seal.

#### 18.8.6 Crash before a complete valid write

If a directory entry exists but the bytes are not TM-2, §18.8.2 controls.

Intent is never inferred from how many bytes the harness expected to write. The
observed exact bytes and their schema and canonical validity control.

#### 18.8.7 Exclusive creation and finalize entry

Exclusive creation is preserved (§17). The implementation must attempt creation
in a way that never silently replaces an existing path.

On entry to `finalize`, if `episode-manifest.json` exists:

```text
validate it read-only

TM-2:
the episode is already sealed — mutation PROHIBITED

TM-1:
terminalization has irrecoverably failed — mutation PROHIBITED
```

Neither branch is a permitted `finalize` retry. Both are fail-closed recognition
of existing state.

#### 18.8.8 Finalize remains the last mutation

`finalize` is the last P-A mutation to an execution episode (§22) in every
state.

```text
TM-1:
the partial or invalid durable creation attempt is itself the last mutation to
that episode — no cleanup mutation follows

TM-2:
successful manifest creation is the last mutation
```

#### 18.8.9 Interaction with structural unseal

`PIC-CORR-7` is preserved. A structurally unsealed stage (§18.4) ordinarily
causes a valid TM-2 manifest, where creation succeeds, to carry
`EPISODE_EVIDENCE_CORRUPT` as `terminal_disposition`.

If terminal-manifest creation itself reaches only TM-1, no `terminal_disposition`
is durably established at all. `EPISODE_EVIDENCE_CORRUPT` must not be claimed to
have been written. The episode remains unusable and unsealed.

#### 18.8.10 Interaction with canonical-main movement

Where canonical-main movement requires an explicit `invalidate` before
`finalize` (§5.2.1, `PIC-3`), that requirement remains in force.

If the movement record was validly persisted and terminal-manifest creation then
reaches TM-1, the invalidation evidence remains preserved, but no canonical
terminal disposition and no terminal identity exist.

```text
fall back to EPISODE_INVALIDATED without a valid TM-2 manifest carrying it:
PROHIBITED
```

#### 18.8.11 No `record_integrity` for the manifest

`WELL_FORMED` and `MALFORMED_PRESERVED` are not applied as a manifest field.
`record_integrity` remains defined only for the already authorized bound evidence
records (§15.4, §20.5).

Manifest validity is determined entirely by the TM-0 / TM-1 / TM-2 semantics of
this section, without adding any persisted field or enumeration.

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

### 19.1 Deterministic failure triad mapping

`failure_class`, `root_cause_class` and `remediation_disposition` are not three
independent judgements. `failure_class` is observed from the failure condition,
and the other two are **derived from it by the exact table below**
(`PIC-CORR-2`). No implementation may substitute another value.

Unless `failure_class` is `CHILD_NONZERO_EXIT`, which is governed by §19.2:

| `failure_class` | `root_cause_class` | `remediation_disposition` |
|---|---|---|
| `ARGUMENT_REFUSAL` | `EVIDENCE_CONFIGURATION_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `CANONICAL_MAIN_MISMATCH` | `CANONICAL_MAIN_MOVEMENT` | `FOUNDER_DISPOSITION_REQUIRED` |
| `PATH_SEPARATION_REFUSAL` | `PATH_SAFETY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `REPARSE_POINT_REFUSAL` | `PATH_SAFETY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `EPISODE_PATH_IDENTITY_DRIFT` | `PATH_SAFETY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `HARNESS_IDENTITY_MISMATCH` | `HARNESS_IDENTITY_MISMATCH` | `FOUNDER_DISPOSITION_REQUIRED` |
| `OPERATOR_IDENTITY_MISMATCH` | `OPERATOR_IDENTITY_MISMATCH` | `FOUNDER_DISPOSITION_REQUIRED` |
| `RUNTIME_IDENTITY_MISMATCH` | `RUNTIME_IDENTITY_MISMATCH` | `FOUNDER_DISPOSITION_REQUIRED` |
| `INPUT_HASH_FAILURE` | `INPUT_IDENTITY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `INPUT_IDENTITY_MISMATCH` | `INPUT_IDENTITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `CHILD_LAUNCH_FAILURE` | `CHILD_PROCESS_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `CHILD_NONZERO_EXIT` | see §19.2 | see §19.2 |
| `OUTPUT_INVENTORY_MISMATCH` | `OUTPUT_INVENTORY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `OUTPUT_HASH_FAILURE` | `EVIDENCE_INTEGRITY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `BYTE_INEQUALITY` | `BYTE_INEQUALITY` | `FOUNDER_DISPOSITION_REQUIRED` |
| `COMPARE_CONTRADICTION` | `EVIDENCE_INTEGRITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `FINGERPRINT_MISMATCH` | `FINGERPRINT_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `EVIDENCE_WRITE_FAILURE` | `EVIDENCE_INTEGRITY_FAILURE` | `NO_REMEDIATION_AUTHORIZED` |
| `EVIDENCE_MALFORMED_PRESERVED` | `EVIDENCE_INTEGRITY_FAILURE` | `NO_REMEDIATION_AUTHORIZED` |
| `VERIFY_FAILURE` | `EVIDENCE_INTEGRITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `UNCLASSIFIED` | `UNDETERMINED` | `FOUNDER_DISPOSITION_REQUIRED` |

The table is total over the twenty-one `failure_class` values of §20.3.

```text
mapping scope:
wherever these closed fields coexist, including stage_failed (§15.2) and
episode invalidation evidence (§15.3)

substitution of another root cause or remediation value:
PROHIBITED
```

`LATER_STAGE_GOVERNANCE_REQUIRED` is **never** emitted by a P-A2 `stage_failed`
event. It remains reserved for a separately governed later stage that discovers a
fact after the P-A episode has been sealed (§26, `R2`).

### 19.2 `CHILD_NONZERO_EXIT` derivation

When `failure_class` is `CHILD_NONZERO_EXIT`, the other two values derive
exactly from the `operator_error_class` already recorded on `child_exited`
(§20.8), so the classification of a child failure has one source
(`PIC-CORR-3`).

| `operator_error_class` | `root_cause_class` | `remediation_disposition` |
|---|---|---|
| `INPUT_IDENTITY_ERROR` | `INPUT_IDENTITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `INPUT_SCHEMA_ERROR` | `INPUT_SCHEMA_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `WORKSPACE_SAFETY_ERROR` | `WORKSPACE_STATE_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `GENERATION_ERROR` | `CHILD_PROCESS_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `INVENTORY_ERROR` | `OUTPUT_INVENTORY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `BYTE_EQUALITY_ERROR` | `BYTE_INEQUALITY` | `FOUNDER_DISPOSITION_REQUIRED` |
| `FINGERPRINT_ERROR` | `FINGERPRINT_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `METADATA_ERROR` | `EVIDENCE_INTEGRITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `EVIDENCE_CONFIGURATION_ERROR` | `EVIDENCE_CONFIGURATION_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `UNCLASSIFIED` | `UNDETERMINED` | `FOUNDER_DISPOSITION_REQUIRED` |
| `NO_ERROR` | `UNDETERMINED` | `FOUNDER_DISPOSITION_REQUIRED` |

The final row is a **contract contradiction**, not a normal outcome: a child that
exited nonzero cannot also carry `NO_ERROR`, which §20.8 reserves for exit code
zero.

```text
CHILD_NONZERO_EXIT with operator_error_class NO_ERROR:
CONTRACT CONTRADICTION

derived root_cause_class:
UNDETERMINED

derived remediation_disposition:
FOUNDER_DISPOSITION_REQUIRED

harness behaviour:
FAIL CLOSED
```

The table is total over the eleven `operator_error_class` values of §20.8, so
every nonzero child exit yields exactly one triad.

### 19.3 Derivation and durability are separate obligations

Deriving a triad is not the same act as persisting one (`PIC-CORR-10`). The
contract may deterministically derive `failure_class`, `root_cause_class` and
`remediation_disposition` without thereby authorizing or requiring a fabricated
durable record.

A triad is persisted only when all three hold:

```text
an authorized record schema contains those fields
and the authorized destination exists
and the event is safely recordable (§18.0)
```

Where any of the three fails, the derivation remains semantically true and
nothing is written. No destination is invented to receive it (§12.1).

```text
PRE-STAGE (§21.1):
the triad may be semantically known,
but no stage journal is fabricated to carry it

MALFORMED_PRESERVED (§18.3):
no later triad event is fabricated into malformed bytes

structurally unsealed stage, §18.4 case C:
the triad may be semantically EVIDENCE_WRITE_FAILURE /
EVIDENCE_INTEGRITY_FAILURE / NO_REMEDIATION_AUTHORIZED,
but if the journal cannot accept an event, no stage_failed is fabricated
```

In every one of those cases the terminal rules still apply: a structurally
unsealed opened stage selects `EPISODE_EVIDENCE_CORRUPT` at seal (§18.4, §18.7,
§20.7), and a PRE-STAGE refusal produces no stage evidence at all (§21.1). The
absence of a durable triad is therefore never an absence of governance.

This is the same separation §5 states for repository-identity observation, applied
to failure classification.

## 20. Closed vocabularies

Values outside these enumerations are rejected. All values are case-sensitive and
exact. No arbitrary extension is permitted without a founder disposition.

```text
closed enumerations:
10

total closed enumeration values:
78

root_cause_class           15
causal_stage                8
failure_class              21
remediation_disposition     4
record_integrity            2
comparison_disposition      4
terminal_disposition        5
operator_error_class       11
stage_disposition           3
path_role                   5
```

`stage_disposition` (`PIC-7`) and `path_role` (`PIC-8`) were added by the P-A1
implementation clarification. Every earlier statement asserting eight closed
enumerations or sixty-nine closed values is withdrawn.

`failure_class` was extended from twenty values to twenty-one by the P-A3 founder
amendment (`PA3-AMD-1`, §20.3). Every earlier statement asserting seventy-seven
closed values, or twenty `failure_class` values, is withdrawn. The enumeration
count is unchanged at ten: no enumeration was added or removed.

This count is the **named closed-enumeration ledger** (`PIC-CORR-6`). It states
how many enumerations §20 names and how many values they hold. It is not a claim
that no other constrained field domain exists.

```text
the 10 / 78 arithmetic covers:
the named enumerations of §20.1 through §20.10 only

other fixed inline domains, fixed but NOT counted here:
mode                  CONTINUATION, CONTAINMENT
stage                 GENERATE_A, GENERATE_B, COMPARE, VERIFY
generation_identity   A, B
byte_equality         EQUAL, UNEQUAL
```

Those inline domains are fixed closed domains, exhaustively specified in §15.2,
and values outside them are rejected exactly as here. They are excluded from the
10 / 78 arithmetic solely because that ledger counts §20's named enumerations.

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
EPISODE_PATH_IDENTITY_DRIFT
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

`EPISODE_PATH_IDENTITY_DRIFT` was admitted by the P-A3 founder amendment
(`PA3-AMD-1`). Its triad is bound normatively here, and identically in the §19.1
table:

```text
EPISODE_PATH_IDENTITY_DRIFT -> PATH_SAFETY_FAILURE / FOUNDER_DISPOSITION_REQUIRED
```

A real-directory-for-real-directory substitution passes both reparse and
containment, so no existing class describes it, and a detected in-flight
substitution evidences a host-level adversary, which no fresh episode on the same
host remediates.

The class is reachable: it is durably recordable through the `invalidate` command
(§4), whose record carries a `failure_class` value (§15.3), and it is emitted as
a closed-vocabulary stderr token by the refusing command. Admitting it changes no
other enumeration.

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
   or any unresolved evidence-integrity corruption exists,
   INCLUDING any opened stage that is structurally unsealed (§18.4):
   EPISODE_EVIDENCE_CORRUPT

2. otherwise, explicit invalidation:
   EPISODE_INVALIDATED

3. otherwise, refusal after successful episode open:
   EPISODE_REFUSED

4. otherwise, terminal failure:
   EPISODE_FAILED

5. otherwise, fully complete success:
   EPISODE_COMPLETE_EQUAL
```

`EPISODE_EVIDENCE_CORRUPT` takes precedence over `EPISODE_INVALIDATED`,
`EPISODE_FAILED` and `EPISODE_REFUSED`.

Rank 1 is satisfied by either of two independent conditions: a bound record
whose bytes are `MALFORMED_PRESERVED`, or a lifecycle-incomplete opened stage
whose bytes are syntactically well formed (§18.4, §18.7). The second condition
is evaluated on structure, not on parse success, so a structurally unsealed
stage never falls through to ranks 2 through 5 merely because its existing
bytes parse correctly. This adds no terminal-disposition value; all five
remain reachable, and §13.1, §17.2 and §18.6 record the paths to each.

Precedence governs the terminal label only. The underlying causal facts remain
independently recorded in the structured failure and invalidation evidence, so an
evidence-corrupt seal never erases the invalidation, refusal or failure that
caused it.

Precedence selects the value that a **complete valid canonical terminal
manifest** carries. A `terminal_disposition` is durably established only inside a
TM-2 manifest (§18.8). Where terminal-manifest creation reaches only TM-0 or
TM-1, no `terminal_disposition` is durably established at all, and no value of
this enumeration — `EPISODE_EVIDENCE_CORRUPT` and `EPISODE_INVALIDATED`
included — may be claimed to have been recorded (`PIC-CORR-14`).

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
NO_ERROR

unmatched nonzero child failure:
UNCLASSIFIED

argparse or usage exit code 2:
UNCLASSIFIED

raw exception class text:
PROHIBITED

raw exception message:
PROHIBITED

value outside this enumeration:
REJECTED
```

`child_exited.error_class` carries exactly one of these values. No free-form error
field exists, and this classification never carries operator message text.

#### 20.8.1 Exact allowlist and mapping

The allowlisted exception-class tokens and their durable mappings are exactly
these ten (`PIC-9`):

| Allowlisted token | `operator_error_class` |
|-------------------|------------------------|
| `FormalInputIdentityError` | `INPUT_IDENTITY_ERROR` |
| `FormalInputSchemaError` | `INPUT_SCHEMA_ERROR` |
| `FormalLabelJoinError` | `INPUT_SCHEMA_ERROR` |
| `FormalWorkspaceSafetyError` | `WORKSPACE_SAFETY_ERROR` |
| `FormalGenerationError` | `GENERATION_ERROR` |
| `FormalInventoryError` | `INVENTORY_ERROR` |
| `FormalByteEqualityError` | `BYTE_EQUALITY_ERROR` |
| `FormalFingerprintError` | `FINGERPRINT_ERROR` |
| `FormalMetadataError` | `METADATA_ERROR` |
| `FormalEvidenceConfigurationError` | `EVIDENCE_CONFIGURATION_ERROR` |

```text
allowlisted tokens:
10

any other token:
NOT ALLOWLISTED -> UNCLASSIFIED
```

The mapping is many-to-one by design: `FormalLabelJoinError` and
`FormalInputSchemaError` both denote a formal input that did not satisfy its
contract, and both map to `INPUT_SCHEMA_ERROR`.

#### 20.8.2 Extraction mechanism

```text
1. capture child stdout and stderr as bytes in memory
2. compute the required SHA-256 and byte sizes from those exact bytes
3. never persist the raw bytes
4. inspect only the final non-empty traceback exception line, in memory
5. extract only an exact ASCII class token anchored to the canonical formal
   exception module/class form
6. compare against the exact allowlist in §20.8.1
7. discard raw stderr once the evidence fields have been derived
8. never persist raw exception class text
9. never persist raw exception message
```

Anchoring to the final non-empty traceback exception line, in the canonical
module-and-class form, is required rather than stylistic: typed operator errors
embed protected identifiers in their messages (§19), so an unanchored scan of
the whole stream could match a token echoed inside protected text and
misclassify the failure.

The extraction operates on **bytes held in memory**, and the full stream need
never be successfully decoded (`PIC-CORR-6`). Decoding the whole stderr is not a
precondition of classification, and a stream that cannot be decoded is not an
error condition — it is simply unclassifiable.

#### 20.8.2.1 Exact logical-line algorithm

The byte-level scan is fixed exactly, so that no implementation choice can
change a durable classification (`PIC-CORR-8`). stderr remains exact bytes in
memory throughout, and no full Unicode decode is required.

```text
1. split the exact stderr bytes ONLY on b"\n"

2. for each resulting segment, remove exactly ONE trailing b"\r",
   if and only if it is the final byte of that segment

3. a bare b"\r" that is not immediately before a b"\n" is NOT a line separator

4. after that one-byte CR normalization, discard zero-length logical lines
   when selecting the final non-empty line

5. inspect the final non-empty normalized segment only
```

Because step `2` removes exactly one trailing carriage return and step `3`
refuses to treat any other carriage return as a separator, LF and CRLF
traceback output produce **identical** classifications for identical logical
content. That equivalence is required, not incidental: the operator runs on
hosts with differing newline conventions, and a durable evidence value may not
depend on which one produced the stream.

#### 20.8.2.2 Exact module anchor and token syntax

The canonical formal exception module literal is exactly (`PIC-CORR-13`):

```text
medscale.mesc._formal_split_v1
```

The recognized prefix, required at **byte offset 0** of the inspected logical
line, is exactly:

```text
b"medscale.mesc._formal_split_v1."
```

Immediately after that prefix there must appear exactly one allowlisted ASCII
formal exception class token from §20.8.1. Immediately after the token there
must appear either:

```text
end of logical line
or
one ASCII colon byte b":"
```

If the colon is present, every following byte is untrusted exception-message
content:

```text
ignored for classification
need not decode
NEVER persisted
```

This is the only accepted module prefix for the `PIC-9` class-token extraction
mechanism. The literal is a classification constant carried in production as an
exact string; production still must not import the formal module to perform the
classification (§27).

#### 20.8.2.3 Fail-closed cases

Every one of the following resolves to `UNCLASSIFIED`:

```text
empty stderr
no final non-empty logical line
nonmatching module prefix
unexpected exception module
class token not exactly allowlisted
non-ASCII bytes inside the required module/token syntax
malformed required syntax
message text that merely contains an allowlisted token away from byte offset 0
bare-CR layout that does not satisfy the exact syntax after the defined scan
```

`UNCLASSIFIED` is a complete and correct answer in each case. Nothing is retried,
nothing is guessed from elsewhere in the stream, and no raw stderr, no raw class
text and no raw message is persisted under any of them.

```text
production import of the formal split or formal generation modules
to perform this mapping:
PROHIBITED
```

The allowlist is therefore carried in production as exact string literals (§27).

### 20.9 `stage_disposition`

```text
STAGE_COMPLETE
STAGE_REFUSED
STAGE_FAILED
```

The boundary is decided by an exact three-way test, not by judgement
(`PIC-CORR-1`).

```text
STAGE_COMPLETE
the opened stage completed every required operation successfully.

STAGE_REFUSED
ALL THREE conditions hold:
1. stage_opened was durably appended;
2. child_started does NOT exist;
3. failure_class is exactly one of:
       CANONICAL_MAIN_MISMATCH
       HARNESS_IDENTITY_MISMATCH
       OPERATOR_IDENTITY_MISMATCH
       RUNTIME_IDENTITY_MISMATCH
       INPUT_IDENTITY_MISMATCH

STAGE_FAILED
every other safely recordable failure after stage_opened.
```

```text
failure_class values that may produce STAGE_REFUSED:
exactly the five listed above

any other failure_class producing STAGE_REFUSED:
PROHIBITED
```

The earlier definition of `STAGE_REFUSED` as a gate holding "before child
execution or completion" is **withdrawn**. It admitted a post-launch reading and
left post-open pre-child harness-operation failures classifiable either way. The
three-condition test above is total and disjoint: `STAGE_REFUSED` requires the
absence of `child_started` **and** membership in the closed five-value set, so
every other opened-stage failure is `STAGE_FAILED` by construction.

Required consequences, stated explicitly so no implementation may diverge:

```text
INPUT_HASH_FAILURE                                   -> STAGE_FAILED
EVIDENCE_WRITE_FAILURE, journal still WELL_FORMED    -> STAGE_FAILED
CHILD_LAUNCH_FAILURE                                 -> STAGE_FAILED
CHILD_NONZERO_EXIT                                   -> STAGE_FAILED
OUTPUT_INVENTORY_MISMATCH                            -> STAGE_FAILED
OUTPUT_HASH_FAILURE                                  -> STAGE_FAILED
BYTE_INEQUALITY                                      -> STAGE_FAILED
COMPARE_CONTRADICTION                                -> STAGE_FAILED
FINGERPRINT_MISMATCH                                 -> STAGE_FAILED
VERIFY_FAILURE                                       -> STAGE_FAILED
UNCLASSIFIED                                         -> STAGE_FAILED
```

`INPUT_HASH_FAILURE` and a clean pre-child `EVIDENCE_WRITE_FAILURE` are
`STAGE_FAILED` even though they occur before the child acts, because they are
harness operations that failed rather than gates that held. Gate refusals are
exactly the five identity and canonical-main conditions.

`stage_sealed.stage_disposition` carries exactly one value from this set
(`PIC-7`).

Both `STAGE_REFUSED` and `STAGE_FAILED` are opened stages with durable evidence,
which is what separates them from a PRE-STAGE refusal (§21.1).

"Safely recordable" in this section carries exactly the §18.0 definition: the
required canonical event can be appended atomically and durably, without
altering any prior byte and without leaving malformed or partial bytes. It is
never an undefined escape clause.

Where a failed append leaves malformed bytes, the `MALFORMED_PRESERVED` rules of
§18.3 control absolutely: no `stage_failed` and no `stage_sealed` may be
fabricated after malformed bytes merely to complete the lifecycle, and the stage
therefore carries no `stage_disposition` at all.

Where the existing bytes remain well formed but a required append is no longer
safely recordable, §18.4 controls: nothing is fabricated, the stage is
structurally unsealed, it likewise carries no `stage_disposition`, and the
episode can only reach `EPISODE_EVIDENCE_CORRUPT` at seal (§18.6, §20.7). The
three cases of §18.1 are disjoint and exhaustive, so every opened stage has
exactly one outcome: `STAGE_COMPLETE`, `STAGE_REFUSED`, `STAGE_FAILED`, or no
`stage_disposition` at all under §18.3 or §18.4.

### 20.10 `path_role`

```text
FORMAL_INPUT_ORDERED_EXAMPLE_REGISTRY
FORMAL_INPUT_SOURCE_DOCUMENT_REGISTRY
FORMAL_INPUT_TRANSFORMED_DATASET_IDENTITY
FORMAL_INPUT_SOURCE_RECORDS
FORMAL_INPUT_DECISION_RECORD
```

`path_role` carries semantic role only (`PIC-8`).

```text
absolute path:                             PROHIBITED
relative path:                             PROHIBITED
filename derived from a local location:    PROHIBITED
username:                                  PROHIBITED
hostname:                                  PROHIBITED
protected identifier:                      PROHIBITED
```

The five values correspond one-to-one with the five logical input surfaces of §9.
The role is what the input *is* to the formal execution, never where it was read
from, so `path_role` can be persisted safely while the location it describes
cannot.

## 21. Episode lifecycle and failure ordering

`generate`, `compare` and `verify` follow one fixed fail-closed order in two
explicit phases (`PIC-5`). The evidence boundary is `stage_opened`.

### 21.1 PRE-STAGE

```text
1. validate harness arguments
2. validate the external evidence location
3. verify path separation and reparse safety
4. verify the episode exists and episode-core agreement
```

A failure during PRE-STAGE:

```text
is a harness or process refusal
does not create a stage journal
does not fabricate a stage
does not imply automatic invalidation
```

PRE-STAGE runs before any stage journal exists, so it produces no stage
evidence. That is correct, not a gap: the closed inventory (§12.1) offers no
durable destination before `stage_opened`, and fabricating one would violate both
§12.1 and the prohibition on representing a stage that never executed
(§13, `PA1-FD-13`).

A PRE-STAGE refusal that the operator judges to invalidate the episode is
recorded by an explicit `invalidate`, with `causal_stage` set to `PREFLIGHT`
(§20.2) — never by the refusing command itself (§17.1).

### 21.2 OPENED STAGE

After PRE-STAGE succeeds:

```text
5.  exclusively create the appropriate stage journal
6.  append stage_opened
7.  observe canonical repository identity and append
    repository_identity_observed
8.  verify harness, operator and runtime identities
9.  hash permitted inputs, digests and sizes only
10. launch exactly one child process
11. append child completion
12. hash completed outputs, or derive the comparison, where applicable
13. append stage_sealed
```

The second repository-identity observation required immediately before a child
launch (§5) occurs between steps `9` and `10` and is durable, because the stage
journal already exists by then.

After `stage_opened` has been durably appended, every subsequent failure —
before or after child launch — that remains **safely recordable** (§18.0) is
represented by `stage_failed` followed by `stage_sealed`, with the applicable
`stage_disposition` (§15.2, §20.9).

If durable append is no longer safely possible, `PIC-CORR-7` controls (§18):

```text
no event is fabricated
the stage remains structurally unsealed
scientific continuation stops
terminal finalization selects EPISODE_EVIDENCE_CORRUPT
```

The earlier unqualified claim that every post-`stage_opened` failure is durably
representable is **withdrawn**. It was false for a stage whose evidence
destination stops accepting appends, and it left that reachable state without a
defined outcome. §18.1 now partitions the three evidence-write outcomes, and
§18.0 defines "safely recordable" exactly, so the qualifier is a defined term
rather than an escape clause.

#### 21.2.1 Failure-event ordering

For any safely recordable (§18.0) opened-stage refusal or failure:

```text
stage_failed MUST precede stage_sealed
```

The exact orderings are:

```text
opened-stage refusal or failure before child launch:
stage_failed
-> stage_sealed

child launch failure (process creation itself fails):
stage_failed
-> stage_sealed
with NO child_started and NO child_exited

child nonzero exit:
child_started
-> child_exited
-> stage_failed
-> stage_sealed

post-child integrity failure:
child_exited
-> any FULLY DERIVABLE outputs_hashed / comparison_derived event
-> stage_failed
-> stage_sealed

outputs or comparison not fully derivable:
child_exited
-> omit those events entirely
-> stage_failed
-> stage_sealed
```

The child's outcome is recorded first and unconditionally; a later harness-side
failure is a separate appended event and never erases what preceded it. A
partially derived `outputs_hashed` or `comparison_derived` event is never
emitted — `outputs_hashed` requires exactly seven entries (§15.2) and
`comparison_derived` requires a complete seven-file equality ledger (§11), so an
incomplete derivation is an omission, never a truncated event.

##### 21.2.1.1 `CHILD_LAUNCH_FAILURE` lifecycle

If process creation itself fails, no child process ever existed, and nothing may
represent one (`PIC-CORR-9`):

```text
child process:  DOES NOT EXIST
child_started:  MUST BE ABSENT
child_exited:   MUST BE ABSENT
pid:            MUST NOT BE FABRICATED
started_at:     MUST NOT BE FABRICATED
ended_at:       MUST NOT BE FABRICATED AS CHILD EVIDENCE
```

The classification is fixed:

```text
failure_class:            CHILD_LAUNCH_FAILURE
root_cause_class:         CHILD_PROCESS_FAILURE
remediation_disposition:  NEW_EPISODE_REQUIRED
```

If the journal remains safely recordable (§18.0):

```text
stage_failed
-> stage_sealed

stage_disposition:
STAGE_FAILED
```

If the evidence cannot safely be appended, `PIC-CORR-7` controls (§18.4): no
event is fabricated and the stage is structurally unsealed. Either way the
absent child is represented by absence, never by a placeholder, a null or an
invented identifier — the same rule §15.2 applies to `generation_identity`,
which is absent rather than null where it does not apply.

If journal bytes become malformed at any point:

```text
preserve the exact malformed bytes
do not fabricate any later event
do not fabricate stage_failed
do not fabricate stage_sealed
```

§18 controls that case absolutely, and the stage carries no `stage_disposition`.

### 21.3 The evidence boundary

```text
Evidence exists before the child once stage_opened has been durably appended.
```

```text
claim that failures before stage creation are stage evidence:
WITHDRAWN
```

A failure after child creation records the child's outcome first and
unconditionally; any later harness-side failure is a separate appended event and
never erases what preceded it.

The boundary is what makes the two phases meaningful. PRE-STAGE failures are
refusals of a stage that never opened and carry no stage evidence. OPENED STAGE
failures carry it whenever the required event is safely recordable (§18.0);
where it is not, §18.4 governs and the stage is structurally unsealed rather
than falsely represented.

## 22. Terminal identity and sealing

```text
stable terminal evidence identity exists only after finalize has durably created
a TM-2 terminal manifest (§18.8)
```

```text
terminal evidence identity:
SHA-256 plus byte size of the COMPLETE VALID exact bytes of
episode-manifest.json

terminal identity exists:
IF AND ONLY IF episode-manifest.json is TM-2
```

Filesystem path existence alone is insufficient (`PIC-CORR-14`).

```text
TM-0 — path absent:                       no terminal identity
TM-1 — path present, bytes not valid:     no terminal identity
TM-2 — complete valid canonical manifest: terminal identity exists
```

Computing or reporting a terminal identity over invalid, partial or incomplete
manifest bytes is prohibited.

The manifest binds every evidence record present at seal by filename, SHA-256,
byte size, `record_integrity` and `event_count` where countable.

```text
FINALIZE IS THE LAST P-A MUTATION TO AN EXECUTION EPISODE.
```

After successful manifest creation, no existing episode file may be rewritten, no
journal may be appended, no invalidation record may be appended, no file may be
deleted and no new file may be created inside that sealed episode.

`record_integrity` in the manifest reports one property only: whether the bound
bytes are syntactically well formed. It never encodes lifecycle completeness, so
a structurally unsealed stage journal whose bytes parse correctly is bound as
`WELL_FORMED` with its actual `event_count`, while the missing terminal
`stage_sealed` event independently selects `EPISODE_EVIDENCE_CORRUPT` (§18.6,
§18.7, §20.7).

```text
finalize retry while episode-manifest.json is TM-0:
PERMITTED — evidence-preserving containment only

finalize retry while episode-manifest.json is TM-1:
PROHIBITED — terminalization has irrecoverably failed and the exact existing
bytes are preserved

finalize retry while episode-manifest.json is TM-2:
PROHIBITED — post-seal immutability is absolute
```

The retry condition is the physical absence of the path, not the mere absence of
a valid seal. A partial, truncated, malformed, schema-invalid or zero-byte
`episode-manifest.json` that physically exists is TM-1, and no retry, repair,
truncation, deletion or overwrite of it is permitted (§18.8.2).

The terminal identity cannot be written inside the manifest it hashes. It is
emitted by the harness at finalize and recorded externally, in the build report
and in the independent review record. This is the same constraint MODEL A′
governs at the scale of a canonical merge.

If the complete valid canonical manifest bytes were durably created and the
harness then crashed before emitting that identity, the episode remains
canonically sealed and the identity may be recomputed read-only from those exact
bytes (§18.8.5). Failure to report an identity never undoes an established seal,
and never authorizes rewriting the manifest, rerunning `finalize` as a mutation,
changing the terminal disposition or creating a second manifest.

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

`resolve_repository_commit` is the **only** formal import permitted at test
scope. The permission is not broadened:

```text
make_environment:      NOT PERMITTED
SYNTHETIC_COMMIT:      NOT PERMITTED
any other helper from a frozen formal test:  NOT PERMITTED
```

`tests/test_mesc_p01_04d_evidence_harness.py` constructs its own synthetic
repositories and fixture inputs inside itself. Reusing a frozen formal test's
helpers would couple the harness qualification to test internals that the frozen
paths may not change to accommodate, and would quietly widen an import boundary
that was granted for one narrow oracle.

Production carries the five logical input surfaces (§9), the seven candidate
filenames (§10), the ten allowlisted exception tokens (§20.8.1) and the
canonical formal exception module literal `medscale.mesc._formal_split_v1`
(§20.8.2.2) as exact string literals. The module literal is a classification
constant only; carrying it grants no import of the module it names.

The harness owns those exact contract literals locally, as authorized by this
documentation contract (`PIC-CORR-15`). The P-A2 test must not import a formal
module to discover or validate them:

```text
test import of medscale.mesc._formal_split_v1:      NOT PERMITTED
test import of medscale.mesc._formal_generation_v1: NOT PERMITTED

for discovering or validating:
exception class names
the exception module literal
input-surface literals
any other contract constant
```

The P-A2 test instead validates those literals using:

```text
literal expected values taken from the P-A1 contract
synthetic stderr byte fixtures
synthetic repository fixtures
subprocess behaviour where authorized
```

`resolve_repository_commit` remains the **only** formal execution-module import
permitted at test scope. No other formal module import is authorized, and no
statement in this package may be read as granting one.

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
