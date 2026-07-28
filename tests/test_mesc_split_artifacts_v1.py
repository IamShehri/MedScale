"""Artifact descriptor, identity core and non-circular fingerprint tests (FD-B2A-4..8).

Golden fingerprint and byte literals are derived independently of the code under
test.  Every input here is synthetic: no P01-03G registry, no dataset, no model,
no inference, no retrieval, no training, no metric and no benchmark is touched.
"""

from __future__ import annotations

import builtins
import dataclasses
import hashlib
import os
import pathlib
import socket
from pathlib import Path
from typing import Any

import pytest

from medscale.mesc._canonical_json_v1 import (
    CanonicalContractError,
    UnsupportedValueTypeError,
    canonical_json_bytes,
    sha256_of_bytes,
)
from medscale.mesc._split_artifacts_v1 import (
    ARTIFACT_SCHEMA_VERSIONS,
    BUNDLE_SCHEMA_VERSION,
    REQUIRED_ARTIFACT_ROLES,
    DuplicateArtifactRoleError,
    FingerprintMismatchError,
    ForbiddenDateOrTimestampError,
    ForbiddenRuntimeMetadataError,
    InvalidByteSizeError,
    InvalidSchemaVersionError,
    InvalidSha256Error,
    MissingArtifactRoleError,
    SplitArtifactDescriptor,
    SplitFingerprintIdentity,
    SplitFingerprintRecord,
    SplitSummaryIdentityCore,
    UnknownArtifactRoleError,
    build_split_fingerprint_identity,
    build_split_fingerprint_record,
    compute_split_fingerprint,
    descriptor_for_bytes,
    reject_forbidden_metadata,
    validate_descriptor_set,
    verify_descriptor_against_bytes,
    verify_split_fingerprint_record,
    verify_split_summary_binding,
)

# --------------------------------------------------------------------------
# Synthetic fixtures and golden literals
# --------------------------------------------------------------------------

GROUP_REGISTRY_PAYLOAD = b'{"groups":[]}\n'
EXAMPLE_REGISTRY_PAYLOAD = b'{"examples":[]}\n'
EXCLUDED_LEDGER_PAYLOAD = b'{"excluded":[]}\n'

VALID_SHA256 = "0" * 64

GOLDEN_CORE_BYTES = (
    b'{"algorithm_version":"mesc-pilot-01-split-algorithm/1","excluded_record_count":1,'
    b'"group_counts_by_partition":{"test":1,"train":4,"validation":1},'
    b'"label_totals":{"maybe":1,"no":2,"yes":3},"partition_label_matrix":{'
    b'"test":{"maybe":0,"no":0,"yes":1},"train":{"maybe":1,"no":2,"yes":1},'
    b'"validation":{"maybe":0,"no":0,"yes":1}},'
    b'"partition_totals":{"test":1,"train":4,"validation":1},'
    b'"schema_version":"mesc-pilot-01-split-summary-identity-core/1",'
    b'"total_example_count":6,"total_group_count":6}\n'
)
GOLDEN_CORE_SHA256 = "e7aaf30801c173bf02bf190f209c8dd2a4bdb5943f6e83b7ea882d305a9e6013"
GOLDEN_SPLIT_FINGERPRINT = "7e2b2b7c5a55bd21bd945ff8c37ee24ab990a64e9c7adee18b7f99f4aae1fce4"

GOLDEN_DESCRIPTOR_DIGESTS = {
    "example_registry": "8618178ea17f0198166e7aedf05e59d6ef9aa84bd498fe3993b2999f558f7857",
    "excluded_ledger": "08b2cd9f4ff7afc83c51f013b2ff0cf9bfcd8c7d9859f60e15c8fb9ace82d20e",
    "group_registry": "9f7ee9af3b6ad9e558e0a4ea51eba331d78e719b0246550529e656be79976fde",
    "split_summary": GOLDEN_CORE_SHA256,
}
GOLDEN_DESCRIPTOR_SIZES = {
    "example_registry": 16,
    "excluded_ledger": 16,
    "group_registry": 14,
    "split_summary": 488,
}


def make_core(**overrides: Any) -> SplitSummaryIdentityCore:
    fields: dict[str, Any] = {
        "total_example_count": 6,
        "total_group_count": 6,
        "excluded_record_count": 1,
        "partition_totals": {"test": 1, "train": 4, "validation": 1},
        "label_totals": {"maybe": 1, "no": 2, "yes": 3},
        "partition_label_matrix": {
            "test": {"maybe": 0, "no": 0, "yes": 1},
            "train": {"maybe": 1, "no": 2, "yes": 1},
            "validation": {"maybe": 0, "no": 0, "yes": 1},
        },
        "group_counts_by_partition": {"test": 1, "train": 4, "validation": 1},
        "algorithm_version": "mesc-pilot-01-split-algorithm/1",
    }
    fields.update(overrides)
    return SplitSummaryIdentityCore(**fields)


