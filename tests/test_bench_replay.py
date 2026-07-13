"""Benchmark replay contract: frozen identities and reproducible results_id."""

from __future__ import annotations

from pathlib import Path

from medscale.cli.bench_replay import main as replay_main


def test_missing_artifact_path_is_usage_error() -> None:
    assert replay_main(["/missing/artifact.json"]) == 2


def test_malformed_json_returns_usage_error(tmp_path: Path) -> None:
    path = tmp_path / "artifact.json"
    path.write_text("not-json", encoding="utf-8")
    assert replay_main([str(path)]) == 2
