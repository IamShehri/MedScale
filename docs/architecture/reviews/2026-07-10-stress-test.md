# Architectural Stress Test — "What breaks first at 1000×?"

- **Date:** 2026-07-10 · **Trigger:** founder directive (pre-public decade-survival review)
- **Method:** every claim below was verified against the code (grep/read), not the docs.
  Assumptions attacked: 1,000× records (~1.35M), thousands of contributors, multiple
  institutions, unknown future models/standards/storage/languages.
- **Classification per finding:** FIX-NOW (safe under governance) · PROPOSED-ADR ·
  DEBT (registered, with trigger) · UNTOUCHED (deliberate, survives).

## Verdict in one line

The *contracts* survive the decade (content-addressed identity, append-only logs, pure
spine, protocol-based models, zero runtime deps); the *engines* behind them are
explicitly v1 and correctly seamed for replacement — the two genuinely dangerous items
were un-versioned persisted formats (fixed now) and evidence-identity/schema coupling
(Proposed ADR-0018).

## Findings, ranked by (impact × cost-to-fix-later)

### F1 — Persisted formats carry no version marker 🔴 FIX-NOW (fixed this session)
**Evidence:** zero `"format"` markers across all serialized artifacts (corpus lines,
review events, screening decisions, manifests, merge/resolution logs); only
`EvidenceObject.schema_version` exists. **Attack:** in 2031, a reader meets a 2026 log
line — which code wrote it? Answer requires git archaeology correlating timestamps to
commits. At millions of lines and N format evolutions, that is unrecoverable ambiguity
in the scientific record. **Fix (cheap, additive, ids untouched):** every serializer
now emits `"format": 1`; all readers tolerate absence (absence ≡ format 1). Committed
*logs* are never rewritten (append-only law); the corpus (a snapshot, not a log) was
rewritten once to be self-describing — `record_id`s hash identifiers only, so identity
and screening references are unaffected (verified by `medscale check`).

### F2 — `evidence_id` couples claim identity to container schema 🟠 PROPOSED-ADR-0018
**Evidence:** ADR-0009 includes `schema_version` in the identity hash. **Attack:** at
millions of Evidence Objects, the first v1→v2 schema bump re-mints *every* id,
breaking every KG edge, benchmark citation, and cross-reference simultaneously — the
ADR-0017 orphaning hazard at ecosystem scale. **Window:** zero evidence objects exist;
the fix is free today and a mass migration later. Amends an accepted ADR → cannot be
self-ratified: see [ADR-0018 (Proposed)](../../adr/0018-evidence-identity-decoupling.md).

### F3 — Storage engine: whole-file JSONL + full-log replay 🟡 DEBT (trigger: 75 MB / ~50k records)
**Evidence:** `load_corpus`/`write_corpus` are whole-file; `append_decisions` replays
the entire log per batch; all in-memory. **Attack:** at 1.35M records the corpus is
~1–2 GB (already forbidden by ADR-0016's tripwire), session-start replay takes minutes,
dedupe needs GBs of RAM. **Why NOT fixed now:** the seam is verified clean — every
corpus read in `src/` and `scripts/` goes through `store.py`; swapping the engine
(SQLite/DuckDB/Parquet) later is contained behind two functions. Abstracting a `Store`
protocol today = one implementation, zero second consumers = the empty abstraction our
own rules forbid. **Trigger:** the ADR-0016 tripwire *is* the storage-engine ADR
trigger; noted there.

### F4 — Single-writer logs: replay-validate-append TOCTOU 🟡 DEBT (trigger: second concurrent reviewer, H2)
**Attack:** two simultaneous reviewers both replay state, both append; a conflicting
screening transition poisons `screening_log` replay for everyone after. **Today:**
solo operator, `append_decisions` validates-before-write; unreachable without
concurrent writers. **Sketch for later:** per-reviewer log shards merged at replay
(append-only makes this CRDT-adjacent and easy) — recorded so the future fix is a
design retrieval, not a redesign.

### F5 — Identity hashes recomputed on every property access 🟢 DEBT (trigger: profiling at scale)
**Evidence:** `record_id`/`evidence_id` are plain properties → `canonical_json` +
SHA-256 per access; hot loops (dedupe, store, integrity) access repeatedly. Fine at
1,346; measurable at millions. Micro-optimization (manual `object.__setattr__` cache)
deferred until a profile demands it — premature now.

### F6 — CI actions pinned to tags, not SHAs 🟢 DEBT (low urgency)
Dependabot already covers `uv` + `github-actions` weekly; workflow permissions are
`contents: read`; CodeQL active; zero runtime dependencies make the supply-chain
surface unusually small. SHA-pinning is the remaining hardening step — queue with the
first release workflow (ADR-0010 pending).

### F7 — Governance mechanics at 1000 contributors 🟢 DEBT (trigger: >3 regular contributors)
Sequential ADR numbering = merge-conflict lottery; solo-operator review cadence doesn't
scale. Conventions (number reservation via PR title; area maintainers) are documented
patterns from Apache/K8s — adopt when contributors exist, not before.

## What survives the decade (attacked and held)

| Subsystem | Attack | Why it held |
|---|---|---|
| Spine primitives | Unknown languages/hardware | Pure functions over standardized algorithms (RFC 8785-adjacent canonical JSON + SHA-256); a Rust/TS port is a re-implementation with byte-compatibility tests, not a redesign |
| Identity & provenance | Distribution across institutions | Content-addressed ids merge without coordination; append-only logs are conflict-free to concatenate + replay |
| Model layer | Unknown LLMs, hundreds of adapters | `TextGenerator`/`SpanExtractor` protocols; grammar-as-request-field; registry law in constructors; models are data (`ModelRef`), not code |
| FHIR R6/R7/unknown standards | Version churn | fhirkit unbuilt (nothing to migrate); repro policy already pins validator by version+SHA per benchmark release; single-representation rule (ADR-0008) prevents dual-model rot |
| Future SDK/REST/MCP/bindings | New surfaces | Everything is frozen typed dataclasses ↔ canonical JSON — a serialization boundary already; no framework lock-in to unwind |
| Package architecture | 1000× code | One package with verified-clean seams + graduation gates (ecosystem_evolution); extraction is `git mv`, not surgery |
| Dataset lifecycle | Unknown storage | R3 per-directory licences + manifests + hashes travel with the data, engine-independent |
| Testing | Unknown maintainers | 183 deterministic offline tests; contracts (byte-stability, state machines, id stability) are tested as invariants, not implementations |
| Disaster recovery | GitHub vanishes | Any clone is the full scientific record (archives + logs + code); Zenodo DOI planned at first release closes the last gap (registered in releases/) |

## Debt register (engineering)

| # | Item | Trigger | Owner note |
|---|---|---|---|
| D1 | Storage engine swap (F3) | `data/` > 75 MB or >50k records | ADR required (0016 mandates) |
| D2 | Multi-writer log protocol (F4) | Second concurrent reviewer | Shard-per-reviewer sketch above |
| D3 | Identity-hash caching (F5) | Profile shows >5% time in hashing | Mechanical |
| D4 | CI action SHA-pinning (F6) | First release workflow | With ADR-0010 implementation |
| D5 | ADR numbering convention (F7) | >3 regular contributors | Convention doc, 1 hour |
| D6 | OpenMed doc pair merge | Next docs pass | Editorial |
| D7 | Zenodo archival | First paper/dataset release | Already in releases/ plan |

Previously registered research debt (S-series) lives in the
[scientific review](../../research/reviews/2026-07-10-scientific-integrity-round1.md).
