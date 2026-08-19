# MESC Backbone Tournament Readiness Repair 2

Status: **FOUNDER-APPROVED CANDIDATE / INACTIVE UNTIL CANONICALLY ADOPTED**

Date: 2026-08-20

## Purpose

This package proposes one new bounded read-only readiness-remediation episode after canonical `FD-MESC-BT-READINESS-REPAIR-1` was consumed with terminal result `BLOCKED`.

The sole blocking finding carried forward for remediation is:

```text
BT-RDY-BLK-APERTUS-AUP-001
```

The exact Apertus 1.5 public AUP artifact identity is already known, but the prior episode could not obtain and bind a complete readable representation of the exact PDF through the interfaces then used.

## Canonical base

```text
main = 4f36d46c4b99829bb91c6d2efcf520c4145eb376
tree = fbceb702aa5e9739013ab8c7b8271e44350ac895
```

Canonical ancestry includes:

- PR #127 / repair-1 authorization adoption;
- PR #128 / terminal blocked repair-1 result;
- `FD-MESC-BT-READINESS-REPAIR-1 = CONSUMED / REUSABLE = NO`.

## Proposed decision

```text
FD-MESC-BT-READINESS-REPAIR-2
```

If and only if this exact package is canonically adopted after exact-head gates, it authorizes one bounded read-only episode to:

1. obtain the exact public Apertus 1.5 AUP binary from the authoritative `swiss-ai/apertus-legal` repository without gated model access;
2. verify the bytes against the authoritative Git blob identity before interpreting them;
3. render and/or extract text from that exact verified PDF locally;
4. record all material use restrictions and deterministically resolve Apertus as `BLOCKED`, `NOT_ADMITTED`, or `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`;
5. refresh all four non-empty candidate identities, immutable revisions, access conditions, and required admission evidence from then-current authoritative public sources;
6. if and only if no non-empty candidate remains `BLOCKED`, complete the R2-compatible corpus/protocol freeze required by the canonical tournament contract;
7. produce a deterministic terminal result package and, only on a ready verdict, a separate inactive execution-authorization candidate.

## Absolute exclusions

This package does not authorize:

- model-weight download, opening, inspection, loading, or access;
- gated model access request or acceptance;
- acceptance of gated-access terms or model-access agreements for any purpose;
- inference or generation;
- benchmark or tournament execution;
- B0/B1/B2/B3 execution;
- P01-06+;
- Pilot-01 test-content inspection;
- PHI, real patient data, product telemetry, or non-R2-compatible benchmark data;
- training, continued pretraining, SFT, fine-tuning, QLoRA, adapters, preference optimization, RL, distillation, or verifier training;
- retrieval activation;
- fallback substitution or quantization changes;
- challenger population;
- excluded model-family admission;
- downstream runtime/product implementation;
- publication, clinical, safety, efficacy, release, or production claims.

## One-shot rule

If activated, `FD-MESC-BT-READINESS-REPAIR-2` is consumed by one bounded episode and ends with exactly one terminal result:

- `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`, or
- `BLOCKED`.

It is never reusable.
