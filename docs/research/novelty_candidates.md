# Novelty Candidate Registry

- **Status:** Living registry (Chief Scientist directive, 2026-07-10). Candidates are
  *analyzed here, implemented nowhere* until validated and approved. Each entry follows
  the 10-step protocol: idea · novelty case · literature comparison · OSS comparison ·
  impact · risks · validation experiments · benchmark methodology · venues · ADR-needed.
- **Honesty rule:** novelty claims below are **hypotheses**. Formal literature
  positioning requires the screened corpus (R1 — no related-work claims from memory in
  a paper); software-landscape comparisons are grey-tier facts, verifiable by anyone.

## Registered candidates

| # | Candidate | Status | Planned paper |
|---|---|---|---|
| N1 | Reproducible-by-construction systematic review infrastructure ("PRISMA-as-code") | Analyzed below | litdb methods paper (unplanned — would be Paper 0) |
| N2 | Grammar decouples form from content in clinical generation | Long-registered (RQ1) | Paper 1 |
| N3 | Validator as infinite exact teacher; executable-ground-truth benchmark | Long-registered (RQ3; Bench) | Papers 2, 4 |

---

## N1 — PRISMA-as-code: reproducible-by-construction systematic review infrastructure

**1. The idea.** MedScale's litdb already constitutes something the systematic-review
world does not have: a review pipeline in which **every PRISMA number is a
deterministic function of committed, append-only artifacts**. Frozen queries (by git
SHA) → verbatim hashed archives → pure parsers → content-addressed records →
conflict-safe logged dedupe with merge lineage → attributed append-only decision events
(reviewer, timestamp, software version, git SHA, machine-readable exclusion taxonomy) →
replayed PRISMA counts — with referential integrity enforced by a CI gate
(`medscale check`). The flow diagram of a review is not *reported*; it is *recomputed*.

**2. Why it appears novel.** Existing tools manage screening; none (to current
knowledge — see honesty rule) make the *entire* review byte-replayable from a git clone
with cryptographic provenance from API response to inclusion decision.

**3. Literature comparison (to be formalized from the corpus).** PRISMA 2020 is a
*reporting* standard — it standardizes what you claim, not whether claims are
recomputable. Reproducibility literature in evidence synthesis focuses on data/code
sharing after the fact. The eval-methodology slice of the corpus (Q4) is the
verification path; screening it will confirm or kill the novelty claim.

**4. OSS/product comparison (verifiable today).** Covidence, Rayyan, DistillerSR:
proprietary SaaS, decisions in opaque databases, exports are snapshots not replayable
logs. ASReview (open source): strong on ML-assisted *prioritization*, but state lives
in project files; no content-addressed identity, no merge lineage, no CI-enforced
referential integrity, no git-native audit trail. SysRev, Abstrackr: similar gaps.
None treat "PRISMA counts recompute identically on any machine" as a design invariant.

**5. Potential scientific impact.** Systematic reviews are the top of the evidence
hierarchy yet are themselves largely unauditable processes. Making the review process
as reproducible as we demand analyses be is a methods contribution independent of
everything else MedScale does — and it is *already built*, needing only its
demonstration (the screened corpus) and its write-up.

**6. Risks.** (a) Reviewers may classify it as "engineering rigor, not science" —
mitigation: frame as methods/infrastructure with a completed demonstration review;
(b) single-screener demonstration weakens the case — mitigation: the washout self-audit
protocol (S3) + invite a second screener for a sample; (c) a competitor may exist
outside my knowledge — mitigation: the Q4/Q6 screening pass is precisely the check;
(d) small demonstration corpus (scoping round) — mitigation: honest scoping framing
already in place, or run the definitive round first.

**7. Validation experiments.** (i) *Replay test*: recompute all PRISMA counts from logs
on a clean machine; assert byte-identity (already CI-enforced — formalize as a
reported experiment). (ii) *Independent audit*: an external researcher reconstructs the
full PRISMA flow diagram from the repository alone, no author contact; measure
success/time. (iii) *Tamper detection*: mutate one historical decision; show
`medscale check`/hash chain flags it. (iv) *Cross-tool case study*: run the same corpus
through Rayyan/ASReview and enumerate which audit questions each tool can answer.

**8. Benchmark methodology.** Not a model benchmark — an *auditability checklist*
(can the tool answer: who decided X, when, under what software, with what reason, and
do the counts recompute?). Publishing that checklist is itself a contribution
(reviewer-facing, deterministic, no LLM judging anything).

**9. Venues.** JAMIA or JMIR (methods); AMIA Annual Symposium (system demonstration);
Cochrane Colloquium (methods community); *Research Synthesis Methods*. NeurIPS D&B only
if bundled with the corpus as a dataset artifact.

**10. ADR needed?** No — nothing architectural changes. If pursued, it adds a paper to
the publication roadmap (founder decision, not an ADR).

**Recommended next validation step:** complete the Q2/Q6 (+Q4) screening — it serves
the novelty verdict for N1, N2, and N3 simultaneously.
