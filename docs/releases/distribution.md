# Distribution Strategy

- **Status:** Strategy (ADR-0010, Proposed)
- **Date:** 2026-07-10
- **Related:** [distribution_hf.md](../architecture/distribution_hf.md) (identity record),
  [ADR-0003](../adr/0003-repository-topology.md)

## Direction of truth

```
GitHub  ──►  CI  ──►  GitHub Releases  ──►  Hugging Face  ──►  Users
```

**Never the reverse.** Concretely:

- No artifact originates on HF; every HF repo mirrors a GitHub Release tag.
- No editing on HF: card fixes are commits in GitHub, re-mirrored by CI.
- Drift detection: each HF repo's card records the source tag + manifest hash; a
  mismatch is a defect to fix from the GitHub side.
- If HF disappeared tomorrow, nothing of record would be lost — that is the test.

## GitHub Releases

| Element | Policy |
|---|---|
| Tags | `vX.Y.Z` (package), `<artifact>-vX.Y` (models/datasets/benchmarks) |
| Release notes | CHANGELOG excerpt + manifest attached + evidence links |
| Assets | Wheels/sdists; dataset snapshots (or pointers when large); manifests always |
| Immutability | Tags are never moved; releases never edited after publication (typo fixes go in a follow-up note) |

## The MedScaleAI Hugging Face organization

Accounts: user `MedScale` (placeholder Space holder), org **`MedScaleAI`** (all
artifacts). Why the org owns artifacts: organizational continuity and collections.

### Expected evolution (nothing created before its gate)

```
MedScaleAI/
├── Models
│   ├── mesc-fhir-v0.1            (T6+)
│   └── mesc-evidence-v0.1        (H2)
├── Datasets
│   ├── medscale-litdb            (end of T1)
│   ├── medscale-bench-data       (T3)
│   └── medscale-fhir-synthetic   (T5)
├── Spaces
│   ├── evidence-explorer         (post litdb v1)
│   ├── benchmark-viewer          (post Bench v0 + baselines)
│   └── medscale-demo             (post MESC-v0)
└── Collections
    └── one per release train (e.g. "MedScale v0: Bench + MESC-v0 + data")
```

### Naming conventions

- Repos: `lowercase-kebab`; models carry family + task (`mesc-fhir`); datasets carry
  the `medscale-` prefix; versions live in card metadata + GitHub tags, **not** in the
  repo name (HF repos accumulate revisions; each mirrored release is a tagged HF revision).
- Why family-first model names: users discover by task; `mesc-fhir` says what it does,
  and the card says what it is built on.

### Required metadata (every HF repo)

| Field | Requirement |
|---|---|
| `license` | SPDX id matching [licensing.md](licensing.md) |
| `tags` | `medical`, `verifiable-ai`, plus class tags: `fhir`, `synthetic-data`, `clinical-nlp` as applicable, `not-for-clinical-use` |
| `base_model` (models) | Exact base id + revision |
| Source pointer | GitHub repo + release tag + manifest hash — mandatory card section |
| Cards | Per [model_cards.md](model_cards.md) / [dataset_cards.md](dataset_cards.md) |

### README/card floor (every HF repo)

Identity paragraph (infrastructure, not a chatbot) · what this artifact is and is not ·
not-for-clinical-use statement · synthetic/PHI-free statement · version + source tag ·
licence · citation block (from CITATION.cff) · reproduction pointer.

### Space policy

Spaces demonstrate **released** artifacts only; pin exact versions; collect no user
data; carry the disclaimer; their source lives in GitHub. A Space is a window, never
the product.

## PyPI

`medscale` publishes to PyPI from v0.2 (first externally useful surface). Trusted
publishing (OIDC) from CI only — no local twine uploads, no long-lived tokens.
