# P01-04D External Execution-Evidence Contract — Founder Decision

This is the controlling document of the P-A1 external execution-evidence
contract package.

## 1. Decision identity

```text
Decision:
XD-EXEC-1:
ARCHITECTURE A — SEPARATE REPOSITORY-CONTROLLED EXECUTION-EVIDENCE HARNESS

Contract model:
MODEL E2′ — PER-STAGE APPEND-ONLY EVIDENCE WITH WRITE-ONCE EPISODE CORE
AND WRITE-ONCE TERMINAL MANIFEST

Decision class:
EXTERNAL EXECUTION-EVIDENCE CONTRACT GOVERNANCE ONLY

Canonical baseline:
035392831c6218b5302b04ca7e392eff8724ff52

Canonical tree:
ee409f9dbb57492514b384e2332487a923bf01f9

XD-EXEC-1:
DECIDED / OPEN

P01-04D entry:
AUTHORIZED

P01-04D control state:
ENTERED — PRE-EXECUTION GOVERNANCE ONLY

P01-04D execution:
NOT AUTHORIZED

P-A2 implementation:
NOT AUTHORIZED BY THIS DECISION

P-A1 implementation clarification:
PIC-1 .. PIC-9 RECORDED — SEE §8

P-A1 implementation corrections:
PIC-CORR-1 .. PIC-CORR-6 RECORDED — SEE §8A

P-A1 final implementation corrections:
PIC-CORR-7 .. PIC-CORR-13 RECORDED — SEE §8B

P-A1 closing implementation corrections:
PIC-CORR-14 .. PIC-CORR-15 RECORDED — SEE §8C

P-A3 founder amendment:
PA3-AMD-1 .. PA3-AMD-2 RECORDED — SEE §8D
```

This decision defines the contract a future execution-evidence harness must
satisfy. It is not that harness, and it does not build, schedule or activate it.

## 2. The defect being resolved

The defect is **absent external execution evidence**.

The canonical P01-04 execution protocol requires every formal execution to
produce external evidence outside both the repository and the evidence root,
referenced by stable identity only, covering thirteen required reporting
obligations.

The adopted P01-04D formal operator satisfies none of them durably.

```text
operator emits a compact completion summary
->
nothing is persisted

operator requires --external-evidence-root
->
the value is used only to refuse an unsafe workspace destination;
the operator never writes there
```

Four further properties of the adopted operator shape this contract and are
recorded here because they are not visible in governance prose:

```text
1. compare cannot report inequality.
   It raises a typed byte-equality failure; a returned comparison result is
   always an equal result.

2. exit codes are coarse.
   Zero is success, one is any typed formal failure, two is an argument or
   usage refusal. Byte inequality is not distinguishable from an input
   identity failure by exit code alone.

3. typed error text can echo protected identifiers.
   Registry and source-record parse failures embed identifier values in their
   messages, so raw child error output is a protected-content vector.

4. compare has no expected-canonical-commit argument.
   Its surface accepts only the two completed generation workspaces.
```

## 3. Governing architecture

```text
ARCHITECTURE A:
CONTROLLING
```

A separate repository-controlled P01-04D execution-evidence harness wraps the
canonical formal operator and invokes it as a separate child process.

```text
the six adopted formal-executor blobs:
BYTE-IDENTICAL — UNCHANGED

the exact seven-file deterministic candidate bundle:
UNCHANGED

runtime evidence in the generation bundle:
PROHIBITED

runtime evidence in the authoritative split fingerprint:
PROHIBITED

runtime evidence in the repository:
PROHIBITED

runtime evidence in the future evidence root:
PROHIBITED
```

Runtime evidence is scientifically non-authoritative. The authoritative split
fingerprint remains recomputed from artifact bytes alone by the adopted layer.

## 4. Founder decisions

### PA1-FD-1 — Evidence architecture

MODEL E2′ is approved: per-stage append-only execution records under a
write-once episode core, sealed by one write-once terminal episode manifest.

A single mutable execution document is rejected. A shared cross-generation
journal is rejected, because one shared writer couples the two generations that
the protocol requires to run independently.

### PA1-FD-2 — Stage ownership

P-A owns canonical required-reporting obligations `1` through `10` and `13`.

Obligations `11` (freeze timestamp) and `12` (evidence-root identity) remain
P01-04F stage obligations. This decision does not remove, weaken or satisfy
them.

P-A exposes no `record-freeze` command. P-A1 defines only that a future,
separately authorized P01-04F record may reference the sealed P01-04D episode by
its terminal evidence identity. Nothing here authorizes P01-04F.

### PA1-FD-3 — MODEL A′ boundary

MODEL A′ activation-verification evidence remains outside P-A.

P-A defines no filename, schema, directory, owner or storage mechanism for
activation evidence. The P-A execution episode records only the
`expected_canonical_commit` value actually supplied for execution, and records
nothing about how that value was activated or verified.

### PA1-FD-4 — Canonical repository identity enforcement

Exclusive reliance on the formal operator for canonical repository identity
enforcement is rejected.

The future harness must independently verify the expected canonical repository
identity before opening an episode, before every generate stage, immediately
before every generate child launch, before compare, immediately before the
compare child launch, before verify, before invalidate where repository identity
is material, and before finalize.

The harness check is read-only. For generate, the operator's existing double
verification remains an additional fail-closed enforcement layer and is not
replaced.

This independent gate is mandatory because the canonical operator compare
surface carries no expected-canonical-commit input.

### PA1-FD-5 — Child execution

The harness invokes the canonical operator as a separate child process for
`generate` and `compare`. Where `verify` reruns canonical compare, it does so as
one separate child.

The harness must not import and call `medscale.mesc._formal_generation_v1` or
`medscale.mesc._formal_split_v1` as an execution shortcut.

Production P-A2 may reuse only pure canonical serialization and digest primitives
from `medscale.mesc._canonical_json_v1`, for evidence serialization and digest
construction, subject to later P-A2 identity verification and fixture-only
testing. That permission does not authorize production import from
`medscale.mesc._formal_generation_v1` or `medscale.mesc._formal_split_v1` for
formal execution, generation, comparison, repository-identity enforcement or any
other shortcut into the formal executor.

### PA1-FD-6 — Command surface

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

`verify` is required in P-A2 and may not be deferred if XD-EXEC-1 is to close for
P01-04D execution readiness. `verify` is P01-04D episode self-verification only.
It is not P01-04F independent verification, and it does not authorize P01-04F.

### PA1-FD-7 — Byte-equality evidence

The harness independently hashes the exact seven candidate artifacts in both
workspaces and derives the byte-equality disposition from its own ledgers. The
canonical operator compare outcome is corroborating enforcement.

The harness fails closed on disagreement between the harness-derived equality
and the operator compare outcome. The harness never repairs, rewrites or copies
a generation workspace.

### PA1-FD-8 — Raw output minimization

Raw child standard output and standard error are not persisted. Only their
SHA-256, byte size and exactly one closed-vocabulary `operator_error_class` value
may persist. Raw exception messages remain prohibited, and no free-form error
field may be created.

Complete Generation A and Generation B argv remains required external evidence.
No process environment dump is permitted. No token, credential, dedicated
hostname field or dedicated username field is permitted.

### PA1-FD-9 — Input evidence

For formal input content, P-A evidence may persist only the logical surface, the
SHA-256, the byte size and a safe path role.

No input bytes, labels, partition membership, question text, context text,
answer text or annotation text may be persisted. No currently unavailable
accepted digest may be invented.

### PA1-FD-10 — Runtime identity

The execution episode core binds the exact configured Python runtime by resolved
executable path, executable SHA-256, executable byte size, Python version and
Python implementation.

The executable SHA-256 binds the configured executable artifact. It does not
claim to cryptographically bind the interpreter's complete dynamic dependency
closure. No additional runtime dependency fields are required. The operator's
existing interpreter-version refusal remains additional enforcement.

### PA1-FD-11 — Output evidence

Generation output evidence covers exactly the seven canonical P01-04D candidate
filenames. For each, only the filename, SHA-256 and byte size are persisted. No
artifact bytes are copied into external evidence, and no eighth
generation-workspace file may be created.

### PA1-FD-12 — Episode sealing

`episode-manifest.json` is the terminal seal, and finalize is the last P-A
mutation to that execution episode.

After the manifest is created, no stage journal may be appended, no invalidation
journal may be appended, no file in the sealed episode may be rewritten, no file
may be deleted and no new file may be added to the sealed episode.

The terminal episode identity is the SHA-256 and byte size of
`episode-manifest.json`. The manifest binds every evidence record present at
seal.

That formula is unchanged, but it is not unconditional: by `PIC-CORR-14` a
terminal episode identity exists if and only if `episode-manifest.json` is
`TM-2` — a complete valid canonical manifest. An absent path (`TM-0`) and a
physically present but invalid or incomplete one (`TM-1`) have no terminal
identity and no durably established terminal disposition.

A later stage that discovers a new invalidation must not mutate the sealed P-A
episode. That later evidence requires its own separately governed immutable
record referencing the prior terminal episode identity.

### PA1-FD-13 — State-dependent evidence inventory

Evidence is not required for a stage that never executed, and a stage that never
executed must not be represented by fabricated execution evidence.

