# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Python workspace (T0):** `medscale` package (src-layout), `pyproject.toml`
  (uv/hatchling), reproducibility primitives (`canonical_json`, `content_hash`,
  `set_global_seed`), and a deterministic test suite.
- **Quality gate:** Ruff (lint + format), Mypy (strict), Pytest + coverage; GitHub
  Actions CI on Python 3.11 and 3.12; pre-commit hooks; CodeQL; Dependabot.
- **Community & governance docs:** `README`, `LICENSE` (Apache-2.0), `CONTRIBUTING`,
  `CODE_OF_CONDUCT`, `SECURITY`, `CITATION.cff`, `ROADMAP`, this changelog.
- **Governance:** canonical program rules `docs/governance/rules.md` (R1–R7); ADR
  template (`0000`); `0004-t0-foundation-scope` (single-package decision); documentation
  index, research index, glossary, and developer guide.
- **Repository hygiene:** `.gitattributes` (LF normalization), `.editorconfig`, expanded
  `.gitignore`; issue/PR templates.

### Changed

- ADR-0003 marked **Accepted** with a post-consolidation note.

### Added (architecture — hybrid layering, model registry, deep OpenMed study — 2026-07-10)

- **ADR-0012 Accepted (hybrid architecture)**: non-negotiable Verification &
  Reproducibility **Spine** (cross-cutting) + **seven capability layers** (Knowledge,
  Evidence, AI, Interoperability, Research, Developer, Application). Verification is never
  a peer layer — it is MedScale's defining identity. Operator-refined from the original
  proposal (layered model retained; Knowledge/Evidence kept as distinct layers; ADR-0005
  pillars retained as the cross-layer mission grouping).
- **`docs/models/`**: canonical **model registry** (two axes — licence tier × role;
  ecosystem position map; verified entries: BioMistral Apache-2.0, MedGemma HAI-DEF,
  Bio_ClinicalBERT MIT, PubMedBERT MIT, OpenMed Apache-2.0; MIMIC-III provenance noted)
  and the **model card schema** (`schemas/model_card_schema.md`, machine-checkable, for
  future card-lint CI). `medscale.registry` is *designed* and deferred to Horizon 2 — no
  package created (ADR-0012). Registry moved out of `ai_model_strategy.md` (dedupe).
- **Deep OpenMed study** (`openmed_capability_analysis.md` expanded): capability map +
  architecture lessons + reusable principles + integration opportunities + things to
  avoid, grounded in OpenMed's verified developer surface. Principles absorbed
  (local-first, no runtime phone-home, task-first discoverability, composition over
  pipelines); product not copied.

### Added (integrity guard — 2026-07-10)

- **`medscale.litdb.integrity`** + **`medscale check`**: referential-integrity guard for
  the corpus↔log coupling. Proactively surfaced a latent hazard — fuzzy dedupe mints new
  `record_id`s and removes merged sources (40 merges removed 80 source ids in the current
  corpus), so a decision keyed to a since-merged id would silently orphan. The check
  verifies every log reference resolves to a live record, merged records are present, and
  merged-away sources are absent; exits non-zero for CI gating. Verified CLEAN against the
  real corpus (1,346 records, 40 merges, 0 issues). 9 new tests (171 total).
- **Proposed ADR-0017** (identifier stability contract + pipeline ordering invariant):
  content-addressed ids are a frozen versioned contract; dedupe must precede any decision;
  `medscale check` is the mechanical enforcement. Surfaced by the architect, not requested.

### Added (human screening workflow — 2026-07-10)

- **`medscale.litdb.review`**: the human decision layer — controlled `ReviewDecision`
  states (PENDING/INCLUDE/EXCLUDE/UNCERTAIN/DUPLICATE_CONFIRMED, never free-form),
  machine-readable `ExclusionReason` taxonomy, and `ReviewEvent` audit records carrying
  record_id, previous/new decision, previous/new PRISMA stage, reviewer, timestamp,
  reason, notes, software version, and git SHA. Append-only `review_log.jsonl`;
  corrections are new events (history never edited); PRISMA counts and the resume queue
  are replayed deterministically from the log. PRISMA stage is a pure function of the
  decision — the accepted `ScreeningStage` machine is untouched.