def make_identity(**overrides: Any) -> SplitFingerprintIdentity:
    fields: dict[str, Any] = {
        "policy_id": "mesc-pilot-01-split-policy/1",
        "algorithm_version": "mesc-pilot-01-split-algorithm/1",
        "split_seed": "mesc-pilot-01-split-v1",
        "group_registry_payload": GROUP_REGISTRY_PAYLOAD,
        "example_registry_payload": EXAMPLE_REGISTRY_PAYLOAD,
        "excluded_ledger_payload": EXCLUDED_LEDGER_PAYLOAD,
        "split_summary_identity_core": make_core(),
    }
    fields.update(overrides)
    return build_split_fingerprint_identity(**fields)


def make_descriptors() -> tuple[SplitArtifactDescriptor, ...]:
    return make_identity().artifact_descriptors


# --------------------------------------------------------------------------
# Role allowlist
# --------------------------------------------------------------------------


def test_required_roles_are_exactly_the_ratified_four() -> None:
    assert set(REQUIRED_ARTIFACT_ROLES) == {
        "group_registry",
        "example_registry",
        "split_summary",
        "excluded_ledger",
    }
    assert len(REQUIRED_ARTIFACT_ROLES) == 4


def test_required_roles_are_in_ascending_order() -> None:
    assert tuple(sorted(REQUIRED_ARTIFACT_ROLES)) == REQUIRED_ARTIFACT_ROLES
    assert REQUIRED_ARTIFACT_ROLES == (
        "example_registry",
        "excluded_ledger",
        "group_registry",
        "split_summary",
    )


def test_leakage_report_is_not_a_required_role() -> None:
    for name in ("leakage_report", "leakage", "leakage_audit"):
        assert name not in REQUIRED_ARTIFACT_ROLES
        assert name not in ARTIFACT_SCHEMA_VERSIONS


def test_exact_schema_identifiers() -> None:
    assert ARTIFACT_SCHEMA_VERSIONS == {
        "example_registry": "mesc-pilot-01-example-registry/1",
        "excluded_ledger": "mesc-pilot-01-excluded-ledger/1",
        "group_registry": "mesc-pilot-01-group-registry/1",
        "split_summary": "mesc-pilot-01-split-summary-identity-core/1",
    }
    assert BUNDLE_SCHEMA_VERSION == "mesc-pilot-01-split-fingerprint-bundle/1"


# --------------------------------------------------------------------------
# Descriptor validation
# --------------------------------------------------------------------------


def test_descriptor_binds_actual_bytes() -> None:
    descriptor = descriptor_for_bytes(role="group_registry", payload=GROUP_REGISTRY_PAYLOAD)
    assert descriptor.sha256 == GOLDEN_DESCRIPTOR_DIGESTS["group_registry"]
    assert descriptor.byte_size == GOLDEN_DESCRIPTOR_SIZES["group_registry"]
    assert descriptor.schema_version == ARTIFACT_SCHEMA_VERSIONS["group_registry"]
    verify_descriptor_against_bytes(descriptor, GROUP_REGISTRY_PAYLOAD)


def test_descriptor_is_immutable() -> None:
    descriptor = descriptor_for_bytes(role="group_registry", payload=GROUP_REGISTRY_PAYLOAD)
    with pytest.raises(dataclasses.FrozenInstanceError):
        descriptor.byte_size = 1  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        descriptor.role = "split_summary"  # type: ignore[misc]


def test_identity_core_and_record_are_immutable() -> None:
    core = make_core()
    with pytest.raises(dataclasses.FrozenInstanceError):
        core.total_example_count = 7  # type: ignore[misc]
    record = build_split_fingerprint_record(make_identity())
    with pytest.raises(dataclasses.FrozenInstanceError):
        record.split_fingerprint = VALID_SHA256  # type: ignore[misc]


@pytest.mark.parametrize(
    "bad",
    ["", "abc", "0" * 63, "0" * 65, "A" * 64, "0" * 63 + "g", "0" * 63 + "Z", " " * 64],
)
def test_invalid_sha256_formats_are_rejected(bad: str) -> None:
    with pytest.raises(InvalidSha256Error) as excinfo:
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=ARTIFACT_SCHEMA_VERSIONS["group_registry"],
            sha256=bad,
            byte_size=1,
        )
    assert excinfo.value.code == "invalid_sha256"


@pytest.mark.parametrize("bad", [None, 123, b"0" * 64, ["0" * 64]])
def test_non_string_sha256_is_rejected(bad: object) -> None:
    with pytest.raises(InvalidSha256Error):
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=ARTIFACT_SCHEMA_VERSIONS["group_registry"],
            sha256=bad,  # type: ignore[arg-type]
            byte_size=1,
        )


def test_uppercase_sha256_is_rejected() -> None:
    digest = sha256_of_bytes(GROUP_REGISTRY_PAYLOAD).upper()
    with pytest.raises(InvalidSha256Error):
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=ARTIFACT_SCHEMA_VERSIONS["group_registry"],
            sha256=digest,
            byte_size=14,
        )


def test_negative_byte_size_is_rejected() -> None:
    with pytest.raises(InvalidByteSizeError) as excinfo:
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=ARTIFACT_SCHEMA_VERSIONS["group_registry"],
            sha256=VALID_SHA256,
            byte_size=-1,
        )
    assert excinfo.value.code == "invalid_byte_size"


