"""Deterministic P01-05 B1 evidence-cue domain tests.

Synthetic fixtures only: no real registry, no real subset, no real annotation,
no test-partition use, no retrieval, no network, no model execution. These tests
pin the ratified B1 supplied-evidence channel (FD-P01-05-B1-EVIDENCE-1):
label blindness, deterministic evidence identity, exact A/B comparison without
invented consensus, and fail-closed cue/pack validation.
"""

from __future__ import annotations

import hashlib
import json
from typing import cast

import pytest

from medscale.mesc._b1_evidence import (
    ANNOTATION_PROTOCOL_VERSION,
    ANNOTATION_VIEW_SCHEMA_VERSION,
    DEVELOPMENT_SUBSET_SCHEMA_VERSION,
    DEVELOPMENT_SUBSET_SIZE,
    EVIDENCE_CUE_SCHEMA_VERSION,
    EVIDENCE_ID_PREFIX,
    EVIDENCE_PACK_SCHEMA_VERSION,
    SUBSET_DOMAIN_SEPARATOR,
    VALIDATION_POPULATION,
    B1AnnotationComparison,
    B1EvidencePack,
    B1EvidenceReferenceError,
    B1EvidenceValidationError,
    B1SourceRecord,
    DevelopmentSubsetSelection,
    ExampleRegistryRow,
    annotation_input_from_source_record,
    build_evidence_pack,
    build_final_cue_from_adjudication,
    build_final_cue_from_agreement,
    compare_annotations,
    cue_from_document,
    cue_to_document,
    load_b1_source_records_from_bytes,
    load_development_subset_from_bytes,
    load_example_registry_from_bytes,
    make_adjudication_submission,
    make_annotation_submission,
    pack_from_document,
    pack_to_document,
    render_annotation_view,
    segment_sha256,
    select_development_subset,
    subset_manifest_document,
    subset_ordering_key,
    validate_evidence_cue,
    validate_evidence_pack,
    validate_view_has_no_prohibited_fields,
)
from medscale.mesc._canonical_json_v1 import canonical_json_bytes

_SPLIT_FINGERPRINT = "43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91"


def _source(example_id: str = "e0", document: str = "pmid:1") -> B1SourceRecord:
    return B1SourceRecord(
        example_id=example_id,
        source_document_id=document,
        question="does aspirin help?",
        context=("first segment", "second segment", "third segment"),
    )


def _agreed(record: B1SourceRecord, *, indices: list[int], status: str) -> B1EvidencePack:
    submission = make_annotation_submission(
        reviewer_id="r1",
        example_id=record.example_id,
        source_document_id=record.source_document_id,
        selected_segment_indices=indices,
        annotation_status=status,
    )
    comparison = B1AnnotationComparison(
        example_id=submission.example_id,
        source_document_id=submission.source_document_id,
        outcome="AGREED",
        submission_a=submission,
        submission_b=submission,
    )
    cue = build_final_cue_from_agreement(comparison, source_record=record)
    return build_evidence_pack(
        [cue], source_split_fingerprint=_SPLIT_FINGERPRINT, subset_digest="0" * 64
    )


def _registry_row(example_id: str, split: str, ordinal: int) -> dict[str, object]:
    return {
        "schema_version": "mesc-pilot-01-example-registry/1",
        "example_id": example_id,
        "source_document_id": f"pmid:{ordinal}",
        "assigned_split": split,
        "partition_key": f"pk-{ordinal}",
        "row_ordinal": ordinal,
    }


# --------------------------------------------------------------- hashing
def test_segment_sha256_uses_exact_utf8_bytes() -> None:
    assert segment_sha256("abc") == hashlib.sha256(b"abc").hexdigest()
    assert segment_sha256("abc") != segment_sha256("abc ")
    assert segment_sha256("A") != segment_sha256("a")


