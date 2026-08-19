# MESC Backbone Tournament Readiness Repair — Terminal Result

Status: **READ-ONLY REPAIR EPISODE CONSUMED / TERMINAL BLOCKED**

Date: 2026-08-20

## Authority consumed

```text
FD-MESC-BT-READINESS-REPAIR-1 = CONSUMED
READINESS_RESULT = BLOCKED
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
TEST_PARTITION_ACCESS = NOT_AUTHORIZED
```

This directory records the single bounded read-only readiness blocker-remediation episode authorized by canonical merge `dea2b05516e0fafadcc5902fdad0558d77c020cd`.

## Canonical repository state inspected

Episode start and end canonical state remained:

```text
main = dea2b05516e0fafadcc5902fdad0558d77c020cd
tree = 2860cbfdc568ab2564d5c8e8e9063ba9f056dd1e
ordered parents of canonical merge:
1. 24faa6fae47f96236407f8e1fa2b262abba5894f
2. 93836e6d192b22797b60bd893148d35d11561696
merge verification = verified=true / reason=valid
```

The result package itself is documentation/evidence only and does not change the canonical authority state until separately reviewed and adopted.

## Terminal blocker

`BT-RDY-BLK-APERTUS-AUP-001` remains unresolved.

The exact official Apertus 1.5 usage-policy artifact is mechanically identified as:

```text
repository = swiss-ai/apertus-legal
path = apertus_1.5/USAGE_POLICY.pdf
git_blob_sha = 8ddd8e25b6672340dd4f921ba623578571a65526
size = 53794 bytes
```

The episode could not obtain a complete readable representation of that exact PDF through the authorized public read interfaces while preserving the absolute prohibition on gated-access request/acceptance. The exact artifact therefore cannot be interpreted and version-bound to the evidence standard required for admission.

Under the canonical fail-closed semantics this is `BLOCKED`, not `NOT_ADMITTED`.

## Roster disposition

| Slot | Candidate | Disposition |
|---|---|---|
| 1 | OpenAI `openai/gpt-oss-20b` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 2 | Swiss AI `swiss-ai/Apertus-v1.5-8B` | `BLOCKED` |
| 3 | Microsoft `microsoft/Phi-4-multimodal-instruct` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 4 | Google `google/medgemma-1.5-4b-it` | `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` |
| 5 | optional challenger | `EMPTY` |

Any non-empty `BLOCKED` slot forces the overall readiness result `BLOCKED`.

## Protocol-freeze consequence

The corpus, prompts, decoding, scoring, role thresholds, schemas, and protocol digests were **not frozen**, because the repair authorization permits those steps only if no non-empty candidate remains `BLOCKED`.

No inactive tournament-execution authorization candidate is produced because readiness did not succeed.

## Files

- `candidate-manifest.md`
- `apertus-blocker-resolution.md`
- `protocol-freeze-report.md`
- `readiness-verdict.md`
- `execution-plan.md`
