"""Synthetic in-memory tests for the private P01-04B2C fixture split facade.

Every fixture here is synthetic identity data built inside the test module.  No
dataset is read, no path is opened, no network or subprocess is used, and none
of these values is real evidence or a real split artifact.  The two fixtures are
deliberately unnamed with respect to P01-04B2D: its three 1,000-row fixtures are
neither implemented nor qualified here.

The golden vectors below are literal bytes and literal digests.  They are frozen
so that any change to the canonical serialization, the member sets, the ordering
rules or the identity payloads breaks a test rather than silently changing an
authoritative value.
"""

from __future__ import annotations

import builtins
import dataclasses
import os
import random
import socket
import subprocess
import time
import types
from pathlib import Path
from typing import Any

import pytest

from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes
from medscale.mesc._fixture_split_v1 import (
    EXAMPLE_REGISTRY_SCHEMA,
    EXCLUDED_LEDGER_SCHEMA,
    FIXTURE_NAMESPACE_PREFIX,
    GROUP_REGISTRY_SCHEMA,
    REQUEST_ID_PREFIX,
    SPLIT_SUMMARY_SCHEMA,
    FixtureFacadeContractError,
    FixtureIdentityMismatchError,
    FixtureOnlyModeError,
    FixtureSplitFacade,
    FixtureSplitRequest,
    FixtureSplitResult,
    InvalidExecutionEvidenceReferenceError,
    InvalidFixtureRequestError,
    _fixture_identity_document,
    _group_id,
    _request_identity_document,
)
from medscale.mesc._leakage_v1 import (
    InvalidReportInvariantError,
    LeakageAuditReport,
    LeakageFinding,
)
from medscale.mesc._split_artifacts_v1 import (
    ARTIFACT_SCHEMA_VERSIONS,
    FingerprintMismatchError,
    InvalidSha256Error,
    SplitFingerprintRecord,
    SplitSummaryIdentityCore,
    verify_descriptor_against_bytes,
    verify_split_fingerprint_record,
)
from medscale.mesc._split_v1 import (
    DECISIONS,
    SPLIT_SEED,
    OrderedExampleRow,
    SourceLabelRow,
    allocate_indivisible_groups,
    constrained_apportionment,
    join_labels,
)
from medscale.mesc.split import (
    PilotSplitManifest,
    PilotSplitNotAuthorizedError,
    SourceDocumentGroupedSplitter,
)

# ---------------------------------------------------------------------------
# Synthetic fixture inputs
# ---------------------------------------------------------------------------

DATASET_ID = "mesc-fixture-dataset"
DATASET_REVISION = "fixture-revision-1"
CONFIGURATION = "fixture-configuration"
TRANSFORMATION_VERSION = "mesc-fixture-transformation/1"
POLICY_ID = "mesc-fixture-policy/1"
EXECUTION_EVIDENCE_REF = "mesc-fixture-evidence/1:unit"
SYNTHETIC_PROOF = "mesc-synthetic-batch/1:sha256:" + "a1b2c3d4" * 8
DETECTION_METHODS = ("exact_example_identity", "exact_question_equality")

GOLDEN_FIXTURE_ID = "b2c-unit-fixture-a"
GROUPED_FIXTURE_ID = "b2c-unit-fixture-b"

#: One example per decision, one source document per example, one place per partition.
GOLDEN_SPEC: tuple[tuple[int, int, str], ...] = ((0, 0, "yes"), (1, 1, "no"), (2, 2, "maybe"))
GOLDEN_TOTALS = {"train": 1, "validation": 1, "test": 1}

