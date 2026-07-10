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

Rules of the directory:

- Nothing lands in `raw/` except through `medscale.litdb.ingest.archive_retrieval`
  (payload verbatim, SHA-256 recorded in the round's manifest).
- Manifests cite the git SHA of the frozen query set they executed.
- The screening log is append-only; states are replayed through the PRISMA state
  machine, never edited in place.
