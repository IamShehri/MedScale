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
import contextlib
import json
import sys
import zipfile
import zlib
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

#: FD-PV-14 envelope field name and its exact accepted form.
CANONICAL_SHA_KEY: Final = "canonical_sha"
CANONICAL_SHA_LENGTH: Final = 40
_LOWER_HEX_DIGITS: Final = "0123456789abcdef"

# FD-PV-6 byte limits, with the FD-PV-12 axes made explicit. The aggregate
# values are the ratified derived maxima (exactly six times the per-artifact
# limits), so they are upper bounds.
#
# Compressed limits bind *archive* bytes and are enforced before or during
# download. Extracted limits bind *extracted regular-file* bytes and are
# enforced during bounded extraction. FD-PV-12: 1048576 is a compressed
# per-artifact limit and must never be reinterpreted as an extracted per-file
# limit. No general per-file 1 MiB extracted limit is ratified, and none is
# enforced anywhere in this module.
MAX_COMPRESSED_ARTIFACT_BYTES: Final = 1_048_576
MAX_EXTRACTED_ARTIFACT_BYTES: Final = 4_194_304
MAX_AGGREGATE_COMPRESSED_BYTES: Final = 6_291_456
MAX_AGGREGATE_EXTRACTED_BYTES: Final = 25_165_824

#: Bounded read granularity. Extraction never materializes a whole member in
#: memory and never trusts a declared size.
EXTRACTION_CHUNK_BYTES: Final = 65_536

ARCHIVE_SUFFIX: Final = ".zip"

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
    # FD-PV-12: only the per-artifact extracted total is bounded here. There is
    # deliberately no per-file extracted limit: a single regular file larger
    # than 1 MiB is acceptable while the artifact total stays within 4 MiB.
    total = sum(len(payloads[name]) for name in REQUIRED_FILES)
    if total > MAX_EXTRACTED_ARTIFACT_BYTES:
        raise ArtifactSizeLimitExceededError(f"{where} exceeds the per-artifact extracted limit")
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
        # FD-PV-12: the per-artifact extracted total is the only file-side bound.
        total += entry.stat().st_size
        if total > MAX_EXTRACTED_ARTIFACT_BYTES:
            raise ArtifactSizeLimitExceededError(
                f"{where} exceeds the per-artifact extracted limit"
            )
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
        # FD-PV-12: extracted bytes are bounded by the extracted aggregate limit
        # only. The compressed aggregate limit binds archive bytes and is
        # enforced against archives before and during download, never here.
        if extracted > MAX_AGGREGATE_EXTRACTED_BYTES:
            raise ArtifactSizeLimitExceededError("aggregate extracted limit exceeded")
        cells[cell] = payloads
    return cells


def require_canonical_sha(value: object) -> str:
    """Return ``value`` if it is exactly forty lowercase hexadecimal characters.

    FD-PV-14. The value must be supplied explicitly by the caller from the
    already guarded canonical-main dispatch input. This function is the only
    gate: uppercase, empty, short, long, non-hexadecimal, whitespace-padded,
    newline-bearing, ref, branch and tag values all fail closed through the
    existing ``evidence_generation_failure`` category. No twenty-second
    category is introduced.
    """
    if not isinstance(value, str):
        raise EvidenceGenerationFailureError("canonical_sha must be a string")
    if len(value) != CANONICAL_SHA_LENGTH:
        raise EvidenceGenerationFailureError(
            f"canonical_sha must be exactly {CANONICAL_SHA_LENGTH} characters"
        )
    if any(character not in _LOWER_HEX_DIGITS for character in value):
        raise EvidenceGenerationFailureError(
            "canonical_sha must be lowercase hexadecimal characters only"
        )
    return value


# --------------------------------------------------------------------------
# Bounded artifact handling (FD-PV-12, FD-PV-13)
#
# The workflow performs artifact metadata lookup and capped transport under
# ``actions: read``. This module is the second, independent line of defence: it
# never trusts declared metadata, opens only bounded local ZIP files, and
# performs no network access of any kind.
# --------------------------------------------------------------------------


def _reject_unsafe_member_name(name: str, *, where: str) -> None:
    """Reject any archive member name that is not a flat expected file name."""
    if name != name.strip() or not name:
        raise UnsafeArchiveEntryError(f"{where} has a blank or padded member name {name!r}")
    if name.endswith("/"):
        raise UnsafeArchiveEntryError(f"{where} contains a directory entry {name!r}")
    if "\\" in name:
        raise UnsafeArchiveEntryError(f"{where} member {name!r} contains a backslash")
    if name.startswith("/"):
        raise UnsafeArchiveEntryError(f"{where} member {name!r} is an absolute path")
    if len(name) >= 2 and name[1] == ":":
        raise UnsafeArchiveEntryError(f"{where} member {name!r} carries a drive prefix")
    parts = name.split("/")
    if len(parts) != 1:
        raise UnsafeArchiveEntryError(f"{where} member {name!r} is nested")
    if name in {".", ".."} or ".." in parts:
        raise UnsafeArchiveEntryError(f"{where} member {name!r} traverses its parent")
    if name not in REQUIRED_FILES:
        raise UnexpectedEvidenceFileError(f"{where} has unexpected member {name!r}")


