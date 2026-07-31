"""Tests for the private B2A portability harness (FD-PV-1..10).

Every one of the twenty-one ratified failure categories has an explicit
fail-closed negative test, named after the exact category identifier.

All fixtures are synthetic, bounded, and in-memory or under ``tmp_path``. No
test requires a real multi-platform run, real GitHub artifacts, the network, a
model, or a dataset. Passing this suite is infrastructure validation only — it
is not portability evidence and does not accept B2A.
"""

from __future__ import annotations

import builtins
import json
import os
import shutil
import socket
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _mesc_b2a_portability as h

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _payloads() -> dict[str, bytes]:
    return h.build_artifact_payloads()


def _write_cell(root: Path, cell: str, payloads: dict[str, bytes]) -> Path:
    cell_dir = root / f"{h.ARTIFACT_PREFIX}{cell}"
    cell_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in payloads.items():
        (cell_dir / name).write_bytes(payload)
    return cell_dir


def _six_cells(root: Path, payloads: dict[str, bytes] | None = None) -> Path:
    data = payloads if payloads is not None else _payloads()
    for cell in h.CELL_IDS:
        _write_cell(root, cell, data)
    return root


def _variant_payloads() -> dict[str, bytes]:
    """Internally consistent payloads whose content differs from the canonical set."""
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes, canonical_jsonl_bytes

    json_payload = canonical_json_bytes({"variant": 1})
    jsonl_payload = canonical_jsonl_bytes([{"variant": 2}])
    return {
        h.CANONICAL_JSON_NAME: json_payload,
        h.CANONICAL_JSONL_NAME: jsonl_payload,
        h.MANIFEST_NAME: h.build_manifest(json_payload, jsonl_payload),
    }


# --------------------------------------------------------------------------
# Taxonomy completeness
# --------------------------------------------------------------------------

EXPECTED_TAXONOMY = (
    "missing_matrix_cell",
    "duplicate_matrix_cell",
    "unexpected_matrix_cell",
    "missing_evidence_file",
    "unexpected_evidence_file",
    "manifest_schema_mismatch",
    "invalid_sha256",
    "byte_size_mismatch",
    "content_hash_mismatch",
    "cross_platform_byte_mismatch",
    "forbidden_runtime_metadata",
    "noncanonical_manifest",
    "evidence_generation_failure",
    "bom_present",
    "malformed_utf8",
    "invalid_json",
    "invalid_jsonl",
    "duplicate_json_object_key",
    "aggregate_verifier_internal_error",
    "unsafe_archive_entry",
    "artifact_size_limit_exceeded",
)


def test_taxonomy_is_exactly_the_ratified_twenty_one() -> None:
    assert set(h.iter_taxonomy_codes()) == set(EXPECTED_TAXONOMY)
    assert len(EXPECTED_TAXONOMY) == 21
    assert len(h.TAXONOMY) == 21


def test_every_taxonomy_error_is_fail_closed() -> None:
    for error in h.TAXONOMY:
        assert issubclass(error, h.PortabilityError)
        assert error.code == error.code.lower()
        assert " " not in error.code


# --------------------------------------------------------------------------
# Positive determinism
# --------------------------------------------------------------------------


def test_generation_creates_exactly_three_files(tmp_path: Path) -> None:
    h.generate(tmp_path / "cell")
    assert sorted(p.name for p in (tmp_path / "cell").iterdir()) == sorted(h.REQUIRED_FILES)


def test_repeated_generation_is_byte_identical(tmp_path: Path) -> None:
    first = h.generate(tmp_path / "a")
    second = h.generate(tmp_path / "b")
    assert first == second
    assert h.build_artifact_payloads() == first


def test_canonical_json_and_jsonl_equality_against_serializer() -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes, canonical_jsonl_bytes

    payloads = _payloads()
    assert payloads[h.CANONICAL_JSON_NAME] == canonical_json_bytes(h.SYNTHETIC_DOCUMENT)
    assert payloads[h.CANONICAL_JSONL_NAME] == canonical_jsonl_bytes(h.SYNTHETIC_RECORDS)


def test_manifest_is_deterministic_and_recomputed_from_bytes() -> None:
    from medscale.mesc._canonical_json_v1 import sha256_of_bytes

    payloads = _payloads()
    document = json.loads(payloads[h.MANIFEST_NAME])
    assert document["schema_version"] == h.MANIFEST_SCHEMA
    for entry in document["files"]:
        actual = payloads[entry["name"]]
        assert entry["sha256"] == sha256_of_bytes(actual)
        assert entry["byte_size"] == len(actual)


def test_artifacts_are_lf_only_utf8_without_bom() -> None:
    for payload in _payloads().values():
        assert b"\r" not in payload
        assert not payload.startswith(b"\xef\xbb\xbf")
        payload.decode("utf-8")


def test_json_has_exactly_one_terminal_lf() -> None:
    payload = _payloads()[h.CANONICAL_JSON_NAME]
    assert payload.endswith(b"\n")
    assert payload.count(b"\n") == 1


def test_unicode_nfc_and_nfd_remain_distinct() -> None:
    payload = _payloads()[h.CANONICAL_JSON_NAME]
    assert "é".encode() in payload
    assert "é".encode() in payload
    assert "日本語".encode() in payload


def test_large_integer_survives_unchanged() -> None:
    payload = _payloads()[h.CANONICAL_JSON_NAME]
    assert b"12345678901234567890123456789" in payload


def test_float_prohibition_is_inherited_from_the_serializer() -> None:
    from medscale.mesc._canonical_json_v1 import (
        FloatingPointValueProhibitedError,
        canonical_json_bytes,
    )

    with pytest.raises(FloatingPointValueProhibitedError):
        canonical_json_bytes({"k": 1.5})


def test_aggregate_over_six_identical_cells_passes(tmp_path: Path) -> None:
    evidence = h.aggregate(_six_cells(tmp_path))
    document = json.loads(evidence)
    assert document["result"] == "pass"
    assert document["cells"] == list(h.CELL_IDS)
    assert [entry["name"] for entry in document["files"]] == list(h.REQUIRED_FILES)


