"""Synthetic-fixture tests for the deterministic B0 pilot loader.

No real PubMedQA file, no P01-03G artifact, no frozen evidence is read. Every
fixture is constructed in-memory or under ``tmp_path``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale.mesc._pilot_loader import (
    B0InputDataset,
    PilotLoaderError,
    load_b0_inputs_from_bytes,
    load_b0_inputs_from_path,
    load_b0_inputs_from_records,
    sha256_hexdigest_of_bytes,
)


def _record(ordinal: int, **overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "example_id": f"e{ordinal}",
        "row_ordinal": ordinal,
        "source_document_id": f"pmid:{ordinal}",
        "dataset_id": "ds",
        "dataset_revision": "rev-1",
        "configuration": "cfg",
        "question": f"question {ordinal}?",
        "context": [f"context {ordinal}"],
        "decision": "yes",
    }
    record.update(overrides)
    return record


def _jsonl(records: list[dict[str, object]]) -> bytes:
    return ("\n".join(json.dumps(record) for record in records) + "\n").encode("utf-8")


def test_valid_records_load_ordered_and_identity_consistent() -> None:
    dataset = load_b0_inputs_from_records([_record(2), _record(0), _record(1)])
    assert isinstance(dataset, B0InputDataset)
    assert [record.row_ordinal for record in dataset.records] == [0, 1, 2]
    assert dataset.dataset_id == "ds"
    assert dataset.records[0].gold_decision == "yes"
    assert len(dataset.input_sha256) == 64
    assert dataset.input_size > 0


def test_bytes_and_path_agree_and_sort_by_ordinal(tmp_path: Path) -> None:
    data = _jsonl([_record(1, decision="no"), _record(0, decision="maybe")])
    from_bytes = load_b0_inputs_from_bytes(data)
    path = tmp_path / "inputs.jsonl"
    path.write_bytes(data)
    from_path = load_b0_inputs_from_path(path)
    assert from_bytes == from_path
    assert [r.row_ordinal for r in from_bytes.records] == [0, 1]
    assert from_bytes.records[0].gold_decision == "maybe"


def test_gold_decision_is_structurally_separate() -> None:
    dataset = load_b0_inputs_from_records([_record(0, decision="no")])
    record = dataset.records[0]
    assert record.gold_decision == "no"
    # The prompt-facing fields never contain the gold label.
    assert "no" not in record.question.split()
    assert all("no" not in segment.split() for segment in record.context)


def test_sha256_and_size_attestation_roundtrip_and_mismatch() -> None:
    data = _jsonl([_record(0)])
    digest = sha256_hexdigest_of_bytes(data)
    load_b0_inputs_from_bytes(data, expected_sha256=digest, expected_size=len(data))
    with pytest.raises(PilotLoaderError, match="size mismatch"):
        load_b0_inputs_from_bytes(data, expected_size=len(data) + 1)
    with pytest.raises(PilotLoaderError, match="SHA-256 mismatch"):
        load_b0_inputs_from_bytes(data, expected_sha256="0" * 64)


def test_empty_input_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="at least one record"):
        load_b0_inputs_from_bytes(b"\n\n")


def test_malformed_json_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="malformed JSON"):
        load_b0_inputs_from_bytes(b'{"example_id": "e0", ')


def test_duplicate_json_keys_fail_closed() -> None:
    line = b'{"example_id": "e0", "example_id": "e0", "row_ordinal": 0}'
    with pytest.raises(PilotLoaderError, match="duplicate JSON key"):
        load_b0_inputs_from_bytes(line + b"\n")


def test_non_object_line_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="must be a JSON object"):
        load_b0_inputs_from_bytes(b"[1, 2, 3]\n")


def test_non_utf8_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="not valid UTF-8"):
        load_b0_inputs_from_bytes(b"\xff\xfe not utf8\n")


def test_missing_and_unexpected_fields_fail_closed() -> None:
    missing = _record(0)
    del missing["question"]
    with pytest.raises(PilotLoaderError, match="missing="):
        load_b0_inputs_from_records([missing])
    extra = _record(0)
    extra["unexpected"] = "x"
    with pytest.raises(PilotLoaderError, match="unexpected="):
        load_b0_inputs_from_records([extra])


def test_blank_identifiers_fail_closed() -> None:
    with pytest.raises(PilotLoaderError, match="example_id must be a non-blank string"):
        load_b0_inputs_from_records([_record(0, example_id="")])
    with pytest.raises(PilotLoaderError, match="source_document_id"):
        load_b0_inputs_from_records([_record(0, source_document_id="   ")])


@pytest.mark.parametrize("bad_ordinal", [True, False, 0.5, 1.0, "1", None, -1])
def test_invalid_row_ordinal_types_fail_closed(bad_ordinal: object) -> None:
    with pytest.raises(PilotLoaderError, match="row_ordinal"):
        load_b0_inputs_from_records([_record(0, row_ordinal=bad_ordinal)])


def test_invalid_decision_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="decision must be one of"):
        load_b0_inputs_from_records([_record(0, decision="unsure")])


def test_invalid_context_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="context must be a list"):
        load_b0_inputs_from_records([_record(0, context="not-a-list")])
    with pytest.raises(PilotLoaderError, match=r"context\[0\] must be a string"):
        load_b0_inputs_from_records([_record(0, context=[1])])


def test_duplicate_example_id_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="duplicate example_id"):
        load_b0_inputs_from_records([_record(0), _record(1, example_id="e0")])


def test_duplicate_row_ordinal_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="duplicate row_ordinal"):
        load_b0_inputs_from_records([_record(0), _record(0, example_id="e-alt")])


def test_inconsistent_dataset_identity_fails_closed() -> None:
    with pytest.raises(PilotLoaderError, match="inconsistent dataset identities"):
        load_b0_inputs_from_records([_record(0), _record(1, dataset_revision="rev-2")])


def test_loader_writes_no_artifact(tmp_path: Path) -> None:
    before = set(tmp_path.iterdir())
    load_b0_inputs_from_records([_record(0)])
    assert set(tmp_path.iterdir()) == before