def _require_regular_member(info: zipfile.ZipInfo, *, where: str) -> None:
    if info.is_dir():
        raise UnsafeArchiveEntryError(f"{where} member {info.filename!r} is a directory")
    mode = (info.external_attr >> 16) & 0o170000
    if mode == 0o120000:
        raise UnsafeArchiveEntryError(f"{where} member {info.filename!r} is a symbolic link")
    if mode not in (0, 0o100000):
        raise UnsafeArchiveEntryError(f"{where} member {info.filename!r} is not a regular file")


def inspect_archive(
    archive: Path,
    *,
    where: str,
    max_extracted_artifact: int = MAX_EXTRACTED_ARTIFACT_BYTES,
) -> list[zipfile.ZipInfo]:
    """Inspect archive structure **before** any output file is created.

    Every member is checked for safety and expectedness, and the declared
    uncompressed total is bounded, so a ZIP bomb is refused before extraction
    begins. Declared sizes are advisory only: extraction re-counts real bytes.
    """
    try:
        with zipfile.ZipFile(archive) as bundle:
            infos = list(bundle.infolist())
    except zipfile.BadZipFile as error:
        raise UnsafeArchiveEntryError(f"{where} is not a readable ZIP archive") from error
    except OSError as error:  # pragma: no cover - platform I/O defect
        raise AggregateVerifierInternalError(f"{where} could not be opened: {error!r}") from error

    seen: set[str] = set()
    declared = 0
    for info in infos:
        _reject_unsafe_member_name(info.filename, where=where)
        _require_regular_member(info, where=where)
        folded = info.filename.casefold()
        if folded in seen:
            raise UnsafeArchiveEntryError(f"{where} has a duplicate member {info.filename!r}")
        seen.add(folded)
        if info.file_size < 0:
            raise UnsafeArchiveEntryError(f"{where} member {info.filename!r} declares a bad size")
        declared += info.file_size
    missing = sorted(set(REQUIRED_FILES) - {info.filename for info in infos})
    if missing:
        raise MissingEvidenceFileError(f"{where} is missing {missing}")
    if len(infos) != len(REQUIRED_FILES):
        raise UnexpectedEvidenceFileError(
            f"{where} must contain exactly {len(REQUIRED_FILES)} regular files"
        )
    if declared > max_extracted_artifact:
        raise ArtifactSizeLimitExceededError(
            f"{where} declares {declared} extracted bytes, above the per-artifact limit"
        )
    return infos


def extract_archive_bounded(
    archive: Path,
    destination: Path,
    *,
    where: str,
    max_extracted_artifact: int = MAX_EXTRACTED_ARTIFACT_BYTES,
    aggregate_budget: int = MAX_AGGREGATE_EXTRACTED_BYTES,
) -> int:
    """Extract one inspected archive through bounded chunked reads.

    Returns the exact number of extracted regular-file bytes. Both the
    per-artifact limit and the remaining aggregate budget are enforced *during*
    the read, never afterwards: the moment either would be exceeded the read
    stops, every file written for this artifact is removed, and the run fails
    closed. No file is left fully written once a limit is crossed.
    """
    infos = inspect_archive(archive, where=where, max_extracted_artifact=max_extracted_artifact)
    destination.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    try:
        # The whole streaming read happens inside this helper so that every file
        # handle is closed before any cleanup runs. Windows refuses to unlink an
        # open file, which would otherwise leave a partial output behind.
        extracted = _stream_members_bounded(
            archive,
            destination,
            infos,
            written,
            where=where,
            max_extracted_artifact=max_extracted_artifact,
            aggregate_budget=aggregate_budget,
        )
    except PortabilityError:
        _remove_partial_outputs(written)
        raise
    except (zipfile.BadZipFile, zlib.error, EOFError) as error:
        _remove_partial_outputs(written)
        raise UnsafeArchiveEntryError(f"{where} is a corrupt or truncated ZIP archive") from error
    except OSError as error:
        _remove_partial_outputs(written)
        raise AggregateVerifierInternalError(f"{where} extraction failed: {error!r}") from error
    return extracted


