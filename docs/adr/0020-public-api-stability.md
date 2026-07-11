# ADR-0020 — Public API Stability Policy

- **Status:** Accepted (2026-07-10; created and ratified by founder directive — Core
  Stabilization Sprint)
- **Date:** 2026-07-10
- **Deciders:** Founder
- **Related:** [ADR-0011](0011-versioning-licensing.md) (versioning schemes, Proposed),
  [ADR-0017](0017-identifier-stability-contract.md) (identity contract),
  `medscale.workspace` (the contract's implementation), architecture tests
  (`tests/test_architecture.py`, the mechanical enforcement)

## Context

The Core Library exists and every future interface (CLI, REST, MCP, SDK, Afia,
notebooks) must consume it. A public contract without a written stability policy decays
into "whatever didn't break yet." This ADR states what is promised, to whom, for how
long.

## Decision

### 1. Stability tiers

| Tier | Contents | Promise |
|---|---|---|
| **Public-frozen** | Root exports: `Workspace`, `Corpus`, `Evidence`, `Benchmark`, `Snapshot`, `VerificationEngine`, `RecordQueryResult`, `EvidenceQueryResult`, `ResearchIndex` (via `Workspace.index()`); spine primitives `canonical_json`, `content_hash`, `set_global_seed`; modelkit protocols `TextGenerator`, `SpanExtractor`, `ModelRef`; bench types returned by the facade (`BenchmarkSpec`, `TaskItem`, `BenchmarkRunArtifact`, `EvidenceSystem`); the `EvidenceObject` data model | Names, signatures, and semantics change only under §3 |
| **Data-contract** | Identifier derivations (ADR-0017), persisted formats (`format` markers + tolerant readers), snapshot identity, storage-layout string *values* (`_layout`) | Append-only evolution; breaking change ⇒ ADR + migration, no exceptions |
| **CLI-stable** | Command names and exit-code semantics of `medscale {screen, extract, check, stats, snapshot, bench}` | Additive flags free; renames/removals follow §3 |
| **Internal** | Everything else — all subpackage internals, `_layout`, `_runtime`, module topology | May change in any release; each surface is marked `Stability: internal` in its docstring |

### 2. Versioning (binds to ADR-0011's SemVer scheme)

Pre-1.0: MINOR may change public-frozen APIs **only** with a CHANGELOG `Changed` entry
and, where mechanically possible, a deprecation alias for one MINOR cycle; PATCH never
does. Post-1.0: public-frozen changes require MAJOR. Internal tiers never gate version
numbers.

### 3. Deprecation policy

1. Announce in CHANGELOG + a runtime `DeprecationWarning` alias where feasible.
2. Keep the old name working for ≥1 MINOR release (pre-1.0) / ≥2 MINOR releases
   (post-1.0).
3. Remove only in the next allowed version per §2, with the migration one-liner in the
   CHANGELOG.
4. Data-contract items are exempt from deprecation-by-warning: they get an ADR and a
   migration tool or they do not change.

### 4. Compatibility rules

- The abstraction promise is contractual: storage engine, implementation language, and
  execution locality are replaceable **without user-code changes**.
- Public objects never expose filesystem paths, file formats, or module topology.
- Determinism is API: same inputs + same knowledge state ⇒ byte-identical outputs; a
  change in result bytes for unchanged inputs is a breaking change even if signatures
  are untouched (scorer/metric changes are benchmark-MAJOR per release law).

### 5. Namespaces

Public = the package root (`medscale.*` top-level exports) plus explicitly marked
protocol/data-model modules. Internal = every subpackage path; importing one is
choosing instability, and docstring markers say so. Enforcement is mechanical: the
architecture tests fail the build on inverted imports, transport leakage, facade
consumption inside the engine, and layout literals outside `_layout`.

## Consequences

**Positive:** downstream consumers (starting with Afia) can pin against a written
promise; refactors inside the engine are provably safe (240 tests, 6 of them
architecture rules). **Negative:** the frozen list is a real cost — every name on it
must be right; additions should be reluctant (a name is easier to add than remove).

## Alternatives considered

- **Everything public (docs-by-usage).** Rejected: guarantees eternal breakage debates.
- **SemVer alone without tiers.** Rejected: version numbers say *when* things may
  change, not *what* — the tier table is the missing half.
