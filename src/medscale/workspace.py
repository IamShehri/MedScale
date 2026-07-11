"""The MedScale Core Library: the stable public contract every interface consumes.

Five years from now, the CLI, REST adapters, MCP servers, the Python SDK, Afia, and
research notebooks must all call exactly this code. Design rules (PyTorch / pandas /
Arrow / HF-datasets discipline):

- **stable objects, not implementation details** — users see ``Workspace``, ``Corpus``,
  ``Evidence``, ``Benchmark``, ``Snapshot``, ``VerificationEngine``; storage layout,
  file formats, and module topology are internal and replaceable;
- the *only* storage-coupled fact in user code is an opaque workspace root;
- every object is immutable; every result is a value; nothing here mutates state
  except the explicitly-named write operations (``snapshot()`` capture, ``run()``
  artifact persistence);
- if the storage engine is swapped, the core rewritten in Rust, or computation
  distributed, **user code does not change** — that is the frozen promise.

The researcher contract this module exists to keep::

    from medscale import Corpus, Benchmark

    corpus = Corpus.load("data/litdb")
    evidence = corpus.evidence()
    results = evidence.query(study_type=StudyType.RANDOMIZED_CONTROLLED_TRIAL)
    snapshot = results.snapshot()
    benchmark = Benchmark.load("data/litdb", "evidence-bench")
    report = benchmark.run(system)
"""

from __future__ import annotations

import subprocess
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from medscale.__about__ import __version__
from medscale.bench.run import BenchmarkRunArtifact, EvidenceSystem, run_benchmark
from medscale.bench.spec import BenchmarkSpec
from medscale.bench.store import list_benchmarks, load_benchmark
from medscale.bench.tasks import TaskItem
from medscale.bench.validate import validate_benchmark
from medscale.evidence import EvidenceObject
from medscale.evidence_checks import CheckResult, archived_payload_hashes, rule_verify_source
from medscale.litdb.integrity import IntegrityReport, check_litdb
from medscale.litdb.records import LiteratureRecord
from medscale.research.index import ResearchIndex
from medscale.research.query import evidence_where, records_where
from medscale.research.snapshot import ResearchSnapshot, capture_snapshot, write_snapshot
from medscale.research.snapshot import verify_snapshot as _verify_snapshot
from medscale.research.stats import corpus_stats, evidence_stats, screening_stats

__all__ = [
    "Benchmark",
    "Corpus",
    "Evidence",
    "EvidenceQueryResult",
    "RecordQueryResult",
    "Snapshot",
    "VerificationEngine",
    "Workspace",
]

#: The stable name of the snapshot type in the public contract.
Snapshot = ResearchSnapshot


def _default_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0000000"


@dataclass(frozen=True)
class Workspace:
    """The root handle: one opaque location, everything else derived and immutable."""

    _root: Path
    _index: ResearchIndex

    @classmethod
    def open(cls, root: str | Path) -> Workspace:
        path = Path(root)
        return cls(_root=path, _index=ResearchIndex.load(path))

    @property
    def corpus(self) -> Corpus:
        return Corpus(self)

    @property
    def evidence(self) -> Evidence:
        return Evidence(self)

    @property
    def verification(self) -> VerificationEngine:
        return VerificationEngine(self)

    def index(self) -> ResearchIndex:
        """The immutable joined read view (already a stable public value)."""
        return self._index

    def stats(self) -> dict[str, Any]:
        """Machine-readable statistics document (corpus / screening / evidence)."""
        return {
            "corpus": corpus_stats(self._index).to_dict(),
            "screening": screening_stats(self._index).to_dict(),
            "evidence": evidence_stats(self._index).to_dict(),
        }

    def integrity(self) -> IntegrityReport:
        """Referential-integrity report over every store and log."""
        return check_litdb(self._root)

    def snapshot(self, *, write: bool = True) -> Snapshot:
        """Capture (and by default persist) the citable knowledge-state identity."""
        snapshot = capture_snapshot(
            self._root,
            git_sha=_default_git_sha(),
            software_version=__version__,
            created_at=datetime.now(UTC).isoformat(),
        )
        if write:
            write_snapshot(self._root, snapshot)
        return snapshot

    def verify(self, snapshot: Snapshot) -> tuple[str, ...]:
        """Recompute every hash against this workspace; empty tuple = state matches."""
        return _verify_snapshot(self._root, snapshot)

    def benchmarks(self) -> tuple[str, ...]:
        return list_benchmarks(self._root)

    def benchmark(self, benchmark_id: str) -> Benchmark:
        return Benchmark._load(self, benchmark_id)


