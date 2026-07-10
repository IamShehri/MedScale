# Model Card Schema

- **Status:** Schema definition (formalizes [model card requirements](../../releases/model_cards.md);
  consumed by future card-lint CI and `medscale.registry`)
- **Date:** 2026-07-10
- **Schema version:** `1` (append-only; changes require an ADR referencing this file)
- **Related:** [model registry](../model_registry.md), [releases/model_cards.md](../../releases/model_cards.md),
  [ci_cd.md](../../releases/ci_cd.md)

This is the machine-checkable field schema behind the model-card *requirements* document.
The prose document says *why* each section exists; this says *what fields must be present
and valid*, so `validate-model` CI can fail a release whose card is incomplete. A card is
a verification document — a field asserting capability without a linked result artifact is
invalid, not merely thin.

## Fields

| Field | Type | Required | Constraint |
|---|---|---|---|
| `schema_version` | string | yes | `"1"` |
| `name` | string | yes | non-empty |
| `version` | string | yes | matches the release tag (`mesc-fhir-v0.1`) |
| `released_at` | string | yes | timezone-aware ISO-8601 |
| `git_sha` | string | yes | 7–40 hex; matches the source tag |
| `manifest_sha256` | string | yes | 64 hex; the release manifest hash |
| `description` | string | yes | one honest sentence; no superlatives |
| `mandatory_statements` | object | yes | both statements below, **verbatim** |
| `base_model` | object | yes | `{id, revision, licence, tier}`; resolves to a Tier-1 generative registry row (or a licence-ADR reference) |
| `adapter` | object | yes | `{method: "qlora", config_hash}` for adapter releases |
| `training_data` | array | yes | each: `{dataset, version, content_sha256, licence}`; synthetic-only |
| `contamination_assertion` | object | yes | `{passed: true, evidence_path}` |
| `evaluation` | array | yes | each: `{benchmark, benchmark_version, metric, seeds:>=3, mean, ci95}` |
| `deltas` | object | yes | `{constraint_delta, prompting_delta}` reported separately |
| `limitations` | array | yes | incl. English/synthetic-only + unmeasured real-clinical transfer |
| `licence` | string | yes | SPDX; Apache-2.0 for adapters over Tier-1 bases |
| `reproduction` | object | yes | `{commands, expected_outputs_path}` |
| `citation` | string | yes | CFF/BibTeX block |
| `secondary_metrics` | array | no | if present, each `labeled_secondary: true`; **no LLM-judge metric may appear as primary** |

## Mandatory statements (verbatim — byte-checked by CI)

```
Not a medical device. This model must not be used for diagnosis, treatment, triage, or
any clinical decision-making.

Synthetic data only. This model was trained and evaluated exclusively on synthetic data.
Its behavior on real clinical data is unmeasured, by policy (one-way PHI boundary).
```

## Validation rules (for card-lint)

1. Every required field present and type-valid.
2. Both mandatory statements present byte-exact.
3. `base_model` resolves to a registry row; tier/role consistent (generative; Tier 1 or a
   licence ADR is referenced).
4. Every `evaluation` entry names a `benchmark_version` and carries ≥3 seeds with a CI.
5. No primary/`model-index` metric is an LLM-as-judge score.
6. `git_sha`/`manifest_sha256` match the tagged release.
7. `training_data` licences all permit derivative + commercial use (R3).

A dataset-card schema will follow the same pattern when the first dataset release (litdb
v1) needs it; it is deferred until then (no speculative schema).
