# MESC Pilot-01 — P01-04 Decision Record

Status: **specification and policy only — no execution authorized**

This record contains founder policy decisions for P01-04 split and leakage auditing. Implementation and execution decisions are not marked complete; they remain pending separate authorization.

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
| -------- | ----: | ---------: | ---: | ----: |
| yes      |   386 |         83 |   83 |   552 |
| no       |   237 |         50 |   51 |   338 |
| maybe    |    77 |         17 |   16 |   110 |
| total    |   700 |        150 |  150 |  1000 |

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