A successful episode requires completed records for Generation A, Generation B,
compare and verify. A failed or refused episode requires only the stages actually
opened or started. Every failed or refused episode that can safely reach finalize
still receives a stable terminal identity, which by `PIC-CORR-14` means exactly
that `finalize` durably created a `TM-2` terminal manifest; where creation
reaches only `TM-0` or `TM-1`, no terminal identity exists.

### PA1-FD-14 — Partial writes

A partial record write is never repaired in place. If an append cannot complete
as one valid canonical event, writing to that record stops, the record is
classified as malformed-preserved, its exact bytes are left unchanged, and no
fabricated seal event is appended after malformed bytes.

No truncation, seek-and-patch or silent repair is permitted. The terminal
manifest may bind those exact preserved bytes where safe finalization remains
possible.

### PA1-FD-15 — Invalidation and structured root-cause analysis

Invalidation evidence is additive before episode seal. It preserves the reason
class, the time, the affected safe candidate identities, the originating episode
identity and the new-episode requirement.

Free-form root-cause prose is not part of the safe P-A evidence contract. Only
structured closed-vocabulary fields are persisted. A richer protected diagnostic
narrative, if ever required, needs a separate founder authorization and a
separate handling contract.

### PA1-FD-16 — Serialization

Evidence records use canonical serialization: UTF-8, line feed, sorted object
keys, tight separators, non-finite numbers rejected, one terminal line feed for
JSON documents and one canonical JSON object followed by a line feed per record
line.

Runtime values need not be scientifically reproducible. Their serialization is
deterministic.

### PA1-FD-17 — Path safety

The external evidence root must be absolute, resolved, existing before episode
open, writable, outside the repository root, outside the Generation A workspace,
outside the Generation B workspace and outside the future evidence root.

Symlinks, junctions and other reparse-point redirects fail closed. Path
containment is evaluated on resolved path components, never on string prefixes.
The harness must not pre-create a generation workspace.

### PA1-FD-18 — P-A1 package scope

P-A1 is documentation and governance only, and uses exactly four additive
documents under `specs/mesc-pilot-01/p01-04d-execution-evidence-harness/`:
`README.md`, `founder-authorization.md`, `evidence-contract.md` and
`acceptance.md`.

P-A1 changes no implementation path.

**Historical scope of "four additive documents" (`PIC-CORR-12`).** That phrase
describes the **original** P-A1 documentation package as built and canonically
adopted through PR #95, where all four paths were additions. It remains an
accurate statement of that package and is not rewritten.

```text
original P-A1 package, adopted through PR #95:
added 4, modified 0

current implementation-clarification candidate:
modified 4, added 0, deleted 0, renamed 0
```

The current candidate modifies those same four existing documents and adds no
documentation path. The package still consists of exactly those four documents,
and still changes no implementation path.

### PA1-FD-19 — Future P-A2 package direction

P-A2 is not authorized by this disposition. Its future additive implementation
scope is expected to contain `scripts/mesc_p01_04d_evidence_harness.py`,
`tests/test_mesc_p01_04d_evidence_harness.py` and an
`implementation-acceptance.md` in this package directory.

Any additional implementation path requires a separate founder scope
disposition. The six adopted formal-executor paths remain immutable under P-A2
unless the founder separately changes that rule.

### PA1-FD-20 — XD-EXEC-1 closure semantics

Real execution is not required to close XD-EXEC-1 for implementation readiness.

XD-EXEC-1 may be marked `CLOSED FOR P01-04D EXECUTION READINESS` only after
Architecture A is recorded; P-A1 is independently reviewed and canonically
adopted; a separate founder authorization for P-A2 has been issued; the P-A2
implementation is independently reviewed; P-A2 is canonically adopted;
fixture-only synthetic tests are green on canonical main; all required commands
including `verify` are implemented and tested; the six frozen formal-executor
paths remain byte-identical; and the seven-file deterministic artifact contract
remains unchanged.

This closure concerns the P01-04D execution-evidence mechanism only. P01-04F
obligations `11` and `12` remain mandatory later-stage obligations and are not
waived.

## 5. Founder amendments

```text
A1  FINALIZE IS THE LAST MUTATION TO A P-A EXECUTION EPISODE.
    After the terminal manifest is created the sealed episode directory is
    immutable and no journal may be appended.

A2  EVIDENCE INVENTORY IS TERMINAL-DISPOSITION DEPENDENT.
    A successful episode requires Generation A, Generation B, compare and
    verify present and sealed. A failed or refused episode requires only the
    stages that actually executed. No synthetic record may be created for a
    stage that never executed.

A3  BIND THE EXACT PYTHON EXECUTABLE IDENTITY.
    Persist the resolved executable path, SHA-256, byte size, version and
    implementation.

A4  FREE-FORM ROOT-CAUSE PROSE IS NOT PART OF SAFE P-A EVIDENCE.
    Persist structured closed-vocabulary fields only.

A5  P-A1 REQUIRES ITS OWN ACCEPTANCE DOCUMENT.
    P-A1 is four additive documentation paths. P-A2 receives a separate
    implementation-acceptance document.
```

## 6. Founder reconciliations

These five items were raised against the disposition and are resolved here.

### R1 — Canonical-main movement versus evidence containment

```text
scientific continuation on identity mismatch:
PROHIBITED

invalidate on identity mismatch:
PERMITTED UNDER EVIDENCE CONTAINMENT MODE

finalize on identity mismatch:
PERMITTED UNDER EVIDENCE CONTAINMENT MODE

automatic re-pin to a moved canonical main:
PROHIBITED
```

The repository identity check is mandatory for every relevant command. For
`open`, `generate`, `compare` and `verify`, the observed canonical commit must
equal `expected_canonical_commit` before scientific continuation.

For `invalidate` and `finalize`, a mismatch does not require abandoning
already-created evidence. It enters evidence containment mode, whose exact
permitted and prohibited actions are recorded in `evidence-contract.md`.

Refusing to seal on a moved canonical main would strand an episode permanently
unsealed with no terminal identity, destroying evidence rather than protecting
it. Containment mode resolves that without permitting any continuation.

### R2 — Obligations 9 and 10 boundary

P-A owns obligations `9` and `10` for invalidations discovered while the P-A
execution episode is still unsealed. After seal the P-A episode is immutable, and
any later invalidation or root-cause evidence belongs to the separately governed
stage that discovers the later fact.

This does not waive the canonical obligation to preserve invalidation and
root-cause evidence.

### R3 — Executable digest scope

The executable SHA-256 binds the configured executable artifact and does not
claim to bind the interpreter's complete dynamic dependency closure. No
additional dependency fields are required. The operator's existing
interpreter-version refusal remains additional enforcement.

### R4 — Production and test import boundary

The production harness must not import `medscale.mesc._formal_generation_v1` or
`medscale.mesc._formal_split_v1` for execution or for repository-identity
enforcement.

The future synthetic test `tests/test_mesc_p01_04d_evidence_harness.py` may
import `resolve_repository_commit` from the adopted formal-generation
implementation solely as a reference oracle for differential conformance testing
of the independent harness resolver. This permission is test-scope only, covers
synthetic repository shapes only, and grants no access to real P01-03G or
source-record bytes.

### R5 — Required paths and incidental identity-like text

Complete argv is recorded as an ordered UTF-8 string array, and the resolved
Python executable path is recorded.

Required absolute path values must not be sanitized or redacted merely because a
path may incidentally contain a username-like component. Incidental
identity-like text inside a required path is part of that required path value and
is not a separate identity field.

A dedicated username field, a dedicated hostname field, deriving a username or
hostname from a path, environment dumps, tokens and credentials all remain
prohibited.

## 7. Founder corrections

These five corrections were issued against the independently reviewed P-A1
candidate and are applied to it. They tighten wording and close two enumeration
gaps. They create no new authority, and they alter no already-approved semantics.

### PA1-C1 — P-A2 authority wording

No sentence in this package may be read as asserting that P-A2 authorization
already exists. Every reference to P-A2 authorization states that a separate
founder authorization is required and has not been issued.

```text
P-A2:
NOT AUTHORIZED
```

### PA1-C2 — Terminal-disposition precedence

Terminal disposition is selected by a fixed precedence, recorded normatively in
`evidence-contract.md` §20.7.

Evidence integrity outranks causal outcome. If any record that must be bound at
seal is `MALFORMED_PRESERVED`, or any unresolved evidence-integrity corruption
exists, the terminal disposition is `EPISODE_EVIDENCE_CORRUPT`, which takes
precedence over `EPISODE_INVALIDATED`, `EPISODE_FAILED` and `EPISODE_REFUSED`.

The underlying causal facts remain independently recorded in the structured
failure and invalidation evidence, so precedence governs the terminal label only
and never erases a cause. No new terminal-disposition value is added.

### PA1-C3 — Exact serializer reuse boundary

Production P-A2 may reuse only pure canonical serialization and digest primitives
from `medscale.mesc._canonical_json_v1`, for evidence serialization and digest
construction, subject to later P-A2 identity verification and fixture-only
testing.

