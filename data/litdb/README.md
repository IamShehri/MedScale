# data/litdb

The literature database's on-disk artifacts. Governed by
[`docs/execution/search_strategy.md`](../../docs/execution/search_strategy.md) and
[`LICENSE.md`](LICENSE.md) (Rule R3).

```
data/litdb/
├── LICENSE.md            # R3 terms record — precedes all data
├── raw/                  # verbatim API responses: <source>/<query-id>/<run-id>.json
├── manifests/            # one canonical-JSON manifest per ingestion round
└── screening/            # append-only PRISMA decision log (screening_log.jsonl)
```

**What this corpus is (and is not).** litdb round 1 is MedScale's
**methods/related-work corpus** — AI, NLP, FHIR, and evaluation literature backing
MedScale's own research questions and papers (R1 citations). It is **not** a
clinical-evidence corpus: PICO-shaped evidence objects (ADR-0009) target clinical
studies, which these queries deliberately do not retrieve. A separate
**clinical-evidence corpus** (clinical PubMed queries, trial registries) will be
ingested through the same machinery when its round is approved — two scientific
objects, one infrastructure (scientific review S5).

**Storage policy (ADR-0016, Accepted Option A):** archives live in-repo, field-trimmed
at request time, capped per round. Tripwire: if `data/` exceeds **~75 MB**, storage
policy is revisited via a superseding ADR before any further round runs.

Rules of the directory:

- Nothing lands in `raw/` except through `medscale.litdb.ingest.archive_retrieval`
  (payload verbatim, SHA-256 recorded in the round's manifest).
- Manifests cite the git SHA of the frozen query set they executed.
- The screening log is append-only; states are replayed through the PRISMA state
  machine, never edited in place.
