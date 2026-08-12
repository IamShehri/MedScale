# P01-04B2B Implementation Authorization

```text
Status:
FOUNDER IMPLEMENTATION-AUTHORIZATION DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

Package revision:
R3 — CLEAN POST-INCIDENT RECONSTRUCTION

Canonical baseline:
06078180eb7c85da80878f3a86c5fdf3655462c5

Canonical baseline tree:
4208ea672a01ac942a1caeee764167d530cc8f1e

FD-B2B-1 through FD-B2B-10:
FOUNDER DECISIONS ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2B implementation authority:
RECORDED BUT INACTIVE

P01-04B2B implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2B acceptance:
NOT ACHIEVED

P01-04B2C / P01-04B2D:
NOT AUTHORIZED

P01-04B as a whole:
INCOMPLETE / NOT ACCEPTED
```

---

## Purpose

This package records founder **implementation-authorization decisions** for the
P01-04B2B leakage primitive library. It authorizes nothing to run and no code to
be written yet.

It does not implement B2B, execute leakage detection, inspect real or canonical
records, authorize B2C or B2D, accept P01-04B as a whole, or authorize any
downstream model, dataset, split, inference, retrieval, benchmark, training,
publication or clinical activity.

Prior governance history is adopted at
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/) and
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/)
and is not restated here.

## Canonical baseline

```text
Baseline SHA:
06078180eb7c85da80878f3a86c5fdf3655462c5

Baseline tree:
4208ea672a01ac942a1caeee764167d530cc8f1e
```

Preceding valid governance state:

```text
PR #67:                            VALIDLY MERGED AND MECHANICALLY VERIFIED
P01-04B2A:                         ACCEPTED
FD-B2A-9:                          ADOPTED ON CANONICAL MAIN
N-12:                              SATISFIED AND DISCHARGED FOR P01-04B2A
Windows and macOS obligations:     CLOSED FOR P01-04B2A
```

## Provenance — why this is revision r3

This package is a **fresh reconstruction directly from the protected canonical
main**. R3 introduces no historical authorization commit, cherry-picks no
historical authorization commit, and adds exactly one new single-parent commit
directly on the current canonical main. Its four package documents are freshly
reconstructed and carry blob identities distinct from both the r1 and the r2
package blobs.

This is a **construction-provenance** claim, not a graph-reachability claim. The
two are deliberately distinguished below.

```text
PR #68:
reviewed and rejected at its exact head
a309f0789c48646e36a87181b23673551a23d74d (tree 5e2c767c);
independent review returned CHANGES REQUIRED with two blocking findings;
never merged, never adopted; non-canonical.

PR #69:
corrected historical package
1c446def4c064b21c2cc60bc894aab3ed8e9ccff (tree 5c3ec5ed);
entered main through an unauthorized Draft merge
c8e476e42aa7c6f0e433836e278cba8940f0ea26;
never validly reviewed and never validly adopted;
mechanically contained through PR #70.

PR #70:
validly merged and mechanically verified as
06078180eb7c85da80878f3a86c5fdf3655462c5;
restored the exact last valid canonical tree
4208ea672a01ac942a1caeee764167d530cc8f1e.

R3:
fresh reconstruction directly from the protected canonical main;
introduces, merges and cherry-picks no historical package commit;
inherits the preserved incident ancestry through canonical main;
requires a completely new independent review and adoption cycle.
```

### Inherited ancestry — stated explicitly

Because PR #70 **preserved** rather than rewrote incident history, the PR #69
head `1c446def4c064b21c2cc60bc894aab3ed8e9ccff` and the unauthorized merge
`c8e476e42aa7c6f0e433836e278cba8940f0ea26` remain reachable through canonical
`main` and are therefore **necessarily inherited by every branch created from
the current canonical main**, including this one.

