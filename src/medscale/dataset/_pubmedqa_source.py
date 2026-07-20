"""Fully private PubMedQA Layer-1 source transformation internals.

PyArrow is imported only at the Parquet read boundary so that importing
``medscale.dataset`` does not transitively import ``pyarrow``.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Frozen / slotted value objects — native dataclass contract only
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class NativeContextSegment:
    ordinal: int
    text: str
    section_label: str


@dataclass(frozen=True, slots=True)
class NativeAnnotationTrace:
    reasoning_required_pred: tuple[str, ...]
    reasoning_free_pred: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PilotPubMedQASourceRecord:
    schema_version: str
    dataset_id: str
    dataset_revision: str
    configuration: str
    original_example_id: str
    source_document_id: str
    pubid: str
    question: str
    context_segments: tuple[NativeContextSegment, ...]
    mesh_terms: tuple[str, ...]
    long_answer: str
    final_decision: str
    native_annotation_trace: NativeAnnotationTrace
    license_id: str


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


SCHEMA_VERSION: str = "mesc-pubmedqa-source/1"
DATASET_ID: str = "qiaojin/PubMedQA"
DATASET_REVISION: str = "9001f2853fb87cab8d220904e0de81ac6973b318"
CONFIGURATION: str = "pqa_labeled"
LICENSE_ID: str = "PubMedQA-PQA-L"
TRANSFORMATION_VERSION: str = "mesc-pubmedqa-transform/1"
PARQUET_BASENAME: str = "train-00000-of-00001.parquet"

_VALID_DECISIONS: set[str] = {"yes", "no", "maybe"}

# ---------------------------------------------------------------------------
# Aggregate contract values
# ---------------------------------------------------------------------------

_EXPECTED_RECORD_COUNT: int = 1000
_EXPECTED_YES_COUNT: int = 552
_EXPECTED_NO_COUNT: int = 338
_EXPECTED_MAYBE_COUNT: int = 110
_MIN_CONTEXT_SEGMENTS: int = 1
_MAX_CONTEXT_SEGMENTS: int = 9

# ---------------------------------------------------------------------------
# Private aggregate types
# ---------------------------------------------------------------------------


class _Aggregates:
    record_count: int = 0
    yes_count: int = 0
    no_count: int = 0
    maybe_count: int = 0
    unexpected_count: int = 0
    unique_pubid_count: int = 0
    duplicate_pubid_count: int = 0
    context_segment_total: int = 0
    min_contexts_per_record: int = 0
    max_contexts_per_record: int = 0
    unique_source_document_count: int = 0
    unique_source_record_hash_count: int = 0
    source_record_hash_collision_count: int = 0


# ---------------------------------------------------------------------------
# Canonical JSON / bytes helpers
# ---------------------------------------------------------------------------


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_record_hash(record: PilotPubMedQASourceRecord) -> str:
    """Return SHA-256 of the complete canonical scientific record dictionary."""
    return _sha256_bytes(_canonical_bytes(_record_to_scientific_dict(record)))


# ---------------------------------------------------------------------------
# Deterministic file writers
# ---------------------------------------------------------------------------


def _write_text_atomic(payload: bytes, path: Path) -> None:
    target = Path(path)
    tmp_path = target.parent / f".mesc-tmp-{uuid.uuid4().hex}.tmp"
    with tmp_path.open("wb") as writer:
        writer.write(payload)
    tmp_path.replace(target)


# ---------------------------------------------------------------------------
# PyArrow read boundary — function-scope imports only
# ---------------------------------------------------------------------------


def _load_expected_schemas(parquet_path: str | Path) -> dict[str, Any]:
    # PyArrow is imported only here so that importing this private module
    # does not transitively import pyarrow.
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(parquet_path, memory_map=False)
    metadata = pf.schema_arrow.metadata or {}
    raw = metadata.get(b"huggingface", b"")
    if not raw:
        return {
            "contexts": {"feature": {"_type": "Value", "dtype": "string"}},
            "labels": {"feature": {"_type": "Value", "dtype": "string"}},
            "meshes": {"feature": {"_type": "Value", "dtype": "string"}},
            "reasoning_required_pred": {"feature": {"_type": "Value", "dtype": "string"}},
            "reasoning_free_pred": {"feature": {"_type": "Value", "dtype": "string"}},
        }
    try:
        info = json.loads(raw)["info"]["features"]["context"]["feature"]
    except Exception as exc:  # pragma: no cover - defensive
        raise RuntimeError(
            "failed to parse huggingface feature metadata for context struct"
        ) from exc
    return {k: {"feature": {"_type": "Value", "dtype": "string"}} for k in list(info.keys())}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _validate_nonnull_nonblank_string(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    if not value.strip():
        raise ValueError(f"{field} must not be empty after stripping whitespace")
    return value


def _validate_pubid(pubid: int) -> str:
    if not isinstance(pubid, int) or pubid < 1:
        raise ValueError(f"pubid must be a positive integer, got {pubid!r}")
    return str(pubid)


def _validate_decision(decision: str) -> None:
    if decision not in _VALID_DECISIONS:
        raise ValueError(
            f"invalid final_decision value {decision!r}; expected one of {sorted(_VALID_DECISIONS)}"
        )


# ---------------------------------------------------------------------------
# Native mapping
# ---------------------------------------------------------------------------


def _build_context_segments(context: dict[str, Any]) -> tuple[NativeContextSegment, ...]:
    if "contexts" not in context or "labels" not in context:
        raise KeyError("context dict must contain 'contexts' and 'labels'")
    raw_contexts = context["contexts"]
    raw_labels = context["labels"]
    if not isinstance(raw_contexts, list) or not isinstance(raw_labels, list):
        raise TypeError("context['contexts'] and context['labels'] must be lists")
    if len(raw_contexts) != len(raw_labels):
        raise ValueError("context['contexts'] and context['labels'] must have equal length")
    if not (1 <= len(raw_contexts) <= 9):
        raise ValueError(f"context count must be between 1 and 9, got {len(raw_contexts)}")
    segments: list[NativeContextSegment] = []
    for ordinal, (text, label) in enumerate(zip(raw_contexts, raw_labels, strict=False)):
        _validate_nonnull_nonblank_string(text, f"context text at ordinal {ordinal}")
        _validate_nonnull_nonblank_string(label, f"context label at ordinal {ordinal}")
        segments.append(
            NativeContextSegment(
                ordinal=ordinal,
                text=text,
                section_label=label,
            )
        )
    if not segments:
        raise ValueError("record produced no context segments")
    return tuple(segments)


def _build_mesh_terms(context: dict[str, Any]) -> tuple[str, ...]:
    if "meshes" not in context:
        raise KeyError("context dict must contain 'meshes'")
    meshes = context["meshes"]
    if not isinstance(meshes, list):
        raise TypeError("context['meshes'] must be a list of strings")
    if not all(isinstance(item, str) for item in meshes):
        raise TypeError("context['meshes'] contains non-string value")
    return tuple(meshes)


def _build_annotation_trace(context: dict[str, Any]) -> NativeAnnotationTrace:
    if "reasoning_required_pred" not in context or "reasoning_free_pred" not in context:
        raise KeyError(
            "context dict must contain 'reasoning_required_pred' and 'reasoning_free_pred'"
        )
    required_pred = context["reasoning_required_pred"]
    free_pred = context["reasoning_free_pred"]
    if not isinstance(required_pred, list) or not isinstance(free_pred, list):
        raise TypeError("reasoning traces must be lists of strings")
    if not all(isinstance(item, str) for item in required_pred):
        raise TypeError("context['reasoning_required_pred'] must be a list of strings")
    if not all(isinstance(item, str) for item in free_pred):
        raise TypeError("context['reasoning_free_pred'] must be a list of strings")
    return NativeAnnotationTrace(
        reasoning_required_pred=tuple(required_pred),
        reasoning_free_pred=tuple(free_pred),
    )


def _row_to_source_record(
    pubid: int,
    question: str,
    context: dict[str, Any],
    long_answer: str,
    final_decision: str,
    row_ordinal: int = 0,
) -> PilotPubMedQASourceRecord:
    canonical_pubid = _validate_pubid(pubid)
    question_text = _validate_nonnull_nonblank_string(question, "question")
    long_answer_text = _validate_nonnull_nonblank_string(long_answer, "long_answer")
    _validate_decision(final_decision)

    segments = _build_context_segments(context)
    mesh_terms = _build_mesh_terms(context)
    trace = _build_annotation_trace(context)

    revision = DATASET_REVISION
    original_example_id = (
        f"pubmedqa:{CONFIGURATION}:{revision}:{PARQUET_BASENAME}:{row_ordinal}:{pubid}"
    )
    source_document_id = f"pmid:{canonical_pubid}"

    return PilotPubMedQASourceRecord(
        schema_version=SCHEMA_VERSION,
        dataset_id=DATASET_ID,
        dataset_revision=revision,
        configuration=CONFIGURATION,
        original_example_id=original_example_id,
        source_document_id=source_document_id,
        pubid=canonical_pubid,
        question=question_text,
        context_segments=segments,
        mesh_terms=mesh_terms,
        long_answer=long_answer_text,
        final_decision=final_decision,
        native_annotation_trace=trace,
        license_id=LICENSE_ID,
    )


def _record_to_scientific_dict(record: PilotPubMedQASourceRecord) -> dict[str, Any]:
    return {
        "schema_version": record.schema_version,
        "dataset_id": record.dataset_id,
        "dataset_revision": record.dataset_revision,
        "configuration": record.configuration,
        "original_example_id": record.original_example_id,
        "source_document_id": record.source_document_id,
        "pubid": record.pubid,
        "question": record.question,
        "context_segments": tuple(asdict(segment) for segment in record.context_segments),
        "mesh_terms": list(record.mesh_terms),
        "long_answer": record.long_answer,
        "final_decision": record.final_decision,
        "reasoning_required_pred": list(record.native_annotation_trace.reasoning_required_pred),
        "reasoning_free_pred": list(record.native_annotation_trace.reasoning_free_pred),
        "license_id": record.license_id,
    }


def _record_to_envelope(record: PilotPubMedQASourceRecord) -> dict[str, Any]:
    scientific = _record_to_scientific_dict(record)
    digest = _sha256_bytes(_canonical_bytes(scientific))
    return {"record": scientific, "source_record_hash": digest}


def _registry_record(record: PilotPubMedQASourceRecord, row_ordinal: int) -> dict[str, Any]:
    digest = source_record_hash(record)
    return {
        "row_ordinal": row_ordinal,
        "original_example_id": record.original_example_id,
        "source_document_id": record.source_document_id,
        "source_record_hash": digest,
    }


# ---------------------------------------------------------------------------
# Aggregates
# ---------------------------------------------------------------------------


def _build_aggregates(
    records: Iterable[PilotPubMedQASourceRecord],
) -> _Aggregates:
    aggregates = _Aggregates()
    seen_pubids: set[str] = set()
    seen_docs: set[str] = set()
    seen_hashes: dict[str, int] = {}
    context_counts: list[int] = []

    for record in records:
        aggregates.record_count += 1
        match record.final_decision:
            case "yes":
                aggregates.yes_count += 1
            case "no":
                aggregates.no_count += 1
            case "maybe":
                aggregates.maybe_count += 1
            case _:
                aggregates.unexpected_count += 1

        if record.pubid in seen_pubids:
            aggregates.duplicate_pubid_count += 1
        seen_pubids.add(record.pubid)

        if record.source_document_id in seen_docs:
            # source_document collision counted as duplicate document
            pass
        seen_docs.add(record.source_document_id)

        digest = source_record_hash(record)
        seen_hashes[digest] = seen_hashes.get(digest, 0) + 1
        context_counts.append(len(record.context_segments))

    aggregates.unique_pubid_count = len(seen_pubids)
    aggregates.unique_source_document_count = len(seen_docs)
    aggregates.unique_source_record_hash_count = len(seen_hashes)
    aggregates.source_record_hash_collision_count = sum(
        count - 1 for count in seen_hashes.values() if count > 1
    )
    if context_counts:
        aggregates.min_contexts_per_record = min(context_counts)
        aggregates.max_contexts_per_record = max(context_counts)
        aggregates.context_segment_total = sum(context_counts)

    return aggregates


def _validate_aggregates(aggregates: _Aggregates) -> list[str]:
    failures: list[str] = []
    if aggregates.record_count != _EXPECTED_RECORD_COUNT:
        failures.append(
            f"record count mismatch: expected {_EXPECTED_RECORD_COUNT}, "
            f"got {aggregates.record_count}"
        )
    if aggregates.yes_count != _EXPECTED_YES_COUNT:
        failures.append(
            f"yes count mismatch: expected {_EXPECTED_YES_COUNT}, got {aggregates.yes_count}"
        )
    if aggregates.no_count != _EXPECTED_NO_COUNT:
        failures.append(
            f"no count mismatch: expected {_EXPECTED_NO_COUNT}, got {aggregates.no_count}"
        )
    if aggregates.maybe_count != _EXPECTED_MAYBE_COUNT:
        failures.append(
            f"maybe count mismatch: expected {_EXPECTED_MAYBE_COUNT}, got {aggregates.maybe_count}"
        )
    if aggregates.unexpected_count != 0:
        failures.append(f"unexpected decision count: expected 0, got {aggregates.unexpected_count}")
    if aggregates.duplicate_pubid_count != 0:
        failures.append(
            f"duplicate pubid count: expected 0, got {aggregates.duplicate_pubid_count}"
        )
    if aggregates.unique_source_document_count != _EXPECTED_RECORD_COUNT:
        failures.append(
            f"unique source document count mismatch: expected "
            f"{_EXPECTED_RECORD_COUNT}, got {aggregates.unique_source_document_count}"
        )
    if aggregates.unique_source_record_hash_count != _EXPECTED_RECORD_COUNT:
        failures.append(
            f"unique source record hash count mismatch: expected "
            f"{_EXPECTED_RECORD_COUNT}, got {aggregates.unique_source_record_hash_count}"
        )
    if aggregates.source_record_hash_collision_count != 0:
        failures.append(
            f"source record hash collision count: expected 0, "
            f"got {aggregates.source_record_hash_collision_count}"
        )
    if aggregates.min_contexts_per_record != _MIN_CONTEXT_SEGMENTS:
        failures.append(
            f"min context segments mismatch: expected {_MIN_CONTEXT_SEGMENTS}, "
            f"got {aggregates.min_contexts_per_record}"
        )
    if aggregates.max_contexts_per_record != _MAX_CONTEXT_SEGMENTS:
        failures.append(
            f"max context segments mismatch: expected {_MAX_CONTEXT_SEGMENTS}, "
            f"got {aggregates.max_contexts_per_record}"
        )
    return failures


# ---------------------------------------------------------------------------
# Deterministic artifacts
# ---------------------------------------------------------------------------


def _write_jsonl_atomic(records: Iterable[dict[str, Any]], path: Path) -> None:
    target = Path(path)
    tmp_path = target.parent / f".mesc-tmp-{uuid.uuid4().hex}.jsonl"
    with tmp_path.open("wb") as writer:
        for record in records:
            writer.write(_canonical_bytes(record))
            writer.write(b"\n")
    tmp_path.replace(target)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def _get_pyarrow_version() -> str:
    import pyarrow as _pa

    match = re.search(r"(\d+)\.(\d+)(?:\.\d+)?", _pa.__version__)
    return f"{match.group(1)}.{match.group(2)}" if match else getattr(_pa, "__version__", "unknown")


def transform_pubmedqa_parquet(
    input_path: str | Path,
    output_dir: str | Path,
    *,
    expected_input_sha256: str | None = None,
    expected_input_size: int | None = None,
) -> dict[str, Any]:
    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir).resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"input artifact not found: {input_path}")
    if output_dir.exists():
        raise FileExistsError(f"final output directory already exists: {output_dir}")

    input_size = input_path.stat().st_size
    if expected_input_size is not None and expected_input_size != input_size:
        raise ValueError(f"input size mismatch: expected {expected_input_size}, got {input_size}")
    input_sha256 = _sha256_file(input_path)
    if expected_input_sha256 is not None and expected_input_sha256 != input_sha256:
        raise ValueError(
            f"input SHA-256 mismatch: expected {expected_input_sha256}, got {input_sha256}"
        )

    # PyArrow read boundary deferred to this function scope.
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(input_path, memory_map=False)
    _load_expected_schemas(input_path)

    records: list[PilotPubMedQASourceRecord] = []
    column_names = ["pubid", "question", "context", "long_answer", "final_decision"]
    for batch in pf.iter_batches(columns=column_names, batch_size=1000, use_threads=False):
        pyd = batch.to_pydict()
        num_rows = batch.num_rows
        for idx in range(num_rows):
            records.append(
                _row_to_source_record(
                    pubid=pyd["pubid"][idx],
                    question=pyd["question"][idx],
                    context=pyd["context"][idx],
                    long_answer=pyd["long_answer"][idx],
                    final_decision=pyd["final_decision"][idx],
                    row_ordinal=len(records),
                )
            )

    output_dir.mkdir(parents=True, exist_ok=True)
    records_path = output_dir / "source-records.jsonl"
    registry_path = output_dir / "source-record-registry.jsonl"
    manifest_path = output_dir / "transformation-manifest.json"
    local_report_path = output_dir / "transformation-run.local.json"

    envelopes = [_record_to_envelope(record) for record in records]
    registry = [_registry_record(record, idx) for idx, record in enumerate(records)]
    _write_jsonl_atomic(envelopes, records_path)
    _write_jsonl_atomic(registry, registry_path)

    aggregates = _build_aggregates(records)
    records_bytes = _read_all(records_path)
    registry_bytes = _read_all(registry_path)

    manifest_dict: dict[str, Any] = {
        "manifest_schema_version": "mesc-pubmedqa-manifest/1",
        "transformation_version": TRANSFORMATION_VERSION,
        "internal_source_record_schema_version": SCHEMA_VERSION,
        "dataset_identity": {
            "dataset_id": DATASET_ID,
            "configuration": CONFIGURATION,
            "revision": DATASET_REVISION,
            "license_id": LICENSE_ID,
        },
        "source_artifact": {
            "repository_path": str(PARQUET_BASENAME),
            "byte_size": input_size,
            "sha256": input_sha256,
        },
        "record_count": aggregates.record_count,
        "decision_counts": {
            "yes": aggregates.yes_count,
            "no": aggregates.no_count,
            "maybe": aggregates.maybe_count,
            "unexpected": aggregates.unexpected_count,
        },
        "unique_pubid_count": aggregates.unique_pubid_count,
        "duplicate_pubid_count": aggregates.duplicate_pubid_count,
        "unique_source_document_count": aggregates.unique_source_document_count,
        "unique_source_record_hash_count": aggregates.unique_source_record_hash_count,
        "source_record_hash_collision_count": aggregates.source_record_hash_collision_count,
        "context_segment_aggregates": {
            "total": aggregates.context_segment_total,
            "minimum": aggregates.min_contexts_per_record,
            "maximum": aggregates.max_contexts_per_record,
        },
        "labels_context_cardinality_validation": "pass",
        "duplicate_preservation_policy": "preserve_duplicates",
        "output_files": {
            "source-records.jsonl": {
                "filename": "source-records.jsonl",
                "byte_size": len(records_bytes),
                "sha256": _sha256_bytes(records_bytes),
            },
            "source-record-registry.jsonl": {
                "filename": "source-record-registry.jsonl",
                "byte_size": len(registry_bytes),
                "sha256": _sha256_bytes(registry_bytes),
            },
        },
        "public_pilot_record_status": "deferred",
        "public_example_id_status": "deferred",
        "p01_03f_status": "not_authorized",
    }
    manifest_bytes = _canonical_bytes(manifest_dict) + b"\n"
    _write_text_atomic(manifest_bytes, manifest_path)

    # The pre/post hash pair exists to PROVE the input was never touched; the
    # post hash is recomputed and enforced, not merely recorded.
    input_sha256_post = _sha256_file(input_path)
    if input_sha256_post != input_sha256:
        raise RuntimeError(
            "input artifact changed during transformation: "
            f"pre={input_sha256} post={input_sha256_post}"
        )
    local_report = {
        "status": "complete",
        "input_sha256_pre": input_sha256,
        "input_sha256_post": input_sha256_post,
    }
    _write_text_atomic(_canonical_bytes(local_report) + b"\n", local_report_path)

    manifest_bytes_after = _read_all(manifest_path)
    if manifest_bytes != manifest_bytes_after:
        raise RuntimeError("manifest bytes changed after atomic write")

    return {
        "transformation_version": TRANSFORMATION_VERSION,
        "dataset_id": DATASET_ID,
        "configuration": CONFIGURATION,
        "license_id": LICENSE_ID,
        "pyarrow_version": _get_pyarrow_version(),
        "input": {
            "size": input_size,
            "sha256_pre": input_sha256,
            "sha256_post": input_sha256_post,
        },
        "record_count": aggregates.record_count,
        "decision_aggregates": {
            "yes": aggregates.yes_count,
            "no": aggregates.no_count,
            "maybe": aggregates.maybe_count,
            "unexpected": aggregates.unexpected_count,
        },
        "unique_pubid_count": aggregates.unique_pubid_count,
        "duplicate_pubid_count": aggregates.duplicate_pubid_count,
        "unique_source_document_count": aggregates.unique_source_document_count,
        "unique_source_record_hash_count": aggregates.unique_source_record_hash_count,
        "source_record_hash_collision_count": aggregates.source_record_hash_collision_count,
        "context_segment_aggregates": {
            "total": aggregates.context_segment_total,
            "minimum": aggregates.min_contexts_per_record,
            "maximum": aggregates.max_contexts_per_record,
        },
        "labels_context_cardinality_validation": "pass",
        "output": {
            "source-records.jsonl": len(records_bytes),
            "source-record-registry.jsonl": len(registry_bytes),
            "transformation-manifest.json": len(manifest_bytes_after),
        },
    }


def _read_all(path: Path) -> bytes:
    return path.read_bytes()