@dataclass(frozen=True)
class RecordQueryResult:
    """An immutable, id-ordered record result set."""

    records: tuple[LiteratureRecord, ...]
    _workspace: Workspace

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self) -> Iterator[LiteratureRecord]:
        return iter(self.records)

    def snapshot(self) -> Snapshot:
        """The citable knowledge state these results were computed from."""
        return self._workspace.snapshot()


@dataclass(frozen=True)
class EvidenceQueryResult:
    """An immutable, id-ordered evidence result set."""

    objects: tuple[EvidenceObject, ...]
    _workspace: Workspace

    def __len__(self) -> int:
        return len(self.objects)

    def __iter__(self) -> Iterator[EvidenceObject]:
        return iter(self.objects)

    def snapshot(self) -> Snapshot:
        """The citable knowledge state these results were computed from."""
        return self._workspace.snapshot()


@dataclass(frozen=True)
class Corpus:
    """The screened literature corpus, queryable and stats-ready."""

    _workspace: Workspace

    @classmethod
    def load(cls, root: str | Path) -> Corpus:
        return Workspace.open(root).corpus

    def __len__(self) -> int:
        return len(self._workspace.index().records)

    def __iter__(self) -> Iterator[LiteratureRecord]:
        return iter(self._workspace.index().records)

    def records(self) -> tuple[LiteratureRecord, ...]:
        return self._workspace.index().records

    def query(self, **filters: Any) -> RecordQueryResult:
        """Deterministic conjunctive filtering (see ``research.query.records_where``)."""
        return RecordQueryResult(
            records=records_where(self._workspace.index(), **filters),
            _workspace=self._workspace,
        )

    def evidence(self) -> Evidence:
        return self._workspace.evidence

    def stats(self) -> dict[str, Any]:
        return corpus_stats(self._workspace.index()).to_dict()


@dataclass(frozen=True)
class Evidence:
    """The verified evidence store, queryable by claim structure and verification."""

    _workspace: Workspace

    @classmethod
    def load(cls, root: str | Path) -> Evidence:
        return Workspace.open(root).evidence

    def __len__(self) -> int:
        return len(self._workspace.index().evidence)

    def __iter__(self) -> Iterator[EvidenceObject]:
        return iter(self._workspace.index().evidence)

    def objects(self) -> tuple[EvidenceObject, ...]:
        return self._workspace.index().evidence

    def query(self, **filters: Any) -> EvidenceQueryResult:
        """Deterministic conjunctive filtering (see ``research.query.evidence_where``)."""
        return EvidenceQueryResult(
            objects=evidence_where(self._workspace.index(), **filters),
            _workspace=self._workspace,
        )

    def stats(self) -> dict[str, Any]:
        return evidence_stats(self._workspace.index()).to_dict()


@dataclass(frozen=True)
class VerificationEngine:
    """Deterministic claim verification: named checks, rule-based state advancement."""

    _workspace: Workspace

    def verify(self, obj: EvidenceObject) -> tuple[EvidenceObject, tuple[CheckResult, ...]]:
        """Run every source check; advance UNVERIFIED -> SOURCE_VERIFIED iff all pass."""
        index = self._workspace.index()
        corpus_ids = frozenset(record.record_id for record in index.records)
        known_hashes = archived_payload_hashes(self._workspace._root)
        return rule_verify_source(obj, corpus_ids, known_hashes)


@dataclass(frozen=True)
class Benchmark:
    """A snapshot-bound benchmark: validate and run, never mutate."""

    spec: BenchmarkSpec
    items: tuple[TaskItem, ...]
    _workspace: Workspace

    @classmethod
    def load(cls, root: str | Path, benchmark_id: str) -> Benchmark:
        return Workspace.open(root).benchmark(benchmark_id)

    @classmethod
    def _load(cls, workspace: Workspace, benchmark_id: str) -> Benchmark:
        spec, items = load_benchmark(workspace._root, benchmark_id)
        return cls(spec=spec, items=items, _workspace=workspace)

    def validate(self) -> tuple[str, ...]:
        """Every scientific-validity issue; empty tuple = runnable."""
        return validate_benchmark(self._workspace._root, self.spec, self.items)

    def run(
        self, system: EvidenceSystem, *, parameters: dict[str, Any] | None = None
    ) -> BenchmarkRunArtifact:
        """Execute against a system; returns the reproducible run report."""
        artifact, _ = run_benchmark(
            self._workspace._root,
            self.spec.benchmark_id,
            system,
            parameters=parameters,
            started_at=datetime.now(UTC).isoformat(),
            software_version=__version__,
            git_sha=_default_git_sha(),
        )
        return artifact
