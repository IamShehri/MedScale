# MESC Backbone Tournament Readiness Repair Gate

Status: **DRAFT GOVERNANCE PACKAGE — INACTIVE / NO EXECUTION AUTHORITY**

Date: 2026-08-20

Canonical base intended for review:

- `main`: `24faa6fae47f96236407f8e1fa2b262abba5894f`
- tree: `7fc48193b3abe9e2249dca4ec2423e220c676b3f`
- canonical readiness-gate merge: PR `#126`
- readiness-gate merge commit: `24faa6fae47f96236407f8e1fa2b262abba5894f`

## Purpose

Open a narrowly bounded governance path after the one-shot `FD-MESC-BT-READINESS-1` readiness episode ended fail-closed with an unresolved Apertus 1.5 acceptable-use-policy evidence requirement.

This package does not reopen or reuse `FD-MESC-BT-READINESS-1`. It proposes a new, separately reviewable authorization candidate:

`FD-MESC-BT-READINESS-REPAIR-1`

If later canonically adopted and activated, that decision may authorize exactly one bounded **read-only blocker-remediation and protocol-freeze-completion episode**.

## Prior readiness outcome to reconcile

The prior episode reported:

```text
FD-MESC-BT-READINESS-1 = CONSUMED
READINESS_RESULT = BLOCKED
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
```

The reported blocking condition was limited to the non-empty Apertus roster slot: the exact Apertus 1.5 usage-policy artifact identity was found, but the complete exact-version policy text/use restrictions were not independently resolved to the evidence standard required by the canonical readiness contract.

This package does not treat that report as self-proving. A later authorized repair episode must mechanically reverify the blocker, then-current repository truth, and all candidate identities/revisions before using them in a readiness verdict.

## Narrow authorized purpose if activated

One repair episode may only:

- reverify then-current canonical MESC main/tree and controlling governance;
- inspect authoritative public Apertus 1.5 license/AUP sources read-only;
- resolve the complete exact-version Apertus 1.5 use restrictions without requesting or accepting gated model access;
- re-resolve exact current IDs and immutable revisions for the four strategy-preserved non-empty candidates because the consumed authorization cannot be reused to refresh versions;
- reverify tokenizer/processor identities, license/access facts, architecture/context/runtime/hardware feasibility from authoritative public metadata;
- deterministically disposition each non-empty candidate using the existing canonical semantics: `BLOCKED`, `NOT_ADMITTED`, or `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`;
- keep the optional challenger slot intentionally empty;
- if and only if no non-empty candidate remains `BLOCKED`, freeze the R2-compatible synthetic/hand-authored corpus contract across all six required axes;
- freeze prompts, decoding, seed policy, parsing, abstention/error handling, metrics, cost/latency accounting, selection thresholds, reproducibility schema, and report digests before any model output exists;
- produce a refreshed candidate manifest, blocker-resolution record, protocol-freeze report, readiness verdict, execution plan, and a separate **inactive** tournament-execution authorization candidate only if readiness succeeds.

## Explicit non-authority

This package does not authorize:

- model-weight download/open/load/access;
- requesting or accepting gated model access, gated-access terms, or model-access agreements for any purpose;
- inference or generation;
- tournament/benchmark execution;
- B0 rerun or B1/B2/B3 execution;
- P01-06+;
- Pilot-01 test scientific-content access;
- PHI, patient, product, telemetry, or non-R2-compatible benchmark data;
- training, continued pretraining, SFT, QLoRA, adapters, preference optimization, RL, or verifier training;
- retrieval;
- fallback-model substitution;
- quantization changes;
- challenger population;
- excluded model-family admission;
- MCRL/AMGE/audio/biosignal/donor-runtime implementation;
- publication, clinical, safety, efficacy, release, or production claims.

## Fail-closed rule

The repair episode must terminate `BLOCKED` if any required evidence for any non-empty candidate remains unresolved; if Apertus use restrictions cannot be proven; if then-current candidate revisions cannot be pinned; if R2 compatibility or security/runtime feasibility remains uncertain; if fewer than two distinct candidates are admitted; if any of the six evaluation axes cannot be frozen; or if equal-treatment/scoring decisions would require observing model outputs.

A conclusively incompatible Apertus license/AUP condition may produce `NOT_ADMITTED`; missing or unreadable evidence must produce `BLOCKED`.

## Adoption boundary

This package is docs/governance only. `FD-MESC-BT-READINESS-REPAIR-1` remains inactive unless this exact package receives exact-head CI/CodeQL, fresh independent exact-head review, zero unresolved or unsupported review-thread dispositions, separate Founder Ready, separate Founder Merge with expected-head protection, and post-merge canonical verification.

Canonical repository/GitHub truth overrides this package if anything moves before adoption.