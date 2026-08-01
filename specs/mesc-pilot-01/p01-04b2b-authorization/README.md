# P01-04B2B Implementation Authorization

```text
Status:
FOUNDER IMPLEMENTATION-AUTHORIZATION DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

Package revision:
CORRECTED REPLACEMENT — supersedes unmerged Draft PR #68

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

Canonical baseline:
`bfc4254b6a028ea7ec5969b505d73e7d66751272`

---

## Purpose

This package records founder **implementation-authorization decisions** for the
P01-04B2B leakage primitive library. It authorizes nothing to run and no code to
be written yet.

It does not implement B2B, execute leakage detection, inspect real records,
authorize B2C or B2D, accept P01-04B as a whole, or authorize any downstream
model, dataset, split, inference, retrieval, benchmark, training, publication or
clinical activity.

Prior governance history is adopted at
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/) and
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/)
and is not restated here.

## Replacement provenance

This is a **corrected replacement** for unmerged Draft PR #68.

```text
Rejected head:
a309f0789c48646e36a87181b23673551a23d74d

Independent clean-room exact-head review verdict:
CHANGES REQUIRED — PR #68 MUST REMAIN DRAFT

Independence attestations:  16 / 16 SATISFIED
Blocking findings:          2
Non-blocking findings:      3
Mutation:                   NONE
```

The rejected head is **non-canonical and was never adopted**. This replacement
was reconstructed directly from canonical `main`; it is not a child of the
rejected head and no commit was cherry-picked. It requires a **new** genuinely
independent exact-head review — the PR #68 review does not carry over.

### BLOCKING-1 — corrected

```text
Observed:
The float-or-null in-memory score contract conflicted with the accepted B2A
canonical serializer, which prohibits binary floating-point values.

Correction:
An authoritative frozen string, score_representation, is now the canonical and
identity-bearing form. The runtime float is derived, runtime-only, and excluded
from canonical documents, canonical bytes, fingerprints and finding-ID payload
bytes. Threshold passage uses exact integer comparison.
```

### BLOCKING-2 — corrected

```text
Observed:
The finding-ID semantic components were listed, but the exact canonical payload
bytes hashed by SHA-256 were not pinned.

Correction:
The identity document is now an exact six-member frozen canonical JSON object,
and FINDING_IDENTITY_BYTES is pinned to the accepted B2A canonical single-object
JSON byte serialization of that document, including its terminal-line-feed rule.
The finding ID is the prefix plus the lowercase 64-hex SHA-256 of those exact
bytes.
```

## Canonical baseline

```text
Merge SHA:
bfc4254b6a028ea7ec5969b505d73e7d66751272

Tree:
4208ea672a01ac942a1caeee764167d530cc8f1e

Ordered parent 1:
1f2d9152281f3136d212dcf7729063f7b1c64ad1

Ordered parent 2:
c59e4e16015a89197622227526458e9cead855fd

Subject:
docs(mesc): record P01-04B2A acceptance (#67)
```

## B2A adoption identity

```text
PR #67:
CLOSED / MERGED / NOT DRAFT — merged 2026-08-01T03:32:26Z

FD-B2A-9:
ADOPTED ON CANONICAL MAIN at bfc4254b6a028ea7ec5969b505d73e7d66751272

P01-04B2A:
ACCEPTED

N-12:
SATISFIED AND DISCHARGED FOR P01-04B2A

Windows portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A

macOS portability obligation:
SATISFIED AND CLOSED FOR P01-04B2A
```

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
activate until canonically adopted.

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
implementation. They amend none of those authorities, and they conform to the
accepted B2A canonical value domain rather than extending it.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-authorization.md`](founder-authorization.md) | **Controlling**: `FD-B2B-1` through `FD-B2B-10`, the exact implementation authorization, the future path allowlist, activation conditions, and pre- and post-adoption classifications |
| [`implementation-contract.md`](implementation-contract.md) | The exact primitive, normalization, threshold, score-representation, finding-identity, classification, boundary, error and test requirements the future implementation must satisfy |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for **this documentation package** |

On any conflict, [`founder-authorization.md`](founder-authorization.md)
controls.

## Score representation and finding identity — summary

```text
Authoritative canonical form:
score_representation ∈ { none, not_evaluable, jaccard:<i>/<u> }

Runtime float:
derived, runtime-only, never canonicalized, never hashed

Threshold passage:
exact integer comparison — 100*i >= 90*u and 100*i >= 95*u

Finding identity document:
exactly six frozen members — schema, finding_type, example_ids,
source_document_ids, partitions, score_representation

FINDING_IDENTITY_BYTES:
accepted B2A canonical single-object JSON serialization of that document

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

Before activation the authority is **recorded but inactive** and implementation
is **not authorized to begin**.

## Exact future implementation allowlist

After this package is canonically adopted, a separate implementation task may
modify exactly two paths:

```text
A src/medscale/mesc/_leakage_v1.py
A tests/test_mesc_leakage_v1.py
```

No other path is authorized for the future B2B implementation pull request. If
implementation later proves impossible within this two-path allowlist, the
correct action is to stop and return for a new founder authorization. The
allowlist must not be expanded during implementation.

## Continuing prohibitions

Even after this package is adopted:

```text
P01-04B2A                                   ACCEPTED
P01-04B2B implementation                    AUTHORIZED — NOT STARTED
P01-04B2B acceptance                        NOT ACHIEVED
P01-04B2C                                   NOT AUTHORIZED
P01-04B2D                                   NOT AUTHORIZED
P01-04B as a whole                          INCOMPLETE / NOT ACCEPTED
P01-04C through P01-04G                     NOT AUTHORIZED
Real Pilot-01 split                         NOT AUTHORIZED
P01-03G or real dataset access              NOT AUTHORIZED
Leakage audit over real or canonical records NOT AUTHORIZED
Fixture facade                              NOT AUTHORIZED
CLI                                         NOT AUTHORIZED
Filesystem publication                      NOT AUTHORIZED
B0/B1 model execution                       NOT AUTHORIZED
Model access                                NOT AUTHORIZED
Inference                                   NOT AUTHORIZED
Retrieval                                   NOT AUTHORIZED
Metrics or benchmark execution              NOT AUTHORIZED
Training or fine-tuning                     NOT AUTHORIZED
Publication                                 NOT AUTHORIZED
Clinical use                                NOT AUTHORIZED
```

Completing the B2B implementation will **not** accept B2B. Acceptance will
require an independent exact-head implementation review, a separate founder
Ready decision, a separate merge decision, canonical merge, mechanical
verification, and then a later separate B2B implementation-acceptance decision.
B2C remains blocked until B2B is **accepted**, not merely implemented.
