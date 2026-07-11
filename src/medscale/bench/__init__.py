"""medscale.bench — the scientific benchmark foundation (contracts before models).

Stability: **internal**, except the types the public ``Benchmark`` facade returns
(``BenchmarkSpec``, ``TaskItem``, ``BenchmarkRunArtifact``, ``EvidenceSystem``) which
are frozen with it.

The benchmark answers one question: *can a system produce correct, reproducible,
evidence-grounded outputs from the same scientific substrate?* Its invariants:

- a benchmark without a frozen knowledge state is **invalid** (spec binds a Research
  Snapshot; validation re-verifies the snapshot against the tree — gold cannot move);
- gold answers are human-validated evidence references with annotator attribution,
  never generated text;
- scorers are deterministic, versioned, and in-repo — no ML, no embeddings, no LLM
  judging, no hidden evaluator logic;
- every run emits a content-addressed artifact a 2035 researcher can reproduce.

Pipeline position: Evidence Objects -> Benchmark Tasks -> Gold Answers -> Metrics ->
Run Artifacts. Systems plug in behind the ``EvidenceSystem`` protocol; models never
shape the benchmark.
"""

from __future__ import annotations

from medscale.bench.baselines import EmptySystem, GoldOracle
from medscale.bench.run import BenchmarkRunArtifact, EvidenceSystem, run_benchmark
from medscale.bench.scorers import SCORER_VERSION, score_item
from medscale.bench.spec import BenchmarkSpec, TaskType
from medscale.bench.store import load_benchmark, write_benchmark
from medscale.bench.tasks import GoldEvidenceSet, Statement, TaskItem, TaskOutput
from medscale.bench.validate import validate_benchmark

__all__ = [
    "SCORER_VERSION",
    "BenchmarkRunArtifact",
    "BenchmarkSpec",
    "EmptySystem",
    "EvidenceSystem",
    "GoldEvidenceSet",
    "GoldOracle",
    "Statement",
    "TaskItem",
    "TaskOutput",
    "TaskType",
    "load_benchmark",
    "run_benchmark",
    "score_item",
    "validate_benchmark",
    "write_benchmark",
]
