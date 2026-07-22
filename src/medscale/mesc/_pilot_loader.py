"""Deterministic, fail-closed loader for B0 pilot input examples.

This private module never discovers a dataset, never knows an evidence root,
never opens P01-03G, and never infers or loads P01-04 partition membership. It
does no work at import time. It accepts only an explicit caller-supplied path,
bytes, or record collection, parses deterministically, and fails closed on any
malformed or ambiguous input.

The gold/final decision is retained structurally separate from the question and
context so it can be used for scoring only and never leak into a model prompt.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from medscale.mesc._split_v1 import (
    DECISIONS,
    Decision,
    canonical_json_bytes,
    sha256_hexdigest,
)

__all__ = [
    "B0InputDataset",
    "B0InputRecord",
    "PilotLoaderError",
    "load_b0_inputs_from_bytes",
    "load_b0_inputs_from_path",
    "load_b0_inputs_from_records",
]

_REQUIRED_KEYS: frozenset[str] = frozenset(
    {
        "example_id",
        "row_ordinal",
        "source_document_id",
        "dataset_id",
        "dataset_revision",
        "configuration",
        "question",
        "context",
        "decision",
    }
)


class PilotLoaderError(ValueError):
    """Raised when B0 pilot input cannot be parsed unambiguously."""


@dataclass(frozen=True, slots=True)
class B0InputRecord:
    """One normalized B0 input example.

    ``gold_decision`` is the held-out label. It is present for scoring only and
    is never part of the prompt-facing fields (``question``, ``context``).
    """

    example_id: str
    row_ordinal: int
    source_document_id: str
    dataset_id: str
    dataset_revision: str
    configuration: str
    question: str
    context: tuple[str, ...]
    gold_decision: Decision


@dataclass(frozen=True, slots=True)
class B0InputDataset:
    """A deterministically ordered, identity-consistent B0 input set."""

    dataset_id: str
    dataset_revision: str
    configuration: str
    records: tuple[B0InputRecord, ...]
    input_sha256: str
    input_size: int


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise PilotLoaderError(f"duplicate JSON key: {key!r}")
        seen.add(key)
    return dict(pairs)


def _require_nonblank_str(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PilotLoaderError(f"{field} must be a non-blank string")
    return value


def _require_nonnegative_int(value: object, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise PilotLoaderError(f"{field} must be a non-negative integer, got {value!r}")
    return value


def _require_decision(value: object) -> Decision:
    if value not in DECISIONS:
        raise PilotLoaderError(f"decision must be one of {DECISIONS}, got {value!r}")
    # ``value`` is one of the Decision literals; narrow for the type checker.
    for candidate in DECISIONS:
        if value == candidate:
            return candidate
    raise PilotLoaderError(f"decision must be one of {DECISIONS}, got {value!r}")


def _require_context(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise PilotLoaderError("context must be a list of strings")
    segments: list[str] = []
    for index, segment in enumerate(value):
        if not isinstance(segment, str):
            raise PilotLoaderError(f"context[{index}] must be a string, got {segment!r}")
        segments.append(segment)
    return tuple(segments)


def _record_from_object(obj: Mapping[str, object]) -> B0InputRecord:
    keys = set(obj)
    missing = sorted(_REQUIRED_KEYS - keys)
    unexpected = sorted(keys - _REQUIRED_KEYS)
    if missing or unexpected:
        raise PilotLoaderError(
            f"record fields must be exactly {sorted(_REQUIRED_KEYS)}; "
            f"missing={missing}, unexpected={unexpected}"
        )
    return B0InputRecord(
        example_id=_require_nonblank_str(obj["example_id"], "example_id"),
        row_ordinal=_require_nonnegative_int(obj["row_ordinal"], "row_ordinal"),
        source_document_id=_require_nonblank_str(obj["source_document_id"], "source_document_id"),
        dataset_id=_require_nonblank_str(obj["dataset_id"], "dataset_id"),
        dataset_revision=_require_nonblank_str(obj["dataset_revision"], "dataset_revision"),
        configuration=_require_nonblank_str(obj["configuration"], "configuration"),
        question=_require_nonblank_str(obj["question"], "question"),
        context=_require_context(obj["context"]),
        gold_decision=_require_decision(obj["decision"]),
    )


def _assemble(
    records: Sequence[B0InputRecord], *, input_sha256: str, input_size: int
) -> B0InputDataset:
    if not records:
        raise PilotLoaderError("B0 input must contain at least one record")
    seen_example_ids: set[str] = set()
    seen_ordinals: set[int] = set()
    identities: set[tuple[str, str, str]] = set()
    for record in records:
        if record.example_id in seen_example_ids:
            raise PilotLoaderError(f"duplicate example_id: {record.example_id}")
        if record.row_ordinal in seen_ordinals:
            raise PilotLoaderError(f"duplicate row_ordinal: {record.row_ordinal}")
        seen_example_ids.add(record.example_id)
        seen_ordinals.add(record.row_ordinal)
        identities.add((record.dataset_id, record.dataset_revision, record.configuration))
    if len(identities) != 1:
        raise PilotLoaderError("records contain inconsistent dataset identities")
    dataset_id, dataset_revision, configuration = next(iter(identities))
    ordered = tuple(sorted(records, key=lambda record: record.row_ordinal))
    return B0InputDataset(
        dataset_id=dataset_id,
        dataset_revision=dataset_revision,
        configuration=configuration,
        records=ordered,
        input_sha256=input_sha256,
        input_size=input_size,
    )


def _canonical_record_payload(records: Sequence[B0InputRecord]) -> list[dict[str, object]]:
    return [
        {
            "example_id": record.example_id,
            "row_ordinal": record.row_ordinal,
            "source_document_id": record.source_document_id,
            "dataset_id": record.dataset_id,
            "dataset_revision": record.dataset_revision,
            "configuration": record.configuration,
            "question": record.question,
            "context": list(record.context),
            "decision": record.gold_decision,
        }
        for record in sorted(records, key=lambda record: record.row_ordinal)
    ]


def load_b0_inputs_from_records(records: Sequence[Mapping[str, object]]) -> B0InputDataset:
    """Load B0 inputs from an in-memory sequence of record mappings."""
    parsed = [_record_from_object(obj) for obj in records]
    payload = _canonical_record_payload(parsed)
    canonical = canonical_json_bytes(payload)
    return _assemble(parsed, input_sha256=sha256_hexdigest(payload), input_size=len(canonical))


def load_b0_inputs_from_bytes(
    data: bytes,
    *,
    expected_sha256: str | None = None,
    expected_size: int | None = None,
) -> B0InputDataset:
    """Load B0 inputs from raw JSONL bytes, verifying any caller attestation."""
    if not isinstance(data, bytes | bytearray):
        raise PilotLoaderError("input must be bytes")
    raw = bytes(data)
    actual_sha256 = sha256_hexdigest_of_bytes(raw)
    actual_size = len(raw)
    if expected_size is not None and expected_size != actual_size:
        raise PilotLoaderError(f"input size mismatch: expected {expected_size}, got {actual_size}")
    if expected_sha256 is not None and expected_sha256 != actual_sha256:
        raise PilotLoaderError("input SHA-256 mismatch")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PilotLoaderError(f"input is not valid UTF-8: {exc}") from exc
    parsed: list[B0InputRecord] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
        except json.JSONDecodeError as exc:
            raise PilotLoaderError(f"line {line_number}: malformed JSON: {exc}") from exc
        if not isinstance(obj, dict):
            raise PilotLoaderError(f"line {line_number}: each record must be a JSON object")
        parsed.append(_record_from_object(obj))
    return _assemble(parsed, input_sha256=actual_sha256, input_size=actual_size)


def load_b0_inputs_from_path(
    path: Path,
    *,
    expected_sha256: str | None = None,
    expected_size: int | None = None,
) -> B0InputDataset:
    """Load B0 inputs from an explicit caller-supplied JSONL file path."""
    return load_b0_inputs_from_bytes(
        path.read_bytes(), expected_sha256=expected_sha256, expected_size=expected_size
    )


def sha256_hexdigest_of_bytes(data: bytes) -> str:
    """Full lowercase SHA-256 of exact bytes (for raw-input attestation)."""
    import hashlib

    return hashlib.sha256(data).hexdigest()
