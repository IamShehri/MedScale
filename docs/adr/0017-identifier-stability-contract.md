# ADR-0017 — Identifier Stability Contract and litdb Pipeline Ordering Invariant

- **Status:** Accepted (2026-07-10, founder approval — the identifier derivations are a
  frozen versioned contract; dedupe-before-decision ordering is binding; `medscale
  check` is the mechanical enforcement, wired into CI)
- **Date:** 2026-07-10
- **Deciders:** Founder
- **Related:** [ADR-0009](0009-evidence-model.md) (evidence_id),
  `medscale.litdb.records` (record_id), `medscale.litdb.integrity`,
  [reproducibility policy](../research/reproducibility_policy.md)

## Context

MedScale's durable data is coupled by **content-addressed identifiers**:
`record_id = content_hash(identifiers)` and `evidence_id = content_hash(claim + PICO +
source + schema_version)`. These ids are used as **keys in append-only logs**
(`review_log.jsonl`, `screening_log.jsonl`), which are the reproducible record of every
human decision.

Two latent hazards make this an expensive-to-change-later decision if left implicit:

1. **Merge orphaning (demonstrated).** Fuzzy dedupe mints a *new* `record_id` (the
   union of identifiers) and removes the merged sources. In the current corpus, 40
   merges removed **80 source ids**. If any human decision had been keyed to one of
   those ids *before* dedupe ran, replaying the log would reference a record that no
   longer exists — a silent reproducibility break. Today this is clean only because
   dedupe preceded all screening; nothing yet *enforces* that ordering.
2. **Derivation drift.** Changing the id inputs, the canonical-JSON serialization, or
   the hash algorithm would silently invalidate every historical id in every committed
   log — unauditable and irreversible without lineage.

## Decision (proposed)

1. **Identifier derivations are a frozen, versioned contract.** The `record_id` and
   `evidence_id` derivations (inputs + `canonical_json` + SHA-256) are stable public
   guarantees. Any change is a **breaking change** requiring: a version bump, an ADR,
   and a migration that rewrites historical log references. They are treated as public
   API (the reproducibility policy's determinism principle, applied to identity).

2. **Pipeline ordering invariant.** Identifier-exact dedupe (corpus store) and fuzzy
   dedupe **must complete before any human decision references a `record_id`.**
   Re-running dedupe after decisions exist is prohibited unless accompanied by a
   migration that remaps orphaned references via the retained `merge_log` lineage.

3. **Enforcement is mechanical, not documentary.** `medscale check`
   (`medscale.litdb.integrity`) verifies that every id referenced by a log resolves to
   a live corpus record, that merged records are present, and that merged-away sources
   are absent. It exits non-zero on any violation, so it gates CI (the future
   `validate-data` workflow) and can be run by any auditor before trusting a corpus.

4. **Merge lineage is retained deliberately** (`merge_log.jsonl` keeps both source
   records verbatim) precisely so a future migration *can* remap references if the
   ordering invariant is ever violated.

## Consequences

**Positive:** the coupling between corpus and logs becomes a checkable guarantee rather
than an implicit assumption; a whole class of silent reproducibility failures is caught
at commit/CI time; the identity scheme is now explicitly a stability contract, which is
what a reference-quality project owes its downstream consumers.

**Negative / costs:** the ordering invariant constrains workflow (no casual re-dedupe
after screening starts) — accepted, because the alternative is orphaned science; a
future id-scheme change now carries an explicit migration obligation — accepted, that
obligation was always real, merely undocumented.

## Alternatives considered

- **Surrogate sequential ids instead of content hashes.** Rejected: content-addressing
  *is* the reproducibility property (equal content ⇒ equal id across machines and
  time); surrogate keys would need a central allocator and break byte-reproducibility.
- **Never merge (drop fuzzy dedupe).** Rejected: leaves version-duplicate records
  (preprint + published twin) in the corpus, a worse scientific defect (S2).
- **Leave it implicit (status quo).** Rejected: works today only by luck of ordering;
  this is exactly the "expensive to change later" decision that should be made explicit
  while it is still cheap.

## Compliance

The check is implemented and passes against the current corpus (1,346 records, 40
merges, 0 issues). On acceptance: wire `medscale check` into the `validate-data` CI job
(releases/ci_cd design) and note the ordering invariant in the search-strategy PRISMA
section. No id derivation changes without a superseding ADR + migration.
