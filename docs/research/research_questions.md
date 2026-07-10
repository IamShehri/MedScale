# MedScale Research Questions

- **Status:** Foundational (governs what is worth building)
- **Date:** 2026-07-09
- **Related:** `docs/vision/MEDSCALE_RESEARCH_VISION.md`, `docs/research/reproducibility_policy.md`

These are the questions MedScale exists to answer. Every ticket must trace to at least
one. Each question is stated so that it can be **falsified**, names the **artifact** that
tests it, and records its **current status**. No claim in this document is settled until
a committed result artifact supports it (Rule R7).

> On citations: this document deliberately contains **no** paper titles, authors, years,
> or DOIs. Under Rule R1, evidence for or against these questions is drawn only from the
> literature database (T1), where every row carries a resolvable identifier, `verified_at`,
> and `source_api`. Related work is referenced by litdb id once populated, never from memory.

---

## RQ1 — Does grammar decouple form from content?

**Statement.** Can grammar-constrained decoding against FHIR StructureDefinitions
guarantee structural validity independently of content quality — so that structural
validity approaches ~100% under constraint regardless of the base model's un-constrained
FHIR competence?

**Why it matters.** This is the load-bearing assumption of the whole program. If form is
free, a cheap adapter needs only to learn content, and MedScale is affordable on
Colab-class compute.

**Test.** T2 grammar engine + T4's 2×2 (unconstrained vs grammar-constrained × zero/few
shot). Report the *constraint delta* separately from the *prompting delta*.

**Falsified if.** Grammar-constrained decoding fails to reach near-total structural
validity, or does so only by collapsing content quality (empty/degenerate but valid
resources). Either outcome refutes "form is free."

**Status.** OPEN — untested until T2/T4.

---

## RQ2 — What is the marginal value of fine-tuning over a grammar-constrained base?

**Statement.** Once the base model is grammar-constrained, how much *additional* content
quality does a QLoRA adapter buy, measured on MedScale-Bench primary metrics?

**Why it matters.** Distinguishes "training teaches content" (adapter helps meaningfully)
from "grammar was doing all the work" (adapter adds nothing beyond seed variance).

**Test.** T7: base vs MESC-v0, both grammar-constrained, three seeds, mean ± 95% CI.

**Falsified / null result if.** MESC-v0 does not beat the grammar-constrained base by
more than seed variance. This null result is **publishable and reported plainly** in the
model card and README — never hidden, never manufactured away by tuning on test.

**Status.** OPEN — depends on RQ1 result first.

---

## RQ3 — Is the validator a perfect, infinitely scalable teacher?

**Statement.** Can the FHIR validator generate unlimited, exact, free supervision for
structural error detection (T-VALIDATE) and repair (T-REPAIR) — such that a model trained
on validator-labeled data learns to reproduce validator judgments?

**Why it matters.** If true, one class of clinical-AI supervision becomes free and exact,
sidestepping the labeling bottleneck that constrains medical NLP.

**Test.** T5 training-data pipeline (validator-as-teacher) + T-VALIDATE / T-REPAIR scores
in T3/T7.

**Falsified if.** Validator-labeled training fails to transfer — the model cannot
reproduce validator judgments on held-out resources, or overfits to the specific
corruption distribution rather than learning error classes.

**Status.** OPEN.

---

## RQ4 — Do FHIR errors decompose cleanly, and does per-class negative sampling help?

**Statement.** Do conformance errors partition cleanly into the five-class taxonomy
(structural / terminology / cardinality / semantic / hallucinated-entity), and does
explicitly corrupting resources along each class (negative sampling) improve per-class
detection and repair?

**Why it matters.** A clean taxonomy makes failure analysis actionable and lets training
target weaknesses class by class.

**Test.** T3 failure taxonomy + T5 negative sampling + T7 per-class failure analysis
(50 sampled errors classified by taxonomy).

**Falsified if.** Errors resist clean classification (large "other"/overlapping bucket),
or per-class negative sampling yields no per-class improvement over uniform corruption.

**Status.** OPEN.

---

## RQ5 — Can we measure and reduce extraction hallucination without an LLM judge?

**Statement.** For note→bundle extraction (T-EXTRACT), can a deterministic span-alignment
scorer measure the rate of output entities with no supporting span in the source note,
and does constraint and/or the adapter reduce that rate?

**Why it matters.** Faithfulness — not fluency — is the safety-critical property in
clinical extraction. It must be measured mechanically, not judged.

**Test.** T7 alignment scorer + hallucination rate across the 2×2 conditions.

**Falsified if.** Span alignment cannot reliably distinguish supported from unsupported
entities (scorer is too noisy to be a primary metric), or neither constraint nor the
adapter moves the hallucination rate.

**Status.** OPEN.

---

## RQ6 — Does competence transfer across resource types and profiles?

**Statement.** Does a model trained on the curriculum (single-resource → multi-resource →
bundle-level) generalize to resource types, cardinalities, and profiles held out of
training?

**Why it matters.** Determines whether MedScale learns FHIR-general skills or memorizes
a fixed set of shapes.

**Test.** Train/dev/test splits (T3) with contamination control (T5 build-time hash
assertion) + T7 transfer analysis.

**Falsified if.** Performance collapses on held-out resource types/profiles despite
strong in-distribution scores.

**Status.** OPEN.

---

## RQ7 — Can terminology be grounded under licence constraints? (Horizon 2)

**Statement.** Can outputs be grounded in real value sets (LOINC, RxNorm; SNOMED CT only
via a licensed, non-vendored interface) well enough to pass terminology validation,
without ever embedding restricted content in the repository?

**Why it matters.** Terminology correctness is where clinical data becomes interoperable
and where licensing is most dangerous.

**Test.** `fhirkit.validate` terminology layer (T2) + a future terminology-focused bench
slice (Horizon 2).

**Falsified if.** Terminology grounding is unattainable within the permissive-licence
envelope, or requires vendoring restricted content (which is prohibited).

**Status.** OPEN — Horizon 2; interface built in T2, not headlined in v0.

---

## Traceability map (RQ → ticket)

| RQ | Primary tickets |
|---|---|
| RQ1 form vs content | T2, T4 |
| RQ2 marginal value of fine-tuning | T6, T7 |
| RQ3 validator as teacher | T5, T3, T7 |
| RQ4 error taxonomy + negative sampling | T3, T5, T7 |
| RQ5 hallucination measurement | T7 |
| RQ6 transfer / generalization | T3, T5, T7 |
| RQ7 terminology grounding | T2 (interface), Horizon 2 (evaluation) |

Work that maps to no RQ is out of scope until the vision document is amended.
