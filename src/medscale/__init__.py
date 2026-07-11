"""MedScale: open research intelligence infrastructure for medicine.

The top level is the **stable public contract** — the objects every interface (CLI,
future REST/MCP adapters, SDKs, Afia, notebooks) consumes. Implementation modules
beneath are internal and replaceable; these names are frozen::

    from medscale import Corpus, Benchmark

    corpus = Corpus.load("data/litdb")
    evidence = corpus.evidence()
    results = evidence.query(...)
    snapshot = results.snapshot()
    benchmark = Benchmark.load("data/litdb", "evidence-bench")
    report = benchmark.run(system)

Plus the spine primitives (:func:`canonical_json`, :func:`content_hash`,
:func:`set_global_seed`) that every layer's determinism rests on.
"""

from __future__ import annotations

from medscale.__about__ import __version__
from medscale.reproducibility import canonical_json, content_hash, set_global_seed
from medscale.workspace import (
    Benchmark,
    Corpus,
    Evidence,
    EvidenceQueryResult,
    RecordQueryResult,
    Snapshot,
    VerificationEngine,
    Workspace,
)

__all__ = [
    "Benchmark",
    "Corpus",
    "Evidence",
    "EvidenceQueryResult",
    "RecordQueryResult",
    "Snapshot",
    "VerificationEngine",
    "Workspace",
    "__version__",
    "canonical_json",
    "content_hash",
    "set_global_seed",
]