#: Three indivisible two-example source-document groups, one per partition.
GROUPED_SPEC: tuple[tuple[int, int, str], ...] = tuple(
    (index, index // 2, "yes") for index in range(6)
)
GROUPED_TOTALS = {"train": 2, "validation": 2, "test": 2}

FALSE_POSITIVE_FINDING = LeakageFinding.create(
    finding_type="exact_question",
    example_ids=("fixture-finding-left", "fixture-finding-right"),
    source_document_ids=("fixture-document-00",),
    partitions=("train",),
    score_representation="none",
    classification="false_positive",
    shared_surface=("question_bytes",),
    evidence_reference="mesc-fixture-evidence/1:finding-a",
)

UNRESOLVED_FINDING = LeakageFinding.create(
    finding_type="source_document",
    example_ids=("fixture-finding-third",),
    source_document_ids=("fixture-document-01",),
    partitions=("test",),
    score_representation="none",
    classification="unresolved",
    shared_surface=("source_document_id",),
)

# ---------------------------------------------------------------------------
# Frozen golden vectors
# ---------------------------------------------------------------------------

GOLDEN_FIXTURE_SHA256 = "6e2853f855f1a580a090ab4ba786c693f7aae5632e2078c54ded1dcbc72d45c3"
GOLDEN_REQUEST_ID = (
    "mesc-pilot-01-fixture-request/1:sha256:"
    "9231371a415e5951c339986a6e45aef8e10dbed97f4f0172e35ce608f056a1e9"
)
GOLDEN_SPLIT_HASH = "c96d44a7feec6db4"
GOLDEN_FINGERPRINT = "5732f573feb1ef9c442010c6640864b78359f1b3c4643cc0d3cb3a6517dafa80"
GOLDEN_TRAIN_GROUP_ID = (
    "mesc-pilot-01-group/1:sha256:a5287ac51bf31b5c237baf694a33301f684967facd046ac437f4402f663630d8"
)

GOLDEN_GROUP_REGISTRY = (
    b'{"assigned_split":"test","example_count":1,"group_id":"mesc-pilot-01-group/1:sha256:'
    b'23f62fb77d298c2d2546815d950c6e1a4dfd81cbf514763edf17a90236910134","partition_key":"'
    b'd1c9f00989fbe4f545954cbb702aa1ce9a38ca30b2b2225375e8f3f17c6eef4a","row_ordinals":[0]'
    b',"schema_version":"mesc-pilot-01-group-registry/1","source_document_id":'
    b'"fixture-document-00"}\n'
    b'{"assigned_split":"train","example_count":1,"group_id":"mesc-pilot-01-group/1:sha256:'
    b'a5287ac51bf31b5c237baf694a33301f684967facd046ac437f4402f663630d8","partition_key":"'
    b'02836bfb7b037c9b97aadee6e7c41bedf113050b9fe8f315a76d62bf413a69cc","row_ordinals":[2]'
    b',"schema_version":"mesc-pilot-01-group-registry/1","source_document_id":'
    b'"fixture-document-02"}\n'
    b'{"assigned_split":"validation","example_count":1,"group_id":"mesc-pilot-01-group/1:'
    b'sha256:9b88ca6c354de5a83da483cb5b4b4ea91a3ded4032ee2e429960a883dc1bcdbe",'
    b'"partition_key":"ab2bbbb0ffc9f4e6c4d67bd845da12aa5df186666763c62479686d9db05fe2f6",'
    b'"row_ordinals":[1],"schema_version":"mesc-pilot-01-group-registry/1",'
    b'"source_document_id":"fixture-document-01"}\n'
)

GOLDEN_EXAMPLE_REGISTRY = (
    b'{"assigned_split":"test","example_id":"mesc-pilot-01:'
    b'195d9a1f0f6466c72c984a44ddefcc4f6963442b5ff93e97c3717b8e454efe28","partition_key":"'
    b'd1c9f00989fbe4f545954cbb702aa1ce9a38ca30b2b2225375e8f3f17c6eef4a","row_ordinal":0,'
    b'"schema_version":"mesc-pilot-01-example-registry/1","source_document_id":'
    b'"fixture-document-00"}\n'
    b'{"assigned_split":"train","example_id":"mesc-pilot-01:'
    b'156967c5e4b9a59003693d3ce00ac7443da5d6d695eb6529c2544bbc232f6f0e","partition_key":"'
    b'02836bfb7b037c9b97aadee6e7c41bedf113050b9fe8f315a76d62bf413a69cc","row_ordinal":2,'
    b'"schema_version":"mesc-pilot-01-example-registry/1","source_document_id":'
    b'"fixture-document-02"}\n'
    b'{"assigned_split":"validation","example_id":"mesc-pilot-01:'
    b'960f41490a9455616e6fc80ce9a50037821677f1adac4fc4a20e68e8fa7d3470","partition_key":"'
    b'ab2bbbb0ffc9f4e6c4d67bd845da12aa5df186666763c62479686d9db05fe2f6","row_ordinal":1,'
    b'"schema_version":"mesc-pilot-01-example-registry/1","source_document_id":'
    b'"fixture-document-01"}\n'
)

GOLDEN_EXCLUDED_LEDGER = (
    b'{"count":0,"excluded_ids":[],"reason":"none",'
    b'"schema_version":"mesc-pilot-01-excluded-ledger/1"}\n'
)

GOLDEN_CORE_BYTES = (
    b'{"algorithm_version":"mesc-pilot-01-split-algorithm/1","excluded_record_count":0,'
    b'"group_counts_by_partition":{"test":1,"train":1,"validation":1},'
    b'"label_totals":{"maybe":1,"no":1,"yes":1},'
    b'"partition_label_matrix":{"test":{"maybe":0,"no":0,"yes":1},'
    b'"train":{"maybe":1,"no":0,"yes":0},"validation":{"maybe":0,"no":1,"yes":0}},'
    b'"partition_totals":{"test":1,"train":1,"validation":1},'
    b'"schema_version":"mesc-pilot-01-split-summary-identity-core/1",'
    b'"total_example_count":3,"total_group_count":3}\n'
)

GOLDEN_SUMMARY_BYTES = (
    b'{"algorithm_version":"mesc-pilot-01-split-algorithm/1","excluded_record_count":0,'
    b'"group_counts_by_partition":{"test":1,"train":1,"validation":1},'
    b'"label_totals":{"maybe":1,"no":1,"yes":1},'
    b'"partition_label_matrix":{"test":{"maybe":0,"no":0,"yes":1},'
    b'"train":{"maybe":1,"no":0,"yes":0},"validation":{"maybe":0,"no":1,"yes":0}},'
    b'"partition_totals":{"test":1,"train":1,"validation":1},'
    b'"schema_version":"mesc-pilot-01-split-summary/1",'
    b'"split_fingerprint":"5732f573feb1ef9c442010c6640864b78359f1b3c4643cc0d3cb3a6517dafa80",'
    b'"split_hash":"c96d44a7feec6db4","total_example_count":3,"total_group_count":3}\n'
)

GOLDEN_AUDIT_BYTES = (
    b'{"detection_methods":["exact_example_identity","exact_question_equality"],'
    b'"finding_count":1,"findings":[{"classification":"false_positive",'
    b'"evidence_reference":"mesc-fixture-evidence/1:finding-a",'
    b'"example_ids":["fixture-finding-left","fixture-finding-right"],'
    b'"finding_id":"mesc-pilot-01-leakage-finding/1:sha256:'
    b'ba9b0bf4707010c0c74730eaa1fdd3a0aa1bc5d79d3614c739a8c40c35154d4e",'
    b'"finding_type":"exact_question","partitions":["train"],'
    b'"schema":"mesc-pilot-01-leakage-finding/1","score_representation":"none",'
    b'"shared_surface":["question_bytes"],"source_document_ids":["fixture-document-00"],'
    b'"suppressed":false}],"leaked":false,"normalization_record":'
    b'{"case_folding":"unicode_case_folding","unicode_normalization":"NFKC",'
    b'"whitespace_collapse":"unicode_whitespace_runs_to_single_ascii_space",'
    b'"whitespace_trim":"strip_leading_and_trailing_whitespace"}}\n'
)

GROUPED_FIXTURE_SHA256 = "1e86875e64a079cc99f0e839d3e4e72a2114d294312f545015ce1cdaa0fac226"
GROUPED_REQUEST_ID = (
    "mesc-pilot-01-fixture-request/1:sha256:"
    "fb7b233284248712735da0df7cec8b44b1207311b5bc144166cf4f322eb6319d"
)
GROUPED_SPLIT_HASH = "f01fe527cfb241b0"
GROUPED_FINGERPRINT = "3a9e2fe1cd8acfe96b7788fd005cfc486c1dd0c38b4357fac0a49bdab1f2bebf"

# ---------------------------------------------------------------------------
# Fixture construction helpers
# ---------------------------------------------------------------------------


def _ordered_rows(spec: tuple[tuple[int, int, str], ...]) -> tuple[OrderedExampleRow, ...]:
    return tuple(
        OrderedExampleRow(
            original_example_id=f"fixture-example-{index:02d}",
            row_ordinal=index,
            source_document_id=f"fixture-document-{document:02d}",
        )
        for index, document, _ in spec
    )


def _source_labels(spec: tuple[tuple[int, int, str], ...]) -> tuple[SourceLabelRow, ...]:
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
        for index, document, decision in spec
    )