@pytest.mark.parametrize("bad", [True, False])
def test_boolean_byte_size_is_rejected(bad: bool) -> None:
    # bool is an int subclass in Python; FD-B2A-2 forbids relying on that.
    with pytest.raises(InvalidByteSizeError):
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=ARTIFACT_SCHEMA_VERSIONS["group_registry"],
            sha256=VALID_SHA256,
            byte_size=bad,
        )


@pytest.mark.parametrize("bad", [1.0, "1", None, object()])
def test_non_integer_byte_size_is_rejected(bad: object) -> None:
    with pytest.raises(InvalidByteSizeError):
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=ARTIFACT_SCHEMA_VERSIONS["group_registry"],
            sha256=VALID_SHA256,
            byte_size=bad,  # type: ignore[arg-type]
        )


def test_zero_byte_size_is_accepted() -> None:
    descriptor = descriptor_for_bytes(role="excluded_ledger", payload=b"")
    assert descriptor.byte_size == 0
    assert descriptor.sha256 == hashlib.sha256(b"").hexdigest()


@pytest.mark.parametrize("bad", ["", "unknown", "mesc-pilot-01-group-registry/2", None, 1])
def test_invalid_schema_versions_are_rejected(bad: object) -> None:
    with pytest.raises(InvalidSchemaVersionError) as excinfo:
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=bad,  # type: ignore[arg-type]
            sha256=VALID_SHA256,
            byte_size=1,
        )
    assert excinfo.value.code == "invalid_schema_version"


def test_schema_version_of_another_role_is_rejected() -> None:
    with pytest.raises(InvalidSchemaVersionError):
        SplitArtifactDescriptor(
            role="group_registry",
            schema_version=ARTIFACT_SCHEMA_VERSIONS["split_summary"],
            sha256=VALID_SHA256,
            byte_size=1,
        )


@pytest.mark.parametrize("bad", ["leakage_report", "", "GROUP_REGISTRY", None, 1])
def test_unknown_roles_are_rejected(bad: object) -> None:
    with pytest.raises(UnknownArtifactRoleError) as excinfo:
        SplitArtifactDescriptor(
            role=bad,  # type: ignore[arg-type]
            schema_version="mesc-pilot-01-group-registry/1",
            sha256=VALID_SHA256,
            byte_size=1,
        )
    assert excinfo.value.code == "unknown_artifact_role"


def test_descriptor_for_bytes_rejects_unknown_role() -> None:
    with pytest.raises(UnknownArtifactRoleError):
        descriptor_for_bytes(role="leakage_report", payload=b"{}\n")


def test_descriptor_for_bytes_rejects_non_bytes_payload() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        descriptor_for_bytes(role="group_registry", payload="not bytes")  # type: ignore[arg-type]


# --------------------------------------------------------------------------
# Descriptor set: duplicate, missing, ordering
# --------------------------------------------------------------------------


def test_duplicate_role_is_rejected() -> None:
    descriptors = list(make_descriptors())
    descriptors.append(descriptors[0])
    with pytest.raises(DuplicateArtifactRoleError) as excinfo:
        validate_descriptor_set(descriptors)
    assert excinfo.value.code == "duplicate_artifact_role"


def test_missing_role_is_rejected() -> None:
    descriptors = [d for d in make_descriptors() if d.role != "excluded_ledger"]
    with pytest.raises(MissingArtifactRoleError) as excinfo:
        validate_descriptor_set(descriptors)
    assert excinfo.value.code == "missing_artifact_role"
    assert "excluded_ledger" in str(excinfo.value)


def test_empty_descriptor_set_is_rejected() -> None:
    with pytest.raises(MissingArtifactRoleError):
        validate_descriptor_set([])


def test_duplicate_is_reported_before_missing() -> None:
    # Supplying the same role twice and omitting another violates both rules;
    # duplicate is checked first, so the outcome is stable.
    descriptors = [d for d in make_descriptors() if d.role != "excluded_ledger"]
    descriptors.append(descriptors[0])
    with pytest.raises(DuplicateArtifactRoleError):
        validate_descriptor_set(descriptors)


def test_descriptor_ordering_is_role_ascending_regardless_of_input_order() -> None:
    descriptors = list(make_descriptors())
    ordered = validate_descriptor_set(descriptors)
    reversed_order = validate_descriptor_set(list(reversed(descriptors)))
    assert [d.role for d in ordered] == list(REQUIRED_ARTIFACT_ROLES)
    assert ordered == reversed_order


def test_identity_normalizes_descriptor_order() -> None:
    identity = make_identity()
    assert [d.role for d in identity.artifact_descriptors] == list(REQUIRED_ARTIFACT_ROLES)


def test_validate_descriptor_set_rejects_foreign_objects() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        validate_descriptor_set([object()])  # type: ignore[list-item]


# --------------------------------------------------------------------------
# Descriptor vs actual bytes
# --------------------------------------------------------------------------


def test_sha256_mismatch_against_actual_bytes_is_rejected() -> None:
    descriptor = descriptor_for_bytes(role="group_registry", payload=GROUP_REGISTRY_PAYLOAD)
    with pytest.raises(InvalidSha256Error):
        verify_descriptor_against_bytes(descriptor, b'{"groups":[1]}\n')


