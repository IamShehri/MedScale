# Survivability Audit — "The Founder Vanished in 2028. It Is Now 2038."

- **Date:** 2026-07-10 · **Trigger:** founder directive (ecosystem immortality review)
- **Premise attacked:** only the repository survives. No tribal knowledge, no chat
  logs, no founder, no Claude. Can strangers continue MedScale?
- **Method:** every knowledge claim below was verified against the repo (grep), not
  assumed. Findings classify as: FIXED-NOW · PROPOSED-ADR-0019 · DEBT (trigger) ·
  STRUCTURAL (needs humans who don't exist yet).

## Verdict in one line

**The knowledge SPOFs are already dead — the discipline of "everything in the repo,
verified, logged" killed them.** What remains are *authority* SPOFs (account ownership,
ratification rights, privacy) — invisible to code review, fatal in the 2038 scenario,
and mostly closable by three acts: going public, organization ownership, and a
succession clause (ADR-0019).

## The 2038 test, honestly scored

A competent 2038 stranger cloning the repo finds: 18 ADRs with rationale *and rejected
alternatives*; rules R1–R7; four review genres including debt registers with triggers;
self-describing data formats (F1); 188 tests encoding contracts; append-only decision
logs replaying every scientific choice; a glossary; phase gates; a conventional
toolchain (uv/ruff/mypy/pytest, zero exotic dependencies, zero runtime deps).
**They can rebuild the *what* and the *why* completely.** What they cannot do:
merge a PR, cut a release, ratify an ADR, respond to a security report, or even *see*
the repo if it never went public. Authority, not knowledge, is where MedScale dies.

## SPOF matrix

P = probability over 10 years · I = impact if it fires · Cost = cost of fixing after it fires