def _golden_kwargs() -> dict[str, Any]:
    """Return the exact keyword arguments of the valid golden request."""
    return {
        "fixture_schema_version": "1",
        "fixture_namespace": FIXTURE_NAMESPACE_PREFIX + GOLDEN_FIXTURE_ID,
        "fixture_id": GOLDEN_FIXTURE_ID,
        "fixture_sha256": GOLDEN_FIXTURE_SHA256,
        "fixture_only": True,
        "non_evidence": True,
        "synthetic_identity_proof": SYNTHETIC_PROOF,
        "request_id": GOLDEN_REQUEST_ID,
        "seed": SPLIT_SEED,
        "policy_id": POLICY_ID,
        "transformation_version": TRANSFORMATION_VERSION,
        "ordered_rows": _ordered_rows(GOLDEN_SPEC),
        "source_labels": _source_labels(GOLDEN_SPEC),
        "partition_totals": dict(GOLDEN_TOTALS),
        "leakage_findings": (FALSE_POSITIVE_FINDING,),
        "detection_methods": DETECTION_METHODS,
        "execution_evidence_ref": EXECUTION_EVIDENCE_REF,
    }


def _grouped_kwargs() -> dict[str, Any]:
    """Return the request arguments of the indivisible two-example-group fixture."""
    return {
        **_golden_kwargs(),
        "fixture_namespace": FIXTURE_NAMESPACE_PREFIX + GROUPED_FIXTURE_ID,
        "fixture_id": GROUPED_FIXTURE_ID,
        "fixture_sha256": GROUPED_FIXTURE_SHA256,
        "request_id": GROUPED_REQUEST_ID,
        "ordered_rows": _ordered_rows(GROUPED_SPEC),
        "source_labels": _source_labels(GROUPED_SPEC),
        "partition_totals": dict(GROUPED_TOTALS),
        "leakage_findings": (),
    }


def _zero_totals(keys: tuple[str, ...]) -> dict[str, int]:
    """Return a complete zero-valued mapping with plain ``str`` keys."""
    totals: dict[str, int] = {}
    for key in keys:
        totals[key] = 0
    return totals


def _request(**overrides: Any) -> FixtureSplitRequest:
    return FixtureSplitRequest(**{**_golden_kwargs(), **overrides})


def _identity_completed_request(**overrides: Any) -> FixtureSplitRequest:
    """Return a request whose two identity values are regenerated for its own payload.

    The frozen golden vectors elsewhere in this module prove the digests never
    drift.  This helper exists only so a test can reach a *later* validation step
    with a genuinely well-formed identity, which is the only way to observe that
    a B1 or B2B typed error propagates as itself.
    """
    skeleton = _request(**overrides)
    digest = sha256_of_bytes(canonical_json_bytes(_fixture_identity_document(skeleton)))
    request_id = REQUEST_ID_PREFIX + sha256_of_bytes(
        canonical_json_bytes(_request_identity_document(skeleton, digest))
    )
    return _request(**{**overrides, "fixture_sha256": digest, "request_id": request_id})


def _grouped_request(**overrides: Any) -> FixtureSplitRequest:
    return FixtureSplitRequest(**{**_grouped_kwargs(), **overrides})


@pytest.fixture
def golden_result() -> FixtureSplitResult:
    return FixtureSplitFacade.run(_request())


@pytest.fixture
def grouped_result() -> FixtureSplitResult:
    return FixtureSplitFacade.run(_grouped_request())


# ---------------------------------------------------------------------------
# 15.1 Request boundary
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "candidate",
    [
        {"fixture_id": GOLDEN_FIXTURE_ID},
        [1, 2, 3],
        "mesc-fixture/p01-04b2/1/b2c-unit-fixture-a",
        None,
        42,
    ],
)
def test_run_requires_the_exact_request_type(candidate: object) -> None:
    """No mapping, sequence, string, path-like or duck-typed substitute is coerced."""
    with pytest.raises(InvalidFixtureRequestError):
        FixtureSplitFacade.run(candidate)  # type: ignore[arg-type]


def test_run_rejects_a_duck_typed_request() -> None:
    duck = types.SimpleNamespace(**_golden_kwargs())
    with pytest.raises(InvalidFixtureRequestError):
        FixtureSplitFacade.run(duck)  # type: ignore[arg-type]


def test_request_is_frozen_and_slotted() -> None:
    request = _request()
    with pytest.raises(dataclasses.FrozenInstanceError):
        request.policy_id = "other"  # type: ignore[misc]
    assert not hasattr(request, "__dict__")


def test_request_has_exactly_the_seventeen_authorized_fields() -> None:
    assert tuple(field.name for field in dataclasses.fields(FixtureSplitRequest)) == (
        "fixture_schema_version",
        "fixture_namespace",
        "fixture_id",
        "fixture_sha256",
        "fixture_only",
        "non_evidence",
        "synthetic_identity_proof",
        "request_id",
        "seed",
        "policy_id",
        "transformation_version",
        "ordered_rows",
        "source_labels",
        "partition_totals",
        "leakage_findings",
        "detection_methods",
        "execution_evidence_ref",
    )


def test_no_request_field_can_carry_raw_text() -> None:
    """Payload ownership is identity-only: no field exists that could hold text."""
    names = {field.name for field in dataclasses.fields(FixtureSplitRequest)}
    for forbidden in ("question", "context", "answer", "text", "body", "prompt"):
        assert not any(forbidden in name for name in names)


@pytest.mark.parametrize("marker", ["fixture_only", "non_evidence"])
def test_false_marker_is_rejected(marker: str) -> None:
    with pytest.raises(FixtureOnlyModeError):
        _request(**{marker: False})


@pytest.mark.parametrize("marker", ["fixture_only", "non_evidence"])
def test_non_bool_marker_is_rejected(marker: str) -> None:
    with pytest.raises(FixtureOnlyModeError):
        _request(**{marker: 1})


def test_invalid_schema_version_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(fixture_schema_version="2")


def test_str_subclass_schema_version_is_rejected() -> None:
    class SchemaVersion(str):
        pass

    with pytest.raises(InvalidFixtureRequestError):
        _request(fixture_schema_version=SchemaVersion("1"))


@pytest.mark.parametrize(
    "fixture_id", ["", "-leading", "trailing-", "Upper", "under_score", "dot.ted", "sp ace"]
)
def test_malformed_fixture_id_is_rejected(fixture_id: str) -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(
            fixture_id=fixture_id,
            fixture_namespace=FIXTURE_NAMESPACE_PREFIX + fixture_id,
        )


def test_namespace_mismatch_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(fixture_namespace="mesc-fixture/p01-04b2/1/other-fixture")


@pytest.mark.parametrize(
    "digest", ["", "a" * 63, "a" * 65, "A" * 64, "g" * 64, "0123456789ABCDEF" * 4]
)
def test_malformed_fixture_digest_is_rejected(digest: str) -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(fixture_sha256=digest)


def test_fixture_digest_mismatch_is_rejected() -> None:
    """A well-formed but wrong digest fails at identity regeneration, not construction."""
    request = _request(fixture_sha256="b" * 64)
    with pytest.raises(FixtureIdentityMismatchError):
        FixtureSplitFacade.run(request)