def test_byte_size_mismatch_against_actual_bytes_is_rejected() -> None:
    payload = GROUP_REGISTRY_PAYLOAD
    descriptor = SplitArtifactDescriptor(
        role="group_registry",
        schema_version=ARTIFACT_SCHEMA_VERSIONS["group_registry"],
        sha256=sha256_of_bytes(payload),
        byte_size=len(payload) + 1,
    )
    with pytest.raises(InvalidByteSizeError):
        verify_descriptor_against_bytes(descriptor, payload)


def test_every_bound_descriptor_reverifies() -> None:
    payloads = {
        "group_registry": GROUP_REGISTRY_PAYLOAD,
        "example_registry": EXAMPLE_REGISTRY_PAYLOAD,
        "excluded_ledger": EXCLUDED_LEDGER_PAYLOAD,
        "split_summary": make_core().canonical_bytes(),
    }
    for descriptor in make_identity().artifact_descriptors:
        verify_descriptor_against_bytes(descriptor, payloads[descriptor.role])
        assert descriptor.sha256 == GOLDEN_DESCRIPTOR_DIGESTS[descriptor.role]
        assert descriptor.byte_size == GOLDEN_DESCRIPTOR_SIZES[descriptor.role]


# --------------------------------------------------------------------------
# Split-summary identity core
# --------------------------------------------------------------------------


def test_core_golden_bytes_and_digest() -> None:
    core = make_core()
    assert core.canonical_bytes() == GOLDEN_CORE_BYTES
    assert sha256_of_bytes(core.canonical_bytes()) == GOLDEN_CORE_SHA256


def test_core_bytes_end_in_exactly_one_line_feed() -> None:
    data = make_core().canonical_bytes()
    assert data.endswith(b"\n")
    assert data.count(b"\n") == 1


def test_core_excludes_the_fingerprint_and_provenance() -> None:
    data = make_core().canonical_bytes()
    for forbidden in (
        b"split_fingerprint",
        b"split_hash",
        b"timestamp",
        b"date",
        b"hostname",
        b"username",
        b"python",
    ):
        assert forbidden not in data


def test_core_carries_no_per_example_or_raw_text() -> None:
    document = make_core().to_canonical_document()
    assert "example_ids" not in document
    assert "question" not in document
    assert "context" not in document
    assert "answers" not in document


@pytest.mark.parametrize("bad", [True, False, 1.5, "3", None])
def test_core_counts_reject_non_integers_and_booleans(bad: object) -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(total_example_count=bad)


def test_core_counts_reject_negative_values() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(excluded_record_count=-1)


def test_core_mapping_values_reject_booleans() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(partition_totals={"train": True, "test": 1, "validation": 1})


def test_core_mapping_rejects_non_string_keys() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(label_totals={1: 2})


def test_core_matrix_rejects_bad_inner_values() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(partition_label_matrix={"train": {"yes": 1.5}})


@pytest.mark.parametrize("bad", [5, "totals", None, [("train", 1)]])
def test_core_count_mapping_must_be_a_mapping(bad: object) -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(partition_totals=bad)


@pytest.mark.parametrize("bad", [5, "matrix", None, [("train", {})]])
def test_core_matrix_must_be_a_mapping(bad: object) -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(partition_label_matrix=bad)


def test_core_matrix_rows_must_be_mappings() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(partition_label_matrix={"train": 3})


def test_core_rejects_wrong_schema_version() -> None:
    with pytest.raises(InvalidSchemaVersionError):
        make_core(schema_version="mesc-pilot-01-split-summary-identity-core/2")


def test_core_rejects_empty_algorithm_version() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        make_core(algorithm_version="")


# --------------------------------------------------------------------------
# Caller-independent immutable core state
# --------------------------------------------------------------------------


def test_caller_mutation_of_every_top_level_mapping_cannot_change_the_core() -> None:
    totals = {"test": 1, "train": 4, "validation": 1}
    labels = {"maybe": 1, "no": 2, "yes": 3}
    groups = {"test": 1, "train": 4, "validation": 1}
    core = make_core(partition_totals=totals, label_totals=labels, group_counts_by_partition=groups)
    document_before = core.to_canonical_document()
    bytes_before = core.canonical_bytes()
    digest_before = sha256_of_bytes(bytes_before)

    totals["train"] = 999
    totals["injected"] = 1
    labels["yes"] = 999
    del labels["no"]
    groups.clear()

    assert core.to_canonical_document() == document_before
    assert core.canonical_bytes() == bytes_before
    assert sha256_of_bytes(core.canonical_bytes()) == digest_before
    assert core.canonical_bytes() == GOLDEN_CORE_BYTES


def test_caller_mutation_of_nested_matrix_rows_cannot_change_the_core() -> None:
    inner = {"maybe": 1, "no": 2, "yes": 1}
    matrix = {
        "test": {"maybe": 0, "no": 0, "yes": 1},
        "train": inner,
        "validation": {"maybe": 0, "no": 0, "yes": 1},
    }
    core = make_core(partition_label_matrix=matrix)
    bytes_before = core.canonical_bytes()

    inner["yes"] = 999
    inner["injected"] = 7
    matrix["extra"] = {"yes": 1}

    assert core.canonical_bytes() == bytes_before
    assert core.canonical_bytes() == GOLDEN_CORE_BYTES