def test_evidence_envelope_bytes_are_deterministic(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    assert h.aggregate(root) == h.aggregate(root)


def test_evidence_envelope_records_the_six_ratified_cell_identifiers(tmp_path: Path) -> None:
    # spec.md §10 requires the envelope to record the six expected cell
    # identifiers. Those are ratified constants, not runtime-derived values.
    document = json.loads(h.aggregate(_six_cells(tmp_path)))
    assert document["cells"] == list(h.CELL_IDS)


def test_evidence_envelope_excludes_runtime_derived_metadata(tmp_path: Path) -> None:
    # The prohibition targets environment-derived provenance, not the ratified
    # cell identifiers, which legitimately encode OS family and Python minor
    # version as frozen constants.
    #
    # Regression guard: on Linux ``sys.platform == "linux"``, which is a
    # substring of the ratified identifiers ``linux-py3.11`` and
    # ``linux-py3.12``. Scanning the whole envelope would therefore fail purely
    # because those required identifiers are present. Excluding the ratified
    # ``cells`` field first keeps the runtime-provenance prohibition strict
    # everywhere else, on every platform, with no OS-specific special case.
    document = json.loads(h.aggregate(_six_cells(tmp_path)))
    assert document["cells"] == list(h.CELL_IDS)
    provenance_free_document = {key: value for key, value in document.items() if key != "cells"}
    lowered = (
        json.dumps(provenance_free_document, sort_keys=True, separators=(",", ":"))
        .encode("utf-8")
        .lower()
    )
    for forbidden in (
        b"timestamp",
        b"created",
        b"hostname",
        b"username",
        b"runner",
        b"image",
        b"workflow",
        b"run_id",
        b"http",
        b"secret",
        b"cwd",
        b"environ",
        sys.version.split()[0].encode(),
        sys.platform.encode(),
    ):
        assert forbidden not in lowered


def test_compared_artifacts_exclude_environment_and_platform_metadata() -> None:
    joined = b"".join(_payloads().values()).lower()
    for forbidden in (b"ubuntu", b"windows", b"macos", b"python", b"runner", b"3.11", b"3.12"):
        assert forbidden not in joined


# --------------------------------------------------------------------------
# The twenty-one ratified failure categories
# --------------------------------------------------------------------------


def test_missing_matrix_cell(tmp_path: Path) -> None:
    for cell in h.CELL_IDS[:-1]:
        _write_cell(tmp_path, cell, _payloads())
    with pytest.raises(h.MissingMatrixCellError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "missing_matrix_cell"


def test_duplicate_matrix_cell() -> None:
    names = [*(f"{h.ARTIFACT_PREFIX}{c}" for c in h.CELL_IDS), h.ARTIFACT_NAMES[0]]
    with pytest.raises(h.DuplicateMatrixCellError) as excinfo:
        h.check_artifact_names(names)
    assert excinfo.value.code == "duplicate_matrix_cell"


def test_duplicate_matrix_cell_by_case_collision() -> None:
    names = [*h.ARTIFACT_NAMES[1:], h.ARTIFACT_NAMES[0], h.ARTIFACT_NAMES[0].upper()]
    with pytest.raises(h.DuplicateMatrixCellError):
        h.check_artifact_names(names)


def test_unexpected_matrix_cell(tmp_path: Path) -> None:
    _six_cells(tmp_path)
    (tmp_path / "b2a-portability-solaris-py3.11").mkdir()
    with pytest.raises(h.UnexpectedMatrixCellError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "unexpected_matrix_cell"


def test_missing_evidence_file(tmp_path: Path) -> None:
    _six_cells(tmp_path)
    (tmp_path / h.ARTIFACT_NAMES[0] / h.MANIFEST_NAME).unlink()
    with pytest.raises(h.MissingEvidenceFileError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "missing_evidence_file"


def test_unexpected_evidence_file(tmp_path: Path) -> None:
    _six_cells(tmp_path)
    (tmp_path / h.ARTIFACT_NAMES[0] / "extra.txt").write_bytes(b"x")
    with pytest.raises(h.UnexpectedEvidenceFileError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "unexpected_evidence_file"


def test_manifest_schema_mismatch(tmp_path: Path) -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    payloads = _payloads()
    payloads[h.MANIFEST_NAME] = canonical_json_bytes({"schema_version": "wrong/9", "files": []})
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.ManifestSchemaMismatchError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "manifest_schema_mismatch"


def test_invalid_sha256(tmp_path: Path) -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    payloads = _payloads()
    document = json.loads(payloads[h.MANIFEST_NAME])
    document["files"][0]["sha256"] = "NOTHEX"
    payloads[h.MANIFEST_NAME] = canonical_json_bytes(document)
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.InvalidSha256Error) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "invalid_sha256"


def test_byte_size_mismatch(tmp_path: Path) -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    payloads = _payloads()
    document = json.loads(payloads[h.MANIFEST_NAME])
    document["files"][0]["byte_size"] = int(document["files"][0]["byte_size"]) + 1
    payloads[h.MANIFEST_NAME] = canonical_json_bytes(document)
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.ByteSizeMismatchError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "byte_size_mismatch"


def test_content_hash_mismatch(tmp_path: Path) -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    payloads = _payloads()
    document = json.loads(payloads[h.MANIFEST_NAME])
    document["files"][0]["sha256"] = "0" * 64
    payloads[h.MANIFEST_NAME] = canonical_json_bytes(document)
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.ContentHashMismatchError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "content_hash_mismatch"


def test_cross_platform_byte_mismatch(tmp_path: Path) -> None:
    for cell in h.CELL_IDS[:-1]:
        _write_cell(tmp_path, cell, _payloads())
    _write_cell(tmp_path, h.CELL_IDS[-1], _variant_payloads())
    with pytest.raises(h.CrossPlatformByteMismatchError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "cross_platform_byte_mismatch"


def test_forbidden_runtime_metadata() -> None:
    for key in ("python_version", "runner_os", "hostname", "created_at", "workspace_path"):
        with pytest.raises(h.ForbiddenRuntimeMetadataError) as excinfo:
            h.reject_forbidden_keys({key: "x"})
        assert excinfo.value.code == "forbidden_runtime_metadata"


def test_noncanonical_manifest(tmp_path: Path) -> None:
    payloads = _payloads()
    payloads[h.MANIFEST_NAME] = payloads[h.MANIFEST_NAME].replace(b'{"', b'{ "', 1)
    _six_cells(tmp_path, payloads)
    # A space after the opening brace is still valid JSON, so the parse
    # succeeds and the canonical-bytes comparison is what fails. Exactly one
    # category applies.
    with pytest.raises(h.NoncanonicalManifestError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "noncanonical_manifest"


def test_evidence_generation_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    root = _six_cells(tmp_path)
    monkeypatch.setattr(
        h,
        "build_evidence",
        lambda cells, *, canonical_sha=None: canonical_json_bytes({"result": "no"}),
    )
    with pytest.raises(h.EvidenceGenerationFailureError) as excinfo:
        h.aggregate(root)
    assert excinfo.value.code == "evidence_generation_failure"


def test_bom_present(tmp_path: Path) -> None:
    payloads = _payloads()
    payloads[h.CANONICAL_JSON_NAME] = b"\xef\xbb\xbf" + payloads[h.CANONICAL_JSON_NAME]
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.BomPresentError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "bom_present"


def test_malformed_utf8(tmp_path: Path) -> None:
    payloads = _payloads()
    payloads[h.CANONICAL_JSON_NAME] = b'{"k":"\xff\xfe"}\n'
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.MalformedUtf8Error) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "malformed_utf8"


def test_invalid_json(tmp_path: Path) -> None:
    payloads = _payloads()
    payloads[h.CANONICAL_JSON_NAME] = b"{not json}\n"
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.InvalidJsonError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "invalid_json"


@pytest.mark.parametrize(
    "payload",
    [b'{"a":1}', b'{"a":1}\r\n', b'{"a":1}\n\n{"b":2}\n', b"notjson\n", b"[1,2]\n"],
)
def test_invalid_jsonl(tmp_path: Path, payload: bytes) -> None:
    payloads = _payloads()
    payloads[h.CANONICAL_JSONL_NAME] = payload
    root = tmp_path / payload.hex()[:12]
    _six_cells(root, payloads)
    with pytest.raises(h.InvalidJsonlError) as excinfo:
        h.aggregate(root)
    assert excinfo.value.code == "invalid_jsonl"


def test_duplicate_json_object_key(tmp_path: Path) -> None:
    payloads = _payloads()
    payloads[h.CANONICAL_JSON_NAME] = b'{"a":1,"a":2}\n'
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.DuplicateJsonObjectKeyError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "duplicate_json_object_key"


def test_duplicate_json_object_key_is_not_last_wins() -> None:
    with pytest.raises(h.DuplicateJsonObjectKeyError):
        h.parse_strict_json(b'{"a":1,"a":2}\n', where="probe")


def test_aggregate_verifier_internal_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _six_cells(tmp_path)

    def boom(cells: object, *, canonical_sha: str | None = None) -> bytes:
        raise RuntimeError("verifier defect")

    monkeypatch.setattr(h, "build_evidence", boom)
    with pytest.raises(h.AggregateVerifierInternalError) as excinfo:
        h.aggregate(root)
    assert excinfo.value.code == "aggregate_verifier_internal_error"


def test_unsafe_archive_entry_nested_directory(tmp_path: Path) -> None:
    _six_cells(tmp_path)
    (tmp_path / h.ARTIFACT_NAMES[0] / "nested").mkdir()
    # The per-entry safety check runs before the name-set checks, so a directory
    # entry is rejected as a non-regular file. Exactly one category applies.
    with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "unsafe_archive_entry"


def test_unsafe_archive_entry_non_directory_artifact(tmp_path: Path) -> None:
    _six_cells(tmp_path)
    (tmp_path / "loose-file.txt").write_bytes(b"x")
    with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "unsafe_archive_entry"


def test_unsafe_archive_entry_symlink(tmp_path: Path) -> None:
    _six_cells(tmp_path)
    target = tmp_path / "outside.txt"
    target.write_bytes(b"x")
    link = tmp_path / h.ARTIFACT_NAMES[0] / "link.json"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is not permitted on this platform")
    with pytest.raises(h.UnsafeArchiveEntryError):
        h.aggregate(tmp_path)


def test_artifact_size_limit_exceeded(tmp_path: Path) -> None:
    # FD-PV-12: the bound is the per-artifact extracted total, not a per-file
    # limit, so the fixture must exceed 4 MiB across the artifact.
    payloads = _payloads()
    payloads[h.CANONICAL_JSON_NAME] = b"x" * (h.MAX_EXTRACTED_ARTIFACT_BYTES + 1)
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code == "artifact_size_limit_exceeded"


# --------------------------------------------------------------------------
# Mutation detection and structural rejection
# --------------------------------------------------------------------------


def test_one_byte_mutation_fails_closed(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    target = root / h.ARTIFACT_NAMES[3] / h.CANONICAL_JSON_NAME
    raw = bytearray(target.read_bytes())
    raw[7] ^= 0x01
    target.write_bytes(bytes(raw))
    with pytest.raises(h.PortabilityError):
        h.aggregate(root)


def test_crlf_mutation_fails_closed(tmp_path: Path) -> None:
    payloads = _payloads()
    payloads[h.CANONICAL_JSONL_NAME] = payloads[h.CANONICAL_JSONL_NAME].replace(b"\n", b"\r\n")
    _six_cells(tmp_path, payloads)
    with pytest.raises(h.PortabilityError):
        h.aggregate(tmp_path)


def test_no_evidence_envelope_is_produced_on_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _six_cells(tmp_path)
    (root / h.ARTIFACT_NAMES[2] / h.CANONICAL_JSON_NAME).unlink()
    called: list[str] = []
    original = h.build_evidence

    def spy(cells: object, *, canonical_sha: str | None = None) -> bytes:
        called.append("x")
        return original(cells, canonical_sha=canonical_sha)  # type: ignore[arg-type]

    monkeypatch.setattr(h, "build_evidence", spy)
    with pytest.raises(h.PortabilityError):
        h.aggregate(root)
    assert called == []


def test_traversal_and_absolute_paths_are_rejected(tmp_path: Path) -> None:
    """Executes the real member-name guard instead of asserting on literals."""
    for name in ("../escape.json", "/abs.json", "..\\escape.json", "C:/abs.json"):
        archive = tmp_path / f"{abs(hash(name))}.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            for required in h.REQUIRED_FILES:
                bundle.writestr(required, b"{}")
            bundle.writestr(name, b"payload")
        destination = tmp_path / f"out-{abs(hash(name))}"
        with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
            h.extract_archive_bounded(archive, destination, where="cell")
        assert excinfo.value.code == "unsafe_archive_entry"
        assert not destination.exists() or list(destination.iterdir()) == []


# --------------------------------------------------------------------------
# Boundary: no network, no model, no dataset, no public surface
# --------------------------------------------------------------------------


def test_no_network_access(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("the portability harness must not touch the network")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    h.generate(tmp_path / "cell")
    h.aggregate(_six_cells(tmp_path / "root"))


def test_no_model_or_dataset_import(monkeypatch: pytest.MonkeyPatch) -> None:
    real_import = builtins.__import__
    blocked = {"torch", "transformers", "datasets", "llama_cpp", "requests", "httpx", "urllib3"}

    def guarded(name: str, *args: object, **kwargs: object) -> object:
        if name.split(".")[0] in blocked:
            raise AssertionError(f"harness must not import {name}")
        return real_import(name, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(builtins, "__import__", guarded)
    h.build_artifact_payloads()


def test_harness_imports_only_the_allowed_surface() -> None:
    import ast

    source = Path(h.__file__).read_text(encoding="utf-8")
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported.add(node.module.split(".")[0])
    assert imported <= {
        "__future__",
        "argparse",
        "contextlib",
        "json",
        "sys",
        "zipfile",
        "zlib",
        "collections",
        "pathlib",
        "typing",
        "medscale",
    }


def test_harness_adds_no_public_medscale_export() -> None:
    import medscale.mesc as mesc

    for name in ("generate", "aggregate", "build_evidence", "PortabilityError", "CELL_IDS"):
        assert name not in mesc.__all__
        assert not hasattr(mesc, name)


def test_cell_ids_and_artifact_names_are_exactly_ratified() -> None:
    assert set(h.CELL_IDS) == {
        "linux-py3.11",
        "linux-py3.12",
        "windows-py3.11",
        "windows-py3.12",
        "macos-py3.11",
        "macos-py3.12",
    }
    assert len(h.CELL_IDS) == 6
    assert tuple(f"b2a-portability-{c}" for c in h.CELL_IDS) == h.ARTIFACT_NAMES


def test_fd_pv_6_values_are_unchanged() -> None:
    # The four ratified byte values, unchanged by remediation. Their axes are
    # asserted separately in test_fd_pv_6_limits_and_axes_are_exact.
    assert h.MAX_COMPRESSED_ARTIFACT_BYTES == 1_048_576
    assert h.MAX_EXTRACTED_ARTIFACT_BYTES == 4_194_304
    assert h.MAX_AGGREGATE_COMPRESSED_BYTES == 6_291_456
    assert h.MAX_AGGREGATE_EXTRACTED_BYTES == 25_165_824


# --------------------------------------------------------------------------
# Canonical-main dispatch guard (logic testable without GitHub Actions)
# --------------------------------------------------------------------------


def test_dispatch_guard_requires_main_ref_and_exact_sha() -> None:
    """The workflow guard is expressed as a pure predicate here.

    The workflow itself fails closed unless the ref is refs/heads/main and the
    checked-out HEAD equals the required expected_sha input.
    """

    def admissible(ref: str, head: str, expected: str) -> bool:
        return ref == "refs/heads/main" and head == expected and bool(expected)

    sha = "f71c6abf2b2f905f605951605efd6c8ab016523e"
    assert admissible("refs/heads/main", sha, sha)
    assert not admissible("refs/heads/other", sha, sha)
    assert not admissible("refs/heads/main", sha, "0" * 40)
    assert not admissible("refs/heads/main", sha, "")


# --------------------------------------------------------------------------
# FD-PV-14 — canonical SHA binding in the evidence envelope
# --------------------------------------------------------------------------

VALID_CANONICAL_SHA = "3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9"

MALFORMED_CANONICAL_SHAS = (
    "3A0FD67C8433BD25EAB77C05B44AA84A3A86DDB9",  # uppercase
    "3a0fd67c8433bd25eab77c05b44aa84a3a86DDB9",  # mixed case
    "",  # empty
    "3a0fd67c8433bd25eab77c05b44aa84a3a86ddb",  # 39 characters
    "3a0fd67c8433bd25eab77c05b44aa84a3a86ddb99",  # 41 characters
    "abc",  # far too short
    "0" * 64,  # far too long
    "3a0fd67c8433bd25eab77c05b44aa84a3a86ddbz",  # non-hexadecimal
    "3a0fd67c-8433-bd25-eab7-7c05b44aa84a3a86",  # punctuation
    "refs/heads/main",  # full ref
    "main",  # branch name
    "v0.2.0",  # tag name
    "refs/tags/v0.2.0",  # full tag ref
    " 3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9",  # leading whitespace
    "3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9 ",  # trailing whitespace
    "3a0fd67c8433bd25eab77c05b44aa84a3a86ddb\n",  # newline
    "3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9\n",  # 41 with newline
)


def test_canonical_sha_is_accepted_and_recorded_on_dispatch(tmp_path: Path) -> None:
    document = json.loads(h.aggregate(_six_cells(tmp_path), canonical_sha=VALID_CANONICAL_SHA))
    assert document[h.CANONICAL_SHA_KEY] == VALID_CANONICAL_SHA
    assert document["schema_version"] == "mesc-pilot-01-b2a-portability-evidence/1"


def test_pull_request_envelope_omits_the_canonical_sha_key_entirely(tmp_path: Path) -> None:
    evidence = h.aggregate(_six_cells(tmp_path))
    document = json.loads(evidence)
    assert h.CANONICAL_SHA_KEY not in document
    # Not null, not blank, not a placeholder: the key is absent from the bytes.
    assert b"canonical_sha" not in evidence


@pytest.mark.parametrize("value", MALFORMED_CANONICAL_SHAS)
def test_malformed_canonical_sha_fails_closed(tmp_path: Path, value: str) -> None:
    root = _six_cells(tmp_path / "root")
    with pytest.raises(h.EvidenceGenerationFailureError) as excinfo:
        h.aggregate(root, canonical_sha=value)
    assert excinfo.value.code == "evidence_generation_failure"


@pytest.mark.parametrize("value", MALFORMED_CANONICAL_SHAS)
def test_malformed_canonical_sha_is_rejected_by_the_validator(value: str) -> None:
    with pytest.raises(h.EvidenceGenerationFailureError):
        h.require_canonical_sha(value)


def test_non_string_canonical_sha_fails_closed() -> None:
    values: tuple[object, ...] = (
        None,
        0,
        3.5,
        True,
        [VALID_CANONICAL_SHA],
        {"sha": VALID_CANONICAL_SHA},
        VALID_CANONICAL_SHA.encode(),
    )
    for value in values:
        with pytest.raises(h.EvidenceGenerationFailureError):
            h.require_canonical_sha(value)


def test_malformed_canonical_sha_produces_no_envelope(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    out = tmp_path / "evidence" / h.EVIDENCE_NAME
    assert (
        h.main(
            [
                "aggregate",
                "--root",
                str(root),
                "--evidence-out",
                str(out),
                "--canonical-sha",
                "refs/heads/main",
            ]
        )
        == 1
    )
    assert not out.exists()


def test_canonical_sha_never_falls_back_to_an_environment_value(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No uncontrolled environment value may supply the field.

    Every plausible source is populated with a decoy that is itself a valid
    forty-character lowercase SHA, so a fallback would silently succeed rather
    than error. The envelope must still omit the key.
    """
    decoy = "b" * 40
    for name in (
        "GITHUB_SHA",
        "GITHUB_REF",
        "GITHUB_REF_NAME",
        "GITHUB_HEAD_REF",
        "GITHUB_BASE_REF",
        "GITHUB_WORKFLOW_SHA",
        "CANONICAL_SHA",
        "EXPECTED_SHA",
    ):
        monkeypatch.setenv(name, decoy)
    evidence = h.aggregate(_six_cells(tmp_path))
    assert h.CANONICAL_SHA_KEY not in json.loads(evidence)
    assert decoy.encode() not in evidence


def test_harness_cannot_read_the_environment_or_shell_out() -> None:
    """The helper has no mechanism to infer the SHA: no os, no subprocess."""
    import ast

    source = Path(h.__file__).read_text(encoding="utf-8")
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported.add(node.module.split(".")[0])
    assert "os" not in imported
    assert "subprocess" not in imported
    assert "platform" not in imported


def test_canonical_sha_serialization_is_stable_and_order_independent(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    first = h.aggregate(root, canonical_sha=VALID_CANONICAL_SHA)
    second = h.aggregate(root, canonical_sha=VALID_CANONICAL_SHA)
    assert first == second

    payloads = _payloads()
    forward: dict[str, dict[str, bytes]] = dict.fromkeys(h.CELL_IDS, payloads)
    reverse: dict[str, dict[str, bytes]] = dict.fromkeys(reversed(h.CELL_IDS), payloads)
    assert list(forward) != list(reverse)
    assert h.build_evidence(forward, canonical_sha=VALID_CANONICAL_SHA) == h.build_evidence(
        reverse, canonical_sha=VALID_CANONICAL_SHA
    )


def test_canonical_sha_does_not_alter_the_three_compared_files(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    before = {name: (root / h.ARTIFACT_NAMES[0] / name).read_bytes() for name in h.REQUIRED_FILES}
    h.aggregate(root, canonical_sha=VALID_CANONICAL_SHA)
    after = {name: (root / h.ARTIFACT_NAMES[0] / name).read_bytes() for name in h.REQUIRED_FILES}
    assert before == after == _payloads()
    for payload in after.values():
        assert b"canonical_sha" not in payload
        assert VALID_CANONICAL_SHA.encode() not in payload


def test_canonical_sha_is_absent_from_manifest_and_split_fingerprint_inputs() -> None:
    payloads = _payloads()
    assert b"canonical_sha" not in payloads[h.MANIFEST_NAME]
    # The envelope is a validation record only: it is never a manifest entry and
    # never enters the promoted split artifacts or their fingerprint inputs.
    document = json.loads(payloads[h.MANIFEST_NAME])
    assert set(document) == {"schema_version", "files"}


def test_canonical_sha_only_differs_by_that_one_key(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    without = json.loads(h.aggregate(root))
    with_sha = json.loads(h.aggregate(root, canonical_sha=VALID_CANONICAL_SHA))
    assert set(with_sha) - set(without) == {h.CANONICAL_SHA_KEY}
    assert {key: value for key, value in with_sha.items() if key != h.CANONICAL_SHA_KEY} == without


def test_evidence_schema_version_is_corrected_in_place(tmp_path: Path) -> None:
    for evidence in (
        h.aggregate(_six_cells(tmp_path / "pr")),
        h.aggregate(_six_cells(tmp_path / "dispatch"), canonical_sha=VALID_CANONICAL_SHA),
    ):
        assert json.loads(evidence)["schema_version"] == h.EVIDENCE_SCHEMA
        assert h.EVIDENCE_SCHEMA.endswith("/1")
        assert b"/2" not in evidence


def test_cli_threads_the_canonical_sha_into_the_envelope(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    out = tmp_path / "evidence" / h.EVIDENCE_NAME
    assert (
        h.main(
            [
                "aggregate",
                "--root",
                str(root),
                "--evidence-out",
                str(out),
                "--canonical-sha",
                VALID_CANONICAL_SHA,
            ]
        )
        == 0
    )
    assert json.loads(out.read_bytes())[h.CANONICAL_SHA_KEY] == VALID_CANONICAL_SHA


def test_cli_without_the_flag_omits_the_key(tmp_path: Path) -> None:
    root = _six_cells(tmp_path)
    out = tmp_path / "evidence" / h.EVIDENCE_NAME
    assert h.main(["aggregate", "--root", str(root), "--evidence-out", str(out)]) == 0
    assert h.CANONICAL_SHA_KEY not in json.loads(out.read_bytes())


def test_taxonomy_is_unchanged_by_the_canonical_sha_binding() -> None:
    assert len(h.TAXONOMY) == 21
    assert set(h.iter_taxonomy_codes()) == set(EXPECTED_TAXONOMY)


def test_workflow_threads_the_guarded_input_and_validates_its_form() -> None:
    """The workflow must pass the guarded input and never a ref or GITHUB_SHA."""
    workflow = (
        Path(h.__file__).resolve().parents[1] / ".github" / "workflows" / "mesc-b2a-portability.yml"
    ).read_text(encoding="utf-8")
    assert '--canonical-sha "${EXPECTED_SHA}"' in workflow
    assert "EXPECTED_SHA: ${{ inputs.expected_sha }}" in workflow
    assert '--canonical-sha "${GITHUB_SHA}"' not in workflow
    assert 'if [ "${#EXPECTED_SHA}" -ne 40 ]' in workflow


def test_cli_generate_and_aggregate_round_trip(tmp_path: Path) -> None:
    cell = tmp_path / "cell"
    assert h.main(["generate", "--out", str(cell)]) == 0
    root = tmp_path / "root"
    for name in h.ARTIFACT_NAMES:
        target = root / name
        target.mkdir(parents=True)
        for file_name in h.REQUIRED_FILES:
            (target / file_name).write_bytes((cell / file_name).read_bytes())
    out = tmp_path / "evidence" / h.EVIDENCE_NAME
    assert h.main(["aggregate", "--root", str(root), "--evidence-out", str(out)]) == 0
    assert out.read_bytes() == h.aggregate(root)


def test_cli_returns_nonzero_on_failure(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    out = tmp_path / "evidence.json"
    assert h.main(["aggregate", "--root", str(root), "--evidence-out", str(out)]) == 1
    assert not out.exists()


# --------------------------------------------------------------------------
# FD-PV-12 / FD-PV-13 — bounded artifact handling
#
# Every test below executes the real bounded-transport implementation against a
# real ZIP file. None asserts source text in place of behaviour, repeats a
# constant instead of exercising a guard, or re-implements the production path.
# --------------------------------------------------------------------------


def _write_archive(
    path: Path,
    members: dict[str, bytes] | None = None,
    *,
    compression: int = zipfile.ZIP_DEFLATED,
) -> Path:
    payloads = members if members is not None else _payloads()
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=compression) as bundle:
        for name, payload in payloads.items():
            bundle.writestr(name, payload)
    return path


def _six_archives(root: Path, members: dict[str, bytes] | None = None) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for name in h.ARTIFACT_NAMES:
        _write_archive(root / f"{name}{h.ARCHIVE_SUFFIX}", members)
    return root


def test_bounded_pipeline_accepts_six_valid_archives(tmp_path: Path) -> None:
    evidence = h.aggregate_from_archives(
        _six_archives(tmp_path / "archives"), tmp_path / "extracted"
    )
    document = json.loads(evidence)
    assert document["result"] == "pass"
    assert document["cells"] == list(h.CELL_IDS)
    for name in h.ARTIFACT_NAMES:
        extracted = tmp_path / "extracted" / name
        assert sorted(p.name for p in extracted.iterdir()) == sorted(h.REQUIRED_FILES)


def test_bounded_pipeline_preserves_raw_bytes_without_normalization(tmp_path: Path) -> None:
    h.aggregate_from_archives(_six_archives(tmp_path / "archives"), tmp_path / "extracted")
    payloads = _payloads()
    for name in h.ARTIFACT_NAMES:
        for file_name in h.REQUIRED_FILES:
            assert (tmp_path / "extracted" / name / file_name).read_bytes() == payloads[file_name]


def test_bounded_pipeline_threads_the_canonical_sha(tmp_path: Path) -> None:
    evidence = h.aggregate_from_archives(
        _six_archives(tmp_path / "archives"),
        tmp_path / "extracted",
        canonical_sha=VALID_CANONICAL_SHA,
    )
    assert json.loads(evidence)[h.CANONICAL_SHA_KEY] == VALID_CANONICAL_SHA


# -- compressed limits ------------------------------------------------------


def test_compressed_per_artifact_limit_exceeded_by_metadata(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    paths = h.collect_archive_paths(archives)
    actual = paths[h.ARTIFACT_NAMES[0]].stat().st_size
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.enforce_compressed_limits(paths, max_compressed_artifact=actual - 1)
    assert excinfo.value.code == "artifact_size_limit_exceeded"


def test_compressed_per_artifact_boundary_is_inclusive(tmp_path: Path) -> None:
    paths = h.collect_archive_paths(_six_archives(tmp_path / "archives"))
    largest = max(path.stat().st_size for path in paths.values())
    assert h.enforce_compressed_limits(paths, max_compressed_artifact=largest) > 0


def test_compressed_aggregate_limit_exceeded(tmp_path: Path) -> None:
    paths = h.collect_archive_paths(_six_archives(tmp_path / "archives"))
    total = sum(path.stat().st_size for path in paths.values())
    assert h.enforce_compressed_limits(paths, max_aggregate_compressed=total) == total
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.enforce_compressed_limits(paths, max_aggregate_compressed=total - 1)
    assert excinfo.value.code == "artifact_size_limit_exceeded"


def test_archive_size_discrepancy_against_declared_metadata(tmp_path: Path) -> None:
    paths = h.collect_archive_paths(_six_archives(tmp_path / "archives"))
    declared = {name: path.stat().st_size for name, path in paths.items()}
    assert h.enforce_compressed_limits(paths, declared_sizes=declared) > 0
    declared[h.ARTIFACT_NAMES[2]] -= 1
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.enforce_compressed_limits(paths, declared_sizes=declared)
    assert excinfo.value.code == "artifact_size_limit_exceeded"


def test_streamed_bytes_exceeding_the_cap_fail_despite_acceptable_metadata(
    tmp_path: Path,
) -> None:
    """Metadata is never the sole defence: on-disk bytes are re-checked."""
    paths = h.collect_archive_paths(_six_archives(tmp_path / "archives"))
    target = paths[h.ARTIFACT_NAMES[1]]
    understated = {name: path.stat().st_size for name, path in paths.items()}
    with target.open("ab") as handle:
        handle.write(b"\x00" * 4096)
    with pytest.raises(h.ArtifactSizeLimitExceededError):
        h.enforce_compressed_limits(paths, declared_sizes=understated)
    with pytest.raises(h.ArtifactSizeLimitExceededError):
        h.enforce_compressed_limits(paths, max_compressed_artifact=understated[h.ARTIFACT_NAMES[1]])


def test_declared_sizes_file_is_validated(tmp_path: Path) -> None:
    bad = tmp_path / "sizes.json"
    bad.write_bytes(b'{"b2a-portability-linux-py3.11": "1024"}')
    with pytest.raises(h.ArtifactSizeLimitExceededError):
        h.load_declared_sizes(str(bad))
    bad.write_bytes(b"[]")
    with pytest.raises(h.ArtifactSizeLimitExceededError):
        h.load_declared_sizes(str(bad))
    assert h.load_declared_sizes(None) is None


# -- extracted limits -------------------------------------------------------


def test_extracted_per_artifact_limit_exceeded_during_extraction(tmp_path: Path) -> None:
    archive = _write_archive(tmp_path / "a.zip")
    total = sum(len(payload) for payload in _payloads().values())
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.extract_archive_bounded(
            archive, tmp_path / "out", where="cell", max_extracted_artifact=total - 1
        )
    assert excinfo.value.code == "artifact_size_limit_exceeded"


def test_extracted_per_artifact_boundary_is_inclusive(tmp_path: Path) -> None:
    archive = _write_archive(tmp_path / "a.zip")
    total = sum(len(payload) for payload in _payloads().values())
    assert (
        h.extract_archive_bounded(
            archive, tmp_path / "out", where="cell", max_extracted_artifact=total
        )
        == total
    )


def test_extracted_aggregate_limit_exceeded_during_extraction(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    per_cell = sum(len(payload) for payload in _payloads().values())
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.extract_all_bounded(
            archives,
            tmp_path / "extracted",
            max_aggregate_extracted=per_cell * 6 - 1,
        )
    assert excinfo.value.code == "artifact_size_limit_exceeded"


def test_extracted_aggregate_boundary_is_inclusive(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    per_cell = sum(len(payload) for payload in _payloads().values())
    assert (
        h.extract_all_bounded(
            archives, tmp_path / "extracted", max_aggregate_extracted=per_cell * 6
        )
        == tmp_path / "extracted"
    )


def test_zip_bomb_is_refused(tmp_path: Path) -> None:
    """A highly compressible member is stopped by the extracted bound."""
    bomb = {
        h.CANONICAL_JSON_NAME: b"\x00" * (h.MAX_EXTRACTED_ARTIFACT_BYTES + 1),
        h.CANONICAL_JSONL_NAME: b"",
        h.MANIFEST_NAME: b"{}",
    }
    archive = _write_archive(tmp_path / "bomb.zip", bomb)
    assert archive.stat().st_size < h.MAX_COMPRESSED_ARTIFACT_BYTES
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert excinfo.value.code == "artifact_size_limit_exceeded"
    assert not (tmp_path / "out" / h.CANONICAL_JSON_NAME).exists()


def test_extraction_is_bounded_by_real_bytes_not_declared_size(tmp_path: Path) -> None:
    payload = b"x" * 200_000
    archive = tmp_path / "liar.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in h.REQUIRED_FILES:
            bundle.writestr(name, payload)
    with pytest.raises(h.ArtifactSizeLimitExceededError):
        h.extract_archive_bounded(
            archive, tmp_path / "out", where="cell", max_extracted_artifact=len(payload)
        )


def test_declared_oversize_is_refused_before_any_output_exists(tmp_path: Path) -> None:
    """Structural inspection precedes extraction: nothing is created at all."""
    archive = _write_archive(tmp_path / "a.zip")
    destination = tmp_path / "out"
    total = sum(len(payload) for payload in _payloads().values())
    with pytest.raises(h.ArtifactSizeLimitExceededError):
        h.extract_archive_bounded(
            archive, destination, where="cell", max_extracted_artifact=total - 1
        )
    assert not destination.exists()


def test_no_file_remains_after_a_limit_is_crossed_mid_extraction(tmp_path: Path) -> None:
    """The aggregate budget trips while bytes are streaming, after files opened.

    Declared sizes are within the per-artifact limit, so inspection passes and
    extraction genuinely begins; the remaining aggregate budget is what runs
    out. Every partially written output must be removed.
    """
    archive = _write_archive(tmp_path / "a.zip")
    destination = tmp_path / "out"
    total = sum(len(payload) for payload in _payloads().values())
    with pytest.raises(h.ArtifactSizeLimitExceededError) as excinfo:
        h.extract_archive_bounded(
            archive,
            destination,
            where="cell",
            max_extracted_artifact=total,
            aggregate_budget=total - 1,
        )
    assert excinfo.value.code == "artifact_size_limit_exceeded"
    assert destination.exists()
    assert list(destination.iterdir()) == []


def test_a_regular_file_over_one_mib_is_accepted_within_the_artifact_total(
    tmp_path: Path,
) -> None:
    """FD-PV-12: the invented per-file 1 MiB extracted limit is gone.

    A single 1.5 MiB regular file is well over the removed constraint and well
    within the ratified 4 MiB per-artifact extracted total, so it must extract.
    """
    big = b"y" * 1_572_864
    assert len(big) > 1_048_576
    members = {
        h.CANONICAL_JSON_NAME: big,
        h.CANONICAL_JSONL_NAME: b"",
        h.MANIFEST_NAME: b"{}",
    }
    archive = _write_archive(tmp_path / "big.zip", members)
    extracted = h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert extracted == len(big) + 2
    assert (tmp_path / "out" / h.CANONICAL_JSON_NAME).stat().st_size == len(big)


def test_verification_accepts_a_payload_over_one_mib() -> None:
    """The comparison layer no longer enforces a per-file extracted limit."""
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes, canonical_jsonl_bytes

    json_payload = canonical_json_bytes({"pad": "z" * 1_200_000})
    assert len(json_payload) > h.MAX_COMPRESSED_ARTIFACT_BYTES
    jsonl_payload = canonical_jsonl_bytes([{"k": 1}])
    payloads = {
        h.CANONICAL_JSON_NAME: json_payload,
        h.CANONICAL_JSONL_NAME: jsonl_payload,
        h.MANIFEST_NAME: h.build_manifest(json_payload, jsonl_payload),
    }
    h.verify_payloads(payloads, where="oversized-but-legal")


def test_per_artifact_extracted_total_still_binds() -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes, canonical_jsonl_bytes

    json_payload = canonical_json_bytes({"pad": "z" * (h.MAX_EXTRACTED_ARTIFACT_BYTES + 16)})
    jsonl_payload = canonical_jsonl_bytes([{"k": 1}])
    payloads = {
        h.CANONICAL_JSON_NAME: json_payload,
        h.CANONICAL_JSONL_NAME: jsonl_payload,
        h.MANIFEST_NAME: h.build_manifest(json_payload, jsonl_payload),
    }
    with pytest.raises(h.ArtifactSizeLimitExceededError):
        h.verify_payloads(payloads, where="oversized")


# -- unsafe archive structure ----------------------------------------------


@pytest.mark.parametrize(
    "member",
    [
        "../escape.json",
        "../../escape.json",
        "/absolute.json",
        "C:/windows.json",
        "C:\\windows.json",
        "..\\escape.json",
        "nested/canonical.json",
        "sub/dir/canonical.json",
        ".",
        "..",
    ],
)
def test_unsafe_member_names_are_rejected_before_extraction(tmp_path: Path, member: str) -> None:
    archive = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in h.REQUIRED_FILES:
            bundle.writestr(name, b"{}")
        bundle.writestr(member, b"payload")
    destination = tmp_path / "out"
    # Every parametrized name is rejected by a structural rule - backslash,
    # absolute, drive prefix, nesting or traversal - before the expected-name
    # membership check, so exactly one category applies to all of them.
    with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
        h.extract_archive_bounded(archive, destination, where="cell")
    assert excinfo.value.code == "unsafe_archive_entry"
    assert not destination.exists() or list(destination.iterdir()) == []


def test_symlink_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "symlink.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in h.REQUIRED_FILES[1:]:
            bundle.writestr(name, b"{}")
        info = zipfile.ZipInfo(h.CANONICAL_JSON_NAME)
        info.external_attr = 0o120777 << 16
        bundle.writestr(info, "/etc/passwd")
    with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert excinfo.value.code == "unsafe_archive_entry"


def test_non_regular_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "fifo.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in h.REQUIRED_FILES[1:]:
            bundle.writestr(name, b"{}")
        info = zipfile.ZipInfo(h.CANONICAL_JSON_NAME)
        info.external_attr = 0o010644 << 16
        bundle.writestr(info, b"")
    with pytest.raises(h.UnsafeArchiveEntryError):
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")


def test_directory_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "dir.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in h.REQUIRED_FILES:
            bundle.writestr(name, b"{}")
        bundle.writestr("subdir/", b"")
    with pytest.raises(h.UnsafeArchiveEntryError):
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")


def test_duplicate_archive_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "dup.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in h.REQUIRED_FILES:
            bundle.writestr(name, b"{}")
        bundle.writestr(h.CANONICAL_JSON_NAME, b"{}")
    with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert excinfo.value.code == "unsafe_archive_entry"


def test_unexpected_archive_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "extra.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in h.REQUIRED_FILES:
            bundle.writestr(name, b"{}")
        bundle.writestr("extra.txt", b"x")
    with pytest.raises(h.UnexpectedEvidenceFileError) as excinfo:
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert excinfo.value.code == "unexpected_evidence_file"


def test_missing_expected_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "missing.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in h.REQUIRED_FILES[:-1]:
            bundle.writestr(name, b"{}")
    with pytest.raises(h.MissingEvidenceFileError) as excinfo:
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert excinfo.value.code == "missing_evidence_file"


def test_more_than_three_regular_files_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "four.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        for name in (*h.REQUIRED_FILES, "canonical.json.bak"):
            bundle.writestr(name, b"{}")
    with pytest.raises(h.UnexpectedEvidenceFileError):
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")


def test_malformed_archive_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "malformed.zip"
    archive.write_bytes(b"this is not a zip file at all")
    with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert excinfo.value.code == "unsafe_archive_entry"


def test_truncated_archive_is_rejected(tmp_path: Path) -> None:
    archive = _write_archive(tmp_path / "good.zip")
    raw = archive.read_bytes()
    truncated = tmp_path / "truncated.zip"
    truncated.write_bytes(raw[: len(raw) // 2])
    with pytest.raises(h.UnsafeArchiveEntryError):
        h.extract_archive_bounded(truncated, tmp_path / "out", where="cell")


def test_corrupt_member_stream_fails_closed(tmp_path: Path) -> None:
    """A CRC-invalid member fails closed during the chunked read."""
    archive = _write_archive(tmp_path / "crc.zip")
    raw = bytearray(archive.read_bytes())
    raw[60] ^= 0xFF
    corrupt = tmp_path / "corrupt.zip"
    corrupt.write_bytes(bytes(raw))
    # Corrupt compressed data surfaces as zlib.error or BadZipFile, both of
    # which the helper maps to the archive-integrity category.
    with pytest.raises(h.UnsafeArchiveEntryError) as excinfo:
        h.extract_archive_bounded(corrupt, tmp_path / "out", where="cell")
    assert excinfo.value.code == "unsafe_archive_entry"


def test_output_write_failure_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive = _write_archive(tmp_path / "a.zip")
    real_open: Any = Path.open

    def failing_open(self: Path, mode: str = "r", *args: Any, **kwargs: Any) -> Any:
        if self.name in h.REQUIRED_FILES and "w" in mode:
            raise OSError("disk full")
        return real_open(self, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", failing_open)
    with pytest.raises(h.AggregateVerifierInternalError) as excinfo:
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")
    assert excinfo.value.code == "aggregate_verifier_internal_error"


def test_chunked_reader_failure_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive = _write_archive(tmp_path / "a.zip")

    class FailingStream:
        def __enter__(self) -> FailingStream:
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self, size: int = -1) -> bytes:
            raise OSError("reader defect")

    def failing_open(self: object, name: object, *args: object, **kwargs: object) -> object:
        return FailingStream()

    monkeypatch.setattr(zipfile.ZipFile, "open", failing_open)
    with pytest.raises(h.AggregateVerifierInternalError):
        h.extract_archive_bounded(archive, tmp_path / "out", where="cell")


# -- archive-set cardinality ------------------------------------------------


def test_missing_archive_is_rejected(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    (archives / f"{h.ARTIFACT_NAMES[0]}{h.ARCHIVE_SUFFIX}").unlink()
    with pytest.raises(h.MissingMatrixCellError) as excinfo:
        h.collect_archive_paths(archives)
    assert excinfo.value.code == "missing_matrix_cell"


def test_unexpected_archive_is_rejected(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    _write_archive(archives / "b2a-portability-solaris-py3.11.zip")
    with pytest.raises(h.UnexpectedMatrixCellError) as excinfo:
        h.collect_archive_paths(archives)
    assert excinfo.value.code == "unexpected_matrix_cell"


def test_non_zip_entry_in_the_archive_directory_is_rejected(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    (archives / "notes.txt").write_bytes(b"x")
    with pytest.raises(h.UnexpectedMatrixCellError):
        h.collect_archive_paths(archives)


def test_directory_in_the_archive_directory_is_rejected(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    (archives / "leftover").mkdir()
    with pytest.raises(h.UnsafeArchiveEntryError):
        h.collect_archive_paths(archives)


def test_missing_archive_root_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(h.MissingMatrixCellError):
        h.collect_archive_paths(tmp_path / "absent")


# -- defaults, CLI, and preserved behaviour ---------------------------------


def test_bounded_defaults_are_exactly_the_ratified_limits() -> None:
    import inspect

    extract = inspect.signature(h.extract_archive_bounded).parameters
    assert extract["max_extracted_artifact"].default == 4_194_304
    assert extract["aggregate_budget"].default == 25_165_824
    compressed = inspect.signature(h.enforce_compressed_limits).parameters
    assert compressed["max_compressed_artifact"].default == 1_048_576
    assert compressed["max_aggregate_compressed"].default == 6_291_456
    every = inspect.signature(h.extract_all_bounded).parameters
    assert every["max_compressed_artifact"].default == 1_048_576
    assert every["max_aggregate_compressed"].default == 6_291_456
    assert every["max_extracted_artifact"].default == 4_194_304
    assert every["max_aggregate_extracted"].default == 25_165_824


def test_fd_pv_6_limits_and_axes_are_exact() -> None:
    assert h.MAX_COMPRESSED_ARTIFACT_BYTES == 1_048_576
    assert h.MAX_EXTRACTED_ARTIFACT_BYTES == 4_194_304
    assert h.MAX_AGGREGATE_COMPRESSED_BYTES == 6_291_456
    assert h.MAX_AGGREGATE_EXTRACTED_BYTES == 25_165_824
    assert h.MAX_AGGREGATE_COMPRESSED_BYTES == 6 * h.MAX_COMPRESSED_ARTIFACT_BYTES
    assert h.MAX_AGGREGATE_EXTRACTED_BYTES == 6 * h.MAX_EXTRACTED_ARTIFACT_BYTES


def test_no_per_file_extracted_limit_constant_remains() -> None:
    assert not hasattr(h, "MAX_FILE_BYTES")


def test_cli_bounded_archive_mode_round_trip(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    sizes = tmp_path / "declared-sizes.json"
    sizes.write_bytes(
        json.dumps(
            {name: path.stat().st_size for name, path in h.collect_archive_paths(archives).items()}
        ).encode()
    )
    out = tmp_path / "evidence" / h.EVIDENCE_NAME
    assert (
        h.main(
            [
                "aggregate",
                "--archives",
                str(archives),
                "--extract-root",
                str(tmp_path / "extracted"),
                "--declared-sizes",
                str(sizes),
                "--evidence-out",
                str(out),
            ]
        )
        == 0
    )
    assert json.loads(out.read_bytes())["result"] == "pass"


def test_cli_bounded_archive_mode_fails_closed_on_unsafe_archive(tmp_path: Path) -> None:
    archives = _six_archives(tmp_path / "archives")
    target = archives / f"{h.ARTIFACT_NAMES[0]}{h.ARCHIVE_SUFFIX}"
    target.unlink()
    with zipfile.ZipFile(target, "w") as bundle:
        for name in h.REQUIRED_FILES:
            bundle.writestr(name, b"{}")
        bundle.writestr("../escape.json", b"x")
    out = tmp_path / "evidence" / h.EVIDENCE_NAME
    assert (
        h.main(
            [
                "aggregate",
                "--archives",
                str(archives),
                "--extract-root",
                str(tmp_path / "extracted"),
                "--evidence-out",
                str(out),
            ]
        )
        == 1
    )
    assert not out.exists()


def test_bounded_pipeline_makes_no_network_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("the bounded pipeline must not touch the network")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    h.aggregate_from_archives(_six_archives(tmp_path / "archives"), tmp_path / "extracted")


def test_taxonomy_is_unchanged_by_bounded_handling() -> None:
    assert len(h.TAXONOMY) == 21
    assert set(h.iter_taxonomy_codes()) == set(EXPECTED_TAXONOMY)


def _workflow_text() -> str:
    return (
        Path(h.__file__).resolve().parents[1] / ".github" / "workflows" / "mesc-b2a-portability.yml"
    ).read_text(encoding="utf-8")


def test_workflow_permission_and_transport_boundary() -> None:
    """Wiring guard for the workflow half of the bounded pipeline."""
    workflow = _workflow_text()
    assert "permissions:\n  contents: read\n  actions: read\n" in workflow
    assert "actions/download-artifact" not in workflow
    assert "--archives archives" in workflow
    assert "MAX_COMPRESSED_ARTIFACT_BYTES: '1048576'" in workflow
    assert "MAX_AGGREGATE_COMPRESSED_BYTES: '6291456'" in workflow
    assert "actions/runs/${GITHUB_RUN_ID}/artifacts" in workflow
    for forbidden in ("packages:", "id-token:", "contents: write", "actions: write", "secrets."):
        assert forbidden not in workflow


def test_preserved_workflow_invariants() -> None:
    workflow = _workflow_text()
    assert "fail-fast: false" in workflow
    assert workflow.count("os: ubuntu-latest") == 2
    assert workflow.count("os: windows-latest") == 2
    assert workflow.count("os: macos-latest") == 2
    assert "exclude:" not in workflow
    assert "timeout-minutes:" in workflow
    assert "version: '0.11.14'" in workflow
    assert "uv sync --frozen" in workflow
    assert "retention-days: 14" in workflow
    assert "enable-cache: false" in workflow
    assert "@v4" not in workflow
    assert (
        "if: github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'"
        in workflow
    )


# --------------------------------------------------------------------------
# Bounded transport and exact artifact-set equality
#
# The audit of head 17cfb845c99de33d229644f1d64945c267cd482c found two defects
# in the workflow half of the pipeline:
#
#   B-1  the artifact body was redirected straight to a file and only measured
#        afterwards, so nothing capped the transfer itself;
#   B-2  each expected name was required to appear once, but the complete
#        non-expired artifact set was never compared, so an extra seventh
#        current-run artifact was ignored instead of failing closed.
#
# The tests below execute the real step script from the workflow, with a stub
# ``gh`` on PATH, so they exercise the actual control flow rather than reading
# comments or matching tokens.
# --------------------------------------------------------------------------

DOWNLOAD_STEP_NAME = "Validate the current-run artifact set and download within caps"
TRANSPORT_LIMIT_BYTES = 1_048_576

RATIFIED_ARTIFACT_NAMES = (
    "b2a-portability-linux-py3.11",
    "b2a-portability-linux-py3.12",
    "b2a-portability-macos-py3.11",
    "b2a-portability-macos-py3.12",
    "b2a-portability-windows-py3.11",
    "b2a-portability-windows-py3.12",
)


def _step_script(step_name: str) -> str:
    """Return the executable body of a named workflow step's ``run:`` block."""
    lines = _workflow_text().splitlines()
    header = f"- name: {step_name}"
    start = next((position for position, line in enumerate(lines) if line.strip() == header), None)
    if start is None:  # pragma: no cover - guarded by test_download_step_exists
        raise AssertionError(f"step {step_name!r} not found")
    for offset in range(start, len(lines)):
        if lines[offset].strip() == "run: |":
            body_start = offset + 1
            break
    else:  # pragma: no cover
        raise AssertionError("step has no run block")
    indent = len(lines[body_start]) - len(lines[body_start].lstrip())
    body: list[str] = []
    for line in lines[body_start:]:
        if line.strip() and (len(line) - len(line.lstrip())) < indent:
            break
        body.append(line[indent:] if line.strip() else "")
    return "\n".join(body) + "\n"


def test_download_step_exists_and_is_extractable() -> None:
    script = _step_script(DOWNLOAD_STEP_NAME)
    assert "set -euo pipefail" in script
    assert "gh api" in script


# -- structural guards ------------------------------------------------------


def test_artifact_body_is_never_redirected_straight_to_a_file() -> None:
    """B-1 regression: the download must not be an unrestricted redirection."""
    script = _step_script(DOWNLOAD_STEP_NAME)
    download_lines = [line for line in script.splitlines() if "actions/artifacts/" in line]
    assert download_lines, "no artifact download command found"
    for line in download_lines:
        assert '> "${part}"' not in line
        assert 'zip.part"' not in line.split("|")[0]


def test_transport_is_a_bounded_streaming_consumer() -> None:
    """B-1: the producer is piped into a sink that stops at limit + 1 bytes."""
    script = _step_script(DOWNLOAD_STEP_NAME)
    assert 'transport_cap="$(( MAX_COMPRESSED_ARTIFACT_BYTES + 1 ))"' in script
    assert '| head -c "${transport_cap}" > "${part}"' in script
    # Both halves of the pipeline must be inspected, so neither a producer nor a
    # consumer failure can be swallowed.
    assert 'statuses=("${PIPESTATUS[@]}")' in script
    assert 'producer="${statuses[0]}"' in script
    assert 'consumer="${statuses[1]}"' in script
    assert 'if [ "${consumer}" != "0" ]' in script
    assert 'if [ "${producer}" != "0" ]' in script


def test_no_false_claim_of_a_control_that_is_absent() -> None:
    workflow = _workflow_text()
    if "max-filesize" in workflow:
        assert "--max-filesize" in workflow.replace("# ", "")


def test_transport_limit_is_the_ratified_compressed_limit() -> None:
    workflow = _workflow_text()
    assert "MAX_COMPRESSED_ARTIFACT_BYTES: '1048576'" in workflow
    assert "MAX_AGGREGATE_COMPRESSED_BYTES: '6291456'" in workflow


def test_post_download_size_check_remains_a_second_defence() -> None:
    script = _step_script(DOWNLOAD_STEP_NAME)
    assert 'actual="$(wc -c < "${part}" | tr -d \'[:space:]\')"' in script
    assert 'if [ "${actual}" -gt "${MAX_COMPRESSED_ARTIFACT_BYTES}" ]' in script
    assert 'if [ "${actual}" != "${size}" ]' in script


def test_set_equality_is_computed_against_the_api_response() -> None:
    """B-2: comparison targets the API response, not the download directory."""
    script = _step_script(DOWNLOAD_STEP_NAME)
    assert "artifacts.tsv" in script
    # The complete response is compared against the ratified set: duplicates,
    # unexpected names and missing names are each detected on their own.
    assert "comm -23 unique-names.txt expected-names.txt" in script
    assert "comm -13 unique-names.txt expected-names.txt" in script
    assert 'if [ "${total_count}" != "${unique_count}" ]' in script
    assert 'if [ "${total_count}" != "6" ]' in script
    assert "expired-names.txt" in script
    equality_index = script.index("comm -23 unique-names.txt expected-names.txt")
    download_index = script.index("actions/artifacts/")
    assert equality_index < download_index, "set equality must precede any download"


def test_current_run_only_endpoint_is_enforced() -> None:
    script = _step_script(DOWNLOAD_STEP_NAME)
    assert "repos/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}/artifacts" in script
    assert "actions/runs/latest" not in script


def test_no_authorization_material_is_echoed() -> None:
    script = _step_script(DOWNLOAD_STEP_NAME)
    assert "set +x" in script
    assert "GH_TOKEN" not in script
    assert 'echo "${GH_TOKEN' not in script


# -- behavioural execution of the real step script --------------------------

_BASH = shutil.which("bash")
#: Stub ``gh``. Routing happens **before** any failure injection, so a forced
#: failure can only occur on the artifact ZIP download producer, never on the
#: enumeration call. ``GH_STUB_FAIL_ON_ZIP`` names the artifact id that must
#: fail (or ``any``).
_STUB_GH = """#!/usr/bin/env bash
set -u
printf '%s\\n' "$*" >> "${GH_CALL_LOG}"
url=""
for arg in "$@"; do
  case "${arg}" in repos/*) url="${arg}" ;; esac
done
case "${url}" in
  */actions/runs/*/artifacts*)
    cat "${ARTIFACTS_TSV}"
    ;;
  */actions/artifacts/*/zip)
    id="${url%/zip}"
    id="${id##*/}"
    if [ "${GH_STUB_FAIL_ON_ZIP:-}" = "${id}" ] || [ "${GH_STUB_FAIL_ON_ZIP:-}" = "any" ]; then
      printf 'stub download producer failure for artifact %s\\n' "${id}" >&2
      exit 4
    fi
    cat "${ZIP_DIR}/${id}.bin"
    ;;
  *)
    printf 'unexpected stub url: %s\\n' "${url}" >&2
    exit 9
    ;;
esac
"""

#: Stub ``head``, injected ahead of the real one on PATH for the consumer test.
#: It begins bounded consumption and then exits with a deterministic status, so
#: the workflow's ``consumer != 0`` branch is the one that fires.
_STUB_HEAD = """#!/usr/bin/env bash
set -u
printf '%s\\n' "head $*" >> "${GH_CALL_LOG}"
IFS= read -r -n 16 -d '' _chunk || true
exit "${HEAD_STUB_STATUS}"
"""


def _run_download_step(
    tmp_path: Path,
    rows: list[tuple[str, int, str, int]],
    *,
    payload_sizes: dict[int, int] | None = None,
    fail_zip_id: str | None = None,
    failing_consumer_status: int | None = None,
    skip_declared_size_guard: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Execute the real workflow step against a stub ``gh``.

    ``rows`` are ``(name, declared_size, expired, artifact_id)`` tuples exactly
    as the API would report them. ``payload_sizes`` overrides how many bytes the
    stub actually streams for a given artifact id, which is how an under-reported
    or oversized response is simulated.

    ``fail_zip_id`` makes the stub fail **only** on that artifact's ZIP download,
    after enumeration has already succeeded, so the producer half of the bounded
    pipeline is what fails. ``failing_consumer_status`` injects a stub ``head``
    ahead of the real one on PATH so the consumer half fails instead.
    """
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    stub = bin_dir / "gh"
    stub.write_text(_STUB_GH, encoding="utf-8", newline="\n")
    stub.chmod(0o755)
    if failing_consumer_status is not None:
        consumer = bin_dir / "head"
        consumer.write_text(_STUB_HEAD, encoding="utf-8", newline="\n")
        consumer.chmod(0o755)

    tsv = tmp_path / "artifacts.tsv"
    tsv.write_text(
        "".join(f"{name}\t{size}\t{expired}\t{ident}\n" for name, size, expired, ident in rows),
        encoding="utf-8",
        newline="\n",
    )
    zip_dir = tmp_path / "zips"
    zip_dir.mkdir(parents=True, exist_ok=True)
    for _name, size, _expired, ident in rows:
        streamed = (payload_sizes or {}).get(ident, size)
        (zip_dir / f"{ident}.bin").write_bytes(b"Z" * streamed)

    script = work / "step.sh"
    script.write_text(_step_script(DOWNLOAD_STEP_NAME), encoding="utf-8", newline="\n")

    environment = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "GITHUB_REPOSITORY": "IamShehri/MedScale",
        "GITHUB_RUN_ID": "424242",
        "GH_TOKEN": "stub-token-never-printed",
        "MAX_COMPRESSED_ARTIFACT_BYTES": str(
            10_000_000 if skip_declared_size_guard else TRANSPORT_LIMIT_BYTES
        ),
        "MAX_AGGREGATE_COMPRESSED_BYTES": str(
            60_000_000 if skip_declared_size_guard else 6_291_456
        ),
        "ARTIFACTS_TSV": str(tsv),
        "ZIP_DIR": str(zip_dir),
        "GH_CALL_LOG": str(tmp_path / "gh-calls.log"),
        "GH_STUB_FAIL_ON_ZIP": fail_zip_id or "",
        "HEAD_STUB_STATUS": str(failing_consumer_status or 0),
    }
    assert _BASH is not None
    # Fixed argv, no shell interpolation: the script path and bash path are ours.
    return subprocess.run(
        [_BASH, str(script)],
        cwd=work,
        env=environment,
        capture_output=True,
        text=True,
        timeout=180,
    )


def _rows(size: int = 855) -> list[tuple[str, int, str, int]]:
    return [(name, size, "false", index + 1) for index, name in enumerate(RATIFIED_ARTIFACT_NAMES)]


def _call_log(tmp_path: Path) -> list[str]:
    log = tmp_path / "gh-calls.log"
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def _downloads_attempted(tmp_path: Path) -> int:
    return sum(1 for line in _call_log(tmp_path) if "/zip" in line)


def _enumerations_attempted(tmp_path: Path) -> int:
    return sum(1 for line in _call_log(tmp_path) if "/actions/runs/" in line)


def _archive_dir(tmp_path: Path) -> Path:
    return tmp_path / "work" / "archives"


CATEGORY_PREFIX = "MESC_PORTABILITY_FAILURE_CATEGORY="


def _category(result: subprocess.CompletedProcess[str]) -> str:
    """Return the single ratified category the workflow guard emitted.

    Fails the test if no category, or more than one, was emitted: one
    deterministic failure must produce exactly one deterministic category.
    """
    emitted = [
        line[len(CATEGORY_PREFIX) :].strip()
        for line in result.stderr.splitlines()
        if line.startswith(CATEGORY_PREFIX)
    ]
    assert len(emitted) == 1, f"expected exactly one category, got {emitted}"
    assert emitted[0] in EXPECTED_TAXONOMY, f"{emitted[0]!r} is not a ratified category"
    return emitted[0]


bash_required = pytest.mark.skipif(_BASH is None, reason="bash is unavailable on this platform")


@bash_required
def test_exactly_the_six_ratified_artifacts_pass(tmp_path: Path) -> None:
    result = _run_download_step(tmp_path, _rows())
    assert result.returncode == 0, result.stderr
    assert CATEGORY_PREFIX not in result.stderr
    archives = sorted(p.name for p in (tmp_path / "work" / "archives").iterdir())
    assert archives == sorted(f"{name}.zip" for name in RATIFIED_ARTIFACT_NAMES)
    for name in RATIFIED_ARTIFACT_NAMES:
        assert (tmp_path / "work" / "archives" / f"{name}.zip").stat().st_size == 855
    declared = json.loads((tmp_path / "work" / "declared-sizes.json").read_text(encoding="utf-8"))
    assert declared == dict.fromkeys(RATIFIED_ARTIFACT_NAMES, 855)


@bash_required
def test_transfer_of_exactly_the_limit_is_accepted(tmp_path: Path) -> None:
    rows = [(RATIFIED_ARTIFACT_NAMES[0], TRANSPORT_LIMIT_BYTES, "false", 1)]
    rows += [
        (other, 10, "false", position + 2)
        for position, other in enumerate(RATIFIED_ARTIFACT_NAMES[1:])
    ]
    result = _run_download_step(tmp_path, rows)
    assert result.returncode == 0, result.stderr
    first = tmp_path / "work" / "archives" / f"{RATIFIED_ARTIFACT_NAMES[0]}.zip"
    assert first.stat().st_size == TRANSPORT_LIMIT_BYTES


@bash_required
def test_one_byte_over_the_limit_is_rejected_and_partial_output_removed(tmp_path: Path) -> None:
    """The response lies: metadata says 855 bytes, the body streams limit + 1."""
    rows = _rows()
    result = _run_download_step(tmp_path, rows, payload_sizes={1: TRANSPORT_LIMIT_BYTES + 1})
    assert result.returncode != 0
    assert _category(result) == "artifact_size_limit_exceeded"
    assert "exceeded the transport cap" in result.stderr
    archives = _archive_dir(tmp_path)
    assert list(archives.iterdir()) == []
    # Nothing larger than limit + 1 was ever written, and the partial file is gone.
    assert not (archives / f"{RATIFIED_ARTIFACT_NAMES[0]}.zip.part").exists()


@bash_required
def test_declared_metadata_over_the_limit_fails_before_download(tmp_path: Path) -> None:
    rows = _rows()
    rows[0] = (rows[0][0], TRANSPORT_LIMIT_BYTES + 1, "false", 1)
    result = _run_download_step(tmp_path, rows, payload_sizes={1: 10})
    assert result.returncode != 0
    assert _category(result) == "artifact_size_limit_exceeded"
    assert "over the per-artifact limit" in result.stderr
    assert _downloads_attempted(tmp_path) == 0


@bash_required
def test_declared_and_actual_size_mismatch_is_rejected(tmp_path: Path) -> None:
    result = _run_download_step(tmp_path, _rows(), payload_sizes={2: 700})
    assert result.returncode != 0
    assert _category(result) == "artifact_size_limit_exceeded"
    assert "does not match declared" in result.stderr
    assert not (tmp_path / "work" / "archives" / f"{RATIFIED_ARTIFACT_NAMES[1]}.zip").exists()


@bash_required
def test_producer_failure_is_not_hidden_by_the_pipeline(tmp_path: Path) -> None:
    """The download producer fails inside the bounded pipeline, not earlier.

    Enumeration returns the complete valid six-artifact response and every
    pre-download guard passes; the stub fails only when the first artifact's ZIP
    URL is requested. That drives the workflow into::

        if [ "${producer}" != "0" ]; then
          echo "download failed for ${name} (status ${producer})" >&2
          rm -f "${part}"; exit 1
        fi
    """
    result = _run_download_step(tmp_path, _rows(), fail_zip_id="1")

    # Enumeration succeeded and the run reached the download pipeline.
    assert _enumerations_attempted(tmp_path) == 1
    assert _downloads_attempted(tmp_path) >= 1
    failing = RATIFIED_ARTIFACT_NAMES[0]

    # The producer branch is the one that reported, which also proves the
    # consumer completed normally: the workflow checks the consumer first and
    # would have exited with a different message had it been non-zero.
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"
    assert f"download failed for {failing}" in result.stderr
    assert "bounded consumer failed" not in result.stderr
    assert "(status 4)" in result.stderr
    assert "producer status 4" in result.stderr

    # No partial file survives and nothing was promoted.
    assert not (_archive_dir(tmp_path) / f"{failing}.zip.part").exists()
    assert list(_archive_dir(tmp_path).iterdir()) == []

    # The loop aborted rather than silently continuing to later artifacts.
    assert _downloads_attempted(tmp_path) == 1


@bash_required
def test_consumer_failure_is_not_hidden_by_the_pipeline(tmp_path: Path) -> None:
    """The bounded consumer fails inside the pipeline, not at setup.

    Setup, enumeration, metadata validation and set comparison all succeed and a
    real download producer is invoked; a stub ``head`` earlier on PATH begins
    consuming and then exits 7. That drives the workflow into::

        if [ "${consumer}" != "0" ]; then
          echo "bounded consumer failed for ${name} (status ${consumer})" >&2
          rm -f "${part}"; exit 1
        fi
    """
    # N1: the producer emits far more than the stub consumer reads, so the
    # producer genuinely observes a broken pipe rather than completing first.
    rows = _rows(size=2_000_000)
    result = _run_download_step(
        tmp_path, rows, failing_consumer_status=7, skip_declared_size_guard=True
    )

    # Setup and enumeration succeeded, and the pipeline was reached.
    assert _enumerations_attempted(tmp_path) == 1
    assert _downloads_attempted(tmp_path) == 1
    assert any(line.startswith("head ") for line in _call_log(tmp_path))
    failing = RATIFIED_ARTIFACT_NAMES[0]

    # The consumer status is the controlling reported failure, not the producer's
    # broken pipe.
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"
    assert f"bounded consumer failed for {failing}" in result.stderr
    assert "(status 7)" in result.stderr
    assert "download failed for" not in result.stderr
    # N1: both statuses are recorded, and the consumer remains the controlling
    # diagnostic even though the producer observes a broken pipe.
    assert "consumer status 7" in result.stderr
    producer_line = next(line for line in result.stderr.splitlines() if "producer status" in line)
    assert "producer status 0" not in producer_line

    assert not (_archive_dir(tmp_path) / f"{failing}.zip.part").exists()
    assert list(_archive_dir(tmp_path).iterdir()) == []


@bash_required
def test_setup_and_enumeration_are_not_what_fails_in_the_pipeline_tests(
    tmp_path: Path,
) -> None:
    """Guard against the earlier defect: neither failure may precede the pipeline.

    A failure at ``mkdir -p archives`` or during enumeration would never reach
    the producer or consumer branches, so this test pins the difference: with no
    injection at all the same fixture runs clean to completion.
    """
    clean = _run_download_step(tmp_path, _rows())
    assert clean.returncode == 0, clean.stderr
    assert _enumerations_attempted(tmp_path) == 1
    assert _downloads_attempted(tmp_path) == 6
    assert (tmp_path / "work" / "declared-sizes.json").exists()


@bash_required
def test_an_unexpected_seventh_artifact_fails_before_any_download(tmp_path: Path) -> None:
    rows = _rows()
    rows.append(("unrelated-debug-bundle", 100, "false", 99))
    result = _run_download_step(tmp_path, rows)
    assert result.returncode != 0
    assert _category(result) == "unexpected_matrix_cell"
    assert "unrelated-debug-bundle" in result.stderr
    assert _downloads_attempted(tmp_path) == 0
    assert list(_archive_dir(tmp_path).iterdir()) == []


@bash_required
def test_a_missing_expected_artifact_fails_before_any_download(tmp_path: Path) -> None:
    rows = _rows()[:-1]
    result = _run_download_step(tmp_path, rows)
    assert result.returncode != 0
    assert _category(result) == "missing_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0
    assert list(_archive_dir(tmp_path).iterdir()) == []


@bash_required
def test_a_duplicate_expected_artifact_fails_before_any_download(tmp_path: Path) -> None:
    rows = _rows()
    rows.append((RATIFIED_ARTIFACT_NAMES[0], 855, "false", 77))
    result = _run_download_step(tmp_path, rows)
    assert result.returncode != 0
    assert _category(result) == "duplicate_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0
    assert list(_archive_dir(tmp_path).iterdir()) == []


@bash_required
def test_an_expired_expected_artifact_fails_before_any_download(tmp_path: Path) -> None:
    rows = _rows()
    rows[3] = (rows[3][0], rows[3][1], "true", rows[3][3])
    result = _run_download_step(tmp_path, rows)
    assert result.returncode != 0
    assert _category(result) == "missing_matrix_cell"
    assert RATIFIED_ARTIFACT_NAMES[3] in result.stderr
    assert _downloads_attempted(tmp_path) == 0
    assert list(_archive_dir(tmp_path).iterdir()) == []


# -- unchanged guarantees ---------------------------------------------------


def test_permissions_remain_exactly_contents_and_actions_read() -> None:
    assert "permissions:\n  contents: read\n  actions: read\n" in _workflow_text()


def test_no_additional_authority_is_introduced() -> None:
    workflow = _workflow_text()
    for forbidden in (
        "packages:",
        "id-token:",
        "contents: write",
        "actions: write",
        "secrets.",
        "workflow_dispatch:\n    inputs:\n      token",
        "actions/cache",
    ):
        assert forbidden not in workflow
    assert workflow.count("workflow_dispatch:") == 1


def test_fd_pv_6_limits_survive_the_transport_correction() -> None:
    assert h.MAX_COMPRESSED_ARTIFACT_BYTES == 1_048_576
    assert h.MAX_EXTRACTED_ARTIFACT_BYTES == 4_194_304
    assert h.MAX_AGGREGATE_COMPRESSED_BYTES == 6_291_456
    assert h.MAX_AGGREGATE_EXTRACTED_BYTES == 25_165_824


def test_taxonomy_survives_the_transport_correction() -> None:
    assert len(h.TAXONOMY) == 21
    assert set(h.iter_taxonomy_codes()) == set(EXPECTED_TAXONOMY)


def test_canonical_sha_behaviour_survives_the_transport_correction(tmp_path: Path) -> None:
    workflow = _workflow_text()
    assert '--canonical-sha "${EXPECTED_SHA}"' in workflow
    assert "EXPECTED_SHA: ${{ inputs.expected_sha }}" in workflow
    document = json.loads(h.aggregate(_six_cells(tmp_path / "pr")))
    assert h.CANONICAL_SHA_KEY not in document
    dispatched = json.loads(
        h.aggregate(_six_cells(tmp_path / "dispatch"), canonical_sha=VALID_CANONICAL_SHA)
    )
    assert dispatched[h.CANONICAL_SHA_KEY] == VALID_CANONICAL_SHA


def test_helper_module_is_untouched_by_this_correction() -> None:
    """The transport fix is workflow-side only; the helper contract is stable."""
    for attribute in (
        "aggregate_from_archives",
        "extract_all_bounded",
        "extract_archive_bounded",
        "enforce_compressed_limits",
        "collect_archive_paths",
        "inspect_archive",
        "require_canonical_sha",
    ):
        assert hasattr(h, attribute)


def test_pipeline_branches_and_helper_surface_are_intact() -> None:
    """Supplemental: the branches these tests drive still exist as written."""
    workflow = _workflow_text()
    assert '"download failed for ${name} (status ${producer})"' in workflow
    assert '"bounded consumer failed for ${name} (status ${consumer})"' in workflow
    assert '| head -c "${transport_cap}" > "${part}"' in workflow
    assert "permissions:\n  contents: read\n  actions: read\n" in workflow
    helper = Path(h.__file__).read_text(encoding="utf-8")
    assert "def extract_archive_bounded(" in helper
    assert "def require_canonical_sha(" in helper


# --------------------------------------------------------------------------
# FD-PV-16 B3 — the canonical-main dispatch guard emits its exact category
# --------------------------------------------------------------------------

DISPATCH_STEP_NAME = "Guard canonical-main dispatch"


def _run_dispatch_guard(
    tmp_path: Path, *, ref: str, expected_sha: str, head_sha: str
) -> subprocess.CompletedProcess[str]:
    """Execute the real dispatch-guard step with a stub ``git rev-parse``."""
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    stub_git = bin_dir / "git"
    stub_git.write_text(
        '#!/usr/bin/env bash\nprintf "%s\\n" "${GIT_STUB_HEAD}"\n',
        encoding="utf-8",
        newline="\n",
    )
    stub_git.chmod(0o755)
    script = work / "guard.sh"
    script.write_text(_step_script(DISPATCH_STEP_NAME), encoding="utf-8", newline="\n")
    environment = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "GITHUB_REF": ref,
        "EXPECTED_SHA": expected_sha,
        "GIT_STUB_HEAD": head_sha,
    }
    assert _BASH is not None
    return subprocess.run(
        [_BASH, str(script)],
        cwd=work,
        env=environment,
        capture_output=True,
        text=True,
        timeout=120,
    )


CANONICAL_MAIN_SHA = "02d0aafb61fa62de414c0e8e5d61187c03b650bd"


@bash_required
def test_dispatch_guard_accepts_a_valid_canonical_sha(tmp_path: Path) -> None:
    result = _run_dispatch_guard(
        tmp_path,
        ref="refs/heads/main",
        expected_sha=CANONICAL_MAIN_SHA,
        head_sha=CANONICAL_MAIN_SHA,
    )
    assert result.returncode == 0, result.stderr
    assert CATEGORY_PREFIX not in result.stderr


@bash_required
@pytest.mark.parametrize(
    "expected_sha",
    [
        "02D0AAFB61FA62DE414C0E8E5D61187C03B650BD",
        "",
        CANONICAL_MAIN_SHA[:-1],
        CANONICAL_MAIN_SHA + "0",
        "refs/heads/main",
        "main",
        "v0.2.0",
        "02d0aafb-61fa-62de-414c-0e8e5d61187c03b",
    ],
)
def test_malformed_canonical_sha_emits_evidence_generation_failure(
    tmp_path: Path, expected_sha: str
) -> None:
    """B3: a malformed dispatch input emits exactly evidence_generation_failure."""
    result = _run_dispatch_guard(
        tmp_path,
        ref="refs/heads/main",
        expected_sha=expected_sha,
        head_sha=CANONICAL_MAIN_SHA,
    )
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"


@bash_required
def test_noncanonical_ref_emits_evidence_generation_failure(tmp_path: Path) -> None:
    result = _run_dispatch_guard(
        tmp_path,
        ref="refs/heads/feature",
        expected_sha=CANONICAL_MAIN_SHA,
        head_sha=CANONICAL_MAIN_SHA,
    )
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"
    assert "not refs/heads/main" in result.stderr


@bash_required
def test_head_mismatch_emits_evidence_generation_failure(tmp_path: Path) -> None:
    result = _run_dispatch_guard(
        tmp_path,
        ref="refs/heads/main",
        expected_sha=CANONICAL_MAIN_SHA,
        head_sha="0" * 40,
    )
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"


# --------------------------------------------------------------------------
# FD-PV-16 B3 — every emitted category is one of the ratified twenty-one
# --------------------------------------------------------------------------


def test_workflow_emits_only_ratified_categories() -> None:
    """Supplemental wiring check: no workflow guard invents a category."""
    workflow = _workflow_text()
    emitted: set[str] = set()
    for line in workflow.splitlines():
        stripped = line.strip()
        if stripped.startswith("fail_with "):
            emitted.add(stripped.split()[1])
        if stripped.startswith("aggregate_verifier_internal_error"):
            emitted.add("aggregate_verifier_internal_error")
    assert emitted, "no workflow-side categories found"
    assert emitted <= set(EXPECTED_TAXONOMY)
    assert len(EXPECTED_TAXONOMY) == 21


def test_workflow_category_emission_is_machine_verifiable() -> None:
    """Supplemental wiring check for the fixed, parseable emission form."""
    workflow = _workflow_text()
    assert "MESC_PORTABILITY_FAILURE_CATEGORY=%s" in workflow
    assert workflow.count("fail_with() {") == 3


def test_complete_response_is_validated_before_expiry_filtering() -> None:
    """Supplemental wiring check for the B2 ordering guarantee."""
    script = _step_script(DOWNLOAD_STEP_NAME)
    all_names_index = script.index("sort > all-names.txt")
    expiry_index = script.index("expired-names.txt")
    download_index = script.index("actions/artifacts/")
    assert all_names_index < expiry_index < download_index


# ==========================================================================
# FD-PV-17 — F1..F4 behavioural coverage
#
# These tests execute the real workflow step bodies extracted from
# .github/workflows/mesc-b2a-portability.yml. The `gh` stub serves raw GitHub
# artifact API JSON and validates the actual arguments the workflow passes,
# including --paginate and the exact --jq projection; it never returns
# pre-rendered TSV. The `git` stub is strict: it records every invocation and
# rejects any command that is not explicitly expected.
# ==========================================================================

EXPECTED_JQ = (
    ".artifacts[] | [.name, (.size_in_bytes|tostring), (.expired|tostring), (.id|tostring)] | @tsv"
)

CARDINALITY_STEP_NAME = "Verify archive cardinality"

#: Raw-JSON gh stub. Implements only the documented contract the workflow uses:
#: `gh api --paginate <artifacts-endpoint> --jq <exact projection>` and
#: `gh api <artifact-zip-endpoint>`. Anything else fails closed.
_STUB_GH_PY = """
import json, os, pathlib, sys

argv = sys.argv[1:]
log = pathlib.Path(os.environ["GH_CALL_LOG"])
with log.open("a", encoding="utf-8") as handle:
    handle.write(" ".join(argv) + "\\n")

def die(message: str, status: int = 90) -> None:
    sys.stderr.write("gh stub: " + message + "\\n")
    raise SystemExit(status)

if not argv or argv[0] != "api":
    die("only `gh api` is supported")

url = next((a for a in argv if a.startswith("repos/")), "")
if not url:
    die("no repos/ endpoint in arguments")

if "/actions/runs/" in url and url.endswith("artifacts?per_page=100"):
    if "--paginate" not in argv:
        die("--paginate is required for the artifacts endpoint")
    if "--jq" not in argv:
        die("--jq projection is required for the artifacts endpoint")
    expression = argv[argv.index("--jq") + 1]
    if expression != os.environ["EXPECTED_JQ"]:
        die("unexpected --jq projection: " + expression)
    if os.environ.get("GH_STUB_DROP_LAST_PAGE") == "1":
        pages = sorted(pathlib.Path(os.environ["PAGES_DIR"]).glob("page-*.json"))[:-1]
    else:
        pages = sorted(pathlib.Path(os.environ["PAGES_DIR"]).glob("page-*.json"))
    if not pages:
        die("no raw API pages available")
    rows = []
    for page in pages:
        document = json.loads(page.read_text(encoding="utf-8"))
        # Faithful evaluation of the exact projection above over raw API JSON.
        for artifact in document["artifacts"]:
            if os.environ.get("GH_STUB_LEGACY_EXPIRY_FILTER") == "1" and artifact["expired"]:
                continue
            rows.append(
                "\\t".join(
                    [
                        artifact["name"],
                        str(artifact["size_in_bytes"]),
                        "true" if artifact["expired"] else "false",
                        str(artifact["id"]),
                    ]
                )
            )
    payload = "".join(row + "\\n" for row in rows).encode("utf-8")
    sys.stdout.buffer.write(payload)
    raise SystemExit(0)

if "/actions/artifacts/" in url and url.endswith("/zip"):
    identifier = url[: -len("/zip")].rsplit("/", 1)[1]
    if os.environ.get("GH_STUB_FAIL_ON_ZIP") in {identifier, "any"}:
        sys.stderr.write("stub download producer failure for artifact " + identifier + "\\n")
        raise SystemExit(4)
    payload = pathlib.Path(os.environ["ZIP_DIR"]) / (identifier + ".bin")
    sys.stdout.buffer.write(payload.read_bytes())
    raise SystemExit(0)

die("unsupported endpoint: " + url)
"""

#: Strict git stub: records every invocation and permits only `rev-parse HEAD`.
_STUB_GIT = """#!/usr/bin/env bash
set -u
printf '%s\\n' "$*" >> "${GIT_CALL_LOG}"
if [ "${1:-}" = "rev-parse" ] && [ "${2:-}" = "HEAD" ] && [ "$#" -eq 2 ]; then
  printf '%s\\n' "${GIT_STUB_HEAD}"
  exit 0
fi
printf 'git stub: unexpected command: %s\\n' "$*" >&2
exit 99
"""


def _all_step_scripts(step_name: str) -> list[str]:
    """Return every ``run:`` body belonging to steps with this exact name."""
    lines = _workflow_text().splitlines()
    header = f"- name: {step_name}"
    bodies: list[str] = []
    for position, line in enumerate(lines):
        if line.strip() != header:
            continue
        run_index = next(i for i in range(position, len(lines)) if lines[i].strip() == "run: |")
        body_start = run_index + 1
        indent = len(lines[body_start]) - len(lines[body_start].lstrip())
        body: list[str] = []
        for candidate in lines[body_start:]:
            if candidate.strip() and (len(candidate) - len(candidate.lstrip())) < indent:
                break
            body.append(candidate[indent:] if candidate.strip() else "")
        bodies.append("\n".join(body) + "\n")
    return bodies


def _write_stub_gh(bin_dir: Path, tmp_path: Path) -> None:
    script = tmp_path / "gh_stub.py"
    script.write_text(_STUB_GH_PY, encoding="utf-8", newline="\n")
    launcher = bin_dir / "gh"
    launcher.write_text(
        f'#!/usr/bin/env bash\nexec "{sys.executable}" "{script}" "$@"\n',
        encoding="utf-8",
        newline="\n",
    )
    launcher.chmod(0o755)


def _artifact(
    name: str, size: int = 855, expired: bool = False, identifier: int = 1
) -> dict[str, Any]:
    """One raw GitHub artifact object, shaped as the REST API returns it."""
    return {
        "id": identifier,
        "name": name,
        "size_in_bytes": size,
        "expired": expired,
        "archive_download_url": f"https://api.github.com/artifacts/{identifier}/zip",
    }


def _pages(*page_artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"total_count": sum(len(p) for p in page_artifacts), "artifacts": list(page)}
        for page in page_artifacts
    ]


def _six_across_two_pages() -> list[dict[str, Any]]:
    first = [
        _artifact(name, identifier=index + 1)
        for index, name in enumerate(RATIFIED_ARTIFACT_NAMES[:3])
    ]
    second = [
        _artifact(name, identifier=index + 4)
        for index, name in enumerate(RATIFIED_ARTIFACT_NAMES[3:])
    ]
    return _pages(first, second)


def _run_download_step_json(
    tmp_path: Path,
    pages: list[dict[str, Any]],
    *,
    payload_sizes: dict[int, int] | None = None,
    fail_zip_id: str | None = None,
    drop_last_page: bool = False,
    legacy_expiry_filter: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Execute the real download step against raw paginated API JSON."""
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    _write_stub_gh(bin_dir, tmp_path)

    pages_dir = tmp_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    zip_dir = tmp_path / "zips"
    zip_dir.mkdir(parents=True, exist_ok=True)
    for index, page in enumerate(pages):
        (pages_dir / f"page-{index:03d}.json").write_text(
            json.dumps(page), encoding="utf-8", newline="\n"
        )
        for artifact in page["artifacts"]:
            streamed = (payload_sizes or {}).get(artifact["id"], artifact["size_in_bytes"])
            (zip_dir / f"{artifact['id']}.bin").write_bytes(b"Z" * streamed)

    script = work / "step.sh"
    script.write_text(_step_script(DOWNLOAD_STEP_NAME), encoding="utf-8", newline="\n")
    environment = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "GITHUB_REPOSITORY": "IamShehri/MedScale",
        "GITHUB_RUN_ID": "424242",
        "GH_TOKEN": "stub-token-never-printed",
        "MAX_COMPRESSED_ARTIFACT_BYTES": str(TRANSPORT_LIMIT_BYTES),
        "MAX_AGGREGATE_COMPRESSED_BYTES": str(6_291_456),
        "PAGES_DIR": str(pages_dir),
        "ZIP_DIR": str(zip_dir),
        "GH_CALL_LOG": str(tmp_path / "gh-calls.log"),
        "EXPECTED_JQ": EXPECTED_JQ,
        "GH_STUB_FAIL_ON_ZIP": fail_zip_id or "",
        "GH_STUB_DROP_LAST_PAGE": "1" if drop_last_page else "0",
        "GH_STUB_LEGACY_EXPIRY_FILTER": "1" if legacy_expiry_filter else "0",
    }
    assert _BASH is not None
    return subprocess.run(
        [_BASH, str(script)],
        cwd=work,
        env=environment,
        capture_output=True,
        text=True,
        timeout=300,
    )


def _no_downstream_output(tmp_path: Path) -> None:
    """No archive, declared-size map, aggregate output or evidence survived."""
    work = tmp_path / "work"
    archives = work / "archives"
    if archives.exists():
        assert list(archives.iterdir()) == []
    assert not (work / "declared-sizes.json").exists()
    assert not (work / "evidence").exists()
    assert not (work / "extracted").exists()


# -- F1: the large-response guard bypass -----------------------------------


@bash_required
def test_f1_ordinary_unexpected_artifact_is_rejected(tmp_path: Path) -> None:
    pages = _six_across_two_pages()
    pages[1]["artifacts"].append(_artifact("unrelated-debug-bundle", identifier=99))
    result = _run_download_step_json(tmp_path, pages)
    assert result.returncode != 0
    assert _category(result) == "unexpected_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0
    _no_downstream_output(tmp_path)


@bash_required
def test_f1_expired_unexpected_artifact_is_rejected(tmp_path: Path) -> None:
    pages = _six_across_two_pages()
    pages[1]["artifacts"].append(_artifact("unrelated-debug-bundle", expired=True, identifier=99))
    result = _run_download_step_json(tmp_path, pages)
    assert result.returncode != 0
    assert _category(result) == "unexpected_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0
    _no_downstream_output(tmp_path)


@bash_required
def test_f1_large_unexpected_response_cannot_bypass_the_guard(tmp_path: Path) -> None:
    """The regression that fails against parent f68f8be879….

    Many long unexpected names make the materialized comparison large enough
    that an early-exit consumer would have taken the SIGPIPE path and skipped
    the guard entirely, letting the run fall through to a later guard.
    """
    pages = _six_across_two_pages()
    extras = [
        _artifact("zz-unexpected-" + ("x" * 180) + f"-{index:04d}", identifier=1000 + index)
        for index in range(800)
    ]
    pages.append({"total_count": len(extras), "artifacts": extras})
    result = _run_download_step_json(tmp_path, pages)
    assert result.returncode != 0
    # The unexpected-artifact guard fired - not the count, missing or expiry guard.
    assert _category(result) == "unexpected_matrix_cell"
    assert "zz-unexpected-" in result.stderr
    assert "missing an expected artifact" not in result.stderr
    assert "inconsistent state" not in result.stderr
    assert "has expired" not in result.stderr
    assert _downloads_attempted(tmp_path) == 0
    _no_downstream_output(tmp_path)


# -- F2: real pagination and projection ------------------------------------


@bash_required
def test_f2_six_expected_artifacts_across_two_pages_pass(tmp_path: Path) -> None:
    result = _run_download_step_json(tmp_path, _six_across_two_pages())
    assert result.returncode == 0, result.stderr
    assert CATEGORY_PREFIX not in result.stderr
    assert _downloads_attempted(tmp_path) == 6
    declared = json.loads((tmp_path / "work" / "declared-sizes.json").read_text(encoding="utf-8"))
    assert declared == dict.fromkeys(RATIFIED_ARTIFACT_NAMES, 855)


@bash_required
def test_f2_stub_serves_raw_json_and_validates_the_real_arguments(tmp_path: Path) -> None:
    """The stub is driven by the workflow's actual gh invocation."""
    _run_download_step_json(tmp_path, _six_across_two_pages())
    calls = _call_log(tmp_path)
    enumeration = next(line for line in calls if "/actions/runs/" in line)
    assert "--paginate" in enumeration
    assert EXPECTED_JQ in enumeration


@bash_required
def test_f2_expired_unexpected_artifact_on_a_later_page_fails(tmp_path: Path) -> None:
    pages = _six_across_two_pages()
    pages.append(
        {"total_count": 1, "artifacts": [_artifact("late-debug", expired=True, identifier=77)]}
    )
    result = _run_download_step_json(tmp_path, pages)
    assert result.returncode != 0
    assert _category(result) == "unexpected_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0


@bash_required
def test_f2_live_unexpected_artifact_on_a_later_page_fails(tmp_path: Path) -> None:
    pages = _six_across_two_pages()
    pages.append({"total_count": 1, "artifacts": [_artifact("late-debug", identifier=77)]})
    result = _run_download_step_json(tmp_path, pages)
    assert result.returncode != 0
    assert _category(result) == "unexpected_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0


@bash_required
def test_f2_dropping_the_final_page_fails_as_missing(tmp_path: Path) -> None:
    result = _run_download_step_json(tmp_path, _six_across_two_pages(), drop_last_page=True)
    assert result.returncode != 0
    assert _category(result) == "missing_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0


@bash_required
def test_f2_duplicate_names_across_pages_fail(tmp_path: Path) -> None:
    pages = _six_across_two_pages()
    pages.append(
        {"total_count": 1, "artifacts": [_artifact(RATIFIED_ARTIFACT_NAMES[0], identifier=88)]}
    )
    result = _run_download_step_json(tmp_path, pages)
    assert result.returncode != 0
    assert _category(result) == "duplicate_matrix_cell"
    assert _downloads_attempted(tmp_path) == 0


@bash_required
def test_f2_expired_expected_artifact_on_a_later_page_fails(tmp_path: Path) -> None:
    pages = _six_across_two_pages()
    pages[1]["artifacts"][-1]["expired"] = True
    result = _run_download_step_json(tmp_path, pages)
    assert result.returncode != 0
    assert _category(result) == "missing_matrix_cell"
    assert RATIFIED_ARTIFACT_NAMES[-1] in result.stderr
    assert _downloads_attempted(tmp_path) == 0


@bash_required
def test_f2_legacy_expiry_filter_is_detected(tmp_path: Path) -> None:
    """Mutation guard: the old select(.expired == false) projection must fail.

    With the legacy filter the expired unexpected artifact disappears from the
    response, so the run would proceed. The suite must notice.
    """
    pages = _six_across_two_pages()
    pages.append(
        {"total_count": 1, "artifacts": [_artifact("late-debug", expired=True, identifier=77)]}
    )
    corrected = _run_download_step_json(tmp_path / "corrected", pages)
    assert corrected.returncode != 0
    assert _category(corrected) == "unexpected_matrix_cell"

    legacy = _run_download_step_json(tmp_path / "legacy", pages, legacy_expiry_filter=True)
    assert legacy.returncode == 0, "legacy filter hides the unexpected artifact"


# -- F3: dispatch guards ----------------------------------------------------


def test_f3_both_dispatch_guard_bodies_are_byte_identical() -> None:
    """Approach B: prove equivalence, then execute the shared body."""
    bodies = _all_step_scripts(DISPATCH_STEP_NAME)
    assert len(bodies) == 2, f"expected two dispatch-guard copies, found {len(bodies)}"
    assert bodies[0] == bodies[1]
    assert "fail_with evidence_generation_failure" in bodies[0]


def _run_dispatch_guard_strict(
    tmp_path: Path, *, ref: str, expected_sha: str, head_sha: str = CANONICAL_MAIN_SHA
) -> tuple[subprocess.CompletedProcess[str], list[str]]:
    """Execute the shared dispatch-guard body with a strict git stub."""
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    stub_git = bin_dir / "git"
    stub_git.write_text(_STUB_GIT, encoding="utf-8", newline="\n")
    stub_git.chmod(0o755)
    log = tmp_path / "git-calls.log"

    bodies = _all_step_scripts(DISPATCH_STEP_NAME)
    assert bodies[0] == bodies[1]
    script = work / "guard.sh"
    script.write_text(bodies[0], encoding="utf-8", newline="\n")

    environment = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "GITHUB_REF": ref,
        "EXPECTED_SHA": expected_sha,
        "GIT_STUB_HEAD": head_sha,
        "GIT_CALL_LOG": str(log),
    }
    assert _BASH is not None
    result = subprocess.run(
        [_BASH, str(script)],
        cwd=work,
        env=environment,
        capture_output=True,
        text=True,
        timeout=120,
    )
    calls = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
    return result, calls


MALFORMED_SHA_CORPUS = {
    "empty": "",
    "short": CANONICAL_MAIN_SHA[:-1],
    "long": CANONICAL_MAIN_SHA + "0",
    "uppercase": CANONICAL_MAIN_SHA.upper(),
    "non_hex": CANONICAL_MAIN_SHA[:-1] + "z",
    "leading_space": " " + CANONICAL_MAIN_SHA,
    "trailing_space": CANONICAL_MAIN_SHA + " ",
    "embedded_space": CANONICAL_MAIN_SHA[:20] + " " + CANONICAL_MAIN_SHA[21:],
    "embedded_tab": CANONICAL_MAIN_SHA[:20] + "\t" + CANONICAL_MAIN_SHA[21:],
    "embedded_newline": CANONICAL_MAIN_SHA[:20] + "\n" + CANONICAL_MAIN_SHA[21:],
    "trailing_newline": CANONICAL_MAIN_SHA + "\n",
    "crlf": CANONICAL_MAIN_SHA + "\r\n",
}


@bash_required
@pytest.mark.parametrize("label", sorted(MALFORMED_SHA_CORPUS))
def test_f3_malformed_sha_is_rejected_before_git(tmp_path: Path, label: str) -> None:
    result, calls = _run_dispatch_guard_strict(
        tmp_path, ref="refs/heads/main", expected_sha=MALFORMED_SHA_CORPUS[label]
    )
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"
    # The exact rejection diagnostic, not a later same-category failure.
    assert (
        "expected_sha is not lowercase hexadecimal" in result.stderr
        or "expected_sha is not exactly 40 characters" in result.stderr
    )
    assert "HEAD" not in result.stderr, "must not reach the HEAD-mismatch branch"
    assert calls == [], f"git was invoked before rejection: {calls}"


@bash_required
def test_f3_noncanonical_ref_is_rejected_before_git(tmp_path: Path) -> None:
    result, calls = _run_dispatch_guard_strict(
        tmp_path, ref="refs/heads/feature", expected_sha=CANONICAL_MAIN_SHA
    )
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"
    assert "not refs/heads/main" in result.stderr
    assert calls == []


@bash_required
def test_f3_head_mismatch_invokes_git_exactly_once(tmp_path: Path) -> None:
    result, calls = _run_dispatch_guard_strict(
        tmp_path, ref="refs/heads/main", expected_sha=CANONICAL_MAIN_SHA, head_sha="0" * 40
    )
    assert result.returncode != 0
    assert _category(result) == "evidence_generation_failure"
    assert "!= expected_sha" in result.stderr
    assert calls == ["rev-parse HEAD"]


@bash_required
def test_f3_clean_canonical_control_path(tmp_path: Path) -> None:
    result, calls = _run_dispatch_guard_strict(
        tmp_path, ref="refs/heads/main", expected_sha=CANONICAL_MAIN_SHA
    )
    assert result.returncode == 0, result.stderr
    assert CATEGORY_PREFIX not in result.stderr
    assert calls == ["rev-parse HEAD"]


@bash_required
def test_f3_strict_git_stub_rejects_unexpected_commands(tmp_path: Path) -> None:
    """The stub itself must fail closed, or the pre-git proof is worthless."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    stub_git = bin_dir / "git"
    stub_git.write_text(_STUB_GIT, encoding="utf-8", newline="\n")
    stub_git.chmod(0o755)
    log = tmp_path / "git-calls.log"
    environment = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "GIT_STUB_HEAD": CANONICAL_MAIN_SHA,
        "GIT_CALL_LOG": str(log),
    }
    assert _BASH is not None
    probe = subprocess.run(
        [_BASH, "-c", "git status --porcelain"],
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert probe.returncode == 99
    assert "unexpected command" in probe.stderr


# -- F4: archive cardinality ------------------------------------------------


def _run_cardinality_step(tmp_path: Path, archive_count: int) -> subprocess.CompletedProcess[str]:
    """Execute the real archive-cardinality step against a prepared directory."""
    work = tmp_path / "work"
    archives = work / "archives"
    archives.mkdir(parents=True, exist_ok=True)
    for index in range(archive_count):
        (archives / f"artifact-{index}.zip").write_bytes(b"PK\x05\x06" + b"\x00" * 18)
    script = work / "cardinality.sh"
    script.write_text(_step_script(CARDINALITY_STEP_NAME), encoding="utf-8", newline="\n")
    assert _BASH is not None
    return subprocess.run(
        [_BASH, str(script)],
        cwd=work,
        env={**os.environ},
        capture_output=True,
        text=True,
        timeout=120,
    )


@bash_required
def test_f4_six_archives_pass(tmp_path: Path) -> None:
    result = _run_cardinality_step(tmp_path, 6)
    assert result.returncode == 0, result.stderr
    assert CATEGORY_PREFIX not in result.stderr


@bash_required
@pytest.mark.parametrize("count", [5, 7])
def test_f4_invalid_archive_counts_fail_with_the_exact_category(tmp_path: Path, count: int) -> None:
    result = _run_cardinality_step(tmp_path, count)
    assert result.returncode != 0
    assert _category(result) == "aggregate_verifier_internal_error"
    assert f"found {count}" in result.stderr
    # Nothing downstream may exist: the step creates no aggregate or evidence.
    work = tmp_path / "work"
    assert not (work / "evidence").exists()
    assert not (work / "extracted").exists()
    assert not (work / "declared-sizes.json").exists()


@bash_required
def test_f4_zero_and_many_archives_also_fail(tmp_path: Path) -> None:
    for count in (0, 12):
        result = _run_cardinality_step(tmp_path / f"n{count}", count)
        assert result.returncode != 0
        assert _category(result) == "aggregate_verifier_internal_error"


# -- supplemental wiring ----------------------------------------------------


def test_f1_no_early_exit_consumer_guard_remains() -> None:
    """Supplemental: no guard depends on a SIGPIPE-prone pipeline."""
    script = _step_script(DOWNLOAD_STEP_NAME)
    executable = "\n".join(
        line for line in script.splitlines() if not line.lstrip().startswith("#")
    )
    assert "| grep -q" not in executable
    assert "comm -23 unique-names.txt expected-names.txt > unexpected-names.txt" in executable
    assert "comm -13 unique-names.txt expected-names.txt > missing-names.txt" in executable
    assert "[ -s unexpected-names.txt ]" in executable
    assert "[ -s missing-names.txt ]" in executable