def test_request_id_mismatch_is_rejected() -> None:
    request = _request(request_id=REQUEST_ID_PREFIX + "c" * 64)
    with pytest.raises(FixtureIdentityMismatchError):
        FixtureSplitFacade.run(request)


def test_malformed_request_id_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(request_id="not-a-request-id")


def test_malformed_synthetic_proof_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(synthetic_identity_proof="mesc-synthetic-batch/1:sha256:short")


def test_wrong_seed_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(seed="mesc-pilot-01")


@pytest.mark.parametrize(
    "reference",
    ["", " padded", "padded ", "/abs/path", "./rel", "../up", "~/home", "C:/drive", "a\\b"],
)
def test_path_shaped_evidence_reference_is_rejected(reference: str) -> None:
    with pytest.raises(InvalidExecutionEvidenceReferenceError):
        _request(execution_evidence_ref=reference)


@pytest.mark.parametrize("value", ["/abs/path", "./rel", "../up", "~/home", "C:/drive", "a\\b"])
def test_path_shaped_policy_id_is_rejected(value: str) -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(policy_id=value)


@pytest.mark.parametrize(
    "totals",
    [
        {"train": 1, "validation": 1},
        {"train": 1, "validation": 1, "test": 1, "holdout": 0},
        {"train": 1, "validation": 1, "holdout": 1},
    ],
)
def test_wrong_partition_keys_are_rejected(totals: dict[str, int]) -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(partition_totals=totals)


def test_partition_total_sum_mismatch_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(partition_totals={"train": 2, "validation": 1, "test": 1})


def test_boolean_partition_total_is_rejected() -> None:
    """``bool`` is an ``int`` subclass and must never satisfy a count invariant."""
    with pytest.raises(InvalidFixtureRequestError):
        _request(partition_totals={"train": True, "validation": 1, "test": 1})


def test_negative_partition_total_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(partition_totals={"train": -1, "validation": 2, "test": 2})


def test_non_mapping_partition_totals_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(partition_totals=[("train", 1), ("validation", 1), ("test", 1)])


def test_partition_totals_are_snapshotted_against_later_mutation() -> None:
    totals = dict(GOLDEN_TOTALS)
    request = _request(partition_totals=totals)
    totals["train"] = 99
    assert dict(request.partition_totals) == GOLDEN_TOTALS
    with pytest.raises(TypeError):
        request.partition_totals["train"] = 99  # type: ignore[index]


@pytest.mark.parametrize("field", ["ordered_rows", "source_labels", "leakage_findings"])
def test_list_substitutes_are_rejected(field: str) -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(**{field: list(_golden_kwargs()[field])})


def test_detection_methods_list_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(detection_methods=list(DETECTION_METHODS))


def test_wrong_row_element_type_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(ordered_rows=(_source_labels(GOLDEN_SPEC)[0],))


def test_empty_ordered_rows_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(ordered_rows=(), partition_totals={"train": 0, "validation": 0, "test": 0})


def test_duplicate_example_identity_is_rejected() -> None:
    rows = _ordered_rows(GOLDEN_SPEC)
    duplicated = (*rows, dataclasses.replace(rows[0], row_ordinal=9))
    with pytest.raises(InvalidFixtureRequestError):
        _request(
            ordered_rows=duplicated,
            partition_totals={"train": 2, "validation": 1, "test": 1},
        )


def test_duplicate_row_ordinal_is_rejected() -> None:
    rows = _ordered_rows(GOLDEN_SPEC)
    duplicated = (*rows, dataclasses.replace(rows[0], original_example_id="fixture-example-09"))
    with pytest.raises(InvalidFixtureRequestError):
        _request(
            ordered_rows=duplicated,
            partition_totals={"train": 2, "validation": 1, "test": 1},
        )


def test_duplicate_source_label_identity_is_rejected() -> None:
    labels = _source_labels(GOLDEN_SPEC)
    duplicated = (*labels, dataclasses.replace(labels[0], source_record_hash="9" * 64))
    with pytest.raises(InvalidFixtureRequestError):
        _request(source_labels=duplicated)


def test_duplicate_finding_identity_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(leakage_findings=(FALSE_POSITIVE_FINDING, FALSE_POSITIVE_FINDING))


def test_duplicate_detection_method_is_rejected() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(detection_methods=("tokenize", "tokenize"))


def test_duplicates_are_never_silently_deduplicated() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(detection_methods=(*DETECTION_METHODS, DETECTION_METHODS[0]))


# ---------------------------------------------------------------------------
# Validation precedence — the earliest applicable rule always controls
# ---------------------------------------------------------------------------


def test_marker_step_precedes_namespace_and_path_steps() -> None:
    with pytest.raises(FixtureOnlyModeError):
        _request(
            fixture_only=False,
            fixture_namespace="wrong",
            fixture_schema_version="2",
            execution_evidence_ref="/abs/path",
        )


def test_schema_step_precedes_primitive_step() -> None:
    with pytest.raises(InvalidFixtureRequestError):
        _request(fixture_schema_version="2", fixture_sha256="not-hex")


def test_path_step_precedes_duplicate_step() -> None:
    with pytest.raises(InvalidExecutionEvidenceReferenceError):
        _request(
            execution_evidence_ref="/abs/path",
            detection_methods=("tokenize", "tokenize"),
        )


def test_request_steps_precede_identity_steps() -> None:
    with pytest.raises(FixtureOnlyModeError):
        _request(fixture_only=False, fixture_sha256="d" * 64)


def test_error_codes_are_stable() -> None:
    assert FixtureFacadeContractError.code == "fixture_facade_contract_error"
    assert FixtureOnlyModeError.code == "fixture_only_mode_error"
    assert InvalidFixtureRequestError.code == "invalid_fixture_request"
    assert FixtureIdentityMismatchError.code == "fixture_identity_mismatch"
    assert InvalidExecutionEvidenceReferenceError.code == "invalid_execution_evidence_reference"


def test_every_facade_error_descends_from_the_private_base() -> None:
    for error in (
        FixtureOnlyModeError,
        InvalidFixtureRequestError,
        FixtureIdentityMismatchError,
        InvalidExecutionEvidenceReferenceError,
    ):
        assert issubclass(error, FixtureFacadeContractError)


def test_error_messages_carry_no_environment_or_path_detail() -> None:
    with pytest.raises(InvalidExecutionEvidenceReferenceError) as caught:
        _request(execution_evidence_ref="/abs/secret/path")
    message = str(caught.value)
    assert "/abs/secret/path" not in message
    assert str(Path.cwd()) not in message


# ---------------------------------------------------------------------------
# Identity documents — exact members and non-circularity
# ---------------------------------------------------------------------------


