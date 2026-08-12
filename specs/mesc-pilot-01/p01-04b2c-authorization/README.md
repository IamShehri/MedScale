# P01-04B2C Implementation Authorization

```text
Status:
FOUNDER IMPLEMENTATION-AUTHORIZATION DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

FD-B2C-1 through FD-B2C-12:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:
RECORDED BUT INACTIVE

P01-04B2C implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

Real split generation, real or canonical leakage-audit execution,
P01-03G or real-data access, model access, inference, retrieval, metrics,
benchmark execution, training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Canonical baseline:
`3c4d7f153522128533fa9aba26209426b248b4f1`

---

## Purpose

This package records the founder's authorization of the **P01-04B2C
implementation** — a private, fixture-only, in-memory facade and integration
entry point that composes the already-accepted B1 split core, B2A canonical
artifact and fingerprint layer, and B2B leakage primitives into one
deterministic, library-only result object.

It is documentation only. It implements nothing, executes nothing, dispatches
nothing, downloads nothing, and changes no implementation, test, workflow,
dependency, configuration, serializer, export, CLI, lockfile, dataset, model or
artifact path.

Prior governance history is adopted at
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/),
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/)
and
[`../p01-04b2b-acceptance/`](../p01-04b2b-acceptance/)
and is **not** restated here.

## Current pre-adoption state

The controlling state this package begins from, and does not yet change:

```text
FD-B2B-11:                          ADOPTED ON CANONICAL MAIN
P01-04B2A:                          ACCEPTED
P01-04B2B:                          ACCEPTED
P01-04B2C:                          ELIGIBLE FOR A SEPARATE AUTHORIZATION
                                    DECISION; NOT YET AUTHORIZED
P01-04B2D:                          NOT AUTHORIZED
P01-04B:                            INCOMPLETE / NOT ACCEPTED
Real split generation:              NOT AUTHORIZED
Real or canonical leakage audit:    NOT AUTHORIZED
P01-03G or real-data access:        NOT AUTHORIZED
Model access, inference, retrieval,
metrics, benchmark execution,
training, fine-tuning, publication,
clinical use:                       NOT AUTHORIZED
```

**Eligibility is not authority.** B2C being eligible for a separate
authorization decision did not authorize any implementation, and recording this
package does not either — see the activation boundary below.

## Canonical baseline

```text
Merge SHA:
3c4d7f153522128533fa9aba26209426b248b4f1

Tree:
e548aab1342c8783c1b919e707e5036a18e4a80a

Ordered parent 1:
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863

Ordered parent 2:
a7b25f1755da2ca62fe516a68ae684b493be6bce

Subject:
Merge pull request #73 from IamShehri/docs/mesc-p01-04b2b-acceptance
docs(mesc): record P01-04B2B implementation acceptance
```

## Authority chain

This package is subordinate to, and must not contradict:

```text
P01-04A decisions D1 through D10
FD-B2-1 through FD-B2-8
FD-B2A-1 through FD-B2A-8
FD-B2A-9
FD-B2B-1 through FD-B2B-10
FD-B2B-11
the accepted B2A implementation
the accepted B2B implementation
```

Accepted implementation identities the future B2C work builds on:

```text
B2A — canonical merge 5736b1171f1aa467105d931713f5749fb81acd5b
      final head      7307fcf9085d3d15114984731b49d484523f09eb
      src/medscale/mesc/_canonical_json_v1.py
      src/medscale/mesc/_split_artifacts_v1.py

B2B — canonical merge d91f76e77c4753e556b2ca9c2ee1bfcd5923d863
      reviewed head   86cfdca1797cf1be60761284af1cc81e25047f41
      accepted tree   070b177194094e5ae55d34570a86997fde956302
      src/medscale/mesc/_leakage_v1.py