def test_caller_mutation_cannot_change_the_split_fingerprint() -> None:
    totals = {"test": 1, "train": 4, "validation": 1}
    identity = make_identity(split_summary_identity_core=make_core(partition_totals=totals))
    before = compute_split_fingerprint(identity)
    totals["train"] = 999
    assert compute_split_fingerprint(identity) == before == GOLDEN_SPLIT_FINGERPRINT
    verify_split_fingerprint_record(build_split_fingerprint_record(identity))


def test_returned_document_does_not_expose_mutable_internal_references() -> None:
    core = make_core()
    document = core.to_canonical_document()
    partition_totals = document["partition_totals"]
    assert isinstance(partition_totals, dict)
    partition_totals["train"] = 999
    matrix = document["partition_label_matrix"]
    assert isinstance(matrix, dict)
    matrix["train"]["yes"] = 999
    # Mutating the returned document must not reach the core.
    assert core.canonical_bytes() == GOLDEN_CORE_BYTES
    assert core.to_canonical_document()["partition_totals"] == {
        "test": 1,
        "train": 4,
        "validation": 1,
    }


def test_stored_mappings_are_read_only() -> None:
    core = make_core()
    with pytest.raises(TypeError):
        core.partition_totals["train"] = 999  # type: ignore[index]
    with pytest.raises(TypeError):
        core.partition_label_matrix["train"]["yes"] = 999  # type: ignore[index]


def test_core_insertion_order_does_not_change_bytes() -> None:
    forward = make_core(partition_totals={"test": 1, "train": 4, "validation": 1})
    reverse = make_core(partition_totals={"validation": 1, "train": 4, "test": 1})
    assert forward.canonical_bytes() == reverse.canonical_bytes()


# --------------------------------------------------------------------------
# Forbidden metadata
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "key", ["created_at", "timestamp", "run_date", "start_time", "epoch_seconds"]
)
def test_date_and_timestamp_keys_are_rejected(key: str) -> None:
    with pytest.raises(ForbiddenDateOrTimestampError) as excinfo:
        reject_forbidden_metadata({key: 1})
    assert excinfo.value.code == "forbidden_date_or_timestamp"


@pytest.mark.parametrize(
    "key", ["hostname", "username", "output_path", "python_version", "environment", "command_log"]
)
def test_runtime_metadata_keys_are_rejected(key: str) -> None:
    with pytest.raises(ForbiddenRuntimeMetadataError) as excinfo:
        reject_forbidden_metadata({key: "x"})
    assert excinfo.value.code == "forbidden_runtime_metadata"


def test_forbidden_metadata_is_detected_when_nested() -> None:
    with pytest.raises(ForbiddenRuntimeMetadataError):
        reject_forbidden_metadata({"a": {"b": [{"hostname": "h"}]}})


def test_core_with_forbidden_key_fails_closed() -> None:
    with pytest.raises(ForbiddenRuntimeMetadataError):
        make_core(partition_totals={"hostname": 1}).canonical_bytes()


def test_clean_documents_pass_the_metadata_scan() -> None:
    reject_forbidden_metadata(make_core().to_canonical_document())
    reject_forbidden_metadata(make_identity().to_canonical_document())


# --------------------------------------------------------------------------
# Fingerprint: golden, non-circular, sensitivity
# --------------------------------------------------------------------------


def test_golden_fingerprint_is_exact() -> None:
    assert compute_split_fingerprint(make_identity()) == GOLDEN_SPLIT_FINGERPRINT


def test_fingerprint_is_full_lowercase_64_hex() -> None:
    fingerprint = compute_split_fingerprint(make_identity())
    assert len(fingerprint) == 64
    assert fingerprint == fingerprint.lower()
    assert all(character in "0123456789abcdef" for character in fingerprint)
    # The authoritative value is the full digest, never B1's 16-hex truncation:
    # a truncated form must not be accepted as the fingerprint.
    with pytest.raises(InvalidSha256Error):
        SplitFingerprintRecord(identity=make_identity(), split_fingerprint=fingerprint[:16])


def test_identity_bytes_end_in_exactly_one_line_feed() -> None:
    data = make_identity().canonical_bytes()
    assert data.endswith(b"\n")
    assert data.count(b"\n") == 1


def test_terminal_line_feed_is_inside_the_fingerprint_input() -> None:
    data = make_identity().canonical_bytes()
    assert hashlib.sha256(data).hexdigest() == GOLDEN_SPLIT_FINGERPRINT
    assert hashlib.sha256(data[:-1]).hexdigest() != GOLDEN_SPLIT_FINGERPRINT


def test_identity_payload_never_contains_the_fingerprint() -> None:
    identity = make_identity()
    data = identity.canonical_bytes()
    assert b"split_fingerprint" not in data
    assert GOLDEN_SPLIT_FINGERPRINT.encode() not in data
    assert "split_fingerprint" not in identity.to_canonical_document()


def test_identity_has_no_fingerprint_field_at_all() -> None:
    field_names = {field.name for field in dataclasses.fields(SplitFingerprintIdentity)}
    assert "split_fingerprint" not in field_names


