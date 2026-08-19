# Founder Decision — FD-P01-05-B0-EXEC-1

Status: **RECORDED / CONSUMED BY ONE EXECUTION EPISODE**

Date: 2026-08-19

## Decision

The founder separately authorized the next gated action after remote model
acquisition/readiness completed:

```text
P01-05 B0 REAL ZERO-SHOT VALIDATION EXECUTION
```

The authorization was consumed by one bounded execution episode over the frozen
150-example validation input.

## Authorized scope

- `meta-llama/Llama-3.2-3B-Instruct`
- exact immutable model/tokenizer revision recorded in this package
- exact frozen P01-04 validation input
- B0 only
- deterministic greedy generation
- canonical B0 prompt/orchestration/loader
- no supplied evidence channel
- no quantization
- validation scoring and deterministic report generation
- external evidence preservation

## Explicitly not authorized

- B1 execution
- test execution or test scientific-content inspection
- training / QLoRA / preference optimization / RL
- retrieval
- fallback-model substitution
- alternate model or revision
- prompt/configuration tuning based on the probe or result
- P01-06 or later
- publication or clinical claims
- repository product/runtime behavior changes

## Consumption and continuation

This decision does not remain as an open-ended execution permit. The authorized
B0 episode completed. Any rerun, replication, comparator run, B1 execution, or
later phase requires a new explicit gate/decision.

The historical P01-05 entry contract remains correct for its own adoption event:
that adoption did not authorize execution. This later decision is the separate
authority that permitted the accepted episode.
