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

A later stage that discovers a new invalidation must not mutate the sealed P-A
episode. That later evidence requires its own separately governed immutable
record referencing the prior terminal episode identity.

### PA1-FD-13 — State-dependent evidence inventory

Evidence is not required for a stage that never executed, and a stage that never
executed must not be represented by fabricated execution evidence.

A successful episode requires completed records for Generation A, Generation B,
compare and verify. A failed or refused episode requires only the stages actually
opened or started. Every failed or refused episode that can safely reach finalize
still receives a stable terminal identity.

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

## 8. Blocker state

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

## 9. No authority expansion

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

## 10. Prohibition boundary

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

## 11. Scope and non-authority

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
