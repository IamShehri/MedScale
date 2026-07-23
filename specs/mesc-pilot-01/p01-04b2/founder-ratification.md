# MESC Pilot-01 — P01-04B2 Decision Record

Status: **design decisions ratified — implementation and execution not authorized**

This document records the founder-ratified architecture decisions for P01-04B2
tooling. The eight decisions below are resolved and binding for design.
None of them authorizes implementation or execution. Ratified decisions in
`specs/mesc-pilot-01/p01-04/decision-record.md` (D1–D10) are unchanged and
remain the authoritative longitudinal record.

---
## Ratified decisions (P01-04A — not repeated here)

D1–D10 remain ratified policy as recorded in `specs/mesc-pilot-01/p01-04/decision-record.md`.
They are not re-ratified here. Any P01-04B2 design that conflicts with D1–D10
is subordinate to D1–D10.

A subordinate implementation-design ratification note was appended to
`specs/mesc-pilot-01/p01-04/decision-record.md` referencing FD-B2-1 through
FD-B2-8. That note does not amend D1–D10. D1–D10 control on conflict. No
implementation or execution authority follows from ratification of this package.

---
## Implementation status

| Decision area | Status |
|---|---|
| D1–D10 ratified policy | Ratified (P01-04A); unchanged |
| P01-04B1 pure split core | Implemented and adopted on canonical main (`ce12722`) |
| B2 design decisions (FD-B2-1 through FD-B2-8) | Founder ratified 2026-07-24; implementation not authorized |
| Public splitter facade | Not implemented; reserved for separate authorization |
| Leakage-detection library | Not implemented; reserved for separate authorization |
| Artifact builders | Not implemented; reserved for separate authorization |
| Split fingerprint artifact (64-hex) | Designed; not implemented |
| CLI entry point | Not implemented; deferred |
| Real split execution | Not authorized |
| Leakage audit execution | Not authorized |
| P01-04C–G stages | Not authorized |

---
## Ratified decisions

### FD-B2-1 — Fixture-only facade and public splitter boundary

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-1):**
`SourceDocumentGroupedSplitter.assign()` in its future authorized form must accept only synthetic fixture rows and must refuse canonical real inputs.

Alternatives considered:
1. Explicit fixture-only request type injected at call time
2. Injected source rows with no disk access
3. Authorization capability/token required at instantiation
4. Private implementation with guarded public facade

Recommended path was: private implementation with guarded public facade (option 4), using explicit fixture-only request type (option 1) for integration entry point.

**Founder-ratified decision:**

1. Existing `SourceDocumentGroupedSplitter.assign()` remains unconditionally fail-closed.
2. It must not be widened to execute fixture or real assignments.
3. B2C may later implement a separate fixture-only facade, provisionally named `FixtureSplitFacade`.
4. The facade accepts only `FixtureSplitRequest`.
5. `FixtureSplitRequest` must be structurally synthetic-only. It cannot be created from:
   * arbitrary registry rows;
   * filesystem paths;
   * P01-03G rows;
   * external source-record rows;
   * evidence-root references.
6. Synthetic identity must be proven by:
   * an approved fixture namespace;
   * fixture schema version;
   * fixture fingerprint;
   * explicit `fixture_only=true` marker.
7. No filename, directory name or path heuristic may establish fixture identity.
8. The eventual formal P01-04D executor must be a separate private/formal entry point under separate authorization.
9. No capability token is required for B2 fixture execution; the typed structural boundary is the authority boundary.

### FD-B2-2 — Authoritative split identity

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-2):**
Distinguish two hash values with different authority:
* `split_fingerprint` (64 lowercase hexadecimal characters; full SHA-256 over the defined canonical split bundle) is the sole authoritative split identity.
* `split_hash` (16 lowercase hexadecimal characters; truncated SHA-256) is a compatibility and display value only, retained for B1 `PilotSplitManifest.computed_split_hash`.

The 16-hex compatibility value must never be silently treated as equivalent to the full 64-hex fingerprint.

**Founder-ratified decision:**

1. `split_fingerprint` is the sole authoritative split identity.
2. Format:
   * full SHA-256;
   * 64 lowercase hexadecimal characters.
3. `split_hash`, the existing 16-hex truncated value, is:
   * B1 compatibility-only;
   * display-only;
   * never authoritative;
   * never promotable-artifact identity;
   * never valid for cross-generation equality.
