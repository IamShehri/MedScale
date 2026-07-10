# Release Reproducibility — The Manifest

- **Status:** Strategy (ADR-0010, Proposed)
- **Date:** 2026-07-10
- **Related:** [reproducibility policy](../research/reproducibility_policy.md) (the
  binding science policy this operationalizes for *published* artifacts)

Every published artifact — package, model, dataset, benchmark, Space, replication
package — carries a **release manifest**. The manifest is the artifact's birth
certificate: without it, the artifact does not ship.

## Required fields (all artifact classes)

| Field | Content | Why |
|---|---|---|
| `artifact` | Name + class + version | Identity |
| `git_sha` | Full commit SHA of the source tag | Traceability to the source of truth |
| `built_at` | Timezone-aware ISO-8601 build timestamp | Audit |
| `python` | Exact interpreter version | Environment |
| `lock_hash` | SHA-256 of `uv.lock` at the tag | Dependency state without shipping the file twice |
| `tool_versions` | ruff, mypy, pytest, uv (+ validator version + SHA-256 when T2 exists) | Gate context; the validator is ground truth and must be pinned |
| `seeds` | Every seed used (build, train, eval) | Determinism (no implicit seeds — policy P1) |
| `dataset_snapshots` | Name + version + content hash of every dataset consumed | Contamination + provenance chain |
| `evaluation_manifest` | Bench version + scorer version + per-seed results paths | Scores are functions of these |
| `environment` | OS class, GPU (if any), peak VRAM for GPU runs | Bounded nondeterminism disclosure (policy P2) |
| `reproduction` | Exact commands + expected-output pointers | The stranger test |

Format: canonical JSON (`medscale.reproducibility.canonical_json`), LF-terminated,
attached to the GitHub Release and referenced by hash in HF cards. The schema will be
implemented as a typed `medscale` structure **when the first release needs it**
(deliberately not now — no speculative implementation).

## Class-specific additions

- **Models:** training manifest (data hashes, config hash, adapter hyperparams,
  compute log) + contamination assertion output.
- **Datasets:** generator/version/seed/config (synthetic) or query-set SHA + run
  manifests + PRISMA counts (literature); field-level licence table reference.
- **Benchmarks:** split content hashes; baseline result artifacts.
- **Spaces:** pinned artifact versions the Space serves.

## Validation

Release CI ([ci_cd.md](ci_cd.md)) fails the release if: any field missing · any hash
mismatching the tagged tree · any dataset hash unknown · any seed absent · any card
lacking its mandatory statements. Reproducibility is enforced by machine, not by
promise — the same principle the benchmark applies to models, applied to ourselves.
