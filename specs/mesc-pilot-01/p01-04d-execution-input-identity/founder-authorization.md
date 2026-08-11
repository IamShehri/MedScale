# P01-04D Execution-Input Identity — P-C1a Contract

This is the controlling document of P-C1a, the documentation-and-contract phase
for `XD-EXEC-3`. It defines the contract a future bounded P-C1b formal-executor
implementation must satisfy. It is not that implementation, and it does not
authorize it.

## 1. Decision identity

```text
Decision:
XD-EXEC-3:
INDEPENDENTLY RECORDED FORMAL INPUT IDENTITIES

Phase:
P-C1a — DOCUMENTATION AND CONTRACTS ONLY

Canonical baseline:
0941e84abcd49ba711382591254a013a50a687c8

XD-EXEC-1:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-2:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-3:
OPEN — NOT CLOSED BY THIS PACKAGE

P-C1b implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

New enumeration, enumeration value, evidence file, command or subsystem:
NONE
```

## 2. The defect being resolved

`MODEL A′` §5.6 requires the post-merge activation verification to establish an
**exact execution-input-manifest identity**. No such identity exists. The
`p01-04d-execution-evidence-harness` evidence contract records the gap directly:

```text
execution-input-manifest identity:
ABSENT UNTIL XD-EXEC-3 CLOSES
```

That same contract already assigns the authority: "After XD-EXEC-3 closes, the
future execution-input manifest remains the authority for accepted input
identity", while P-A evidence records only what bytes were actually presented.

## 3. What already exists, and what is missing

The formal executor **already measures** all five surfaces. `_formal_split_v1`
exposes `build_input_identity`, which refuses unless exactly the five required
surfaces are supplied and returns one descriptor per surface carrying `surface`,
`schema_version`, `sha256` and `byte_size`, ordered by sorted surface name.

```text
independent measurement:   ALREADY EXISTS — build_input_identity
canonical serializer:      ALREADY EXISTS — _canonical_json_v1
manifest document:         MISSING
manifest identity digest:  MISSING
emission at execution:     MISSING
```

P-C1b is therefore an **emit-and-derive** step over an existing in-memory
structure. It is not new measurement logic, and it is not a subsystem. No
service, database, registry, daemon, signing system, provenance framework,
evidence harness, ingestion pipeline, model runner or workspace manager is
created, required or authorized.

## 4. The formal input set — exact and closed

Exactly five surfaces, fixed by `p01-04/execution-protocol.md` "Accepted inputs"
and already implemented as `REQUIRED_INPUT_SURFACES`:

| Surface literal | Accepted input |
|---|---|
| `ordered_example_registry` | `specs/mesc-pilot-01/p01-03g/ordered-example-id-registry.jsonl` |
| `source_document_registry` | `specs/mesc-pilot-01/p01-03g/source-document-id-registry.jsonl` |
| `transformed_dataset_identity` | `specs/mesc-pilot-01/p01-03g/transformed-dataset-identity.json` |
| `source_records` | the accepted external `source-records.jsonl` (XD-EXEC-2 custody) |
| `decision_record` | `specs/mesc-pilot-01/p01-04/decision-record.md` |

```text
count:
5 — EXACT AND CLOSED

sixth input surface:
PROHIBITED

new surface literal:
NONE — the five already exist in both the executor and P-A2
```

### 4.1 Reconciliation with P-A2, and the boundary between them

The literals are identical in both layers. That is reconciliation, not
substitution, and the two records are **not** interchangeable:

```text
P-A2 harness — inputs_hashed:
binds what bytes were presented to THIS execution episode.
Harness-side evidence. Not the authority for accepted input identity.

P-C1b formal executor — execution-input manifest:
independently measures and records the formal input identities, and derives the
identity MODEL A′ activation binds. THE authority for accepted input identity.
```

