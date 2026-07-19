#!/usr/bin/env python3
"""P01-03F PubMedQA bundle validation operator.

Standard-library only.
Read-only validation of an existing deterministic Layer-1 bundle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from medscale.dataset._pubmedqa_validation import BundleValidationReport, validate_pubmedqa_bundle

_REQUIRED_BUNDLE_FILES = [
    "source-records.jsonl",
    "source-record-registry.jsonl",
    "transformation-manifest.json",
    "transformation-run.local.json",
]
_REPORT_SCHEMA_VERSION = "mesc-pubmedqa-validation-report/1"


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run P01-03F formal validation against a PubMedQA source-record bundle.",
    )
    parser.add_argument(
        "--bundle-dir",
        required=True,
        help="Path to the existing deterministic bundle directory.",
    )
    parser.add_argument(
        "--raw-artifact",
        required=True,
        help=(
            "Path to the raw Parquet artifact. Verified by filename basename, "
            "size, and SHA-256 only."
        ),
    )
    parser.add_argument(
        "--expected-raw-size",
        required=True,
        type=int,
        help="Expected size of the raw artifact in bytes.",
    )
    parser.add_argument(
        "--expected-raw-sha256",
        required=True,
        help="Expected SHA-256 hex digest of the raw artifact.",
    )
    return parser.parse_args(argv)


def _stream_sha256(path: str, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _file_identity(path: str) -> tuple[str, int]:
    return _stream_sha256(path), Path(path).stat().st_size


def _build_summary(report: BundleValidationReport) -> dict[str, object]:
    return {
        "schema_version": _REPORT_SCHEMA_VERSION,
        "status": report.status,
        "success": report.success,
        "authorized": report.authorized,
        "issues_count": len(report.issues),
        "bundle_inventory_match": report.bundle_inventory_match,
        "byte_equivalence": report.byte_equivalence,
        "raw_artifact_unchanged": report.raw_artifact_unchanged,
        "public_contract_unchanged": report.public_contract_unchanged,
        "transformation_rerun": report.transformation_rerun,
        "bundle_mutation_count": report.bundle_mutation_count,
        "record_validation_passed": report.record_validation_passed,
        "record_validation_failed": report.record_validation_failed,
        "registry_validation_passed": report.registry_validation_passed,
        "registry_validation_failed": report.registry_validation_failed,
    }


def main(argv: list[str]) -> int:
    try:
        args = _parse_args(argv)
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - defensive argparse failure
        print(json.dumps({"error": f"argument parsing failure: {exc}"}, sort_keys=True))
        return 2

    bundle_dir = Path(args.bundle_dir).resolve()
    raw_artifact = Path(args.raw_artifact).resolve()

    if not bundle_dir.is_dir():
        print(
            json.dumps(
                {"error": "bundle directory does not exist", "issue": "missing-bundle-dir"},
                sort_keys=True,
            )
        )
        return 2

    if not raw_artifact.is_file():
        print(
            json.dumps(
                {"error": "raw artifact does not exist", "issue": "missing-raw-artifact"},
                sort_keys=True,
            )
        )
        return 2

    actual_files = sorted(path.name for path in bundle_dir.iterdir() if path.is_file())
    expected_files = sorted(_REQUIRED_BUNDLE_FILES)
    if actual_files != expected_files:
        print(
            json.dumps(
                {
                    "error": "unexpected bundle inventory",
                    "expected": expected_files,
                    "actual": actual_files,
                },
                sort_keys=True,
            )
        )
        return 1

    try:
        report = validate_pubmedqa_bundle(
            bundle_dir,
            raw_artifact=raw_artifact,
            authorized=True,
            expected_raw_size=args.expected_raw_size,
            expected_raw_sha256=args.expected_raw_sha256,
            require_byte_equivalence=True,
            strict=True,
        )
    except ValueError as exc:
        print(json.dumps({"error": str(exc), "issue": "invalid-bundle"}, sort_keys=True))
        return 1
    except Exception as exc:  # pragma: no cover - defensive internal failure
        print(json.dumps({"error": f"unexpected validation failure: {exc}"}, sort_keys=True))
        return 3

    summary = _build_summary(report)
    print(json.dumps(summary, sort_keys=True))
    return 0 if report.success else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - defensive top-level failure
        print(json.dumps({"error": f"unexpected error: {exc}"}, sort_keys=True))
        sys.exit(3)
