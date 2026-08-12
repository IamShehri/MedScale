# P01-04D Execution Authorization — Founder Decision

This is the controlling document of the P01-04D execution-authorization
package.

## 1. Decision identity

```text
Decision:
P01-04D EXECUTION AUTHORIZED — CONDITIONAL

Decision class:
EXECUTION-AUTHORIZATION GOVERNANCE ONLY — INACTIVE UNTIL MODEL A′ PASS

Canonical baseline:
e8cd1f516efa4f9dde0281cbd07d1d47250d1c58

Canonical tree:
f184c7bb247ca8f8639e1ed3aeb076663a60f7b6

Activation model:
MODEL A′

P01-04D execution authorization:
CONDITIONAL — INACTIVE UNTIL MODEL A′ POST-MERGE ACTIVATION VERIFICATION
RETURNS PASS
```

This document issues the separate founder execution authorization required by
the canonically adopted P01-04D governing protocol and by `MODEL A′` §5 item
11. It is not that activation verification, and it does not begin, schedule,
stage or draft execution.

## 2. Substantive disposition

```text
I authorize the bounded P01-04D execution defined by the canonically adopted
P01-04D governing protocol, using exactly the canonically bound execution-input
manifest identity SHA-256
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939
with byte size 973.

This authorization is inactive until:

1. this execution-authorization package is canonically adopted on main; and
2. the required MODEL A′ read-only post-merge activation verification returns
   PASS against the actual execution-authorization merge identity and the exact
   execution-input-manifest identity above.

If MODEL A′ does not PASS, P01-04D execution remains NOT AUTHORIZED.

This authorization permits only the exact P01-04D execution workflow already
defined by the adopted governing protocol.

It does not authorize training, fine-tuning, unrelated model experiments,
unrelated datasets, expansion of the execution-input set, publication beyond
the protocol, or any subsequent MESC phase.
```

## 3. Canonical readiness baseline

Resolved from canonical main at the time of drafting:

```text
canonical main:
e8cd1f516efa4f9dde0281cbd07d1d47250d1c58

canonical main tree:
f184c7bb247ca8f8639e1ed3aeb076663a60f7b6

XD-EXEC-1:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-2:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-3:
CLOSED FOR P01-04D EXECUTION READINESS

P01-04D entry:
AUTHORIZED

P01-04D execution:
NOT AUTHORIZED — until this package's MODEL A′ verification passes
```

## 4. Bound prerequisites

The following already-existing immutable prerequisites are bound. Each is a
canonical repository fact; none depends on the future merge identity of this
package.

### 4.1 Adopted governance and implementation lineage

```text
formal executor implementation adoption:
PR #90 — merge e924027f1c8ea08ac4e5e4281fdcf75e5b419693

MODEL A′ activation rule adoption:
PR #94 — merge 035392831c6218b5302b04ca7e392eff8724ff52

P-A2 execution-evidence harness adoption:
PR #97 — merge 13add97d7f5dde97ea1835d444f5cef31e5d1d2c

P01-04D entry authorization:
PR #92 — merge 693c900bbe5e0f752ca915b527c89d1d9aaa43ad

XD-EXEC-1 closure:
CLOSED — evidence-harness package

XD-EXEC-2 closure:
PR #99 — merge 0941e84abcd49ba711382591254a013a50a687c8

XD-EXEC-3 P-C1a contract adoption:
PR #100 — merge 6f0bd5955c2bead435d3f3f4971094922fc7b74a

XD-EXEC-3 P-C1b implementation adoption:
PR #101 — merge c6657b7213f817462b75f4abfda32018cba1f32a

XD-EXEC-3 closure:
PR #102 — merge e8cd1f516efa4f9dde0281cbd07d1d47250d1c58
```

### 4.2 Execution-input-manifest identity — the bound value

```text
execution-input-manifest SHA-256:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939

execution-input-manifest byte_size:
973

schema version:
mesc-p01-04d-execution-input/manifest/v1
```

This is the exact identity the P-C1b verification canonically recorded in
`specs/mesc-pilot-01/p01-04d-execution-input-identity/verification.md` and the
identity `MODEL A′` §5.6 activation binds. It is a pure deterministic function
of the five formal input byte streams and carries no path, timestamp or
commit.

### 4.3 Accepted external source-record identity

```text
SHA-256:
22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce

byte_size:
2770193
```

Authority remains the accepted identity. No physical copy is designated
authoritative merely because it exists in a particular directory, and no
absolute custody path is persisted here. Every held copy that measures to this
identity satisfies custody equally.

### 4.4 Formal operator and evidence-harness identities