def _stream_members_bounded(
    archive: Path,
    destination: Path,
    infos: Sequence[zipfile.ZipInfo],
    written: list[Path],
    *,
    where: str,
    max_extracted_artifact: int,
    aggregate_budget: int,
) -> int:
    extracted = 0
    with zipfile.ZipFile(archive) as bundle:
        for info in sorted(infos, key=lambda item: item.filename):
            target = destination / info.filename
            if target.exists() or target.is_symlink():
                raise UnsafeArchiveEntryError(
                    f"{where} member {info.filename!r} would overwrite an existing path"
                )
            written.append(target)
            with bundle.open(info) as source, target.open("wb") as sink:
                while True:
                    chunk = source.read(EXTRACTION_CHUNK_BYTES)
                    if not chunk:
                        break
                    extracted += len(chunk)
                    if extracted > max_extracted_artifact:
                        raise ArtifactSizeLimitExceededError(
                            f"{where} exceeds the per-artifact extracted limit"
                        )
                    if extracted > aggregate_budget:
                        raise ArtifactSizeLimitExceededError(
                            "aggregate extracted limit exceeded during extraction"
                        )
                    sink.write(chunk)
    return extracted


def _remove_partial_outputs(written: Iterable[Path]) -> None:
    for path in written:
        with contextlib.suppress(OSError):  # best-effort cleanup
            path.unlink(missing_ok=True)


def collect_archive_paths(archives_dir: Path) -> dict[str, Path]:
    """Map each expected artifact name to its local archive, fail-closed."""
    if not archives_dir.is_dir():
        raise MissingMatrixCellError("archive root is not a directory")
    found: dict[str, Path] = {}
    names: list[str] = []
    for entry in sorted(archives_dir.iterdir(), key=lambda item: item.name):
        if entry.is_symlink() or not entry.is_file():
            raise UnsafeArchiveEntryError(f"archive entry {entry.name!r} is not a regular file")
        if entry.suffix != ARCHIVE_SUFFIX:
            raise UnexpectedMatrixCellError(f"unexpected archive {entry.name!r}")
        names.append(entry.stem)
        found[entry.stem] = entry
    check_artifact_names(names)
    return found


def enforce_compressed_limits(
    archives: Mapping[str, Path],
    *,
    declared_sizes: Mapping[str, int] | None = None,
    max_compressed_artifact: int = MAX_COMPRESSED_ARTIFACT_BYTES,
    max_aggregate_compressed: int = MAX_AGGREGATE_COMPRESSED_BYTES,
) -> int:
    """Bound archive bytes on disk, independently of any declared metadata.

    The workflow already refuses oversized artifacts from run metadata and caps
    the bytes it will read during transport. This re-check exists because
    metadata alone is never a sufficient defence: a server that under-reports a
    size, or a truncated or padded transfer, must still fail closed here.
    """
    total = 0
    for name in sorted(archives):
        actual = archives[name].stat().st_size
        if actual > max_compressed_artifact:
            raise ArtifactSizeLimitExceededError(
                f"{name} archive is {actual} bytes, above the per-artifact compressed limit"
            )
        if declared_sizes is not None:
            declared = declared_sizes.get(name)
            if declared is None or declared != actual:
                raise ArtifactSizeLimitExceededError(
                    f"{name} archive size {actual} does not match declared {declared}"
                )
        total += actual
        if total > max_aggregate_compressed:
            raise ArtifactSizeLimitExceededError("aggregate compressed limit exceeded")
    return total


def extract_all_bounded(
    archives_dir: Path,
    extract_root: Path,
    *,
    declared_sizes: Mapping[str, int] | None = None,
    max_compressed_artifact: int = MAX_COMPRESSED_ARTIFACT_BYTES,
    max_aggregate_compressed: int = MAX_AGGREGATE_COMPRESSED_BYTES,
    max_extracted_artifact: int = MAX_EXTRACTED_ARTIFACT_BYTES,
    max_aggregate_extracted: int = MAX_AGGREGATE_EXTRACTED_BYTES,
) -> Path:
    """Run the full bounded pipeline: cardinality, compressed bounds, extraction.

    Order matters and is fail-closed at every step: exactly the six expected
    archives, compressed limits before anything is opened, structural inspection
    before any output file exists, then bounded chunked extraction that enforces
    the per-artifact and aggregate extracted limits while bytes are read.
    """
    archives = collect_archive_paths(archives_dir)
    enforce_compressed_limits(
        archives,
        declared_sizes=declared_sizes,
        max_compressed_artifact=max_compressed_artifact,
        max_aggregate_compressed=max_aggregate_compressed,
    )
    extract_root.mkdir(parents=True, exist_ok=True)
    extracted_total = 0
    for name in ARTIFACT_NAMES:
        remaining = max_aggregate_extracted - extracted_total
        extracted_total += extract_archive_bounded(
            archives[name],
            extract_root / name,
            where=name,
            max_extracted_artifact=max_extracted_artifact,
            aggregate_budget=remaining,
        )
    return extract_root


