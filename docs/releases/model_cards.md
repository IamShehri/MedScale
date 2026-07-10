# Model Card Requirements

- **Status:** Strategy (ADR-0010, Proposed)
- **Date:** 2026-07-10

A MedScale model card is a *verification document*, not marketing. A card that asserts
capability without a committed result artifact violates R7 and fails release
validation. Required sections, in order:

## 1. Identity

- Name + version (`mesc-fhir-v0.1`), release date, GitHub source tag, manifest hash.
- One-sentence honest description ("QLoRA adapter over <base> for FHIR
  generation/validation/repair on synthetic data").

## 2. Mandatory statements (verbatim floor, every card)

> **Not a medical device.** This model must not be used for diagnosis, treatment,
> triage, or any clinical decision-making.
>
> **Synthetic data only.** This model was trained and evaluated exclusively on
> synthetic data. Its behavior on real clinical data is unmeasured — deliberately, as
> a matter of privacy policy (one-way PHI boundary).

Why verbatim: these two statements are load-bearing for the whole program's safety and
licensing posture; paraphrase drift weakens them.

## 3. Model details

Base model (exact id + revision + licence tier), adapter method (QLoRA config), grammar
constraint used, context of the form-vs-content hypothesis (RQ1/RQ2), parameters
touched, compute used (recorded, because the affordability claim is part of the science).

## 4. Training data

Dataset name + version + content hash; generator (Synthea version, seed, config);
per-class corruption sampling if used (RQ4); licence of every source; the build-time
contamination assertion output.

## 5. Evaluation

Benchmark name + **version** (scores are meaningless without it); all primary metrics
with 3 seeds, mean ± 95% CI; constraint delta and prompting delta reported separately;
per-class failure analysis; **negative results stated plainly** — a null RQ2 result
appears here in the same font size as any win.

## 6. Limitations & out-of-scope use

English/synthetic-only; unmeasured transfer to real clinical text (stated, not hedged);
resource types/profiles held out; known failure classes from the taxonomy; explicit
out-of-scope list (clinical use, PHI processing, unconstrained generation claims).

## 7. Reproduction

Pointer to the replication package: repo tag, manifest, exact commands, expected
outputs. A reader with the manifest must be able to re-run the evaluation.

## 8. Citation & licence

CFF/BibTeX block; Apache-2.0 (adapter) + base-model attribution per its terms.

## HF metadata block (front-matter)

`license`, `base_model`, `tags` (incl. `not-for-clinical-use`), `datasets` (the exact
versioned dataset ids), `model-index` results only for deterministic primary metrics —
never a secondary/judged score.
