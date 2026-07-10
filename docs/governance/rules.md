# Program Rules (R1–R7)

- **Status:** Foundational (binding on all MedScale work; changes require an ADR)
- **Date:** 2026-07-10
- **Related:** [reproducibility policy](../research/reproducibility_policy.md),
  [Research Vision](../vision/MEDSCALE_RESEARCH_VISION.md), [ADRs](../adr/)

These are the seven rules the rest of the documentation cites by number. They are stated
here once, canonically. Every other document references these definitions rather than
restating them. A change to any rule requires an ADR and explicit operator approval.

---

## R1 — No fabricated citations

No paper title, author, year, or identifier is ever written from memory. Every citation
enters via a live API response (Semantic Scholar, OpenAlex, PubMed, arXiv) carrying a
resolvable identifier plus `verified_at` and `source_api`. An API returning nothing is
recorded as `NOT_FOUND`, never backfilled. Raw responses are stored for audit.

## R2 — Synthetic-only; the PHI boundary is one-way and absolute

MedScale trains and evaluates on synthetic data only (Synthea, hand-authored fixtures).
No real patient data, product telemetry, or clinical content — from Afia or anywhere —
may ever enter MedScale training, evaluation, or benchmark data. If a task appears to
need real or credentialed data (e.g. MIMIC), **work stops** and a licensing/PHI note is
raised. Models and schemas flow MedScale → Afia; data never flows back.

## R3 — Licensing permits derivative models and commercial use

Every model, dataset, and value set MedScale ships or trains on must permit **derivative
models and commercial use**, so that Afia and others may build on it. Each `data/`
directory carries a `LICENSE.md` (source, SPDX id, redistribution + derivative rights,
DUA status, URL). SNOMED CT is interface-only, licence-gated, never vendored. Enforced in
CI once data exists.

## R4 — One ticket per session

Finish, verify, and commit one unit of work before starting the next. Never open ticket
N+1 while N is unfinished. This is the primary defense against the scope sprawl that
kills solo research programs.

## R5 — Verification is a run, not a claim

"Done" means a verification command was actually executed and its output recorded — never
"should work." Each ticket names its acceptance command; the pasted output is the
evidence. Reproduction instructions must be complete enough for a third party to re-run
from committed artifacts alone.

## R6 — Expensive decisions require an ADR

Any decision costing more than roughly one day to reverse is recorded as an
[Architecture Decision Record](../adr/): propose, wait for approval, then implement.
Program-level decisions (topology, licensing, base model) sit above technical ones.

## R7 — No result without a script and a committed artifact

No performance claim exists without a reproducible script **and** a committed result
artifact. No superlatives, no "state of the art." Comparisons report three seeds,
mean ± 95% confidence interval; a difference inside seed variance is reported as *no
difference*. Well-run **negative results are first-class** and published plainly.

---

## Quick reference

| Rule | One line |
|---|---|
| R1 | Citations only from live APIs with resolvable ids. |
| R2 | Synthetic-only; PHI boundary is one-way and absolute. |
| R3 | Everything shipped permits derivative + commercial use. |
| R4 | One ticket per session. |
| R5 | Verification is an executed command with pasted output. |
| R6 | Decisions >1 day to reverse get an ADR (propose → approve → implement). |
| R7 | No claim without a reproducible script + committed artifact; negatives count. |