Neither may be derived from the other. `PA1-FD-9` and the P-A evidence inventory
are unchanged by this contract: no P-A evidence file is added, and the seven-file
evidence inventory stays closed at seven.

## 5. The execution-input manifest

### 5.1 Schema version

```text
mesc-p01-04d-execution-input/manifest/v1
```

Exact literal, required. It is deliberately distinct from every existing schema
literal, and in particular from the seven-file bundle's `generation-manifest.json`
— see §8, `F3`.

### 5.2 Exact and closed field set

Two top-level fields. Nothing else may appear.

```text
schema_version
input_surfaces
```

Each `input_surfaces` entry carries exactly:

```text
surface        one of the five literals of §4
sha256         SHA-256 of the exact input bytes, lowercase hex, 64 characters
byte_size      exact byte count, integer
schema_version the surface's input schema version, PRESENT ONLY where one
               exists; omitted entirely where none exists, never null
```

```text
absolute or relative path:  PROHIBITED — no path field of any kind
timestamp:                  PROHIBITED — see §5.5
canonical commit:           PROHIBITED — see §7
partition membership:       PROHIBITED
question, context, answer, annotation, label or final_decision content:
                            PROHIBITED
any other field:            PROHIBITED
```

The omit-rather-than-null rule follows the existing convention that absent values
are absent, and matches `build_input_identity`, whose `schema_version` is already
optional per surface.

### 5.3 Deterministic ordering

`input_surfaces` is ordered by `surface`, ascending, byte-wise on the literal —
the ordering `build_input_identity` already produces. Exactly five entries, no
duplicates, no omissions.

### 5.4 Canonical serialization

The frozen canonical serializer is **called and never modified**: UTF-8, sorted
object keys, tight separators, non-finite numbers rejected, one terminal line
feed. The manifest is exactly one canonical JSON document produced by
`canonical_json_bytes` from `medscale.mesc._canonical_json_v1`.

### 5.5 No timestamp

The manifest carries no timestamp and no date-derived value. This is required,
not stylistic: the manifest must be a pure deterministic function of the five
input byte streams so that the read-only activation verification can recompute it
and reach the same identity. `FD-DREADY-9`'s date-free determinism rule applies.

### 5.6 Manifest identity

```text
execution-input-manifest identity =
  SHA-256 of the exact canonical manifest bytes,
  together with the byte size of those same exact bytes
```

This mirrors the terminal-identity formula convention already in force. Because
§5.2 and §5.5 exclude every non-input-derived value, the identity is a pure
function of the five input surfaces and is independently recomputable.

### 5.7 Path treatment

The manifest names surfaces, never locations. No absolute path, no relative
path, no filename derived from a local location, no username, no hostname. The
XD-EXEC-2 custody location is not carried here, consistent with that package
binding custody to identity rather than to a persisted path.

### 5.8 Emission, overwrite and reuse

```text
durable file written by the executor:
NONE

emission:
one canonical JSON document on the operator's existing standard output

repository, generation workspace, P-A evidence root, future evidence root:
NO MANIFEST FILE IS WRITTEN TO ANY OF THEM
```

This is deliberate and is what keeps every closed inventory closed: the seven
P-A evidence records stay seven, and the seven-file candidate bundle stays seven
with no eighth workspace file. Because nothing is written, there is no overwrite
and no reuse semantics to define. An operator may capture the emitted bytes into
custody; that capture is outside this contract and creates no repository
artifact.

The harness's existing `PA1-FD-8` treatment of child stdout is unchanged: only
the SHA-256 and byte size of child output may persist, never the raw bytes.

### 5.9 Error and refusal semantics

```text
any of the five surfaces missing, unreadable, or not exactly the required set:
REFUSE FAIL-CLOSED — no manifest is emitted

a surface measurement cannot be completed:
REFUSE FAIL-CLOSED — no partial manifest, no placeholder, no null descriptor

refusal class:
the executor's existing typed formal failures — no new exception type, no new
enumeration value
```