`PA1-FD-5` is corrected accordingly and its generic "canonical-serialization
helpers" wording is withdrawn. The permission does not authorize production
import from `medscale.mesc._formal_generation_v1` or
`medscale.mesc._formal_split_v1` for formal execution, generation, comparison,
repository-identity enforcement or any other shortcut into the formal executor.

`_canonical_json_v1.py` is not modified by this correction.

### PA1-C4 — Closed operator error classification

`operator_error_class` is added as an eighth closed enumeration of eleven exact
case-sensitive values, recorded in `evidence-contract.md` §20.8.

The durable value of `child_exited.error_class` is exactly one
`operator_error_class` value. Exit code zero requires `NO_ERROR`. Nonzero
operator failures map in memory from an allowlisted exception-class token to one
semantic value, and an unmatched nonzero failure maps to `UNCLASSIFIED`. Raw
exception class text need not be durable, raw exception messages remain
prohibited, values outside the enumeration are rejected, and no free-form error
field is created.

### PA1-C5 — Pre-open refusal

If a refusal occurs before `episode-core.json` has been successfully created, no
P-A execution episode exists. Nothing may be fabricated to record that refusal:
no episode directory, no `episode-core.json`, no stage journal, no
`episode-invalidation.jsonl`, no `episode-manifest.json` and no terminal episode
identity.

A pre-open refusal is a harness or process refusal outside a sealed P-A episode.
This is consistent with the state-dependent inventory, with the prohibition on
fabricating a record for an unexecuted stage, and with evidence containment,
which applies only to an already-open episode.

## 8. Founder implementation clarifications

These nine clarifications were issued against the canonically adopted P-A1
contract after an independent P-A2 implementation-readiness review. They resolve
implementation-level contradictions and ambiguities so that a future P-A2 can be
built exactly, without inventing an evidence file, a schema field, an
enumeration, a lifecycle rule, a command, an execution authority or a
protected-data access.

```text
Clarification baseline:
ddd9766e7362a43e79cd8b0728b0eb0d00830441

Clarification tree:
bc3b1a1db5dbca3daf09c13f46631d290de0e692

Clarification class:
DOCUMENTATION CORRECTION ONLY

P-A2 implementation:
NOT AUTHORIZED BY THESE CLARIFICATIONS

XD-EXEC-1:
DECIDED / OPEN — NOT CLOSED BY THESE CLARIFICATIONS
```

They create no new authority and alter no already-approved semantics.
`ARCHITECTURE A`, `MODEL E2′`, the six-command surface, the absence of
`record-freeze`, the seven scientific artifacts, the terminal-manifest identity,
the P01-04F boundary, the MODEL A′ boundary, post-seal immutability, the
five-field runtime identity, raw stdout and stderr non-persistence, the six
frozen formal-executor paths and the expected three-path P-A2 scope are all
unchanged.

### PIC-1 — Evidence inventory remains exact and closed

The evidence inventory recorded in `evidence-contract.md` §12 is **exact and
closed**, not a minimum. No new evidence file is authorized for P-A2.

```text
episode-control.jsonl:        PROHIBITED
repository-observation.jsonl: PROHIBITED
preflight.jsonl:              PROHIBITED
failure.jsonl:                PROHIBITED
any eighth evidence record class: PROHIBITED
```

State dependence governs which of the seven records must exist, never whether an
eighth may be created.

### PIC-2 — Open repository identity

Before `open`, the canonical repository identity observation is **mandatory**,
and it produces **no durable `repository_identity_observed` event**.

```text
observation before open:                MANDATORY
durable repository_identity_observed:   NOT CREATED
```

On `observed_canonical_commit != expected_canonical_commit`, `open` refuses and
creates nothing.

```text
episode directory:  NOT CREATED
episode-core.json:  NOT CREATED
any evidence:       NOT CREATED
```

On equality, `open` may continue. `episode-core.json` continues to carry
`expected_canonical_commit` only.

```text
observed_canonical_commit in episode-core: PROHIBITED
identity_match in episode-core:            PROHIBITED
```

Every prior unqualified statement that every command persists a
`repository_identity_observed` event is amended by this clarification.

### PIC-3 — Finalize repository identity

Before `finalize`, the observation is **mandatory**. A matching observation is
**non-durable**.

On `observed == expected`, `finalize` may continue.

On `observed != expected`, `finalize` must not silently append invalidation
evidence and must not seal unless a prior explicit `invalidate` has already
recorded canonical-main movement for the same episode and the exact
expected/observed pair.

```text
required mismatch sequence:
invalidate
-> durable canonical_main_movement record
-> finalize retry
-> re-observe repository identity
-> confirm the current observed movement equals the recorded movement
-> seal in containment mode
```

If canonical main moves again after `invalidate`, `finalize` refuses, and a new
explicit `invalidate` is required before another `finalize` attempt.

```text
repository-observation field in episode-manifest.json: PROHIBITED
```

### PIC-4 — Invalidate repository identity

Repository identity is **material** to `invalidate` exactly when:

```text
root_cause_class == CANONICAL_MAIN_MOVEMENT
or
failure_class == CANONICAL_MAIN_MISMATCH
```

For that case the observation is mandatory, `expected != observed` is mandatory,
and both values persist under `canonical_main_movement`:

```text
expected_canonical_commit
observed_canonical_commit
```

For every other invalidation cause the observation is not required for
invalidation evidence, and a matching observation is never persisted.

```text
identity_match in episode-invalidation.jsonl:          PROHIBITED
stage-event structure in episode-invalidation.jsonl:   PROHIBITED
```

### PIC-5 — Pre-stage versus opened-stage lifecycle

For `generate`, `compare` and `verify` the ambiguous single lifecycle is replaced
by an explicit two-phase lifecycle with the evidence boundary at `stage_opened`.
The normative ordering is recorded in `evidence-contract.md` §21.

A PRE-STAGE failure is a harness or process refusal. It creates no stage
journal, fabricates no stage and implies no automatic invalidation.

The old claim that evidence exists before the child unconditionally is corrected
to:

```text
Evidence exists before the child once stage_opened has been durably appended.
```

Failures before stage creation are not stage evidence and must not be described
as such.

### PIC-6 — `stage_failed` event and invalidation ownership

One stage-event type is added:

```text
stage_failed

additional fields, exactly:
failure_class
root_cause_class
remediation_disposition
```

Every value comes from an existing closed vocabulary. No free-form text is
permitted.

A stage failure event is technical stage evidence. It is **not** an episode
invalidation.

```text
create or append episode-invalidation.jsonl:
EXPLICIT invalidate ONLY

automatic append by generate, compare, verify or finalize:
PROHIBITED
```

When an opened stage ends `STAGE_REFUSED` or `STAGE_FAILED`, further
`generate`, `compare` or `verify` continuation in that episode is prohibited.

```text
permitted evidence progression:
explicit invalidate, then finalize

retry of the failed or refused scientific stage in the same episode:
PROHIBITED
```

The progression line above is **superseded by `PIC-CORR-4`** (§8A): explicit
`invalidate` is not universally mandatory before `finalize`, and where no
separate pre-seal invalidation fact exists `finalize` may seal directly. The
prohibition on continuation and on retrying the same scientific stage, and the
invalidation-ownership rule of `PIC-6`, are unchanged.

### PIC-7 — `stage_disposition`

A ninth closed enumeration is added, recorded normatively in
`evidence-contract.md` §20.9:

```text
STAGE_COMPLETE
STAGE_REFUSED
STAGE_FAILED
```

`stage_sealed.stage_disposition` carries exactly one value from this set.

### PIC-8 — `path_role`

A tenth closed enumeration is added, recorded normatively in
`evidence-contract.md` §20.10:

```text
FORMAL_INPUT_ORDERED_EXAMPLE_REGISTRY
FORMAL_INPUT_SOURCE_DOCUMENT_REGISTRY
FORMAL_INPUT_TRANSFORMED_DATASET_IDENTITY
FORMAL_INPUT_SOURCE_RECORDS
FORMAL_INPUT_DECISION_RECORD
```

`path_role` carries semantic role only. It must never carry an absolute path, a
relative path, a filename derived from a local location, a username, a hostname
or a protected identifier.

The closed-vocabulary totals become:

```text
closed enumerations:
10

total closed enumeration values:
77
```

Every stale statement asserting eight enumerations or sixty-nine values is
withdrawn.

### PIC-9 — Operator exception mapping

The allowlisted exception-class tokens and their durable mappings are exactly:

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

No other token is allowlisted.

```text
unmatched nonzero child failure:  UNCLASSIFIED
argparse or usage exit code 2:    UNCLASSIFIED
exit code 0:                      NO_ERROR
```

The extraction mechanism is fixed and recorded normatively in
`evidence-contract.md` §20.8. Production must not import the formal split or
formal generation modules to perform this mapping.

This tightens `PA1-C4` on one point and contradicts it on none: `PA1-C4` said
raw exception class text *need not* be durable, and `PIC-9` makes it prohibited.
The mapping target, the closed enumeration, the `NO_ERROR` and `UNCLASSIFIED`
rules and the prohibition on raw exception messages are unchanged.

### Deterministic implementation decisions

These decisions are controlling. They fix the value domains and derivations that
would otherwise permit incompatible P-A2 implementations, and they are recorded
normatively in `evidence-contract.md`.