def test_fixture_identity_document_has_exactly_sixteen_members() -> None:
    document = _fixture_identity_document(_request())
    assert len(document) == 16
    assert set(document) == {
        "schema",
        "fixture_schema_version",
        "fixture_namespace",
        "fixture_id",
        "fixture_only",
        "non_evidence",
        "synthetic_identity_proof",
        "seed",
        "policy_id",
        "transformation_version",
        "ordered_rows",
        "source_labels",
        "partition_totals",
        "leakage_finding_documents",
        "detection_methods",
        "execution_evidence_ref",
    }


def test_fixture_identity_is_non_circular() -> None:
    document = _fixture_identity_document(_request())
    assert "fixture_sha256" not in document
    assert "request_id" not in document
    assert GOLDEN_FIXTURE_SHA256.encode() not in canonical_json_bytes(document)
    assert GOLDEN_REQUEST_ID.encode() not in canonical_json_bytes(document)


def test_fixture_digest_matches_its_golden_vector() -> None:
    document = _fixture_identity_document(_request())
    assert sha256_of_bytes(canonical_json_bytes(document)) == GOLDEN_FIXTURE_SHA256


def test_request_identity_document_has_exactly_four_members() -> None:
    document = _request_identity_document(_request(), GOLDEN_FIXTURE_SHA256)
    assert document == {
        "schema": "mesc-pilot-01-fixture-request-identity/1",
        "fixture_sha256": GOLDEN_FIXTURE_SHA256,
        "fixture_namespace": FIXTURE_NAMESPACE_PREFIX + GOLDEN_FIXTURE_ID,
        "request_id_domain": "p01-04b2c",
    }


def test_request_identity_is_non_circular_and_matches_its_golden_vector() -> None:
    document = _request_identity_document(_request(), GOLDEN_FIXTURE_SHA256)
    assert "request_id" not in document
    derived = REQUEST_ID_PREFIX + sha256_of_bytes(canonical_json_bytes(document))
    assert derived == GOLDEN_REQUEST_ID


def test_request_identity_binds_the_recomputed_fixture_digest() -> None:
    """A caller-supplied digest is never the value bound into the request identity."""
    document = _request_identity_document(_request(fixture_sha256="e" * 64), GOLDEN_FIXTURE_SHA256)
    assert document["fixture_sha256"] == GOLDEN_FIXTURE_SHA256


# ---------------------------------------------------------------------------
# 15.2 Deterministic integration
# ---------------------------------------------------------------------------


def test_same_semantic_request_produces_identical_bytes() -> None:
    first = FixtureSplitFacade.run(_request())
    second = FixtureSplitFacade.run(_request())
    assert first.group_registry_bytes == second.group_registry_bytes
    assert first.example_registry_bytes == second.example_registry_bytes
    assert first.excluded_ledger_bytes == second.excluded_ledger_bytes
    assert first.split_summary_identity_core_bytes == second.split_summary_identity_core_bytes
    assert first.split_summary_document_bytes == second.split_summary_document_bytes
    assert first.audit_report_bytes == second.audit_report_bytes
    assert (
        first.split_fingerprint_record.split_fingerprint
        == second.split_fingerprint_record.split_fingerprint
    )


def test_caller_row_and_label_order_is_not_semantic(golden_result: FixtureSplitResult) -> None:
    """Reversing the normalized collections changes no digest and no byte surface."""
    reversed_request = _request(
        ordered_rows=tuple(reversed(_ordered_rows(GOLDEN_SPEC))),
        source_labels=tuple(reversed(_source_labels(GOLDEN_SPEC))),
    )
    result = FixtureSplitFacade.run(reversed_request)
    assert result.group_registry_bytes == golden_result.group_registry_bytes
    assert result.example_registry_bytes == golden_result.example_registry_bytes
    assert (
        result.split_fingerprint_record.split_fingerprint
        == golden_result.split_fingerprint_record.split_fingerprint
    )


def test_detection_method_order_is_semantic() -> None:
    """Method order is declared semantic, so reordering must change the identity."""
    reordered = tuple(reversed(DETECTION_METHODS))
    with pytest.raises(FixtureIdentityMismatchError):
        FixtureSplitFacade.run(_request(detection_methods=reordered))
    regenerated = _identity_completed_request(detection_methods=reordered)
    assert regenerated.fixture_sha256 != GOLDEN_FIXTURE_SHA256


def test_facade_reuses_the_accepted_b1_pipeline(golden_result: FixtureSplitResult) -> None:
    request = _request()
    joined = join_labels(
        request.ordered_rows,
        request.source_labels,
        transformation_version=request.transformation_version,
    )
    label_totals = _zero_totals(DECISIONS)
    for example in joined:
        label_totals[example.decision] += 1
    targets = constrained_apportionment(label_totals, request.partition_totals)
    assignments = allocate_indivisible_groups(joined, targets)

    assert golden_result.split_summary_identity_core.total_example_count == len(joined)
    assert golden_result.split_summary_identity_core.total_group_count == len(assignments)
    assert {
        assignment.example_id for assignment in golden_result.split_manifest.split_assignments
    } == {example.example_id for example in joined}
    assert sum(target.train + target.validation + target.test for target in targets) == len(joined)


def test_example_ids_come_from_the_accepted_join(golden_result: FixtureSplitResult) -> None:
    """B2C never derives an example identifier; every one carries the B1 prefix."""
    for assignment in golden_result.split_manifest.split_assignments:
        assert assignment.example_id.startswith("mesc-pilot-01:")
        assert len(assignment.example_id) == len("mesc-pilot-01:") + 64


def test_every_example_is_assigned_exactly_once(golden_result: FixtureSplitResult) -> None:
    ids = [assignment.example_id for assignment in golden_result.split_manifest.split_assignments]
    assert len(ids) == len(set(ids)) == 3


def test_source_document_groups_remain_indivisible(grouped_result: FixtureSplitResult) -> None:
    """Every two-example source-document group lands wholly inside one partition."""
    partitions_by_document: dict[str, set[str]] = {}
    for assignment in grouped_result.split_manifest.split_assignments:
        partitions_by_document.setdefault(assignment.source_document_id, set()).add(
            assignment.split
        )
    assert len(partitions_by_document) == 3
    assert all(len(splits) == 1 for splits in partitions_by_document.values())
    assert grouped_result.split_summary_identity_core.total_group_count == 3


def test_b1_typed_error_propagates_as_itself() -> None:
    """A B1 contract failure stays attributable to B1, never a generic facade error."""
    from medscale.mesc._split_v1 import SplitInputError

    # One source document now carries two decision strata, which B1 refuses to group.
    crossing = tuple(
        dataclasses.replace(label, decision="no") if index == 0 else label
        for index, label in enumerate(_source_labels(GROUPED_SPEC))
    )
    request = _identity_completed_request(
        fixture_namespace=FIXTURE_NAMESPACE_PREFIX + GROUPED_FIXTURE_ID,
        fixture_id=GROUPED_FIXTURE_ID,
        ordered_rows=_ordered_rows(GROUPED_SPEC),
        source_labels=crossing,
        partition_totals=dict(GROUPED_TOTALS),
        leakage_findings=(),
    )
    with pytest.raises(SplitInputError) as caught:
        FixtureSplitFacade.run(request)
    assert not isinstance(caught.value, FixtureFacadeContractError)


