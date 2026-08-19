# MESC Backbone Tournament — Prior Readiness Blocker Record

Status: **DRAFT RECORD FOR CANONICAL REVIEW**

Date: 2026-08-20

## Scope

This document records the bounded result that motivated the proposed readiness-repair gate. It does not itself prove or reactivate the prior episode, and it grants no new authority.

If this exact repair package is later canonically adopted, this record may serve as the canonical reconciliation of the prior episode's reported terminal state. Before adoption it remains a proposed reconciliation only.

## Prior authorization

```text
FD-MESC-BT-READINESS-1
```

The controlling canonical gate states that the authorization may be consumed by one bounded readiness/protocol-freeze episode only and ends in either `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE` or `BLOCKED`.

## Reported terminal state

```text
FD-MESC-BT-READINESS-1 = CONSUMED
READINESS_RESULT = BLOCKED
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
TEST_PARTITION_ACCESS = NOT_AUTHORIZED
```

## Reported roster disposition

The bounded episode reported the following provisional evidence outcome, which a later authorized repair episode must independently refresh against then-current authoritative sources:

| Slot | Family | Reported disposition |
|---|---|---|
| 1 | OpenAI `gpt-oss-20b` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 2 | Swiss AI `Apertus 1.5 8B` | `BLOCKED` |
| 3 | Microsoft `Phi-4 Multimodal 5.6B` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 4 | Google `MedGemma 1.5 4B IT` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 5 | optional challenger | `EMPTY` |

These dispositions are not execution authority and must not be treated as frozen current model identities after the prior one-shot authorization has been consumed.

## Blocking finding

```text
ID: BT-RDY-BLK-APERTUS-AUP-001
CANDIDATE: Swiss AI Apertus 1.5 8B
CATEGORY: LICENSE / ACCEPTABLE-USE EVIDENCE
DISPOSITION: BLOCKED
```

The episode reported that the authoritative Apertus legal repository exposed the exact Apertus 1.5 usage-policy artifact:

```text
repository:
swiss-ai/apertus-legal

path:
apertus_1.5/USAGE_POLICY.pdf

git_blob_sha:
8ddd8e25b6672340dd4f921ba623578571a65526

size:
53794 bytes
```

The unresolved issue was not artifact identity. The unresolved issue was the inability, within that episode's read interfaces, to independently resolve the complete exact-version policy text and all material use restrictions to the evidence standard required for candidate admission.

## Required semantics

The canonical readiness rules distinguish:

- `BLOCKED`: required evidence remains unresolved, unproven, contradictory, or unavailable;
- `NOT_ADMITTED`: authoritative evidence conclusively proves a disqualifying condition;
- `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`: all admission evidence is proven for proposal into a later inactive execution-authorization package.

Therefore the Apertus slot may become `NOT_ADMITTED` only if exact authoritative Apertus 1.5 terms conclusively establish incompatibility. Missing, unreadable, incomplete, or ambiguous evidence remains `BLOCKED`.

## Gated-access boundary

The blocker may be investigated only through authoritative public legal/AUP material. A later repair episode may not request or accept gated model access, gated-access terms, or model-access agreements for any purpose to obtain additional evidence or resolve uncertainty.

## No protocol-freeze completion claim

Because a non-empty candidate remained `BLOCKED`, the prior episode did not claim a successful execution-ready protocol freeze. The following remain subject to a later separately authorized episode:

- refreshed exact candidate revisions;
- exact synthetic/hand-authored corpus hash and count;
- all-six-axis corpus coverage proof;
- exact system/task prompts;
- decoding and seed policy;
- parser/error/abstention contract;
- metric weights and role thresholds;
- runtime/provider/hardware envelope;
- prompt/protocol digest;
- reproducibility/artifact schema;
- inactive execution-authorization candidate eligibility.

## Non-effects

This record does not authorize Apertus gated access, any other model access, requesting or accepting gated-access terms or model-access agreements, model execution, inference, benchmark execution, training, retrieval, test access, quantization changes, or downstream implementation.