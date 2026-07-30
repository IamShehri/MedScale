"""Private CI-only harness for the P01-04B2A cross-platform portability gate.

This module is infrastructure, not product code.  It lives under ``tests/`` on
purpose (FD-PV-4, FC-PV-1): it is never shipped in the wheel, never enters the
``medscale`` public surface, and never inflates the ``src/medscale`` coverage
denominator.  Its filename does not match ``test_*.py``, so pytest does not
collect it as a test module, while mypy still type-checks it.

It generates the three per-cell evidence files from **fixed synthetic inputs**
by calling the adopted B2A serializers directly — it never reimplements
canonical serialization — and it aggregates six extracted per-cell directories
into a byte-for-byte cross-platform comparison.

The comparison normalizes nothing.  It performs no network access, loads no
model, reads no dataset, and runs no inference, retrieval, training, split
generation, transformation, leakage audit, benchmark, or clinical logic.

Running this harness is synthetic infrastructure validation.  It is not
admissible portability evidence and it does not accept B2A.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, ClassVar, Final

from medscale.mesc._canonical_json_v1 import (
    canonical_json_bytes,
    canonical_jsonl_bytes,
    sha256_of_bytes,
)

# --------------------------------------------------------------------------
# Ratified identifiers and limits
# --------------------------------------------------------------------------

#: Stable per-cell identifiers. Derived from the ratified matrix, never from
#: ``runner.os``, ``matrix.os`` or any Python runtime string.
CELL_IDS: Final[tuple[str, ...]] = (
    "linux-py3.11",
    "linux-py3.12",
    "macos-py3.11",
    "macos-py3.12",
    "windows-py3.11",
    "windows-py3.12",
)

#: Uploaded artifact name for each stable cell identifier.
ARTIFACT_PREFIX: Final = "b2a-portability-"
ARTIFACT_NAMES: Final[tuple[str, ...]] = tuple(f"{ARTIFACT_PREFIX}{cell}" for cell in CELL_IDS)

#: The exact three files every cell produces, in canonical sort order.
CANONICAL_JSON_NAME: Final = "canonical.json"
CANONICAL_JSONL_NAME: Final = "canonical.jsonl"
MANIFEST_NAME: Final = "manifest.json"
REQUIRED_FILES: Final[tuple[str, ...]] = (
    CANONICAL_JSON_NAME,
    CANONICAL_JSONL_NAME,
    MANIFEST_NAME,
)

EVIDENCE_NAME: Final = "portability-evidence.json"

MANIFEST_SCHEMA: Final = "mesc-pilot-01-b2a-portability-manifest/1"
EVIDENCE_SCHEMA: Final = "mesc-pilot-01-b2a-portability-evidence/1"

# FD-PV-6 byte limits. The aggregate values are the ratified derived maxima
# (exactly six times the per-artifact limits), so they are upper bounds.
MAX_FILE_BYTES: Final = 1_048_576
MAX_ARTIFACT_BYTES: Final = 4_194_304
MAX_AGGREGATE_COMPRESSED_BYTES: Final = 6_291_456
MAX_AGGREGATE_EXTRACTED_BYTES: Final = 25_165_824

_UTF8_BOM: Final = b"\xef\xbb\xbf"

# --------------------------------------------------------------------------
# Failure taxonomy — the twenty-one ratified categories, verbatim
# --------------------------------------------------------------------------


class PortabilityError(Exception):
    """Base class for every fail-closed portability-harness failure."""

    code: ClassVar[str] = "portability_error"


class MissingMatrixCellError(PortabilityError):
    code: ClassVar[str] = "missing_matrix_cell"


class DuplicateMatrixCellError(PortabilityError):
    code: ClassVar[str] = "duplicate_matrix_cell"


class UnexpectedMatrixCellError(PortabilityError):
    code: ClassVar[str] = "unexpected_matrix_cell"


class MissingEvidenceFileError(PortabilityError):
    code: ClassVar[str] = "missing_evidence_file"


class UnexpectedEvidenceFileError(PortabilityError):
    code: ClassVar[str] = "unexpected_evidence_file"


class ManifestSchemaMismatchError(PortabilityError):
    code: ClassVar[str] = "manifest_schema_mismatch"


class InvalidSha256Error(PortabilityError):
    code: ClassVar[str] = "invalid_sha256"


class ByteSizeMismatchError(PortabilityError):
    code: ClassVar[str] = "byte_size_mismatch"


class ContentHashMismatchError(PortabilityError):
    code: ClassVar[str] = "content_hash_mismatch"


class CrossPlatformByteMismatchError(PortabilityError):
    code: ClassVar[str] = "cross_platform_byte_mismatch"


class ForbiddenRuntimeMetadataError(PortabilityError):
    code: ClassVar[str] = "forbidden_runtime_metadata"


class NoncanonicalManifestError(PortabilityError):
    code: ClassVar[str] = "noncanonical_manifest"


class EvidenceGenerationFailureError(PortabilityError):
    code: ClassVar[str] = "evidence_generation_failure"


class BomPresentError(PortabilityError):
    code: ClassVar[str] = "bom_present"


class MalformedUtf8Error(PortabilityError):
    code: ClassVar[str] = "malformed_utf8"


class InvalidJsonError(PortabilityError):
    code: ClassVar[str] = "invalid_json"


class InvalidJsonlError(PortabilityError):
    code: ClassVar[str] = "invalid_jsonl"


class DuplicateJsonObjectKeyError(PortabilityError):
    code: ClassVar[str] = "duplicate_json_object_key"


class AggregateVerifierInternalError(PortabilityError):
    code: ClassVar[str] = "aggregate_verifier_internal_error"


class UnsafeArchiveEntryError(PortabilityError):
    code: ClassVar[str] = "unsafe_archive_entry"


class ArtifactSizeLimitExceededError(PortabilityError):
    code: ClassVar[str] = "artifact_size_limit_exceeded"


#: Every ratified category, for coverage assertions.
TAXONOMY: Final[tuple[type[PortabilityError], ...]] = (
    MissingMatrixCellError,
    DuplicateMatrixCellError,
    UnexpectedMatrixCellError,
    MissingEvidenceFileError,
    UnexpectedEvidenceFileError,
    ManifestSchemaMismatchError,
    InvalidSha256Error,
    ByteSizeMismatchError,
    ContentHashMismatchError,
    CrossPlatformByteMismatchError,
    ForbiddenRuntimeMetadataError,
    NoncanonicalManifestError,
    EvidenceGenerationFailureError,
    BomPresentError,
    MalformedUtf8Error,
    InvalidJsonError,
    InvalidJsonlError,
    DuplicateJsonObjectKeyError,
    AggregateVerifierInternalError,
    UnsafeArchiveEntryError,
    ArtifactSizeLimitExceededError,
)

# Key fragments that would leak runtime, host, or clock provenance into a
# compared payload. Checked against manifest and evidence keys, fail-closed.
_FORBIDDEN_KEY_FRAGMENTS: Final[tuple[str, ...]] = (
    "date",
    "timestamp",
    "_at",
    "time",
    "clock",
    "epoch",
    "path",
    "username",
    "user",
    "hostname",
    "host",
    "machine",
    "platform",
    "python",
    "runtime",
    "runner",
    "environ",
    "env",
    "command",
    "cwd",
    "locale",
    "timezone",
    "workflow",
    "run_id",
    "url",
    "os",
    "image",
    "secret",
)

# --------------------------------------------------------------------------
# Fixed synthetic inputs
# --------------------------------------------------------------------------

#: Closed-domain synthetic document. No floats: the canonical domain forbids
#: them, which removes the largest cross-platform formatting hazard outright.
SYNTHETIC_DOCUMENT: Final[Mapping[str, object]] = {
    "zulu": None,
    "alpha": {"nested": [1, 2, 3], "flag": True},
    "Beta": "café ☕",
    "nfc": "é",
    "nfd": "é",
    "cjk": "日本語",
    "delta": [],
    "echo": {},
    "big": 12345678901234567890123456789,
    "neg": -42,
    "zero": 0,
    "false": False,
    "tuple_as_array": (1, "x"),
}

#: Deterministically ordered synthetic records for the JSONL artifact.
SYNTHETIC_RECORDS: Final[tuple[Mapping[str, object], ...]] = (
    {"b": 1, "a": "x"},
    {"z": [True, False, None]},
    {},
    {"unicode": "é", "decomposed": "é"},
)


def build_canonical_json() -> bytes:
    """Return the canonical JSON artifact bytes for the synthetic document."""
    return canonical_json_bytes(SYNTHETIC_DOCUMENT)


def build_canonical_jsonl() -> bytes:
    """Return the canonical JSONL artifact bytes for the synthetic records."""
    return canonical_jsonl_bytes(SYNTHETIC_RECORDS)


def build_manifest(json_payload: bytes, jsonl_payload: bytes) -> bytes:
    """Return the canonical manifest describing the two payloads.

    The manifest carries only deterministic schema identifiers, file names,
    SHA-256 values, and byte sizes recomputed from the actual bytes.
    """
    document: dict[str, object] = {
        "schema_version": MANIFEST_SCHEMA,
        "files": [
            {
                "name": CANONICAL_JSON_NAME,
                "sha256": sha256_of_bytes(json_payload),
                "byte_size": len(json_payload),
            },
            {
                "name": CANONICAL_JSONL_NAME,
                "sha256": sha256_of_bytes(jsonl_payload),
                "byte_size": len(jsonl_payload),
            },
        ],
    }
    reject_forbidden_keys(document)
    return canonical_json_bytes(document)


def build_artifact_payloads() -> dict[str, bytes]:
    """Return the exact three artifact payloads, keyed by file name."""
    json_payload = build_canonical_json()
    jsonl_payload = build_canonical_jsonl()
    return {
        CANONICAL_JSON_NAME: json_payload,
        CANONICAL_JSONL_NAME: jsonl_payload,
        MANIFEST_NAME: build_manifest(json_payload, jsonl_payload),
    }


# --------------------------------------------------------------------------
# Structural and content validation
# --------------------------------------------------------------------------


def reject_forbidden_keys(document: object, *, _path: str = "") -> None:
    """Reject runtime, host, or clock provenance anywhere in a compared payload."""
    if isinstance(document, Mapping):
        for key in sorted(str(key) for key in document):
            lowered = key.lower()
            location = f"{_path}.{key}" if _path else key
            if any(fragment in lowered for fragment in _FORBIDDEN_KEY_FRAGMENTS):
                raise ForbiddenRuntimeMetadataError(f"forbidden metadata key at {location!r}")
            reject_forbidden_keys(document[key], _path=location)
    elif isinstance(document, list | tuple):
        for index, item in enumerate(document):
            reject_forbidden_keys(item, _path=f"{_path}[{index}]")


def _decode_utf8(payload: bytes, *, where: str) -> str:
    if payload.startswith(_UTF8_BOM):
        raise BomPresentError(f"{where} begins with a UTF-8 BOM")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise MalformedUtf8Error(f"{where} is not valid UTF-8") from error


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise DuplicateJsonObjectKeyError(f"duplicate JSON object key: {key!r}")
        seen.add(key)
    return dict(pairs)


def parse_strict_json(payload: bytes, *, where: str) -> object:
    """Parse one canonical JSON object, rejecting BOM, bad UTF-8 and duplicate keys."""
    text = _decode_utf8(payload, where=where)
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except DuplicateJsonObjectKeyError:
        raise
    except ValueError as error:
        raise InvalidJsonError(f"{where} is not valid JSON") from error


def parse_strict_jsonl(payload: bytes, *, where: str) -> list[object]:
    """Parse canonical JSONL: one object per line, LF only, no blank lines."""
    if payload == b"":
        return []
    if not payload.endswith(b"\n"):
        raise InvalidJsonlError(f"{where} does not end with LF")
    if b"\r" in payload:
        raise InvalidJsonlError(f"{where} contains CR")
    if b"\n\n" in payload:
        raise InvalidJsonlError(f"{where} contains a blank line")
    text = _decode_utf8(payload, where=where)
    records: list[object] = []
    for index, line in enumerate(text.split("\n")[:-1]):
        try:
            record = json.loads(line, object_pairs_hook=_no_duplicate_keys)
        except DuplicateJsonObjectKeyError:
            raise
        except ValueError as error:
            raise InvalidJsonlError(f"{where} line {index} is not valid JSON") from error
        if not isinstance(record, dict):
            raise InvalidJsonlError(f"{where} line {index} is not an object")
        records.append(record)
    return records


def validate_manifest(manifest_payload: bytes, payloads: Mapping[str, bytes]) -> None:
    """Validate manifest canonicality, schema, and binding to the actual bytes."""
    document = parse_strict_json(manifest_payload, where=MANIFEST_NAME)
    if not isinstance(document, dict):
        raise ManifestSchemaMismatchError("manifest is not a JSON object")
    reject_forbidden_keys(document)
    if canonical_json_bytes(document) != manifest_payload:
        raise NoncanonicalManifestError("manifest bytes are not canonical")
    if set(document) != {"schema_version", "files"}:
        raise ManifestSchemaMismatchError(f"unexpected manifest keys: {sorted(document)}")
    if document["schema_version"] != MANIFEST_SCHEMA:
        raise ManifestSchemaMismatchError(f"manifest schema must be {MANIFEST_SCHEMA!r}")
    entries = document["files"]
    if not isinstance(entries, list) or len(entries) != 2:
        raise ManifestSchemaMismatchError("manifest must describe exactly two files")
    described: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"name", "sha256", "byte_size"}:
            raise ManifestSchemaMismatchError("manifest entry has unexpected keys")
        name = entry["name"]
        if not isinstance(name, str) or name not in (CANONICAL_JSON_NAME, CANONICAL_JSONL_NAME):
            raise ManifestSchemaMismatchError(f"manifest names unknown file {name!r}")
        described.append(name)
        digest = entry["sha256"]
        _require_sha256(digest, where=f"manifest[{name}]")
        size = entry["byte_size"]
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise ByteSizeMismatchError(f"manifest[{name}] byte_size is not a non-negative int")
        actual = payloads[name]
        if digest != sha256_of_bytes(actual):
            raise ContentHashMismatchError(f"manifest[{name}] digest does not match bytes")
        if size != len(actual):
            raise ByteSizeMismatchError(f"manifest[{name}] byte size does not match bytes")
    if sorted(described) != sorted((CANONICAL_JSON_NAME, CANONICAL_JSONL_NAME)):
        raise ManifestSchemaMismatchError("manifest does not describe both payloads")


def _require_sha256(value: object, *, where: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise InvalidSha256Error(f"{where} sha256 must be 64 hex characters")
    if any(character not in "0123456789abcdef" for character in value):
        raise InvalidSha256Error(f"{where} sha256 must be lowercase hexadecimal")
    return value


def verify_payloads(payloads: Mapping[str, bytes], *, where: str) -> None:
    """Verify one cell's three payloads: names, bounds, encoding, and manifest."""
    names = set(payloads)
    missing = sorted(set(REQUIRED_FILES) - names)
    if missing:
        raise MissingEvidenceFileError(f"{where} is missing {missing}")
    unexpected = sorted(names - set(REQUIRED_FILES))
    if unexpected:
        raise UnexpectedEvidenceFileError(f"{where} has unexpected {unexpected}")
    total = 0
    for name in REQUIRED_FILES:
        payload = payloads[name]
        if len(payload) > MAX_FILE_BYTES:
            raise ArtifactSizeLimitExceededError(f"{where}/{name} exceeds the per-file limit")
        total += len(payload)
    if total > MAX_ARTIFACT_BYTES:
        raise ArtifactSizeLimitExceededError(f"{where} exceeds the per-artifact limit")
    parse_strict_json(payloads[CANONICAL_JSON_NAME], where=f"{where}/{CANONICAL_JSON_NAME}")
    parse_strict_jsonl(payloads[CANONICAL_JSONL_NAME], where=f"{where}/{CANONICAL_JSONL_NAME}")
    validate_manifest(payloads[MANIFEST_NAME], payloads)


