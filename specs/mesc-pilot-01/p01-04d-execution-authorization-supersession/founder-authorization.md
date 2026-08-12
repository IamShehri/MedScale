# P01-04D Superseding Execution Authorization — Founder Decision

This is the controlling document of the P01-04D execution-authorization-
supersession package. It supersedes, for all future P01-04D execution
episodes, the earlier execution authorization recorded in
`specs/mesc-pilot-01/p01-04d-execution-authorization/` (which is not edited or
deleted and remains historical evidence).

## 1. Decision identity

```text
Decision:
P01-04D EXECUTION AUTHORIZATION — SUPERSEDING — CONDITIONAL
(EXACTLY ONE FRESH EPISODE)

Decision class:
EXECUTION-AUTHORIZATION GOVERNANCE ONLY — INACTIVE UNTIL MODEL A′ PASS

Canonical baseline:
636540c761aba65d569af3d40b321616497aeb7c

Canonical tree:
7570e1cba2777fe08bec3db8008ab6decad3a340

Activation model:
MODEL A′

P01-04D execution authorization:
CONDITIONAL — INACTIVE UNTIL MODEL A′ POST-MERGE ACTIVATION VERIFICATION
RETURNS PASS AND THE EPISODE #1 CUSTODY RECONCILIATION RETURNS PASS
```

This document issues the separate superseding founder execution authorization
required by the canonically adopted P01-04D governing protocol and by
`MODEL A′` §5 item 11. It is not that activation verification, it does not
begin, schedule, stage or draft execution, and it does not execute P01-04D.

## 2. Substantive disposition

```text
I authorize exactly one fresh P01-04D execution episode under the corrected
canonical formal executor and the canonically adopted P01-04D execution
protocol, using exactly the five accepted formal input surfaces bound by
execution-input-manifest identity:

SHA-256:
b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004

byte_size:
820

This authorization supersedes the earlier execution authorization for all
future P01-04D execution episodes.

The earlier authorization and its 85c623... / 973 manifest binding remain
historical evidence and are not rewritten.

This superseding authorization is INACTIVE until:

1. this superseding authorization package is canonically adopted;
2. MODEL A′ post-merge activation verification returns PASS against the
   actual superseding-authorization merge and corrected canonical runtime;
3. the separate read-only Episode #1 custody reconciliation returns PASS.

If either activation condition fails, Episode #2 remains NOT AUTHORIZED.
```

## 3. Canonical readiness baseline

Resolved from canonical main at the time of drafting:

```text
canonical main:
636540c761aba65d569af3d40b321616497aeb7c

canonical main tree:
7570e1cba2777fe08bec3db8008ab6decad3a340

XD-EXEC-1:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-2:
CLOSED FOR P01-04D EXECUTION READINESS

XD-EXEC-3:
CLOSED FOR P01-04D EXECUTION READINESS
(re-verified and re-closed on corrected canonical inputs)

P01-04D entry:
AUTHORIZED

P01-04D execution:
NOT AUTHORIZED — until this package's MODEL A′ verification and the
Episode #1 custody reconciliation pass
```

## 4. Historical superseded authorization

```text
earlier execution authorization:
specs/mesc-pilot-01/p01-04d-execution-authorization/

earlier bound execution-input-manifest identity:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939 / 973

status:
HISTORICAL
VALID FOR THE HISTORICAL BASELINE/ATTEMPT IT GOVERNED
SUPERSEDED FOR FUTURE EPISODES
NOT VALID FOR EPISODE #2
```

