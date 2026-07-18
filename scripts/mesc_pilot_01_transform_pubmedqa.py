"""Deterministic PubMedQA Layer-1 source transformation orchestrator.

Reads the approved PubMedQA Parquet artifact twice into sibling temporary
directories, verifies that three deterministic output files are byte-for-byte
identical, and atomically promotes one run to the final output directory.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

# Network isolation must be established before any Hugging Face / dataset import
# is attempted.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")


@dataclass(frozen=True)
class RunArtifacts:
    directory: Path
    source_records_path: Path
    registry_path: Path
    manifest_path: Path
    report_path: Path
    local_report_path: Path
    source_records_sha256: str
    registry_sha256: str
    manifest_sha256: str
    source_records_size: int
    registry_size: int
    manifest_size: int


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_size(path: Path) -> int:
    return path.stat().st_size


def _prepare_run_directory(final_output: Path, run_index: int) -> Path:
    sibling_dir = final_output.parent
    run_dir = sibling_dir / f"{final_output.name}-run-{run_index}"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _collect_artifacts(run_dir: Path) -> RunArtifacts:
    source_records_path = run_dir / "source-records.jsonl"
    registry_path = run_dir / "source-record-registry.jsonl"
    manifest_path = run_dir / "source-record-manifest.json"
    report_path = run_dir / "transformation-report.json"
    local_report_path = run_dir / "transformation-run.local.json"
    return RunArtifacts(
        directory=run_dir,
        source_records_path=source_records_path,
        registry_path=registry_path,
        manifest_path=manifest_path,
        report_path=report_path,
        local_report_path=local_report_path,
        source_records_sha256=_file_sha256(source_records_path),
        registry_sha256=_file_sha256(registry_path),
        manifest_sha256=_file_sha256(manifest_path),
        source_records_size=_file_size(source_records_path),
        registry_size=_file_size(registry_path),
        manifest_size=_file_size(manifest_path),
    )


def _compare_artifacts(a: RunArtifacts, b: RunArtifacts) -> list[str]:
    failures: list[str] = []
    fields = [
        ("filenames", (a.source_records_path.name, b.source_records_path.name)),
        ("source-records length", (a.source_records_size, b.source_records_size)),
        ("source-records SHA-256", (a.source_records_sha256, b.source_records_sha256)),
        (
            "source-record-registry length",
            (a.registry_size, b.registry_size),
        ),
        (
            "source-record-registry SHA-256",
            (a.registry_sha256, b.registry_sha256),
        ),
        (
            "source-record-manifest length",
            (a.manifest_size, b.manifest_size),
        ),
        (
            "source-record-manifest SHA-256",
            (a.manifest_sha256, b.manifest_sha256),
        ),
    ]
    for label, values in fields:
        if values[0] != values[1]:
            failures.append(f"{label} mismatch: {values[0]!r} != {values[1]!r}")
    for left, right in [
        (a.source_records_path.name, b.source_records_path.name),
        (a.registry_path.name, b.registry_path.name),
        (a.manifest_path.name, b.manifest_path.name),
    ]:
        if left != right:
            failures.append(f"filename mismatch: {left!r} != {right!r}")
    with a.source_records_path.open("rb") as fa, b.source_records_path.open("rb") as fb:
        if fa.read() != fb.read():
            failures.append("source-records.jsonl full-byte mismatch")
    with a.registry_path.open("rb") as fa, b.registry_path.open("rb") as fb:
        if fa.read() != fb.read():
            failures.append("source-record-registry.jsonl full-byte mismatch")
    with a.manifest_path.open("rb") as fa, b.manifest_path.open("rb") as fb:
        if fa.read() != fb.read():
            failures.append("source-record-manifest.json full-byte mismatch")
    return failures


def _promote(run: RunArtifacts, final_output: Path) -> None:
    if final_output.exists():
        shutil.rmtree(final_output)
    final_output.mkdir(parents=True, exist_ok=True)
    for source in run.directory.iterdir():
        target = final_output / source.name
        if source.is_file():
            shutil.copy2(source, target)


def _print_summary(run: RunArtifacts) -> None:
    sys.stdout.write(
        f"source-records.jsonl   -> {run.source_records_path}  "
        f"({run.source_records_size} bytes, sha256 {run.source_records_sha256})\n"
    )
    sys.stdout.write(
        f"source-record-registry.jsonl -> {run.registry_path}  "
        f"({run.registry_size} bytes, sha256 {run.registry_sha256})\n"
    )
    sys.stdout.write(
        f"source-record-manifest.json  -> {run.manifest_path}  "
        f"({run.manifest_size} bytes, sha256 {run.manifest_sha256})\n"
    )
    sys.stdout.write(
        "\nDeterministic bundle promoted to final output directory. Raw text is not printed.\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic PubMedQA Layer-1 source transformation orchestrator"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to approved PubMedQA Parquet artifact",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Final output directory for deterministic source records",
    )
    parser.add_argument(
        "--expected-sha256",
        required=True,
        help="Expected SHA-256 of the input Parquet artifact",
    )
    parser.add_argument(
        "--expected-size",
        type=int,
        required=True,
        help="Expected size in bytes of the input Parquet artifact",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not input_path.is_file():
        raise SystemExit(f"input artifact not found: {input_path}")
    if input_path.stat().st_size != args.expected_size:
        raise SystemExit(
            f"input size mismatch: expected {args.expected_size}, got {input_path.stat().st_size}"
        )
    actual_sha256 = hashlib.sha256(input_path.read_bytes()).hexdigest()
    if actual_sha256 != args.expected_sha256:
        raise SystemExit(
            f"input SHA-256 mismatch: expected {args.expected_sha256}, got {actual_sha256}"
        )

    from medscale.dataset._pubmedqa_source import (
        transform_pubmedqa_parquet,
    )

    # Two runs into sibling temporary directories.
    run_one_dir = _prepare_run_directory(output_dir, 1)
    run_two_dir = _prepare_run_directory(output_dir, 2)

    run_one_meta = transform_pubmedqa_parquet(
        str(input_path),
        str(run_one_dir),
        expected_input_sha256=args.expected_sha256,
        expected_input_size=args.expected_size,
        run_label="run-one",
    )
    run_two_meta = transform_pubmedqa_parquet(
        str(input_path),
        str(run_two_dir),
        expected_input_sha256=args.expected_sha256,
        expected_input_size=args.expected_size,
        run_label="run-two",
    )

    run_one = _collect_artifacts(run_one_dir)
    run_two = _collect_artifacts(run_two_dir)

    comparison_failures = _compare_artifacts(run_one, run_two)
    if comparison_failures:
        sys.stderr.write("Byte-for-byte comparison failed:\n")
        for failure in comparison_failures:
            sys.stderr.write(f"  - {failure}\n")
        shutil.rmtree(run_one_dir, ignore_errors=True)
        shutil.rmtree(run_two_dir, ignore_errors=True)
        return 2

    _promote(run_one, output_dir)
    shutil.rmtree(run_one_dir, ignore_errors=True)
    shutil.rmtree(run_two_dir, ignore_errors=True)
    _print_summary(run_one)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