def test_public_splitter_remains_fail_closed() -> None:
    """B2C introduces no path by which the public allocator can succeed."""
    splitter = SourceDocumentGroupedSplitter()
    with pytest.raises(PilotSplitNotAuthorizedError):
        splitter.assign(["a"], ["b"])


# ---------------------------------------------------------------------------
# 15.3 Compatibility manifest
# ---------------------------------------------------------------------------


def test_manifest_carries_one_assignment_per_example(grouped_result: FixtureSplitResult) -> None:
    assert len(grouped_result.split_manifest.split_assignments) == 6


def test_manifest_has_no_holdout(golden_result: FixtureSplitResult) -> None:
    assert golden_result.split_manifest.holdout_example_ids == ()
    assert all(
        assignment.split in {"train", "validation", "test"}
        for assignment in golden_result.split_manifest.split_assignments
    )


def test_manifest_uses_the_explicit_b1_seed(golden_result: FixtureSplitResult) -> None:
    """The class default is a different seed, so the B1 seed must be passed explicitly."""
    assert golden_result.split_manifest.split_seed == SPLIT_SEED
    assert PilotSplitManifest(split_assignments=()).split_seed != SPLIT_SEED


def test_manifest_split_hash_is_genuinely_computed(golden_result: FixtureSplitResult) -> None:
    """An empty ``split_hash`` is required for ``computed_split_hash`` to derive a value."""
    manifest = golden_result.split_manifest
    assert manifest.split_hash == ""
    assert manifest.computed_split_hash == GOLDEN_SPLIT_HASH
    assert len(manifest.computed_split_hash) == 16
    supplied = PilotSplitManifest(
        split_assignments=manifest.split_assignments,
        split_hash="supplied-value",
        split_seed=SPLIT_SEED,
    )
    assert supplied.computed_split_hash == "supplied-value"


def test_compatibility_hash_is_never_the_authoritative_identity(
    golden_result: FixtureSplitResult,
) -> None:
    fingerprint = golden_result.split_fingerprint_record.split_fingerprint
    assert fingerprint == GOLDEN_FINGERPRINT
    assert len(fingerprint) == 64
    assert golden_result.split_manifest.computed_split_hash != fingerprint
    assert golden_result.split_manifest.computed_split_hash != fingerprint[:16]


def test_manifest_order_is_canonical_partition_order_then_ordinal_then_id(
    grouped_result: FixtureSplitResult,
) -> None:
    """The manifest uses train, validation, test — not lexicographic split order."""
    splits = [assignment.split for assignment in grouped_result.split_manifest.split_assignments]
    assert splits == ["train", "train", "validation", "validation", "test", "test"]


def test_grouped_fixture_matches_its_golden_identities(
    grouped_result: FixtureSplitResult,
) -> None:
    assert grouped_result.split_manifest.computed_split_hash == GROUPED_SPLIT_HASH
    assert grouped_result.split_fingerprint_record.split_fingerprint == GROUPED_FINGERPRINT


# ---------------------------------------------------------------------------
# 15.4 Canonical artifacts
# ---------------------------------------------------------------------------


def test_group_registry_golden_bytes(golden_result: FixtureSplitResult) -> None:
    assert golden_result.group_registry_bytes == GOLDEN_GROUP_REGISTRY


def test_example_registry_golden_bytes(golden_result: FixtureSplitResult) -> None:
    assert golden_result.example_registry_bytes == GOLDEN_EXAMPLE_REGISTRY


def test_excluded_ledger_golden_bytes(golden_result: FixtureSplitResult) -> None:
    assert golden_result.excluded_ledger_bytes == GOLDEN_EXCLUDED_LEDGER


def test_summary_identity_core_golden_bytes(golden_result: FixtureSplitResult) -> None:
    assert golden_result.split_summary_identity_core_bytes == GOLDEN_CORE_BYTES


def test_summary_document_golden_bytes(golden_result: FixtureSplitResult) -> None:
    assert golden_result.split_summary_document_bytes == GOLDEN_SUMMARY_BYTES


def test_audit_report_golden_bytes(golden_result: FixtureSplitResult) -> None:
    assert golden_result.audit_report_bytes == GOLDEN_AUDIT_BYTES


def test_group_id_golden_vector(golden_result: FixtureSplitResult) -> None:
    assert GOLDEN_TRAIN_GROUP_ID.encode() in golden_result.group_registry_bytes


def test_group_id_payload_has_exactly_six_members() -> None:
    request = _request()
    joined = join_labels(
        request.ordered_rows,
        request.source_labels,
        transformation_version=request.transformation_version,
    )
    label_totals = _zero_totals(DECISIONS)
    for example in joined:
        label_totals[example.decision] += 1
    assignments = allocate_indivisible_groups(
        joined, constrained_apportionment(label_totals, request.partition_totals)
    )
    assignment = assignments[0]
    # ``decision`` is deliberately not a seventh member: B1 derives partition_key
    # from the algorithm version, the seed, the document and the decision
    # stratum, so the decision is already bound transitively.
    payload = {
        "schema": "mesc-pilot-01-group/1",
        "source_document_id": assignment.source_document_id,
        "assigned_split": assignment.partition,
        "example_ids": sorted(assignment.example_ids),
        "row_ordinals": sorted(assignment.row_ordinals),
        "partition_key": assignment.partition_key,
    }
    assert len(payload) == 6
    assert "decision" not in payload
    expected = "mesc-pilot-01-group/1:sha256:" + sha256_of_bytes(canonical_json_bytes(payload))
    assert _group_id(assignment) == expected
    assert len(expected.split(":")[-1]) == 64


@pytest.mark.parametrize(
    "surface",
    [
        "group_registry_bytes",
        "example_registry_bytes",
        "excluded_ledger_bytes",
        "split_summary_identity_core_bytes",
        "split_summary_document_bytes",
        "audit_report_bytes",
    ],
)
def test_every_byte_surface_ends_in_exactly_one_terminal_lf(
    golden_result: FixtureSplitResult, surface: str
) -> None:
    """The B2A serializer keeps its terminal LF inside the hashed bytes."""
    payload: bytes = getattr(golden_result, surface)
    assert type(payload) is bytes
    assert payload.endswith(b"\n")
    assert not payload.endswith(b"\n\n")