def aggregate_from_archives(
    archives_dir: Path,
    extract_root: Path,
    *,
    canonical_sha: str | None = None,
    declared_sizes: Mapping[str, int] | None = None,
) -> bytes:
    """Bounded-extract six local archives, then verify and emit the envelope."""
    if canonical_sha is not None:
        require_canonical_sha(canonical_sha)
    try:
        root = extract_all_bounded(archives_dir, extract_root, declared_sizes=declared_sizes)
    except PortabilityError:
        raise
    except Exception as error:  # a transport defect must fail closed, never pass
        raise AggregateVerifierInternalError(f"bounded extraction failed: {error!r}") from error
    return aggregate(root, canonical_sha=canonical_sha)


def build_evidence(
    cells: Mapping[str, Mapping[str, bytes]],
    *,
    canonical_sha: str | None = None,
) -> bytes:
    """Return the deterministic evidence envelope for a fully passing comparison.

    ``canonical_sha`` is present only when the caller supplies it, which happens
    only for a guarded canonical-main ``workflow_dispatch`` run. On a
    pull-request run the caller passes nothing and the key is omitted entirely —
    never serialized as null, blank, placeholder or sentinel.
    """
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
    if canonical_sha is not None:
        document[CANONICAL_SHA_KEY] = require_canonical_sha(canonical_sha)
    reject_forbidden_keys(document)
    return canonical_json_bytes(document)


def aggregate(root: Path, *, canonical_sha: str | None = None) -> bytes:
    """Verify six extracted per-cell directories and return the evidence bytes.

    Every structural, encoding, manifest, digest, size and cross-cell byte check
    must pass before an envelope exists.  Any internal failure is converted to a
    typed aggregate error so a verifier defect can never produce a pass.

    ``canonical_sha`` is threaded explicitly from the guarded canonical-main
    dispatch input. It is never read from ``GITHUB_SHA``, a ref, a branch name,
    a tag, ``git`` output, or any other environment value: this module imports
    neither ``os`` nor ``subprocess``, so no such fallback exists.
    """
    if canonical_sha is not None:
        require_canonical_sha(canonical_sha)
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
        evidence = build_evidence(cells, canonical_sha=canonical_sha)
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


def load_declared_sizes(source: str | None) -> dict[str, int] | None:
    """Load the workflow-recorded archive sizes, if the workflow supplied them.

    The file is written by the workflow from current-run artifact metadata. It
    is advisory: every value is re-checked against the bytes actually on disk,
    and a mismatch fails closed.
    """
    if source is None:
        return None
    try:
        document = json.loads(Path(source).read_bytes())
    except (OSError, ValueError) as error:
        raise ArtifactSizeLimitExceededError(
            f"declared archive sizes could not be read: {error!r}"
        ) from error
    if not isinstance(document, dict):
        raise ArtifactSizeLimitExceededError("declared archive sizes must be a JSON object")
    sizes: dict[str, int] = {}
    for key, value in document.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ArtifactSizeLimitExceededError(f"declared size for {key!r} is not a byte count")
        sizes[str(key)] = value
    return sizes


def _cmd_aggregate(args: argparse.Namespace) -> int:
    # ``--canonical-sha`` is threaded straight through from the guarded dispatch
    # input. When the flag is absent the value stays ``None`` and the envelope
    # omits the key entirely; an explicitly empty value fails closed.
    if args.archives is not None:
        evidence = aggregate_from_archives(
            Path(args.archives),
            Path(args.extract_root),
            canonical_sha=args.canonical_sha,
            declared_sizes=load_declared_sizes(args.declared_sizes),
        )
    else:
        evidence = aggregate(Path(args.root), canonical_sha=args.canonical_sha)
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
    source = agg.add_mutually_exclusive_group(required=True)
    source.add_argument("--root", help="directory of six already-extracted cell directories")
    source.add_argument(
        "--archives",
        help="directory of exactly six bounded local artifact ZIP archives",
    )
    agg.add_argument(
        "--extract-root",
        default="extracted",
        help="destination for bounded extraction when --archives is used",
    )
    agg.add_argument(
        "--declared-sizes",
        default=None,
        help="JSON file of artifact-name to archive byte size from current-run metadata",
    )
    agg.add_argument("--evidence-out", required=True)
    agg.add_argument(
        "--canonical-sha",
        default=None,
        help=(
            "exact guarded canonical-main commit SHA; canonical-main dispatch runs only. "
            "Omit entirely on pull-request runs."
        ),
    )
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
