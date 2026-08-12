# MESC Pilot-01 — P01-04 Decision Record

Status: **specification and policy only — no execution authorized**

This record contains founder policy decisions for P01-04 split and leakage auditing. Implementation and execution decisions are not marked complete; they remain pending separate authorization.

## Founder ratification metadata

- Ratification status: Ratified for specification and policy only
- Ratification date: 2026-07-20
- Review reference: P01-04A-final-ratification-review-20260720-707195f1
- Ratified PR head: 707195f12294d2c3e6e1d483bd1398493f023cb9
- Execution status: Not authorized

---

## D1 — Partition set

Decision: The initial canonical split contains exactly `train`, `validation`, and `test`. No holdout partition is included in P01-04 version 1.

A future holdout requires a separately ratified policy amendment and a new split-algorithm version.

**Status**: Ratified for specification only. Execution not authorized.

---

## D2 — Target sizes

Decision: For the accepted 1,000-example PubMedQA dataset:

- train: 700
- validation: 150
- test: 150

The ±5-example tolerance proposed by the readiness review is rejected for the current dataset version.

A future dataset containing multi-example groups may define a separately ratified grouped-allocation tolerance.

**Status**: Ratified for specification only. Execution not authorized.

---

## D3 — Grouping unit

Decision: The canonical indivisible grouping unit is `source_document_id`.

All examples belonging to one `source_document_id` must remain in the same partition.

The specification explicitly acknowledges that the accepted current registry contains:

- 1,000 examples;
- 1,000 source documents;
- zero source documents containing more than one example;
- maximum group size of one.

Therefore, source-document grouping is currently structurally vacuous but remains the correct forward-compatible grouping invariant.

P01-04 must not claim that this invariant alone rules out question-level or context-level leakage.

**Status**: Ratified for specification only. Execution not authorized.

---

## D4 — Stratification field

Decision: The canonical stratification field is `decision`.

Canonical strata are: `yes`, `no`, `maybe`.

Stratification is applied to group allocation. It must never split a source-document group.

The current dataset contains:

- `yes`: 552
- `no`: 338
- `maybe`: 110

**Status**: Ratified for specification only. Execution not authorized.

---

## D5 — Integer apportionment

Decision: The split policy must produce exact row totals of 700 / 150 / 150, integer label counts, and minimum deviation from ideal 70/15/15 label proportions.

Deterministic constrained-apportionment algorithm:

1. Compute the ideal real-valued class-by-partition matrix.
2. Enumerate or derive valid integer matrices satisfying:
   - every class total exactly;
   - every partition total exactly.
3. Minimize the sum of squared deviations from the ideal matrix.
4. Break ties by selecting the lexicographically smallest integer vector, compared in this order:
   - label order: `yes`, `no`, `maybe`
   - partition order: `train`, `validation`, `test`

Expected target matrix for the current 1,000-example dataset:

| Decision | Train | Validation | Test | Total |
|---|---|---|---|---|
| yes | 386 | 83 | 83 | 552 |
| no | 237 | 50 | 51 | 338 |
| maybe | 77 | 17 | 16 | 110 |
| total | 700 | 150 | 150 | 1000 |

These are aggregate policy targets only. Example membership must not be calculated or disclosed during P01-04A.

**Status**: Ratified for specification only. Execution not authorized.

---

## D6 — Deterministic ranking contract

Decision: Do not allocate by raw lexicographic ordering of `source_document_id`. Do not use a pseudorandom generator.

Within each decision stratum, rank complete groups by ascending SHA-256 digest of canonical UTF-8 bytes representing:

```json
{
  "algorithm_version": "mesc-pilot-01-split-algorithm/1",
  "seed": "mesc-pilot-01-split-v1",
  "stratum": "<yes|no|maybe>",
  "source_document_id": "<canonical source_document_id>"
}
```

Canonical serialization rules:

- recursively sorted keys;
- UTF-8;
- `ensure_ascii=False`;
- `allow_nan=False`;
- separators: `(",", ":")`;
- no indentation;
- no BOM;
- no terminal newline.

Ranking order:

1. digest ascending as lowercase hexadecimal;
2. `source_document_id` ascending as collision tie-break;
3. minimum `row_ordinal` ascending as final defensive tie-break.

The seed is a domain-separation value, not an RNG seed.

Changing the seed, algorithm version, grouping unit, ratios, stratifier, normalization, or tie-breaking rules requires a new split-algorithm version and explicit founder amendment.

**Status**: Ratified for specification only. Execution not authorized.

---

## D7 — Minimum sizes

