# CTO Review #1 — "Would we build it the same way today?"

- **Date:** 2026-07-10 · **Trigger:** round-1 corpus milestone
- **Stance:** current implementation ignored; only the founding question asked, per
  [roles & authority](../../governance/roles_and_authority.md)

## The question

If MedScale were founded today, with everything learned since T0, would we build it
the same way?

## Answer: substantially yes — with three honest deviations and one warning

### What we would build identically (the load-bearing choices)

- **Verification spine as cross-cutting identity** — every week of work has confirmed
  this framing; it is the differentiator, not a tax.
- **Single dependency-free Python package** — zero dependency friction has made every
  session productive; the graduation-gated ecosystem plan is the right growth story.
- **Evidence before AI** — the corpus existing before any model code has already paid
  off (the novelty question is now answerable from our own data).
- **Model-agnostic contracts before backends** — ADR-0015's interfaces cost days and
  removed the single-model-shape risk permanently.
- **ADR governance + quality gate** — 16 ADRs and a green gate are why this review can
  be short.

### What we would do differently from day one

1. **Decide archive storage before the first byte** (now ADR-0016). We learned this by
   committing 18 MB first. A day-one founder writes the storage ADR *with* the
   archival policy.
2. **Two corpora named from the start** (Scientific Review S5): a methods/related-work
   corpus and a clinical-evidence corpus are different scientific objects that happen
   to share machinery. Founding docs would name both; we conflated them under "litdb."
3. **A leaner constitution set.** Vision + Blueprint + directives-as-docs accumulate
   overlap; founded today, one constitution + one narrative would carry the same
   content with less drift surface. (Editorial consolidation candidate — not urgent,
   worth one pass before external contributors arrive.)

### One environment warning (not architecture)

Development on Windows + OneDrive has produced real friction (CRLF traps, SSL trust
store, sync latency on `data/`). The architecture absorbed it (LF pinning, truststore
runs), but a founded-today project would develop in WSL2 or a dev container from day
one. Recommendation, not a mandate: worth adopting before ingestion volumes grow.

## Redesigns recommended

**None.** The founding question was asked in earnest; the answer is that the mission
still shapes the architecture rather than the reverse. Re-ask at the next major
milestone — the day this review gets long is the day it earns its place in the
constitution.
