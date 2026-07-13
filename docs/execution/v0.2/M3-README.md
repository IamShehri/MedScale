# M3 — Benchmark Determinism and Replay Contract

ADR-0029 is accepted.  M3 does not create a sandboxed toy; it wires
reproducibility checks into the existing bench core and CLI so that M4-MM6
start from a verifiable contract rather than a placeholder.

## Evidence Boundaries

- Gold answers are never generated text.  They are evidence
  IDs plus annotator attribution + timestamp, defined in
  `medscale.bench.tasks.GoldEvidenceSet`.
- Scorers are deterministic implementations of set coverage,
  citation accuracy, and summarization recall.  No ML, no embeddings,
  no LLM judging.
- Any system evaluated by the bench must implement `EvidenceSystem`.
  Reference systems (`gold-oracle`, `empty`) live in
  `medscale.bench.baselines`.

## Deterministic Task Contract

Item-side determinism is mandatory:

- `task_id` is kebab-case, sortable, immutable.
- task type vocabulary is frozen in `BenchmarkSpec.implemented_types`;
  `TaskType.CLINICAL_REASONING` is reserved until its directive lands.
- `seed` is per-task.  Task modules under `medscale/bench/tasks/` expose
  `version` and `seed` in metadata so drift is inspectable.
- context is the only allowed external input to `build()`; no hidden
  randomness, no environment reads.

## Synthetic Fixtures Only

M3 benchmarks use in-repo synthetic evidence sets.  No external datasets
are fetched at runtime.  The data boundary is the same as the evidence
boundary in M2: bench never imports `litdb`, `modelkit`, or `bench`
outside its own subpackage.

## Manifest

`data/bench/manifests/medscale-bench-v1.json` is the canonical frozen
benchmark manifest.  It records:

- `benchmark_id`
- `dataset_id`
- `git_sha`
- `software_version`
- `seed`
- task versions
- scorer versions

The manifest is content-addressed: any edit produces a new manifest
identity through `BenchmarkSpec.spec_id`.  The layout helper lives in
`medscale._layout.BENCHMARKS_DIR`.

## CLI (artifact-first replay)

Replay is read-only and fails loudly:

- `medscale bench list` lists benchmarks under `data/litdb/benchmarks/`.
- `medscale bench validate <benchmark_id>` re-verifies the benchmark
  spec and evidence tree; non-zero exit on any failure.
- `medscale bench run <benchmark_id> --system gold-oracle` executes a
  reference system and writes a content-addressed run artifact.
- `medscale bench replay <artifact.json>` recomputes five frozen
  identities from the current tree and compares them byte-for-byte
  to the stored artifact.  Mismatches produce actionable messages for
  spec drift, snapshot drift, software version drift, repo state drift,
  or scorer drift.  Replay never silently rewrites or ignores history.

The five identities a run artifact records and replay checks:

1. `spec_id`
2. `snapshot_id`
3. `software_version`
4. `git_sha`
5. `scorer_version`

Run artifacts live at:

`data/litdb/benchmarks/<benchmark_id>/runs/<results_id[:16]>.json`

## Validation Rules

`medscale.bench.validate` checks:

- spec_id matches the current spec code and metadata
- snapshot_id is a 64-hex Research Snapshot identity
- task_ids are unique and sorted
- task_types are from the implemented set
- gold sets have non-empty annotator and valid timestamp
- supporting and contradicting ids are disjoint
- every run artifact's frozen identities match the current tree
  on replay

## Reproducibility Guarantees

- scorer output is a pure function of `(item, output, known_ids)`;
  no mutable static state, no randomness.
- sorted task iteration removes nondeterministic ordering.
- content addressing means verified run artifacts are identical regardless
  of whose workstation produced them; they are evidence objects, not logs.

## Separation from Training

M3 deliverables stop at executable benchmark contracts and run artifacts.
No model training pipeline, no knowledge graph, no web UI, and no
autonomous clinical AI branches are introduced.

## CI Expectations

- `medscale bench validate` must pass for every committed benchmark.
- `medscale bench replay <artifact>` for M3 run artifacts must pass.
- Benchmarks without a verified replay are not publishable.