def test_jsonl_surfaces_have_one_line_per_record(golden_result: FixtureSplitResult) -> None:
    assert golden_result.group_registry_bytes.count(b"\n") == 3
    assert golden_result.example_registry_bytes.count(b"\n") == 3
    assert b"\n\n" not in golden_result.example_registry_bytes


def test_registry_order_is_lexicographic_not_canonical_partition_order(
    grouped_result: FixtureSplitResult,
) -> None:
    """Lexicographically ``test`` sorts before ``train`` before ``validation``."""
    for surface in (grouped_result.group_registry_bytes, grouped_result.example_registry_bytes):
        splits = [
            line.split(b'"assigned_split":"')[1].split(b'"')[0] for line in surface.splitlines()
        ]
        assert splits == sorted(splits)
        assert splits[0] == b"test"


def test_registry_schema_versions_match_the_accepted_b2a_roles() -> None:
    assert ARTIFACT_SCHEMA_VERSIONS["group_registry"] == GROUP_REGISTRY_SCHEMA
    assert ARTIFACT_SCHEMA_VERSIONS["example_registry"] == EXAMPLE_REGISTRY_SCHEMA
    assert ARTIFACT_SCHEMA_VERSIONS["excluded_ledger"] == EXCLUDED_LEDGER_SCHEMA


def test_identity_core_schema_is_not_the_final_summary_schema(
    golden_result: FixtureSplitResult,
) -> None:
    assert (
        golden_result.split_summary_identity_core.schema_version
        == (ARTIFACT_SCHEMA_VERSIONS["split_summary"])
    )
    assert ARTIFACT_SCHEMA_VERSIONS["split_summary"] != SPLIT_SUMMARY_SCHEMA
    assert SPLIT_SUMMARY_SCHEMA.encode() in golden_result.split_summary_document_bytes


def test_excluded_ledger_is_a_zero_exclusion_constant(golden_result: FixtureSplitResult) -> None:
    assert golden_result.split_summary_identity_core.excluded_record_count == 0
    assert b'"count":0' in golden_result.excluded_ledger_bytes
    assert b'"excluded_ids":[]' in golden_result.excluded_ledger_bytes
    assert b'"reason":"none"' in golden_result.excluded_ledger_bytes


def test_summary_core_carries_every_combination_explicitly(
    golden_result: FixtureSplitResult,
) -> None:
    core = golden_result.split_summary_identity_core
    assert set(core.partition_totals) == {"train", "validation", "test"}
    assert set(core.group_counts_by_partition) == {"train", "validation", "test"}
    assert set(core.label_totals) == set(DECISIONS)
    assert set(core.partition_label_matrix) == {"train", "validation", "test"}
    for row in core.partition_label_matrix.values():
        assert set(row) == set(DECISIONS)


def test_final_summary_is_not_fed_into_its_own_fingerprint(
    golden_result: FixtureSplitResult,
) -> None:
    """The fingerprint binds the fingerprint-free identity core, never the summary."""
    fingerprint = golden_result.split_fingerprint_record.split_fingerprint
    assert fingerprint.encode() not in golden_result.split_summary_identity_core_bytes
    assert b"split_fingerprint" not in golden_result.split_summary_identity_core_bytes
    assert b"split_hash" not in golden_result.split_summary_identity_core_bytes
    assert fingerprint.encode() in golden_result.split_summary_document_bytes
    assert GOLDEN_SPLIT_HASH.encode() in golden_result.split_summary_document_bytes


def test_all_four_descriptors_bind_the_exact_bytes(golden_result: FixtureSplitResult) -> None:
    payloads = {
        "group_registry": golden_result.group_registry_bytes,
        "example_registry": golden_result.example_registry_bytes,
        "excluded_ledger": golden_result.excluded_ledger_bytes,
        "split_summary": golden_result.split_summary_identity_core_bytes,
    }
    descriptors = golden_result.split_fingerprint_record.identity.artifact_descriptors
    assert {descriptor.role for descriptor in descriptors} == set(payloads)
    for descriptor in descriptors:
        payload = payloads[descriptor.role]
        assert descriptor.sha256 == sha256_of_bytes(payload)
        assert descriptor.byte_size == len(payload)
        verify_descriptor_against_bytes(descriptor, payload)


def test_authoritative_fingerprint_verifies(golden_result: FixtureSplitResult) -> None:
    verify_split_fingerprint_record(golden_result.split_fingerprint_record)


def test_tampered_payload_fails_closed(golden_result: FixtureSplitResult) -> None:
    descriptor = next(
        item
        for item in golden_result.split_fingerprint_record.identity.artifact_descriptors
        if item.role == "group_registry"
    )
    with pytest.raises(InvalidSha256Error):
        verify_descriptor_against_bytes(descriptor, golden_result.group_registry_bytes + b"x")


def test_tampered_fingerprint_fails_closed(golden_result: FixtureSplitResult) -> None:
    tampered = SplitFingerprintRecord(
        identity=golden_result.split_fingerprint_record.identity,
        split_fingerprint="0" * 64,
    )
    with pytest.raises(FingerprintMismatchError):
        verify_split_fingerprint_record(tampered)


def test_tampered_identity_core_fails_closed(golden_result: FixtureSplitResult) -> None:
    core = golden_result.split_summary_identity_core
    tampered_core = dataclasses.replace(core, total_example_count=core.total_example_count + 1)
    descriptor = next(
        item
        for item in golden_result.split_fingerprint_record.identity.artifact_descriptors
        if item.role == "split_summary"
    )
    with pytest.raises(InvalidSha256Error):
        verify_descriptor_against_bytes(descriptor, tampered_core.canonical_bytes())


def test_summary_core_is_the_accepted_b2a_type(golden_result: FixtureSplitResult) -> None:
    assert type(golden_result.split_summary_identity_core) is SplitSummaryIdentityCore
    assert (
        golden_result.split_summary_identity_core_bytes
        == golden_result.split_summary_identity_core.canonical_bytes()
    )


# ---------------------------------------------------------------------------
# 15.5 Leakage integration
# ---------------------------------------------------------------------------


def test_explicit_findings_are_preserved_exactly(golden_result: FixtureSplitResult) -> None:
    assert golden_result.audit_report.findings == (FALSE_POSITIVE_FINDING,)
    assert golden_result.audit_report.finding_count == 1
    assert golden_result.audit_report.detection_methods == DETECTION_METHODS


def test_empty_report_is_permitted_for_a_unit_fixture(grouped_result: FixtureSplitResult) -> None:
    """An empty report is never evidence that a fixture is clean; B2D decides that."""
    assert grouped_result.audit_report.findings == ()
    assert grouped_result.audit_report.finding_count == 0
    assert grouped_result.audit_report.leaked is False


