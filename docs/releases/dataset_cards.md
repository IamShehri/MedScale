# Dataset Card Requirements

- **Status:** Strategy (ADR-0010, Proposed)
- **Date:** 2026-07-10

A dataset card answers three questions with evidence: *where did every field come
from, what may you do with it, and how do you rebuild it byte-for-byte.*

## Required sections

### 1. Identity

Name + version (`medscale-litdb-v1.0`), release date, GitHub tag, content hash of the
canonical export, size (records/bytes), schema version.

### 2. Provenance

- **Literature-derived** (litdb): source APIs, query-set commit SHA
  (search_strategy), run manifests, PRISMA counts per stage (identified → included),
  screening log reference. Every record carries a resolvable identifier +
  `verified_at` + `source_api` (R1).
- **Synthetic** (bench/FHIR data): generator + version + seed + config hash; corruption
  taxonomy and sampling parameters; validator version + SHA-256 used for labels.
- **PHI statement (every card):** "This dataset contains no real patient data. It is
  synthetic and/or bibliographic-metadata only." (R2)

### 3. Schema & metadata model

Field table: name, type, source, licence class per field. For litdb: the litdb schema
(identifiers, tier, screening state, evidence objects with verification states). For
bench data: task format, split definitions, and the split content hashes used by the
contamination assertion.

### 4. Licensing (field-level where composite)

Per [licensing.md](licensing.md): blanket CC-BY-4.0 for wholly-synthetic data; the
field-level table for composite sources (CC0 pass-through, ODC-BY attribution,
exclusions named — e.g. PubMed abstracts). What the consumer may do is stated in one
sentence per class.

### 5. Validation

The validation pipeline run and its output: schema check green, licence check green,
contamination assertion green (where splits exist), record counts matching manifests.

### 6. Versioning & immutability

This version's diff vs prior (added/removed/changed and why); statement that the
snapshot is immutable; DOI (Zenodo) once paper-cited.

### 7. Known limitations

Honest gaps: English-only queries; source-API coverage bias; screening is
single-operator (stated, per PRISMA reporting norms); synthetic data's external
validity limit.

### 8. Reproduction & citation

Rebuild instructions (frozen queries → archives → parse → screen → export, or
`medscale data build --seed S` once it exists); CFF/BibTeX block.

## HF metadata block

`license` (or per-config licences), `tags` (`medical`, `synthetic-data` /
`bibliographic`, `verifiable-ai`), `size_categories`, `source_datasets` where
applicable, and the GitHub source tag in the card body.
