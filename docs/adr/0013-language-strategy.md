# ADR-0013 — Language Strategy: Python-First, Role-Gated Rust/Go

- **Status:** Proposed (awaiting operator approval — records a founder-directed
  direction with the architect's constraints; not self-ratified)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [ADR-0004](0004-t0-foundation-scope.md) (single-package discipline),
  [ADR-0012](0012-layered-architecture-model.md) (capability layers)

## Context

The founder's directive designates MedScale a multi-language infrastructure project:
Python as the research language, Rust for trust infrastructure (verification,
provenance, hashing, deterministic processing), Go for platform services (APIs,
orchestration, cloud-native) — with the rule that neither Rust nor Go is introduced
because it is fashionable, only when architecture requires it.

The architect's counterweight, stated plainly: **a solo-founder program that maintains
three toolchains maintains none of them well.** Today MedScale is one dependency-free
Python package with a strict gate and 68 deterministic tests; every core operation
(hashing, canonical JSON, state machines) is I/O-free stdlib code whose performance is
nowhere near a bottleneck. Premature Rust would trade real, working verification code
for an FFI boundary, a second CI matrix, and a contributor-pool split — costs paid
immediately, benefits speculative.

## Decision (proposed)

1. **Python is the primary language** for research, evaluation, data processing, and —
   at current scale — the spine itself. MedScale remains a single Python package
   (ADR-0004) until a trigger below fires.
2. **Rust is the designated language for trust-infrastructure hardening**, admissible
   only when a named trigger exists, via the pattern *Python prototype → Rust hardened
   implementation → Python bindings (same public API, same test suite passing against
   both)*. Triggers (any one, evidenced):
   - a measured performance bottleneck in spine operations (validation, hashing,
     canonical serialization) that materially limits benchmark or ingestion scale;
   - an external consumer requiring a non-Python embedding of the verification core;
   - a security-sensitive component whose threat model justifies memory-safe
     compiled code.
3. **Go is the designated language for platform services**, admissible only when
   MedScale actually operates services (H3 at the earliest — today MedScale ships
   artifacts, not services; [ci_cd.md](../releases/ci_cd.md) non-goals apply).
4. **Entry protocol for any second language:** a dedicated ADR naming the trigger
   evidence, the first consumer, the CI cost, and the maintenance plan — approved
   before the first line lands. The burden of proof is on the new language.
5. **Standing guard:** no rewrite of working, tested Python for its own sake; the
   spine's *contracts* (byte-stability, deterministic tests) are the permanent asset
   and must survive any future language port unchanged.

## Consequences

**Positive:** the long-term direction is recorded (contributors know Rust/Go are
sanctioned futures, not scope drift) while the present stays simple, green, and
maintainable by one person; language adoption becomes an evidenced decision, not a
temptation.

**Negative / costs:** if a trigger fires suddenly (e.g. benchmark scale-up), the port
happens under time pressure rather than leisurely — accepted; the prototype-first
pattern and frozen contracts keep that port mechanical.

## Alternatives considered

- **Adopt Rust for the spine now.** Rejected: no measured bottleneck, no external
  consumer, one maintainer; would slow T1–T3 for zero present benefit.
- **Python-only forever.** Rejected: forecloses legitimate futures (a Rust
  verification core consumed by hospitals' non-Python stacks is a plausible 2030
  asset); the role-gated policy keeps the door open without opening the floor.
- **Polyglot from the start (services in Go now).** Rejected: MedScale operates no
  services; building them would violate the artifact-not-service identity.

## Compliance

This ADR governs language additions repo-wide. Any PR introducing a non-Python
toolchain without its entry ADR fails review. The glossary gains "trust infrastructure"
and the roadmap phase table cross-references this policy.
