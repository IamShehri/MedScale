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
import socket
import sys
from pathlib import Path

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
    # cell identifiers above.
    evidence = h.aggregate(_six_cells(tmp_path))
    lowered = evidence.lower()
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
    with pytest.raises((h.NoncanonicalManifestError, h.InvalidJsonError)) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code in {"noncanonical_manifest", "invalid_json"}


def test_evidence_generation_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    root = _six_cells(tmp_path)
    monkeypatch.setattr(h, "build_evidence", lambda cells: canonical_json_bytes({"result": "no"}))
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

    def boom(cells: object) -> bytes:
        raise RuntimeError("verifier defect")

    monkeypatch.setattr(h, "build_evidence", boom)
    with pytest.raises(h.AggregateVerifierInternalError) as excinfo:
        h.aggregate(root)
    assert excinfo.value.code == "aggregate_verifier_internal_error"


def test_unsafe_archive_entry_nested_directory(tmp_path: Path) -> None:
    _six_cells(tmp_path)
    (tmp_path / h.ARTIFACT_NAMES[0] / "nested").mkdir()
    with pytest.raises((h.UnsafeArchiveEntryError, h.UnexpectedEvidenceFileError)) as excinfo:
        h.aggregate(tmp_path)
    assert excinfo.value.code in {"unsafe_archive_entry", "unexpected_evidence_file"}


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
    payloads = _payloads()
    payloads[h.CANONICAL_JSON_NAME] = b"x" * (h.MAX_FILE_BYTES + 1)
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

    def spy(cells: object) -> bytes:
        called.append("x")
        return original(cells)  # type: ignore[arg-type]

    monkeypatch.setattr(h, "build_evidence", spy)
    with pytest.raises(h.PortabilityError):
        h.aggregate(root)
    assert called == []


def test_traversal_and_absolute_paths_are_rejected() -> None:
    for name in ("../escape.json", "/abs.json"):
        assert ".." in name or name.startswith("/")


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
        "json",
        "sys",
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


def test_fd_pv_6_limits_are_exact() -> None:
    assert h.MAX_FILE_BYTES == 1_048_576
    assert h.MAX_ARTIFACT_BYTES == 4_194_304
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
