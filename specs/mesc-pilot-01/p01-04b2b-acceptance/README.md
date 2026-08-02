# P01-04B2B Acceptance

```text
Status:
FOUNDER IMPLEMENTATION-ACCEPTANCE DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

FD-B2B-11:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2B:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B2C:
NOT AUTHORIZED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

Real split, real or canonical leakage audit, real-data access,
model access, inference, retrieval, metrics, benchmark execution,
training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Canonical baseline:
`d91f76e77c4753e556b2ca9c2ee1bfcd5923d863`

---

## Purpose

This package records the founder's acceptance of the **P01-04B2B
implementation** — the private, fixture-only leakage primitive library merged
through PR #72 under the authorization adopted through PR #71.

It is documentation only. It implements nothing, executes nothing, dispatches
nothing, downloads nothing, and changes no implementation, test, workflow,
dependency, configuration, serializer, export, CLI, lockfile, dataset, model or
artifact path.

Prior governance history is adopted at
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/)
and
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/)
and is **not** restated here.

## Canonical baseline

```text
Merge SHA:
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863

Tree:
070b177194094e5ae55d34570a86997fde956302

Ordered parent 1:
aeff056cb02fc9f72d2d861cadb84622c5558032

Ordered parent 2:
86cfdca1797cf1be60761284af1cc81e25047f41

Subject:
Merge pull request #72 from IamShehri/feat/mesc-p01-04b2b-leakage-primitives
feat(mesc): implement P01-04B2B leakage primitives
```

## Accepted implementation identity

```text
Authorization package:
PR #71 — canonical merge aeff056cb02fc9f72d2d861cadb84622c5558032
FD-B2B-1 through FD-B2B-10 and the r3 implementation contract

Implementation:
PR #72 — canonical merge d91f76e77c4753e556b2ca9c2ee1bfcd5923d863
reviewed and merged head 86cfdca1797cf1be60761284af1cc81e25047f41
implementation tree 070b177194094e5ae55d34570a86997fde956302
implementation parent aeff056cb02fc9f72d2d861cadb84622c5558032
1 commit / 2 files / +2260 / -0
```

Exactly two paths, both private and non-executable:

```text
src/medscale/mesc/_leakage_v1.py
blob 61f2bf4dff7e71f0a7f2be21b425ba8686badf16          +964

tests/test_mesc_leakage_v1.py
blob a7a77ceee84206c5bfb64b07e64083bb4b0af660         +1296
```

The acceptance decision applies to **this exact implementation identity** under
**this exact adopted contract**, and to nothing else.

## Review and check summary

```text
Independent implementation review:
APPROVE WITH NON-BLOCKING NOTES

Independence:
SATISFIED

Blocking findings:
NONE

Reviewed head:
86cfdca1797cf1be60761284af1cc81e25047f41

Reviewed tree:
070b177194094e5ae55d34570a86997fde956302
```

Exact-head GitHub checks:

```text
CI run 30725954034 — event pull_request, attempt 1, completed / success
  quality (py3.11)   success
  quality (py3.12)   success

CodeQL run 30725954031 — event pull_request, attempt 1, completed / success
  analyze (python)   success
```

Both `quality` jobs covered locked dependency sync, Ruff lint, Ruff format,
Mypy strict, Pytest and `medscale check`. No rerun, retry, replacement workflow
or manual dispatch occurred.

The complete evidence ledger is in [`decision-basis.md`](decision-basis.md).

## Accepted observations

Six non-blocking observations from the independent implementation review are
carried forward as **accepted**. None was corrected, none was silently
resolved, and none is upgraded into new public behaviour.

```text
NB-1  empty identity arrays rejected through necessary fail-closed inference
NB-2  threshold boundary tests do not alone discriminate integer from float
      comparison, though source inspection confirms integer-only logic
NB-3  evidence-reference local-path check uses an implementation-defined
      heuristic grounded in the senior "not local path" requirement
NB-4  canonical finding document includes a schema member not expressly listed
      in the senior LeakageFinding field list
NB-5  detection_methods allowlist is narrower than the senior generic
      array-of-strings type
NB-6  Unicode combining marks act as token boundaries, consistent with maximal
      Unicode alphanumeric-run semantics
```

Their full text and dispositions are in
[`founder-disposition.md`](founder-disposition.md).

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| [`founder-disposition.md`](founder-disposition.md) | **Controlling**: `FD-B2B-11`, the acceptance decision, its exact scope, the accepted observations, the adoption conditions, the post-adoption state and the continuing prohibitions |
| [`decision-basis.md`](decision-basis.md) | The immutable evidence ledger — authorization, implementation, PR and merge identity, blobs, diff statistics, review, checks, Ready and merge evidence, post-merge mechanical verification, and the criterion-by-criterion mapping to the adopted implementation contract §§1–15 |
| [`acceptance.md`](acceptance.md) | Acceptance criteria for this governance package |

On any conflict, [`founder-disposition.md`](founder-disposition.md) controls.

## Adoption boundary

While this package is local, Draft, Ready-but-unmerged, or
merged-but-not-mechanically-verified, every decision it records is **issued but
not canonically adopted**. Adoption requires all five conditions:

1. a genuinely independent clean-room exact-head review of **this** acceptance
   package;
2. a separate founder Ready decision;
3. a separate founder merge decision;
4. merge into canonical `main`;
5. mechanical post-merge verification.

```text
No subset adopts FD-B2B-11.
```

Until then:

```text
P01-04B2B:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED
```

## Continuing separation

Even after canonical adoption:

```text
FD-B2B-11:                          ADOPTED ON CANONICAL MAIN
P01-04B2B:                          ACCEPTED
P01-04B2C:                          ELIGIBLE FOR A SEPARATE AUTHORIZATION
                                    DECISION; NOT AUTOMATICALLY AUTHORIZED
P01-04B2D:                          NOT AUTHORIZED
P01-04B as a whole:                 INCOMPLETE / NOT ACCEPTED
P01-04C through P01-04G:            NOT AUTHORIZED
Orchestration, dataset scanning,
record-pair discovery:              NOT AUTHORIZED
Real Pilot-01 split:                NOT AUTHORIZED
Real or canonical leakage audit:    NOT AUTHORIZED
Fixture facade, split facade, CLI,
filesystem publication:             NOT AUTHORIZED
P01-03G or real dataset access:     NOT AUTHORIZED
B0/B1 execution:                    NOT AUTHORIZED
Model access:                       NOT AUTHORIZED
Inference:                          NOT AUTHORIZED
Retrieval:                          NOT AUTHORIZED
Metrics or benchmark execution:     NOT AUTHORIZED
Training or fine-tuning:            NOT AUTHORIZED
Publication:                        NOT AUTHORIZED
Clinical use:                       NOT AUTHORIZED
```

B2B acceptance makes a later B2C authorization decision **eligible for
consideration**. It does not itself authorize B2C, and this package contains no
prospective B2C implementation authority.

## What this package does not do

It does not authorize B2C or B2D, accept P01-04B as a whole, correct any
accepted observation, expand the accepted two-path implementation scope,
authorize orchestration or dataset scanning, execute the real Pilot-01 split,
run a real or canonical leakage audit, authorize dataset or model access,
authorize inference, retrieval, metrics, benchmark execution, training or
fine-tuning, dispatch or rerun any workflow, modify implementation, tests,
workflows, dependencies or artifacts, modify any prior governance package, or
authorize a Ready transition or merge.
