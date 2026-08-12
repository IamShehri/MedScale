# P01-04D Execution-Authorization Activation Rule — Founder Decision

This is the controlling document of the P01-04D execution-activation-rule
package.

## 1. Decision identity

```text
Decision:
XD-EXEC-4:
MODEL A′ — CANONICAL POST-ADOPTION ACTIVATION RULE

Decision class:
EXECUTION-AUTHORIZATION ACTIVATION GOVERNANCE ONLY

Canonical baseline:
5515f37d989f39bbb4d2f72e8ec27f109cc97dce

Canonical tree:
d1b5bc61061d1ef8d4f053b37bdfd44a75b286c7

P01-04D entry:
AUTHORIZED

P01-04D control state:
ENTERED — PRE-EXECUTION GOVERNANCE ONLY

P01-04D execution:
NOT AUTHORIZED
```

This decision defines how a future execution authorization becomes operative. It
is not that authorization, and it does not begin, schedule, stage or draft it.

## 2. The defect being resolved

The defect is **execution-authorization activation self-reference**.

The adopted formal operator requires an exact expected canonical commit and
verifies the repository checkout against it twice: once at request construction,
and again immediately before the first filesystem mutation. A future
execution-authorization package, once canonically adopted, itself moves canonical
main, so the authorization cannot name the commit its own adoption will produce.

```text
authorization names a pre-adoption commit
->
execution checkout is behind canonical main

authorization is followed by a second canonical commit binding the
resolved identity
->
canonical main moves again and the same defect returns one step later
```

## 3. Superseded mechanism

```text
MODEL A:
SUPERSEDED FOR THE ACTIVATION MECHANISM
```

Specifically superseded and no longer required:

```text
a canonical activation-record commit after the execution-authorization merge
```

That mechanism is replaced in full by MODEL A′. No package may reintroduce it,
and no document in this package describes the accepted mechanism as MODEL A.

## 4. Self-reference rule

The execution-authorization candidate cannot embed the merge identity its own
adoption will produce. That identity is unknowable while the candidate is being
written, because the candidate's own content participates in it.

```text
predict a future merge identity:      PROHIBITED
fabricate a future merge identity:    PROHIBITED
reserve a future merge identity:      PROHIBITED
embed a future merge identity:        PROHIBITED
```

The future merge identity is resolved only after adoption, and only through
read-only verification.

## 5. The activation rule

```text
1. A future P01-04D execution-authorization package is drafted and
   independently reviewed against an exact pre-adoption canonical baseline
   and an exact candidate tree.

2. The authorization package defines the activation RULE.

3. The authorization package MUST NOT predict, fabricate, reserve or embed
   its own future merge commit identity.

4. The authorization package is canonically adopted through the normal
   protected main process.

5. After adoption, one read-only post-merge verification resolves the unique
   actual merge commit produced by that adoption.

6. That verification must establish all activation prerequisites defined by
   the authorization, including at minimum:

   - exact execution-authorization merge commit;
   - exact merge tree;
   - expected ordered parents;
   - zero candidate-to-merge tree drift;
   - required checks successful;
   - exact formal-operator identity;
   - exact runtime identity;
   - exact execution-input-manifest identity;
   - exact external-evidence-harness identity;
   - all remaining bindings required by the authorization.

7. Only after that post-merge verification passes does the verified
   execution-authorization merge commit become the exact value supplied as
   --expected-canonical-commit.

8. The post-merge verification is evidence only.

9. The post-merge verification is NOT:
   - another founder authorization;
   - another activation authorization;
   - a repository mutation;
   - a second canonical adoption commit.

10. No second canonical commit may be required merely to record the resolved
    activation identity, because doing so would move canonical main again and
    recreate the self-reference problem.

11. Execution remains unauthorized until:
    - all execution-readiness blockers are CLOSED;
    - a separate founder execution authorization is issued and canonically
      adopted;
    - its MODEL A′ post-merge activation verification passes.
```

The accepted mechanism, stated as a sequence:

