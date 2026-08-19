# P01-05 B0 Scientific Result Reconciliation

Status: **DESCRIPTIVE BASELINE RECORDED — NO TUNING AUTHORIZED**

## What the result establishes

The accepted B0 episode provides one frozen validation baseline for the exact
Pilot-01 model/revision/configuration under the canonical B0 runner:

```text
accuracy: 104 / 150 = 0.6933333333333334
coverage: 150 / 150 = 1.0
generation failures: 0
```

It establishes that this exact execution path produced a complete, parseable
validation report under the recorded runtime and inputs.

## Output-distribution observation

The model output distribution was:

```text
predicted:
maybe 1
no    47
yes   102

gold aggregate:
maybe 17
no    50
yes   83
```

A bounded descriptive observation is therefore warranted: the B0 output
distribution emits `maybe` much less often than the validation gold distribution.

This record does **not** infer class-specific recall, precision, calibration, or a
confusion matrix because the canonical preserved report does not expose per-example
gold labels. It also does not assign a causal explanation to the distribution
difference.

## What the result does not establish

The B0 result does not establish:

- test-set performance
- clinical safety or effectiveness
- evidence-grounding benefit
- B1 benefit
- uncertainty calibration quality
- abstention superiority
- robustness to distribution shift
- superiority to MedGemma or any other comparator
- readiness for training, release, publication, or deployment

## Anti-adaptation rule

No prompt, decoding setting, model revision, class policy, or evaluation rule may
be changed retroactively to improve this B0 result.

The single-example infrastructure probe preceded the full run, but its semantic
answer was withheld and no configuration was changed from the frozen B0 settings.
The later hash-domain reconciliation changed no scientific computation and
performed no additional inference.

Any future intervention motivated by the observed `maybe` imbalance belongs to a
separately preregistered/authorized experiment. This acceptance package does not
authorize that intervention.
