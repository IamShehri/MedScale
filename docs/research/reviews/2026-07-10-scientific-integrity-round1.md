# Scientific Integrity Review #1 — Post Round-1 Corpus

- **Date:** 2026-07-10 · **Trigger:** first corpus milestone (1,386 records)
- **Stance:** as a Nature/NEJM methods reviewer and NIH panelist would read the project
  today — hostile to convenience, friendly to honesty
- **Scope reviewed:** litdb methodology, corpus, evidence model, statistical plan,
  benchmark design intentions, ethics/regulatory posture

## Verdict in one line

The *policies* are unusually rigorous for a project this young; the **round-1 corpus
has four methodological weaknesses that must be addressed before any publication
describes it as a systematic search** — none fatal, all fixable, and one
(the corpus-purpose mismatch, S5) changes how pillar 2 should be described.

## Findings (ordered by scientific impact)

### S1 — Result caps make round 1 a *scoping* search, not a systematic one 🔴 High

Source APIs return relevance-ranked results; taking the top 50 per query is a
relevance-biased sample, not the matching population. Q2 alone matched 7,530 OpenAlex
works — round 1 captured 0.66% of them. **Why it matters:** any paper calling this a
systematic review would be rejected on search-completeness grounds; PRISMA requires
reporting the full identified population or a defensible sampling frame.
**Resolution:** (a) describe round 1 as a *scoping round* in all documents (it was
capped deliberately, pending ADR-0016 — legitimate, if named honestly); (b) record
per-query total-match counts (already in the archived payloads) as coverage ratios in
the round report; (c) plan a definitive round at meaningful caps after ADR-0016.

### S2 — Identifier-exact dedupe leaves version duplicates in the corpus 🔴 High

The documented fuzzy title+year pass (strategy §3, pass 2) is not yet implemented.
Cross-source duplicates with disjoint identifier types — classically, an arXiv preprint
and its published DOI version — remain as two records. **Why it matters:** inflates
PRISMA counts; risks double-inclusion; conflates preprint and published versions of the
same claim (version confounding). **Resolution:** implement the fuzzy pass *before*
screening begins, with merge decisions logged (both provenances retained, as the
strategy already specifies).

### S3 — Single-operator screening has no reliability control 🟠 Medium

PRISMA-grade reviews use dual screening or at minimum report single-reviewer status as
a limitation with a calibration/audit mechanism. **Why it matters:** reviewer-1
question on any litdb methods paper. **Resolution:** state the limitation explicitly in
the search strategy now; add a self-audit mechanism (re-screen a random 5–10% sample
after a washout period, report agreement); invite a second screener when a collaborator
exists (H2).

### S4 — Parser-proposed evidence tiers are assumptions, not verifications 🟡 Medium-low

"Journal ⇒ peer-reviewed" from OpenAlex venue type admits non-reviewed and predatory
venues; tier is currently a metadata inference. **Why it matters:** tier feeds future
evidence weighting. **Resolution:** already half-done (tiers documented as proposals
screening may correct) — make tier confirmation an explicit screening-checklist item.

### S5 — Corpus-purpose mismatch: this is a *methods* corpus, not clinical evidence 🔴 High (conceptual)

Round 1's queries (correctly, per the RQs) retrieved AI/NLP/FHIR *methods* literature —
~35% arXiv. But pillar 2's evidence model is built for *clinical* claims (PICO slots,
effect measures, study-design grading). Methods papers rarely contain PICO-shaped
claims. **Why it matters:** demonstrating the evidence-object pipeline on this corpus
will look forced; a reviewer would note the mismatch between the evidence schema and
the corpus feeding it. **Resolution:** name the two corpora explicitly — litdb round 1
= the *related-work/methods corpus* backing MedScale's own papers (R1 citations);
a future *clinical-evidence corpus* (PubMed clinical queries, trial registries) is the
pillar-2 demonstration substrate, ingested under the same machinery when its round is
approved. No code changes — a documentation and framing fix, cheap now, expensive after
a paper submission.

### S6 — n=3 seeds with Student-t CIs is fragile, and no multiplicity plan exists 🟠 Medium (future)

t(df=2)=4.30 makes 3-seed CIs enormous; the 2×2 × tasks × models grid invites multiple
comparisons with no correction plan. **Why it matters:** underpowered claims and
uncorrected multiplicity are standard rejection grounds. **Resolution (pre-register in
the bench spec at T3):** report all per-seed values (already policy); prefer 5 seeds
where the compute ceiling allows; declare a Holm–Bonferroni (or similar) plan for the
primary-metric family; treat within-CI differences as "no difference" (already policy).

### S7 — Synthea contamination is a real benchmark-validity threat 🟠 Medium (future)

Synthea and its outputs are public and plausibly in base-model pretraining corpora — a
model may "know" Synthea's templates and distributions. **Why it matters:** inflates
apparent FHIR competence; a sharp reviewer will ask. **Resolution (T3/T5 spec items):**
generate with non-default Synthea configs/modules and fresh seeds; include a
memorization probe (e.g., prompt-completion of Synthea-canonical fragments) as a
reported diagnostic; document the threat in the bench limitations.

### S8 — RQ5's scorer needs its own validation study 🟡 Medium-low (future)

The span-alignment hallucination scorer is a *measurement instrument*; instruments
require validation. **Resolution:** T3 adds a scorer-validation step — human-labeled
span sample, report scorer-vs-human agreement before the scorer may headline.

## Ethics & regulatory

No human subjects (synthetic + bibliographic metadata): no IRB trigger. PHI boundary
and not-a-medical-device statements are structurally enforced — better than most
funded projects. Abstract storage/redistribution is licence-managed per source
(PubMed abstracts excluded from any export). No issues found.

## Novelty status (honest)

The core claims (verification-first FHIR generation; executable-ground-truth medical
benchmark) remain *plausibly novel but unverified against the literature*. The corpus
that can answer this now exists but is unscreened. **Screening Q2/Q6 (FHIR×LLM,
medical benchmarks) first is the fastest path to a novelty verdict** — and should
happen before Paper 1 effort is committed.

## Research debt register

S1 coverage reporting · S2 fuzzy dedupe · S3 reliability mechanism · S5 corpus framing
(all pre-screening); S6 statistical plan, S7 contamination probes, S8 scorer validation
(all pre-T3-spec-freeze). Tracked here; resolved items get struck through in future
reviews.
