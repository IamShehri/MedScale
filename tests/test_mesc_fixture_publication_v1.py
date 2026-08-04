"""Synthetic tests for the private P01-04B publication boundary (FD-BPUB-1..18).

Every fixture here is synthetic identity data built inside this module and every
filesystem operation happens inside a pytest temporary directory.  No dataset is
read, no registry is scanned, no network or subprocess is used, no model is
touched, and nothing produced here is a real split, a canonical partition or any
kind of evidence.

The publication contract guarantees atomic namespace visibility only.  Nothing in
this module asserts or implies power-loss, storage-controller, filesystem-journal
or directory-entry durability.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

import pytest

from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes
from medscale.mesc._fixture_publication_v1 import (
    MANIFEST_SCHEMA_VERSION,
    _ContentVerificationError,
    _ExclusiveWriteError,
    _InvalidPublicationInputError,
    _InventoryVerificationError,
    _PlannedFile,
    _PostRenameVerificationError,
    _PublicationError,
    _PublicationReceipt,
    _PublicationTargetConflictError,
    _publish_fixture_split_v1,
    _UnsafePublicationPathError,
    _UnsupportedAtomicRenameError,
)
from medscale.mesc._fixture_split_v1 import (
    FIXTURE_NAMESPACE_PREFIX,
    REQUEST_ID_PREFIX,
    FixtureSplitFacade,
    FixtureSplitRequest,
    FixtureSplitResult,
    _fixture_identity_document,
    _request_identity_document,
)
from medscale.mesc._leakage_v1 import LeakageFinding
from medscale.mesc._split_v1 import SPLIT_SEED, OrderedExampleRow, SourceLabelRow
from medscale.mesc.split import PilotSplitNotAuthorizedError, SourceDocumentGroupedSplitter

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "medscale" / "mesc"
PUBLICATION_MODULE = MODULE_PATH / "_fixture_publication_v1.py"

DATASET_ID = "mesc-publication-fixture-dataset"
DATASET_REVISION = "publication-fixture-revision-1"
CONFIGURATION = "publication-fixture-configuration"
TRANSFORMATION_VERSION = "mesc-publication-fixture-transformation/1"
POLICY_ID = "mesc-publication-fixture-policy/1"
EXECUTION_EVIDENCE_REF = "mesc-publication-fixture-evidence/1:unit"
SYNTHETIC_PROOF = "mesc-synthetic-batch/1:sha256:" + "b7c4d1e9" * 8
DETECTION_METHODS = ("exact_example_identity", "exact_question_equality")
FIXTURE_ID = "bpub-unit-fixture-a"

#: One example per decision, one source document each, one place per partition.
SPEC: tuple[tuple[int, int, str], ...] = ((0, 0, "yes"), (1, 1, "no"), (2, 2, "maybe"))
TOTALS = {"train": 1, "validation": 1, "test": 1}

FINDING = LeakageFinding.create(
    finding_type="exact_question",
    example_ids=("publication-finding-left", "publication-finding-right"),
    source_document_ids=("fixture-document-00",),
    partitions=("train",),
    score_representation="none",
    classification="false_positive",
    shared_surface=("question_bytes",),
    evidence_reference="mesc-publication-fixture-evidence/1:finding-a",
)

PAYLOAD_FILENAMES = (
    "example-registry.jsonl",
    "excluded-ledger.json",
    "group-registry.jsonl",
    "leakage-audit.json",
    "split-summary-identity-core.json",
    "split-summary.json",
)
MANIFEST_FILENAME = "publication-manifest.json"
ALL_FILENAMES = tuple(sorted([*PAYLOAD_FILENAMES, MANIFEST_FILENAME]))
SURFACES = (
    "example_registry",
    "excluded_ledger",
    "group_registry",
    "leakage_audit",
    "split_summary_identity_core",
    "split_summary_document",
)


# ---------------------------------------------------------------------------
# Synthetic fixture construction
# ---------------------------------------------------------------------------


def _ordered_rows() -> tuple[OrderedExampleRow, ...]:
    return tuple(
        OrderedExampleRow(
            original_example_id=f"fixture-example-{index:02d}",
            row_ordinal=index,
            source_document_id=f"fixture-document-{document:02d}",
        )
        for index, document, _ in SPEC
    )


def _source_labels() -> tuple[SourceLabelRow, ...]:
    return tuple(
        SourceLabelRow(
            dataset_id=DATASET_ID,
            dataset_revision=DATASET_REVISION,
            configuration=CONFIGURATION,
            original_example_id=f"fixture-example-{index:02d}",
            source_document_id=f"fixture-document-{document:02d}",
            decision=decision,  # type: ignore[arg-type]
            source_record_hash=f"{index:064x}",
        )
        for index, document, decision in SPEC
    )


def _skeleton_kwargs() -> dict[str, Any]:
    return {
        "fixture_schema_version": "1",
        "fixture_namespace": FIXTURE_NAMESPACE_PREFIX + FIXTURE_ID,
        "fixture_id": FIXTURE_ID,
        "fixture_sha256": "0" * 64,
        "fixture_only": True,
        "non_evidence": True,
        "synthetic_identity_proof": SYNTHETIC_PROOF,
        "request_id": REQUEST_ID_PREFIX + "0" * 64,
        "seed": SPLIT_SEED,
        "policy_id": POLICY_ID,
        "transformation_version": TRANSFORMATION_VERSION,
        "ordered_rows": _ordered_rows(),
        "source_labels": _source_labels(),
        "partition_totals": dict(TOTALS),
        "leakage_findings": (FINDING,),
        "detection_methods": DETECTION_METHODS,
        "execution_evidence_ref": EXECUTION_EVIDENCE_REF,
    }


def _build_request() -> FixtureSplitRequest:
    """Return a request whose two identity digests are regenerated for its payload."""
    skeleton = FixtureSplitRequest(**_skeleton_kwargs())
    digest = sha256_of_bytes(canonical_json_bytes(_fixture_identity_document(skeleton)))
    completed = FixtureSplitRequest(**{**_skeleton_kwargs(), "fixture_sha256": digest})
    request_id = REQUEST_ID_PREFIX + sha256_of_bytes(
        canonical_json_bytes(_request_identity_document(completed, digest))
    )
    return FixtureSplitRequest(
        **{**_skeleton_kwargs(), "fixture_sha256": digest, "request_id": request_id}
    )


@pytest.fixture
def request_object() -> FixtureSplitRequest:
    return _build_request()


@pytest.fixture
def result_object(request_object: FixtureSplitRequest) -> FixtureSplitResult:
    return FixtureSplitFacade.run(request_object)


@pytest.fixture
def parent(tmp_path: Path) -> Path:
    target = (tmp_path / "publication-parent").resolve()
    target.mkdir()
    return target


@pytest.fixture
def protected(tmp_path: Path) -> tuple[Path, ...]:
    target = (tmp_path / "protected-root").resolve()
    target.mkdir()
    return (target,)


def _publish(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> _PublicationReceipt:
    return _publish_fixture_split_v1(
        request_object,
        result_object,
        publication_parent=parent,
        protected_roots=protected,
    )


def _fingerprint(result_object: FixtureSplitResult) -> str:
    return result_object.split_fingerprint_record.split_fingerprint


def _try_symlink(link: Path, target: Path) -> None:
    """Create a symlink, or skip narrowly when the platform forbids it."""
    try:
        link.symlink_to(target, target_is_directory=True)
    except (OSError, NotImplementedError):  # pragma: no cover - platform dependent
        pytest.skip("symlink creation is not permitted on this platform")


# ---------------------------------------------------------------------------
# Successful publication (FD-BPUB-5, FD-BPUB-6, FD-BPUB-11, FD-BPUB-17)
# ---------------------------------------------------------------------------


def test_publishes_exactly_seven_files(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    published = receipt.publication_directory
    assert sorted(entry.name for entry in published.iterdir()) == list(ALL_FILENAMES)
    assert sorted(entry.name for entry in parent.iterdir()) == [published.name]


def test_exact_directory_names_carry_the_split_component(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    fingerprint = _fingerprint(result_object)
    receipt = _publish(request_object, result_object, parent, protected)
    assert receipt.publication_directory.name == f"mesc-p01-04b-split-{fingerprint}"
    assert "-split-" in receipt.publication_directory.name
    staging_name = f".mesc-p01-04b-split-{fingerprint}.staging"
    assert "-split-" in staging_name
    assert not (parent / staging_name).exists()


def test_directory_name_is_stable_across_repeated_publication(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    tmp_path: Path,
    protected: tuple[Path, ...],
) -> None:
    names: list[str] = []
    for index in range(3):
        target = (tmp_path / f"parent-{index}").resolve()
        target.mkdir()
        receipt = _publish(request_object, result_object, target, protected)
        names.append(receipt.publication_directory.name)
    assert len(set(names)) == 1


def test_exact_six_byte_bindings(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    published = receipt.publication_directory
    assert (published / "group-registry.jsonl").read_bytes() == result_object.group_registry_bytes
    assert (
        published / "example-registry.jsonl"
    ).read_bytes() == result_object.example_registry_bytes
    assert (published / "excluded-ledger.json").read_bytes() == result_object.excluded_ledger_bytes
    assert (
        published / "split-summary-identity-core.json"
    ).read_bytes() == result_object.split_summary_identity_core_bytes
    assert (
        published / "split-summary.json"
    ).read_bytes() == result_object.split_summary_document_bytes
    assert (published / "leakage-audit.json").read_bytes() == result_object.audit_report_bytes


def test_leakage_filename_has_no_report_variant(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    names = {entry.name for entry in receipt.publication_directory.iterdir()}
    assert "leakage-audit.json" in names
    rejected = "leakage-audit" + "-report" + ".json"
    assert rejected not in names


# ---------------------------------------------------------------------------
# Manifest (FD-BPUB-7)
# ---------------------------------------------------------------------------


def test_manifest_has_exactly_five_top_level_members(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    document = json.loads((receipt.publication_directory / MANIFEST_FILENAME).read_text("utf-8"))
    assert set(document) == {
        "schema_version",
        "request_id",
        "split_fingerprint",
        "publication_directory_name",
        "files",
    }
    for forbidden in (
        "fixture_only",
        "non_evidence",
        "fixture_id",
        "synthetic_identity_proof",
        "split_hash",
        "execution_evidence_ref",
    ):
        assert forbidden not in document


def test_manifest_records_are_exact_and_ascending(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    document = json.loads((receipt.publication_directory / MANIFEST_FILENAME).read_text("utf-8"))
    records = document["files"]
    assert len(records) == 6
    assert [record["filename"] for record in records] == list(PAYLOAD_FILENAMES)
    assert [record["filename"] for record in records] == sorted(PAYLOAD_FILENAMES)
    assert [record["surface"] for record in records] == list(SURFACES)
    for record in records:
        assert set(record) == {"filename", "surface", "sha256", "byte_size"}
        assert "schema_version" not in record
        payload = (receipt.publication_directory / record["filename"]).read_bytes()
        assert record["sha256"] == sha256_of_bytes(payload)
        assert record["byte_size"] == len(payload)


def test_manifest_is_non_circular_and_metadata_free(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    manifest_path = receipt.publication_directory / MANIFEST_FILENAME
    raw = manifest_path.read_bytes()
    document = json.loads(raw.decode("utf-8"))
    assert document["schema_version"] == MANIFEST_SCHEMA_VERSION
    assert document["publication_directory_name"] == receipt.publication_directory.name
    assert not Path(document["publication_directory_name"]).is_absolute()
    assert MANIFEST_FILENAME not in {record["filename"] for record in document["files"]}
    assert sha256_of_bytes(raw).encode() not in raw
    assert str(parent).encode("utf-8") not in raw
    assert raw == canonical_json_bytes(document)
    assert raw.endswith(b"\n")


def test_manifest_does_not_borrow_artifact_schema_versions(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    from medscale.mesc._split_artifacts_v1 import ARTIFACT_SCHEMA_VERSIONS

    receipt = _publish(request_object, result_object, parent, protected)
    raw = (receipt.publication_directory / MANIFEST_FILENAME).read_text("utf-8")
    for schema in ARTIFACT_SCHEMA_VERSIONS.values():
        assert schema not in raw


# ---------------------------------------------------------------------------
# Receipt (FD-BPUB-17)
# ---------------------------------------------------------------------------


def test_receipt_has_exactly_five_fields(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    assert _PublicationReceipt.__slots__ == (
        "publication_directory",
        "request_id",
        "split_fingerprint",
        "publication_manifest_sha256",
        "published_filenames",
    )
    assert not hasattr(receipt, "final_directory")
    assert not hasattr(receipt, "publication_manifest_bytes")
    assert type(receipt.publication_directory) is type(parent)
    assert isinstance(receipt.publication_directory, Path)
    assert type(receipt.request_id) is str
    assert type(receipt.split_fingerprint) is str
    assert type(receipt.publication_manifest_sha256) is str
    assert type(receipt.published_filenames) is tuple
    assert receipt.published_filenames == ALL_FILENAMES
    assert receipt.request_id == request_object.request_id
    assert receipt.split_fingerprint == _fingerprint(result_object)
    manifest = (receipt.publication_directory / MANIFEST_FILENAME).read_bytes()
    assert receipt.publication_manifest_sha256 == sha256_of_bytes(manifest)


def test_receipt_is_frozen_and_never_written(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    with pytest.raises(AttributeError):
        receipt.request_id = "mutated"  # type: ignore[misc]
    published = {entry.name for entry in receipt.publication_directory.iterdir()}
    assert published == set(ALL_FILENAMES)
    assert not any("receipt" in name for name in published)


# ---------------------------------------------------------------------------
# Input validation (FD-BPUB-3)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        {"request_id": "x"},
        "a-string",
        b"bytes",
        123,
        None,
        iter(()),
    ],
)
def test_rejects_non_exact_request_types(
    bad: object,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            bad,  # type: ignore[arg-type]
            result_object,
            publication_parent=parent,
            protected_roots=protected,
        )


def test_rejects_subclass_of_request(
    result_object: FixtureSplitResult, parent: Path, protected: tuple[Path, ...]
) -> None:
    class _Derived(FixtureSplitRequest):
        pass

    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            _Derived(**_skeleton_kwargs()),
            result_object,
            publication_parent=parent,
            protected_roots=protected,
        )


@pytest.mark.parametrize("bad", ["a-string", b"bytes", 7, None, {"a": 1}])
def test_rejects_non_exact_result_types(
    bad: object,
    request_object: FixtureSplitRequest,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            request_object,
            bad,  # type: ignore[arg-type]
            publication_parent=parent,
            protected_roots=protected,
        )


def test_rejects_mismatched_request_result_binding(
    result_object: FixtureSplitResult, parent: Path, protected: tuple[Path, ...]
) -> None:
    other = FixtureSplitRequest(
        **{**_skeleton_kwargs(), "request_id": REQUEST_ID_PREFIX + "1" * 64}
    )
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            other, result_object, publication_parent=parent, protected_roots=protected
        )
    assert list(parent.iterdir()) == []


@pytest.mark.parametrize(
    "bad_parent",
    ["/tmp/not-a-path", b"/tmp", 5, None],
)
def test_rejects_non_path_publication_parent(
    bad_parent: object,
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    protected: tuple[Path, ...],
) -> None:
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=bad_parent,  # type: ignore[arg-type]
            protected_roots=protected,
        )


def test_rejects_relative_publication_parent(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    protected: tuple[Path, ...],
) -> None:
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=Path("relative-parent"),
            protected_roots=protected,
        )


def test_rejects_missing_publication_parent(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    tmp_path: Path,
    protected: tuple[Path, ...],
) -> None:
    missing = (tmp_path / "absent").resolve()
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=missing,
            protected_roots=protected,
        )
    assert not missing.exists()


def test_rejects_file_as_publication_parent(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    tmp_path: Path,
    protected: tuple[Path, ...],
) -> None:
    target = tmp_path / "a-file"
    target.write_bytes(b"x")
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=target.resolve(),
            protected_roots=protected,
        )


@pytest.mark.parametrize("bad_roots", [[], (), "root", None, 5])
def test_rejects_invalid_protected_root_container(
    bad_roots: object,
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
) -> None:
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=bad_roots,  # type: ignore[arg-type]
        )


def test_rejects_list_of_paths_instead_of_tuple(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=list(protected),  # type: ignore[arg-type]
        )


def test_rejects_string_protected_root(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=(str(protected[0]),),  # type: ignore[arg-type]
        )


def test_rejects_duplicate_protected_roots(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=(protected[0], protected[0]),
        )
    assert list(parent.iterdir()) == []


def test_rejects_parent_equal_to_protected_root(
    request_object: FixtureSplitRequest, result_object: FixtureSplitResult, parent: Path
) -> None:
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=(parent,),
        )
    assert list(parent.iterdir()) == []


def test_rejects_parent_inside_protected_root(
    request_object: FixtureSplitRequest, result_object: FixtureSplitResult, tmp_path: Path
) -> None:
    root = (tmp_path / "root").resolve()
    inner = root / "inner"
    inner.mkdir(parents=True)
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=inner,
            protected_roots=(root,),
        )
    assert list(inner.iterdir()) == []


def test_rejects_protected_root_inside_parent(
    request_object: FixtureSplitRequest, result_object: FixtureSplitResult, tmp_path: Path
) -> None:
    outer = (tmp_path / "outer").resolve()
    inner = outer / "inner"
    inner.mkdir(parents=True)
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=outer,
            protected_roots=(inner,),
        )
    assert [entry.name for entry in outer.iterdir()] == ["inner"]


def test_rejects_symlinked_publication_parent(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    tmp_path: Path,
    protected: tuple[Path, ...],
) -> None:
    real = (tmp_path / "real-parent").resolve()
    real.mkdir()
    link = tmp_path / "linked-parent"
    _try_symlink(link, real)
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=link,
            protected_roots=protected,
        )
    assert list(real.iterdir()) == []


def test_rejects_symlinked_protected_root(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    tmp_path: Path,
) -> None:
    real = (tmp_path / "real-root").resolve()
    real.mkdir()
    link = tmp_path / "linked-root"
    _try_symlink(link, real)
    with pytest.raises(_UnsafePublicationPathError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=(link,),
        )
    assert list(parent.iterdir()) == []


def test_rejects_traversal_and_separator_injection() -> None:
    from medscale.mesc._fixture_publication_v1 import _assert_direct_child_name

    for candidate in ("..", ".", "", "a/b", "a\\b", "a:b", "../escape"):
        with pytest.raises(_UnsafePublicationPathError):
            _assert_direct_child_name(candidate)
    _assert_direct_child_name("mesc-p01-04b-split-" + "0" * 64)


# ---------------------------------------------------------------------------
# Absent POSIX alternate separator
#
# ``os.altsep`` is ``None`` on Linux and macOS. These tests simulate that exact
# platform value on whatever host runs them. Simulation is NOT a substitute for
# real Linux or macOS execution; it exists so the regression is observable
# locally before the cross-platform matrix runs in CI.
# ---------------------------------------------------------------------------


FINGERPRINT_PLACEHOLDER = "0" * 64
VALID_FINAL_NAME = f"mesc-p01-04b-split-{FINGERPRINT_PLACEHOLDER}"
VALID_STAGING_NAME = f".mesc-p01-04b-split-{FINGERPRINT_PLACEHOLDER}.staging"


def _simulated_altsep() -> object:
    """Return ``os.altsep`` as a plain object.

    The Windows type stubs declare ``os.altsep`` as ``str``, so asserting it is
    ``None`` directly would narrow to an impossible type and mark the rest of the
    test unreachable. Reading it through ``object`` keeps the runtime assertion
    while staying honest about the declared type.
    """
    return os.altsep


@pytest.fixture
def posix_separators(monkeypatch: pytest.MonkeyPatch) -> None:
    """Simulate the POSIX separator configuration; monkeypatch restores it."""
    monkeypatch.setattr(os, "sep", "/")
    monkeypatch.setattr(os, "altsep", None)


def test_separator_set_never_contains_an_empty_candidate(
    posix_separators: None,
) -> None:
    """An empty or absent separator must never reach ``separator in name``."""
    from medscale.mesc._fixture_publication_v1 import _path_separators

    separators = _path_separators()
    assert _simulated_altsep() is None
    assert "" not in separators
    assert None not in separators
    assert all(separator for separator in separators)
    assert set(separators) == {"/", "\\"}


def test_valid_final_name_accepted_when_altsep_is_absent(posix_separators: None) -> None:
    from medscale.mesc._fixture_publication_v1 import _assert_direct_child_name

    assert _simulated_altsep() is None
    _assert_direct_child_name(VALID_FINAL_NAME)


def test_valid_staging_name_accepted_when_altsep_is_absent(posix_separators: None) -> None:
    from medscale.mesc._fixture_publication_v1 import _assert_direct_child_name

    assert _simulated_altsep() is None
    _assert_direct_child_name(VALID_STAGING_NAME)


def test_forward_slash_still_rejected_when_altsep_is_absent(posix_separators: None) -> None:
    from medscale.mesc._fixture_publication_v1 import _assert_direct_child_name

    for candidate in ("a/b", "/absolute", f"{VALID_FINAL_NAME}/nested", "../escape"):
        with pytest.raises(_UnsafePublicationPathError):
            _assert_direct_child_name(candidate)


def test_backslash_still_rejected_when_altsep_is_absent(posix_separators: None) -> None:
    from medscale.mesc._fixture_publication_v1 import _assert_direct_child_name

    for candidate in ("a\\b", "\\absolute", f"{VALID_FINAL_NAME}\\nested"):
        with pytest.raises(_UnsafePublicationPathError):
            _assert_direct_child_name(candidate)


def test_traversal_and_empty_names_still_rejected_when_altsep_is_absent(
    posix_separators: None,
) -> None:
    from medscale.mesc._fixture_publication_v1 import _assert_direct_child_name

    for candidate in ("", ".", ".."):
        with pytest.raises(_UnsafePublicationPathError):
            _assert_direct_child_name(candidate)


def test_publication_succeeds_when_altsep_is_absent(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A complete synthetic publication must survive ``os.altsep is None``.

    Only ``os.altsep`` is simulated here: ``os.sep`` is left at the host value so
    the host's own path handling stays consistent while the exact POSIX
    difference that caused the regression is exercised end to end.
    """
    monkeypatch.setattr(os, "altsep", None)
    receipt = _publish(request_object, result_object, parent, protected)
    assert receipt.publication_directory.name == f"mesc-p01-04b-split-{_fingerprint(result_object)}"
    assert sorted(entry.name for entry in receipt.publication_directory.iterdir()) == list(
        ALL_FILENAMES
    )
    assert receipt.published_filenames == ALL_FILENAMES
    assert len(receipt.published_filenames) == 7


