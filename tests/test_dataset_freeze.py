"""Focused acceptance tests for ALIGN-14 SplitAssignmentFreeze."""

from __future__ import annotations

import dataclasses

import pytest

from medscale.dataset.builder import __all__ as builder_all
from medscale.dataset.builder.contracts import __all__ as contracts_all
from medscale.dataset.builder.fingerprint import __all__ as fingerprint_all
from medscale.dataset.builder.freeze import (
    _SUPPORTED_VERSION,
    SplitAssignmentFreeze,
    _identity_payload,
)
from medscale.dataset.builder.manifest import (
    DatasetReleaseManifest,
)
from medscale.dataset.builder.manifest import (
    __all__ as manifest_all,
)
from medscale.dataset.split import SplitStrategy
from medscale.reproducibility import content_hash

_EXPECTED_FREEZE_FINGERPRINT_LENGTH = 64
_EXPECTED_BUILDER_SYMBOLS = {
    "AuditReport",
    "DatasetReleaseManifest",
    "PipelineContext",
    "QualityReport",
    "StageDefinition",
    "SplitAssignmentFreeze",
    "StageResult",
    "context_fingerprint",
    "pipeline_fingerprint",
}
_PLACEHOLDERS = {
    "FingerprintInput",
    "ManifestRecord",
    "DatasetBinding",
    "DataloaderPolicy",
    "EvidenceDomain",
    "BondingKey",
    "ReleaserBinding",
    "ProvenanceCursor",
    "DatasetEngine",
}


def test_builder_module_exports_remain_exact() -> None:
    assert set(builder_all) == _EXPECTED_BUILDER_SYMBOLS


def test_contracts_module_exports_are_exact() -> None:
    assert set(contracts_all) == {"PipelineContext", "StageDefinition", "StageResult"}


def test_manifest_module_exports_are_exact() -> None:
    assert set(manifest_all) == {"AuditReport", "DatasetReleaseManifest", "QualityReport"}


def test_fingerprint_module_exports_are_exact() -> None:
    assert set(fingerprint_all) == {"context_fingerprint", "pipeline_fingerprint"}


def test_placeholder_names_are_not_exported() -> None:
    for module_symbols in (builder_all, contracts_all, manifest_all, fingerprint_all):
        assert _PLACEHOLDERS.isdisjoint(module_symbols)


def _valid_freeze() -> SplitAssignmentFreeze:
    return SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=7,
        train=["α-1", "β-2"],  # noqa: RUF001
        validation=["γ-3"],  # noqa: RUF001
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )


def test_valid_freeze_is_frozen_and_stable() -> None:
    freeze = _valid_freeze()
    with pytest.raises(dataclasses.FrozenInstanceError):
        freeze.train = ()  # type: ignore[misc]


def test_valid_version_is_accepted() -> None:
    _valid_freeze()


def test_empty_individual_splits_are_accepted() -> None:
    freeze = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=[],
        validation=[],
        test=["only-test"],
        contract_version=_SUPPORTED_VERSION,
    )
    assert freeze.assignment_count == 1