def test_record_is_built_only_after_the_fingerprint_exists() -> None:
    identity = make_identity()
    record = build_split_fingerprint_record(identity)
    assert record.split_fingerprint == GOLDEN_SPLIT_FINGERPRINT
    assert record.identity is identity
    # The completed record is not, and cannot become, its own hash input.
    assert compute_split_fingerprint(record.identity) == record.split_fingerprint


def test_record_bytes_are_not_recursively_fingerprinted() -> None:
    record = build_split_fingerprint_record(make_identity())
    display = {
        "identity": record.identity.to_canonical_document(),
        "split_fingerprint": record.split_fingerprint,
    }
    display_bytes = canonical_json_bytes(display)
    assert b"split_fingerprint" in display_bytes
    # Hashing the display form gives a different value, and the authoritative
    # fingerprint is still the one computed from the identity alone.
    assert sha256_of_bytes(display_bytes) != record.split_fingerprint
    assert compute_split_fingerprint(record.identity) == GOLDEN_SPLIT_FINGERPRINT


def test_split_summary_descriptor_digests_only_the_core() -> None:
    identity = make_identity()
    summary = next(d for d in identity.artifact_descriptors if d.role == "split_summary")
    assert summary.sha256 == GOLDEN_CORE_SHA256
    assert summary.sha256 == sha256_of_bytes(make_core().canonical_bytes())


# --------------------------------------------------------------------------
# split_summary descriptor binding
# --------------------------------------------------------------------------


def _identity_fields(
    summary: SplitArtifactDescriptor, core: SplitSummaryIdentityCore
) -> dict[str, Any]:
    others = [d for d in make_identity().artifact_descriptors if d.role != "split_summary"]
    return {
        "bundle_schema_version": BUNDLE_SCHEMA_VERSION,
        "policy_id": "mesc-pilot-01-split-policy/1",
        "algorithm_version": "mesc-pilot-01-split-algorithm/1",
        "split_seed": "mesc-pilot-01-split-v1",
        "artifact_descriptors": (summary, *others),
        "split_summary_identity_core": core,
    }


def _summary_descriptor(sha256: str, byte_size: int) -> SplitArtifactDescriptor:
    return SplitArtifactDescriptor(
        role="split_summary",
        schema_version=ARTIFACT_SCHEMA_VERSIONS["split_summary"],
        sha256=sha256,
        byte_size=byte_size,
    )


def test_directly_constructed_identity_with_valid_binding_passes() -> None:
    core = make_core()
    summary = _summary_descriptor(GOLDEN_CORE_SHA256, len(core.canonical_bytes()))
    identity = SplitFingerprintIdentity(**_identity_fields(summary, core))
    assert compute_split_fingerprint(identity) == GOLDEN_SPLIT_FINGERPRINT


def test_direct_identity_rejects_wrong_summary_digest() -> None:
    core = make_core()
    summary = _summary_descriptor("a" * 64, len(core.canonical_bytes()))
    with pytest.raises(InvalidSha256Error) as excinfo:
        SplitFingerprintIdentity(**_identity_fields(summary, core))
    assert excinfo.value.code == "invalid_sha256"


def test_direct_identity_rejects_wrong_summary_byte_size() -> None:
    core = make_core()
    summary = _summary_descriptor(GOLDEN_CORE_SHA256, len(core.canonical_bytes()) + 1)
    with pytest.raises(InvalidByteSizeError) as excinfo:
        SplitFingerprintIdentity(**_identity_fields(summary, core))
    assert excinfo.value.code == "invalid_byte_size"


def test_direct_identity_reports_digest_before_size_when_both_are_wrong() -> None:
    core = make_core()
    summary = _summary_descriptor("b" * 64, len(core.canonical_bytes()) + 5)
    with pytest.raises(InvalidSha256Error):
        SplitFingerprintIdentity(**_identity_fields(summary, core))


def test_builder_cannot_accept_an_unbound_summary_descriptor() -> None:
    core = make_core()
    summary = _summary_descriptor("c" * 64, 1)
    with pytest.raises(InvalidSha256Error):
        build_split_fingerprint_record(SplitFingerprintIdentity(**_identity_fields(summary, core)))


def _low_level_identity(
    summary: SplitArtifactDescriptor, core: SplitSummaryIdentityCore
) -> SplitFingerprintIdentity:
    """Bypass __init__/__post_init__ entirely, as a direct low-level path would."""
    identity = object.__new__(SplitFingerprintIdentity)
    fields = _identity_fields(summary, core)
    fields["artifact_descriptors"] = tuple(
        sorted(fields["artifact_descriptors"], key=lambda item: item.role)
    )
    for name, value in fields.items():
        object.__setattr__(identity, name, value)
    return identity


def test_verification_rechecks_binding_built_through_a_low_level_path() -> None:
    core = make_core()
    identity = _low_level_identity(_summary_descriptor("d" * 64, 1), core)
    with pytest.raises(InvalidSha256Error):
        verify_split_summary_binding(identity)


def test_correct_fingerprint_cannot_mask_an_invalid_summary_descriptor() -> None:
    core = make_core()
    identity = _low_level_identity(_summary_descriptor("e" * 64, 1), core)
    # The record's fingerprint is genuinely correct for this identity...
    record = SplitFingerprintRecord(
        identity=identity, split_fingerprint=compute_split_fingerprint(identity)
    )
    # ...and verification must still fail, because the binding is wrong.
    with pytest.raises(InvalidSha256Error):
        verify_split_fingerprint_record(record)