# --------------------------------------------------------------------------
# Generation
# --------------------------------------------------------------------------


def generate(out_dir: Path) -> dict[str, bytes]:
    """Write the exact three files as raw bytes in binary mode, then verify them."""
    payloads = build_artifact_payloads()
    verify_payloads(payloads, where="generated")
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in REQUIRED_FILES:
        # Binary mode only: text mode would translate LF to CRLF on Windows and
        # manufacture a false cross-platform mismatch.
        (out_dir / name).write_bytes(payloads[name])
    written = _read_cell_dir(out_dir, where="generated")
    if written != payloads:
        raise EvidenceGenerationFailureError("written bytes differ from generated bytes")
    return payloads


# --------------------------------------------------------------------------
# Aggregation
# --------------------------------------------------------------------------


def _reject_unsafe_entry(entry: Path, root: Path, *, where: str) -> None:
    if entry.is_symlink():
        raise UnsafeArchiveEntryError(f"{where}/{entry.name} is a symbolic link")
    if entry.is_absolute() and not str(entry).startswith(str(root)):
        raise UnsafeArchiveEntryError(f"{where}/{entry.name} is an absolute path")
    if ".." in entry.parts:
        raise UnsafeArchiveEntryError(f"{where}/{entry.name} contains a parent traversal")
    try:
        resolved = entry.resolve(strict=True)
    except OSError as error:
        raise UnsafeArchiveEntryError(f"{where}/{entry.name} cannot be resolved") from error
    if root.resolve(strict=True) not in resolved.parents:
        raise UnsafeArchiveEntryError(f"{where}/{entry.name} escapes the extraction root")
    if not resolved.is_file():
        raise UnsafeArchiveEntryError(f"{where}/{entry.name} is not a regular file")
    if resolved.stat().st_nlink > 1:
        raise UnsafeArchiveEntryError(f"{where}/{entry.name} is a hard link")