A partial or best-effort manifest is prohibited. An absent manifest is an honest
absence; a partial one would be a false claim of accepted input identity.

## 6. Independence rule

The weakest definition that makes "independently recorded" true and testable.
Three requirements, all mechanically checkable:

```text
1. SEPARATE MEASUREMENT.
   The manifest is derived from the executor's own direct read-only measurement
   of the five input byte streams.

2. SEPARATE CODE PATH.
   The manifest is constructed inside the formal executor modules, never inside
   scripts/mesc_p01_04d_evidence_harness.py.

3. NO CONSUMPTION OF P-A2 EVIDENCE.
   The executor must not read, import, parse or otherwise consume inputs_hashed,
   any P-A2 evidence record, or any harness module as a source of truth.
```

Testability, stated so P-C1b cannot claim it without demonstrating it:

```text
- the executor produces a byte-identical manifest with no harness present and no
  P-A evidence root in existence;
- static assertion that the formal executor imports no harness module;
- a differential test: corrupting a P-A2 inputs_hashed record changes nothing
  about the manifest or its identity.
```

Organizational or process independence is **not** required. No governing document
imposes it, and inventing it here would be a new gate.

## 7. MODEL A′ binding

`MODEL A′` §5.6 requires the read-only post-merge activation verification to
establish the exact execution-input-manifest identity. It binds exactly the
§5.6 pair:

```text
bound value:
the SHA-256 and byte size of the exact canonical execution-input manifest bytes
```

There is no self-reference. The manifest depends only on the five input surfaces
— never on the execution-authorization merge commit, its tree, its parents or its
adoption. `MODEL A′` §4's prohibition on predicting, fabricating, reserving or
embedding a future merge identity is therefore satisfied by construction: the
manifest could not embed that identity even if someone tried, because no field
admits it.

Activation verification recomputes the manifest read-only from the five inputs
and compares. A mismatch fails verification, and by `MODEL A′` §7 a failed
verification activates nothing.

This package does not draft the execution-authorization package.

## 8. Required preserved findings

`MODEL A′` §10 requires fresh independent verification that `B-1`, `B-2`, `F1`,
`F2` and `F3` remain CLOSED after P-C1b. Their exact existing definitions, the
property each could threaten, and the minimum re-verification:

### B-1 — controlled formal operator invocation path

Defined in `p01-04/decision-record.md`: "No controlled formal operator invocation
path exists for Generation A and Generation B." Closed at implementation level by
`FD-DREADY-2` .. `FD-DREADY-5`.

```text
threat:
P-C1b touches the operator to emit the manifest and alters the controlled
surface — a third command, a changed argument set, or more than one generation
per invocation.

minimum re-verification:
assert exactly two operator commands, the argument surface unchanged, one
generation per invocation, and fail-closed rejections unchanged.
```

### B-2 — policy artifact inventory reconciled with implementation inventory

Defined in `p01-04/decision-record.md`. Closed by `FD-DREADY-6` .. `FD-DREADY-10`.

```text
threat:
the manifest is written into the generation workspace and becomes an eighth
artifact, desynchronising the inventories.

minimum re-verification:
assert the exact seven-file candidate inventory, and assert that a generation
run creates no eighth workspace file.
```

### F1 — independent workspace verification and fingerprint/descriptor recomputation

Closed the gap where comparison accepted two identically corrupted workspaces
because it proved only carrier consistency and A/B byte equality.

```text
threat:
manifest construction reuses or short-circuits descriptor recomputation, so
recomputation silently becomes a cached read.

minimum re-verification:
rerun the identically-corrupted-workspaces discriminator; comparison must still
reject.
```

### F2 — second repository-identity verification immediately before first mutation

Closed the gap where commit identity was verified at request construction but not
re-read immediately before the first filesystem mutation.

