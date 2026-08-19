# Founder Authorization Candidate — FD-MESC-BT-READINESS-REPAIR-1

Status: **RECORDED IN DRAFT PACKAGE — INACTIVE UNTIL CANONICALLY ADOPTED**

Date: 2026-08-20

## Decision identity

`FD-MESC-BT-READINESS-REPAIR-1`

## Proposed authorized action

`MESC BACKBONE TOURNAMENT — BOUNDED READ-ONLY READINESS BLOCKER REMEDIATION AND PROTOCOL-FREEZE COMPLETION`

## Preconditions

This authorization may activate only after all of the following are mechanically satisfied:

1. then-current canonical `main` is equal to or descends from readiness-gate merge `24faa6fae47f96236407f8e1fa2b262abba5894f`;
2. PR #126 / readiness-gate adoption remains present in canonical ancestry;
3. the separate prior readiness result is adopted or otherwise canonically reconciled as `FD-MESC-BT-READINESS-1 = CONSUMED` with terminal result `BLOCKED`;
4. this repair package is based on then-current canonical truth or is rebased/reissued before review if main moved materially;
5. the exact repair-package head passes required exact-head CI;
6. the exact repair-package head passes required exact-head CodeQL;
7. fresh independent exact-head review reports no unresolved blocking findings;
8. zero review threads remain unresolved or undispositioned, and every resolved or explicitly dispositioned thread has recorded evidence;
9. the founder separately exercises Founder Ready;
10. the founder separately exercises Founder Merge using an exact expected-head guard or equivalent fail-closed protection;
11. post-merge mechanical verification proves canonical main/tree/ordered parents for this package;
12. post-merge canonical `main` is reverified to contain PR #126's readiness-gate merge in ancestry.

Historical chat state or an earlier model-card observation is insufficient evidence for activation or later candidate admission.

## Authority if activated

One bounded repair episode may:

- inspect canonical repository/governance history read-only;
- inspect authoritative public candidate documentation, official registry metadata, licenses, technical reports, and exact Apertus 1.5 legal/AUP material;
- render or otherwise inspect the authoritative Apertus 1.5 AUP without requesting/accepting gated model access and without touching model weights;
- cryptographically or mechanically bind the inspected Apertus 1.5 policy text to its authoritative exact artifact/revision where possible;
- record all material Apertus use restrictions and determine compatibility with the MESC synthetic/hand-authored R2 tournament scope;
- re-resolve all four strategy-preserved candidate model IDs, immutable revisions, and tokenizer/processor revisions from then-current authoritative sources;
- reverify license/access/gating, architecture/context/modalities, security/loading requirements, precision/runtime assumptions, and hardware feasibility without model execution;
- assign candidate dispositions using only the canonical semantics `BLOCKED`, `NOT_ADMITTED`, or `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`;
- keep the optional challenger slot empty;
- if no non-empty candidate remains `BLOCKED`, design and freeze a synthetic/hand-authored R2-compatible evaluation corpus contract covering all six canonical axes;
- create hand-authored/synthetic fixture specifications but not run any model against them;
- freeze exact prompts, formatting, input/output limits, decoding parameters, deterministic seed policy, stop rules, parser, timeout/retry behavior, generation-failure classes, abstention categories, metrics, cost/latency/resource accounting, Compact thresholds, Flagship/Reasoner thresholds, and `NO_SELECTION` rules;
- freeze reproducibility/report/artifact schemas and deterministic digests;
- produce a refreshed candidate manifest, Apertus blocker-resolution report, protocol-freeze report, readiness verdict, execution plan, and a separate **inactive** tournament-execution authorization candidate only if readiness succeeds.

## Mandatory refresh rule

No model identity, revision, tokenizer/processor revision, or access condition from `FD-MESC-BT-READINESS-1` may be silently carried forward as current.

The repair episode must re-resolve every non-empty roster candidate against then-current authoritative sources. If any required current fact cannot be proven, that slot is `BLOCKED`.

## Apertus disposition rule

For the Apertus slot:

- exact authoritative terms conclusively compatible with the bounded R2 tournament scope -> continue normal admission analysis;
- exact authoritative terms conclusively incompatible -> `NOT_ADMITTED` with recorded evidence;
- exact terms incomplete, unreadable, ambiguous, contradictory, or not bindable to the exact Apertus 1.5 artifact -> `BLOCKED`.

The repair episode may not resolve uncertainty by accepting gated model access, accessing weights, running inference, or substituting an older/newer Apertus policy.

## Challenger rule

The optional challenger slot is frozen `EMPTY` for this repair episode. This authorization does not permit population or substitution of a challenger.

## Explicit exclusions

This authorization does **not** permit:

- downloading, opening, loading, inspecting, or accessing model weights;
- requesting or accepting gated model access, gated-access terms, or model-access agreements for any purpose;
- inference or generation;
- benchmark or tournament execution;
- B0 rerun or replication;
- B1/B2/B3 execution;
- P01-06+;
- Pilot-01 test access or scientific-content inspection;
- non-R2-compatible external benchmark ingestion;
- PHI, patient, product, or telemetry data;
- training, continued pretraining, SFT, fine-tuning, QLoRA, adapters, preference optimization, RL, verifier training, or distillation;
- retrieval activation;
- fallback-model substitution;
- quantization changes or derivative quantized tournament entries;
- challenger admission;
- DeepSeek or any other excluded model-family admission;
- MCRL/AMGE/audio/biosignal/donor-runtime implementation;
- publication, clinical, safety, efficacy, release, or production claims.

## Consumption rule

If activated, `FD-MESC-BT-READINESS-REPAIR-1` may be consumed by **one** bounded read-only repair/protocol-freeze episode only.

It ends with exactly one terminal outcome:

- `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`, or
- `BLOCKED`.

Any `BLOCKED` non-empty candidate forces the overall result `BLOCKED`. Fewer than two admitted candidates also forces `BLOCKED`. A conclusively `NOT_ADMITTED` candidate is not itself a package blocker if all other readiness rules remain satisfied.

It cannot be reused to refresh versions, add candidates, or execute the tournament.

## Execution boundary

Even a successful repair episode grants no execution authority.

Until a later exact execution package is separately reviewed, adopted, and mechanically verified:

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