def _read_cell_dir(cell_dir: Path, *, where: str) -> dict[str, bytes]:
    if not cell_dir.is_dir():
        raise MissingMatrixCellError(f"{where} is not a directory")
    entries = sorted(cell_dir.iterdir(), key=lambda item: item.name)
    lowered: dict[str, str] = {}
    for entry in entries:
        folded = entry.name.casefold()
        if folded in lowered:
            raise UnsafeArchiveEntryError(f"{where} has case-colliding names: {entry.name!r}")
        lowered[folded] = entry.name
        _reject_unsafe_entry(entry, cell_dir, where=where)
    names = [entry.name for entry in entries]
    missing = sorted(set(REQUIRED_FILES) - set(names))
    if missing:
        raise MissingEvidenceFileError(f"{where} is missing {missing}")
    unexpected = sorted(set(names) - set(REQUIRED_FILES))
    if unexpected:
        raise UnexpectedEvidenceFileError(f"{where} has unexpected {unexpected}")
    payloads: dict[str, bytes] = {}
    total = 0
    for entry in entries:
        size = entry.stat().st_size
        if size > MAX_FILE_BYTES:
            raise ArtifactSizeLimitExceededError(f"{where}/{entry.name} exceeds the per-file limit")
        total += size
        if total > MAX_ARTIFACT_BYTES:
            raise ArtifactSizeLimitExceededError(f"{where} exceeds the per-artifact limit")
        payloads[entry.name] = entry.read_bytes()
    return payloads


