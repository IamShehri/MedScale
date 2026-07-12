# Independent Architecture & Research Review — pre-v1.0

- **Date:** 2026-07-12 · **Baseline:** `500e81d` · **Requested by:** Founder
- **Reviewer disclosure:** the reviewer authored most of this architecture. True
  independence is impossible; the compensation is that every claim below was verified
  against the repository at `500e81d` (not memory), and the review deliberately
  privileges findings that indict the reviewer's own decisions. Where the review
  agrees with an existing decision, evidence is cited for *why*, not deference.

---

## The central finding

MedScale has inverted the usual failure mode. Most projects ship features without
contracts. MedScale has shipped **contracts without use**:

| Frozen surface | Real material that has passed through it |
|---|---|
| Screening state machine + review log | **0** human decisions (1,346 records all PENDING) |
| Evidence model (ADR-0009/0017/0018) | **0** evidence objects |
| Verification engine | **0** real verifications |
| Benchmark engine + gold-set schema | **0** benchmarks (`bench list` → "no benchmarks defined") |
| modelkit protocols (`TextGenerator` etc.) | **0** backends have ever implemented them |
| Public API stability policy (ADR-0020) | frozen the day the sprint ended |
| Reviewer-agreement statistics | `agreement_rate: null` |

Every one of these is well-designed *by inspection*. None has been **falsified by
contact with reality**. The project's own scientific creed — "designed to be
falsified, not assumed" (README) — applies to its architecture and is currently
unmet. The deepest risk to the next decade is not any single design choice below; it
is ratifying v1.0 before real screening decisions, real evidence objects, one real
benchmark, and one real model backend have each had the chance to prove a frozen
contract wrong. **Everything else in this review is subordinate to that.**

---

## 1. Software Architecture

**What holds up.** The layering is real, not aspirational: `tests/test_architecture.py`
enforces six import-graph rules at build time, and it demonstrably catches violations
(it caught 13 introduced during the stabilization sprint itself). Transports are thin;
the spine (`reproducibility`, `provenance`, `_layout`, `_runtime`) has no upward
dependencies; the engine never imports the facade. ~6,700 LOC of src against 3,400 LOC
of tests is a healthy ratio. Zero runtime dependencies is a genuine decade asset.

**What I would change.**

1. **`_layout` abstracts locations, not access.** It centralizes *where* files live,
   but every loader still knows *how* to read JSONL. The advertised guarantee —
   "storage engine replaceable without user-code change" — is true for users but not
   for maintainers: swapping to SQLite (D1 tripwire) touches every loader in litdb,
   research, bench. The missing seam is a record-stream reader/writer interface, not a
   path module. Do not build it now (one implementation = no abstraction), but stop
   describing storage as "abstracted." It is *confined*, which is weaker.
2. **The `Workspace` facade is on a God-object trajectory.** Today: corpus, evidence,
   index, stats, snapshot, verify, benchmarks. Every future capability will want a
   method here, and ADR-0020 makes each addition permanent. Adopt a rule now:
   Workspace only *hands out* capability objects; it never grows verbs.
3. **The layer map lives only inside a test file.** `_LAYER` in
   `test_architecture.py` is now the most authoritative architecture document in the
   repo, and it is not referenced by `docs/architecture/`. Shadow-spec drift risk.
4. **The facade leaks by omission.** `run_benchmark` returns `(artifact, path)`;
   `Workspace`'s `Benchmark.run` discards the path (workspace.py:269), so the bench
   CLI reconstructs it by importing `_layout`. A transport compensating for a facade
   hole by reaching into an internal module is exactly the pattern the architecture
   tests exist to prevent — it passes only because cli is the top layer. The facade
   should return an opaque artifact handle that knows how to report its own location.
5. **modelkit is a frozen interface with zero implementations.** `TextGenerator` is
   synchronous, non-streaming, non-batched, with no token accounting and no logprobs
   (interfaces.py:91–102). The first real backend — llama.cpp or an API provider —
   will almost certainly demand changes. Freezing a protocol before its second (or
   even first) implementation is the classic interface error, and ADR-0020 has now
   made this specific mistake expensive.

## 2. Public API

**Size:** 12 root names. Not too large — the discipline is admirable. It is **too
small in one structural way: the entire public API is read-only** (plus
benchmark-run). Screening decisions, evidence creation, duplicate resolution — every
*write* — is reachable only through the CLI or internal modules. The first real
application (a screening UI, Afia, a web tool) will need writes and will have exactly
two options: shell out to the CLI or import internals. Either violates the
architecture's own premise. The write-side needs a public, audited contract
(`workspace.review(...)` returning append-only events) *before* the first non-CLI
transport, or the contract will be broken by its first consumer.