B1  — src/medscale/mesc/_split_v1.py
```

The future implementation **reuses** these accepted modules. It must not fork
or reimplement their canonical serialization, fingerprint, allocation or
leakage contracts.

## B2C scope

In scope for the future implementation:

```text
one private stateless facade      FixtureSplitFacade
one immutable request             FixtureSplitRequest
one immutable result              FixtureSplitResult
deterministic composition of the accepted B1, B2A and B2B layers
six in-memory canonical byte surfaces
one authoritative 64-hex split fingerprint
one 16-hex B1 compatibility hash, display only
explicit-finding leakage report construction
five typed private error categories
synthetic in-memory tests
```

Out of scope, and prohibited:

```text
record-pair enumeration, dataset scanning, registry scanning
automatic finding discovery
real split generation or a real leakage audit
any filesystem, network, subprocess, clock, environment or locale access
any public export, CLI or entry point
B2D's three 1,000-row fixtures and their qualification
```

## Exact future implementation allowlist

```text
A src/medscale/mesc/_fixture_split_v1.py
A tests/test_mesc_fixture_split_v1.py
```

Exactly two paths. No third implementation path is authorized. The future
implementation must not modify `__init__.py`, `split.py`, `_split_v1.py`,
`_canonical_json_v1.py`, `_split_artifacts_v1.py`, `_leakage_v1.py`, any CLI,
any workflow, any dependency or lockfile, or any governance document.

## Founder decisions index

| Decision | Subject |
|---|---|
| `FD-B2C-1` | Private module and exact future path allowlist |
| `FD-B2C-2` | Stateless fixture-only facade |
| `FD-B2C-3` | Exact immutable request contract |
| `FD-B2C-4` | Fixture identity and honest proof semantics |
| `FD-B2C-5` | Exact B1 integration pipeline |
| `FD-B2C-6` | B1 compatibility manifest |
| `FD-B2C-7` | Canonical in-memory artifacts |
| `FD-B2C-8` | Leakage integration without scanning |
| `FD-B2C-9` | Exact immutable result contract |
| `FD-B2C-10` | Typed errors and validation order |
| `FD-B2C-11` | Side-effect and authority prohibition |
| `FD-B2C-12` | Activation and sequencing |

## Honest structural-proof semantics

`fixture_only`, `non_evidence` and `synthetic_identity_proof` are **declared
markers**. They establish that a request is internally consistent with the
identity it claims. They are **not** a cryptographic or real-world provenance
oracle, and no combination of flags can detect a caller who deliberately
repackages real data into the accepted row types.

B2C safety derives from structure, not from flags:

```text
private module
no public export
no CLI
no path input
no registry adapter
no filesystem access
no real-data entry point
SourceDocumentGroupedSplitter.assign remaining fail-closed
```

## Activation boundary

While this package is local, Draft, Ready-but-unmerged, or
merged-but-not-mechanically-verified, every decision it records is **issued but
not canonically adopted**, and the implementation authority is **inactive**.
Activation requires all five conditions:

1. a genuinely independent clean-room exact-head review of **this**
   authorization package;
2. a separate founder Ready decision;
3. a separate founder merge decision;
4. merge into canonical `main`;
5. mechanical post-merge verification.

```text
No subset activates P01-04B2C implementation authority.
```

After valid activation the authority is **ACTIVE FOR ONE BOUNDED
IMPLEMENTATION ONLY** and is spent once one implementation commit series is
accepted for publication.

**Implementation does not equal acceptance.** After implementation, B2C still
requires an independent exact-head implementation review, exact-head CI and
CodeQL, a separate Ready decision, a separate merge decision, post-merge
mechanical verification, a separate implementation-acceptance disposition, and
canonical adoption of that disposition. B2D remains unauthorized until B2C is
canonically accepted.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-authorization.md`](founder-authorization.md) | **Controlling**: `FD-B2C-1` through `FD-B2C-12`, the authorization decision, its exact scope, the request and result boundary, honest structural-proof semantics, the activation conditions, the post-adoption state and the continuing prohibitions |
| [`implementation-contract.md`](implementation-contract.md) | The complete implementable contract — allowed imports, exact classes and fields, exact validation order, exact fixture and request identity payloads, the exact integration pipeline, compatibility-manifest rules, canonical artifact schemas and ordering, non-circular summary and fingerprint construction, leakage integration, errors and codes, result invariants, the test matrix and the two-path allowlist |
| [`acceptance.md`](acceptance.md) | Acceptance criteria — for this authorization package, and separately for the future implementation |

On any conflict, [`founder-authorization.md`](founder-authorization.md)
controls.

## Continuing prohibitions

Even after canonical adoption, this package does not authorize:

```text
P01-04B2D or its three 1,000-row fixtures
P01-04C through P01-04G
P01-04B whole-phase acceptance
acceptance of the future B2C implementation
a second B2C implementation attempt
real split generation
a real or canonical leakage audit
leakage-audit orchestration, dataset scanning, registry scanning
record-pair enumeration or automatic finding discovery
CLI or filesystem publication
P01-03G or real dataset access
B0 or B1 execution
model access
inference
retrieval
metrics or benchmark execution
training or fine-tuning
publication
clinical use
any workflow dispatch, rerun or cancellation
modification of any prior governance package
modification of any accepted B1, B2A or B2B module
a Ready transition, merge or auto-merge of this package
```

## What this package does not do

It does not implement the facade, accept a future implementation, authorize
B2D, accept P01-04B as a whole, expand the two-path allowlist, authorize
orchestration or dataset scanning, execute a real split, run a real or
canonical leakage audit, authorize dataset or model access, authorize
inference, retrieval, metrics, benchmark execution, training or fine-tuning,
dispatch or rerun any workflow, modify implementation, tests, workflows,
dependencies or artifacts, modify any prior governance package, or authorize a
Ready transition or merge.