Decision: The formal split must contain at least 100 validation examples and at least 100 test examples.

The ratified exact totals of 150 each satisfy these minima.

**Status**: Ratified for specification only. Execution not authorized.

---

## D8 — Holdout policy

Decision: No holdout is created during P01-04 version 1.

Do not:

- reserve undisclosed membership;
- create a founder-only hidden partition;
- store sealed labels;
- imply a holdout exists.

Any later holdout must use a separately authorized policy, sealing protocol, access model, and versioned split contract.

**Status**: Ratified for specification only. Execution not authorized.

---

## D9 — Public repository policy

Decision: The following may be repository-promotable after successful formal execution, acceptance, and separate promotion authorization:

- example identifiers
- source-document identifiers
- row ordinals
- assigned partition names
- group membership
- aggregate label counts
- deterministic split fingerprints
- stable provenance identities

Do not include in public split registries:

- question text
- context text
- long-answer text
- per-example answer labels
- local paths
- usernames
- hostnames
- timestamps
- command logs
- workspace locations

This authorization makes no new source-data license or redistribution claim. All future promotion must remain bounded by the canonical rights-and-provenance record and a fresh promotion review.

**Status**: Ratified for specification only. Execution not authorized.

---

## D10 — Split-version policy

Decision: Only one canonical official split version is permitted initially: `mesc-pilot-01-split-algorithm/1`.

A different official split, seed, ratio, grouping unit, stratification method, or leakage policy requires:

- explicit founder amendment;
- a new algorithm version;
- new formal generation;
- new acceptance;
- no silent replacement of version 1.

**Status**: Ratified for specification only. Execution not authorized.

---

## Implementation Status Appendix

This appendix records implementation and adoption status. It does not amend,
repeal, or reinterpret D1–D10. D1–D10 remain ratified policy as recorded above.

- D1–D10 remain ratified policy; no founder ratification in this appendix.
- P01-04B1 implements only private pure primitives: `PilotSplitAssignment`,
  `PilotSplitManifest`, `PilotSplitNotAuthorizedError`, `SourceDocumentGroupedSplitter` fail-closed,
  `PilotLeakageFinding`, `PilotLeakageAuditReport`, and `_split_v1` private core.
- No partition membership has been generated, disclosed, or promoted.
- Public tooling, artifact builders, leakage-detection library, CLI entry point,
  write-path protections, and end-to-end synthetic qualification remain incomplete.
- B2 recommendations in `specs/mesc-pilot-01/p01-04b2/decision-record.md` were reviewed by independent Opus and ratified by the founder as design decisions FD-B2-1 through FD-B2-8 on 2026-07-24; they do not amend D1–D10.
- Any future B2 implementation or execution authorization requires separate founder authorization and remains nil.
- On conflict between this appendix and D1–D10, D1–D10 control.

Current maintenance context:

This decision record is currently maintained within the broader P01-04
documentation set on canonical baseline
`ce1272235cb48dbacdb18f20e1ae8db695b01328`.

This maintenance context does not alter the original P01-04A ratification
identity, scope, branch, baseline, or decisions D1–D10.

- Implementation adoption does not equal execution authorization.
  P01-04B1 adoption does not authorize real split generation.
  B2 specification does not authorize B2 implementation.
  B2 implementation does not authorize execution.
  Execution authorization requires explicit founder authorization for each stage
  (P01-04B, P01-04C, P01-04D, P01-04E, P01-04F, P01-04G).

### Current controlling closeout — P01-04B acceptance

This section is the current controlling status of the Implementation Status
Appendix. It supersedes the appendix entries above for current status only. It
does not amend, repeal or reinterpret D1–D10, and it records no new founder
ratification of split policy.

```text
P01-04B implementation:
ADOPTED AND ACCEPTED

Canonical acceptance baseline:
d5a6ac1654cabd33b6a795756d2796bceaf1652a

Accepted reviewed head:
e78d1fca2d972cdbcdb7ff78bdf09af4cd03966f

Merged PR:
#83

Real execution:
NOT AUTHORIZED
```

The appendix entries above, and every prior entry recording P01-04B as
incomplete or as `CHANGES REQUIRED / NOT ACCEPTED`, remain truthful historical
snapshots of the baselines they describe. They are preserved unrewritten. They
are superseded for current status by this closeout.

This closeout records tooling acceptance only. D1–D10 remain ratified policy for
specification purposes and were not executed. No real split was generated, no
real partition membership exists, no canonical leakage execution was performed
and no evidence was published. Real split generation, real partition membership,
canonical leakage execution, evidence publication, model access, inference,
retrieval, training and fine-tuning all remain unauthorized, as do P01-04C
through P01-04G. Each remains subject to its own separate founder authorization.