```text
stage:
GENERATE_A, GENERATE_B, COMPARE, VERIFY

generation_identity:
A, B — present only where applicable

schema_version, episode-core:
mesc-p01-04d-execution-evidence/episode-core/v1

schema_version, stage events:
mesc-p01-04d-execution-evidence/stage-event/v1

schema_version, invalidation events:
mesc-p01-04d-execution-evidence/invalidation-event/v1

schema_version, episode manifest:
mesc-p01-04d-execution-evidence/episode-manifest/v1

event_ordinal:
starts at 1; scoped independently to each physical JSONL file; increases by
exactly one per successfully appended complete canonical event; never invented
after malformed bytes

timestamps:
UTC RFC3339, exact form YYYY-MM-DDTHH:MM:SS.ffffffZ

byte_equality:
EQUAL, UNEQUAL

comparison_derived:
NOT EMITTED when a complete seven-file equality ledger cannot be derived; the
stage records stage_failed and seals failed or refused as applicable

repository resolver differential testing:
exact equality with resolve_repository_commit for every supported non-reparse
shape; the harness refuses symlink, junction and reparse-point shapes even where
the oracle resolves them, and that stricter refusal is the only authorized
divergence

split_fingerprint_observed:
never derived from persisted stdout; Generation A and B read
generation-manifest.json read-only after successful child completion; compare
and verify read both manifests read-only and require agreement before one
observed value is recorded

harness self-identity:
the exact bytes of <repository-root>/scripts/mesc_p01_04d_evidence_harness.py,
whose resolved target must equal the running script's resolved __file__ path

operator_relative_path:
scripts/mesc_p01_04d_operator.py — POSIX "/" separators regardless of host OS

production input-surface literals:
ordered_example_registry, source_document_registry,
transformed_dataset_identity, source_records, decision_record — hardcoded, never
obtained by importing the formal split or formal generation modules

test-scope formal import permission:
resolve_repository_commit ONLY; not broadened to make_environment,
SYNTHETIC_COMMIT or any other helper from a frozen formal test
```

## 8A. Founder implementation corrections

An independent full-content review of the `PIC-1` .. `PIC-9` clarification
candidate returned `CHANGES REQUIRED` on three blocking implementation
ambiguities: `root_cause_class` and `remediation_disposition` had no derivation
rule, and the `STAGE_REFUSED` / `STAGE_FAILED` boundary overlapped for post-open
pre-child harness failures. These six corrections resolve them. A later
independent review of the corrected candidate found one further blocking gap,
resolved by `PIC-CORR-7` .. `PIC-CORR-13` in §8B.

```text
Correction class:
DOCUMENTATION CORRECTION ONLY

New enumeration or enumeration value:
NONE

P-A2 implementation:
NOT AUTHORIZED BY THESE CORRECTIONS

XD-EXEC-1:
DECIDED / OPEN — NOT CLOSED BY THESE CORRECTIONS
```

`PIC-1` through `PIC-9` are preserved in full. `ARCHITECTURE A`, `MODEL E2′`,
the six-command surface, the absence of `record-freeze`, the seven scientific
artifacts, the terminal-manifest identity, the P01-04F boundary, the MODEL A′
boundary, post-seal immutability, the five-field runtime identity, raw stdout
and stderr non-persistence, the six frozen formal-executor paths and the
expected three-path P-A2 scope are all unchanged.

### PIC-CORR-1 — Exact stage-disposition boundary

`stage_disposition` is decided by an exact test, recorded normatively in
`evidence-contract.md` §20.9.

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

No other `failure_class` may produce `STAGE_REFUSED`. In particular
`INPUT_HASH_FAILURE`, a clean pre-child `EVIDENCE_WRITE_FAILURE`,
`CHILD_LAUNCH_FAILURE`, `CHILD_NONZERO_EXIT`, `OUTPUT_INVENTORY_MISMATCH`,
`OUTPUT_HASH_FAILURE`, `BYTE_INEQUALITY`, `COMPARE_CONTRADICTION`,
`FINGERPRINT_MISMATCH`, `VERIFY_FAILURE` and `UNCLASSIFIED` are all
`STAGE_FAILED`.

The phrase "before child execution or completion" is withdrawn as a definition
of `STAGE_REFUSED`.

Where a failed append leaves malformed bytes, the `MALFORMED_PRESERVED` rules
control: no `stage_failed` and no `stage_sealed` may be fabricated after
malformed bytes merely to complete the lifecycle.

### PIC-CORR-2 — Exact universal failure mapping

`failure_class` is observed; `root_cause_class` and `remediation_disposition`
are derived from it. The mapping is recorded normatively in
`evidence-contract.md` §19.1 and is total over the twenty `failure_class`
values. Unless `CHILD_NONZERO_EXIT` applies, it is exactly:

| `failure_class` | `root_cause_class` | `remediation_disposition` |
|---|---|---|
| `ARGUMENT_REFUSAL` | `EVIDENCE_CONFIGURATION_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `CANONICAL_MAIN_MISMATCH` | `CANONICAL_MAIN_MOVEMENT` | `FOUNDER_DISPOSITION_REQUIRED` |
| `PATH_SEPARATION_REFUSAL` | `PATH_SAFETY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `REPARSE_POINT_REFUSAL` | `PATH_SAFETY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `HARNESS_IDENTITY_MISMATCH` | `HARNESS_IDENTITY_MISMATCH` | `FOUNDER_DISPOSITION_REQUIRED` |
| `OPERATOR_IDENTITY_MISMATCH` | `OPERATOR_IDENTITY_MISMATCH` | `FOUNDER_DISPOSITION_REQUIRED` |
| `RUNTIME_IDENTITY_MISMATCH` | `RUNTIME_IDENTITY_MISMATCH` | `FOUNDER_DISPOSITION_REQUIRED` |
| `INPUT_HASH_FAILURE` | `INPUT_IDENTITY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `INPUT_IDENTITY_MISMATCH` | `INPUT_IDENTITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `CHILD_LAUNCH_FAILURE` | `CHILD_PROCESS_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `CHILD_NONZERO_EXIT` | see `PIC-CORR-3` | see `PIC-CORR-3` |
| `OUTPUT_INVENTORY_MISMATCH` | `OUTPUT_INVENTORY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `OUTPUT_HASH_FAILURE` | `EVIDENCE_INTEGRITY_FAILURE` | `NEW_EPISODE_REQUIRED` |
| `BYTE_INEQUALITY` | `BYTE_INEQUALITY` | `FOUNDER_DISPOSITION_REQUIRED` |
| `COMPARE_CONTRADICTION` | `EVIDENCE_INTEGRITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `FINGERPRINT_MISMATCH` | `FINGERPRINT_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `EVIDENCE_WRITE_FAILURE` | `EVIDENCE_INTEGRITY_FAILURE` | `NO_REMEDIATION_AUTHORIZED` |
| `EVIDENCE_MALFORMED_PRESERVED` | `EVIDENCE_INTEGRITY_FAILURE` | `NO_REMEDIATION_AUTHORIZED` |
| `VERIFY_FAILURE` | `EVIDENCE_INTEGRITY_FAILURE` | `FOUNDER_DISPOSITION_REQUIRED` |
| `UNCLASSIFIED` | `UNDETERMINED` | `FOUNDER_DISPOSITION_REQUIRED` |

These mappings apply wherever the corresponding closed fields coexist, including
`stage_failed` and episode invalidation evidence. No implementation may
substitute another root cause or remediation value.

`LATER_STAGE_GOVERNANCE_REQUIRED` is not emitted by a P-A2 `stage_failed`. It
remains reserved for a separately governed later stage discovering a fact after
the P-A episode is sealed.

### PIC-CORR-3 — `CHILD_NONZERO_EXIT` mapping

For `failure_class` `CHILD_NONZERO_EXIT`, the other two values derive exactly
from the `operator_error_class` already recorded on `child_exited`, recorded
normatively in `evidence-contract.md` §19.2:

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
| `NO_ERROR` | `UNDETERMINED` | `FOUNDER_DISPOSITION_REQUIRED` — CONTRACT CONTRADICTION / FAIL CLOSED |

The table is total over all eleven `operator_error_class` values
(`PIC-CORR-11`). The eleventh row is stated in the controlling table itself and
not left table-external.

The combination `CHILD_NONZERO_EXIT` with `operator_error_class` `NO_ERROR` is a
contract contradiction, not a normal outcome: `NO_ERROR` is reserved for exit
code zero. If encountered, derive `UNDETERMINED` and
`FOUNDER_DISPOSITION_REQUIRED`, and fail closed. No mapping value changes.

### PIC-CORR-4 — Post-failed-stage progression

After `STAGE_REFUSED` or `STAGE_FAILED`, `generate`, `compare`, `verify` and
retry of the same scientific stage in that episode all remain prohibited, and a
fresh scientific attempt requires a new episode.

Explicit `invalidate` is **not** universally mandatory before `finalize`. The
prior wording that could imply it is corrected in `evidence-contract.md` §17.2.

```text
no separate pre-seal invalidation fact:
finalize MAY seal directly

terminal disposition then reachable as:
EPISODE_REFUSED or EPISODE_FAILED, by the existing precedence