def test_subset_ordering_key_is_domain_separated_and_deterministic() -> None:
    key = subset_ordering_key("e0")
    assert len(key) == 64
    assert key == subset_ordering_key("e0")
    assert subset_ordering_key("e0") != subset_ordering_key("e1")
    assert key == hashlib.sha256(f"{SUBSET_DOMAIN_SEPARATOR}:e0".encode()).hexdigest()


# --------------------------------------------------------------- source records
def test_source_records_are_label_free_and_reject_label_fields() -> None:
    with pytest.raises(B1EvidenceValidationError, match="decision"):
        load_b1_source_records_from_bytes(
            b'{"example_id":"e0","source_document_id":"pmid:1",'
            b'"question":"q","context":["c"],"decision":"yes"}\n'
        )


def test_source_records_require_exact_fields() -> None:
    with pytest.raises(B1EvidenceValidationError, match="fields must be exactly"):
        load_b1_source_records_from_bytes(
            b'{"example_id":"e0","source_document_id":"pmid:1",'
            b'"question":"q","context":["c"],"extra":1}\n'
        )


# --------------------------------------------------------------- annotation views
def test_annotation_view_is_label_blind() -> None:
    record = _source()
    view = render_annotation_view(annotation_input_from_source_record(record))
    assert view["schema_version"] == ANNOTATION_VIEW_SCHEMA_VERSION
    assert set(view) == {
        "schema_version",
        "example_id",
        "source_document_id",
        "question",
        "context",
    }
    assert view["context"] == list(record.context)
    validate_view_has_no_prohibited_fields(view)


def test_prohibited_view_field_names_are_rejected_recursively() -> None:
    with pytest.raises(B1EvidenceValidationError, match="prohibited field"):
        validate_view_has_no_prohibited_fields({"decision": "yes"})
    with pytest.raises(B1EvidenceValidationError, match="prohibited field"):
        validate_view_has_no_prohibited_fields({"nested": [{"long_answer": "x"}]})


# --------------------------------------------------------------- submissions
def test_available_submission_requires_at_least_one_segment() -> None:
    with pytest.raises(B1EvidenceValidationError, match="at least one selected segment"):
        make_annotation_submission(
            reviewer_id="r1",
            example_id="e0",
            source_document_id="pmid:1",
            selected_segment_indices=[],
            annotation_status="AVAILABLE",
        )


def test_insufficient_submission_must_have_no_segments() -> None:
    with pytest.raises(B1EvidenceValidationError, match="must have no selected segment"):
        make_annotation_submission(
            reviewer_id="r1",
            example_id="e0",
            source_document_id="pmid:1",
            selected_segment_indices=[1],
            annotation_status="INSUFFICIENT",
        )


def test_submission_indices_must_be_strictly_increasing() -> None:
    with pytest.raises(B1EvidenceValidationError, match="strictly increasing"):
        make_annotation_submission(
            reviewer_id="r1",
            example_id="e0",
            source_document_id="pmid:1",
            selected_segment_indices=[1, 0],
            annotation_status="AVAILABLE",
        )


# --------------------------------------------------------------- comparison
def test_identical_submissions_agree() -> None:
    a = make_annotation_submission(
        reviewer_id="r1",
        example_id="e0",
        source_document_id="pmid:1",
        selected_segment_indices=[1],
        annotation_status="AVAILABLE",
    )
    b = make_annotation_submission(
        reviewer_id="r2",
        example_id="e0",
        source_document_id="pmid:1",
        selected_segment_indices=[1],
        annotation_status="AVAILABLE",
    )
    comparison = compare_annotations(a, b)
    assert comparison.outcome == "AGREED"
    assert comparison.submission_a.reviewer_id == "r1"
    assert comparison.submission_b.reviewer_id == "r2"


def test_divergent_submissions_require_adjudication_never_consensus() -> None:
    a = make_annotation_submission(
        reviewer_id="r1",
        example_id="e0",
        source_document_id="pmid:1",
        selected_segment_indices=[1],
        annotation_status="AVAILABLE",
    )
    b = make_annotation_submission(
        reviewer_id="r2",
        example_id="e0",
        source_document_id="pmid:1",
        selected_segment_indices=[2],
        annotation_status="AVAILABLE",
    )
    comparison = compare_annotations(a, b)
    assert comparison.outcome == "ADJUDICATION_REQUIRED"
    with pytest.raises(B1EvidenceValidationError, match="human adjudication"):
        build_final_cue_from_agreement(comparison, source_record=_source())