On conflict between this closeout and D1–D10, D1–D10 control.

### Current controlling closeout — P01-04C acceptance

This section is the current controlling status of the Implementation Status
Appendix for P01-04C. It supersedes the entries above for current P01-04C status
only. It does not amend, repeal or reinterpret D1–D10, and it records no new
founder ratification of split policy.

```text
P01-04C qualification implementation:
CANONICALLY ADOPTED

P01-04C synthetic fixture qualification:
ACCEPTED

Canonical acceptance baseline:
b20dbe0000a129f3019d6f7d2895622ce0560069

Accepted reviewed head:
c9cf1cc58b3ff89c39327c328a10308c0a9dbf4d

Merged PR:
#85

Real execution:
NOT AUTHORIZED

P01-04D:
NOT AUTHORIZED
```

D1–D10 remain specification policy only. No real split was generated. No real
partition membership exists. No canonical leakage execution occurred. No real
evidence was published.

The accepted P01-04C qualification exercised deterministic synthetic fixtures
against the private fixture-only tooling. It did not execute D1–D10 against the
real dataset, and no part of it constitutes a real split, a real partition
assignment or a canonical leakage audit. Real split generation, real partition
membership, canonical leakage execution, evidence publication, model access,
inference, retrieval, training and fine-tuning all remain unauthorized, as do
P01-04D through P01-04G. Each remains subject to its own separate founder
authorization.

On conflict between this closeout and D1–D10, D1–D10 control.

---

## Implementation and Readiness Appendix — P01-04D entry-readiness remediation

This appendix records founder decisions `FD-DREADY-1` through `FD-DREADY-12`,
issued on 2026-08-04 as **design and contract authority only**.

```text
FD-DREADY-1 THROUGH FD-DREADY-12:
ISSUED ON 2026-08-04

Decision class:
DESIGN AND CONTRACT AUTHORITY ONLY

P01-04D implementation authority:
NOT ISSUED

P01-04D execution authority:
NOT ISSUED
```

### This appendix does not amend D1–D10

```text
D1 partition set                          UNCHANGED
D2 exact 700 / 150 / 150 totals           UNCHANGED
D3 source_document_id grouping            UNCHANGED
D4 decision stratification                UNCHANGED
D5 constrained integer apportionment      UNCHANGED
D6 deterministic SHA-256 ranking          UNCHANGED
D7 minimum sizes                          UNCHANGED
D8 no holdout                             UNCHANGED
D9 public repository content boundary     UNCHANGED
D10 split-version policy                  UNCHANGED
```

No text of D1 through D10 is edited, repealed or reinterpreted by this appendix.
Scientific identity is unchanged. Only operator and artifact-contract ambiguity
is reconciled.

On conflict between this appendix and D1–D10, **D1–D10 control**.

### The two readiness blockers resolved at design level

The founder-authorized P01-04D entry-readiness review completed with the verdict
**NOT READY** on two blocking findings:

```text
B-1:
No controlled formal operator invocation path exists for Generation A and
Generation B.

B-2:
The P01-04A/E policy artifact inventory is not reconciled with the accepted
fixture-only implementation inventory.
```

```text
B-1 resolved at design level by:
FD-DREADY-2, FD-DREADY-3, FD-DREADY-4, FD-DREADY-5

B-2 resolved at design level by:
FD-DREADY-6, FD-DREADY-7, FD-DREADY-8, FD-DREADY-9, FD-DREADY-10
```

Design-level resolution of a readiness blocker is not entry, not implementation
authority and not execution authority.

### FD-DREADY decision summary

```text
FD-DREADY-1   scope and authority — design and contracts only
FD-DREADY-2   a separate private formal executor; fixture-only tooling
              untouched and never reused for formal execution
FD-DREADY-3   one controlled operator surface; exactly two commands
FD-DREADY-4   one generation per invocation; explicit inputs;
              fail-closed rejections
FD-DREADY-5   comparison boundary; any inequality invalidates both
              candidates
FD-DREADY-6   the exact seven-file P01-04D generation inventory
FD-DREADY-7   the artifact-name supersession map
FD-DREADY-8   stage separation across P01-04D, E, F and G
FD-DREADY-9   deterministic, date-free formal policy snapshot
FD-DREADY-10  non-circular, identity-free formal generation manifest
FD-DREADY-11  future implementation boundary — synthetic only
FD-DREADY-12  D1 through D10 preserved unchanged
```