```text
1c446def4c064b21c2cc60bc894aab3ed8e9ccff:  reachable ancestor of r3
c8e476e42aa7c6f0e433836e278cba8940f0ea26:  reachable ancestor of r3
a309f0789c48646e36a87181b23673551a23d74d:  not an ancestor of r3
```

Mechanically:

```text
git merge-base --is-ancestor 1c446def... <r3 head>   ->  exit 0   (expected)
git merge-base --is-ancestor a309f078... <r3 head>   ->  nonzero  (expected)
```

The exit-0 result is **correct and expected**. It is a consequence of
history-preserving containment, not of any action by r3. That historical
reachability is **not adoption, not approval, not reuse, and not introduction
by r3**. No document in this package may claim that `1c446def...` is absent
from the ancestry of r3 or of canonical `main`.

The PR #69 content was **neither substantively approved nor substantively
rejected** — it was never validly adjudicated. Its corrected design is preserved
here on the merits it was always intended to be judged on, under a review cycle
that has not yet begun.

## Corrections carried forward from the rejected r1 head

The two blocking findings raised against PR #68 are resolved in this
reconstruction and are stated here so a reviewer can verify them directly.

```text
BLOCKING-1 — the float-or-null score contract conflicted with the accepted B2A
canonical serializer, which prohibits binary floating-point values.

Resolution: an authoritative frozen string, score_representation, is the
canonical and identity-bearing form. The runtime float is derived, runtime-only,
and excluded from canonical documents, canonical bytes, fingerprints and
finding-ID payload bytes. Threshold passage uses exact integer comparison.
```

```text
BLOCKING-2 — the finding-ID semantic components were listed, but the exact
canonical payload bytes hashed by SHA-256 were not pinned.

Resolution: the identity document is an exact six-member frozen canonical JSON
object, and FINDING_IDENTITY_BYTES is pinned to the accepted B2A canonical
single-object JSON byte serialization of that document, including its terminal
LF rule. The finding ID is the prefix plus the lowercase 64-hex SHA-256 of those
exact bytes.
```

## Blocking corrections applied after the independent r3 review

The independent clean-room review of the rejected exact head
`0907b45904e237462fff10f835f15a2dcfa748d6` returned CHANGES REQUIRED with three
blocking findings. All three are founder-accepted and corrected here.

```text
B-1 — the package asserted a graph-reachability claim denying that the historical
package commits appear in r3 ancestry. That claim is false for the PR #69 head,
and it was additionally encoded as an acceptance criterion that could never be
satisfied.

Resolution: every graph-reachability claim is replaced by construction-provenance
language, and the inherited PR #69 ancestry is stated explicitly as a correct and
expected consequence of history-preserving containment.
```

```text
B-2 — token_set_jaccard was required to be total, but every representable
score_representation was forbidden when the union is zero.

Resolution: the union-zero case is pinned to not_evaluable with a null runtime
score and neither threshold passed; jaccard:0/0 is prohibited and jaccard:0/1 is
explicitly not used for that case; punctuation-only inputs that tokenize to two
empty sets are routed to this rule rather than to empty_normalized_question.
```

```text
B-3 — the multiplicity of the three identity arrays was never pinned, leaving
FINDING_IDENTITY_BYTES under-determined.

Resolution: example_ids, source_document_ids and partitions are unique-value
lists; duplicates are invalid and fail closed through the existing typed
invalid-finding-identifier error; silent deduplication is prohibited; input
permutation is non-semantic.
```

## Blocking correction applied after the second independent review

The independent clean-room review of the superseded exact head
`adc01a4ce6919ac7e4de6d915cbe0ffcf6d3cf63` confirmed B-1, B-3 and the B-2
union-zero correction as resolved, and returned one further blocking finding,
which is founder-accepted and corrected here.