def check_artifact_names(names: Sequence[str]) -> None:
    """Enforce artifact cardinality: exactly the six expected names, no repeats.

    Kept as a pure function so duplicate and case-collision cardinality can be
    verified on every platform, including filesystems that cannot represent two
    directory names differing only by case.
    """
    folded: dict[str, str] = {}
    for name in names:
        key = name.casefold()
        if key in folded:
            raise DuplicateMatrixCellError(f"duplicate or case-colliding artifact: {name!r}")
        folded[key] = name
    expected = set(ARTIFACT_NAMES)
    missing = sorted(expected - set(names))
    if missing:
        raise MissingMatrixCellError(f"missing artifacts: {missing}")
    unexpected = sorted(set(names) - expected)
    if unexpected:
        raise UnexpectedMatrixCellError(f"unexpected artifacts: {unexpected}")
    if len(names) != len(CELL_IDS):
        raise DuplicateMatrixCellError(f"expected {len(CELL_IDS)} artifacts, found {len(names)}")


def _collect_cells(root: Path) -> dict[str, dict[str, bytes]]:
    if not root.is_dir():
        raise MissingMatrixCellError("artifact root is not a directory")
    directories = sorted((item for item in root.iterdir()), key=lambda item: item.name)
    for item in directories:
        if not item.is_dir() or item.is_symlink():
            raise UnsafeArchiveEntryError(f"artifact entry {item.name!r} is not a plain directory")
    check_artifact_names([item.name for item in directories])
    cells: dict[str, dict[str, bytes]] = {}
    extracted = 0
    for cell in CELL_IDS:
        payloads = _read_cell_dir(root / f"{ARTIFACT_PREFIX}{cell}", where=cell)
        extracted += sum(len(payload) for payload in payloads.values())
        if extracted > MAX_AGGREGATE_EXTRACTED_BYTES:
            raise ArtifactSizeLimitExceededError("aggregate extraction limit exceeded")
        cells[cell] = payloads
    if extracted > MAX_AGGREGATE_COMPRESSED_BYTES:
        raise ArtifactSizeLimitExceededError("aggregate byte limit exceeded")
    return cells


