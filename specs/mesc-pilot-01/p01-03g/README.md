# P01-03G Handoff Package

## Purpose

P01-03G is the MESC Pilot-01 validated handoff package for the PubMedQA-based evidence freeze generated from accepted P01-03E transformation and P01-03F validation results. This package contains only the accepted portability artifacts required to advance Pilot-01. It does not start P01-04, assign splits, or claim leak-free or benchmark-ready status.

## Package Inventory

This directory contains:

- `transformed-dataset-identity.json` — canonical identity for the accepted transformed dataset
- `dataset-fingerprint.json` — version `mesc-pubmedqa-dataset-fingerprint/2` payload with deterministic recomputable SHA-256
- `schema-version.json` — declared schema version
- `transformation-version.json` — declared transformation version
- `validation-report-reference.json` — accepted P01-03F validation summary reference
- `ordered-example-id-registry.jsonl` — compact JSONL registry with row-ordinal-ordered example IDs
- `source-document-id-registry.jsonl` — compact JSONL registry grouped by source document
- `excluded-record-ledger.json` — explicit exclusion ledger
- `rights-and-provenance-record.json` — provenance boundary and third-party dataset attribution
- `p01-04-responsibility-acknowledgment.json` — boundary acknowledgment for P01-04 scope
- `p01-03-closeout-record.json` — accepted history and closeout record

## Artifact Schemas

Each JSON artifact declares its schema version in a top-level identifier field. The registries use compact JSONL with one JSON object per line. No headers, comments, or blank lines are present.

## Ordered Registry Contract

`ordered-example-id-registry.jsonl` contains exactly 1,000 accepted example rows. Row ordinals are integers `0..999`, strictly increasing by 1, with no duplicate ordinals. Example IDs are unique across the registry.

## Source-Document Registry Contract

`source-document-id-registry.jsonl` groups accepted rows by `source_document_id`. Group order follows ascending minimum row ordinal. Within each group, row-ordinal arrays are numerically ascending. No fabricated grouping fields are included.

## Dataset Fingerprint v2 Algorithm

`dataset-fingerprint.json` uses schema `mesc-pubmedqa-dataset-fingerprint/2`. The logical payload is a canonical JSON object encoding SHA-256 identities and byte sizes for:

- raw artifact
- source records
- source-record registry
- transformation manifest
- transformation local-run record

Canonical serialization uses recursive key sorting, UTF-8, `ensure_ascii=False`, `allow_nan=False`, separators `(",", ":")`, no indentation, no BOM, and no terminal newline. The fingerprint payload identity is separate from the presentation-file bytes identity.

## Stable Identity-Reference Model

All cross-artifact references use SHA-256 and byte size rather than mutable local paths. Promotable artifacts are byte-immutable from frozen upstream inputs and frozen V3 evidence. Any requested change requires a separately authorized candidate.

## Provenance Boundary

This package is derived from:

- upstream dataset: `qiaojin/PubMedQA` at revision `9001f2853fb87cab8d220904e0de81ac6973b318`
- accepted transformation: P01-03E Attempt-2 bundle
- accepted validation: P01-03F Invocation 2

This package does not create or claim any license grant, redistribution right, or ownership interest in the upstream dataset beyond truthful attribution recorded in `rights-and-provenance-record.json`.

## Exclusion-Ledger Interpretation

`excluded-record-ledger.json` records zero exclusions for the accepted pass. The zero count is proven through explicit reconciliation of accepted counts. Absent metrics are marked `not_recorded` when the countable evidence does not establish a value.

## Historical Chain

- **V1:** initial local candidate requiring correction; superseded.
- **V2:** invalidated by an evidence-integrity incident; must never be promoted.
- **V3:** independently regenerated from accepted P01-03E Attempt-2 and P01-03F Invocation 2 evidence; passed write-once freeze and separate forensic acceptance review.

This package does not repair, restore, or overwrite V2 evidence.

## P01-04 Responsibility Boundary

P01-04 is **not authorized** and **not started**. Split assignment, leakage audit, benchmark execution, and model evaluation are explicitly reserved for separate P01-04 authorization. The `p01-04-responsibility-acknowledgment.json` artifact records this boundary and does not imply execution or completion of P01-04 duties.

## Large JSONL Registries

The large JSONL registry files are handoff metadata and split-assignment-free zone. They define accepted dataset membership and document provenance, not train, validation, test, or holdout partitions.

## Promotion Notes

This README is the only new explanatory document authorized in this package for repository promotion. Repository promotion of P01-03G does not complete or authorize P01-04. Any future promotion or further governance change requires separate founder authorization.