def test_comparison_rejects_different_examples() -> None:
    a = make_annotation_submission(
        reviewer_id="r1",
        example_id="e0",
        source_document_id="pmid:1",
        selected_segment_indices=[1],
        annotation_status="AVAILABLE",
    )
    b = make_annotation_submission(
        reviewer_id="r2",
        example_id="e1",
        source_document_id="pmid:1",
        selected_segment_indices=[1],
        annotation_status="AVAILABLE",
    )
    with pytest.raises(B1EvidenceValidationError, match="different example_ids"):
        compare_annotations(a, b)


# --------------------------------------------------------------- final cues
def test_evidence_id_is_deterministic_and_reviewer_independent() -> None:
    record = _source()
    first = _agreed(record, indices=[1], status="AVAILABLE").cues[0]
    second = _agreed(record, indices=[1], status="AVAILABLE").cues[0]
    assert first.evidence_id == second.evidence_id
    assert first.evidence_id.startswith(EVIDENCE_ID_PREFIX)
    assert first.review_status == "FINAL"


def test_evidence_id_changes_with_status_and_segments() -> None:
    record = _source()
    available = _agreed(record, indices=[1], status="AVAILABLE").cues[0]
    insufficient = _agreed(record, indices=[], status="INSUFFICIENT").cues[0]
    other = _agreed(record, indices=[2], status="AVAILABLE").cues[0]
    assert available.evidence_id != insufficient.evidence_id
    assert available.evidence_id != other.evidence_id


def test_adjudication_builds_final_cue() -> None:
    record = _source()
    adjudication = make_adjudication_submission(
        reviewer_id="adjudicator-1",
        example_id="e0",
        source_document_id="pmid:1",
        selected_segment_indices=[0, 2],
        annotation_status="AVAILABLE",
    )
    cue = build_final_cue_from_adjudication(adjudication, source_record=record)
    assert cue.review_status == "FINAL"
    assert tuple(ref.context_segment_index for ref in cue.ordered_segment_references) == (0, 2)
    validate_evidence_cue(cue, record.context)


# --------------------------------------------------------------- cue validation
def test_cue_segment_hash_mismatch_fails_closed() -> None:
    record = _source()
    cue = _agreed(record, indices=[1], status="AVAILABLE").cues[0]
    with pytest.raises(B1EvidenceReferenceError, match="segment hash mismatch"):
        validate_evidence_cue(cue, ("first segment", "TAMPERED second segment", "third segment"))


def test_non_final_cue_fails_validation() -> None:
    record = _source()
    cue = _agreed(record, indices=[1], status="AVAILABLE").cues[0]
    document = cue_to_document(cue)
    document["review_status"] = "AGREED"
    parsed = cue_from_document(document)
    with pytest.raises(B1EvidenceValidationError, match="FINAL"):
        validate_evidence_cue(parsed, record.context)


def test_cue_serialization_round_trip_is_lossless() -> None:
    record = _source()
    cue = _agreed(record, indices=[1], status="AVAILABLE").cues[0]
    assert cue_from_document(cue_to_document(cue)) == cue


# --------------------------------------------------------------- subset selection
def _registry(rows: list[dict[str, object]]) -> tuple[tuple[ExampleRegistryRow, ...], str]:
    lines = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    return load_example_registry_from_bytes(lines.encode("utf-8"))