```text
BLOCKING-R3-1 — score_representation was contradictorily specified for the
exactly-one-empty token-set case. The unqualified rule and golden vector
"intersection 0, union positive -> jaccard:0/1" and the empty-input rule
"exactly one token set empty -> not_evaluable" both applied to the same input,
with no precedence stated, making an identity-bearing value non-deterministic
and making two required tests mutually unsatisfiable.

Resolution: empty-input handling is evaluated before general fraction
construction and controls; a jaccard fraction is constructed only when both
token sets are non-empty; exactly-one-empty remains not_evaluable as
policy-defined under senior FD-B2-6; the zero-score golden vector is scoped to
two non-empty disjoint token sets with the literal witness
frozenset({"a"}), frozenset({"b"}); the exactly-one-empty case is no longer
classified as a union-zero case; required tests and acceptance criteria are made
mutually consistent.
```

Neither prior review carries forward. This corrected head requires a completely
new independent clean-room exact-head review.

## Protected-main context

Canonical `main` is protected by an active repository ruleset:

```text
Ruleset ID:    20172239
Name:          MedScale canonical main protection v1
Enforcement:   active
Target:        refs/heads/main
Bypass actors: none
```

It requires a pull request, merge-commit method only, review-thread resolution,
and strict up-to-date status checks `quality (py3.11)`, `quality (py3.12)` and
`analyze (python)`; it blocks force pushes and branch deletion.

This is **security configuration context only**. It does not replace, satisfy,
or substitute for the governance review and founder-decision gates, and it
confers no authority on this package.

## Dependency-DAG satisfaction

The adopted P01-04B2 plan records:

```text
B2B requires B2A acceptance.
B2C requires B2A and B2B acceptance.
B2D requires B2A, B2B and B2C acceptance.
```

B2A is accepted and canonically adopted, so the B2B prerequisite is satisfied.
**That makes a B2B authorization decision eligible. It does not automatically
authorize B2B** — this package is that separate decision, and even it does not
activate until validly adopted.

## B2B design authority

`FD-B2-6` (founder-ratified 2026-07-24) defines the leakage normalization and
classification rules. The adopted plan defines P01-04B2B as the **leakage
primitive library** with these deliverables:

```text
exact_example_identity
exact_source_document_identity
exact_question_equality
normalized_question_equality
token_set_jaccard
context_equality
deterministic finding-identifier generation
false-positive classification rules
suppression prohibition
```

B2B explicitly does **not** include:

```text
FixtureSplitFacade
FixtureSplitRequest integration
public facade
CLI
filesystem publication
real registry scanning
formal audit execution
integrated qualification
P01-04B acceptance
```

Those belong to B2C, B2D or later stages.

`FD-B2B-1` through `FD-B2B-10` are **subordinate** to P01-04A `D1`–`D10`,
`FD-B2-1` through `FD-B2-8`, `FD-B2A-1` through `FD-B2A-8`, and the accepted B2A
implementation. They amend none of those authorities.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-authorization.md`](founder-authorization.md) | **Controlling**: `FD-B2B-1` through `FD-B2B-10`, the future path allowlist, activation conditions, and pre- and post-adoption classifications |
| [`implementation-contract.md`](implementation-contract.md) | The exact primitive, normalization, threshold, score-representation, finding-identity, classification, boundary, error and test requirements |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for **this documentation package** |

On any conflict, [`founder-authorization.md`](founder-authorization.md)
controls.

## Score representation and finding identity — summary

```text
Authoritative canonical form:
score_representation ∈ { none, not_evaluable, jaccard:<i>/<u> }

Golden vectors:
both non-empty, 6 / 9            -> jaccard:2/3
both non-empty and disjoint      -> jaccard:0/1
both non-empty, 9 / 9            -> jaccard:1/1
exact method                     -> none
non-evaluable                    -> not_evaluable

Zero-score golden-vector witness:
frozenset({"a"}), frozenset({"b"}) -> intersection 0, union 2, jaccard:0/1,
runtime score 0.0, neither threshold passed

