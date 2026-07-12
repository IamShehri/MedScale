# ADR-0022 — Screening Decision Semantics (Two-Stage Review)

- **Status:** Accepted (2026-07-12 — ratified by the founder's Mission Zero approval;
  this ADR was the mission's GO gate: semantics fixed *before* the first real
  screening decision is logged, because every event written afterwards is permanent
  and must mean something exact).
- **Date:** 2026-07-12
- **Deciders:** Founder
- **Related:** [ADR-0017](0017-identifier-stability-contract.md) (the precedent:
  ordering invariants before permanent records), [ADR-0009](0009-evidence-model.md),
  `docs/guides/first_systematic_review.md` (operator-facing statement of the same),
  PRISMA 2020. *Numbering note:* the data-publication strategy ADR sketched in the
  post-review planning session will take 0023 when written; this ADR takes the next
  free number because Mission Zero needs it first.

## Context

PRISMA 2020 defines two sequential assessment stages: **screening** (title/abstract)
and **eligibility** (full text). MedScale's review state machine currently records one
decision per record with no stage dimension. 1,346 permanent decisions are about to be
written; their meaning must be fixed now, not reinterpreted later.

## Decision

1. **`INCLUDE` means "passes title/abstract screening"** — the record proceeds to the
   (future) full-text eligibility stage. It is *not* final inclusion in any synthesis.
2. **`EXCLUDE` is stage-terminal** with a mandatory taxonomy reason; these become the
   PRISMA screening-stage exclusion breakdown.
3. **`UNCERTAIN` is an intra-stage revisit marker** (stays in the queue), not a
   scientific state.
4. **`DUPLICATE_CONFIRMED` belongs to the pre-screening dedupe bucket** in PRISMA
   accounting, regardless of when it is recorded.
5. **Eligibility is a distinct, future decision stage** with its own log semantics,
   full-text acquisition (licensing decided at design time), and population of the
   reserved `license_spdx` field. It is *designed by this ADR's boundary, not built* —
   implementation follows Mission Zero evidence, per the no-speculative-engineering
   rule.
6. **No code changes now.** Events written under these semantics stay valid forever:
   when eligibility lands, existing `INCLUDE` events already mean exactly "passed
   title/abstract" — no migration, no reinterpretation.
7. Any evidence extracted before the eligibility stage exists is **abstract-anchored
   by definition** and must not be presented as synthesis-grade; the extraction
   tutorial says so and extraction campaigns at scale wait for eligibility.

## Consequences

**Positive:** the audit trail's meaning is written down before it exists; PRISMA
mapping is exact; the eligibility stage can land later without touching a single
recorded event. **Negative:** "included" in status output means less than a casual
reader might assume — the docs carry that burden deliberately.

## Alternatives considered

- **Implement the two-stage state machine now.** Rejected: speculative — its design
  should be shaped by real screening friction (Mission Zero is the evidence collector).
- **Let INCLUDE mean final inclusion.** Rejected: guarantees mass reinterpretation of
  permanent events the day full-text assessment arrives.