Bound as the exact canonical blob identities at the canonical baseline:

```text
formal operator:
scripts/mesc_p01_04d_operator.py
blob f41c23136adcac49cc1141b067fcc5c9e9def625

external evidence harness:
scripts/mesc_p01_04d_evidence_harness.py
blob f9b87e3f2bdbf25497693dd89662cab818dba593
```

### 4.5 Governing protocol identities

```text
execution protocol:
specs/mesc-pilot-01/p01-04/execution-protocol.md
blob 76da4fecc67d097b6f33f71bb7635051a0bfb974

ratified decision record:
specs/mesc-pilot-01/p01-04/decision-record.md
blob 1fb36e2a6c6f0a32dbf3180170d8b93dc9409b47

activation rule:
specs/mesc-pilot-01/p01-04d-execution-activation-rule/founder-authorization.md
blob 434355639882c9c5e1fa9364d59f92f3f6e6820b
```

## 5. Scope of the authorization

This authorization permits only the exact P01-04D execution workflow already
defined by the adopted governing protocol:

```text
two independent generations — Generation A and Generation B — each one
per process, through the canonical formal operator, over exactly the five
accepted formal input surfaces bound by the execution-input-manifest identity
of §4.2

the canonical compare step over the completed workspaces, byte-for-byte,
with the seven-file candidate inventory

external evidence recording through the adopted P-A2 evidence harness

stop conditions, invalidation rules and anti-writeback controls of the
execution protocol apply unchanged
```

It does not authorize:

```text
training
fine-tuning
unrelated model experiments
unrelated datasets
expansion of the execution-input set
publication beyond the protocol
P01-04E through P01-04G
any subsequent MESC phase
```

## 6. Activation rule

By `MODEL A′`, this authorization becomes operative only as follows:

```text
1. this package is canonically adopted on main through the normal protected
   main process;

2. one read-only post-merge activation verification resolves the unique actual
   merge commit produced by that adoption;

3. that verification establishes every activation prerequisite of `MODEL A′`
   §5 item 6, including at minimum:
   - exact execution-authorization merge commit;
   - exact merge tree;
   - expected ordered parents;
   - zero candidate-to-merge tree drift;
   - required checks successful;
   - exact formal-operator identity (§4.4);
   - exact runtime identity;
   - exact execution-input-manifest identity (§4.2);
   - exact external-evidence-harness identity (§4.4);
   - all remaining bindings of §3 and §4;

4. only on a PASS does the verified execution-authorization merge commit
   become the exact value supplied as --expected-canonical-commit;

5. the post-merge verification is evidence only — not another founder
   authorization, not a repository mutation, not a second canonical adoption
   commit.
```

This package does not record its own future merge identity. That identity does
not exist until canonical adoption, and `MODEL A′` §4 prohibits predicting,
fabricating, reserving or embedding it.

## 7. Failed verification

```text
post-merge activation verification FAILS:
P01-04D EXECUTION REMAINS NOT AUTHORIZED
```

A failed verification activates nothing, supplies no expected canonical
commit, and is never partially honoured. The matter returns to founder
disposition.

## 8. Prohibition boundary

Every line below remains in force until the §6 activation verification
returns PASS, and every line not explicitly lifted by it remains in force
afterwards.

```text
P01-04D execution:
NOT AUTHORIZED — until MODEL A′ PASS

P01-03G registry content access:
NOT AUTHORIZED — execution-time protocol access only

external source-record access:
NOT AUTHORIZED — execution-time protocol access only

real dataset access:
NOT AUTHORIZED — execution-time protocol access only

Generation A:
NOT AUTHORIZED — until MODEL A′ PASS

Generation B:
NOT AUTHORIZED — until MODEL A′ PASS

compare:
NOT AUTHORIZED — until MODEL A′ PASS

generation workspace creation:
NOT AUTHORIZED — until MODEL A′ PASS

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

## 9. Scope and non-authority

```text
records a conditional execution-authorization decision only
activates nothing on its own
creates no implementation authority
grants no input access before activation
creates no generation workspace
generates no artifact
executes no leakage analysis
publishes nothing
unlocks no later stage
```

This decision amends no earlier founder decision. It does not alter
`FD-DREADY-1` through `FD-DREADY-12`, the formal operator contract, the
seven-file candidate artifact inventory, the artifact-name supersession map,
the P01-04D/E/F/G stage separation or the ratified scientific decisions D1
through D10. On any conflict, D1 through D10 control.

The identity of the commit that introduces this record is resolved only after
canonical adoption, through the `MODEL A′` post-merge activation verification,
and is never written inside the content it would have to hash.