def test_all_splits_empty_are_rejected() -> None:
    with pytest.raises(ValueError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=0,
            train=[],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_boolean_seed_rejected() -> None:
    with pytest.raises(TypeError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=True,
            train=["id"],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )
    with pytest.raises(TypeError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=False,
            train=["id"],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_non_integer_seed_rejected() -> None:
    with pytest.raises(TypeError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed="1",
            train=["id"],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_valid_strategy_members_are_accepted() -> None:
    for strategy in SplitStrategy:
        freeze = SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=strategy,
            seed=0,
            train=["id"],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )
        assert freeze.strategy is strategy


def test_valid_strategy_influences_fingerprint() -> None:
    first = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["id"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    second = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["id"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    assert first.freeze_fingerprint == second.freeze_fingerprint
    assert first.strategy is SplitStrategy.DETERMINISTIC_HASH_SPLIT


def test_invalid_strategy_is_rejected() -> None:
    for invalid in (
        123,
        "deterministic_hash_split",
        "",
        True,
        False,
        None,
        [],
        {},
        object(),
    ):
        with pytest.raises(TypeError):
            SplitAssignmentFreeze(
                source_dataset_fingerprint="dataset-fingerprint",
                strategy=invalid,
                seed=0,
                train=["id"],
                validation=[],
                test=[],
                contract_version=_SUPPORTED_VERSION,
            )


def test_whitespace_only_identifier_rejected() -> None:
    with pytest.raises(ValueError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=0,
            train=[" "],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_non_string_identifier_rejected() -> None:
    with pytest.raises(TypeError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=0,
            train=[1],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_empty_identifier_rejected() -> None:
    with pytest.raises(ValueError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=0,
            train=[""],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_duplicate_within_split_rejected() -> None:
    with pytest.raises(ValueError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=0,
            train=["id", "id"],
            validation=[],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_duplicate_across_splits_rejected() -> None:
    with pytest.raises(ValueError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=0,
            train=["id"],
            validation=["id"],
            test=[],
            contract_version=_SUPPORTED_VERSION,
        )


def test_invalid_version_rejected() -> None:
    with pytest.raises(ValueError):
        SplitAssignmentFreeze(
            source_dataset_fingerprint="dataset-fingerprint",
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=0,
            train=["id"],
            validation=[],
            test=[],
            contract_version="unsupported/v9",
        )


def test_negative_seed_is_accepted() -> None:
    freeze = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=-1,
        train=["id"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    assert freeze.seed == -1


def test_unicode_and_case_are_preserved() -> None:
    freeze = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["ID-1", "id-1"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    assert freeze.train == ("ID-1", "id-1")
    assert freeze.assignment_count == 2


def test_leading_and_trailing_whitespace_preserved() -> None:
    freeze = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=[" ID-1 ", "ID-1"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    assert freeze.train == (" ID-1 ", "ID-1")


def test_mutating_caller_input_does_not_mutate_object() -> None:
    train = ["id"]
    validation = []
    test = []
    freeze = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=train,
        validation=validation,
        test=test,
        contract_version=_SUPPORTED_VERSION,
    )
    train.append("mutated")
    validation.append("mutated")
    test.append("mutated")
    assert freeze.train == ("id",)
    assert freeze.validation == ()
    assert freeze.test == ()
    assert freeze.assignment_count == 1


def test_derived_properties_expose_immutable_values() -> None:
    freeze = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["id"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    assert freeze.assignment_count == 1
    assert len(freeze.freeze_fingerprint) == _EXPECTED_FREEZE_FINGERPRINT_LENGTH
    assert freeze.freeze_fingerprint == content_hash(
        {
            "contract_version": _SUPPORTED_VERSION,
            "kind": "medscale.dataset.split_assignment_freeze",
            "seed": 0,
            "source_dataset_fingerprint": "dataset-fingerprint",
            "strategy": str(SplitStrategy.DETERMINISTIC_HASH_SPLIT),
            "test": [],
            "train": ["id"],
            "validation": [],
        }
    )


def test_assignment_count_derivation() -> None:
    freeze = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["a", "b"],
        validation=["c"],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    assert freeze.assignment_count == 3


def test_input_order_does_not_affect_fingerprint() -> None:
    first = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["a", "b", "c"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    second = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["c", "a", "b"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    assert first.freeze_fingerprint == second.freeze_fingerprint


def test_material_difference_changes_fingerprint() -> None:
    base = SplitAssignmentFreeze(
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=["id"],
        validation=[],
        test=[],
        contract_version=_SUPPORTED_VERSION,
    )
    changed_seed = dataclasses.replace(base, seed=1)
    changed_identifier = dataclasses.replace(base, train=["other"])
    payload_a = _identity_payload(
        contract_version=_SUPPORTED_VERSION,
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=("id",),
        validation=(),
        test=(),
    )
    payload_b = _identity_payload(
        contract_version=_SUPPORTED_VERSION,
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=("id",),
        validation=(),
        test=(),
    )
    payload_c = _identity_payload(
        contract_version=_SUPPORTED_VERSION,
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=1,
        train=("id",),
        validation=(),
        test=(),
    )
    assert base.freeze_fingerprint != changed_seed.freeze_fingerprint
    assert base.freeze_fingerprint != changed_identifier.freeze_fingerprint
    assert content_hash(payload_a) == content_hash(payload_b)
    assert content_hash(payload_a) != content_hash(payload_c)


def test_release_manifest_remains_unchanged() -> None:
    expected_fields = dataclasses.fields(DatasetReleaseManifest)
    assert tuple(field.name for field in expected_fields) == (
        "dataset_id",
        "dataset_version",
        "dataset_fingerprint",
        "release_id",
        "released_at",
        "released_by",
        "dataset_manifest_sha256",
        "bundle_id_registry_sha256",
        "validation_summary",
        "quality_summary",
        "release_notes",
        "previous_release_id",
    )


def test_identity_payload_excludes_derived_fields() -> None:
    payload = _identity_payload(
        contract_version=_SUPPORTED_VERSION,
        source_dataset_fingerprint="dataset-fingerprint",
        strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
        seed=0,
        train=("a",),
        validation=(),
        test=(),
    )
    assert "assignment_count" not in payload
    assert "freeze_fingerprint" not in payload
    assert payload["kind"] == "medscale.dataset.split_assignment_freeze"
    assert payload["contract_version"] == _SUPPORTED_VERSION