def build_evidence(cells: Mapping[str, Mapping[str, bytes]]) -> bytes:
    """Return the deterministic evidence envelope for a fully passing comparison."""
    reference = cells[CELL_IDS[0]]
    document: dict[str, object] = {
        "schema_version": EVIDENCE_SCHEMA,
        "cells": list(CELL_IDS),
        "files": [
            {
                "name": name,
                "sha256": sha256_of_bytes(reference[name]),
                "byte_size": len(reference[name]),
            }
            for name in REQUIRED_FILES
        ],
        "result": "pass",
    }
    reject_forbidden_keys(document)
    return canonical_json_bytes(document)


def aggregate(root: Path) -> bytes:
    """Verify six extracted per-cell directories and return the evidence bytes.

    Every structural, encoding, manifest, digest, size and cross-cell byte check
    must pass before an envelope exists.  Any internal failure is converted to a
    typed aggregate error so a verifier defect can never produce a pass.
    """
    try:
        cells = _collect_cells(root)
        for cell, payloads in cells.items():
            verify_payloads(payloads, where=cell)
        reference_cell = CELL_IDS[0]
        reference = cells[reference_cell]
        for cell in CELL_IDS[1:]:
            for name in REQUIRED_FILES:
                if cells[cell][name] != reference[name]:
                    raise CrossPlatformByteMismatchError(
                        f"{name} differs between {reference_cell} and {cell}"
                    )
        evidence = build_evidence(cells)
    except PortabilityError:
        raise
    except Exception as error:  # a verifier defect must fail closed, never pass
        raise AggregateVerifierInternalError(f"aggregate verifier failed: {error!r}") from error
    parsed = parse_strict_json(evidence, where=EVIDENCE_NAME)
    if not isinstance(parsed, dict) or parsed.get("result") != "pass":
        raise EvidenceGenerationFailureError("evidence envelope is not a passing record")
    return evidence


