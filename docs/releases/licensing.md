# Licensing Strategy

- **Status:** Strategy (ADR-0011, Proposed)
- **Date:** 2026-07-10
- **Related:** Rule R3, [governance rules](../governance/rules.md), ADR-0006 (model tiers),
  `data/litdb/LICENSE.md` (live example of field-level review)

Platform invariant (Vision §8): everything MedScale ships must permit **derivative
works + commercial use**, so Afia and anyone else can build on it. This document maps
that invariant onto every artifact class.

## The matrix

| Artifact | Licence | Reasoning |
|---|---|---|
| Code (`medscale`, scorers, adapters) | **Apache-2.0** (LICENSE in repo) | Permissive + patent grant; the platform promise |
| Documentation, ADRs, guides | Apache-2.0 (repo-wide single licence) | One licence per repo avoids boundary disputes; docs are part of the engineered artifact |
| Model **adapters** (MESC family) | Apache-2.0, released only over Tier-1 bases | Adapter weights are MedScale-authored; Tier-1 bases impose no passthrough (ADR-0006) |
| `medscale-base-ref` (config release) | Apache-2.0 (it is config + docs, no third-party weights) | — |
| MedGemma derivatives | **Not released** unless a dedicated Accepted ADR accepts HAI-DEF passthrough | Passthrough would narrow the platform promise silently (ADR-0006) |
| BioMistral derivatives | Eligible (Apache-2.0 base = Tier 1); still subject to model checklist | — |
| Synthetic data (Synthea-derived, fixtures) | **CC-BY-4.0** for published datasets | Data ≠ code: CC-BY is the standard, citable data licence; Synthea (Apache-2.0) output carries no restriction |
| Generated data (Tier-1 model outputs in datasets) | Folded into the dataset's CC-BY-4.0; generating model + revision recorded in provenance | Output-terms risk is why only Tier-1 models may generate training/benchmark data |
| LitDB export | **Composite, field-level**: CC0 fields (OpenAlex) pass through; S2-derived fields carry ODC-BY attribution; PubMed abstracts **excluded** from exports | Mixed upstream terms cannot be blanket-licensed; the per-field table ships in the dataset's LICENSE.md |
| Benchmark (spec + scorers + data) | Code Apache-2.0; data CC-BY-4.0 | Standard split for executable benchmarks |
| Papers/preprints | Venue terms; preprints CC-BY-4.0 where the venue allows | — |
| External runtime dependencies | Permissive-only (Apache/MIT/BSD/PSF class); checked at adoption | Currently zero runtime deps; the rule guards the future |
| OpenMed adapter extra | OpenMed is Apache-2.0 → no constraint; pinned revisions recorded | ADR-0007 |

## Inheritance rules

1. **Base → adapter:** released adapters inherit no restriction only because bases are
   Tier-1; that is why the tier system exists. Evaluation-only use of Tier-2 models
   imposes nothing on consumers.
2. **Data source → dataset:** the most restrictive contributing field governs that
   field: pass through (CC0), attribute (ODC-BY), or exclude (PubMed abstracts, SNOMED
   — never vendored, RQ7).
3. **Dataset → model:** training data terms must permit model training + redistribution
   of the resulting weights; recorded per-source in the training manifest.
4. **Apache-2.0 compatibility check** for anything vendored into the repo: Apache-2.0,
   MIT, BSD, CC0 in; GPL/AGPL, research-only, no-derivatives out.

## Citation requirements

- Repo: `CITATION.cff` (exists) — kept current with releases.
- Each dataset/model card carries a BibTeX/CFF block; papers cite artifact versions
  (e.g. `medscale-bench-v1.0`), never "latest".
- Upstream attribution honored where required (S2 ODC-BY; base models per their terms;
  Synthea cited as generator).
- Inbound: MedScale cites per Rule R1 — litdb-verified identifiers only.