def test_typed_input_errors_are_not_masked_when_altsep_is_absent(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The separator check must not shadow the earlier typed input categories.

    The child-name check runs before the write-path boundary, so a name rejected
    unconditionally would surface as an unsafe-path error for every caller and
    hide the real input defect.
    """
    monkeypatch.setattr(os, "altsep", None)

    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=list(protected),  # type: ignore[arg-type]
        )
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            request_object,
            result_object,
            publication_parent=parent,
            protected_roots=(),
        )
    with pytest.raises(_InvalidPublicationInputError):
        _publish_fixture_split_v1(
            "not-a-request",  # type: ignore[arg-type]
            result_object,
            publication_parent=parent,
            protected_roots=protected,
        )
    assert list(parent.iterdir()) == []


# ---------------------------------------------------------------------------
# Conflicts (FD-BPUB-9)
# ---------------------------------------------------------------------------


def test_existing_staging_directory_is_a_typed_conflict(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    staging = parent / f".mesc-p01-04b-split-{_fingerprint(result_object)}.staging"
    staging.mkdir()
    (staging / "pre-existing").write_bytes(b"untouched")
    with pytest.raises(_PublicationTargetConflictError):
        _publish(request_object, result_object, parent, protected)
    assert [entry.name for entry in staging.iterdir()] == ["pre-existing"]
    assert (staging / "pre-existing").read_bytes() == b"untouched"


def test_existing_final_directory_is_a_typed_conflict(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    final = parent / f"mesc-p01-04b-split-{_fingerprint(result_object)}"
    final.mkdir()
    with pytest.raises(_PublicationTargetConflictError):
        _publish(request_object, result_object, parent, protected)
    assert list(final.iterdir()) == []
    assert [entry.name for entry in parent.iterdir()] == [final.name]


def test_staging_conflict_writes_no_payload(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    staging = parent / f".mesc-p01-04b-split-{_fingerprint(result_object)}.staging"
    staging.mkdir()
    with pytest.raises(_PublicationTargetConflictError):
        _publish(request_object, result_object, parent, protected)
    assert list(staging.iterdir()) == []


# ---------------------------------------------------------------------------
# Rename primitive (FD-BPUB-14)
# ---------------------------------------------------------------------------


def test_unsupported_primitive_fails_before_any_mutation(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    def _unsupported() -> str:
        raise _UnsupportedAtomicRenameError("no primitive")

    monkeypatch.setattr(module, "_resolve_rename_primitive", _unsupported)
    with pytest.raises(_UnsupportedAtomicRenameError):
        _publish(request_object, result_object, parent, protected)
    assert list(parent.iterdir()) == []


def test_resolved_primitive_is_a_known_no_replace_primitive() -> None:
    from medscale.mesc._fixture_publication_v1 import _resolve_rename_primitive

    assert _resolve_rename_primitive() in {
        "windows-rename-no-replace",
        "linux-renameat2-noreplace",
        "macos-renamex-np-excl",
    }


def test_rename_refuses_to_replace_a_racing_destination(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The primitive itself must refuse, not a precheck."""
    import medscale.mesc._fixture_publication_v1 as module

    final = parent / f"mesc-p01-04b-split-{_fingerprint(result_object)}"
    original = module._verify_directory_inventory

    def _race(directory: Path, plan: Any, failure: Any) -> None:
        original(directory, plan, failure)
        final.mkdir()
        (final / "squatter").write_bytes(b"do-not-replace")

    monkeypatch.setattr(module, "_verify_directory_inventory", _race)
    with pytest.raises(_PublicationTargetConflictError):
        _publish(request_object, result_object, parent, protected)
    assert (final / "squatter").read_bytes() == b"do-not-replace"
    staging = parent / f".mesc-p01-04b-split-{_fingerprint(result_object)}.staging"
    assert sorted(entry.name for entry in staging.iterdir()) == list(ALL_FILENAMES)


def test_module_never_uses_os_replace_or_a_copy_fallback() -> None:
    source = PUBLICATION_MODULE.read_text("utf-8")
    assert "os.replace" not in source
    assert "shutil" not in source
    assert "copytree" not in source
    assert "copyfile" not in source


# ---------------------------------------------------------------------------
# Failure preservation (FD-BPUB-15)
# ---------------------------------------------------------------------------


def _staging_of(parent: Path, result_object: FixtureSplitResult) -> Path:
    return parent / f".mesc-p01-04b-split-{_fingerprint(result_object)}.staging"


def test_payload_write_failure_preserves_staging(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    original = module._write_exact_once
    calls: list[str] = []

    def _fail_on_third(directory: Path, planned: _PlannedFile) -> None:
        calls.append(planned.filename)
        if len(calls) == 3:
            raise _ExclusiveWriteError("injected write failure")
        original(directory, planned)

    monkeypatch.setattr(module, "_write_exact_once", _fail_on_third)
    with pytest.raises(_ExclusiveWriteError):
        _publish(request_object, result_object, parent, protected)
    staging = _staging_of(parent, result_object)
    assert sorted(entry.name for entry in staging.iterdir()) == sorted(calls[:2])
    assert not (parent / f"mesc-p01-04b-split-{_fingerprint(result_object)}").exists()


def test_synchronization_failure_preserves_staging(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    def _fail(file_descriptor: int) -> None:
        raise OSError("injected fsync failure")

    monkeypatch.setattr(module, "_sync_file", _fail)
    with pytest.raises(_ExclusiveWriteError):
        _publish(request_object, result_object, parent, protected)
    staging = _staging_of(parent, result_object)
    assert staging.is_dir()
    assert [entry.name for entry in staging.iterdir()] == ["example-registry.jsonl"]


def test_readback_mismatch_preserves_staging(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    original = module._write_exact_once

    def _corrupt(directory: Path, planned: _PlannedFile) -> None:
        original(directory, planned)
        if planned.filename == "excluded-ledger.json":
            (directory / planned.filename).write_bytes(b"corrupted")

    monkeypatch.setattr(module, "_write_exact_once", _corrupt)
    with pytest.raises(_ContentVerificationError):
        _publish(request_object, result_object, parent, protected)
    staging = _staging_of(parent, result_object)
    assert (staging / "excluded-ledger.json").read_bytes() == b"corrupted"
    assert not (parent / f"mesc-p01-04b-split-{_fingerprint(result_object)}").exists()


def test_digest_and_size_mismatch_are_content_failures(tmp_path: Path) -> None:
    from medscale.mesc._fixture_publication_v1 import _read_back

    target = tmp_path / "payload.bin"
    target.write_bytes(b"exact")
    wrong_digest = _PlannedFile(
        filename="payload.bin", payload=b"exact", sha256="0" * 64, byte_size=5
    )
    with pytest.raises(_ContentVerificationError):
        _read_back(target, wrong_digest)
    wrong_size = _PlannedFile(
        filename="payload.bin", payload=b"exact", sha256=sha256_of_bytes(b"exact"), byte_size=9
    )
    with pytest.raises(_ContentVerificationError):
        _read_back(target, wrong_size)


def test_unexpected_staging_entry_is_rejected(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    original = module._write_exact_once

    def _add_extra(directory: Path, planned: _PlannedFile) -> None:
        original(directory, planned)
        if planned.filename == MANIFEST_FILENAME:
            (directory / "unexpected.txt").write_bytes(b"extra")

    monkeypatch.setattr(module, "_write_exact_once", _add_extra)
    with pytest.raises(_InventoryVerificationError):
        _publish(request_object, result_object, parent, protected)
    staging = _staging_of(parent, result_object)
    assert (staging / "unexpected.txt").exists()


def test_missing_staging_entry_is_rejected(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    original = module._write_exact_once

    def _remove_one(directory: Path, planned: _PlannedFile) -> None:
        original(directory, planned)
        if planned.filename == MANIFEST_FILENAME:
            (directory / "split-summary.json").unlink()

    monkeypatch.setattr(module, "_write_exact_once", _remove_one)
    with pytest.raises(_InventoryVerificationError):
        _publish(request_object, result_object, parent, protected)


def test_non_regular_staging_entry_is_rejected(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    original = module._write_exact_once

    def _add_directory(directory: Path, planned: _PlannedFile) -> None:
        original(directory, planned)
        if planned.filename == MANIFEST_FILENAME:
            (directory / "a-directory").mkdir()

    monkeypatch.setattr(module, "_write_exact_once", _add_directory)
    with pytest.raises(_InventoryVerificationError):
        _publish(request_object, result_object, parent, protected)


def test_no_receipt_is_returned_on_failure(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    def _fail(file_descriptor: int) -> None:
        raise OSError("injected")

    monkeypatch.setattr(module, "_sync_file", _fail)
    outcome: object = "unset"
    with pytest.raises(_PublicationError):
        outcome = _publish(request_object, result_object, parent, protected)
    assert outcome == "unset"


# ---------------------------------------------------------------------------
# Post-rename verification (FD-BPUB-16)
# ---------------------------------------------------------------------------


def test_post_rename_failure_leaves_final_visible(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    original = module._atomic_no_replace_rename

    def _rename_then_damage(source: Path, destination: Path, primitive: str) -> None:
        original(source, destination, primitive)
        (destination / "post-rename-extra").write_bytes(b"damage")

    monkeypatch.setattr(module, "_atomic_no_replace_rename", _rename_then_damage)
    with pytest.raises(_PostRenameVerificationError):
        _publish(request_object, result_object, parent, protected)
    final = parent / f"mesc-p01-04b-split-{_fingerprint(result_object)}"
    assert final.is_dir()
    assert (final / "post-rename-extra").read_bytes() == b"damage"
    assert sorted(entry.name for entry in final.iterdir()) == sorted(
        [*ALL_FILENAMES, "post-rename-extra"]
    )
    assert not _staging_of(parent, result_object).exists()


def test_manifest_presence_does_not_publish(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    def _fail(source: Path, destination: Path, primitive: str) -> None:
        raise _PublicationError("injected rename failure")

    monkeypatch.setattr(module, "_atomic_no_replace_rename", _fail)
    with pytest.raises(_PublicationError):
        _publish(request_object, result_object, parent, protected)
    staging = _staging_of(parent, result_object)
    assert sorted(entry.name for entry in staging.iterdir()) == list(ALL_FILENAMES)
    assert not (parent / f"mesc-p01-04b-split-{_fingerprint(result_object)}").exists()


# ---------------------------------------------------------------------------
# Write ordering and exclusivity (FD-BPUB-10, FD-BPUB-11)
# ---------------------------------------------------------------------------


def test_payloads_are_written_ascending_and_manifest_last(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import medscale.mesc._fixture_publication_v1 as module

    original = module._write_exact_once
    order: list[str] = []

    def _record(directory: Path, planned: _PlannedFile) -> None:
        order.append(planned.filename)
        original(directory, planned)

    monkeypatch.setattr(module, "_write_exact_once", _record)
    _publish(request_object, result_object, parent, protected)
    assert order == [*PAYLOAD_FILENAMES, MANIFEST_FILENAME]
    assert order[:-1] == sorted(order[:-1])
    assert order[-1] == MANIFEST_FILENAME


def test_writes_are_exclusive_and_never_overwrite(tmp_path: Path) -> None:
    from medscale.mesc._fixture_publication_v1 import _write_exact_once

    planned = _PlannedFile(
        filename="only-once.bin",
        payload=b"first",
        sha256=sha256_of_bytes(b"first"),
        byte_size=5,
    )
    _write_exact_once(tmp_path, planned)
    assert (tmp_path / "only-once.bin").read_bytes() == b"first"
    with pytest.raises(_ExclusiveWriteError):
        _write_exact_once(tmp_path, planned)
    assert (tmp_path / "only-once.bin").read_bytes() == b"first"


def test_plan_is_frozen_and_complete_before_mutation(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    from medscale.mesc._fixture_publication_v1 import _build_plan

    plan = _build_plan(request_object, result_object, parent, protected)
    assert list(parent.iterdir()) == []
    assert len(plan.payload_files) == 6
    assert plan.manifest_file.filename == MANIFEST_FILENAME
    assert plan.manifest_file.payload.endswith(b"\n")
    with pytest.raises(AttributeError):
        plan.request_id = "mutated"  # type: ignore[misc]
    with pytest.raises(AttributeError):
        plan.payload_files[0].payload = b"mutated"  # type: ignore[misc]
    second = _build_plan(request_object, result_object, parent, protected)
    assert second.manifest_file.payload == plan.manifest_file.payload


# ---------------------------------------------------------------------------
# Boundary invariants (FD-BPUB-2, FD-BPUB-18)
# ---------------------------------------------------------------------------


def test_public_surfaces_expose_no_publication_name() -> None:
    import medscale
    import medscale.mesc

    for module in (medscale, medscale.mesc):
        exported = set(getattr(module, "__all__", ()))
        for name in ("publish", "publication", "Publication", "PublicationReceipt"):
            assert not any(name in item for item in exported)
        assert not hasattr(module, "_publish_fixture_split_v1")


def test_splitter_remains_fail_closed() -> None:
    with pytest.raises(PilotSplitNotAuthorizedError):
        SourceDocumentGroupedSplitter().assign((), ())
    with pytest.raises(PilotSplitNotAuthorizedError):
        SourceDocumentGroupedSplitter().assign(("a",), ("d",))
    with pytest.raises(PilotSplitNotAuthorizedError):
        SourceDocumentGroupedSplitter().assign(None, None)  # type: ignore[arg-type]


def test_every_error_category_derives_from_one_private_base() -> None:
    from medscale.mesc._fixture_publication_v1 import (
        _FinalRenameError,
        _StagingAcquisitionError,
    )

    categories = (
        _InvalidPublicationInputError,
        _UnsafePublicationPathError,
        _PublicationTargetConflictError,
        _UnsupportedAtomicRenameError,
        _StagingAcquisitionError,
        _ExclusiveWriteError,
        _ContentVerificationError,
        _InventoryVerificationError,
        _FinalRenameError,
        _PostRenameVerificationError,
    )
    assert len(set(categories)) == 10
    for category in categories:
        assert issubclass(category, _PublicationError)
        assert category is not _PublicationError


def test_module_reads_no_clock_randomness_environment_or_network() -> None:
    source = PUBLICATION_MODULE.read_text("utf-8")
    for forbidden in (
        "import time",
        "import random",
        "import secrets",
        "import uuid",
        "import socket",
        "import subprocess",
        "import urllib",
        "import datetime",
        "os.environ",
        "getenv",
    ):
        assert forbidden not in source


def test_published_directory_is_not_promoted_anywhere(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    assert receipt.publication_directory.is_relative_to(parent)
    assert list(protected[0].iterdir()) == []
    assert receipt.publication_directory.parent == parent


def test_published_files_are_regular_and_single_linked(
    request_object: FixtureSplitRequest,
    result_object: FixtureSplitResult,
    parent: Path,
    protected: tuple[Path, ...],
) -> None:
    receipt = _publish(request_object, result_object, parent, protected)
    for entry in receipt.publication_directory.iterdir():
        status = entry.lstat()
        assert stat.S_ISREG(status.st_mode)
        assert not stat.S_ISLNK(status.st_mode)
        assert not getattr(status, "st_file_attributes", 0) & getattr(
            stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
        )
        if os.name != "nt":
            assert status.st_nlink == 1