def test_low_level_size_only_mismatch_is_rejected_at_verification() -> None:
    core = make_core()
    identity = _low_level_identity(
        _summary_descriptor(GOLDEN_CORE_SHA256, len(core.canonical_bytes()) + 3), core
    )
    record = SplitFingerprintRecord(
        identity=identity, split_fingerprint=compute_split_fingerprint(identity)
    )
    with pytest.raises(InvalidByteSizeError):
        verify_split_fingerprint_record(record)


def test_verification_accepts_a_matching_record() -> None:
    verify_split_fingerprint_record(build_split_fingerprint_record(make_identity()))


def test_verification_rejects_a_tampered_fingerprint() -> None:
    record = SplitFingerprintRecord(identity=make_identity(), split_fingerprint=VALID_SHA256)
    with pytest.raises(FingerprintMismatchError) as excinfo:
        verify_split_fingerprint_record(record)
    assert excinfo.value.code == "fingerprint_mismatch"


def test_record_rejects_a_malformed_fingerprint() -> None:
    with pytest.raises(InvalidSha256Error):
        SplitFingerprintRecord(identity=make_identity(), split_fingerprint="abc")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("policy_id", "mesc-pilot-01-split-policy/2"),
        ("algorithm_version", "mesc-pilot-01-split-algorithm/2"),
        ("split_seed", "mesc-pilot-01-split-v2"),
        ("group_registry_payload", b'{"groups":[1]}\n'),
        ("example_registry_payload", b'{"examples":[1]}\n'),
        ("excluded_ledger_payload", b'{"excluded":[1]}\n'),
    ],
)
def test_changing_any_bound_input_changes_the_fingerprint(field: str, value: object) -> None:
    assert compute_split_fingerprint(make_identity(**{field: value})) != GOLDEN_SPLIT_FINGERPRINT


def test_changing_the_identity_core_changes_the_fingerprint() -> None:
    altered = make_identity(split_summary_identity_core=make_core(total_example_count=7))
    assert compute_split_fingerprint(altered) != GOLDEN_SPLIT_FINGERPRINT


def test_unbound_environment_cannot_change_the_fingerprint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name, value in (
        ("TZ", "Pacific/Kiritimati"),
        ("LC_ALL", "tr_TR.UTF-8"),
        ("LANG", "de_DE.UTF-8"),
        ("HOSTNAME", "another-host"),
        ("USERNAME", "another-user"),
        ("PYTHONHASHSEED", "12345"),
    ):
        monkeypatch.setenv(name, value)
    assert compute_split_fingerprint(make_identity()) == GOLDEN_SPLIT_FINGERPRINT


def test_fingerprint_is_stable_across_repeated_runs() -> None:
    assert len({compute_split_fingerprint(make_identity()) for _ in range(32)}) == 1


def test_identity_rejects_a_wrong_bundle_schema() -> None:
    with pytest.raises(InvalidSchemaVersionError):
        SplitFingerprintIdentity(
            bundle_schema_version="mesc-pilot-01-split-fingerprint-bundle/2",
            policy_id="p",
            algorithm_version="a",
            split_seed="s",
            artifact_descriptors=make_descriptors(),
            split_summary_identity_core=make_core(),
        )


@pytest.mark.parametrize("field", ["policy_id", "algorithm_version", "split_seed"])
def test_identity_rejects_empty_identity_strings(field: str) -> None:
    fields: dict[str, Any] = {
        "bundle_schema_version": BUNDLE_SCHEMA_VERSION,
        "policy_id": "p",
        "algorithm_version": "a",
        "split_seed": "s",
        "artifact_descriptors": make_descriptors(),
        "split_summary_identity_core": make_core(),
        field: "",
    }
    with pytest.raises(UnsupportedValueTypeError):
        SplitFingerprintIdentity(**fields)


# --------------------------------------------------------------------------
# B1 boundary
# --------------------------------------------------------------------------


def test_b1_constants_may_be_read_without_touching_b1() -> None:
    from medscale.mesc import _split_v1

    identity = make_identity(
        algorithm_version=_split_v1.ALGORITHM_VERSION,
        split_seed=_split_v1.SPLIT_SEED,
    )
    # The ratified fixture uses exactly the B1 constants, so reading them
    # reproduces the golden fingerprint.
    assert compute_split_fingerprint(identity) == GOLDEN_SPLIT_FINGERPRINT


def test_b1_short_split_hash_is_never_authoritative() -> None:
    from medscale.mesc import _split_v1

    b1_short = _split_v1.sha256_hexdigest({"a": 1})[:16]
    fingerprint = compute_split_fingerprint(make_identity())
    assert len(b1_short) == 16
    assert fingerprint != b1_short
    assert not fingerprint.startswith(b1_short)
    assert len(fingerprint) == 64


def test_b2a_does_not_reuse_the_b1_serializer() -> None:
    import ast

    from medscale.mesc import _canonical_json_v1, _split_artifacts_v1

    # The prohibition is on importing B1, not on naming it in prose: the module
    # docstring explains precisely why B1 must not be reused.
    for module in (_canonical_json_v1, _split_artifacts_v1):
        source = Path(module.__file__ or "").read_text(encoding="utf-8")
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert "_split_v1" not in node.module
            if isinstance(node, ast.Import):
                assert all("_split_v1" not in alias.name for alias in node.names)