explicit invalidation recorded:
EPISODE_INVALIDATED, unless evidence corruption has higher precedence

canonical-main movement:
the PIC-3 explicit invalidate-before-finalize containment sequence REMAINS
MANDATORY and is not weakened
```

### PIC-CORR-5 — Acceptance historical scoping

`acceptance.md` criteria `A-1` and `A-2` describe the **original** P-A1 package
that was canonically adopted through PR #95. They must not describe the current
clarification commit as though its four paths were additions.

```text
current clarification candidate truth:
modified 4, added 0, deleted 0, renamed 0
```

### PIC-CORR-6 — Explicit deterministic safety details

Three details are made explicit, recorded normatively in `evidence-contract.md`
§20.8.2, §20 and §15.3.2.

Operator error-class extraction operates on stderr bytes in memory. The full
stderr need not be successfully decoded, only the final non-empty line is
inspected, and only an exact ASCII form matching the canonical formal exception
module plus an exact allowlisted class token is accepted. Empty stderr,
non-ASCII or non-UTF-8 bytes, a malformed final line, an unexpected exception
module, a non-allowlisted token, and message text that merely contains an
allowlisted token all resolve to `UNCLASSIFIED`. No raw class text and no raw
message is persisted.

The §20 count of ten named closed enumerations and seventy-seven values is the
**named closed-enumeration ledger**. Other fixed inline domains — `mode`,
`stage`, `generation_identity` and `byte_equality` — remain fixed closed domains
but are not included in that 10 / 77 arithmetic.

Where a non-main stage failure and canonical-main movement coexist, the stage
failure is preserved in `stage_failed`, the canonical-main movement requires its
own explicit `invalidate` record, and containment `finalize` may proceed only
after that movement record satisfies `PIC-3`.

### Stage failure event ordering

For any safely recordable opened-stage refusal or failure, `stage_failed` must
precede `stage_sealed`. Recorded normatively in `evidence-contract.md` §21.2.1.

```text
child nonzero:
child_started -> child_exited -> stage_failed -> stage_sealed

post-child integrity failure:
child_exited -> any fully derivable outputs_hashed / comparison_derived
-> stage_failed -> stage_sealed

outputs or comparison not fully derivable:
omit those events -> stage_failed -> stage_sealed

journal bytes malformed:
preserve exact malformed bytes; fabricate no later event; fabricate no
stage_sealed
```

## 8B. Final founder implementation corrections

A second independent full-content review of the corrected clarification
candidate returned `CHANGES REQUIRED` on one blocking gap: the case where an
opened stage's journal bytes remain well formed but a required append can no
longer be durably written had no fail-closed treatment, while
`evidence-contract.md` §21.2 asserted without qualification that every
post-`stage_opened` failure was durably representable. These seven corrections
close that gap and six smaller determinism items.

```text
Correction class:
DOCUMENTATION CORRECTION ONLY

New enumeration or enumeration value:
NONE

New evidence file:
NONE

New manifest field:
NONE

P-A2 implementation:
NOT AUTHORIZED BY THESE CORRECTIONS

XD-EXEC-1:
DECIDED / OPEN — NOT CLOSED BY THESE CORRECTIONS
```

`PIC-1` through `PIC-9` and `PIC-CORR-1` through `PIC-CORR-6` are preserved in
full. `ARCHITECTURE A`, `MODEL E2′`, the six-command surface, the absence of
`record-freeze`, the seven evidence record classes with no eighth, the seven
scientific artifacts, the twenty-value failure mapping, the eleven-value
`CHILD_NONZERO_EXIT` derivation, the 10 / 77 named vocabulary ledger, the
terminal-manifest identity, the P01-04F boundary, the MODEL A′ boundary,
post-seal immutability, the five-field runtime identity, raw stdout and stderr
non-persistence, the canonical JSON contract, the authorized resolver
divergence, `path_role`, terminal precedence and the expected three-path P-A2
scope are all unchanged.

### PIC-CORR-7 — Destination-unwritable and structurally unsealed stages

Recorded normatively in `evidence-contract.md` §18, §13.1, §20.7 and §21.2.

**Three evidence-write outcomes.** For an opened stage whose journal already
exists, an attempted required append has exactly three disjoint outcomes.

```text
CASE A — ZERO-BYTE WRITE FAILURE, LATER SAFE APPEND POSSIBLE
the append fails, no byte was added or changed, the journal remains
syntactically WELL_FORMED, and a subsequent append can still be safely and
durably completed.

failure_class:            EVIDENCE_WRITE_FAILURE
root_cause_class:         EVIDENCE_INTEGRITY_FAILURE
remediation_disposition:  NO_REMEDIATION_AUTHORIZED

durable recording still possible:
stage_failed -> stage_sealed, stage_disposition STAGE_FAILED

CASE B — PARTIAL OR MALFORMED BYTES REMAIN
preserve exact bytes; record_integrity MALFORMED_PRESERVED; do not truncate,
repair or seek-and-patch; append no fabricated stage_failed; append no
fabricated stage_sealed; fabricate no stage_disposition.
Terminal precedence selects EPISODE_EVIDENCE_CORRUPT.
The existing partial-write rules remain controlling.

CASE C — BYTES WELL FORMED BUT FURTHER APPEND NOT SAFELY POSSIBLE
examples: the evidence destination becomes unwritable; storage denies a
subsequent append; a required event cannot be durably appended even though
prior bytes remain intact.

do NOT fabricate stage_failed
do NOT fabricate stage_sealed
do NOT repair or backfill the journal later
```

**Structural unseal.** In case C the stage is `STRUCTURALLY UNSEALED`. That
phrase is a structural condition, not a new enumeration and not a new durable
field. A stage is structurally unsealed when `stage_opened` exists and the
journal does not end in exactly one valid `stage_sealed` event.

At `finalize`, a structurally unsealed opened stage is by definition an
unresolved evidence-integrity corruption condition, regardless of whether its
existing JSONL bytes are syntactically well formed. Terminal precedence rank 1
therefore selects `EPISODE_EVIDENCE_CORRUPT`, and it must not fall through to
`EPISODE_INVALIDATED`, `EPISODE_REFUSED`, `EPISODE_FAILED` or
`EPISODE_COMPLETE_EQUAL` solely because the existing bytes parse correctly.

**Continuation.** Immediately on detecting that required stage evidence can no
longer be safely appended, `generate`, `compare`, `verify`, same-stage retry,
any new scientific stage, child launch, new protected-input access, new
protected-input hashing, generation-workspace mutation, automatic re-pin,
journal repair and journal backfill after storage recovery are all prohibited.
The episode enters evidence-preserving containment only, and no new enumeration
or record represents that fact.

**Finalize.** If `episode-manifest.json` does not yet exist and the evidence
root later permits it to be written, `finalize` may be invoked or retried only
as an evidence-preserving containment operation. It must not append to or repair
the structurally unsealed journal; it reads and binds the exact existing bytes,
computes their SHA-256 and byte size, records `record_integrity` `WELL_FORMED`
where those bytes are syntactically canonical and countable, records the actual
`event_count` where countable, independently treats the absent terminal
`stage_sealed` event as unresolved evidence-integrity corruption, and selects
`EPISODE_EVIDENCE_CORRUPT`.

The structural corruption condition is not encoded by falsely changing
`record_integrity` to `MALFORMED_PRESERVED`. Syntactic record integrity and
lifecycle completeness are separate properties.

If `finalize` itself cannot durably create the manifest, no valid manifest and no
terminal identity exist, no success or adoption claim is permitted, and no
scientific continuation is permitted. A later `finalize` retry is permitted only
after storage becomes writable and only while no `episode-manifest.json` exists.
After successful manifest creation, post-seal immutability applies absolutely.

The retry condition in the preceding paragraph is qualified exactly by
`PIC-CORR-14` below: "while no `episode-manifest.json` exists" means the TM-0
state, in which the path is physically absent. A path that physically exists but
whose bytes are not a complete valid canonical manifest is TM-1, and no retry of
any kind is permitted there. No other part of `PIC-CORR-7` is changed.

**General abrupt-stop rule.** At `finalize`, any opened stage journal that does
not end in exactly one valid `stage_sealed` event is an unresolved
evidence-integrity corruption condition — whether caused by evidence destination
failure, process termination, harness crash or abrupt host interruption. No
causal event that was never durably recorded may be invented. The observable
structural incompleteness alone prevents scientific success and selects
`EPISODE_EVIDENCE_CORRUPT`.

**Success prerequisite.** `EPISODE_COMPLETE_EQUAL` requires every required
opened stage journal to end in exactly one valid `stage_sealed` event, and that
event must carry `STAGE_COMPLETE` for every scientifically successful required
stage. An opened but structurally unsealed stage can never satisfy the
successful-episode prerequisites.

**The §21.2 absolute claim is corrected.** The unqualified statement that every
subsequent failure is durably representable is withdrawn and replaced by: after
`stage_opened`, every subsequent failure that remains safely recordable is
represented by `stage_failed` followed by `stage_sealed`; if durable append is
no longer safely possible, `PIC-CORR-7` controls — no event is fabricated, the
stage remains structurally unsealed, scientific continuation stops, and terminal
finalization selects `EPISODE_EVIDENCE_CORRUPT`.

`safely recordable` is defined exactly, in `evidence-contract.md` §18.0, as: the
required canonical event can be appended atomically and durably, without
altering prior bytes and without leaving malformed or partial bytes. It is never
an undefined escape clause.

### PIC-CORR-8 — Exact stderr logical-line algorithm

Recorded normatively in `evidence-contract.md` §20.8.2.1. stderr remains exact
bytes in memory and no full Unicode decode is required.

```text
1. split the exact stderr bytes ONLY on b"\n"
2. from each segment remove exactly ONE trailing b"\r", if and only if it is
   the final byte of that segment