4. The fingerprint is computed over canonical JSON bytes of a canonical bundle manifest.
5. The canonical bundle manifest must bind:
   * `bundle_schema_version`;
   * `policy_id`;
   * `algorithm_version`;
   * `split_seed`;
   * canonical artifact role;
   * SHA-256;
   * byte size;
   * stable schema version for each artifact.
6. Artifact entries are ordered by stable artifact role.
7. The bundle must bind the exact canonical bytes of:
   * group-registry artifact;
   * example-split-registry artifact;
   * split-summary identity core;
   * excluded-or-unassigned ledger;
   * any other ratified formal split artifact.
8. The split-summary identity core must exclude:
   * `split_fingerprint` itself;
   * provenance dates;
   * local/runtime metadata;
   * command evidence.
9. Assignment rows and group structure are bound through the full SHA-256 and byte size of their canonical artifact bytes.
10. Any mismatch in fingerprint, artifact hash or artifact byte size is fail-closed.

### FD-B2-3 — Dates, provenance and reproducibility

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-3):**
* `ratified_at`: ISO date only, injected at authorization time, excluded from fingerprint payloads.
* `generated_at`: ISO date only, NOT populated by runtime timestamp generation in deterministic artifacts.
* No runtime timestamps in any deterministic artifact.
* Date fields excluded from fingerprint payloads to ensure reproducibility across time zones and clock drift.

**Founder-ratified decision:**

1. No date or timestamp field is permitted in a fingerprinted promotable split artifact.
2. Remove proposed fields such as `ratified_at` and `generated_at` from promotable artifact contracts.
3. Runtime timestamps are prohibited in deterministic artifact bytes.
4. Founder-ratification dates belong only in the repository decision/authorization record and the external provenance envelope.
5. Generation dates and execution times belong only in external execution evidence.
6. External provenance is non-promotable, outside the evidence root, excluded from split-fingerprint payloads, and referenced only by stable identity where required.
7. Equal authoritative fingerprints must correspond to byte-identical promotable artifact bundles.

### FD-B2-4 — Canonical JSON and JSONL

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-4):**
* sorted keys (recursive);
* UTF-8;
* no BOM;
* LF-only line endings;
* terminal newline at end of each line;
* `ensure_ascii=False`;
* `allow_nan=False`;
* separators: `(",", ":")`;
* no indentation;
* identical output on repeated runs with identical inputs across supported runtimes.

**Founder-ratified decision:**

1. Encoding: UTF-8.
2. BOM: prohibited.
3. Key ordering: recursive lexicographic key sorting.
4. `ensure_ascii=False`.
5. `allow_nan=False`.
6. Separators: `(",", ":")`.
7. Indentation: none.
8. Line ending: LF only.
9. CRLF output is prohibited.
10. JSONL: one object per line; exactly one LF after every object; no blank lines; zero records produce a zero-byte file.
11. Single-object JSON: exactly one canonical JSON object; exactly one final LF.
12. Record ordering is defined before serialization and cannot depend on map insertion order.
13. Required ordering:
    * group registry: `(assigned_split, group_id)`;
    * example registry: `(assigned_split, row_ordinal)`;
    * artifact manifest entries: stable artifact role;
    * findings: deterministic finding identifier.
14. Identical inputs must produce byte-identical outputs across supported Python 3.11 and 3.12; Windows, Linux and macOS; locale settings; time zones.
15. Serialization must not depend on local paths, usernames, hostnames, runtime clocks or environment ordering.

### FD-B2-5 — Atomic publication and concurrency

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-5):**
* unique temporary names for all in-progress writes;
* no-overwrite semantics on completed artifacts;
* atomic rename for finalization;
* concurrent writer rejection (explicit error, not silent serialization);
* invalidated candidate preservation (never overwritten or deleted);
* cleanup of failed writes from workspace only, never from evidence root or repository.

**Founder-ratified decision:**

