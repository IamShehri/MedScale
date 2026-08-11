"""Synthetic qualification of the pure P01-04D formal split layer.

Every input used here is freshly generated synthetic data written under
``tmp_path``.  No test reads a P01-03G registry, an external source-record file
or any real dataset artifact, and no synthetic value copies a real identifier or
real text.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from medscale.mesc._canonical_json_v1 import sha256_of_bytes
from medscale.mesc._formal_split_v1 import (
    ARTIFACT_FILENAMES,
    DECISION_RECORD_SURFACE,
    EXAMPLE_REGISTRY_FILENAME,
    EXCLUDED_LEDGER_FILENAME,
    EXECUTION_INPUT_MANIFEST_SCHEMA,
    GENERATION_MANIFEST_FILENAME,
    GROUP_REGISTRY_FILENAME,
    MINIMUM_PARTITION_SIZES,
    ORDERED_EXAMPLE_REGISTRY_SCHEMA,
    ORDERED_EXAMPLE_REGISTRY_SURFACE,
    REQUIRED_INPUT_SURFACES,
    SOURCE_DOCUMENT_REGISTRY_SCHEMA,
    SOURCE_DOCUMENT_REGISTRY_SURFACE,
    SOURCE_RECORDS_SCHEMA,
    SOURCE_RECORDS_SURFACE,
    SPLIT_POLICY_FILENAME,
    SPLIT_SUMMARY_FILENAME,
    SPLIT_SUMMARY_IDENTITY_CORE_FILENAME,
    TARGET_PARTITION_TOTALS,
    TRANSFORMED_DATASET_IDENTITY_SCHEMA,
    TRANSFORMED_DATASET_IDENTITY_SURFACE,
    FormalArtifactBundle,
    FormalGenerationManifest,
    FormalInputDescriptor,
    FormalInputIdentityError,
    FormalInputSchemaError,
    FormalLabelJoinError,
    FormalSplitInputIdentity,
    allocate_formal_groups,
    build_execution_input_manifest,
    build_formal_bundle,
    build_input_identity,
    build_split_policy_bytes,
    build_split_policy_document,
    execution_input_manifest_bytes,
    execution_input_manifest_identity,
    join_formal_examples,
    parse_ordered_example_registry,
    parse_source_document_registry,
    parse_source_records,
    parse_transformed_dataset_identity,
    verify_bundle,
)

DATASET_ID = "mesc-synthetic-formal-dataset"
DATASET_REVISION = "synthetic-revision-0001"
CONFIGURATION = "synthetic-configuration"
TRANSFORMATION_VERSION = "mesc-synthetic-transform/1"

#: The ratified decision distribution, reproduced with wholly synthetic rows.
SYNTHETIC_LABEL_TOTALS: Mapping[str, int] = {"yes": 552, "no": 338, "maybe": 110}

#: Multi-example indivisible groups per decision, so grouping is not vacuous.
_MULTI_GROUP_SIZES: Mapping[str, tuple[int, ...]] = {
    "yes": (3, 2),
    "no": (3, 2),
    "maybe": (2,),
}


def _synthetic_hash(token: str) -> str:
    return hashlib.sha256(f"mesc-synthetic-formal::{token}".encode()).hexdigest()


def synthetic_group_plan() -> tuple[tuple[str, str, int], ...]:
    """Return ``(decision, source_document_id, example_count)`` in a fixed order."""
    plan: list[tuple[str, str, int]] = []
    for decision in ("yes", "no", "maybe"):
        sizes = list(_MULTI_GROUP_SIZES[decision])
        remaining = SYNTHETIC_LABEL_TOTALS[decision] - sum(sizes)
        sizes.extend([1] * remaining)
        for index, size in enumerate(sizes):
            plan.append((decision, f"mesc-syn-doc-{decision}-{index:04d}", size))
    return tuple(plan)


def synthetic_payloads() -> dict[str, bytes]:
    """Build the five synthetic formal input payloads deterministically."""
    ordered_lines: list[str] = []
    document_lines: list[str] = []
    record_lines: list[str] = []
    ordinal = 0
    for decision, source_document_id, size in synthetic_group_plan():
        document_lines.append(
            json.dumps(
                {
                    "schema_version": SOURCE_DOCUMENT_REGISTRY_SCHEMA,
                    "source_document_id": source_document_id,
                    "example_count": size,
                },
                sort_keys=True,
            )
        )
        for member in range(size):
            original_example_id = f"mesc-syn-ex-{ordinal:04d}"
            ordered_lines.append(
                json.dumps(
                    {
                        "schema_version": ORDERED_EXAMPLE_REGISTRY_SCHEMA,
                        "original_example_id": original_example_id,
                        "row_ordinal": ordinal,
                        "source_document_id": source_document_id,
                    },
                    sort_keys=True,
                )
            )
            record_lines.append(
                json.dumps(
                    {
                        "schema_version": SOURCE_RECORDS_SCHEMA,
                        "source_record_hash": _synthetic_hash(f"{original_example_id}:{member}"),
                        "record": {
                            "dataset_id": DATASET_ID,
                            "dataset_revision": DATASET_REVISION,
                            "configuration": CONFIGURATION,
                            "original_example_id": original_example_id,
                            "source_document_id": source_document_id,
                            "final_decision": decision,
                        },
                    },
                    sort_keys=True,
                )
            )
            ordinal += 1

    ordered_bytes = ("\n".join(ordered_lines) + "\n").encode("utf-8")
    document_bytes = ("\n".join(document_lines) + "\n").encode("utf-8")
    records_bytes = ("\n".join(record_lines) + "\n").encode("utf-8")
    identity_bytes = (
        json.dumps(
            {
                "schema_version": TRANSFORMED_DATASET_IDENTITY_SCHEMA,
                "dataset_id": DATASET_ID,
                "dataset_revision": DATASET_REVISION,
                "configuration": CONFIGURATION,
                "transformation_version": TRANSFORMATION_VERSION,
                "source_records_sha256": sha256_of_bytes(records_bytes),
                "source_records_byte_size": len(records_bytes),
            },
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    decision_bytes = b"# Synthetic ratified decision record\n\nD1 through D10 (synthetic copy).\n"
    return {
        ORDERED_EXAMPLE_REGISTRY_SURFACE: ordered_bytes,
        SOURCE_DOCUMENT_REGISTRY_SURFACE: document_bytes,
        TRANSFORMED_DATASET_IDENTITY_SURFACE: identity_bytes,
        SOURCE_RECORDS_SURFACE: records_bytes,
        DECISION_RECORD_SURFACE: decision_bytes,
    }


_SURFACE_FILENAMES: Mapping[str, str] = {
    ORDERED_EXAMPLE_REGISTRY_SURFACE: "ordered-example-id-registry.jsonl",
    SOURCE_DOCUMENT_REGISTRY_SURFACE: "source-document-id-registry.jsonl",
    TRANSFORMED_DATASET_IDENTITY_SURFACE: "transformed-dataset-identity.json",
    SOURCE_RECORDS_SURFACE: "source-records.jsonl",
    DECISION_RECORD_SURFACE: "decision-record.md",
}


def write_synthetic_inputs(
    directory: Path, payloads: Mapping[str, bytes] | None = None
) -> dict[str, Path]:
    """Write the synthetic inputs into a temporary directory and return their locations."""
    directory.mkdir(parents=True, exist_ok=True)
    resolved = dict(payloads) if payloads is not None else synthetic_payloads()
    locations: dict[str, Path] = {}
    for surface, payload in resolved.items():
        target = directory / _SURFACE_FILENAMES[surface]
        target.write_bytes(payload)
        locations[surface] = target.resolve()
    return locations


def build_synthetic_bundle(payloads: Mapping[str, bytes] | None = None) -> FormalArtifactBundle:
    """Run the whole pure pipeline over synthetic payloads."""
    resolved = dict(payloads) if payloads is not None else synthetic_payloads()
    identity = build_input_identity(resolved)
    dataset_identity = parse_transformed_dataset_identity(
        resolved[TRANSFORMED_DATASET_IDENTITY_SURFACE]
    )
    joined = join_formal_examples(
        parse_ordered_example_registry(resolved[ORDERED_EXAMPLE_REGISTRY_SURFACE]),
        parse_source_records(resolved[SOURCE_RECORDS_SURFACE]),
        dataset_identity,
        parse_source_document_registry(resolved[SOURCE_DOCUMENT_REGISTRY_SURFACE]),
    )
    return build_formal_bundle(
        input_identity=identity, joined=joined, assignments=allocate_formal_groups(joined)
    )


@pytest.fixture(scope="module")
def bundle() -> FormalArtifactBundle:
    return build_synthetic_bundle()


# ---------------------------------------------------------------------------
# Dataclass contracts
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "cls", [FormalInputDescriptor, FormalSplitInputIdentity, FormalGenerationManifest]
)
def test_required_dataclasses_are_frozen_and_slotted(cls: type) -> None:
    assert dataclasses.is_dataclass(cls)
    assert cls.__dataclass_params__.frozen  # type: ignore[attr-defined]
    assert "__slots__" in cls.__dict__


def test_input_identity_snapshots_caller_sequence() -> None:
    payloads = synthetic_payloads()
    identity = build_input_identity(payloads)
    mutable = list(identity.descriptors)
    mutable.clear()
    assert len(identity.descriptors) == len(REQUIRED_INPUT_SURFACES)
    with pytest.raises(dataclasses.FrozenInstanceError):
        identity.descriptors = ()  # type: ignore[misc]


def test_input_identity_rejects_duplicate_and_missing_surfaces() -> None:
    payloads = synthetic_payloads()
    identity = build_input_identity(payloads)
    first = identity.descriptors[0]
    with pytest.raises(FormalInputIdentityError):
        FormalSplitInputIdentity(descriptors=(*identity.descriptors, first))
    with pytest.raises(FormalInputIdentityError):
        FormalSplitInputIdentity(descriptors=identity.descriptors[:-1])


def test_input_descriptor_rejects_wrong_schema_and_digest() -> None:
    with pytest.raises(FormalInputSchemaError):
        FormalInputDescriptor(
            surface=ORDERED_EXAMPLE_REGISTRY_SURFACE,
            schema_version="wrong/1",
            sha256="0" * 64,
            byte_size=1,
        )
    with pytest.raises(FormalInputIdentityError):
        FormalInputDescriptor(
            surface=DECISION_RECORD_SURFACE, schema_version=None, sha256="Z" * 64, byte_size=1
        )


def test_input_identity_carries_no_content_or_location() -> None:
    identity = build_input_identity(synthetic_payloads())
    document = identity.to_canonical_document()
    text = json.dumps(document, sort_keys=True)
    for prohibited in ("mesc-syn-ex-", "mesc-syn-doc-", "final_decision", "\\", ".jsonl", '.json"'):
        assert prohibited not in text
    # A schema version legitimately carries a version slash; nothing else may
    # carry a directory separator, and no member may be a filesystem location.
    for entry in document:
        assert set(entry) <= {"byte_size", "schema_version", "sha256", "surface"}
        for key, value in entry.items():
            if key == "schema_version":
                continue
            assert "/" not in str(value)


# ---------------------------------------------------------------------------
# Strict input parsing
# ---------------------------------------------------------------------------


def test_parsers_reject_bom_and_invalid_utf8() -> None:
    payloads = synthetic_payloads()
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(b"\xef\xbb\xbf" + payloads[ORDERED_EXAMPLE_REGISTRY_SURFACE])
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(b"\xff\xfe not utf-8 \n")


def test_jsonl_parser_rejects_blank_record_and_missing_terminator() -> None:
    payloads = synthetic_payloads()
    text = payloads[ORDERED_EXAMPLE_REGISTRY_SURFACE].decode("utf-8")
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(text.rstrip("\n").encode("utf-8"))
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(("\n" + text).encode("utf-8"))
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(text.replace("\n", "\r\n").encode("utf-8"))


def test_parser_rejects_duplicate_json_keys_and_boolean_integers() -> None:
    duplicated = (
        f'{{"schema_version":"{ORDERED_EXAMPLE_REGISTRY_SCHEMA}",'
        '"original_example_id":"a","original_example_id":"b",'
        '"row_ordinal":0,"source_document_id":"d"}\n'
    )
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(duplicated.encode("utf-8"))
    boolean = json.dumps(
        {
            "schema_version": ORDERED_EXAMPLE_REGISTRY_SCHEMA,
            "original_example_id": "a",
            "row_ordinal": True,
            "source_document_id": "d",
        }
    )
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry((boolean + "\n").encode("utf-8"))


def test_parser_rejects_unknown_member_and_wrong_schema() -> None:
    extra = json.dumps(
        {
            "schema_version": ORDERED_EXAMPLE_REGISTRY_SCHEMA,
            "original_example_id": "a",
            "row_ordinal": 0,
            "source_document_id": "d",
            "note": "x",
        }
    )
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry((extra + "\n").encode("utf-8"))
    wrong = json.dumps(
        {
            "schema_version": "mesc-pilot-01-other/1",
            "original_example_id": "a",
            "row_ordinal": 0,
            "source_document_id": "d",
        }
    )
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry((wrong + "\n").encode("utf-8"))


def test_parser_rejects_duplicate_identity_and_non_contiguous_ordinals() -> None:
    payloads = synthetic_payloads()
    lines = payloads[ORDERED_EXAMPLE_REGISTRY_SURFACE].decode("utf-8").splitlines()
    duplicated = "\n".join([*lines, lines[0]]) + "\n"
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(duplicated.encode("utf-8"))
    shifted = json.loads(lines[0])
    shifted["row_ordinal"] = 10_000
    gapped = "\n".join([json.dumps(shifted, sort_keys=True), *lines[1:]]) + "\n"
    with pytest.raises(FormalInputSchemaError):
        parse_ordered_example_registry(gapped.encode("utf-8"))


def test_source_records_reject_free_text_members() -> None:
    payloads = synthetic_payloads()
    lines = payloads[SOURCE_RECORDS_SURFACE].decode("utf-8").splitlines()
    envelope = json.loads(lines[0])
    envelope["record"]["question"] = "synthetic prohibited text"
    poisoned = "\n".join([json.dumps(envelope, sort_keys=True), *lines[1:]]) + "\n"
    with pytest.raises(FormalInputSchemaError, match="free-text"):
        parse_source_records(poisoned.encode("utf-8"))


def test_source_records_reduce_to_identity_and_label_only() -> None:
    labels = parse_source_records(synthetic_payloads()[SOURCE_RECORDS_SURFACE])
    assert len(labels) == sum(TARGET_PARTITION_TOTALS.values())
    fields = {field.name for field in dataclasses.fields(labels[0])}
    assert fields == {
        "dataset_id",
        "dataset_revision",
        "configuration",
        "original_example_id",
        "source_document_id",
        "decision",
        "source_record_hash",
    }


def test_source_document_registry_disagreement_is_rejected() -> None:
    payloads = synthetic_payloads()
    lines = payloads[SOURCE_DOCUMENT_REGISTRY_SURFACE].decode("utf-8").splitlines()
    record = json.loads(lines[0])
    record["example_count"] += 1
    broken = "\n".join([json.dumps(record, sort_keys=True), *lines[1:]]) + "\n"
    payloads[SOURCE_DOCUMENT_REGISTRY_SURFACE] = broken.encode("utf-8")
    with pytest.raises(FormalInputIdentityError, match="source-document registry"):
        build_synthetic_bundle(payloads)


def test_orphan_and_unexpected_label_records_are_rejected() -> None:
    payloads = synthetic_payloads()
    lines = payloads[SOURCE_RECORDS_SURFACE].decode("utf-8").splitlines()
    payloads[SOURCE_RECORDS_SURFACE] = ("\n".join(lines[:-1]) + "\n").encode("utf-8")
    identity = json.loads(payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE])
    identity["source_records_sha256"] = sha256_of_bytes(payloads[SOURCE_RECORDS_SURFACE])
    identity["source_records_byte_size"] = len(payloads[SOURCE_RECORDS_SURFACE])
    payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE] = (
        json.dumps(identity, sort_keys=True) + "\n"
    ).encode("utf-8")
    with pytest.raises(FormalLabelJoinError):
        build_synthetic_bundle(payloads)


def test_dataset_identity_disagreement_is_rejected() -> None:
    payloads = synthetic_payloads()
    identity = json.loads(payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE])
    identity["dataset_revision"] = "synthetic-revision-9999"
    payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE] = (
        json.dumps(identity, sort_keys=True) + "\n"
    ).encode("utf-8")
    with pytest.raises(FormalInputIdentityError, match="dataset identity"):
        build_synthetic_bundle(payloads)


def test_transformed_dataset_identity_round_trip() -> None:
    payloads = synthetic_payloads()
    parsed = parse_transformed_dataset_identity(payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE])
    assert parsed.dataset_id == DATASET_ID
    assert parsed.transformation_version == TRANSFORMATION_VERSION
    assert parsed.source_records_sha256 == sha256_of_bytes(payloads[SOURCE_RECORDS_SURFACE])


# ---------------------------------------------------------------------------
# Scientific identity
# ---------------------------------------------------------------------------


def test_policy_is_deterministic_and_date_free() -> None:
    document = build_split_policy_document()
    assert document["target_counts"] == dict(TARGET_PARTITION_TOTALS)
    assert document["grouping_key"] == "source_document_id"
    assert document["stratification_field"] == "decision"
    assert document["label_order"] == ["yes", "no", "maybe"]
    assert document["partition_order"] == ["train", "validation", "test"]
    assert document["holdout_policy"] == "none"
    assert document["minimum_partition_sizes"] == dict(MINIMUM_PARTITION_SIZES)
    assert build_split_policy_bytes() == build_split_policy_bytes()
    text = build_split_policy_bytes().decode("utf-8")
    for prohibited in ("date", "timestamp", "20", "/home", "C:\\"):
        assert prohibited not in text


def test_policy_contains_no_floating_point_value() -> None:
    def walk(value: object) -> None:
        if isinstance(value, float):  # pragma: no cover - a failure would raise below
            raise AssertionError("policy must not contain a binary float")
        if isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(build_split_policy_document())


def test_totals_grouping_and_stratification(bundle: FormalArtifactBundle) -> None:
    summary = json.loads(bundle.payloads[SPLIT_SUMMARY_FILENAME])
    assert summary["partition_totals"] == dict(TARGET_PARTITION_TOTALS)
    assert summary["total_example_count"] == 1000
    assert summary["label_totals"] == dict(SYNTHETIC_LABEL_TOTALS)
    assert summary["excluded_record_count"] == 0
    assert summary["partition_totals"]["validation"] >= MINIMUM_PARTITION_SIZES["validation"]
    assert summary["partition_totals"]["test"] >= MINIMUM_PARTITION_SIZES["test"]
    groups = [json.loads(line) for line in bundle.payloads[GROUP_REGISTRY_FILENAME].splitlines()]
    by_document: dict[str, set[str]] = {}
    for group in groups:
        by_document.setdefault(group["source_document_id"], set()).add(group["assigned_split"])
    assert all(len(splits) == 1 for splits in by_document.values())
    assert any(group["example_count"] > 1 for group in groups)


def test_apportionment_and_allocation_are_deterministic() -> None:
    first = build_synthetic_bundle()
    second = build_synthetic_bundle()
    assert first.payloads[EXAMPLE_REGISTRY_FILENAME] == second.payloads[EXAMPLE_REGISTRY_FILENAME]
    assert first.split_fingerprint == second.split_fingerprint


def test_label_source_order_does_not_change_bytes() -> None:
    payloads = synthetic_payloads()
    baseline = build_synthetic_bundle(payloads)
    lines = payloads[SOURCE_RECORDS_SURFACE].decode("utf-8").splitlines()
    reordered = ("\n".join(reversed(lines)) + "\n").encode("utf-8")
    identity = json.loads(payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE])
    identity["source_records_sha256"] = sha256_of_bytes(reordered)
    identity["source_records_byte_size"] = len(reordered)
    payloads[SOURCE_RECORDS_SURFACE] = reordered
    payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE] = (
        json.dumps(identity, sort_keys=True) + "\n"
    ).encode("utf-8")
    shuffled = build_synthetic_bundle(payloads)
    for filename in ARTIFACT_FILENAMES:
        if filename == GENERATION_MANIFEST_FILENAME:
            continue
        assert shuffled.payloads[filename] == baseline.payloads[filename]
    assert shuffled.split_fingerprint == baseline.split_fingerprint


def test_wrong_population_size_fails_closed() -> None:
    payloads = synthetic_payloads()
    lines = payloads[ORDERED_EXAMPLE_REGISTRY_SURFACE].decode("utf-8").splitlines()
    payloads[ORDERED_EXAMPLE_REGISTRY_SURFACE] = ("\n".join(lines[:-1]) + "\n").encode("utf-8")
    with pytest.raises((FormalLabelJoinError, FormalInputSchemaError)):
        build_synthetic_bundle(payloads)


# ---------------------------------------------------------------------------
# Artifact bytes
# ---------------------------------------------------------------------------


def test_exact_seven_artifact_inventory(bundle: FormalArtifactBundle) -> None:
    assert sorted(bundle.payloads) == sorted(ARTIFACT_FILENAMES)
    assert len(ARTIFACT_FILENAMES) == 7
    assert ARTIFACT_FILENAMES == (
        "split-policy.json",
        "group-registry.jsonl",
        "example-registry.jsonl",
        "excluded-ledger.json",
        "split-summary-identity-core.json",
        "split-summary.json",
        "generation-manifest.json",
    )
    assert "split-fingerprint.json" not in bundle.payloads
    assert bundle.ordered_payloads()[-1][0] == GENERATION_MANIFEST_FILENAME


def test_artifact_schema_versions(bundle: FormalArtifactBundle) -> None:
    assert json.loads(bundle.payloads[SPLIT_POLICY_FILENAME])["schema_version"] == (
        "mesc-pilot-01-split-policy/1"
    )
    assert json.loads(bundle.payloads[EXCLUDED_LEDGER_FILENAME])["schema_version"] == (
        "mesc-pilot-01-excluded-ledger/1"
    )
    assert json.loads(bundle.payloads[SPLIT_SUMMARY_IDENTITY_CORE_FILENAME])["schema_version"] == (
        "mesc-pilot-01-split-summary-identity-core/1"
    )
    assert json.loads(bundle.payloads[SPLIT_SUMMARY_FILENAME])["schema_version"] == (
        "mesc-pilot-01-split-summary/1"
    )
    first_group = json.loads(bundle.payloads[GROUP_REGISTRY_FILENAME].splitlines()[0])
    assert first_group["schema_version"] == "mesc-pilot-01-group-registry/1"
    first_example = json.loads(bundle.payloads[EXAMPLE_REGISTRY_FILENAME].splitlines()[0])
    assert first_example["schema_version"] == "mesc-pilot-01-example-registry/1"


def test_canonical_jsonl_bytes_end_in_single_line_feed(bundle: FormalArtifactBundle) -> None:
    for filename in (GROUP_REGISTRY_FILENAME, EXAMPLE_REGISTRY_FILENAME):
        payload = bundle.payloads[filename]
        assert payload.endswith(b"\n")
        assert b"\n\n" not in payload
        assert b"\r" not in payload
    for filename in (SPLIT_POLICY_FILENAME, SPLIT_SUMMARY_FILENAME):
        assert bundle.payloads[filename].endswith(b"\n")
        assert bundle.payloads[filename].count(b"\n") == 1


def test_registry_ordering_is_canonical(bundle: FormalArtifactBundle) -> None:
    groups = [json.loads(line) for line in bundle.payloads[GROUP_REGISTRY_FILENAME].splitlines()]
    assert groups == sorted(groups, key=lambda item: (item["assigned_split"], item["group_id"]))
    examples = [
        json.loads(line) for line in bundle.payloads[EXAMPLE_REGISTRY_FILENAME].splitlines()
    ]
    assert examples == sorted(
        examples,
        key=lambda item: (item["assigned_split"], item["row_ordinal"], item["example_id"]),
    )


def test_no_raw_text_reaches_any_artifact(bundle: FormalArtifactBundle) -> None:
    for payload in bundle.payloads.values():
        text = payload.decode("utf-8")
        for prohibited in ("question", "context", "long_answer", "rationale", "final_decision"):
            assert prohibited not in text


def test_excluded_ledger_is_the_deterministic_empty_ledger(bundle: FormalArtifactBundle) -> None:
    ledger = json.loads(bundle.payloads[EXCLUDED_LEDGER_FILENAME])
    assert ledger == {
        "count": 0,
        "excluded_ids": [],
        "reason": "none",
        "schema_version": "mesc-pilot-01-excluded-ledger/1",
    }


def test_authoritative_fingerprint_and_compatibility_hash(bundle: FormalArtifactBundle) -> None:
    assert len(bundle.split_fingerprint) == 64
    assert bundle.split_fingerprint == bundle.split_fingerprint.lower()
    assert all(character in "0123456789abcdef" for character in bundle.split_fingerprint)
    summary = json.loads(bundle.payloads[SPLIT_SUMMARY_FILENAME])
    assert summary["split_fingerprint"] == bundle.split_fingerprint
    assert len(summary["split_hash"]) == 16
    assert summary["split_hash"] != bundle.split_fingerprint[:16]
    core = json.loads(bundle.payloads[SPLIT_SUMMARY_IDENTITY_CORE_FILENAME])
    assert "split_fingerprint" not in core
    assert "split_hash" not in core


def test_manifest_is_non_circular_and_metadata_free(bundle: FormalArtifactBundle) -> None:
    manifest = json.loads(bundle.payloads[GENERATION_MANIFEST_FILENAME])
    assert manifest["bundle_filenames"] == list(ARTIFACT_FILENAMES)
    digested = [entry["filename"] for entry in manifest["artifacts"]]
    assert GENERATION_MANIFEST_FILENAME not in digested
    assert len(digested) == 6
    assert manifest["split_fingerprint"] == bundle.split_fingerprint
    text = bundle.payloads[GENERATION_MANIFEST_FILENAME].decode("utf-8")
    for prohibited in ("workspace", "hostname", "username", "pid", "argv", "generation_identity"):
        assert prohibited not in text
    assert sha256_of_bytes(bundle.payloads[GENERATION_MANIFEST_FILENAME]) not in text
    assert str(len(bundle.payloads[GENERATION_MANIFEST_FILENAME])) not in manifest


def test_manifest_binds_every_input_identity(bundle: FormalArtifactBundle) -> None:
    manifest = json.loads(bundle.payloads[GENERATION_MANIFEST_FILENAME])
    surfaces = sorted(entry["surface"] for entry in manifest["input_identity"])
    assert surfaces == sorted(REQUIRED_INPUT_SURFACES)
    for entry in manifest["input_identity"]:
        assert len(entry["sha256"]) == 64
        assert entry["byte_size"] > 0


def test_verify_bundle_accepts_and_rejects(bundle: FormalArtifactBundle) -> None:
    verify_bundle(bundle)
    tampered = dict(bundle.payloads)
    tampered[SPLIT_POLICY_FILENAME] = tampered[SPLIT_POLICY_FILENAME] + b" "
    broken = FormalArtifactBundle(
        payloads=tampered,
        split_fingerprint=bundle.split_fingerprint,
        split_hash=bundle.split_hash,
        manifest=bundle.manifest,
    )
    with pytest.raises(Exception, match="descriptor"):
        verify_bundle(broken)


def test_bundle_rejects_wrong_inventory(bundle: FormalArtifactBundle) -> None:
    short = {
        name: value for name, value in bundle.payloads.items() if name != SPLIT_POLICY_FILENAME
    }
    with pytest.raises(Exception, match="bundle must contain"):
        FormalArtifactBundle(
            payloads=short,
            split_fingerprint=bundle.split_fingerprint,
            split_hash=bundle.split_hash,
            manifest=bundle.manifest,
        )


def test_write_synthetic_inputs_round_trip(tmp_path: Path) -> None:
    payloads = synthetic_payloads()
    locations = write_synthetic_inputs(tmp_path / "inputs", payloads)
    assert sorted(locations) == sorted(REQUIRED_INPUT_SURFACES)
    for surface, location in locations.items():
        assert location.read_bytes() == payloads[surface]


def test_synthetic_plan_shape() -> None:
    plan: Sequence[tuple[str, str, int]] = synthetic_group_plan()
    assert sum(size for _, _, size in plan) == 1000
    assert len({source_document_id for _, source_document_id, _ in plan}) == len(plan)
    assert {decision for decision, _, _ in plan} == {"yes", "no", "maybe"}
    assert sum(1 for _, _, size in plan if size > 1) == 5


# ---------------------------------------------------------------------------
# XD-EXEC-3 / P-C1b — the execution-input manifest
#
# The contract is `p01-04d-execution-input-identity/founder-authorization.md`.
# Every literal below is an expected value taken from that adopted contract,
# never one discovered by reading the implementation back.
# ---------------------------------------------------------------------------

EXPECTED_MANIFEST_SCHEMA = "mesc-p01-04d-execution-input/manifest/v1"
EXPECTED_MANIFEST_TOP_LEVEL = ("input_surfaces", "schema_version")
EXPECTED_SURFACE_REQUIRED = ("byte_size", "sha256", "surface")


def manifest_entries(manifest: Mapping[str, object]) -> list[Mapping[str, object]]:
    """Return the manifest entries with a concrete type for static checking."""
    entries = manifest["input_surfaces"]
    assert isinstance(entries, list)
    for entry in entries:
        assert isinstance(entry, dict)
    return list(entries)


def test_execution_input_manifest_covers_exactly_the_five_surfaces() -> None:
    identity = build_input_identity(synthetic_payloads())
    manifest = build_execution_input_manifest(identity)
    surfaces = [str(entry["surface"]) for entry in manifest_entries(manifest)]

    assert len(surfaces) == 5
    assert sorted(surfaces) == sorted(REQUIRED_INPUT_SURFACES)
    assert surfaces == sorted(surfaces), "entries must be ordered by surface"


def test_execution_input_manifest_field_set_is_exact_and_closed() -> None:
    identity = build_input_identity(synthetic_payloads())
    manifest = build_execution_input_manifest(identity)

    assert tuple(sorted(manifest)) == EXPECTED_MANIFEST_TOP_LEVEL
    assert manifest["schema_version"] == EXPECTED_MANIFEST_SCHEMA
    assert EXECUTION_INPUT_MANIFEST_SCHEMA == EXPECTED_MANIFEST_SCHEMA

    for entry in manifest_entries(manifest):
        required = set(EXPECTED_SURFACE_REQUIRED)
        permitted = required | {"schema_version"}
        assert required <= set(entry) <= permitted, entry


def test_absent_schema_version_is_omitted_and_never_null() -> None:
    """The decision record is Markdown governance prose and declares no schema."""
    identity = build_input_identity(synthetic_payloads())
    manifest = build_execution_input_manifest(identity)
    entries = {entry["surface"]: entry for entry in manifest_entries(manifest)}

    assert "schema_version" not in entries[DECISION_RECORD_SURFACE]
    assert "schema_version" in entries[SOURCE_RECORDS_SURFACE]
    assert b"null" not in execution_input_manifest_bytes(identity)


def test_execution_input_manifest_bytes_are_deterministic_and_canonical() -> None:
    payloads = synthetic_payloads()
    first = execution_input_manifest_bytes(build_input_identity(payloads))
    second = execution_input_manifest_bytes(build_input_identity(dict(payloads)))

    assert first == second
    assert first.endswith(b"\n")
    assert first.count(b"\n") == 1
    assert b", " not in first and b": " not in first
    decoded = json.loads(first.decode("utf-8"))
    assert list(decoded) == sorted(decoded), "object keys must be sorted"


def test_execution_input_manifest_identity_is_deterministic() -> None:
    payloads = synthetic_payloads()
    identity = build_input_identity(payloads)
    payload = execution_input_manifest_bytes(identity)
    first = execution_input_manifest_identity(identity)
    second = execution_input_manifest_identity(build_input_identity(dict(payloads)))

    assert first == second
    assert first.sha256 == sha256_of_bytes(payload)
    assert first.byte_size == len(payload)
    assert len(first.sha256) == 64


def test_a_changed_input_changes_the_manifest_identity() -> None:
    payloads = synthetic_payloads()
    before = execution_input_manifest_identity(build_input_identity(payloads))
    mutated = dict(payloads)
    mutated[DECISION_RECORD_SURFACE] = payloads[DECISION_RECORD_SURFACE] + b"\n"

    after = execution_input_manifest_identity(build_input_identity(mutated))
    assert after != before


def test_execution_input_manifest_leaks_no_path_time_commit_or_content() -> None:
    payloads = synthetic_payloads()
    text = execution_input_manifest_bytes(build_input_identity(payloads)).decode("utf-8")

    for prohibited in (
        "path",
        "location",
        "workspace",
        "timestamp",
        "recorded_at",
        "commit",
        "partition",
        "question",
        "context",
        "answer",
        "annotation",
        "final_decision",
        "label",
    ):
        assert prohibited not in text, prohibited
    # No input payload byte may appear in the manifest.
    for payload in payloads.values():
        assert payload[:64].decode("utf-8", "ignore") not in text


def test_execution_input_manifest_is_distinct_from_the_generation_manifest() -> None:
    """F3: the seven-file bundle's generation manifest is a different concept."""
    from medscale.mesc._formal_split_v1 import GENERATION_MANIFEST_SCHEMA

    execution_schema: str = EXECUTION_INPUT_MANIFEST_SCHEMA
    generation_schema: str = GENERATION_MANIFEST_SCHEMA
    assert execution_schema != generation_schema
    assert "execution-input" in EXECUTION_INPUT_MANIFEST_SCHEMA
    assert GENERATION_MANIFEST_FILENAME not in EXECUTION_INPUT_MANIFEST_SCHEMA
    assert GENERATION_MANIFEST_FILENAME in ARTIFACT_FILENAMES


def test_execution_input_manifest_requires_an_exact_identity_object() -> None:
    with pytest.raises(FormalInputIdentityError):
        build_execution_input_manifest({"not": "an identity"})  # type: ignore[arg-type]