3. a bare b"\r" not immediately before a b"\n" is NOT a line separator
4. after that one-byte CR normalization, discard zero-length logical lines when
   selecting the final non-empty line
5. inspect the final non-empty normalized segment only
```

The recognized prefix, required at byte offset 0 of the inspected line, is
exactly `b"medscale.mesc._formal_split_v1."`. Immediately after it there must
appear exactly one allowlisted ASCII formal exception class token, and
immediately after the token either the end of the logical line or one ASCII
colon byte `b":"`. Where the colon is present, all following bytes are untrusted
exception-message bytes: ignored for classification, never required to decode,
never persisted.

Everything else resolves to `UNCLASSIFIED`: empty stderr, no final non-empty
logical line, a nonmatching module prefix, an unexpected module, a token that is
not exactly allowlisted, non-ASCII bytes inside the required module/token
syntax, malformed required syntax, message text that merely contains an
allowlisted token away from byte offset zero, and any bare-CR layout that does
not satisfy the exact syntax after the defined scan.

This rule must produce the same classification for LF and CRLF traceback output.
Raw stderr, raw exception class text and raw exception messages remain
prohibited from durable evidence.

### PIC-CORR-9 — Explicit `CHILD_LAUNCH_FAILURE` lifecycle

Recorded normatively in `evidence-contract.md` §21.2.1.1. If process creation
itself fails:

```text
child process:  DOES NOT EXIST
child_started:  MUST BE ABSENT
child_exited:   MUST BE ABSENT
pid:            MUST NOT BE FABRICATED
started_at:     MUST NOT BE FABRICATED
ended_at:       MUST NOT BE FABRICATED AS CHILD EVIDENCE

failure_class:            CHILD_LAUNCH_FAILURE
root_cause_class:         CHILD_PROCESS_FAILURE
remediation_disposition:  NEW_EPISODE_REQUIRED

journal safely recordable:
stage_failed -> stage_sealed, stage_disposition STAGE_FAILED

evidence cannot safely be appended:
PIC-CORR-7 controls
```

### PIC-CORR-10 — Semantic derivation versus durable destination

Recorded normatively in `evidence-contract.md` §19.3. Derivation and durability
are separate obligations. The contract may deterministically derive
`failure_class`, `root_cause_class` and `remediation_disposition` without
thereby authorizing or requiring a fabricated durable record.

A triad is persisted only when an authorized record schema contains those
fields, the authorized destination exists, and the event is safely recordable.

```text
PRE-STAGE:
the triad may be semantically known, but no stage journal is fabricated

MALFORMED_PRESERVED:
no later triad event is fabricated into malformed bytes

PIC-CORR-7 case C:
the triad may be semantically EVIDENCE_WRITE_FAILURE /
EVIDENCE_INTEGRITY_FAILURE / NO_REMEDIATION_AUTHORIZED, but if the journal
cannot accept an event, no stage_failed is fabricated
```

The terminal structural-corruption rule still applies in every such case.

### PIC-CORR-11 — Controlling `CHILD_NONZERO_EXIT` table completeness

The controlling `CHILD_NONZERO_EXIT` table in `PIC-CORR-3` above now contains
all eleven `operator_error_class` values, with `NO_ERROR` present as an actual
eleventh row deriving `UNDETERMINED` and `FOUNDER_DISPOSITION_REQUIRED` and
marked `CONTRACT CONTRADICTION / FAIL CLOSED`. The eleventh branch is no longer
table-external. No mapping value changes.

### PIC-CORR-12 — `PA1-FD-18` historical scope

Recorded in `PA1-FD-18` above. The phrase "four additive documents" describes
the original P-A1 documentation package canonically adopted through PR #95,
where all four paths were additions. The current implementation-clarification
candidate modifies those same four existing documents and adds zero
documentation paths. History is not rewritten, and nothing here implies the
original package was not additive.

### PIC-CORR-13 — Exact exception-module anchor

The literal canonical formal exception module is exactly:

```text
medscale.mesc._formal_split_v1
```

Recorded normatively in `evidence-contract.md` §20.8.2.2 and §27. It is the only
accepted module prefix for the `PIC-9` / `PIC-CORR-8` traceback class-token
extraction mechanism. Production must still not import the formal module to
perform classification; the string is a classification constant only.

## 8C. Closing founder implementation corrections

A third independent full-content review of the corrected clarification candidate
returned `CHANGES REQUIRED` on one blocking finding, `PIC-FFR1`: partial
terminal-manifest creation was undefined. The contract stated that a `finalize`
retry was permitted "while no `episode-manifest.json` exists" and that terminal
identity was the SHA-256 and byte size of `episode-manifest.json`, without ever
deciding what governs when that path physically exists but its bytes are not a
complete valid canonical manifest. `PIC-CORR-14` closes that gap.
`PIC-CORR-15` is a non-blocking wording correction issued with it.

```text
Correction class:
DOCUMENTATION CORRECTION ONLY

New enumeration or enumeration value:
NONE

New evidence file:
NONE

New manifest field:
NONE

New terminal-disposition value:
NONE

Recovery sidecar, repair marker or retry marker:
NONE

P-A2 implementation:
NOT AUTHORIZED BY THESE CORRECTIONS

XD-EXEC-1:
DECIDED / OPEN — NOT CLOSED BY THESE CORRECTIONS
```

`PIC-1` through `PIC-9` and `PIC-CORR-1` through `PIC-CORR-13` are preserved in
full. `ARCHITECTURE A`, `MODEL E2′`, the seven evidence record classes, the
six-command surface, the absence of `record-freeze`, the failure mappings, the
stage dispositions, terminal precedence for valid TM-2 manifests, the
structural-unseal semantics, the stderr parser, `path_role`, the 10 / 77 named
vocabulary ledger, post-seal immutability, the P01-04F boundary, the MODEL A′
boundary, the five-field runtime identity and the expected three-path P-A2 scope
are all unchanged.

The terminal-manifest identity **formula** is also unchanged: it remains the
SHA-256 and byte size of the terminal manifest's exact bytes. What `PIC-CORR-14`
changes is only the condition under which that identity exists at all, which was
previously stated without qualification. Earlier statements in §8 and §8B that
the terminal-manifest identity is unchanged remain true of the corrections they
describe and are correctly scoped to them.

### PIC-CORR-14 — Terminal-manifest creation semantics

Recorded normatively in `evidence-contract.md` §18.8, and reflected in §5.2.1,
§13.2, §15.4, §17, §18.6, §20.7 and §22.

**The physical path state and manifest validity are distinct.** Terminal
authority follows validity, never mere existence. `episode-manifest.json` has
exactly three creation states, which are mutually exclusive, exhaustive,
observable and deterministic. There is no fourth state.

```text
TM-0   the path does not exist
TM-1   the path exists, but its exact bytes are NOT exactly one complete,
       canonical, schema-valid episode manifest
TM-2   the path exists, and its exact bytes ARE exactly one complete,
       canonical, schema-valid episode manifest