```text
CANONICAL AUTHORIZATION RULE
->
CANONICAL AUTHORIZATION ADOPTION
->
READ-ONLY POST-MERGE ACTIVATION VERIFICATION
->
VERIFIED MERGE COMMIT BECOMES --expected-canonical-commit
```

## 6. No second canonical activation commit

```text
post-merge activation verification:
READ-ONLY ACTIVATION EVIDENCE

second canonical activation commit:
NOT REQUIRED AND NOT PERMITTED FOR THIS PURPOSE
```

The verification result is recorded as evidence outside the canonical commit
history. Requiring a commit to bind the resolved identity would move canonical
main and defeat the rule.

This prohibition is scoped exactly to binding the resolved activation identity.
It does not prohibit later, separately authorized canonical commits made for
their own independent reasons.

## 7. Failed verification

```text
post-merge activation verification FAILS:
EXECUTION REMAINS NOT AUTHORIZED
```

A failed verification activates nothing. It supplies no value for
`--expected-canonical-commit`, and it is never partially honoured. There is no
automatic retry, no repair and no downgrade of any prerequisite. A failure
returns the matter to founder disposition.

## 8. Canonical main movement after activation verification

The execution protocol already requires formal generation to stop if canonical
main has moved from the expected commit. That stop condition is unchanged and
is not weakened by MODEL A′.

```text
CANONICAL MAIN MOVEMENT AFTER ACTIVATION VERIFICATION:
INVALIDATES ACTIVATION;
NEW FOUNDER-GOVERNED DISPOSITION OR RE-VERIFICATION REQUIRED BEFORE EXECUTION
```

This applies to movement at any point after a passing verification and before
Generation A begins, and equally to movement between Generation A and
Generation B.

```text
automatic reactivation:              DOES NOT EXIST
implicit re-pinning to a new main:   PROHIBITED
silent continuation:                 PROHIBITED
```

Where existing canonical policy is stricter than this clause, the stricter
policy controls.

## 9. Blocker state

```text
XD-EXEC-1   external execution-evidence recording
DECIDED / OPEN

XD-EXEC-2   external source-record custody and binding
DECIDED / OPEN

XD-EXEC-3   independently recorded formal input identities
DECIDED / OPEN

XD-EXEC-4   execution-authorization activation baseline
DECIDED — ACTIVATION MECHANISM RECORDED BY THIS PACKAGE
```

This package closes XD-EXEC-4 only at the governance-mechanism level. It makes
no claim about XD-EXEC-1, XD-EXEC-2 or XD-EXEC-3, and it does not reduce,
reframe or defer any of them.

Execution readiness requires every blocker to be CLOSED. Recording an activation
mechanism does not make the remaining blockers smaller.

## 10. The XD-EXEC-3 implementation boundary remains in force

The founder separately approved the execution-input identity-manifest direction
while withholding authority for the implementation changes it requires.

```text
P-C1a:
DOCUMENTATION AND CONTRACTS ONLY

P-C1b:
SEPARATELY FOUNDER-AUTHORIZED BOUNDED IMPLEMENTATION, which must name an exact
path allowlist and must require fresh independent verification that B-1, B-2,
F1, F2 and F3 remain CLOSED
```

This package neither implements nor authorizes P-C1a or P-C1b, and nothing here
may be cited as authority for either.

## 11. No authority expansion

MODEL A′ does not:

```text
authorize execution
authorize protected input access
authorize source-record access
authorize P01-03G access
authorize real dataset access
create a workspace
invoke generate
invoke compare
close XD-EXEC-1
close XD-EXEC-2
close XD-EXEC-3
draft the future execution authorization
```

## 12. Prohibition boundary

Every line below remains in force after this decision.

```text
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

## 13. Scope and non-authority

```text
records an activation-governance decision only
creates no execution authority
creates no implementation authority
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
P01-04D/E/F/G stage separation or the ratified scientific decisions D1 through
D10. On any conflict, D1 through D10 control.

The identity of the commit that introduces this record is recorded externally,
in its build report and in its independent review record, and is never written
inside the content it would have to hash. That is the same constraint MODEL A′
governs at the scale of a canonical merge.