1. Generators write only to a dedicated generation workspace.
2. They must never write directly to repository paths, evidence root, or frozen canonical artifact locations.
3. Each in-progress write uses a unique temporary name, exclusive creation, and the same filesystem as its intended final destination.
4. Completed artifacts use strict no-overwrite semantics.
5. An existing destination is a hard failure.
6. Finalization must use an atomic no-overwrite operation.
7. POSIX behavior must not rely on ordinary rename replacement semantics.
8. Windows behavior must preserve destination-exists rejection.
9. Concurrent writers must be rejected explicitly.
10. Race detection cannot silently serialize or overwrite writers.
11. Before finalization: file content is flushed; file durability sync is performed.
12. After finalization: containing-directory durability sync is performed where supported; any platform durability limitation is explicitly recorded in external evidence.
13. A failed run may clean only temporary files owned by that run.
14. A failed run must never delete completed artifacts, another writer's files, evidence-root contents, or invalidated candidate evidence.
15. Invalidated candidates receive immutable unique identities and are preserved for forensic review.
16. The known B0 single-writer report limitation is not acceptable for concurrent B2 publication.

### FD-B2-6 — Leakage normalization and classification

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-6):**
* exact-example: byte-equality on `example_id`
* exact-source-document: byte-equality on `source_document_id`
* exact-question: byte-equality on question text
* normalized-question: NFKC normalization, case folding, whitespace collapse
* token-set Jaccard: tokenization on whitespace/punctuation boundary, Jaccard >= 0.90 threshold
* empty token sets: classified as non-leakage with explicit evidence
* finding identifiers: deterministic, stable across reruns
* suppression is prohibited. Every finding must carry an explicit `classification` of `unresolved`, `false_positive`, or `confirmed_leakage`. A finding remains `unresolved` unless it is classified as `false_positive` with supporting evidence or as `confirmed_leakage`. The `suppressed` flag must always be `false`. Setting `suppressed=true`, silently dropping a finding, or omitting a finding without classification is a hard stop condition that halts the audit.

**Founder-ratified decision:**

#### Exact identity checks

1. Exact example leakage: byte equality of canonical `example_id`.
2. Exact source-document leakage: byte equality of canonical `source_document_id`.
3. Exact question: byte equality of UTF-8 question bytes.
4. Exact context: byte equality of UTF-8 context bytes.

#### Normalization

The normalization pipeline is exactly:
1. Unicode NFKC normalization;
2. Unicode case folding;
3. collapse every run of Unicode whitespace to one ASCII space;
4. strip leading and trailing whitespace.

#### Tokenization

1. Tokens are maximal consecutive Unicode alphanumeric runs.
2. Punctuation and whitespace are token boundaries.
3. Empty tokens are discarded.
4. Similarity uses token sets, not token multisets.

#### Thresholds

1. Question near-duplicate: token-set Jaccard >= 0.90.
2. Context approximate overlap: token-set Jaccard >= 0.95.
3. Approximate context findings remain `unresolved` until human classification.
4. Exact equality and approximate overlap are separate finding types.

#### Empty normalized content

1. If both normalized questions are empty: do not auto-classify as non-leakage; emit an `empty_normalized_question` finding; initial classification is `unresolved`.
2. If exactly one token set is empty: no Jaccard score is fabricated; the comparison is recorded as not evaluable in audit evidence; it is not silently declared clean.

#### Findings

1. `finding_id` is deterministic over finding schema version, finding type, sorted example IDs, sorted source-document IDs, sorted partitions, and normalized score representation.
2. Every detected finding must be represented.
3. Allowed classifications are exactly `unresolved`, `false_positive`, or `confirmed_leakage`.
4. `false_positive` requires a stable supporting-evidence reference.
5. Suppression is prohibited.
6. `suppressed` must always be `false`.
7. Any dropped, omitted or suppressed finding is a hard stop.
8. Raw question, context or answer text may be inspected only in authorized transient memory.
9. Raw text must never enter promotable artifacts.
10. Promotable reports contain stable identifiers, semantic finding types, scores, classification and external evidence references only.

### FD-B2-7 — Synthetic fixture identity and qualification suite

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-7):**
synthetic 1,000-row fixture generated from synthetic identities only; reproduces label totals 552/338/110; targets 700/150/150; contains no P01-03G membership; cannot be confused with formal dataset evidence; produces byte-identical repeated outputs.

**Founder-ratified decision:**

Ratify a versioned fixture suite rather than one vacuous fixture.

#### Universal fixture requirements