def test_subset_selection_is_deterministic() -> None:
    rows = [_registry_row(f"e{i}", "validation", i) for i in range(200)]
    rows += [_registry_row(f"t{i}", "test", 200 + i) for i in range(20)]
    registry_rows, registry_sha256 = _registry(rows)
    first = select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
        require_production_counts=False,
    )
    second = select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
        require_production_counts=False,
    )
    assert first.subset_digest == second.subset_digest
    assert first.schema_version == DEVELOPMENT_SUBSET_SCHEMA_VERSION
    assert first.selected_count == 100
    assert len(first.ordered_selected_example_ids) == 100
    assert len(set(first.ordered_selected_example_ids)) == 100
    assert first.validation_population == 200


def test_subset_selection_never_reads_labels_or_test_rows() -> None:
    rows = [_registry_row(f"e{i}", "validation", i) for i in range(200)]
    rows += [_registry_row(f"t{i}", "test", 200 + i) for i in range(20)]
    registry_rows, registry_sha256 = _registry(rows)
    selection = select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
    )
    assert all("t" not in example_id for example_id in selection.ordered_selected_example_ids)


def test_production_count_guards_fail_closed() -> None:
    rows = [_registry_row(f"e{i}", "validation", i) for i in range(20)]
    registry_rows, registry_sha256 = _registry(rows)
    with pytest.raises(B1EvidenceValidationError, match="validation population"):
        select_development_subset(
            registry_rows,
            registry_sha256=registry_sha256,
            source_split_fingerprint=_SPLIT_FINGERPRINT,
            require_production_counts=True,
        )


def test_subset_digest_changes_with_split_fingerprint() -> None:
    rows = [_registry_row(f"e{i}", "validation", i) for i in range(200)]
    registry_rows, registry_sha256 = _registry(rows)
    a = select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
    )
    b = select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint="0" * 64,
    )
    assert a.subset_digest != b.subset_digest


def _subset_selection() -> DevelopmentSubsetSelection:
    rows = [_registry_row(f"e{i}", "validation", i) for i in range(200)]
    registry_rows, registry_sha256 = _registry(rows)
    return select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
    )


def test_subset_manifest_round_trip_preserves_identity() -> None:
    selection = _subset_selection()
    loaded = load_development_subset_from_bytes(
        canonical_json_bytes(subset_manifest_document(selection)) + b"\n"
    )
    assert loaded == selection


def test_subset_manifest_rejects_tampered_digest() -> None:
    selection = _subset_selection()
    document = subset_manifest_document(selection)
    document["subset_digest"] = "f" * 64
    with pytest.raises(B1EvidenceValidationError, match="does not match its content"):
        load_development_subset_from_bytes(canonical_json_bytes(document))


def test_pack_binds_to_supplied_subset_identity() -> None:
    selection = _subset_selection()
    selected = selection.ordered_selected_example_ids
    outside = next(f"e{i}" for i in range(200) if f"e{i}" not in selected)
    member_pack = _agreed(
        _source(example_id=selected[0], document=selection.ordered_selected_source_document_ids[0]),
        indices=[1],
        status="AVAILABLE",
    )
    bound = build_evidence_pack(
        list(member_pack.cues),
        source_split_fingerprint=_SPLIT_FINGERPRINT,
        subset_digest=selection.subset_digest,
        development_subset=selection,
    )
    assert bound.subset_digest == selection.subset_digest
    with pytest.raises(B1EvidenceValidationError, match="does not match the supplied"):
        build_evidence_pack(
            list(member_pack.cues),
            source_split_fingerprint=_SPLIT_FINGERPRINT,
            subset_digest="0" * 64,
            development_subset=selection,
        )
    outsider_pack = _agreed(
        _source(example_id=outside, document="pmid:1"), indices=[1], status="AVAILABLE"
    )
    with pytest.raises(B1EvidenceValidationError, match="not a member"):
        build_evidence_pack(
            list(outsider_pack.cues),
            source_split_fingerprint=_SPLIT_FINGERPRINT,
            subset_digest=selection.subset_digest,
            development_subset=selection,
        )


