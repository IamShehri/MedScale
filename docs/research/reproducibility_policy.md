# Reproducibility Policy

- **Status:** Foundational (binding on all MedScale work)
- **Date:** 2026-07-09
- **Related:** the program rules R1–R7; `docs/vision/MEDSCALE_RESEARCH_VISION.md`;
  `docs/research/research_questions.md`

This policy is the scientific companion to the engineering rules. It translates R1–R7
into operational requirements that every ticket, script, and result artifact must meet. A
result that does not satisfy this policy is not a result — it is an anecdote, and it does
not merit a place in a model card, README, or publication.

---

## Principle 1 — Determinism

Every scorer and every data-generation step is **deterministic and unit-tested**. Given
the same inputs and seed, it produces byte-identical output.

- Seeds are explicit inputs, never implicit (`--seed 0`, recorded in the artifact).
- `medscale data build --split train --n N --seed S` is **byte-reproducible**.
- Where hardware/library nondeterminism is unavoidable (GPU kernels), it is disclosed in
  the artifact and its magnitude is bounded by the reported confidence interval.

## Principle 2 — Environment is pinned and captured

- Python 3.11, dependency lockfile committed; no unpinned runtime dependency.
- External tools are pinned **and checksummed** — the HL7 Java validator is recorded by
  version + SHA-256; Synthea by version + config + seed.
- Every run artifact records: git sha, config hash, dataset hash, seed, wall-clock, and
  (for GPU runs) peak VRAM. No hidden state, no un-versioned local tweaks.

## Principle 3 — Data provenance and licensing (R2, R3)

- **Synthetic data only.** No PHI, ever. If a task appears to need MIMIC or any
  credentialed dataset, work **stops** and a licensing/PHI note is raised.
- Every `data/` directory carries a `LICENSE.md`: source, SPDX id, redistribution rights,
  derivative-model rights, DUA (y/n), and the URL the terms were read from. Enforced by
  `check_dataset_licenses.py` in CI from T0.
- Platform-wide licence invariant: every model, dataset, and value set MedScale ships or
  trains on must permit **derivative models + commercial use**. SNOMED CT is interface-only,
  licence-gated, never vendored.

## Principle 4 — Contamination control is a test, not a comment

- Train / dev / test splits are created up front (T3) and fixed.
- The training-data build **asserts at build time** that no test-split bundle hash appears
  in training. This is a hard, failing test — not a comment, not a manual check.
- `bench/test/` is never used for model selection or tuning. Nothing is tuned on test.
  Ever. Doing so to manufacture a win is explicitly prohibited.

## Principle 5 — Metric integrity: no LLM-as-judge in any primary metric

- Every headline (primary) metric is **deterministic and executable**: validator output,
  executed FHIRPath results, or set-F1 over `(resource_type, field, value)` triples.
- LLM-as-judge is **never** part of a primary metric. Any secondary quality score is
  isolated, explicitly labeled as secondary, and never headlined.
- Ground truth for T-VALIDATE is the validator's exact output — no model in the loop.

## Principle 6 — Statistical honesty

- No performance claim without a reproducible script **and** a committed result artifact
  (R7). No "state of the art." No superlatives.
- Comparisons report **three seeds, mean ± 95% confidence interval.** A difference inside
  seed variance is reported as *no difference*, not as a win.
- **Constraint delta and prompting delta are reported separately** (the 2×2 in T4/T7), so
  the source of any improvement is unambiguous.

## Principle 7 — Negative results are first-class

If MESC-v0 does not beat the grammar-constrained base by more than seed variance, that is
stated plainly in the model card and README. A well-run null result is publishable and
worth more than a quiet retreat or a tuned-on-test illusion. Refuting a research question
in `research_questions.md` is a valid, valued outcome.

## Principle 8 — Citation integrity (R1)

- No paper title, author, year, or DOI is written from memory. Every citation comes from a
  live API response with a resolvable identifier plus `verified_at` and `source_api`.
- `check_citations.py` fails CI if any litdb row lacks an identifier or `verified_at` /
  `source_api` — wired in from T0, before data exists.
- Raw API responses are stored verbatim for audit.

## Principle 9 — Verification is a command that was actually run (R5)

- "Done" means a verification command was executed and its output pasted — never
  "should work."
- Each ticket names its acceptance command; the pasted output is the evidence.
- Reproduction instructions are complete enough for a third party to re-run from the
  committed artifacts alone.

## Principle 10 — Auditability and change control

- Result artifacts are committed alongside the code that produced them; benchmarks version
  their task and metric definitions.
- Controlled vocabularies (see `paper_taxonomy.md`) are append-only.
- Any decision costing >1 day to reverse gets an ADR (R6): propose, wait for approval,
  then implement. Any change that weakens this policy requires an ADR and explicit
  operator approval.

---

## Compliance checklist (applied per result artifact)

- [ ] Seed(s) recorded; run is reproducible from committed artifacts.
- [ ] Environment pinned; git sha + config/dataset hashes captured.
- [ ] Data is synthetic; `LICENSE.md` present; licence permits derivative + commercial use.
- [ ] Contamination assertion passed at build time.
- [ ] Primary metric is deterministic + executable; no LLM judge in it.
- [ ] Numbers reported as mean ± 95% CI over ≥3 seeds; constraint vs prompting deltas split.
- [ ] Any citations carry resolvable ids + `verified_at` + `source_api`.
- [ ] Verification command run and output pasted.
- [ ] Null results reported honestly if that is the outcome.