The exact meaning of each identifier is carried by
[`../p01-04d-entry-readiness-remediation/founder-authorization.md`](../p01-04d-entry-readiness-remediation/founder-authorization.md),
which controls. No identifier beyond `FD-DREADY-12` exists.

### Reconciled operator and artifact contracts

```text
formal operator script:
scripts/mesc_p01_04d_operator.py

operator commands:
generate
compare

P01-04D artifact count:
7

P01-04D artifact filenames:
split-policy.json
group-registry.jsonl
example-registry.jsonl
excluded-ledger.json
split-summary-identity-core.json
split-summary.json
generation-manifest.json

standalone fingerprint file:
none

P01-04E audit filename:
leakage-audit.json

P01-04F closeout filename:
p01-04-closeout-record.json

fixture manifest:
publication-manifest.json

formal D manifest:
generation-manifest.json
```

Superseded names:

```text
example-split-registry.jsonl       ->  example-registry.jsonl
excluded-or-unassigned-ledger.json ->  excluded-ledger.json
split-fingerprint.json             ->  no standalone file
```

The authoritative full lowercase 64-hex `split_fingerprint` is carried and
verified through `split-summary.json` and `generation-manifest.json`. The 16-hex
`split_hash` is compatibility/display-only.

### This appendix authorizes nothing

At the FD-DREADY design-only baseline of 2026-08-04, the state was as recorded
below. The block is preserved unrewritten as historical evidence of what this
appendix issued and withheld; it is not the current governing status. Its
`P01-04D entry` and `P01-04D implementation` lines have since been superseded
by later, separate founder and adoption decisions, and current status is
recorded in **Current controlling status — P01-04D pre-execution governance**
at the end of this document. Every other line in the block remains in force.

```text
P01-04D entry:
NOT AUTHORIZED

P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-03G registry access:
NOT AUTHORIZED

External source-record access:
NOT AUTHORIZED

Real dataset access:
NOT AUTHORIZED

Real split generation:
NOT AUTHORIZED

Real partition membership:
NOT AUTHORIZED

Canonical leakage execution:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

At the FD-DREADY design-only baseline: no formal executor was implemented, no
operator script was created, no generation workspace was created, no split
artifact was generated, no partition membership was calculated, no leakage
check was executed, no P01-03G registry content was accessed and no real
dataset was accessed. Every one of the six prospective implementation paths was
absent or unchanged at that baseline.

That paragraph describes the FD-DREADY design-only baseline and is preserved
for it. The six implementation paths were subsequently authorized, implemented
and canonically adopted through PR #90. No protected input has been opened, no
generation workspace has been created and no artifact has been generated at any
point since.

---

### Current controlling status — P01-04D pre-execution governance

This section is the current controlling status of the P01-04D appendices above.
It supersedes their `P01-04D entry` and `P01-04D implementation` lines for
current status only, and preserves every historical statement for the baseline
it describes.

```text
formal executor implementation:
CANONICALLY ADOPTED THROUGH PR #90

formal-executor adoption truth:
CANONICALLY RECONCILED THROUGH PR #91

founder P01-04D entry authorization:
ISSUED AND CANONICALLY ADOPTED THROUGH PR #92

P01-04D entry:
AUTHORIZED

P01-04D control state:
ENTERED — PRE-EXECUTION GOVERNANCE ONLY

P01-04D execution:
NOT AUTHORIZED

P01-03G registry content access:
NOT AUTHORIZED

external real source-record access:
NOT AUTHORIZED

real dataset access:
NOT AUTHORIZED

Generation A:
NOT AUTHORIZED

Generation B:
NOT AUTHORIZED

compare:
NOT AUTHORIZED

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED

current next gate:
P01-04D EXECUTION-AUTHORIZATION READINESS RE-EVALUATION
```

The current readiness disposition is
`NOT READY FOR FOUNDER P01-04D EXECUTION-AUTHORIZATION DISPOSITION`, and it
remains so until the present current-truth reconciliation is independently
reviewed, canonically adopted and the readiness gate is rerun.

Entry is not execution. No protected input has been opened, no generation
workspace has been created, neither `generate` nor `compare` has been invoked,
neither Generation A nor Generation B has occurred, no partition membership
exists, no canonical leakage execution has been performed and no evidence has
been published.

**This section does not amend D1 through D10.** It records implementation,
adoption and authorization status only. It alters no partition set, target
count, grouping key, stratification field, apportionment rule, ranking
contract, minimum size, holdout policy, repository-content boundary or
split-version policy, and it does not amend `FD-DREADY-1` through
`FD-DREADY-12`. On any conflict between this section and D1–D10, D1–D10
control.
