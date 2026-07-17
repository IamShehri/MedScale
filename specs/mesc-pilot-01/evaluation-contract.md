# MESC Pilot-01 — Evaluation Contract

Status: **foundation evaluation contract**
Authorization: Foundation *** only
Freeze date: 2026-07-17

---

## Layer 1 — Native PubMedQA evaluation

Layer 1 metrics operate on PubMedQA-native deterministic outputs without retrieval or adaptation.

### Decision accuracy

Compares predicted yes/no/maybe/abstain decisions with reference labels across the evaluated split. Missing references or empty inputs produce `status: not_applicable`.

### Macro F1

Computes macro-averaged F1 over yes, no, maybe, and abstain classes. Zero-support classes contribute 0.0 to the macro average. Empty inputs produce `status: not_applicable`.

### Structured-output validity

Reports the fraction of model outputs that parse as valid JSON. Invalid JSON increases abstention and lowers evidence-reference validity.

### Evidence-reference validity

For records with gold annotations, reports the fraction of gold claims whose identifiers appear in predicted claim-support outputs. Missing gold annotations or empty inputs produce `status: not_applicable`.

### Abstention metrics

Reports abstention precision and recall for explicit abstention decisions. Abstention is only valid when evidence is insufficient or ambiguous.

---

## Layer 2 — MESC grounding evaluation

Layer 2 metrics require the manually reviewed 100-example gold subset. They must not be computed or claimed without that subset.

### Supported-claim precision

Fraction of predicted claim-support pairs that match gold claim-support pairs.

### Supported-claim recall

Fraction of gold claim-support pairs recovered by predictions.

### Unsupported-claim rate

Fraction of predicted claim-support pairs with empty or invalid evidence references.

### Citation correctness

Fraction of evidence-reference citations that resolve to valid evidence objects in the gold subset.

### Evidence coverage

Fraction of gold claims that have at least one supporting evidence object in predicted outputs.

---

## Gold-subset gate

Layer 2 metrics are gated behind the reviewed gold subset. Missing gold annotations must produce `status: not_applicable`. No LLM judge is defined as ground truth. An LLM judge may assist validation, but it does not replace manual review.

---

## Missing metric policy

Any metric that cannot be computed because of missing data, missing annotations, empty inputs, or unauthorized execution must return:

```text
value: None
status: not_applicable
note: <reason>
```

Silent omission is not permitted. Metrics must be explicit about unavailability.

---

## Deterministic requirements

All metrics must be deterministic. No stochastic or inference-dependent logic is permitted in the foundation package. Metric implementations must not depend on runtime timestamps, hardware state, or external service availability.

---

## Baseline and QLoRA gates

B0–B3 are definitions only. Baseline execution and QLoRA training require separate explicit authorization. Evaluation contracts must not assume baseline or training execution.

---

## Non-clinical and non-production scope

Evaluation metrics are defined for research and verification purposes only. They are not approved for clinical decision support, production triage, or automated medical inference.