# --------------------------------------------------------------------------
# Private command-line surface (workflow use only)
# --------------------------------------------------------------------------


def _cmd_generate(args: argparse.Namespace) -> int:
    generate(Path(args.out))
    return 0


def _cmd_aggregate(args: argparse.Namespace) -> int:
    evidence = aggregate(Path(args.root))
    out = Path(args.evidence_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(evidence)
    sys.stdout.write(evidence.decode("utf-8"))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Private CLI entry point. Returns 0 on success, 1 on any typed failure."""
    parser = argparse.ArgumentParser(add_help=True, description="B2A portability harness")
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="write the three per-cell files")
    gen.add_argument("--out", required=True)
    gen.set_defaults(func=_cmd_generate)
    agg = sub.add_parser("aggregate", help="verify six cells and emit the envelope")
    agg.add_argument("--root", required=True)
    agg.add_argument("--evidence-out", required=True)
    agg.set_defaults(func=_cmd_aggregate)
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        result: int = args.func(args)
    except PortabilityError as error:
        sys.stderr.write(f"{error.code}: {error}\n")
        return 1
    return result


def iter_taxonomy_codes() -> Iterable[str]:
    """Yield every ratified failure-category identifier."""
    return (error.code for error in TAXONOMY)


if __name__ == "__main__":  # pragma: no cover - exercised by the workflow
    raise SystemExit(main())
