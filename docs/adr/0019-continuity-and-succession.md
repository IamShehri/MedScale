# ADR-0019 — Continuity & Succession (Making MedScale Founder-Survivable)

- **Status:** Proposed (awaiting founder approval — this creates governance that
  activates precisely when the founder cannot approve things; it is the one ADR that
  must exist *before* it is needed)
- **Date:** 2026-07-10
- **Deciders:** Founder
- **Related:** [survivability audit](../architecture/reviews/2026-07-10-survivability-audit.md)
  (SPOF matrix S1–S14), [roles & authority](../governance/roles_and_authority.md),
  ADR-0010 (release approvals)

## Context

The survivability audit's verdict: knowledge SPOFs are dead (the repo is verified
self-contained), but **authority SPOFs are fatal** — a vanished founder today means a
private repo nobody can fork, ADRs nobody can ratify, releases nobody can approve, and
security reports nobody answers. Immortality is three acts: publication, shared
ownership, and a vacancy rule. None may be improvised during a crisis.

## Decision (proposed)

1. **Publication is a survivability deadline.** Until the repository is public, every
   other mitigation is moot (S1). Target: publication no later than the litdb-v1 /
   first-paper milestone; earlier if founder-availability risk changes. Once public,
   Software Heritage archival happens automatically; a Zenodo DOI (debt D7) follows at
   first release.
2. **Organization ownership.** At publication, the canonical repo moves to a GitHub
   organization (`MedScale` or successor name). The founder is sole owner until a
   trusted second human exists, at which point **two owners minimum** becomes the
   standing rule. HF (`MedScaleAI`) mirrors the same rule (S2, S6).
3. **Stewardship vacancy clause.** If the founder is unreachable for **6 consecutive
   months** (no commits, issues, or maintainer contact): (a) active maintainers may
   ratify *non-constitutional* ADRs by documented supermajority with a 14-day lazy-
   consensus window; (b) *constitutional* changes (vision, PHI boundary, dependency
   direction, licence) remain frozen for 24 months, after which the same supermajority
   may amend with a published rationale; (c) release approvals transfer to maintainers
   under the same supermajority. If no maintainers exist, any fork that preserves this
   governance verbatim and the full history may declare stewardship publicly; earliest
   such fork with continuous activity is the legitimate successor (S3, S4).
4. **Security succession.** SECURITY.md gains GitHub private-advisory reporting (an
   account-independent channel) alongside the direct contact; a second responder is
   named the day one exists (S5).
5. **Namespace custody.** The PyPI name `medscale` is claimed only via the governed
   release path (v0.2, trusted publishing — never manually); HF org admin duplication
   per §2; trademark registration is deferred to public traction (debt S14) (S6).
6. **Mirrors.** At publication: one passive read-only mirror (Codeberg or GitLab)
   updated by CI, documented in the README. Mirrors are never canonical (S7).
7. **The repository is the only memory.** Standing rule, now explicit: any fact
   required to continue MedScale — process, quirks, status, decisions — must live in
   the repository. Assistant memory files, chat logs, and private notes are
   conveniences, never sources of truth. (Verified true as of this ADR; S9.)
8. **AI-collaboration disclosure.** An honest, permanent statement in the repository
   (README or CONTRIBUTING section): MedScale's engineering has been substantially
   produced through founder-directed AI (Claude) sessions under the governance in
   `roles_and_authority.md`, with every change gated by executed tests and founder-
   ratified ADRs. Commit trailers (`Co-Authored-By`) are adopted going forward;
   history is never rewritten (S10). Papers follow venue AI-disclosure policies
   (already in papers.md).
9. **Foundation path (H2+).** When ≥3 sustained maintainers exist, evaluate NumFOCUS
   fiscal sponsorship first (scientific-software native), Apache incubation second.
   Recorded now so successors know the intended trajectory (foundation-readiness
   analysis in the audit).

## Consequences

**Positive:** the founder becomes replaceable in exactly the ways that keep the project
alive, while remaining the decision-maker in every scenario where they are present; a
2038 stranger holds not just the knowledge but the *authority procedure*.
**Negative:** the vacancy clause is untested governance (all such clauses are, until
fired); publication deadline adds pressure — intended.

## Alternatives considered

- **Do nothing until community exists.** Rejected: S1–S3 are fatal *before* community
  can form; this is the bootstrap paradox the clause resolves.
- **Immediate foundation transfer.** Rejected: no foundation accepts a one-human
  project; premature and heavier than needed.
- **Rewrite history to add AI trailers retroactively.** Rejected outright: append-only
  history is constitutional; disclosure is additive.

## Compliance

On acceptance: §7 and §8's disclosure text land in-repo immediately; §4's advisory
channel enabled at publication; §1–§2, §6 execute at publication; §3 activates only on
vacancy. Review this ADR annually (it is the one document whose staleness is dangerous).
