# MESC Pilot-01 — P01-04 Acceptance Criteria

Status: **specification and policy only — no execution authorized**

Acceptance is defined separately for each stage. Acceptance of an earlier stage does not automatically grant execution authorization for a later stage.

---

## P01-04A — Documentation Acceptance

P01-04A passes acceptance when:

1. All eight required documents exist in `specs/mesc-pilot-01/p01-04/`.
2. Every ratified founder decision from the authorization is reflected accurately in `decision-record.md`.
3. No document claims execution has started.
4. No document claims leakage has been ruled out.
5. No document includes source-data redistribution claims not present in the canonical `rights-and-provenance-record.json`.
6. No document contains placeholder text or markers indicating unfinished drafting work.
7. No document contains unresolved merge-conflict markers.
8. No document contains local paths, usernames, hostnames, or timestamps.
9. Cross-document references are internally consistent.
10. `git diff --check` produces no whitespace errors.
11. Changed-path scope is limited to:
    - `specs/mesc-pilot-01/p01-04/**`
    - minimum necessary updates to `specs/mesc-pilot-01/plan.md` and `specs/mesc-pilot-01/tasks.md`

P01-04A acceptance does not authorize P01-04B or any later stage.

---

## P01-04B — Tooling Acceptance

P01-04B passes acceptance when:

1. Existing `SourceDocumentGroupedSplitter.assign()` remains unconditionally fail-closed.
2. A separate fixture-only `FixtureSplitFacade` is defined for B2 synthetic fixture execution.
3. Library-only, in-memory execution path is established for B2.
4. No formal B2 CLI is part of P01-04B acceptance.
5. The full 64-hex `split_fingerprint` artifact is ratified as the authoritative split identity.
6. The 16-hex `split_hash` remains a B1 compatibility/display value; it is not authoritative.
7. Leakage normalization rules follow FD-B2-6.
8. Three synthetic fixtures (`exact-reference-1000-v1`, `constraint-stress-1000-v1`, `leakage-positive-v1`) are the qualification suite.
9. All rank-determining inputs are stable synthetic values; outputs are byte-identical across supported runtimes when inputs are identical.
10. No real P01-03G registry membership is generated or disclosed during P01-04B acceptance.

P01-04B acceptance requires a separate founder authorization.

## P01-04B — Implementation Status Matrix

### Historical implementation snapshot — SUPERSEDED

HISTORICAL IMPLEMENTATION SNAPSHOT — SUPERSEDED.

The block below records the implementation status that was true on canonical
main at `3edf328f583f13fcd9d566e5080ec3cce83ae178`, with documentation
maintenance on canonical documentation baseline
`ce1272235cb48dbacdb18f20e1ae8db695b01328`. It was accurate for those baselines
and is preserved unrewritten as a historical record. It does not state current
status. The "Current acceptance disposition" subsection below supersedes it in
full for all current status purposes.

```text
The matrix does not mark P01-04B accepted. P01-04B overall remains incomplete.

Public SourceDocumentGroupedSplitter activation:
NOT AN ACCEPTANCE REQUIREMENT — MUST REMAIN FAIL-CLOSED

Separate FixtureSplitFacade:
UNSATISFIED

Full split-fingerprint:
DESIGN RATIFIED — IMPLEMENTATION UNSATISFIED

CLI:
DEFERRED / NOT PART OF B2 ACCEPTANCE

Three-fixture integrated qualification:
UNSATISFIED

P01-04B1 satisfies the private pure split-core criteria only.
No real partition membership has been generated or disclosed.
Public tooling, artifact builders, leakage checks, execution controls,
and end-to-end synthetic qualification remain incomplete.
```

### Current acceptance disposition

This subsection is the current controlling status for P01-04B.

```text
Canonical acceptance baseline:
d5a6ac1654cabd33b6a795756d2796bceaf1652a

Founder P01-04B acceptance:
ISSUED ON 2026-08-04

P01-04B tooling:
ACCEPTED

Implementation merged:
YES

Post-merge CI:
SUCCESS

Post-merge CodeQL:
SUCCESS

Cross-platform qualification:
SUCCESS

Optional backends:
SUCCESS

Real split execution:
NOT AUTHORIZED

Real partition membership:
NOT AUTHORIZED

Canonical leakage execution:
NOT AUTHORIZED

P01-04C:
NOT AUTHORIZED

P01-04D through P01-04G:
NOT AUTHORIZED
```

Tooling acceptance is not real execution authorization. Accepting P01-04B
accepts the implemented and qualified tooling only. It does not authorize any
real split, real partition membership, canonical leakage execution, evidence
publication, model access, inference, retrieval, training or fine-tuning, and it
is never permission to perform P01-04C, P01-04D or any later stage. Each of
those requires its own separate founder authorization.

### Acceptance criterion mapping

Each of the ten P01-04B acceptance criteria above is mapped individually against
canonical main `d5a6ac1654cabd33b6a795756d2796bceaf1652a`.