- **`medscale` CLI** (`[project.scripts]`): `medscale screen {status|next|resume}` —
  operator-first, pure-function core (format/decide/build-event) with a thin
  interactive shell; `--reviewer`, `--limit` for session control. Verified against the
  real corpus (1,346 pending).
- 22 new tests (162 total): state transitions, invalid decisions, append-only, exclusion
  validation, resume, PRISMA calculations, CLI dispatch + interactive include path.

### Added (screening readiness — 2026-07-10)

- **`litdb.dedupe`** (S2): conflict-safe fuzzy dedupe — applied to the real corpus:
  1,386 → **1,346 records** (40 preprint/published twins merged with full lineage in
  merge_log.jsonl; 16 uncertain groups for human confirmation). **`litdb.coverage`**
  (S1): per-query/source coverage ratios (round-1 lowest: Q8/OpenAlex 0.10% — round 1
  formally classified a *scoping* round). **`append_decisions`** (all-or-nothing batch)
  + **`litdb.workqueue`**; all 1,346 records advanced to DEDUPED in the screening log.
- Search strategy §2b: scoping classification + single-screener limitation + washout
  re-screen protocol (S3). data/litdb README: methods-vs-clinical two-corpora framing
  (S5). Research-debt register: S1/S2/S3/S5 struck through with mechanisms.
- 13 new tests (138 total).

### Added (scientific-integrity & CTO review constitution — 2026-07-10)

- **Constitution amendments** (roles_and_authority.md): Scientific Integrity Review
  (Chief Scientist role — Nature/NEJM/NIH-reviewer standard after every major
  milestone; rigor outranks speed, trustworthy outranks impressive); CTO Review
  ("would we build it the same way today?" — redesigns recommended without fear, as
  Proposed ADRs); Duty to Challenge (the architect may tell the founder they are
  wrong; the founder remains final decision-maker).
- **Scientific Integrity Review #1**: eight findings — headline: round-1 is a *scoping*
  search (relevance-biased caps; 0.66% coverage on Q2), version-duplicate dedupe gap,
  single-screener limitation, and the corpus-purpose mismatch (methods corpus ≠
  clinical-evidence corpus — pillar-2 framing fix). Research-debt register opened.
- **CTO Review #1**: no redesigns; three founded-today deviations recorded (storage
  ADR first, two corpora named from day one, leaner constitution set) + WSL2/dev-
  container recommendation.

### Added (governance addendum + architecture review — 2026-07-10)

- **`docs/governance/roles_and_authority.md`** (binding): founder owns roadmap/scope/
  epic approval; architect executes approved scope, challenges weak ideas, and
  recommends via explicit options — approval never assumed. Session-report format and
  continuous-architecture-review cadence institutionalized.
- **Post-round-1 architecture review** (`docs/architecture/reviews/`): pipeline
  survived first real data intact; no redesigns; one urgent decision surfaced.
- **Proposed ADR-0016** (raw-archive storage): git history is append-only — storage
  policy must be decided before further ingestion. Recommended: in-repo, field-trimmed,
  capped, with a ~75 MB tripwire. **Blocks further ingestion rounds until decided.**

### Added (T1 round-1 corpus — 2026-07-10)

- **`medscale.litdb.store`**: byte-stable corpus persistence (JSONL, deduplicated by
  record_id on write, sorted, LF; load re-validates every record).
- **`scripts/ingest_round.py`**: reproducible round runner (frozen query set at git
  SHA; PubMed esearch→batched esummary; S2 backoff + abort-after-2-429s rule; manifest
  + corpus + PRISMA report). Scripts added to mypy strict scope.