def test_registry_rows_reject_duplicate_json_keys() -> None:
    with pytest.raises(B1EvidenceValidationError, match="duplicate JSON key"):
        load_example_registry_from_bytes(
            b'{"schema_version":"mesc-pilot-01-example-registry/1",'
            b'"example_id":"e0","example_id":"e1","source_document_id":"pmid:1",'
            b'"assigned_split":"validation","partition_key":"pk","row_ordinal":0}\n'
        )


def test_registry_rows_reject_unknown_splits() -> None:
    row = _registry_row("e0", "tuning", 0)
    line = json.dumps(row, sort_keys=True, separators=(",", ":"))
    with pytest.raises(B1EvidenceValidationError, match="assigned_split"):
        load_example_registry_from_bytes((line + "\n").encode("utf-8"))


# --------------------------------------------------------------- evidence pack
def test_pack_round_trip_and_self_hash() -> None:
    record = _source()
    pack = _agreed(record, indices=[1], status="AVAILABLE")
    assert pack.schema_version == EVIDENCE_PACK_SCHEMA_VERSION
    assert pack.record_count == 1
    assert len(pack.pack_sha256) == 64
    assert pack_from_document(pack_to_document(pack)) == pack
    validate_evidence_pack(pack, {(record.example_id, record.source_document_id): record.context})


def test_pack_rejects_non_final_cues() -> None:
    record = _source()
    pack = _agreed(record, indices=[1], status="AVAILABLE")
    document = pack_to_document(pack)
    cues = cast("list[dict[str, object]]", document["cues"])
    cues[0]["review_status"] = "ADJUDICATED"
    with pytest.raises(B1EvidenceValidationError, match="FINAL"):
        build_evidence_pack(
            [cue_from_document(cues[0])],
            source_split_fingerprint=_SPLIT_FINGERPRINT,
            subset_digest="0" * 64,
        )


def test_pack_requires_exact_record_count_when_fixed() -> None:
    record = _source()
    pack = _agreed(record, indices=[1], status="AVAILABLE")
    with pytest.raises(B1EvidenceValidationError, match="exactly 100"):
        build_evidence_pack(
            list(pack.cues),
            source_split_fingerprint=_SPLIT_FINGERPRINT,
            subset_digest="0" * 64,
            require_record_count=100,
        )


def test_pack_rejects_tampered_sha() -> None:
    record = _source()
    pack = _agreed(record, indices=[1], status="AVAILABLE")
    document = pack_to_document(pack)
    document["pack_sha256"] = "f" * 64
    parsed = pack_from_document(document)
    with pytest.raises(B1EvidenceValidationError, match="SHA-256"):
        validate_evidence_pack(
            parsed, {(record.example_id, record.source_document_id): record.context}
        )


def test_derive_evidence_id_excludes_reviewer_and_environment() -> None:
    record = _source()
    first = make_annotation_submission(
        reviewer_id="r1",
        example_id=record.example_id,
        source_document_id=record.source_document_id,
        selected_segment_indices=[1],
        annotation_status="AVAILABLE",
    )
    second = make_annotation_submission(
        reviewer_id="reviewer-999",
        example_id=record.example_id,
        source_document_id=record.source_document_id,
        selected_segment_indices=[1],
        annotation_status="AVAILABLE",
    )
    cue_a = build_final_cue_from_agreement(compare_annotations(first, second), source_record=record)
    cue_b = build_final_cue_from_agreement(compare_annotations(second, first), source_record=record)
    assert cue_a.evidence_id.startswith("mesc-b1-evidence:")
    assert cue_a.evidence_id == cue_b.evidence_id
    assert ANNOTATION_PROTOCOL_VERSION == "mesc-pilot-01-b1-annotation/1"
    assert EVIDENCE_CUE_SCHEMA_VERSION == "mesc-pilot-01-b1-evidence-cue/1"


def test_constants_pin_production_contract() -> None:
    assert VALIDATION_POPULATION == 150
    assert DEVELOPMENT_SUBSET_SIZE == 100
    assert SUBSET_DOMAIN_SEPARATOR == "mesc-pilot-01-b1-evidence-subset/1"