Every fixture must:
1. use namespace `mesc-fixture/p01-04b2/<fixture-schema-version>/<fixture-id>`;
2. use synthetic identities only;
3. contain no P01-03G membership;
4. contain no copied canonical registry identifiers;
5. have fixture schema version, fixture ID, fixture SHA-256 fingerprint, `fixture_only=true`, and explicit `non_evidence=true`;
6. remain non-promotable;
7. be impossible to confuse with formal dataset evidence;
8. produce byte-identical outputs across supported Python versions and operating systems.

#### Fixture A — exact-reference-1000-v1

1. exactly 1,000 synthetic rows;
2. label totals: yes: 552, no: 338, maybe: 110;
3. exact target partition counts: train: 700, validation: 150, test: 150;
4. multi-example groups are mandatory;
5. group sizes must include: 1, 2, 3, 5, 8, 13;
6. group construction must make the exact partition target feasible;
7. each partition must contain at least one multi-example group;
8. no source-document group may cross partitions.

#### Fixture B — constraint-stress-1000-v1

1. exactly 1,000 synthetic rows;
2. the same 552/338/110 label totals;
3. the same nominal 700/150/150 targets;
4. multi-example group sizes intentionally make exact targets infeasible;
5. acceptance is deterministic globally minimum deviation under the indivisible-group constraint, zero cross-partition group overlap, byte-identical repeated output, explicit recorded deviation.

#### Fixture C — leakage-positive-v1

1. synthetic only;
2. includes deterministic cases for exact example identity, exact source-document identity, exact question, normalized question equality, question Jaccard at and above threshold, exact context, approximate context overlap, both-empty normalized questions;
3. expected findings are predefined;
4. at least one expected finding is classified as a supported synthetic `false_positive`;
5. at least one remains `unresolved`;
6. the audit report must not be empty;
7. no raw text appears in the promotable expected report.

### FD-B2-8 — Entry point and CLI boundary

**Status:** FOUNDER RATIFIED ON 2026-07-24 — IMPLEMENTATION AND EXECUTION NOT AUTHORIZED

**Historical proposal context (PD-8):**
* fixture-only entry point accepts only synthetic fixture inputs;
* rejects canonical P01-03G registry paths;
* rejects external source-record files;
* rejects evidence-root destinations;
* requires no real execution authorization;
* defines exit-code classes consistent with MedScale CLI governance.

**Founder-ratified decision:**

1. B2 execution surface is library-only and in-memory.
2. B2 does not add a CLI.
3. B2 does not accept arbitrary filesystem input paths.
4. B2 does not accept arbitrary filesystem output paths.
5. The fixture facade accepts only a verified `FixtureSplitRequest`.
6. Fixture identity is validated structurally, never inferred from a filename.
7. A fixture file may be supported only in a later separately-authorized phase using a frozen fixture registry and fingerprint verification.
8. CLI work is deferred until B2A, B2B, B2C and B2D are complete and independently accepted.
9. Any later CLI requires separate founder authorization and must reuse the existing MedScale CLI exit-code contract rather than inventing new codes.
10. The eventual formal P01-04D entry point is separate from the B2 fixture facade.
11. B2 cannot read P01-03G registry paths, external source-record files, or evidence-root locations.
12. B2 cannot publish formal evidence.

---
## Boundary violations to avoid

The following are explicitly prohibited in any implementation authorized under P01-04B2:

* modifying `src/medscale/mesc/split.py` data contracts (`PilotSplitAssignment`, `PilotSplitManifest`, `PilotLeakageFinding`, `PilotLeakageAuditReport`) without founder decision;
* adding a public `assign()` that silently fabricates assignments without authorization;
* exposing raw question, context, or answer text in any promotable artifact;
* generating real P01-03G registry membership;
* authorizing P01-04C–G implicitly;
* modifying P01-04A decisions D1–D10;
* using runtime timestamps in deterministic artifacts;
* claiming leakage is ruled out.

---
## Ratification does not imply authorization

Completion of P01-04B2 documentation does not authorize implementation.
Completion of P01-04B2 implementation does not authorize execution.
Execution authorization requires explicit founder authorization for each stage
(P01-04B, P01-04C, P01-04D, etc.).

Founder Abdulaziz M. Alshehri ratified FD-B2-1 through FD-B2-8 on 2026-07-24.
Repository adoption occurs when the P01-04B2 documentation PR referring to this ratification is merged.
Any future amendment requires a new founder decision and independent review.