| # | SPOF | Class | P | I | Cost later | Mitigation | Status |
|---|---|---|---|---|---|---|---|
| S1 | **Repo is private on a personal account** — founder vanishes pre-publication ⇒ nobody can even fork; the project literally ceases to exist | Founder+Infra | med | **fatal** | infinite (no copy exists) | Go public (already the plan); until then, publication date is a survivability deadline, not a marketing choice | PROPOSED-ADR-0019 §1 |
| S2 | **Personal-account ownership** (`IamShehri/MedScale`) — no second admin, ever | Founder+Infra | med | fatal for canonical continuity (forks fragment) | community schism, trust reset | Migrate to a GitHub organization at publication; ≥2 owners the day a trusted second human exists | PROPOSED-ADR-0019 §2 |
| S3 | **Founder is the only ratifier** — governance deadlocks by design on vacancy; no absence clause exists in roles_and_authority | Governance | med | project frozen in amber (maintainable but unevolvable) | contested forks | Succession clause: inactivity threshold → documented stewardship transfer rules → maintainer supermajority for non-constitutional changes | PROPOSED-ADR-0019 §3 |
| S4 | **Release/approval environments founder-only** (per ADR-0010 design) | Release | med | no releases ever again | same as S3 | Covered by S3's succession clause | PROPOSED-ADR-0019 §3 |
| S5 | **Security contact = founder** (SECURITY.md private reporting) | Security | med | vulnerabilities unanswered | reputation | Second responder when one exists; GitHub private-advisory as account-independent channel | PROPOSED-ADR-0019 §4 |
| S6 | **HF org + future PyPI name single-admin** | Infra | med | distribution freeze; name squatting (PyPI `medscale` unclaimed today) | rename (brand loss) | Second HF admin later; PyPI claim at v0.2 via trusted publishing (never manual); trademark awareness noted | PROPOSED-ADR-0019 §5 |
| S7 | **Single hosting provider** — GitHub account suspension/outage pre-mirrors | Infra | low | coordination loss (clones survive) | re-bootstrap | Public ⇒ Software Heritage auto-archival; add a passive mirror + Zenodo DOI (D7) at first release | PROPOSED-ADR-0019 §6 + DEBT D7 |
| S8 | **Development velocity is 100 % Claude-dependent** | Claude | med | velocity cliff, not death: stack is deliberately conventional; a competent Python dev continues from the repo alone (verified: no exotic tooling, contracts tested, process documented in roles_and_authority) | slower evolution | Keep the boring-stack rule; the repo-is-the-only-memory rule (below) | STRUCTURAL — mitigated by design |
| S9 | **Claude's memory files live outside the repo** | Knowledge | — | — | — | Verified this session: every load-bearing fact (S2-key status, quirks, workflow, screening order*) is mirrored in-repo. *One gap found and fixed today (duplicates-first ordering was tool-only). Rule made explicit in ADR-0019: the repository is the only memory | FIXED-NOW + ADR-0019 §7 |
| S10 | **AI collaboration invisible in git history** — zero co-authorship trailers; a 2038 reader (or journal) cannot see how the code was produced | Knowledge+Scientific | certain (it's already true) | scientific-transparency question at first paper; norms (JAMIA/Nature) increasingly require AI-contribution disclosure | awkward retroactive disclosure | History is append-only — never rewrite; add an in-repo AI-collaboration disclosure + trailers going forward, per founder decision | PROPOSED-ADR-0019 §8 |
| S11 | **Founder is the only scientist** (screening, tier confirmation, novelty verdicts) | Scientific | med | in-flight science pauses; **but** every past decision replays from logs, and future screening is re-doable by any qualified human via the documented protocol | duplicated screening effort | Already maximally mitigated for solo phase (S3 washout protocol, attributed logs); the real fix = second screener (H2) | STRUCTURAL |
| S12 | **No community = no successors** — deliberate H1 choice ("community after results") | Community | high short-term | combines lethally with S1–S3 only | — | The H2 community plan *is* the mitigation; until then S1–S3 fixes carry the risk | STRUCTURAL (accepted trade-off) |
| S13 | **Funding** | Funding | low | none today — the compute ceiling (Colab-class, zero paid infra) is itself SPOF-armor; grants become relevant only at H2 scale | — | Foundation/fiscal-sponsor path documented (below) | Untouched |
| S14 | **Trademark/name** — "MedScale" unregistered | Legal | low | rename under pressure | brand loss | Note only; register or foundation-transfer at H2 | DEBT (trigger: public traction) |

## Foundation-readiness (Apache / Linux F / PyTorch F / NumFOCUS comparison)

What those bodies require vs MedScale today: **governance docs** ✓ (unusually complete) ·
**IP hygiene** ✓ (Apache-2.0, single-author provenance, no CLA needed yet; DCO adoptable
later) · **transparent decision record** ✓ (ADRs exceed most incubator entrants) ·
**diverse maintainers** ✗ (one human) · **community** ✗ · **trademark clarity** ✗.
**Conclusion:** nothing *structural* blocks a foundation path; the only blockers are
humans-count and time. Best-fit umbrella when eligible: **NumFOCUS fiscal sponsorship**
(scientific-software native — home of NumPy/Jupyter-adjacent projects), with Apache-style
incubation as the heavier alternative. Recorded in ADR-0019 §9 as the H2+ path.

## Which assumptions still depend on…

- **Abdulaziz:** ratification (S3), all account ownership (S1/S2/S6), security response
  (S5), the scientific decisions only a human may make (S11), publication timing (S1).
- **Claude:** velocity only (S8) — deliberately not correctness, not knowledge, not
  process; all three live in the repo.
- **Undocumented knowledge:** after today's fix — **nothing found** (S9 verified empty).
- **One person:** everything in the first bullet, until publication + succession clause
  + a second human. That triad is the immortality condition.

## Actions from this audit

1. FIXED-NOW: duplicates-first screening order written into the execution docs (S9's
   one gap).
2. [**ADR-0019 (Proposed): Continuity & Succession**](../../adr/0019-continuity-and-succession.md)
   — §1 publication-as-survivability-deadline, §2 org ownership, §3 stewardship
   vacancy clause, §4 security succession, §5 namespace custody, §6 mirrors/archival,
   §7 repo-is-the-only-memory rule, §8 AI-collaboration disclosure, §9 foundation path.
3. Debt: S14 trademark (trigger: public traction) added alongside D1–D7.