```

`TM-0`, `TM-1` and `TM-2` are structural states: not an enumeration, not
enumeration values, not a durable field. Nothing is written to record which state
holds.

**TM-0 — ABSENT.** No directory entry exists at the path, including where
`finalize` failed before creating it.

```text
valid manifest:                           NO
canonical seal:                           NO
terminal identity:                        NO
terminal disposition durably established: NO
```

A later `finalize` retry MAY occur if storage becomes usable, but only while
`episode-manifest.json` is still physically absent, no successful seal previously
occurred, the retry remains evidence-preserving containment, no scientific
continuation occurs, no stage journal is repaired or backfilled, and all existing
pre-finalize evidence is read-only.

**TM-1 — PRESENT BUT INVALID OR INCOMPLETE.** The path exists and its exact bytes
are not exactly one complete canonical schema-valid manifest. This includes a
zero-byte file, truncated bytes, partial JSON, malformed JSON, syntactically
valid JSON missing mandatory fields, syntactically valid but noncanonical JSON, a
wrong `schema_version`, an incomplete `records[]` binding, an absent
`terminal_disposition`, and any bytes failing exact canonical-manifest
validation. A zero-byte file that physically exists is TM-1, never TM-0.

The exact existing bytes are preserved. Truncation, deletion, overwrite,
replacement, rename, repair, seek-and-patch, appending to complete it, re-running
manifest creation and creating a second terminal manifest are all prohibited.

```text
finalize retry:            PROHIBITED
canonical seal:            FAILED / NOT ESTABLISHED
terminal identity:         NOT ESTABLISHED
terminal_disposition:      NOT DURABLY ESTABLISHED
scientific success:        PROHIBITED
scientific continuation:   PROHIBITED
generate:                  PROHIBITED
compare:                   PROHIBITED
verify:                    PROHIBITED
protected-input access:    PROHIBITED
protected-input hashing:   PROHIBITED
workspace mutation:        PROHIBITED
```

The episode is an irrecoverably failed terminalization attempt. That phrase is a
governance condition only; no enumeration, value, field, evidence record, marker
or sidecar is created for it. Any fresh scientific attempt requires a separate
new episode, which remains subject to every existing execution and governance
authorization and is neither created nor authorized here.

**The corruption distinction is mandatory.** Under TM-1 the episode must be
treated as unusable and evidence-corrupt for any scientific or adoption claim,
but it must not be claimed that `EPISODE_EVIDENCE_CORRUPT` was durably recorded
as `terminal_disposition`. That value exists only inside a complete valid
canonical terminal manifest, so under TM-1 the durable terminal disposition, the
terminal identity and the canonical seal are all absent.

**TM-2 — COMPLETE VALID CANONICAL MANIFEST.** The exact bytes satisfy all of:
complete file; UTF-8; canonical JSON; exact episode-manifest `schema_version`;
all mandatory fields; complete required record binding; valid record metadata;
exactly one valid `terminal_disposition`; no extra prohibited fields; and
canonical serializer round-trip and exact-byte validation as the contract
requires.

```text
canonical seal:            ESTABLISHED
terminal identity:         ESTABLISHED
post-seal immutability:    ABSOLUTE
finalize retry:            PROHIBITED
rewrite:                   PROHIBITED
```

Terminal identity is exactly the SHA-256 of the complete valid exact manifest
bytes together with the byte size of those same exact bytes.

**Path existence is not terminal identity.** Every unqualified rule equivalent to
"terminal identity = SHA-256 plus size of `episode-manifest.json`" is replaced
by: terminal identity exists if and only if `episode-manifest.json` is TM-2.
TM-0 and TM-1 have no terminal identity. Computing or reporting a terminal
identity over invalid, partial or incomplete bytes is prohibited.

**Crash after a complete valid write.** If the complete valid canonical TM-2
bytes were durably created and the harness then crashed or terminated before
reporting the terminal identity, the episode is still canonically sealed.
Terminal identity is a deterministic derived property of the exact valid manifest
bytes and may be recomputed read-only from them. Rewriting the manifest,
rerunning `finalize` as a mutation, changing the terminal disposition and
creating another manifest all remain prohibited. A process failing to report the
identity does not undo an already-valid terminal seal.

**Crash before a complete valid write.** If a directory entry exists but the
bytes are not TM-2, the TM-1 rules control. Intent is never inferred from how
many bytes the harness expected to write; the observed exact bytes and their
schema and canonical validity control.

**Exclusive creation is preserved.** The implementation must attempt creation so
that an existing path is never silently replaced. On entry to `finalize`, an
existing `episode-manifest.json` is validated read-only: TM-2 means the episode
is already sealed and mutation is prohibited; TM-1 means terminalization has
irrecoverably failed and mutation is prohibited. Neither branch is a permitted
`finalize` retry — both are fail-closed recognition of existing state.

**Finalize remains the last P-A mutation.** Under TM-1 the partial or invalid
durable creation attempt is itself the last mutation to that episode and no
cleanup mutation follows. Under TM-2 successful manifest creation is the last
mutation.

**Structural-unseal interaction.** `PIC-CORR-7` is preserved. A structurally
unsealed stage ordinarily causes a valid TM-2 manifest, where creation succeeds,
to carry `EPISODE_EVIDENCE_CORRUPT`. But if terminal-manifest creation itself
reaches TM-1, no `terminal_disposition` is durably established at all,
`EPISODE_EVIDENCE_CORRUPT` must not be claimed to have been written, and the
episode remains unusable and unsealed.

**Canonical-main-movement interaction.** Where canonical-main movement requires an
explicit `invalidate` before `finalize`, that requirement remains. If the
movement record was validly persisted and terminal-manifest creation then reaches
TM-1, the invalidation evidence remains preserved, but no canonical terminal
disposition and no terminal identity exist, and `EPISODE_INVALIDATED` must not be
claimed without a valid TM-2 manifest carrying it.

**No `record_integrity` invention for the manifest.** `WELL_FORMED` and
`MALFORMED_PRESERVED` are not applied as a manifest field. `record_integrity`
remains defined only for the already authorized bound evidence records. Manifest
validity is determined by the TM-0 / TM-1 / TM-2 semantics alone, without adding
a persisted field or enumeration.

### PIC-CORR-15 — Test-authority wording

Recorded normatively in `evidence-contract.md` §27. The sentence that could be
read as granting additional formal test imports is removed and replaced.

```text
the ONLY formal execution-module import permitted at test scope:
resolve_repository_commit

any other formal module import:
NOT AUTHORIZED
```

The P-A2 test must not import `medscale.mesc._formal_split_v1` or
`medscale.mesc._formal_generation_v1` to discover or validate exception class
names, the exception module literal, input-surface literals or any other contract
constant. The harness owns those exact contract literals locally, as authorized
by the documentation contract.

P-A2 tests validate them using literal expected values taken from the P-A1
contract, synthetic stderr byte fixtures, synthetic repository fixtures and
subprocess behaviour where authorized, without broadening the formal import
exception. This changes no earlier permission: `resolve_repository_commit` was
and remains the sole formal test-scope import, and it is still not broadened to
`make_environment`, `SYNTHETIC_COMMIT` or any other helper from a frozen formal
test.

## 8D. P-A3 founder amendment

An independent P-A3 review of the P-A2 implementation candidate returned
`CHANGES REQUIRED` on four blocking findings. Two of them, `F-3` and `F-4`, are
not implementation defects. They are contract-level: the implementation carries
one `failure_class` value and one manifest binding that this package's governing
contract does not admit, and neither can be reconciled by editing code.

`F-3` — the implementation carries a `failure_class` enumeration of twenty-one
values against a governing ledger of twenty, because `evidence-contract.md` §20
permits no extension without a founder disposition and no such disposition had
been issued.

`F-4` — the manifest binding of episode path identity was left unimplemented
because §15.4 declares the `episode-manifest.json` field set exact and closed at
six fields. That closure now blocks a required control rather than protecting
one.

This section issues the disposition those two findings compel. Unlike §7, §8, §8A,
§8B and §8C, this is an **amendment**, not a correction: it extends two closed
sets.

```text
Decision class:
FOUNDER AMENDMENT TO THE P-A1 CONTRACT — GOVERNANCE ONLY

New enumeration:
NONE — the named enumeration count stays 10

New enumeration value:
EXACTLY ONE — failure_class EPISODE_PATH_IDENTITY_DRIFT

New manifest field:
EXACTLY ONE — episode_path_identity

New evidence file:
NONE — EVIDENCE_FILENAMES stays 7

New command:
NONE — COMMANDS stays 6

New event kind:
NONE

Record-freeze:
STILL DOES NOT EXIST

P01-04D execution:
NOT AUTHORIZED BY THIS AMENDMENT

XD-EXEC-1:
DECIDED / OPEN — NOT CLOSED BY THIS AMENDMENT
```

`PA1-FD-1` through `PA1-FD-20`, `A1` through `A5`, `R1` through `R5`, `PA1-C1`
through `PA1-C5`, `PIC-1` through `PIC-9` and `PIC-CORR-1` through `PIC-CORR-15`
are preserved in full. `ARCHITECTURE A`, `MODEL E2′`, the seven evidence record
classes, the six-command surface, the absence of `record-freeze`, the stage
dispositions, the terminal-manifest creation semantics, the structural-unseal
semantics, the stderr parser, post-seal immutability, the P01-04F boundary, the
MODEL A′ boundary and the five-field runtime identity are all unchanged.

Statements elsewhere in this package that recite a `10 / 77` ledger,
seventy-seven closed values, twenty `failure_class` values or a six-field
manifest set describe the pre-amendment baseline. They remain true of the items
they were written to describe and are correctly scoped to them, exactly as
`PIC-CORR-5` and `PIC-CORR-12` scope their predecessors. The current ledger is
`10 / 78` and the current manifest set is seven fields.

`acceptance.md` recites the ledger in exactly two places, both **descriptive**:
criterion `A-18 — Closed vocabularies`, whose count block is a census of the
contract as it stood at that gate, and the §4 package-disposition census. Neither
imposes a count on an implementation. `acceptance.md` accepts a documentation
package and states so itself — "This document records criteria satisfaction, not
adoption", and §5 "would not accept an implementation". The normative content of
`A-18` is the *property* it names: exact, case-sensitive closed enumerations,
values outside them rejected, and **no arbitrary extension permitted without a
founder disposition**. That property is not weakened by this amendment; it is the
clause under which this amendment is issued. `A-18`'s further sentence that no
statement in the package asserts eight enumerations or sixty-nine values is also
undisturbed — the enumeration count remains ten.

`acceptance.md` and the package `README.md` are therefore **not edited** by this
amendment, and their bytes stand at `f6428994…` and `247abcf7…`. A later gate
comparing `A-18`'s census against `evidence-contract.md` §20 will see `77` against
`78`; that difference is this amendment, is declared here, and is not drift.

### PA3-AMD-1 — `failure_class` extension

Recorded normatively in `evidence-contract.md` §20 and §20.3, and reflected in
the §19.1 triad table.

```text
named closed enumerations:
10 — UNCHANGED