Evaluation order (controlling):
1. normalized-question empty routing;
2. token-set empty-input rules;
3. Jaccard fraction only if both token sets are non-empty;
4. threshold comparison on integer counts.
The earlier applicable rule controls.

Token-set empty-input cases — all three stated:
both empty            -> not_evaluable (union zero; jaccard:0/0 prohibited)
exactly one empty     -> not_evaluable (union positive; policy-defined under
                         senior FD-B2-6; jaccard:0/1 not used)
both non-empty and disjoint -> jaccard:0/1 (runtime score 0.0)

In the two empty cases the runtime score is null, no fraction is constructed and
neither threshold passes. jaccard:0/1 is never emitted when either token set is
empty; not_evaluable is never emitted for two non-empty disjoint token sets.

Runtime float:
derived, runtime-only, never canonicalized, never hashed

Threshold passage:
exact integer comparison — 100*i >= 90*u and 100*i >= 95*u

Finding identity document:
exactly six frozen members — schema, finding_type, example_ids,
source_document_ids, partitions, score_representation

Identity arrays:
unique-value lists; duplicates invalid and never silently collapsed;
unique values sorted lexicographically before canonical serialization;
input permutation is non-semantic

FINDING_IDENTITY_BYTES:
accepted B2A canonical single-object JSON serialization of that document,
including the accepted terminal LF rule

finding_id:
mesc-pilot-01-leakage-finding/1:sha256:<64-lowercase-hex of SHA-256 over
FINDING_IDENTITY_BYTES>
```

Full definitions are in
[`implementation-contract.md`](implementation-contract.md) §5 and §6.

## Activation conditions — all five required

1. a genuinely independent clean-room exact-head review of this authorization
   package;
2. a separate founder Ready decision;
3. a separate founder merge decision;
4. merge into canonical `main`;
5. mechanical post-merge verification.

```text
No subset activates P01-04B2B implementation authority.
```

Before valid adoption the authority is **recorded but inactive** and
implementation is **not authorized to begin**.

## Exact future implementation allowlist

After valid canonical adoption, a separate implementation task may modify
exactly two paths:

```text
A src/medscale/mesc/_leakage_v1.py
A tests/test_mesc_leakage_v1.py
```

No other path is authorized. If implementation later proves impossible within
this two-path allowlist, the correct action is to stop and return for a new
founder authorization. The allowlist must not be expanded during
implementation.

## Continuing prohibitions

Even after this package is validly adopted:

```text
P01-04B2A                                    ACCEPTED
P01-04B2B implementation                     AUTHORIZED — NOT STARTED
P01-04B2B acceptance                         NOT ACHIEVED
P01-04B2C                                    NOT AUTHORIZED
P01-04B2D                                    NOT AUTHORIZED
P01-04B as a whole                           INCOMPLETE / NOT ACCEPTED
P01-04C through P01-04G                      NOT AUTHORIZED
Real Pilot-01 split                          NOT AUTHORIZED
Real or canonical leakage audit               NOT AUTHORIZED
P01-03G or real dataset access                NOT AUTHORIZED
Fixture facade                                NOT AUTHORIZED
CLI                                           NOT AUTHORIZED
Filesystem publication                        NOT AUTHORIZED
B0/B1 model execution                         NOT AUTHORIZED
Model access                                  NOT AUTHORIZED
Inference                                     NOT AUTHORIZED
Retrieval                                     NOT AUTHORIZED
Metrics and benchmark execution               NOT AUTHORIZED
Training and fine-tuning                      NOT AUTHORIZED
Publication                                   NOT AUTHORIZED
Clinical use                                  NOT AUTHORIZED
```

Completing the B2B implementation will **not** accept B2B. Acceptance will
require an independent exact-head implementation review, a separate founder
Ready decision, a separate merge decision, canonical merge, mechanical
verification, and then a later separate B2B implementation-acceptance decision.
B2C remains blocked until B2B is **accepted**, not merely implemented.