def test_findings_are_sorted_by_the_accepted_b2b_code() -> None:
    unsorted = tuple(
        sorted((FALSE_POSITIVE_FINDING, UNRESOLVED_FINDING), key=lambda f: f.finding_id)
    )[::-1]
    report = LeakageAuditReport.create(findings=unsorted, detection_methods=DETECTION_METHODS)
    identifiers = [finding.finding_id for finding in report.findings]
    assert identifiers == sorted(identifiers)


def test_aggregate_leaked_is_derived_not_declared() -> None:
    report = LeakageAuditReport.create(
        findings=(UNRESOLVED_FINDING,), detection_methods=DETECTION_METHODS
    )
    assert report.leaked is True


def test_b2b_typed_error_propagates_as_itself() -> None:
    """A detection method outside the B2B allowlist fails as a B2B contract error."""
    request = _identity_completed_request(detection_methods=("not-a-detection-method",))
    with pytest.raises(InvalidReportInvariantError) as caught:
        FixtureSplitFacade.run(request)
    assert not isinstance(caught.value, FixtureFacadeContractError)


def test_report_bytes_come_from_the_accepted_b2b_serializer(
    golden_result: FixtureSplitResult,
) -> None:
    assert type(golden_result.audit_report) is LeakageAuditReport
    assert golden_result.audit_report_bytes == golden_result.audit_report.to_canonical_bytes()


def test_facade_performs_no_pair_enumeration_or_discovery(
    grouped_result: FixtureSplitResult,
) -> None:
    """Six examples across three documents still yield zero findings without input."""
    assert grouped_result.audit_report.finding_count == 0
    assert b'"findings":[]' in grouped_result.audit_report_bytes


def test_no_b2d_fixture_is_implemented_or_qualified() -> None:
    from medscale.mesc import _fixture_split_v1

    source_values = [value for value in vars(_fixture_split_v1).values() if isinstance(value, str)]
    for reserved in ("exact-reference-1000-v1", "constraint-stress-1000-v1", "leakage-positive-v1"):
        assert reserved not in source_values


# ---------------------------------------------------------------------------
# 15.6 Side-effect boundary
# ---------------------------------------------------------------------------


def test_facade_runs_with_every_side_effect_channel_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The whole pipeline runs with I/O, clock, randomness and environment poisoned."""

    def refuse(*args: object, **kwargs: object) -> Any:
        raise AssertionError("the fixture facade must perform no side effect")

    monkeypatch.setattr(builtins, "open", refuse)
    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(subprocess, "Popen", refuse)
    monkeypatch.setattr(subprocess, "run", refuse)
    monkeypatch.setattr(time, "time", refuse)
    monkeypatch.setattr(time, "monotonic", refuse)
    monkeypatch.setattr(random, "random", refuse)
    monkeypatch.setattr(random, "shuffle", refuse)
    monkeypatch.setattr(os, "getenv", refuse)
    monkeypatch.setattr(os, "urandom", refuse)

    result = FixtureSplitFacade.run(_request())
    assert result.split_fingerprint_record.split_fingerprint == GOLDEN_FINGERPRINT


def test_module_imports_no_io_capable_module() -> None:
    from medscale.mesc import _fixture_split_v1

    imported = {
        name
        for name, value in vars(_fixture_split_v1).items()
        if isinstance(value, types.ModuleType)
    }
    assert imported == set()


def test_module_adds_no_dependency_outside_the_authorized_internals() -> None:
    from medscale.mesc import _fixture_split_v1

    allowed_prefixes = ("medscale.mesc._", "medscale.mesc.split")
    for value in vars(_fixture_split_v1).values():
        module_name = getattr(value, "__module__", None)
        if module_name is None or not module_name.startswith("medscale"):
            continue
        assert module_name.startswith(allowed_prefixes)


def test_facade_is_stateless(golden_result: FixtureSplitResult) -> None:
    facade = FixtureSplitFacade()
    assert not hasattr(facade, "__dict__")
    assert FixtureSplitFacade.__slots__ == ()
    repeated = FixtureSplitFacade.run(_request())
    assert repeated.split_summary_document_bytes == golden_result.split_summary_document_bytes


# ---------------------------------------------------------------------------
# 15.7 Scope and predecessor preservation
# ---------------------------------------------------------------------------


def test_module_is_not_publicly_exported() -> None:
    import medscale.mesc as mesc_package

    for name in (
        "FixtureSplitFacade",
        "FixtureSplitRequest",
        "FixtureSplitResult",
        "FixtureFacadeContractError",
    ):
        assert name not in mesc_package.__all__
        assert not hasattr(mesc_package, name)


def test_module_defines_no_dunder_all() -> None:
    from medscale.mesc import _fixture_split_v1

    assert not hasattr(_fixture_split_v1, "__all__")


def test_module_exposes_no_cli_entry_point() -> None:
    from medscale.mesc import _fixture_split_v1

    assert not hasattr(_fixture_split_v1, "main")
    assert not hasattr(_fixture_split_v1, "app")
    assert not hasattr(_fixture_split_v1, "cli")


def test_accepted_predecessor_surfaces_are_unchanged() -> None:
    assert PilotSplitManifest(split_assignments=()).split_seed == "mesc-pilot-01"
    assert SPLIT_SEED == "mesc-pilot-01-split-v1"
    assert set(ARTIFACT_SCHEMA_VERSIONS) == {
        "example_registry",
        "excluded_ledger",
        "group_registry",
        "split_summary",
    }


# ---------------------------------------------------------------------------
# Result contract
# ---------------------------------------------------------------------------


def test_result_has_exactly_the_twelve_authorized_fields() -> None:
    assert tuple(field.name for field in dataclasses.fields(FixtureSplitResult)) == (
        "request_id",
        "split_manifest",
        "group_registry_bytes",
        "example_registry_bytes",
        "excluded_ledger_bytes",
        "split_summary_identity_core",
        "split_summary_identity_core_bytes",
        "split_summary_document_bytes",
        "split_fingerprint_record",
        "audit_report",
        "audit_report_bytes",
        "execution_evidence_ref",
    )


def test_result_is_frozen_and_slotted(golden_result: FixtureSplitResult) -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        golden_result.request_id = "other"  # type: ignore[misc]
    assert not hasattr(golden_result, "__dict__")


def test_result_binds_the_validated_request_identity(golden_result: FixtureSplitResult) -> None:
    assert golden_result.request_id == GOLDEN_REQUEST_ID
    assert golden_result.execution_evidence_ref == EXECUTION_EVIDENCE_REF


def test_result_partition_counts_reconcile(golden_result: FixtureSplitResult) -> None:
    observed = _zero_totals(("train", "validation", "test"))
    for assignment in golden_result.split_manifest.split_assignments:
        observed[assignment.split] += 1
    assert observed == GOLDEN_TOTALS
    assert dict(golden_result.split_summary_identity_core.partition_totals) == GOLDEN_TOTALS