```text
1. Public SourceDocumentGroupedSplitter remains fail-closed:
SATISFIED

2. Separate private FixtureSplitFacade:
SATISFIED

3. Library-only in-memory execution path:
SATISFIED

4. No formal CLI:
SATISFIED

5. Full 64-hex split_fingerprint authoritative:
SATISFIED

6. 16-hex split_hash compatibility/display only:
SATISFIED

7. FD-B2-6 leakage normalization:
SATISFIED

8. Three accepted synthetic qualification fixtures:
SATISFIED

9. Deterministic byte-identical supported-runtime qualification:
SATISFIED

10. No real P01-03G membership generated or disclosed:
SATISFIED
```

The three accepted synthetic qualification fixtures are exactly:

```text
exact-reference-1000-v1
constraint-stress-1000-v1
leakage-positive-v1
```

All ten criteria are SATISFIED. The fixtures are synthetic. No real partition
membership has been generated or disclosed, and no real P01-03G registry
membership was accessed.

```text
P01-04B:
ACCEPTED

P01-04C:
NOT AUTHORIZED
```

The P01-04C acceptance criteria recorded below are unchanged by this
disposition. P01-04C is not accepted and is not authorized.

---

## P01-04C — Fixture Qualification

P01-04C passes acceptance when:

1. All fixture tests pass for synthetic small input (e.g. 20 rows).
2. All artifacts produce byte-identical output on repeated runs.
3. Edge cases pass: empty inputs, single-example input, all-one-label input.
4. No real dataset partition membership is generated.

P01-04C acceptance requires a separate founder authorization.

### Current acceptance disposition

This subsection is the current controlling status for P01-04C.

```text
Canonical acceptance baseline:
b20dbe0000a129f3019d6f7d2895622ce0560069

Accepted reviewed head:
c9cf1cc58b3ff89c39327c328a10308c0a9dbf4d

Merged PR:
#85

Founder P01-04C acceptance:
ISSUED ON 2026-08-04

P01-04C synthetic fixture qualification:
ACCEPTED

Post-merge CI:
SUCCESS

Post-merge CodeQL:
SUCCESS

Post-merge Optional Extras / Backends:
SUCCESS

P01-04D:
NOT AUTHORIZED

Real dataset execution:
NOT AUTHORIZED
```

Each of the four P01-04C acceptance criteria above is mapped individually
against canonical main `b20dbe0000a129f3019d6f7d2895622ce0560069`.

```text
1. Deterministic synthetic small-input fixture tests:
SATISFIED

2. Repeated-run artifact byte identity:
SATISFIED

3. Ratified edge-case semantics:
SATISFIED

4. No real dataset partition membership:
SATISFIED
```

The ratified edge-case semantics are that `pass` does not require a successful
split in every case: empty input is expected to fail closed deterministically,
single-example input is expected to succeed, and all-one-label input is expected
to succeed.

The accepted synthetic qualification fixtures are exactly:

```text
p01-04c-small-20-v1
p01-04c-single-example-v1
p01-04c-all-one-label-20-v1
empty-input deterministic fail-closed case
```

This disposition accepts the synthetic fixture qualification only. It authorizes
no real dataset access, no P01-03G registry access, no real split generation, no
real partition membership, no canonical leakage execution, no dataset or
registry scanning, no record-pair discovery, no public export, no filesystem or
evidence publication, no model access, inference, retrieval, benchmark
execution, training, fine-tuning, adapter creation and no clinical use.

```text
P01-04C:
ACCEPTED

P01-04D:
NOT AUTHORIZED
```

The P01-04D acceptance criteria recorded below are unchanged by this
disposition. P01-04D is not accepted and is not authorized.

---

## P01-04D — Formal Split Generation

P01-04D passes acceptance when:

1. Split was generated by executed code, not hand-written.
2. Generation was performed in two independent workspaces (Generation A and Generation B).
3. Generation A output byte-identical to Generation B output.
4. Exact row totals are 700 / 150 / 150.
5. No source-document group is split across partitions.
6. Zero cross-partition `original_example_id` duplicates.
7. Zero cross-partition `source_document_id` overlaps.
8. Label distributions match the ratified target matrix within integer rounding.
9. Split fingerprint recomputes to the same value from the canonical split manifest.
10. All promoted artifacts exclude runtime metadata, local paths, timestamps, and usernames.

P01-04D acceptance requires a separate founder authorization.

### P01-04D acceptance disposition

**Current truth.** The sentence above describes the state before execution and
is preserved for it. The separate founder authorization was issued, the
execution was performed, and P01-04D is now accepted.

The ten criteria above are unchanged. They were not modified after the result
was known, and each is mapped individually in
[`../p01-04d-execution-acceptance/acceptance-verification.md`](../p01-04d-execution-acceptance/acceptance-verification.md).
The controlling decision is
[`../p01-04d-execution-acceptance/founder-disposition.md`](../p01-04d-execution-acceptance/founder-disposition.md).