- **Ingestion round 1 executed and committed**: 1,462 identified → 1,450 parsed (12
  skipped, reasons recorded) → **1,386 unique literature records** (767 peer-reviewed,
  619 preprint; arXiv 480 / OpenAlex 454 / PubMed 452). Semantic Scholar rate-limited;
  all 10 failures recorded; re-run pending API key. 5 new tests (125 total).

### Added (T1 parsers + ecosystem long view — 2026-07-10)

- **`medscale.litdb.parsers`**: deterministic parsers for all four sources — OpenAlex
  (incl. abstract reconstruction from inverted index, DOI/PMID URL normalization),
  Semantic Scholar (externalIds, arXiv version collapsing for dedupe), PubMed
  (esummary records + esearch id extraction), arXiv (Atom XML). Per-record provenance
  anchors to the SHA-256 of the archived payload (R1); unparseable items are skipped
  with recorded reasons, never silently. Evidence tiers are deterministic proposals;
  screening remains the decision of record. Tests include end-to-end parses of the
  real committed pilot archives. 10 new tests (120 total).
- **`docs/architecture/ecosystem_evolution.md`**: the founder's Linux-style ecosystem
  vision recorded with graduation gates (external consumers, stable API, real cadence
  need, maintainer capacity, dedicated ADR) — one package now, extraction later;
  interface roadmap (protocols added with first consumers, never ahead) and registry
  schema evolution (measurement fields arrive when T3/T4 manifests can fill them).

### Added (model-agnostic AI platform — 2026-07-10)

- **`medscale.modelkit`** (ADR-0015, operator-directed): the AI-Infrastructure layer's
  contract surface, pure and dependency-free — `TextGenerator`/`SpanExtractor`
  protocols with `ModelRef` identity (grammar is a request field; backends that cannot
  enforce it must raise); the machine-readable licence-first registry (Tier-2/encoder
  base candidacy is a constructor error); content-addressed LoRA/QLoRA recipe schemas
  (no training execution — T5 gate stands); deterministic experiment manifests with
  runner portability (Colab/Kaggle/RunPod/Lambda/local/cluster detection); honest
  metric reporting (mean ± 95% CI, Student-t, single implementation). 42 new offline
  tests (110 total). Backends, benchmark runners, and training remain gated at
  T4/T3/T5; model selection stays benchmark-manifest-driven (reserved ADR-0002).

### Added (model research program groundwork — 2026-07-10)

- **`docs/models/llm_landscape.md`**: open-LLM landscape + licence evaluation, all
  licences verified from primary sources 2026-07-10 — Qwen3 (Apache-2.0),
  Mistral-7B-v0.3 (Apache-2.0, with per-model MRL caution), DeepSeek-R1 (MIT,
  distillation permitted; distills inherit base licences) = Tier 1; Llama 3.1
  (community licence: passthrough, branding, 700M-MAU) and Meditron-7B (Llama-2
  inheritance) = Tier 2. T4 shortlist rule recorded; capability ranking deliberately
  deferred to the empirical 2×2. Registry entries extended accordingly.
- **`docs/research/experiment_framework.md`**: the reproducible experiment framework —
  mandatory experiment manifest (config, dataset hash, model revision, code SHA, seeds,
  metrics, environment, reproduction), runner policy (Colab/local/cloud admissible;
  replay-exact scoring over saved outputs), pre-registration discipline, storage layout.
  "Never train without reproducibility," operationalized.
- **Proposed ADR-0013** (language strategy: Python-first; Rust/Go role-gated by
  evidenced triggers + entry ADRs) and **Proposed ADR-0014** (`medscale.core` spine
  namespace — recommended now, while the rename is free). Not self-ratified.
- ROADMAP: founder-phase ↔ T-phase mapping table (one plan, two vocabularies);
  T1-gate text refreshed; stale "0012 Proposed" index entry corrected to Accepted.

### Added (release infrastructure design — 2026-07-10)