```text
threat:
manifest construction is inserted BETWEEN the second verification and the first
mutation, reopening the window. This is the same ordering defect class that
PA3-R2 found in the harness seal path, and it is the most likely way P-C1b
regresses something.

minimum re-verification:
assert the second repository-identity verification is still the last step before
the first mutation, with no manifest work between them.
```

### F3 — exact generation-manifest schema, semantic and canonical-byte validation

Closed the gap where two byte-identical workspaces were accepted when both
manifests carried a modified `algorithm_version` or an extra top-level key.

```text
threat:
NAME COLLISION. generation-manifest.json already exists in the seven-file
bundle. Conflating it with the new execution-input manifest could relax its
validation or add a top-level key to it.

minimum re-verification:
assert generation-manifest validation is unchanged and still rejects a modified
algorithm_version and an extra top-level key; assert the two manifests are
distinct artifacts with distinct schema literals and that neither is written
where the other belongs.
```

No `B-3`, `F4` or any further finding is created by this package.

## 9. P-C1b exact path allowlist

`PA1-FD-19` freezes the formal-executor paths. P-C1b is the bounded executor
change the founder approved in principle, so its authorization must name the
allowlist exactly. This section defines it; it does not grant it.

```text
MAY BE MODIFIED — exactly 6 paths:
src/medscale/mesc/_formal_split_v1.py          manifest construction,
                                               serialization, identity derivation
src/medscale/mesc/_formal_generation_v1.py     return the manifest from the
                                               generation result
scripts/mesc_p01_04d_operator.py               emit it on existing stdout
tests/test_mesc_formal_split_v1.py             tests
tests/test_mesc_formal_generation_v1.py        tests
tests/test_mesc_p01_04d_operator.py            tests

MUST REMAIN BYTE-IDENTICAL:
src/medscale/mesc/_canonical_json_v1.py        frozen serializer — called only
scripts/mesc_p01_04d_evidence_harness.py       adopted P-A2
tests/test_mesc_p01_04d_evidence_harness.py    adopted P-A2

NEW REPOSITORY PATH:
NONE — no seventh source path, no new module, no new script

NEW CLI SURFACE:
NOT REQUIRED — the manifest travels on the operator's existing stdout, and the
two-command surface is unchanged

TESTS:
may be added ONLY within the three listed test paths
```

Modifying any path outside this list, or adding one, requires its own founder
disposition.

**A smaller two-path allowlist exists and is not recommended.** If the founder
accepted a *recomputable-only* manifest — never emitted at execution — P-C1b
would touch only `_formal_split_v1.py` and its test. It is rejected here because
`XD-EXEC-3` requires input identities to be **independently recorded**, and a
value that is only recomputable later is not recorded at execution time.

## 10. XD-EXEC-3 closure condition

```text
XD-EXEC-3 may be marked CLOSED FOR P01-04D EXECUTION READINESS only after:

1. P-C1a is canonically adopted;
2. a separately founder-authorized P-C1b implementation is produced within the
   exact allowlist of §9;
3. the formal executor independently records the required input identities and
   derives the execution-input-manifest identity exactly as specified in §5
   and §6;
4. the bounded implementation gates pass;
5. fresh independent verification confirms B-1, B-2, F1, F2 and F3 remain
   CLOSED, by at least the discriminators of §8;
6. P-C1b is canonically adopted.
```

No existing governing authority requires a materially different condition, so
the shape above stands unchanged.

## 11. No authority expansion

This package does not:

```text
authorize P-C1b
close XD-EXEC-3
authorize P01-04D execution
reopen or alter XD-EXEC-1 or XD-EXEC-2
modify production code, tests or scripts
unfreeze any path
authorize P01-03G access, real dataset access, Generation A or B, compare or
  verify over real inputs, workspace creation, model execution, training or
  fine-tuning
draft the execution-authorization package
complete P01-04 or unlock P01-05
```

Execution additionally requires XD-EXEC-3 closed, a separate founder execution
authorization canonically adopted, and a passing `MODEL A′` post-merge activation
verification.