The earlier authorization led to the first fail-closed execution attempt
(Episode #1, terminal disposition `EPISODE_FAILED`). It is not edited to
replace its historical bound identity, and its evidence is not rewritten.

## 5. Bound prerequisites

The following already-existing immutable prerequisites are bound. Each is a
canonical repository fact; none depends on the future merge identity of this
package.

### 5.1 Corrected implementation lineage

```text
real-input executor correction:
PR #104
reviewed head:
768b83e1b8b6f2bf71f40db6224ffce6d2562fbd

correction merge:
493564d144633a18b3ba535d94681efc70b122ea

XD-EXEC-3 re-verification commit:
0d3df0612400465a01d9252ed3aaa5437475aa7b

XD-EXEC-3 re-closure merge:
636540c761aba65d569af3d40b321616497aeb7c
```

### 5.2 Execution-input-manifest identity — the bound value

```text
execution-input-manifest SHA-256:
b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004

execution-input-manifest byte_size:
820

schema version:
mesc-p01-04d-execution-input/manifest/v1
```

This is the exact identity independently re-measured on corrected canonical
main and canonically recorded by the XD-EXEC-3 re-closure in
`specs/mesc-pilot-01/p01-04d-execution-input-identity/verification.md`. It is
a pure deterministic function of the five formal input byte streams and
carries no path, timestamp or commit.

### 5.3 Accepted external source-record identity

```text
SHA-256:
22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce

byte_size:
2770193
```

Authority is identity, not physical path. No absolute custody path is
persisted here. Every held copy that measures to this identity satisfies
custody equally.

### 5.4 Corrected canonical runtime identities

Bound as the exact canonical blob identities at the canonical baseline,
including the post-PR-104 formal executor:

```text
corrected formal executor runtime:
src/medscale/mesc/_formal_split_v1.py
blob 638df8689b63384f25ec66127879b3604bc912bd

formal executor companion:
src/medscale/mesc/_formal_generation_v1.py
blob 2d208146fa69b7a7bda03c21d371243de4a55247

formal operator:
scripts/mesc_p01_04d_operator.py
blob f41c23136adcac49cc1141b067fcc5c9e9def625

external evidence harness:
scripts/mesc_p01_04d_evidence_harness.py
blob f9b87e3f2bdbf25497693dd89662cab818dba593
```

### 5.5 Governing protocol identities

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

XD-EXEC-3 re-closure verification record:
specs/mesc-pilot-01/p01-04d-execution-input-identity/verification.md
blob eb6987de03d6acabfdb173c32cb0adef3c83d0e8
```

## 6. Scope of the authorization

When activated, this authorization permits exactly one NEW P01-04D episode. It
permits only the canonically adopted P01-04D workflow:

```text
Generation A
Generation B
canonical compare/verify/finalization stages
canonical P-A2 external evidence recording
exact five formal inputs
exact corrected formal executor
```

It does NOT authorize:

```text
reuse of Episode #1
repair of Episode #1
training
fine-tuning
LoRA / QLoRA
model-weight modification
new datasets
new formal input surfaces
new generation parameters
P01-04E or later stages
unrelated experiments
publication beyond existing protocol
```

## 7. Activation rule

By `MODEL A′`, this authorization becomes operative only as follows:

```text
1. this package is canonically adopted on main through the normal protected
   main process;

2. one read-only post-merge activation verification resolves the unique actual
   merge commit produced by that adoption — not the PR candidate SHA, not the
   branch head, not a predicted merge SHA;

3. that verification establishes every activation prerequisite of `MODEL A′`
   §5 item 6, including at minimum:
   - exact superseding-authorization merge commit;
   - exact merge tree;
   - expected ordered parents;
   - zero candidate-to-merge tree drift;
   - required checks successful;
   - exact formal-operator identity (§5.4);
   - exact corrected runtime identity (§5.4);
   - exact execution-input-manifest identity (§5.2);
   - exact external-evidence-harness identity (§5.4);
   - all remaining bindings of §3, §4 and §5;

4. only on a PASS does the verified superseding-authorization merge commit
   become the exact value supplied as --expected-canonical-commit;

5. the post-merge verification is evidence only — not another founder
   authorization, not a repository mutation, not a second canonical adoption
   commit.
```

Activation additionally requires the separate read-only Episode #1 custody
reconciliation to return PASS (Episode #1 evidence located and verified
against the historical execution record). Activation is complete only when all
of the following are true:

```text
superseding authorization = CANONICALLY ADOPTED
MODEL A′ = PASS
Episode #1 custody reconciliation = PASS
XD-EXEC-1 = CLOSED
XD-EXEC-2 = CLOSED
XD-EXEC-3 = CLOSED
```

This package does not record its own future merge identity. That identity does
not exist until canonical adoption, and `MODEL A′` §4 prohibits predicting,
fabricating, reserving or embedding it.

## 8. Failed verification

```text
MODEL A′ post-merge activation verification FAILS:
EPISODE #2 REMAINS NOT AUTHORIZED

Episode #1 custody reconciliation FAILS:
EPISODE #2 REMAINS NOT AUTHORIZED
```

A failed verification activates nothing, supplies no expected canonical
commit, and is never partially honoured. The matter returns to founder
disposition.

## 9. Prohibition boundary

Every line below remains in force until the §7 activation verification and
custody reconciliation return PASS, and every line not explicitly lifted by
them remains in force afterwards.

```text
P01-04D execution:
NOT AUTHORIZED — until MODEL A′ PASS and Episode #1 custody reconciliation PASS

P01-03G registry content access:
NOT AUTHORIZED — execution-time protocol access only

external source-record access:
NOT AUTHORIZED — execution-time protocol access only

real dataset access:
NOT AUTHORIZED — execution-time protocol access only

Generation A:
NOT AUTHORIZED — until activation

Generation B:
NOT AUTHORIZED — until activation

compare:
NOT AUTHORIZED — until activation

generation workspace creation:
NOT AUTHORIZED — until activation

Episode #1 (all operations):
NOT AUTHORIZED — not reusable, not repairable, immutable

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

## 10. Scope and non-authority

```text
records a conditional superseding execution-authorization decision only
activates nothing on its own
creates no implementation authority
grants no input access before activation
creates no generation workspace
generates no artifact
executes no leakage analysis
publishes nothing
unlocks no later stage
starts no execution episode
```

This decision supersedes the earlier execution authorization for all future
P01-04D execution episodes and amends no other founder decision. It does not
alter `FD-DREADY-1` through `FD-DREADY-12`, the formal operator contract, the
seven-file candidate artifact inventory, the artifact-name supersession map,
the P01-04D/E/F/G stage separation or the ratified scientific decisions D1
through D10. On any conflict, D1 through D10 control.

The identity of the commit that introduces this record is resolved only after
canonical adoption, through the `MODEL A′` post-merge activation verification,
and is never written inside the content it would have to hash.