**Leaks:** minimal. `Workspace.open(root)` takes one opaque path; results are values;
paths don't escape (except the facade hole in §1.4). `canonical_json`/`content_hash`
as public spine primitives is right — they are language-neutral concepts.

**Python-specificity:** acceptable for a library-first strategy, with one exception:
there is **no written wire-format specification** for query results and stats. The
docstrings promise future REST surfaces; a REST adapter will need a versioned JSON
schema for `RecordQueryResult`/stats output that is currently implicit in dataclass
shapes.

**Would I freeze it today?** The read API: **yes** — it is small, tested against the
researcher contract verbatim, and additive growth is cheap. The modelkit protocols:
**no** (§1.5). The write API: **cannot freeze what does not exist**, and that is the
gap. ADR-0020's tier table quietly froze protocols that have never been exercised;
I would amend it to mark `TextGenerator`/`SpanExtractor` as *provisional until first
real backend*.

## 3. Scientific Reproducibility

**Strong, with three concrete spine defects found in this review:**

1. **`canonical_json` accepts NaN/Infinity** (reproducibility.py:30 — no
   `allow_nan=False`). `canonical_json(float("nan"))` emits `NaN`, which is **not
   JSON**. Any future numeric field (a score, a CI bound) could silently produce
   artifacts other parsers reject — in the one function everything hashes through.
2. **No cross-language canonicalization spec.** Key sorting, float formatting
   (Python's shortest-round-trip repr), `-0.0`, int-key coercion (`{1:"a"}` and
   `{"1":"a"}` hash identically), unicode normalization — none is written down. The
   moment a Rust core or a JS client re-implements `content_hash`, byte-identity
   becomes a matter of luck. This is the single biggest blocker to the multi-language
   future and it costs one document plus two `json.dumps` flags to fix.
3. **`set_global_seed` sets `PYTHONHASHSEED` at runtime** (reproducibility.py:51),
   which does not affect the running interpreter — only child processes. The docstring
   claims more than the code does. Harmless today (nothing hash-order-dependent is
   hashed), but a reproducibility library must not overclaim.

Also: **CI never verifies the committed snapshot.** The workflow runs lint, types,
tests, and `medscale check`, but not `medscale snapshot --verify` against
`cfdfcce5e2830391` — the artifact this review re-verified by hand is the one artifact
CI does not gate. One YAML line.

**Would journal reviewers trust it?** The machinery (append-only logs, content-
addressed identity, snapshot-bound benchmarks, no LLM-judge) is *ahead* of common
practice and would impress a JAMIA/JMIR methods reviewer. What they would still reject:
(a) single annotator, no inter-rater reliability — the framework computes agreement
but no second reviewer has ever existed; (b) abstract-only screening presented as a
systematic review (see §4); (c) all hashes are self-attested — nothing anchors the
history externally (signed tags, third-party timestamp, Zenodo DOI), so "the operator
never rewrote history" is a trust assumption, not a property. For *regulatory*
evidence the gap is larger: no authn, no e-signatures, no access control — the audit
trail is honest but the actor identity behind it is a git config string.

## 4. Research Workflow

The pipeline order is correct: screening before evidence, verification before
research intelligence, snapshots before benchmarks. Two findings:

1. **The full-text eligibility stage exists in the docs and not in the software.**
   `docs/execution/search_strategy.md` §4 and `paper_taxonomy.md` both promise an
   eligibility stage ("full-text check; licence and reproducibility signals
   extracted"). The `ReviewDecision` state machine has no title-abstract vs full-text
   distinction — one INCLUDE covers both. PRISMA 2020 mandates the two-stage flow.
   Consequence chain: no full-text stage → no full-text acquisition/storage design →
   evidence objects will be extracted **from abstracts** (836/1,346 records even have
   one; 510 have none) → evidence claims sourced from abstracts alone would not
   survive systematic-review peer review. This is the largest *scientific* gap in the
   platform and it is currently invisible because zero screening has occurred.
2. **`license_spdx` is `None` on all 1,346 records.** The field was designed
   (eligibility was supposed to populate it) and never wired to anything. A designed-
   but-dead field in the frozen record schema is schema debt.

Missing stages that must at least be *designed* before evidence synthesis is claimed:
risk-of-bias assessment (RoB 2 / ROBINS-I) and any synthesis layer (even qualitative).
An evidence platform without critical appraisal produces evidence *inventory*, not
evidence *synthesis* — the docs should say which one MedScale v1 is.

## 5. Governance

The ADR discipline is genuinely rare and the architecture tests are the best
governance artifact in the repo — rules that execute scale better than rules that
persuade. But the current model is a **founder–AI dyad codified**, and three things
will not survive contact with contributors:

1. **Ratification concentration.** ADRs 0009, 0015, 0020 were written and marked
   Accepted by the same actor in the same commit ("founder-directed"). Fine at n=1;
   at n=10 it reads as governance theater. The continuity ADR (0019) — the one that
   addresses exactly this — is itself unratified, which is the most eloquent risk
   statement in the repository.
2. **Six Proposed ADRs are pending, and one (0018, evidence identity) gates the next
   phase of work.** A decision queue that only the founder can drain is a pipeline
   stall by design.
3. **Sequential ADR numbering and one-ticket-per-session norms** are dyad artifacts;
   they collide at the first concurrent contributor (known as D5 — correctly
   triaged, trigger not yet hit).

Scaling verdict: to 10 contributors — yes, with a named-maintainers rule and ADR
review-before-accept. To 100 — no; would need RFC process, CODEOWNERS, working
groups. But the *substrate* (written decisions + mechanical enforcement) is the right
one to grow that from; most projects have neither.

## 6. Long-term Evolution

- **REST / MCP / SDK:** the read path is genuinely ready — `Workspace` is GET-shaped
  and an MCP server over it is days of work. The write path is not (§2). A REST layer
  also needs the wire-format spec (§2) and an authn/identity story the audit trail
  currently lacks (reviewer identity = free-text string).
- **Plugins:** ADR-0021's "design now, build at first external consumer" is correct.
- **Multiple storage engines:** blocked by §1.1 (locations ≠ access). Fine pre-1.0.
- **Rust core:** blocked by §3.2 (no canonicalization spec). This is the cheapest
  decade-insurance available and it is not written.
- **Distributed / multi-writer:** single-writer append-only JSONL with no locking.
  Correctly deferred (D2), but note the current operational hazard: the canonical
  working tree lives inside **OneDrive**, whose sync can produce conflicted copies of
  append-only logs. Git is the real ledger, but the corpus's day-to-day durability
  currently depends on a consumer sync product not corrupting a JSONL append.
- **Desktop/Web:** blocked on write contract; otherwise clean.

No current decision is an *irreversible* bottleneck — the JSONL/no-deps/library-first
choices all have exits. The bottlenecks are the two missing documents (wire format,
canonicalization spec) and the missing write contract.

## 7. Open Source Readiness

1. **The README is a prospectus, not documentation.** Its headline promises
   FHIR-native, grammar-constrained, validator-grounded — **none of which exists in
   the code** (there is no FHIR code at `500e81d`). The status badge says T0; the
   repo is at T1+. An outside engineer who clones, reads, and greps will conclude the
   README oversells — the worst first impression a *verification-branded* project can
   make. The actual shipped value (deterministic corpus + screening + snapshot +
   benchmark engine, 240 tests) is undersold beneath the vision. Restructure: what
   works today first, vision clearly labeled as roadmap.
2. **Docs skew internal:** 66 markdown files, dominated by ADRs (20) and
   internal reviews/governance; there is no task-oriented quickstart ("clone → open
   the included corpus → run a query → capture a snapshot" — all of which *works
   today* and would be a superb 20-line demo).
3. **Data licensing at repo-publication.** `data/litdb/LICENSE.md` is honest and
   ahead of most projects: it names the PubMed-abstract copyright issue and commits
   published *exports* to exclude those fields. But making the **repo** public *is*
   redistribution of the raw archives (16 MB, 43 files, verbatim API responses
   including abstracts). "Audit artifact, not a published dataset" is an argument, not
   a safe harbor. Before flipping to public: segregate or strip PubMed-derived
   abstract text from the public history (raw archives to a private/access-controlled
   store, or rebuild history without them), or obtain a clearer basis. This is the
   single hard *blocker* to going public and it grows more expensive with every
   commit, because history rewriting is forbidden by ADR-0019.
4. **CI:** solid (two Python versions, locked sync, integrity gate) with three gaps:
   no snapshot-verify step (§3), actions pinned by tag not SHA (known, D4), and no
   Windows runner although development happens on Windows — the cp1252/CRLF class of
   bugs that already bit twice is untested in CI.
5. **Release strategy:** designed thoroughly in docs, executed never. Zero tags, zero
   PyPI presence. Contributors calibrate on releases, not design docs.

## 8. Medical AI Platform adequacy

| Capability | Verdict |
|---|---|
| Systematic reviews | **Strong foundation, incomplete pipeline** — missing full-text stage and RoB (§4); abstract-screening infra is publication-grade |
| Evidence synthesis | **Not yet** — inventory ≠ synthesis; no appraisal layer |
| Benchmark generation | **Design ahead of the field** (snapshot-bound, human gold, no LLM-judge) — but unproven with a single real benchmark |
| Medical AI evaluation | **Contracts only** — no backend has ever run; §1.5 applies |
| Clinical reasoning research | Honestly deferred (reserved enum) — correct |
| Regulatory evidence | **No** — audit trail yes; identity, signatures, access control, external anchoring no. Plausible path, long road |
| Reproducible publications | **Closest to ready** — N1 "PRISMA-as-code" is genuinely novel and the machinery for it exists; it needs the screening to happen |

## 9. Risk Register

| # | Risk | Rank | Probability | Impact | Mitigation |
|---|---|---|---|---|---|
| R1 | **Contracts frozen before falsified** — v1.0 ratified before real screening/evidence/benchmark/backend exercise the frozen surfaces | **Critical** | High (it is the current trajectory) | A decade of compatibility promises anchored to untested designs | Gate v1.0 on the four proofs (§10 Q1–Q2); mark modelkit protocols provisional in ADR-0020 |
| R2 | **Authority/bus factor = 1** — private repo, personal account, sole ratifier; continuity ADR unratified | **Critical** | Certain (it is the present state) | Project death is one absence away; all other risks are moot | Ratify 0019; org ownership; publish (after R3) |
| R3 | **Corpus copyright at publication** — verbatim PubMed abstracts in raw archives enter public git history irreversibly (ADR-0019 forbids rewrite) | **High** | Certain *if* published as-is | Legal exposure + un-removable history; blocks the survivability deadline R2 needs | Segregate raw archives / strip protected fields *before* first public push; decide now, cost compounds per commit |
| R4 | **No public write contract** — first UI/transport must import internals or shell the CLI | **High** | High (any application work triggers it) | The architecture's core promise breaks at first real consumer | Design audited write API before first non-CLI transport |
| R5 | **Abstract-only evidence** — full-text stage in docs only; extraction would source claims from abstracts | **High** | High (next phase hits it) | Scientific credibility of the entire evidence layer | ADR for two-stage screening + full-text acquisition before `medscale extract` is used in anger |
| R6 | **Canonicalization unspecified** — NaN accepted, float/key-coercion semantics implicit | **Medium** | Medium (latent until numerics or second language) | Silent hash divergence at the spine | Spec document + `allow_nan=False` + input validation; cheap |
| R7 | **CI doesn't gate the snapshot**; no Windows runner; unpinned actions | **Medium** | Medium | Drift ships silently; the flagship guarantee is hand-checked | Three CI lines |
| R8 | **Single-writer JSONL inside OneDrive** | **Medium** | Low–Medium (git bounds the loss) | Log corruption between commits | Move canonical tree out of synced dir, or commit-per-session discipline; D2 at second reviewer |
| R9 | **Workspace facade accretion** under a frozen-API policy | **Medium** | Medium (slow) | Un-shrinkable God object by 2030 | Capability-object rule (§1.2) |
| R10 | **README/docs overpromise** vs shipped code | **Low** | Certain at publication | Credibility tax on a verification brand | Rewrite before public; label vision as roadmap |

## 10. Twelve-month roadmap (as Chief Architect)

Ordering principle: **run reality through the machine before promising the machine to
anyone.** No cosmetics; every item either falsifies a frozen contract or removes a
decade risk.

**Q1 — Falsification quarter (no new architecture).**
Resolve the 16 uncertain duplicate groups; screen the Q2/Q6 subsets for real
(~300 records) — first real data through the review contract. Ratify/reject the
pending ADR queue, 0018 first (it gates evidence). Decide R3 (data segregation)
now, while history is short. Fix the spine trio (NaN, seed docstring, CI
snapshot-verify + Windows runner) — one day, disproportionate value.

**Q2 — Evidence proven, gaps closed by what Q1 taught.**
ADR + implementation for two-stage screening and full-text acquisition (R5);
first ~25 real evidence objects through extract→verify; second annotator on a
sample so `agreement_rate` stops being null; write the canonicalization spec and
the wire-format spec (R6, decade insurance); design the public write contract
(R4) from the screening UI's actual needs, not speculation.

**Q3 — First benchmark, first external anchor.**
One real benchmark: human gold from the screened corpus, GoldOracle/EmptySystem
baselines published as artifacts — the benchmark engine's first falsification.
One real modelkit backend (llama.cpp or API) implementing `TextGenerator`; amend
the protocols with what reality demands *before* they harden further. Signed
tags + Zenodo DOI for the first tagged release (0.x on PyPI): external trust
anchor, release muscle exercised once for real.

**Q4 — Publication.**
Execute R3 remediation; rewrite README around what demonstrably works; ship the
quickstart against the included corpus; go public; first read-only transport
(MCP or REST) over the now-proven Workspace. **v1.0 only when all four proofs
exist:** real screening decisions, real verified evidence, one published
benchmark, one working backend. If any of them forced a contract change, the
sprint that froze the contracts was still cheap insurance — but only if v1.0
waited for the proof.

---

*Review conducted read-only at `500e81d`; all quantitative claims verified by
execution against the working tree on 2026-07-12.*
