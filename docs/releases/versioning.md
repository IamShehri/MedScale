# Versioning

- **Status:** Strategy (ADR-0011, Proposed)
- **Date:** 2026-07-10

One rule everywhere: **a version identifies immutable content.** Anything changed is a
new version. Content hashes (`medscale.reproducibility.content_hash`) back identity
checks wherever the artifact is data.

## Per-class schemes

| Class | Scheme | MAJOR means | MINOR means | PATCH means |
|---|---|---|---|---|
| Python package | SemVer `X.Y.Z` | Breaking API | Additive API | Fixes only |
| Models | `vX.Y` | Base model, objective, or task-definition change (scores not comparable) | Retrain: new data snapshot/seeds/hyperparams, same task + base | — (no silent weight patches; any weight change is at least MINOR) |
| Datasets | `vX.Y` | Schema or generation change breaking comparability | Additive rows/fields, same schema | — |
| Benchmarks | `vX.Y` | Task or metric definition change → **new leaderboard** | Additive tasks/slices; existing scores stay valid | — |
| Evidence/knowledge/FHIR schemas | Integer `1, 2, …` (append-only, ADR-0009) | Any non-optional change | — | — |
| Documentation | Repo git history + release tags snapshot the docs | — | — | — |
| ADRs | Immutable once Accepted; changes = new ADR with `Supersedes:` header | — | — | — |

**Why models/datasets/benchmarks drop PATCH:** a "patch" to data or weights silently
changes results; forcing MINOR makes every content change visible in citations.

## Package pre-1.0 policy

`0.Y.Z`: MINOR may break API (recorded in CHANGELOG under "Changed/Removed"); PATCH
never does. **1.0.0 criterion** (not a date): MESC-v0 evaluated + MedScale-Bench v0
public + litdb v1 exported — the platform's core promise demonstrated end to end.

## Version sources (single-sourced, no drift)

| Class | Source of the number |
|---|---|
| Package | `src/medscale/__about__.py` (already wired to hatch) |
| Git tags | Package: `vX.Y.Z`; other artifacts: `<artifact>-vX.Y` (e.g. `medscale-bench-v1.0`, `mesc-fhir-v0.1`, `litdb-v1.0`) |
| Datasets/models | The tag + the release manifest; HF repo carries the same version in card metadata |
| Schemas | The `schema_version` field in the objects themselves |

**Why per-artifact tags in one repo:** MedScale is a single-repo program (ADR-0004);
prefixed tags give each artifact class an independent release cadence without
splitting the repository.

## Cross-version compatibility statements

Every model release names the benchmark version it was evaluated on; every benchmark
MAJOR bump states explicitly that prior scores are incomparable; every dataset release
names its schema integer. A release manifest missing any of these fails validation
([reproducibility.md](reproducibility.md)).
