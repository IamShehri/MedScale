"""Transform PubMedQA parquet into deterministic MedScale Layer-1 source records.

Exit codes:
  0 - success
  1 - validation, input, transformation, determinism, or existing-output failure
  2 - argparse usage error
  3 - unexpected internal error
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import shutil
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

# ============================================================================
# Authoritative constants — sourced from private transformation module
# ============================================================================


CONFIGURATION: str = "pqa_labeled"
DATASET_REVISION: str = "9001f2853fb87cab8d220904e0de81ac6973b318"
LICENSE_ID: str = "PubMedQA-PQA-L"
PARQUET_BASENAME: str = "train-00000-of-00001.parquet"
TRANSFORMATION_RUN_SCHEMA: str = "mesc-pubmedqa-operator-result/1"

# ============================================================================
# Artifacts
# ============================================================================


@dataclass(frozen=True, slots=True)
class RunArtifacts:
    run_dir: Path
    records_path: Path
    records_size: int
    records_sha256: str
    registry_path: Path
    registry_size: int
    registry_sha256: str
    manifest_path: Path
    manifest_size: int
    manifest_sha256: str
    manifest_bytes: bytes
    local_path: Path
    records_bytes: bytes
    registry_bytes: bytes


# ============================================================================
# Readers / helpers
# ============================================================================


def _read_all(path: Path) -> bytes:
    return path.read_bytes()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _unique_temp_dir(final_output: Path) -> Path:
    parent = final_output.parent
    for _ in range(1000):
        candidate = parent / f".{final_output.name}-tmp-{uuid.uuid4().hex}"
        if not candidate.exists():
            return candidate
    raise RuntimeError("unable to allocate unique temporary run directory")


def _is_safe_output_parent(final_output: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    raw_root = repo_root / "data" / "raw"
    resolved = final_output.resolve()
    if str(resolved).startswith(str(repo_root)):
        raise ValueError("output path must not be inside the MedScale repository")
    onedrive_markers = ["OneDrive", "OneDriveTemp", "OneDrive for Business"]
    if any(marker in str(resolved) for marker in onedrive_markers):
        raise ValueError("output path must not be inside OneDrive")
    try:
        resolved.relative_to(raw_root)
        raise ValueError("output path must not be inside the raw-data directory")
    except ValueError:
        if "output path must not be inside the raw-data directory" in str(resolved):
            raise
        # not under raw root — safe
    with contextlib.suppress(ValueError):
        _ = os.path.commonpath([str(resolved), str(repo_root)])


# ============================================================================
# Promotion
# ============================================================================


def _promote(source: RunArtifacts, final_output: Path) -> None:
    if final_output.exists():
        raise FileExistsError(f"final output already exists at promotion time: {final_output}")
    rename_src = source.run_dir
    rename_src.replace(final_output)


# ============================================================================
# Compare
# ============================================================================


def _compare_runs(first: RunArtifacts, second: RunArtifacts) -> list[str]:
    fields = [
        (
            "source-records.jsonl",
            first.records_size,
            second.records_size,
            first.records_sha256,
            second.records_sha256,
        ),
        (
            "source-record-registry.jsonl",
            first.registry_size,
            second.registry_size,
            first.registry_sha256,
            second.registry_sha256,
        ),
        (
            "transformation-manifest.json",
            first.manifest_size,
            second.manifest_size,
            first.manifest_sha256,
            second.manifest_sha256,
        ),
    ]
    failures: list[str] = []
    for name, size_a, size_b, hash_a, hash_b in fields:
        if size_a != size_b:
            failures.append(f"{name} size mismatch: {size_a} != {size_b}")
        if hash_a != hash_b:
            failures.append(f"{name} sha256 mismatch: {hash_a} != {hash_b}")
    if first.records_bytes != second.records_bytes:
        failures.append("source-records.jsonl full-byte mismatch")
    if first.registry_bytes != second.registry_bytes:
        failures.append("source-record-registry.jsonl full-byte mismatch")
    if first.manifest_bytes != second.manifest_bytes:
        failures.append("transformation-manifest.json full-byte mismatch")
    return failures


# ============================================================================
# Execute a single run
# ============================================================================


def _execute_run(
    input_path: Path,
    expected_sha256: str,
    expected_size: int,
    run_dir: Path,
) -> RunArtifacts:
    from medscale.dataset._pubmedqa_source import transform_pubmedqa_parquet

    transform_pubmedqa_parquet(
        input_path,
        run_dir,
        expected_input_sha256=expected_sha256,
        expected_input_size=expected_size,
    )
    records_path = run_dir / "source-records.jsonl"
    registry_path = run_dir / "source-record-registry.jsonl"
    manifest_path = run_dir / "transformation-manifest.json"
    local_path = run_dir / "transformation-run.local.json"
    records_bytes = _read_all(records_path)
    registry_bytes = _read_all(registry_path)
    manifest_bytes = _read_all(manifest_path)
    return RunArtifacts(
        run_dir=run_dir,
        records_path=records_path,
        records_size=records_path.stat().st_size,
        records_sha256=_sha256_bytes(records_bytes),
        registry_path=registry_path,
        registry_size=registry_path.stat().st_size,
        registry_sha256=_sha256_bytes(registry_bytes),
        manifest_path=manifest_path,
        manifest_size=manifest_path.stat().st_size,
        manifest_sha256=_sha256_bytes(manifest_bytes),
        manifest_bytes=manifest_bytes,
        local_path=local_path,
        records_bytes=records_bytes,
        registry_bytes=registry_bytes,
    )


# ============================================================================
# Main
# ============================================================================


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transform PubMedQA parquet")
    parser.add_argument("--input", required=True, help="Source parquet file")
    parser.add_argument("--output-dir", required=True, help="Final output directory")
    parser.add_argument("--expected-sha256", required=True, help="Expected input SHA-256")
    parser.add_argument("--expected-size", required=True, type=int, help="Expected input byte size")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    input_path = Path(args.input).resolve()
    final_output = Path(args.output_dir).resolve()
    expected_sha256 = args.expected_sha256
    expected_size = args.expected_size

    if not input_path.is_file():
        print(json.dumps({"error": "input artifact not found"}, sort_keys=True))
        return 1

    try:
        _is_safe_output_parent(final_output)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 1

    if final_output.exists():
        print(json.dumps({"error": "final output already exists"}, sort_keys=True))
        return 1

    input_size = input_path.stat().st_size
    if expected_size != input_size:
        print(json.dumps({"error": "input size mismatch"}, sort_keys=True))
        return 1

    input_sha256 = _sha256_bytes(_read_all(input_path))
    if expected_sha256 != input_sha256:
        print(json.dumps({"error": "input sha256 mismatch"}, sort_keys=True))
        return 1

    temp_dir = _unique_temp_dir(final_output)
    try:
        first = _execute_run(input_path, expected_sha256, expected_size, temp_dir)
        second_temp = _unique_temp_dir(final_output)
        try:
            second = _execute_run(input_path, expected_sha256, expected_size, second_temp)
        finally:
            shutil.rmtree(second_temp, ignore_errors=True)
        failures = _compare_runs(first, second)
        if failures:
            print(
                json.dumps(
                    {
                        "error": "determinism-check failed",
                        "failures": failures,
                    },
                    sort_keys=True,
                )
            )
            return 1
        _promote(first, final_output)
        print(
            json.dumps(
                {
                    "schema_version": TRANSFORMATION_RUN_SCHEMA,
                    "output_files": [
                        "source-records.jsonl",
                        "source-record-registry.jsonl",
                        "transformation-manifest.json",
                        "transformation-run.local.json",
                    ],
                },
                sort_keys=True,
            )
        )
        return 0
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        print(json.dumps({"error": f"unexpected error: {exc}"}, sort_keys=True))
        sys.exit(3)