def test_b1_behavior_is_unchanged() -> None:
    from medscale.mesc import _split_v1

    assert _split_v1.ALGORITHM_VERSION == "mesc-pilot-01-split-algorithm/1"
    assert _split_v1.SPLIT_SEED == "mesc-pilot-01-split-v1"
    assert _split_v1.canonical_json_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}'
    assert not _split_v1.canonical_json_bytes({"a": 1}).endswith(b"\n")


# --------------------------------------------------------------------------
# Boundary: no exports, no side effects
# --------------------------------------------------------------------------


def test_new_symbols_are_absent_from_the_public_facade() -> None:
    import medscale.mesc as mesc

    for name in (
        "SplitArtifactDescriptor",
        "SplitFingerprintIdentity",
        "SplitFingerprintRecord",
        "SplitSummaryIdentityCore",
        "ARTIFACT_SCHEMA_VERSIONS",
        "REQUIRED_ARTIFACT_ROLES",
        "BUNDLE_SCHEMA_VERSION",
        "compute_split_fingerprint",
        "build_split_fingerprint_record",
        "descriptor_for_bytes",
    ):
        assert name not in mesc.__all__
        assert not hasattr(mesc, name)


def test_facade_all_is_exactly_the_pre_existing_surface() -> None:
    import medscale.mesc as mesc

    assert set(mesc.__all__) == {
        "SCHEMA_VERSION",
        "PilotClaim",
        "PilotEvaluationReport",
        "PilotEvaluationResult",
        "PilotEvidence",
        "PilotLeakageAuditReport",
        "PilotMetricValue",
        "PilotProvenance",
        "PilotRecord",
        "PilotRunManifest",
        "PilotSourceIdentity",
        "PilotSplitAssignment",
        "PilotSplitManifest",
        "PilotSplitNotAuthorizedError",
        "PilotTarget",
        "SourceDocumentGroupedSplitter",
        "pilot_abstention_precision_recall",
        "pilot_aggregate_counts",
        "pilot_decision_accuracy",
        "pilot_evidence_reference_validity",
        "pilot_macro_f1",
        "pilot_supported_claim_metrics",
        "pilot_valid_json_rate",
    }


def test_all_errors_share_the_private_contract_base() -> None:
    for error in (
        DuplicateArtifactRoleError,
        MissingArtifactRoleError,
        UnknownArtifactRoleError,
        InvalidSha256Error,
        InvalidByteSizeError,
        InvalidSchemaVersionError,
        ForbiddenRuntimeMetadataError,
        ForbiddenDateOrTimestampError,
        FingerprintMismatchError,
    ):
        assert issubclass(error, CanonicalContractError)
        # CLI exit-code semantics are not reused inside the library.
        assert not issubclass(error, SystemExit)
        assert not hasattr(error, "exit_code")


def test_taxonomy_codes_are_exactly_the_ratified_thirteen() -> None:
    from medscale.mesc import _canonical_json_v1 as cj
    from medscale.mesc import _split_artifacts_v1 as sa

    codes = set()
    for module in (cj, sa):
        for value in vars(module).values():
            if (
                isinstance(value, type)
                and issubclass(value, CanonicalContractError)
                and value is not CanonicalContractError
            ):
                codes.add(value.code)
    assert codes == {
        "unsupported_value_type",
        "floating_point_value_prohibited",
        "non_string_object_key",
        "duplicate_artifact_role",
        "missing_artifact_role",
        "unknown_artifact_role",
        "invalid_sha256",
        "invalid_byte_size",
        "invalid_schema_version",
        "forbidden_runtime_metadata",
        "forbidden_date_or_timestamp",
        "fingerprint_mismatch",
        "canonicalization_failure",
    }


def test_no_filesystem_or_network_access(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("B2A artifact construction must have no side effects")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(os, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_bytes", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_text", forbidden)
    monkeypatch.setattr(pathlib.Path, "mkdir", forbidden)
    monkeypatch.setattr(os, "replace", forbidden)
    monkeypatch.setattr(os, "rename", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)

    identity = make_identity()
    record = build_split_fingerprint_record(identity)
    verify_split_fingerprint_record(record)
    assert record.split_fingerprint == GOLDEN_SPLIT_FINGERPRINT


def test_no_files_are_created(tmp_path: Path) -> None:
    before = set(tmp_path.iterdir())
    build_split_fingerprint_record(make_identity())
    assert set(tmp_path.iterdir()) == before


def test_artifact_module_imports_no_data_or_model_dependency() -> None:
    import ast

    from medscale.mesc import _split_artifacts_v1

    source = Path(_split_artifacts_v1.__file__ or "").read_text(encoding="utf-8")
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported.add(node.module.split(".")[0])
    assert imported <= {
        "__future__",
        "collections",
        "dataclasses",
        "types",
        "typing",
        "medscale",
    }
    for forbidden in ("torch", "transformers", "datasets", "pandas", "numpy", "requests", "httpx"):
        assert forbidden not in imported
