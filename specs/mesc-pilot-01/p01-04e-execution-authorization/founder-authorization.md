# P01-04E Real Leakage Audit — Founder Execution Authorization

This is the controlling document of the P01-04E execution-authorization
package. It records the founder authorization to perform exactly one initial
real P01-04E leakage audit against the accepted P01-04D Episode #2 split after
the runtime commit-binding correction is canonically adopted and post-merge
activation passes. On any conflict with the other document in this package,
this document controls.

## 1. Decision identity

```text
Decision:
P01-04E REAL LEAKAGE AUDIT — CONDITIONALLY ISSUED

Decision class:
EXECUTION AUTHORIZATION — CONDITIONAL, EXACTLY ONE INVOCATION

Prior state:
P01-04E implementation canonically adopted / synthetically qualified
P01-04E execution not active, acceptance not established
```

## 2. Runtime commit-binding correction

The adopted P01-04E operator previously carried a compile-time
`_EXPECTED_CANONICAL_MAIN` constant, intentionally fail-closed but unmaintainable:
every adoption commit creates a new canonical main and immediately stales the
constant again.

The correction (commit subject `fix(mesc): make P01-04E canonical commit
runtime-bound`) removes that constant and replaces it with a required runtime
argument:

```text
--expected-canonical-commit
exactly 40 lowercase hexadecimal characters
```

The operator verifies the checked-out repository `HEAD` equals
`--expected-canonical-commit` before protected processing, and again
immediately before the first audit-workspace mutation. The invocation
authority — not arbitrary operator code — supplies the expected commit.

No scientific logic, detection class, threshold, classification rule,
suppression rule, finding identity, audit schema, filename or FD-E-CTX-1
semantics changed.

## 3. Bound identities

The audit must bind exactly to the accepted Episode #2 split. No substituted
or regenerated P01-04D split is permitted.

```text
P01-04D Episode #2 episode identity:
731ec4d6cb879eec935ce70667648a9acae656fbb36c791689fa615df04d385a

authoritative split fingerprint:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91

generation-manifest.json:
sha256 5ae5b91b8c11671e91bc9ca18f3d8741045ba04d83f1307c87ad71ac05f47bdd
size   2451

example-registry.jsonl:
sha256 4783d57bf9e0cdb642e0b5410ec0a388bd90d5c3d73a9b466d34f2e7b04ba310
size   311432

source-records.jsonl:
sha256 22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce
size   2770193
```

```text
P01-04E operator blob:
6cfabde523867189a8b6c9e5de847a07fa23ab26

P01-04E orchestration-module blob:
596adae652b1eec8545baafa12342b49341ac6a7
```

These blob identities are the SHA-256 object identities of the corrected
candidate, measured after the correction commit. No predicted merge SHA is
bound, and no merge SHA is bound before it is observed.

## 4. Activation rule

```text
P01-04E real execution authorization:
CONDITIONALLY ISSUED
```

Activation requires all of:

```text
1. correction + authorization canonically merged
2. candidate tree == merge tree
3. required CI green
4. actual merge SHA known
5. operator blob == authorization-bound operator blob
6. orchestration module blob == authorization-bound module blob
7. accepted P01-04D identities all exact
8. external source-record identity exact
9. clean isolated execution checkout at actual merge SHA
```

The actual merge SHA becomes the value passed to `--expected-canonical-commit`.
No self-reference exists: the expected commit is a runtime argument supplied by
the invocation authority.

## 5. Authorized scope

After activation:

```text
read the accepted P01-04D example-registry.jsonl
read the accepted P01-04D generation-manifest.json
read the accepted external source-records.jsonl
inspect only the minimum scientific fields required by P01-04E:
  question
  context_segments
  original_example_id
  source_document_id
  and canonical input-identity/schema fields
perform the canonical cross-partition leakage audit
write exactly one leakage-audit.json
  to one fresh P01-04E audit workspace
```

The first real audit uses NO classification ledger:

```text
structural finding:  confirmed_leakage
scientific-text finding: unresolved
```

No real scientific finding may be preemptively classified `false_positive`.
The empirical result is preserved before human adjudication.

## 6. Not authorized

```text
P01-04F
P01-04G
new split generation
P01-04D retry
model inference
retrieval
training
fine-tuning
LoRA / QLoRA
publication of raw scientific text
any audit retry, code modification, or input substitution after refusal
```

## 7. Scientific-content boundary

Real source-record access is transient and in-memory only. P01-04E may inspect
`question` and `context_segments` because they are necessary for leakage
detection, but must not emit raw scientific text into `leakage-audit.json`,
stdout, stderr, exception messages, Git, governance documents, or a
classification ledger.

## 8. Failure disposition

The authorization permits exactly one initial real audit invocation. If the
operator refuses or fails: do not retry, do not modify code, do not modify
inputs, do not reuse the audit workspace. Preserve the resulting state and
report the first failing invariant.

## 9. Outcome disposition

```text
if finding_count == 0 and leaked == false:
  P01-04E acceptance review proceeds (Phase E of the completion task)

if finding_count > 0:
  P01-04E NOT ACCEPTED YET
  independent scientific finding review required
```

## 10. Privacy and repository integrity

No absolute path, workspace location, custody location or timestamp is
persisted by this package. No raw scientific content and no audit bytes are
persisted by this package. The execution itself mutates no tracked repository
file, no P01-04D workspace file, and no source-record file.