- **`docs/releases/`** (12 documents): complete publication & artifact lifecycle —
  lifecycle states with immutable releases and visible retraction; per-class versioning
  (SemVer package, no-PATCH `vX.Y` for models/datasets/benchmarks, append-only integer
  schemas); release process with ten checklists (package, HF model/dataset/Space,
  benchmark, paper, updates, deprecation, retraction); GitHub→CI→Releases→HF
  distribution with CI-only publishing; per-artifact licensing matrix (field-level for
  composite datasets); model/dataset card requirements with mandatory verbatim safety
  statements; benchmark publication + leaderboard policy; paper→replication-package
  workflow; release manifest spec; future GitHub Actions design. Documentation only —
  nothing implemented, nothing uploaded.
- **Proposed ADRs 0010** (release architecture; MESC naming — "MedScale-Base" is a
  config reference, never trained base weights) **and 0011** (versioning schemes +
  licensing matrix; closes the long-pending licence ADR debt). Awaiting operator
  approval; not self-ratified.

### Added (T1 ingestion foundation — 2026-07-10)

- **`medscale.litdb` ingestion machinery**: frozen v1 query set as code (Q1–Q10),
  four source adapters (Semantic Scholar, OpenAlex, PubMed, arXiv) behind an injectable
  HTTP layer (CI offline; 404 recorded as NOT_FOUND; 429/transport failures abort
  honestly), verbatim raw archival with SHA-256, byte-stable run manifests, and the
  append-only PRISMA screening log (replay-validated).
- **`data/litdb/` scaffolding** with R3 `LICENSE.md` (per-source terms, verified
  2026-07-10) committed before the first archived byte.
- **Pilot ingestion round 0** (Q2 × 4 sources, cap 3): OpenAlex, arXiv, PubMed archived
  with manifest; Semantic Scholar rate-limited (HTTP 429) after backoff — skipped and
  recorded; full round 1 needs an S2 API key or longer backoff.
- **`docs/architecture/distribution_hf.md`**: Hugging Face (`MedScale` /
  org `MedScaleAI`) recognized as the future distribution layer with publishing gates;
  nothing published before its gate. 22 new offline tests (68 total).

### Added (T1 foundation — 2026-07-10)

- **ADRs 0005–0008 Accepted** with operator refinements (identity: "Open Research
  Intelligence Infrastructure for Medicine"; no hard model dependencies; OpenMed
  boundaries kept ready for future clinical/privacy capabilities; FHIR supports, not
  defines). **ADR-0009 (Evidence Model) Accepted**: evidence objects, verification state
  machine, provenance datatype, deterministic study-design grading.
- **`medscale.provenance`** — Rule R1 as a datatype (SourceAPI, Provenance, NOT_FOUND).
- **`medscale.evidence`** — EvidenceObject with content-derived ids, PICO slots, the
  verification state machine, and the model-cannot-self-verify guard.
- **`medscale.litdb`** — LiteratureRecord (R1 identifier requirement,
  dedupe-by-construction record ids), PRISMA screening state machine (mandatory
  exclusion reasons), SourceAdapter protocol + RawRetrieval envelope (no network code).
- **`docs/execution/search_strategy.md`** — frozen-by-commit query set, PRISMA
  workflow, raw-response archival policy. 38 new deterministic tests (46 total).

### Added (architecture analysis — 2026-07-10)

- **`docs/architecture/`**: evidence-based ecosystem analysis (OpenMed, MedGemma,
  BioMistral, FHIR/EHR-FM, openEHR bridge, OpenEvidence/Medwise), reference architecture
  (adds the verification & reproducibility spine omitted from the proposed 4-layer
  model), AI model strategy, OpenMed integration strategy, interoperability strategy.
- **Proposed ADRs 0005–0008** (awaiting operator approval): research-intelligence scope
  amendment; licence-first two-tier model registry; OpenMed as optional evaluation-time
  adapter; FHIR as single canonical representation with boundary adapters.

## [0.0.0] — 2026-07-09

### Added

- Initial documentation foundation: Strategic Blueprint, Research Vision, research
  questions, paper taxonomy, reproducibility policy, ADR-0003, and archive of the
  superseded working draft. Repository consolidated into a single canonical git repo.
