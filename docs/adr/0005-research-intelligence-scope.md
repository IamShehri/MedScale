# ADR-0005 — Research Intelligence as a Second Pillar (Mission Scope Amendment)

- **Status:** Proposed (awaiting operator approval — this is a scope decision the
  architect cannot self-ratify; Research Vision §9 requires it)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [Research Vision](../vision/MEDSCALE_RESEARCH_VISION.md) (scope authority),
  [ecosystem analysis §5](../architecture/ecosystem_analysis.md#5-market-references-not-dependencies),
  [reference architecture](../architecture/medscale_reference_architecture.md), Rules R1/R4/R6

## Context

A principal-architect mission brief describes MedScale as *"Open Research Intelligence
Infrastructure for Medicine"* — literature discovery, evidence analysis, citation
engines, knowledge graphs, research agents. The frozen Research Vision defines MedScale
as *verifiable clinical AI* (FHIR-native, grammar-constrained, validator-grounded,
deterministically benchmarked). These are not the same mission, and under the governance
this repository lives by, the gap cannot be papered over: scope changes require an ADR.

Three facts bear on the decision:

1. **The bridge already exists.** T1 (litdb) already commits MedScale to literature
   ingestion, PRISMA screening, and citation-verified provenance (R1) — as *internal*
   research tooling. The new mission generalizes exactly that machinery into a platform
   capability.
2. **The market gap is real and on-thesis.** OpenEvidence (reported >40% of US
   physicians daily, $3.5B valuation) and Medwise prove enormous demand for
   evidence-grounded medical answers — all served by closed products whose citations
   cannot be audited. "Verifiable evidence infrastructure" is MedScale's thesis applied
   to literature.
3. **The risk is the known killer.** Knowledge graphs and research agents were part of
   the archived, superseded draft that the program deliberately walked away from.
   Unbounded, this amendment recreates the scope sprawl the Vision exists to prevent.

## Decision (proposed)

1. **Ratify "research intelligence" as MedScale's second pillar**, subordinate to the
   same spine: verification-first, deterministic provenance, no unauditable claims. The
   mission sentence becomes: *MedScale is open research infrastructure for verifiable
   medical AI — verifiable clinical generation (pillar 1) and verifiable research
   intelligence (pillar 2).*
2. **T1 builds litdb as a reusable capability** (`medscale.litdb`: schema, ingestion,
   PRISMA state machine, citation verification) rather than throwaway internal tooling.
   This is the only near-term change of substance, and it changes *how* T1 is built,
   not *whether* or *when*.
3. **Knowledge graph and research agents remain Horizon-2+ and gated**: KG work opens
   only after litdb is populated (T1) and deterministic extraction is proven (T3/T7);
   agent work only under validator-gating (RQ3/RQ4). Neither enters Horizon 1.
4. **Horizon-1 phase order, gates, and the compute ceiling are unchanged.**

## Consequences

**Positive:** the mission expansion is captured without breaking scope discipline; T1
gains a second consumer for the same work; MedScale's differentiation against closed
evidence products becomes an explicit, documented axis.

**Negative / costs:** pillar 2 widens the eventual maintenance surface; the operator
must hold the H2 gates against the temptation to chase the OpenEvidence market early;
Research Vision §2/§6 requires a small amendment (one paragraph naming pillar 2 and its
gates) upon acceptance.

## Alternatives considered

- **Reject the expansion (Vision as-is).** Safest, but forfeits a real, on-thesis
  opportunity and leaves T1 built as throwaway tooling — a waste the program would
  regret at H2.
- **Adopt the full brief now (KG + agents in scope).** Rejected: recreates the
  archived draft's sprawl; violates the horizon-gating that keeps a solo program alive.

## Compliance

On acceptance: amend Research Vision §2/§6 (one paragraph), update the Blueprint's §5–§6
cross-references, and reflect pillar 2 in ROADMAP.md. Until accepted, no litdb API design
work beyond what T1 already required.
