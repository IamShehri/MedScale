# MESC Pilot-01 — P01-04 Specification

Status: **specification and policy only — no execution authorized**

---

## Scientific objective

P01-04 exists to produce:

1. A deterministic grouped train/validation/test split manifest, where every source-document group is assigned as a complete unit to exactly one partition.
2. A leakage audit report documenting exact and normalized question leakage, source-document overlap, and near-duplicate findings.
3. A frozen split hash that is byte-reproducible from the input registries.
4. Responsibility and acceptance records documenting the operation was generated under explicit authorization with provenance preserved.

P01-04 does not authorize benchmark execution, model evaluation, or gold-subset creation.

## Grouping invariant

The canonical indivisible grouping unit is `source_document_id`.

All examples belonging to one `source_document_id` must remain in the same partition.

The accepted current P01-03G registry contains:

- 1,000 examples;
- 1,000 source documents;
- zero source documents containing more than one example;
- maximum group size of one.

Therefore, source-document grouping is currently structurally vacuous — it cannot produce cross-partition group memberships because every group is a singleton. The policy must acknowledge this limitation explicitly. P01-04 must not claim that this invariant alone rules out question-level or context-level leakage.

## Exact counts

For the accepted 1,000-example PubMedQA dataset, the formal split must contain exactly:

- 700 train examples
- 150 validation examples
- 150 test examples

Total: 1,000 examples.

## Stratification policy

The canonical stratification field is `decision`.

Canonical strata are: `yes`, `no`, `maybe`.

Current dataset distribution:

- `yes`: 552 examples
- `no`: 338 examples
- `maybe`: 110 examples

Stratification is applied to group allocation. It must never split a source-document group.

## Determinism contract

No pseudorandom generator is used.

Within each decision stratum, complete groups are ranked by ascending SHA-256 digest of canonical UTF-8 bytes representing:

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
- UTF-8 encoding;
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

The seed is a domain-separation value, not an RNG seed. Changing any of: seed, algorithm version, grouping unit, ratios, stratifier, normalization, or tie-breaking rules requires a new split-algorithm version and explicit founder amendment.

## Leakage taxonomy

P01-04 must distinguish between different evidence strengths:

1. **Exact example identity** — no `original_example_id` may appear in more than one partition.
2. **Source-document identity** — no `source_document_id` may appear in more than one partition.
3. **Exact raw-question equality** — byte- or code-point-exact equality of question text across different partitions.
4. **Normalized-question equality** — equality after Unicode NFKC normalization, case folding, and whitespace collapse.
5. **Near-duplicate question detection** — token-set Jaccard similarity >= 0.90 across partitions.
6. **Context equality and overlap** — exact normalized context-segment equality and complete context-list equality.
7. **Semantic similarity** — deferred; P01-04 version 1 must not claim all semantic leakage was ruled out.

## Minimum sizes

The formal split must contain at least:

- 100 validation examples
- 100 test examples

The ratified exact totals of 150 each satisfy these minima.

## Integer apportionment

The split policy must produce:

- exact row totals of 700 / 150 / 150
- integer label counts
- minimum deviation from ideal 70/15/15 label proportions

Deterministic constrained-apportionment algorithm:

1. Compute the ideal real-valued class-by-partition matrix.
2. Enumerate or derive valid integer matrices satisfying:
   - every class total exactly;
   - every partition total exactly.
3. Minimize the sum of squared deviations from the ideal matrix.
4. Break ties by lexicographically comparing the integer vector in this order:
   - label order: `yes`, `no`, `maybe`
   - partition order: `train`, `validation`, `test`

Expected target matrix for the current 1,000-example dataset:

| Decision | Train | Validation | Test | Total |
| -------- | ----: | ---------: | ---: | ----: |
| yes      |   386 |         83 |   83 |   552 |
| no       |   237 |         50 |   51 |   338 |
| maybe    |    77 |         17 |   16 |   110 |
| total    |   700 |        150 |  150 |  1000 |

These are aggregate policy targets only. Do not calculate or disclose example membership during P01-04A.

## Rights and provenance boundary

The upstream dataset is `qiaojin/PubMedQA` under MIT package rules. Split registries contain only identifiers (`example_id`, `source_document_id`, `row_ordinal`, `assigned_split`). They do not include raw question text, context, or labels. Commit is scientifically acceptable: public repository storage does not redistribute upstream content; it records membership in identifiers only.

Open risk: if any future partition membership artifact accidentally includes `question` or `answer` text, rights review must be re-evaluated before promotion.

## Exclusions and limitations

P01-04 does not cover:

- benchmark execution;
- model evaluation;
- gold-subset creation;
- semantic duplicate detection beyond token-set Jaccard 0.90;
- holdout creation or management;
- P01-05 or any later Pilot-01 phase.

P01-04A does not authorize any of the above.
