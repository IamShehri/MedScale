# P01-04D External Source-Record Custody — Founder Decision

This is the controlling document of the XD-EXEC-2 disposition. It defines the
blocker's closure condition and records that the condition is met.

## 1. Decision identity

```text
Decision:
XD-EXEC-2:
EXTERNAL SOURCE-RECORD CUSTODY AND BINDING

Decision class:
EXECUTION-READINESS BLOCKER DEFINITION AND CLOSURE — GOVERNANCE ONLY

Canonical baseline:
97a67560430b428759d6121bc5bdf1c0f3f8a317

XD-EXEC-2:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-3:
OPEN

P01-04D execution:
NOT AUTHORIZED

New enumeration, enumeration value, evidence file, manifest field or command:
NONE
```

## 2. The defect being resolved

The P01-04 execution protocol requires one formal input that does not live in
the repository: the accepted external `source-records.jsonl`, read-only and
outside the repository, used solely as the per-example `final_decision` label
source. The protocol fixes its required identity and forbids copying it in.

What the repository did **not** record is whether that exact artifact is
actually held and recoverable. An execution authorization issued without that
fact could be void on contact: the only copy of the label source might not
exist. The blocker names custody, and custody was the missing fact.

```text
identity of the artifact:      ALREADY ATTESTED — P01-03G
rules for reading it:          ALREADY FIXED — P01-04 execution protocol
proof it is actually held:     ABSENT — this is XD-EXEC-2
```

## 3. Definition

XD-EXEC-2 is the requirement that the exact external `source-records.jsonl`
named by the accepted P01-03G transformed-dataset identity be provably held in
operator custody, outside every protected root, before P01-04D execution is
authorized.

Its **binding into execution evidence is not part of this blocker.** That is
already provided by the canonically adopted P-A2 harness, which carries
`source_records` as one of its five closed input surfaces and durably records
the surface, SHA-256, byte size and `path_role` under `PA1-FD-9`.

```text
XD-EXEC-2 owns:
the pre-execution custody fact for the one artifact held outside the
repository — that it exists, is recoverable, matches the P01-03G attestation,
and sits outside every protected root.

XD-EXEC-3 owns:
the independent recording of formal input identities by the formal executor at
execution time, across all five input surfaces, into the execution-input
manifest that MODEL A′ §5.6 requires. NOT closed by this disposition.

XD-EXEC-1 already delivered:
harness-side binding of all five input surfaces into inputs_hashed.
```

## 4. Closure condition

XD-EXEC-2 may be marked `CLOSED FOR P01-04D EXECUTION READINESS` only when all
three hold:

```text
1. The held external source-records.jsonl is measured read-only and yields
   exactly
       sha256     22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce
       byte_size  2770193
   matching the accepted P01-03G transformed-dataset identity.

2. Its custody location is outside the repository root, the external evidence
   root, the Generation A workspace, the Generation B workspace and the future
   P01-04D evidence root, and no copy of the artifact exists inside any of
   those roots.

3. The measurement is recorded once as a canonical governance evidence record
   persisting only surface_name, sha256, byte_size, match_result and
   path_role — never an absolute path, artifact bytes, question text, context
   text, answer text, annotations, labels, final_decision values or any other
   source-record content.
```

## 5. Closure

All three conditions are established. The measurement evidence is recorded in
[`custody-verification.md`](custody-verification.md).

```text
condition 1  SATISFIED — exact match on both attested values
condition 2  SATISFIED — see §5.1
condition 3  SATISFIED — custody-verification.md persists exactly the five
                         permitted fields

XD-EXEC-2:
CLOSED FOR P01-04D EXECUTION READINESS
```

### 5.1 Path separation, stated exactly

The repository root is a real, existing path, and separation from it was
verified concretely by component comparison rather than string prefix, together
with a reparse-point scan of every custody path component and a recursive
search establishing that no copy of the artifact exists anywhere inside the
repository root.

The other four roots — the external evidence root, both generation workspaces
and the future P01-04D evidence root — **do not exist at this baseline**.
P01-04D execution is not authorized, and no execution workspace or evidence
root may be created. A path that does not exist contains nothing, so the
custody location is outside all four. This is recorded plainly rather than
claimed as a containment measurement that could not have been performed.

The separation obligation therefore continues forward as a constraint on the
future declaration: when those four roots are declared at execution time, each
must be disjoint from the custody location. The adopted harness independently
enforces the evidence-root separation rules of `PA1-FD-17` at that point.

## 6. Custody durability observation

The artifact is held under a directory whose name denotes quarantine of an
earlier pipeline run. Its bytes match the accepted attestation exactly, so its
identity is not in question, and directory naming confers no property on
content. It is recorded here only because a location named for quarantine may
be subject to routine cleanup, and the closure asserts custody **at this
baseline**. If the artifact is later moved or removed, custody must be
re-established before execution. No remediation is required now and none is
authorized by this document.

## 7. No authority expansion

This decision does not:

```text
close or authorize XD-EXEC-3
authorize P01-04D execution
authorize P01-03G registry content access
authorize real dataset access
authorize semantic parsing of source-record contents
create a generation workspace
create an external evidence root
invoke generate, compare or verify over real inputs
authorize model execution, training or fine-tuning
authorize P01-04E through P01-04G
complete P01-04 or unlock P01-05
authorize P-C1a or P-C1b
```

## 8. Prohibition boundary

Every line below remains in force after this decision.

```text
XD-EXEC-3:
OPEN

P01-04D execution:
NOT AUTHORIZED

P01-03G registry content access:
NOT AUTHORIZED

real dataset access:
NOT AUTHORIZED

Generation A:
NOT AUTHORIZED

Generation B:
NOT AUTHORIZED

compare and verify over real inputs:
NOT AUTHORIZED

generation workspace creation:
NOT AUTHORIZED

model execution, training, fine-tuning:
NOT AUTHORIZED

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

Execution additionally requires XD-EXEC-3 closed, a separate founder execution
authorization canonically adopted, and a passing MODEL A′ post-merge activation
verification.
