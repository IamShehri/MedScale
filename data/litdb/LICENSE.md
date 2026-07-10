# data/litdb — Licence and Terms Record (Rule R3)

- **Created:** 2026-07-10 (before the first archived byte, per search_strategy §4)
- **Contents:** raw bibliographic API responses (audit archives), run manifests, and the
  PRISMA screening log. **No PHI. No clinical data. Metadata and abstracts only.**
- **DUA:** none.

## Per-source terms (verified 2026-07-10)

| Source | Terms read from | Metadata licence | Redistribution note |
|---|---|---|---|
| OpenAlex | https://openalex.org/about (API docs) | **CC0** | Freely redistributable, incl. commercial and derivative use. |
| Semantic Scholar | https://www.semanticscholar.org/product/api (API terms; S2AG under ODC-BY) | ODC-BY-style attribution | Redistribute with attribution to Semantic Scholar. |
| PubMed / NCBI E-utilities | https://www.ncbi.nlm.nih.gov/home/about/policies/ | US-gov works; **per-record abstracts may carry publisher copyright** | Archives kept as research audit artifacts; bulk redistribution of abstracts is not claimed. Derived litdb records store identifiers + metadata fields. |
| arXiv API | https://info.arxiv.org/help/api/tou.html | Metadata redistribution permitted | Atom responses archived verbatim; paper full texts are NOT stored here. |

## Platform invariant

Everything MedScale *ships as a dataset* must permit derivative + commercial use (R3).
Raw archives in `raw/` are **audit artifacts** supporting reproducibility (R1/R7), not a
published dataset; any future published litdb export will carry its own licence file and
will exclude fields whose source terms do not permit redistribution (e.g. PubMed
abstracts), keeping identifiers + provenance which are always reproducible from source.
