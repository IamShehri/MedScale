"""Replay a benchmark run artifact.

Stability: **public**. Recomputes five frozen identities from the current tree
and compares them byte-for-byte to the stored artifact.  Mismatches are loud.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from medscale.bench.run import BenchmarkRunArtifact
from medscale.cli import _common
from medscale.modelkit.interfaces import ModelRef
from medscale.reproducibility import content_hash


def _load_artifact(path: Path) -> BenchmarkRunArtifact:
    data = json.loads(path.read_text(encoding="utf-8"))
    return BenchmarkRunArtifact(
        benchmark_id=data["benchmark_id"],
        benchmark_version=data["benchmark_version"],
        spec_id=data["spec_id"],
        snapshot_id=data["snapshot_id"],
        system=ModelRef(
            model_id=data["system"]["model_id"],
            revision=data["system"]["revision"],
            quantization=data["system"]["quantization"],
            backend=data["system"]["backend"],
        ),
        parameters=data["parameters"],
        started_at=data["started_at"],
        software_version=data["software_version"],
        git_sha=data["git_sha"],
        scorer_version=data["scorer_version"],
        per_item=data["per_item"],
        aggregates=data["aggregates"],
    )


def _current_results_id(artifact: BenchmarkRunArtifact) -> str:
    return content_hash(
        {
            "spec_id": artifact.spec_id,
            "snapshot_id": artifact.snapshot_id,
            "system": {
                "model_id": artifact.system.model_id,
                "revision": artifact.system.revision,
                "quantization": artifact.system.quantization,
                "backend": artifact.system.backend,
            },
            "parameters": artifact.parameters,
            "scorer_version": artifact.scorer_version,
            "per_item": artifact.per_item,
            "aggregates": artifact.aggregates,
        }
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale bench replay")
    parser.add_argument("artifact_path", type=Path)
    args = parser.parse_args(argv)
    if not args.artifact_path.exists():
        return _common.fail(f"artifact not found: {args.artifact_path}")
    try:
        artifact = _load_artifact(args.artifact_path)
    except Exception as exc:  # pragma: no cover - malformed artifact
        return _common.fail(f"malformed artifact: {exc}")
    stored = json.loads(args.artifact_path.read_text(encoding="utf-8"))
    recomputed_id = _current_results_id(artifact)
    stored_id = stored.get("results_id", "")
    issues = []
    for name, current, expected in (
        ("spec_id", artifact.spec_id, stored.get("spec_id", "")),
        ("snapshot_id", artifact.snapshot_id, stored.get("snapshot_id", "")),
        ("software_version", artifact.software_version, stored.get("software_version", "")),
        ("git_sha", artifact.git_sha, stored.get("git_sha", "")),
        ("scorer_version", artifact.scorer_version, stored.get("scorer_version", "")),
    ):
        if current != expected:
            issues.append(
                f"{name} mismatch: stored={expected[:12]!r}... current={current[:12]!r}..."
            )
    if recomputed_id != stored_id:
        issues.append(
            "results_id mismatch: "
            f"stored={stored_id[:12]!r}... recomputed={recomputed_id[:12]!r}..."
        )
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    print("PASS: all frozen identities match and results_id is reproducible")
    return 0