```text
1. Executed code, not hand-written:                       SATISFIED
2. Two independent workspaces:                            SATISFIED
3. Generation A byte-identical to Generation B:           SATISFIED
4. Exact row totals 700 / 150 / 150:                      SATISFIED
5. No source-document group split across partitions:      SATISFIED
6. Zero cross-partition example-identity duplicates:      SATISFIED
7. Zero cross-partition source_document_id overlaps:      SATISFIED
8. Label distributions match the ratified target matrix:  SATISFIED
9. Split fingerprint recomputes to the same value:        SATISFIED
10. No runtime metadata, paths, timestamps or usernames:  SATISFIED
```

```text
P01-04D:
ACCEPTED

FORMAL SPLIT GENERATION:
COMPLETE

AUTHORITATIVE RESULT:
Episode #2

AUTHORITATIVE SPLIT FINGERPRINT:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91

P01-04E:
NOT STARTED — NOT AUTHORIZED

P01-04F and P01-04G:
NOT AUTHORIZED
```

This disposition accepts the formal split generation only. It establishes a
deterministic, formally verified, independently reproduced split. It establishes
nothing about model quality, clinical validity, benchmark superiority or
training effectiveness, and it authorizes no leakage execution, no freeze, no
promotion, no model access, no inference, no retrieval, no training, no
fine-tuning and no clinical use.

---

## P01-04E — Leakage Audit

### FD-E-CTX-1 — Context contract adjudication

Issued 2026-08-12 before any P01-04E execution. This resolution is controlling
for P01-04E.

The context leakage contract is the previously founder-ratified FD-B2-6 contract.

P01-04E performs exactly two context detection classes:

**Exact context:** byte equality of raw UTF-8 bytes of individual context
segments. No normalization is applied before the exact-context comparison.

**Approximate context overlap:** each context segment is normalized using the
ratified pipeline (NFKC, casefold, whitespace collapse, trim), tokenized using
the canonical maximal-Unicode-alphanumeric-run contract, and compared via exact
integer Jaccard arithmetic with threshold >= 0.95.

The older criterion phrase "no identical normalized context segments across
partitions" is prospectively superseded for P01-04E by FD-E-CTX-1.  It does not
introduce a third `normalized_context` detection class, a new finding type, or a
new finding-schema version.

Context findings use `finding_type = context_overlap`:
- exact context: `score_representation = none`
- approximate context: `score_representation = jaccard:<reduced-i>/<reduced-u>`

### Acceptance criteria

P01-04E passes acceptance when:

1. Exact-example cross-partition check: zero cross-partition `original_example_id` duplicates.
2. Source-document identity cross-partition check: zero cross-partition `source_document_id` overlaps.
3. Exact-question cross-partition check: zero unresolved byte-exact cross-partition matches.
4. Normalized-question cross-partition check: zero unresolved normalized cross-partition matches (NFKC, case-folded, whitespace-collapsed).
5. Near-duplicate question detection: zero unresolved Jaccard >= 0.90 cross-partition candidates.
6. Context detection: zero unresolved cross-partition context findings (exact-byte equality and normalized-tokenized Jaccard >= 0.95 per FD-E-CTX-1 above).
7. All detected candidates are classified through evidence-preserved review rules; no candidate is silently suppressed.
8. Findings are zero or all findings are classified as non-leakage with explicit evidence.
9. `leakage-audit.json` is produced with `leaked: false`.

A finding is unresolved unless it is explicitly classified as a false positive with supporting evidence. Suppression of a finding is a stop condition.

P01-04E acceptance requires a separate founder authorization.

### Current implementation status

```text
P01-04E:
ACCEPTED / CLOSED

P01-04F:
ACCEPTED / CLOSED

P01-04G:
NOT STARTED / NOT AUTHORIZED
```

---

## P01-04F — Freeze and Independent Acceptance

P01-04F passes acceptance when:

1. All outputs are written exactly once to a frozen evidence root.
2. Pre-freeze and post-freeze inventories match.
3. An independent rerun produces identical outputs.
4. No post-freeze mutation occurred.
5. `p01-04-closeout-record.json` records:
   - authorization reference
   - input artifact SHA-256s
   - split hash
   - generation workspace identity (stable reference, not local path)
   - independent verification result
6. Any invalidated candidates are preserved and never rewritten.

P01-04F acceptance requires a separate founder authorization.

---

## P01-04G — Repository Promotion and Closeout

P01-04G passes acceptance when:

1. A separate promotion authorization has been granted.
2. Frozen artifacts are promoted to `specs/mesc-pilot-01/p01-04/`.
3. All promoted artifacts pass the promotable-artifact scan (no runtime metadata, no local paths, no timestamps).
4. Closeout record is finalized.
5. No unauthorized paths were modified during promotion.
6. P01-04 promotion does not authorize P01-05.

---

## Missing metric policy

Any acceptance metric that cannot be computed because of missing data, missing artifacts, or unauthorized execution must return:

```text
value: None
status: not_applicable
note: <reason>
```

Silent omission is not permitted.