total closed enumeration values:
77 -> 78

failure_class:
20 -> 21

admitted value:
EPISODE_PATH_IDENTITY_DRIFT

triad:
EPISODE_PATH_IDENTITY_DRIFT -> PATH_SAFETY_FAILURE /
                               FOUNDER_DISPOSITION_REQUIRED

root_cause_class:            15 — UNCHANGED
remediation_disposition:      4 — UNCHANGED
terminal_disposition:         5 — UNCHANGED
causal_stage:                 8 — UNCHANGED
record_integrity:             2 — UNCHANGED
comparison_disposition:       4 — UNCHANGED
operator_error_class:        11 — UNCHANGED
stage_disposition:            3 — UNCHANGED
path_role:                    5 — UNCHANGED
```

A real-directory-for-real-directory substitution passes both reparse and
containment, so no existing class describes it, and a detected in-flight
substitution evidences a host-level adversary, which no fresh episode on the same
host remediates. The remediation disposition is therefore
`FOUNDER_DISPOSITION_REQUIRED` and not `NEW_EPISODE_REQUIRED`.

The §19.1 triad table is extended by the same one row, and its totality statement
now reads twenty-one. A closed enumeration whose derivation table is not total
over it would be a contradiction, so the table row is part of this amendment and
not a separate act.

### PA3-AMD-2 — `episode-manifest.json` field-set extension

Recorded normatively in `evidence-contract.md` §15.4.

```text
episode-manifest.json field set:
EXACT AND CLOSED AT 6 -> EXACT AND CLOSED AT 7

added field:
episode_path_identity

definition:
the digest of the episode directory's (st_dev, st_ino) pair, reduced through
the frozen canonical serializer, measured at episode open and re-confirmed at
terminalization

verifier obligation:
recompute the identity of the directory the manifest was found in, compare it
to this field, and treat a mismatch as TERMINAL

terminal-identity formula:
UNCHANGED — SHA-256 and byte size of the terminal manifest's exact bytes

manifest record_integrity field:
STILL ABSENT — PIC-CORR-14 UNCHANGED

repository-observation field:
STILL PROHIBITED — PIC-3 UNCHANGED
```

The set is still closed. It is closed at seven. Closure is the control, and the
count is not; a closure that excluded the field binding a manifest to the
directory it was sealed in was protecting the wrong thing.

#### Schema-version determination — consequential to `PA3-AMD-2`

Whether extending the field set forces an `episode-manifest` `schema_version`
bump was determined before this amendment was committed, because discovering it
later would reproduce the `F-3` shape. Three questions, answered:

```text
1. does the contract fix the manifest schema_version string?
YES — evidence-contract.md §15.4 fixes the exact literal
      mesc-p01-04d-execution-evidence/episode-manifest/v1
      recited at founder-authorization.md §8 and at acceptance.md criterion
      A-36 "Exact schema versions"; §18.8.3 requires the exact literal for TM-2
      and §18.8.2 makes a wrong schema_version a TM-1 condition

2. is that string a member of any closed enumeration?
NO — the ten named enumerations are §20.1 through §20.10 and schema_version is
     not among them, nor among the four uncounted inline domains (mode, stage,
     generation_identity, byte_equality). A bump would leave the ledger at
     10 / 78 exactly.

3. do the "exact and closed" set semantics require a version change?
NO — the contract states no versioning, migration or compatibility policy of
     any kind. §15.4 and §18.8.3 are internally consistent without a bump: the
     exact literal remains v1, and "all mandatory fields" now means seven.
```

```text
DETERMINATION:
NO BUMP. schema_version STAYS .../episode-manifest/v1.
```

No answer forces a bump, so none is authorized. A bump is also affirmatively
undesirable. P01-04D execution is not authorized and no episode manifest exists
anywhere, so a bump would version an empty population; the terminal-identity
formula of §22 is unchanged either way; and changing the literal would falsify
criterion `A-36` of `acceptance.md`, whose bytes must stand at `f6428994…`. `A-36`
recites the exact literal as a criterion, not as a census, so unlike `A-18` it
could not be dispatched as descriptive. Not bumping leaves `A-36` satisfied
exactly as written. Bumping would manufacture a second `acceptance.md`
divergence — the harder kind — to solve a problem that does not exist.

Recorded normatively in `evidence-contract.md` §15.4. A conforming manifest
carrying only the former six fields fails the mandatory-field test of §18.8.3 and
is TM-1. Bumping the version requires its own founder disposition.

### Standing constraints on the S2 continuity anchor

Recorded here so the implementation cannot drift off them. These constrain; they
authorize nothing and extend nothing.

The continuity token is **operator-held**. Two prohibitions follow:

```text
reading an expected token from anything on disk:
PROHIBITED — argv only, with no fallback of any kind

persisting the next token inside the episode directory:
PROHIBITED — stdout emission is the whole mechanism
```

A token the harness can recover from a file is a token the attacker can supply,
because the attacker controls every byte inside a swapped directory. A fallback
path returns the anchor to the interior and reinstates `F-1` in full. Writing the
next token down does the same.

The consumed token will land in `argv` evidence under §8. That is harmless: an
attacker cannot make a swapped directory hash to a value the operator will
supply. It must be the **consumed** token only, never the emitted next one.

An in-directory anchor of any shape — a sidecar identity file, an eighth evidence
record, a field added to `episode-core.json` — is refused. This is not a stylistic
preference. It is the finding.

### PA3-DET-1 — argument-surface determination, declaratory

Recorded in `evidence-contract.md` §4.

This is **not** an authorization and is not part of the scope granted below. It
records a fact about what this contract already fixes: §4 fixes the command set,
each command's child-process relation and each command's mutation; §8 fixes the
argv recording obligation; §21.1 requires arguments to be validated. Nothing in
this contract enumerates the arguments a command accepts.

```text
per-command argument sets:
NEVER FIXED BY THIS CONTRACT — NO EXTENSION WAS REQUIRED OR GRANTED
```

Recording the determination prevents a later reviewer from reading an added
command argument as the widening of a stated contract. It grants nothing, and an
implementation still remains bound by the six-command surface, by §8 and by §24.

### Scope of this amendment

```text
authorized:
the failure_class extension of PA3-AMD-1
the episode-manifest.json field extension of PA3-AMD-2

authorized for nothing else
```

This authorization is scoped to those two extensions. It confers no general right
to extend a closed vocabulary, a closed field set, the evidence inventory, the
command surface or the event sequence. Any further extension requires its own
founder disposition, exactly as §20 has required throughout.

It does not authorize P-A2 implementation, P01-04D execution, P01-03G access,
real dataset access, Generation A, Generation B, compare or verify over real
inputs, or publication. §9 through §12 are unchanged and remain in force in full.

## 9. Blocker state

```text
XD-EXEC-1   external execution-evidence recording
DECIDED / OPEN — CONTRACT RECORDED BY THIS PACKAGE

XD-EXEC-2   external source-record custody and binding
OPEN

XD-EXEC-3   independently recorded formal input identities
OPEN

XD-EXEC-4   execution-authorization activation baseline
DECIDED — GOVERNANCE MECHANISM CANONICALLY ADOPTED
```

This package records the XD-EXEC-1 contract only. It makes no claim about
XD-EXEC-2 or XD-EXEC-3 and does not reduce, reframe or defer either of them.

Execution readiness requires every blocker to be closed. Recording a contract
does not make the remaining blockers smaller.

## 10. No authority expansion

This decision does not:

```text
authorize P-A2 implementation
authorize execution
authorize protected input access
authorize source-record access
authorize P01-03G access
authorize real dataset access
create a workspace
invoke generate
invoke compare
invoke verify over real inputs
close XD-EXEC-1
close XD-EXEC-2
close XD-EXEC-3
authorize P01-04F
```

## 11. Prohibition boundary

Every line below remains in force after this decision.

```text
P-A2 implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-03G registry content access:
NOT AUTHORIZED

external source-record access:
NOT AUTHORIZED

real dataset access:
NOT AUTHORIZED

Generation A:
NOT AUTHORIZED

Generation B:
NOT AUTHORIZED

compare:
NOT AUTHORIZED

verify over real inputs:
NOT AUTHORIZED

generation workspace creation:
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

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

## 12. Scope and non-authority

```text
records an execution-evidence contract decision only
creates no implementation authority
creates no execution authority
grants no input access
creates no generation workspace
generates no artifact
creates no partition membership
executes no leakage analysis
publishes nothing
unlocks no later stage
```

This decision amends no earlier founder decision. It does not alter
`FD-DREADY-1` through `FD-DREADY-12`, the formal operator contract, the
seven-file candidate artifact inventory, the artifact-name supersession map, the
P01-04D/E/F/G stage separation, the MODEL A′ activation rule or the ratified
scientific decisions D1 through D10. On any conflict, D1 through D10 control.

The identity of the commit that introduces this record is recorded externally, in
its build report and in its independent review record, and is never written
inside the content it would have to hash.
