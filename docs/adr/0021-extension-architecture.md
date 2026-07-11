# ADR-0021 — Extension & Plugin Architecture (Design Only)

- **Status:** Proposed (design prepared per the Core Stabilization Sprint; **no
  implementation** until a first external extension actually exists)
- **Date:** 2026-07-10
- **Deciders:** Founder
- **Related:** [ADR-0015](0015-model-agnostic-platform.md) (the protocols that are the
  plugin points), [ADR-0020](0020-public-api-stability.md) (what extensions may rely on)

## Context

MedScale already has its extension seams — they are protocols, not registries:
`EvidenceSystem` (benchmark systems), `TextGenerator` / `SpanExtractor` (model
backends), `SourceAdapter` (literature sources). Today every implementation lives
in-repo. The open question is only *discovery*: how a third-party package contributes
an implementation without MedScale importing it by name.

## Decision (proposed)

1. **Protocols remain the only plugin contract.** An extension implements a frozen
   protocol (ADR-0020 tier: public-frozen) — nothing else is promised to it.
2. **Discovery via Python entry points** when the time comes: extensions declare
   `[project.entry-points."medscale.systems"]` (and `.backends`, `.sources`) in their
   own packaging; MedScale enumerates lazily and *validates before trusting* — a
   discovered system still passes the same licence/tier/verification gates as an
   in-repo one. No import-time side effects; enumeration is explicit
   (`medscale bench run --system <entry-point-name>`), never automatic execution.
3. **Trust model:** discovery is not endorsement. Benchmark artifacts record the
   extension's package name + version + `ModelRef`; results from unpinned or
   unverifiable extensions are labeled as such.
4. **Trigger to implement:** the first genuine third-party extension (or Afia's first
   out-of-repo system). Until then this ADR is the design shelf — implementing a
   registry with zero external plugins would be the empty abstraction our rules forbid.

## Consequences

**Positive:** the plugin story is decided before anyone asks, without paying for it
early; extension authors already know their contract today (the protocols).
**Negative:** entry-point discovery adds a supply-chain surface when it lands —
mitigations (pinning, verification-before-trust, no auto-execution) are stated now so
they are requirements then, not afterthoughts.

## Alternatives considered

- **Custom plugin registry file.** Rejected: reinvents packaging metadata.
- **Auto-discovery with import side effects** (pytest-style). Rejected for a scientific
  engine: implicit execution of third-party code contradicts the no-hidden-state rule.
- **Implement now.** Rejected: zero external consumers.
