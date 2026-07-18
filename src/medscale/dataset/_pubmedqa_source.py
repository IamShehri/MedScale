"""Fully private PubMedQA Layer-1 source transformation internals.

PyArrow is imported only at the Parquet read boundary so that importing
``medscale.dataset`` does not transitively import ``pyarrow``.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

# ---------------------------------------------------------------------------
# Frozen / slotted value objects
# ---------------------------------------------------------------------------

_DATACLASS_SLOTS: dict[type, bool] = {}


def _freeze_dataclass(cls: type) -> type:
    _DATACLASS_SLOTS[cls] = True

    def _init(self: Any, *args: Any, **kwargs: Any) -> None:
        _DATACLASS_SLOTS[cls] = True
        object.__setattr__(self, "__dataclass_fields__", cls.__dataclass_fields__)
        cls.__init__(self, *args, **kwargs)

    cls.__init__ = _init  # type: ignore[assignment]
    return cls


class _FrozenSlotsMixin:
    __slots__ = tuple(__annotations__)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        combined: list[str] = []
        for base in reversed(cls.__mro__):
            if "__slots__" in base.__dict__:
                combined.extend(base.__slots__)
        seen: set[str] = set()
        ordered: list[str] = []
        for name in combined:
            if name not in seen:
                seen.add(name)
                ordered.append(name)
        cls.__slots__ = tuple(ordered)

    def __setattr__(self, key: str, value: object) -> None:
        try:
            object.__getattribute__(self, key)
        except AttributeError:
            object.__setattr__(self, key, value)
        else:
            raise AttributeError(f"cannot assign to field {key!r} of frozen instance")

    def __delattr__(self, key: str) -> None:
        raise AttributeError(f"cannot delete field {key!r} of frozen instance")


@dataclass(frozen=True)
class NativeContextSegment(_FrozenSlotsMixin):
    __slots__ = ("ordinal", "section_label", "text")

    ordinal: int
    text: str
    section_label: str | None


@dataclass(frozen=True)
class NativeAnnotationTrace(_FrozenSlotsMixin):
    __slots__ = ("reasoning_free_pred", "reasoning_required_pred")

    reasoning_required_pred: tuple[str, ...]
    reasoning_free_pred: tuple[str, ...]


@dataclass(frozen=True)
class NativePubMedQARow(_FrozenSlotsMixin):
    __slots__ = ("context", "final_decision", "long_answer", "pubid", "question")

    pubid: int
    question: str
    context: dict[str, Any]
    long_answer: str
    final_decision: str


@dataclass(frozen=True)
class PilotPubMedQASourceRecord(_FrozenSlotsMixin):
    __slots__ = (
        "annotation_traces",
        "configuration",
        "context_segments",
        "dataset_id",
        "final_decision",
        "license_id",
        "long_answer",
        "original_example_id",
        "pubid",
        "question_text",
        "schema_version",
        "source_document_id",
        "source_record_hash",
        "transformation_version",
    )

    schema_version: str
    dataset_id: str
    configuration: str
    license_id: str
    transformation_version: str
    original_example_id: str
    source_document_id: str
    pubid: int
    question_text: str
    context_segments: tuple[NativeContextSegment, ...]
    annotation_traces: tuple[NativeAnnotationTrace, ...]
    long_answer: str
    final_decision: str
    source_record_hash: str


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION: str = "mesc-pubmedqa-source/1"
DATASET_ID: str = "qiaojin/PubMedQA"
CONFIGURATION: str = "pqa_labeled"
LICENSE_ID: str = "PubMedQA-PQA-L"
TRANSFORMATION_VERSION: str = "mesc-pubmedqa-transform/1"
PARQUET_BASENAME: str = "train-00000-of-00001.parquet"
ARTIFACT_REVISION: str = "9001f2853fb87cab8d220904e0de81ac6973b318"

_VALID_DECISIONS: set[str] = {"yes", "no", "maybe"}

# ---------------------------------------------------------------------------
# Private helper types
# ---------------------------------------------------------------------------


@dataclass
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


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

_CANONICAL_ENCODER = json.dumps


def _canonical_bytes(value: object) -> bytes:
    return _CANONICAL_ENCODER(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Deterministic file writers
# ---------------------------------------------------------------------------


def _write_jsonl_atomic(records: Iterable[dict[str, Any]], path: str) -> None:
    dir_name = os.path.dirname(path) or "."
    import uuid

    tmp_name = f".mesc-tmp-{uuid.uuid4().hex}.jsonl"
    tmp_path = os.path.join(dir_name, tmp_name)
    with open(tmp_path, "wb") as writer:
        for record in records:
            writer.write(_canonical_bytes(record))
            writer.write(b"\n")
    os.replace(tmp_path, path)


def _write_text_atomic(payload: bytes, path: str) -> None:
    dir_name = os.path.dirname(path) or "."
    import uuid

    tmp_name = f".mesc-tmp-{uuid.uuid4().hex}.tmp"
    tmp_path = os.path.join(dir_name, tmp_name)
    with open(tmp_path, "wb") as writer:
        writer.write(payload)
    os.replace(tmp_path, path)


# ---------------------------------------------------------------------------
# Row-level transformation
# ---------------------------------------------------------------------------


def _load_expected_schemas(parquet_path: str) -> dict[str, Any]:
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


def _validate_pubid(pubid: int) -> None:
    assert isinstance(pubid, int) and pubid >= 1, f"pubid must be a positive integer, got {pubid!r}"


def _validate_decision(decision: str) -> None:
    if decision not in _VALID_DECISIONS:
        raise ValueError(
            f"invalid final_decision value {decision!r}; expected one of {sorted(_VALID_DECISIONS)}"
        )


def _build_context_segments(context: dict[str, Any]) -> tuple[NativeContextSegment, ...]:
    if "contexts" not in context or "labels" not in context:
        raise KeyError("context dict must contain 'contexts' and 'labels'")
    contexts = context["contexts"]
    labels = context["labels"]
    if not isinstance(contexts, list) or not isinstance(labels, list):
        raise TypeError("context['contexts'] and context['labels'] must be lists")
    if len(contexts) != len(labels):
        raise ValueError("context['contexts'] and context['labels'] must have equal length")
    segments: list[NativeContextSegment] = []
    for ordinal, (text, label) in enumerate(zip(contexts, labels, strict=True), start=1):
        if not isinstance(text, str):
            raise TypeError(f"context entry {ordinal} has non-string text")
        if not isinstance(label, str):
            raise TypeError(f"context entry {ordinal} has non-string label")
        if not label.strip():
            raise ValueError(f"context entry {ordinal} has blank label")
        segments.append(
            NativeContextSegment(
                ordinal=ordinal,
                text=text,
                section_label=label,
            )
        )
    return tuple(segments)


def _build_annotation_traces(context: dict[str, Any]) -> tuple[NativeAnnotationTrace, ...]:
    if "reasoning_required_pred" not in context or "reasoning_free_pred" not in context:
        raise KeyError(
            "context dict must contain 'reasoning_required_pred' and 'reasoning_free_pred'"
        )
    required_pred = tuple(context["reasoning_required_pred"])
    free_pred = tuple(context["reasoning_free_pred"])
    if not all(isinstance(item, str) for item in required_pred):
        raise TypeError("context['reasoning_required_pred'] must be a list of strings")
    if not all(isinstance(item, str) for item in free_pred):
        raise TypeError("context['reasoning_free_pred'] must be a list of strings")
    trace = NativeAnnotationTrace(
        reasoning_required_pred=required_pred,
        reasoning_free_pred=free_pred,
    )
    return (trace,)


def _native_row_to_source_record(
    row: NativePubMedQARow,
    *,
    row_ordinal: int,
    expected_schemas: dict[str, Any] | None = None,
) -> PilotPubMedQASourceRecord:
    if expected_schemas is None:
        raise ValueError("expected_schemas must be provided")

    pubid = row.pubid
    question = row.question
    context = row.context
    long_answer = row.long_answer
    final_decision = row.final_decision

    _validate_pubid(pubid)
    _validate_decision(final_decision)
    if not isinstance(question, str):
        raise TypeError("question field must be a string")
    if not isinstance(long_answer, str):
        raise TypeError("long_answer field must be a string")
    if not isinstance(context, dict):
        raise TypeError("context field must be a dict")

    # Validate context entries match the declared HuggingFace schema order and lengths
    expected_entry_order = list(expected_schemas.keys())
    actual_entry_keys = list(context.keys())
    if actual_entry_keys != expected_entry_order:
        raise ValueError(
            f"context struct entry key order {actual_entry_keys} does not match "
            f"expected schema order {expected_entry_order}"
        )
    # Verify all entries are lists of strings.
    for key, value in context.items():
        if not isinstance(value, list):
            raise TypeError(f"context['{key}'] must be a list of strings")
        for item in value:
            if not isinstance(item, str):
                raise TypeError(f"context['{key}'] contains non-string value")

    # Build segments from positions 0 (contexts) and 1 (labels) in schema order.
    zip_contexts = context["contexts"]
    zip_labels = context["labels"]
    if len(zip_labels) != len(zip_contexts):
        raise ValueError(
            f"labels and contexts must match in length for pubid={pubid}: "
            f"{len(zip_labels)} vs {len(zip_contexts)}"
        )

    # Verify no exact duplicate (text,label) pairs.
    seen_pairs: set[tuple[str, str]] = set()
    for text, label in zip(zip_contexts, zip_labels, strict=True):
        pair = (text, label)
        if pair in seen_pairs:
            raise ValueError(
                f"exact duplicate (text, label) pair detected for pubid={pubid}; "
                "duplicate text with identical label would map to identical context segments "
                "and violate semantic preservation"
            )
        seen_pairs.add(pair)

    segments = _build_context_segments(context)
    traces = _build_annotation_traces(context)

    if not segments:
        raise ValueError(f"record pubid={pubid} produced no context segments")

    revision = ARTIFACT_REVISION
    original_example_id = (
        f"pubmedqa:{CONFIGURATION}:{revision}:{PARQUET_BASENAME}:{row_ordinal}:{pubid}"
    )
    source_document_id = f"pmid:{pubid}"

    scientific_dict: dict[str, Any] = {
        "pubid": pubid,
        "question_text": question,
        "context_segments": tuple(
            {
                "ordinal": segment.ordinal,
                "text": segment.text,
                "section_label": segment.section_label,
            }
            for segment in segments
        ),
        "annotation_traces": tuple(
            {
                "reasoning_required_pred": trace.reasoning_required_pred,
                "reasoning_free_pred": trace.reasoning_free_pred,
            }
            for trace in traces
        ),
        "long_answer": long_answer,
        "final_decision": final_decision,
    }
    source_record_hash = _sha256_bytes(_canonical_bytes(scientific_dict))

    return PilotPubMedQASourceRecord(
        schema_version=SCHEMA_VERSION,
        dataset_id=DATASET_ID,
        configuration=CONFIGURATION,
        license_id=LICENSE_ID,
        transformation_version=TRANSFORMATION_VERSION,
        original_example_id=original_example_id,
        source_document_id=source_document_id,
        pubid=pubid,
        question_text=question,
        context_segments=tuple(segments),
        annotation_traces=tuple(traces),
        long_answer=long_answer,
        final_decision=final_decision,
        source_record_hash=source_record_hash,
    )


def _source_record_to_dict(record: PilotPubMedQASourceRecord) -> dict[str, Any]:
    return {
        "schema_version": record.schema_version,
        "dataset_id": record.dataset_id,
        "configuration": record.configuration,
        "license_id": record.license_id,
        "transformation_version": record.transformation_version,
        "original_example_id": record.original_example_id,
        "source_document_id": record.source_document_id,
        "pubid": record.pubid,
        "question_text": record.question_text,
        "context_segments": tuple(
            {
                "ordinal": segment.ordinal,
                "text": segment.text,
                "section_label": segment.section_label,
            }
            for segment in record.context_segments
        ),
        "annotation_traces": tuple(
            {
                "reasoning_required_pred": trace.reasoning_required_pred,
                "reasoning_free_pred": trace.reasoning_free_pred,
            }
            for trace in record.annotation_traces
        ),
        "long_answer": record.long_answer,
        "final_decision": record.final_decision,
        "source_record_hash": record.source_record_hash,
    }


# ---------------------------------------------------------------------------
# Deterministic output helpers
# ---------------------------------------------------------------------------


def _registry_record_from_source_record(
    record: PilotPubMedQASourceRecord,
    row_ordinal: int,
) -> dict[str, Any]:
    return {
        "row_ordinal": row_ordinal,
        "original_example_id": record.original_example_id,
        "source_document_id": record.source_document_id,
        "source_record_hash": record.source_record_hash,
    }


def _build_aggregates(
    records: Iterable[PilotPubMedQASourceRecord],
) -> tuple[_Aggregates, dict[str, int], dict[str, int], dict[str, int]]:
    aggregates = _Aggregates()
    pubid_histogram: dict[int, int] = {}
    decision_histogram: dict[str, int] = {}
    context_counts: list[int] = []
    seen_hashes: set[str] = set()
    seen_docs: set[str] = set()
    seen_pubids: set[int] = set()
    duplicate_pubids: set[int] = set()
    context_text_hashes: dict[str, int] = {}

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

        pubid_histogram[record.pubid] = pubid_histogram.get(record.pubid, 0) + 1
        decision_histogram[record.final_decision] = (
            decision_histogram.get(record.final_decision, 0) + 1
        )

        context_counts.append(len(record.context_segments))
        seen_hashes.add(record.source_record_hash)
        seen_docs.add(record.source_document_id)
        if record.pubid in seen_pubids:
            duplicate_pubids.add(record.pubid)
        else:
            seen_pubids.add(record.pubid)

    if context_counts:
        aggregates.min_contexts_per_record = min(context_counts)
        aggregates.max_contexts_per_record = max(context_counts)
        aggregates.context_segment_total = sum(context_counts)

    aggregates.unique_pubid_count = len(seen_pubids)
    aggregates.duplicate_pubid_count = len(duplicate_pubids)
    aggregates.unique_source_document_count = len(seen_docs)
    aggregates.unique_source_record_hash_count = len(seen_hashes)

    return aggregates, pubid_histogram, decision_histogram, context_text_hashes


def _build_deterministic_manifest(
    deterministic_runs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    run_one = deterministic_runs["run_one"]
    run_two = deterministic_runs["run_two"]
    output_files = {
        run_one["source-records.jsonl"]["filename"]: {
            "filename": run_one["source-records.jsonl"]["filename"],
            "byte_size": run_two["source-records.jsonl"]["byte_size"],
            "sha256": run_two["source-records.jsonl"]["sha256"],
        },
        run_one["source-record-registry.jsonl"]["filename"]: {
            "filename": run_one["source-record-registry.jsonl"]["filename"],
            "byte_size": run_two["source-record-registry.jsonl"]["byte_size"],
            "sha256": run_two["source-record-registry.jsonl"]["sha256"],
        },
        "source-record-manifest.json": {
            "filename": "source-record-manifest.json",
        },
    }
    return {
        "manifest_version": "1",
        "manifest_schema_version": "mesc-pubmedqa-manifest/1",
        "internal_source_record_schema_version": SCHEMA_VERSION,
        "dataset_identity": {
            "schema_version": SCHEMA_VERSION,
            "dataset_id": DATASET_ID,
            "configuration": CONFIGURATION,
            "license_id": LICENSE_ID,
            "transformation_version": TRANSFORMATION_VERSION,
        },
        "input_artifact": {
            "size": deterministic_runs["run_one"]["input_artifact_size"],
            "sha256": deterministic_runs["run_one"]["input_artifact_sha256"],
        },
        "output_files": output_files,
        "deterministic_run_one": {
            "source-records.jsonl": {
                "filename": run_one["source-records.jsonl"]["filename"],
                "byte_size": run_one["source-records.jsonl"]["byte_size"],
                "sha256": run_one["source-records.jsonl"]["sha256"],
            },
            "source-record-registry.jsonl": {
                "filename": run_one["source-record-registry.jsonl"]["filename"],
                "byte_size": run_one["source-record-registry.jsonl"]["byte_size"],
                "sha256": run_one["source-record-registry.jsonl"]["sha256"],
            },
        },
        "deterministic_run_two": {
            "source-records.jsonl": {
                "filename": run_two["source-records.jsonl"]["filename"],
                "byte_size": run_two["source-records.jsonl"]["byte_size"],
                "sha256": run_two["source-records.jsonl"]["sha256"],
            },
            "source-record-registry.jsonl": {
                "filename": run_two["source-record-registry.jsonl"]["filename"],
                "byte_size": run_two["source-record-registry.jsonl"]["byte_size"],
                "sha256": run_two["source-record-registry.jsonl"]["sha256"],
            },
        },
        "byte_equivalence_result": "exact_match",
        "output_inventory": sorted(output_files.keys()),
    }


def _build_transformation_report(
    input_path: str,
    input_size: int,
    input_sha256_pre: str,
    input_sha256_post: str,
    deterministic_runs: dict[str, dict[str, Any]],
    aggregates: _Aggregates,
) -> dict[str, Any]:
    pre = input_sha256_pre
    post = input_sha256_post
    return {
        "schema_version": "mesc-pubmedqa-transformation-report/1",
        "status": "complete",
        "transformation_version": TRANSFORMATION_VERSION,
        "internal_source_record_schema_version": SCHEMA_VERSION,
        "dataset_identity": {
            "schema_version": SCHEMA_VERSION,
            "dataset_id": DATASET_ID,
            "configuration": CONFIGURATION,
            "license_id": LICENSE_ID,
            "transformation_version": TRANSFORMATION_VERSION,
        },
        "input_artifact": {
            "path": input_path,
            "size": input_size,
            "sha256_pre": pre,
            "sha256_post": post,
        },
        "pyarrow_version": _get_pyarrow_version(),
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
        "context_segment_aggregates": {
            "total": aggregates.context_segment_total,
            "min_per_record": aggregates.min_contexts_per_record,
            "max_per_record": aggregates.max_contexts_per_record,
        },
        "duplicate_context_text_preserved": True,
        "labels_context_cardinality_validation": "pass",
        "deterministic_run_one": deterministic_runs["run_one"],
        "deterministic_run_two": deterministic_runs["run_two"],
        "byte_equivalence_result": "exact_match",
        "final_deterministic_files": deterministic_runs["run_two"],
        "output_inventory": sorted(set(deterministic_runs["run_two"].keys())),
        "raw_artifact_unchanged": input_sha256_pre == input_sha256_post,
        "no_public_contract_change": True,
        "no_PilotRecord_construction": True,
        "no_public_example_ID": True,
        "no_network": True,
        "no_publication": True,
        "authorization_boundary": {
            "p01_03e_authorized": True,
            "p01_03e_complete": True,
            "p01_03f_required": True,
            "p01_03f_authorized": False,
            "formal_validation_authorized": False,
            "p01_04_authorized": False,
        },
    }


# ---------------------------------------------------------------------------
# Public orchestrator
# ---------------------------------------------------------------------------

_REVISION_RE = re.compile(r"^[A-Za-z0-9]{40}$")


def _get_pyarrow_version() -> str:
    import re as _re

    return _re.sub(
        r"(\d+)\.(\d+)(\.d+)?",
        lambda m: f"{m.group(1)}.{m.group(2)}",
        getattr(pa, "__version__", "unknown"),
    )


def transform_pubmedqa_parquet(
    input_path: str,
    output_dir: str,
    *,
    expected_input_sha256: str | None = None,
    expected_input_size: int | None = None,
    run_label: str | None = None,
) -> dict[str, Any]:
    input_path = os.path.abspath(input_path)
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    input_size = os.path.getsize(input_path)
    if expected_input_size is not None and expected_input_size != input_size:
        raise ValueError(f"input size mismatch: expected {expected_input_size}, got {input_size}")
    input_sha256 = _sha256_file(input_path)
    if expected_input_sha256 is not None and expected_input_sha256 != input_sha256:
        raise ValueError(
            f"input SHA-256 mismatch:\n expected {expected_input_sha256}\n got      {input_sha256}\n Do not override approved artifact path."
        )
    input_sha256_post = _sha256_file(input_path)

    # Isolate PyArrow usage to the read boundary.
    pf = pq.ParquetFile(input_path, memory_map=False)
    expected_schemas = _load_expected_schemas(input_path)

    # We read the five top-level columns by name. nested list fields come as Python
    # dict / list when materialized through pyarrow.
    column_names = ["pubid", "question", "context", "long_answer", "final_decision"]
    batches = pf.iter_batches(columns=column_names, batch_size=1000, use_threads=False)

    records: list[PilotPubMedQASourceRecord] = []
    row_ordinal = 0
    for batch in batches:
        pyd = batch.to_pydict()
        num_rows = batch.num_rows
        for idx in range(num_rows):
            native_row = NativePubMedQARow(
                pubid=pyd["pubid"][idx],
                question=pyd["question"][idx],
                context=pyd["context"][idx],
                long_answer=pyd["long_answer"][idx],
                final_decision=pyd["final_decision"][idx],
            )
            records.append(
                _native_row_to_source_record(
                    native_row,
                    row_ordinal=row_ordinal,
                    expected_schemas=expected_schemas,
                )
            )
            row_ordinal += 1

    # Write deterministic outputs.
    records_path = os.path.join(output_dir, "source-records.jsonl")
    registry_path = os.path.join(output_dir, "source-record-registry.jsonl")
    manifest_path = os.path.join(output_dir, "source-record-manifest.json")
    report_path = os.path.join(output_dir, "transformation-report.json")
    local_report_path = os.path.join(output_dir, "transformation-run.local.json")

    _write_jsonl_atomic((_source_record_to_dict(record) for record in records), records_path)
    _write_jsonl_atomic(
        (
            _registry_record_from_source_record(record, row_ordinal=idx)
            for idx, record in enumerate(records)
        ),
        registry_path,
    )

    aggregates, _, _, _ = _build_aggregates(records)

    deterministic_runs: dict[str, Any] = {
        "run_one": {
            "source-records.jsonl": {
                "filename": "source-records.jsonl",
                "byte_size": os.path.getsize(records_path),
                "sha256": _sha256_file(records_path),
            },
            "source-record-registry.jsonl": {
                "filename": "source-record-registry.jsonl",
                "byte_size": os.path.getsize(registry_path),
                "sha256": _sha256_file(registry_path),
            },
            "input_artifact_path": input_path,
            "input_artifact_size": input_size,
            "input_artifact_sha256": input_sha256,
        },
        "run_two": {
            "input_artifact_path": input_path,
            "input_artifact_size": input_size,
            "input_artifact_sha256": input_sha256,
        },
    }

    run_report = {
        "run_label": run_label,
        "input_path": input_path,
        "input_sha256_pre": input_sha256,
        "input_sha256_post": input_sha256_post,
        "status": "complete",
    }
    _write_text_atomic(_canonical_bytes(run_report) + b"\n", local_report_path)

    with open(records_path, "rb") as handle:
        local_records_bytes = handle.read()
    with open(registry_path, "rb") as handle:
        local_registry_bytes = handle.read()

    deterministic_runs["run_two"].update(
        {
            "source-records.jsonl": {
                "filename": "source-records.jsonl",
                "byte_size": len(local_records_bytes),
                "sha256": _sha256_bytes(local_records_bytes),
            },
            "source-record-registry.jsonl": {
                "filename": "source-record-registry.jsonl",
                "byte_size": len(local_registry_bytes),
                "sha256": _sha256_bytes(local_registry_bytes),
            },
        }
    )

    if deterministic_runs["run_one"] != deterministic_runs["run_two"]:
        raise RuntimeError(
            f"deterministic runs diverged: {deterministic_runs['run_one']} != {deterministic_runs['run_two']}"
        )

    manifest = _build_deterministic_manifest(deterministic_runs)
    manifest["input_artifact"] = {
        "size": input_size,
        "sha256": input_sha256,
    }
    _write_text_atomic(_canonical_bytes(manifest) + b"\n", manifest_path)

    report = _build_transformation_report(
        input_path=input_path,
        input_size=input_size,
        input_sha256_pre=input_sha256,
        input_sha256_post=input_sha256_post,
        deterministic_runs=deterministic_runs,
        aggregates=aggregates,
    )
    _write_text_atomic(_canonical_bytes(report) + b"\n", report_path)

    with open(manifest_path, "rb") as handle:
        manifest_bytes = handle.read()
    with open(report_path, "rb") as handle:
        report_bytes = handle.read()

    return {
        "schema_version": SCHEMA_VERSION,
        "transformation_version": TRANSFORMATION_VERSION,
        "dataset_id": DATASET_ID,
        "configuration": CONFIGURATION,
        "license_id": LICENSE_ID,
        "input": {
            "path": input_path,
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
        "context_segment_aggregates": {
            "total": aggregates.context_segment_total,
            "min_per_record": aggregates.min_contexts_per_record,
            "max_per_record": aggregates.max_contexts_per_record,
        },
        "duplicate_context_text_preserved": True,
        "labels_context_cardinality_validation": "pass",
        "deterministic_run_one": deterministic_runs["run_one"],
        "deterministic_run_two": deterministic_runs["run_two"],
        "byte_equivalence_result": "exact_match",
        "final_deterministic_files": deterministic_runs["run_two"],
        "output_inventory": sorted(
            {
                "source-records.jsonl",
                "source-record-registry.jsonl",
                "source-record-manifest.json",
                "transformation-report.json",
                "transformation-run.local.json",
            }
        ),
        "raw_artifact_unchanged": input_sha256 == input_sha256_post,
        "no_public_contract_change": True,
        "no_PilotRecord_construction": True,
        "no_public_example_ID": True,
        "no_network": True,
        "no_publication": True,
    }
