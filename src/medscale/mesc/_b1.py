"""Deterministic MESC B1 manually evidence-cued baseline orchestration (private).

B1 is the smallest safe extension of the existing B0 architecture
(FD-P01-05-B1-EVIDENCE-1). It keeps the exact B0 scientific input — question
plus complete native context — and adds an explicit supplied-evidence cue
channel. The cue references native context segments only; there is no
retrieval, no external corpus, no teacher model, and no LLM-generated evidence
in B1.

Like B0, the runner is dependency-injected with a generator and is exercised
only with deterministic fakes. The gold decision never enters a prompt and is
never passed to the generator. Evidence-layer failures happen BEFORE generator
invocation and are represented as typed errors, never as model output states.
"""

from __future__ import annotations

import contextlib
import re
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from medscale.backends.common import BackendError
from medscale.backends.transformers.validation import APPROVED_B0_MODELS, is_commit_sha
from medscale.mesc._b0 import (
    B0Aggregate,
    B0ExampleScore,
    B0Generator,
    B0Prediction,
    _aggregate,
    _default_package_version,
    parse_b0_output,
)
from medscale.mesc._b1_evidence import (
    ANNOTATION_PROTOCOL_VERSION,
    EVIDENCE_PACK_SCHEMA_VERSION,
    B1EvidenceCue,
    B1EvidencePack,
    validate_evidence_cue,
    validate_evidence_pack,
)
from medscale.mesc._pilot_loader import B0InputDataset, B0InputRecord
from medscale.mesc._split_v1 import canonical_json_bytes, sha256_hexdigest
from medscale.modelkit.interfaces import GenerationRequest

__all__ = [
    "B1_EVIDENCE_CONDITION",
    "B1_EXPERIMENT_ID",
    "B1_PROMPT_TEMPLATE_VERSION",
    "B1Config",
    "B1ConfigError",
    "B1EvidenceJoinError",
    "B1Report",
    "B1RuntimeManifest",
    "build_b1_prompt",
    "capture_b1_runtime_manifest",
    "join_b1_inputs",
    "report_to_document",
    "run_b1",
    "validate_b1_config",
    "write_b1_report",
]

B1_EVIDENCE_CONDITION = "manual_native_context_cues"
B1_PROMPT_TEMPLATE_VERSION = "mesc-b1-prompt/1"
B1_EXPERIMENT_ID = "mesc-b1"

_HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class B1ConfigError(ValueError):
    """Raised when a B1 experiment configuration or manifest is invalid."""


class B1EvidenceJoinError(B1ConfigError):
    """Raised when the model input and the evidence pack cannot be joined exactly."""


@dataclass(frozen=True, slots=True)
class B1Config:
    """Deterministic B1 configuration with run-level evidence-pack identity.

    Because a B1 run consumes a multi-example evidence pack, the evidence
    identity is a run-level pack identity, not a singular per-example object.
    """

    experiment_version: str
    model_id: str
    model_revision: str
    tokenizer_revision: str
    max_new_tokens: int
    seed: int
    evidence_pack_sha256: str
    evidence_pack_size: int
    subset_digest: str
    experiment_id: str = B1_EXPERIMENT_ID
    prompt_template_version: str = B1_PROMPT_TEMPLATE_VERSION
    evidence_condition: str = B1_EVIDENCE_CONDITION
    evidence_schema_version: str = EVIDENCE_PACK_SCHEMA_VERSION
    annotation_protocol_version: str = ANNOTATION_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True)
class B1RuntimeManifest:
    """Reproducibility manifest; every field below enters the canonical digest."""

    code_commit: str
    python_version: str
    medscale_version: str
    transformers_version: str
    torch_version: str
    tokenizers_version: str
    huggingface_hub_version: str
    safetensors_version: str
    model_revision: str
    tokenizer_revision: str
    device: str
    dtype: str
    quantization: str
    seed: int
    prompt_template_version: str
    evidence_condition: str
    evidence_pack_sha256: str
    evidence_pack_size: int
    evidence_schema_version: str
    annotation_protocol_version: str
    subset_digest: str


@dataclass(frozen=True, slots=True)
class B1Report:
    """Full B1 run output; reuses the B0 prediction/score/aggregate shapes."""

    run_id: str
    run_digest: str
    config: B1Config
    manifest: B1RuntimeManifest
    input_sha256: str
    input_size: int
    evidence_pack_sha256: str
    evidence_pack_size: int
    subset_digest: str
    predictions: tuple[B0Prediction, ...]
    scores: tuple[B0ExampleScore, ...]
    aggregate: B0Aggregate


def validate_b1_config(config: B1Config) -> None:
    """Fail closed on any unapproved or nondeterministic B1 configuration."""
    if not isinstance(config.model_id, str) or config.model_id not in APPROVED_B0_MODELS:
        raise B1ConfigError(
            f"model_id must be one of {sorted(APPROVED_B0_MODELS)}, got {config.model_id!r}"
        )
    for value, field in (
        (config.experiment_id, "experiment_id"),
        (config.experiment_version, "experiment_version"),
    ):
        if not isinstance(value, str) or not value.strip():
            raise B1ConfigError(f"{field} must be a non-blank string")
    if config.experiment_id != B1_EXPERIMENT_ID:
        raise B1ConfigError(
            f"B1 experiment_id must be {B1_EXPERIMENT_ID!r}, got {config.experiment_id!r}"
        )
    for value, field in (
        (config.model_revision, "model_revision"),
        (config.tokenizer_revision, "tokenizer_revision"),
    ):
        if not is_commit_sha(value):
            raise B1ConfigError(
                f"{field} must be a full lowercase 40-hex commit SHA, got {value!r}"
            )
    if config.prompt_template_version != B1_PROMPT_TEMPLATE_VERSION:
        raise B1ConfigError(
            f"prompt_template_version must be {B1_PROMPT_TEMPLATE_VERSION!r}, "
            f"got {config.prompt_template_version!r}"
        )
    if config.evidence_condition != B1_EVIDENCE_CONDITION:
        raise B1ConfigError(
            f"B1 evidence_condition must be {B1_EVIDENCE_CONDITION!r}, "
            f"got {config.evidence_condition!r}"
        )
    if config.evidence_schema_version != EVIDENCE_PACK_SCHEMA_VERSION:
        raise B1ConfigError(
            f"evidence_schema_version must be {EVIDENCE_PACK_SCHEMA_VERSION!r}, "
            f"got {config.evidence_schema_version!r}"
        )
    if config.annotation_protocol_version != ANNOTATION_PROTOCOL_VERSION:
        raise B1ConfigError(
            f"annotation_protocol_version must be {ANNOTATION_PROTOCOL_VERSION!r}, "
            f"got {config.annotation_protocol_version!r}"
        )
    if not _is_hex64(config.evidence_pack_sha256):
        raise B1ConfigError(
            "evidence_pack_sha256 must be a full lowercase 64-hex SHA-256, "
            f"got {config.evidence_pack_sha256!r}"
        )
    if not _is_int(config.evidence_pack_size) or config.evidence_pack_size <= 0:
        raise B1ConfigError(
            f"evidence_pack_size must be a positive integer, got {config.evidence_pack_size!r}"
        )
    if not _is_hex64(config.subset_digest):
        raise B1ConfigError(
            f"subset_digest must be a full lowercase 64-hex SHA-256, got {config.subset_digest!r}"
        )
    if not _is_int(config.max_new_tokens) or config.max_new_tokens <= 0:
        raise B1ConfigError(
            f"max_new_tokens must be a positive integer, got {config.max_new_tokens!r}"
        )
    if not _is_int(config.seed) or config.seed < 0:
        raise B1ConfigError(f"seed must be a non-negative integer, got {config.seed!r}")


def capture_b1_runtime_manifest(
    *,
    code_commit: str,
    config: B1Config,
    device: str,
    dtype: str,
    quantization: str,
    version_source: Callable[[str], str] | None = None,
) -> B1RuntimeManifest:
    """Build the B1 reproducibility manifest, capturing library versions on demand."""
    if not is_commit_sha(code_commit):
        raise B1ConfigError(
            f"code_commit must be an explicit full lowercase 40-hex SHA, got {code_commit!r}"
        )
    resolve = version_source if version_source is not None else _default_package_version
    return B1RuntimeManifest(
        code_commit=code_commit,
        python_version=".".join(str(part) for part in sys.version_info[:3]),
        medscale_version=resolve("medscale"),
        transformers_version=resolve("transformers"),
        torch_version=resolve("torch"),
        tokenizers_version=resolve("tokenizers"),
        huggingface_hub_version=resolve("huggingface-hub"),
        safetensors_version=resolve("safetensors"),
        model_revision=config.model_revision,
        tokenizer_revision=config.tokenizer_revision,
        device=device,
        dtype=dtype,
        quantization=quantization,
        seed=config.seed,
        prompt_template_version=config.prompt_template_version,
        evidence_condition=config.evidence_condition,
        evidence_pack_sha256=config.evidence_pack_sha256,
        evidence_pack_size=config.evidence_pack_size,
        evidence_schema_version=config.evidence_schema_version,
        annotation_protocol_version=config.annotation_protocol_version,
        subset_digest=config.subset_digest,
    )


def _require_manifest_matches_config(config: B1Config, manifest: B1RuntimeManifest) -> None:
    if not is_commit_sha(manifest.code_commit):
        raise B1ConfigError(
            "manifest code_commit must be a full lowercase 40-hex SHA, "
            f"got {manifest.code_commit!r}"
        )
    pairs = (
        (manifest.model_revision, config.model_revision, "model_revision"),
        (manifest.tokenizer_revision, config.tokenizer_revision, "tokenizer_revision"),
        (
            manifest.prompt_template_version,
            config.prompt_template_version,
            "prompt_template_version",
        ),
        (manifest.evidence_condition, config.evidence_condition, "evidence_condition"),
        (
            manifest.evidence_schema_version,
            config.evidence_schema_version,
            "evidence_schema_version",
        ),
        (
            manifest.annotation_protocol_version,
            config.annotation_protocol_version,
            "annotation_protocol_version",
        ),
        (manifest.evidence_pack_sha256, config.evidence_pack_sha256, "evidence_pack_sha256"),
        (manifest.subset_digest, config.subset_digest, "subset_digest"),
    )
    for manifest_value, config_value, field in pairs:
        if manifest_value != config_value:
            raise B1ConfigError(
                f"manifest {field} {manifest_value!r} does not match config {config_value!r}"
            )
    if manifest.seed != config.seed:
        raise B1ConfigError(
            f"manifest seed {manifest.seed!r} does not match config {config.seed!r}"
        )
    if manifest.evidence_pack_size != config.evidence_pack_size:
        raise B1ConfigError(
            f"manifest evidence_pack_size {manifest.evidence_pack_size!r} "
            f"does not match config {config.evidence_pack_size!r}"
        )


def _require_pack_matches_config(config: B1Config, pack: B1EvidencePack) -> None:
    if pack.schema_version != config.evidence_schema_version:
        raise B1ConfigError(
            f"pack schema_version {pack.schema_version!r} does not match "
            f"config evidence_schema_version {config.evidence_schema_version!r}"
        )
    if pack.annotation_protocol_version != config.annotation_protocol_version:
        raise B1ConfigError(
            f"pack annotation_protocol_version {pack.annotation_protocol_version!r} "
            f"does not match config annotation_protocol_version "
            f"{config.annotation_protocol_version!r}"
        )
    if pack.pack_sha256 != config.evidence_pack_sha256:
        raise B1ConfigError(
            f"pack SHA-256 {pack.pack_sha256!r} does not match config "
            f"evidence_pack_sha256 {config.evidence_pack_sha256!r}"
        )
    if pack.record_count != config.evidence_pack_size:
        raise B1ConfigError(
            f"pack record_count {pack.record_count} does not match config "
            f"evidence_pack_size {config.evidence_pack_size}"
        )
    if pack.subset_digest != config.subset_digest:
        raise B1ConfigError(
            f"pack subset_digest {pack.subset_digest!r} does not match config "
            f"subset_digest {config.subset_digest!r}"
        )


def build_b1_prompt(record: B0InputRecord, cue: B1EvidenceCue) -> str:
    """Build the deterministic B1 prompt: B0 input plus the evidence-cue block.

    The cue is validated against the record's native context before any prompt
    byte is produced; a hash mismatch or any other cue defect fails closed.
    Segment text is included verbatim, in canonical segment-index order, and is
    never rewritten, summarized, paraphrased, expanded, or retrieved.
    """
    validate_evidence_cue(cue, record.context)
    context_block = "\n".join(record.context)
    base = (
        "Answer the biomedical research question using only the provided context.\n"
        f"Question: {record.question}\n"
        "Context:\n"
        f"{context_block}\n"
    )
    if cue.annotation_status == "AVAILABLE":
        segments = "\n".join(
            record.context[reference.context_segment_index]
            for reference in cue.ordered_segment_references
        )
        cue_block = (
            f"Supplied evidence cue status: AVAILABLE\nSupplied evidence segments:\n{segments}\n"
        )
    elif cue.annotation_status == "INSUFFICIENT":
        cue_block = "Supplied evidence cue status: INSUFFICIENT\n"
    else:
        cue_block = "Supplied evidence cue status: AMBIGUOUS\n"
    return base + cue_block + "Respond with exactly one word: yes, no, or maybe.\n" + "Answer:"


def join_b1_inputs(
    dataset: B0InputDataset, cues: Sequence[B1EvidenceCue]
) -> tuple[B1EvidenceCue, ...]:
    """Exact deterministic join: one model input example <-> one final cue.

    Rejects missing cues, extra cues, duplicate cues, wrong example, wrong
    document, unreviewed cues, and segment hash mismatches. Never silently
    falls back to B0.
    """
    by_key: dict[tuple[str, str], B1EvidenceCue] = {}
    for cue in cues:
        key = (cue.example_id, cue.source_document_id)
        if key in by_key:
            raise B1EvidenceJoinError(
                f"duplicate cue for ({cue.example_id}, {cue.source_document_id})"
            )
        by_key[key] = cue
    ordered: list[B1EvidenceCue] = []
    for record in dataset.records:
        key = (record.example_id, record.source_document_id)
        matched = by_key.get(key)
        if matched is None:
            raise B1EvidenceJoinError(
                f"missing evidence cue for example {record.example_id!r} "
                f"document {record.source_document_id!r}"
            )
        validate_evidence_cue(matched, record.context)
        ordered.append(matched)
    if len(ordered) != len(cues):
        raise B1EvidenceJoinError(
            "evidence cues not consumed by the input join: "
            f"input examples={len(ordered)}, cues={len(cues)}"
        )
    return tuple(ordered)


def run_b1(
    config: B1Config,
    dataset: B0InputDataset,
    pack: B1EvidencePack,
    generator: B0Generator,
    *,
    manifest: B1RuntimeManifest,
) -> B1Report:
    """Execute B1 over the dataset with an injected generator.

    Configuration, manifest, pack identity, and every cue are validated before
    the generator is ever invoked. Evidence-layer failures raise typed errors
    and never become model/output parse states.
    """
    validate_b1_config(config)
    _require_manifest_matches_config(config, manifest)
    _require_pack_matches_config(config, pack)
    contexts: dict[tuple[str, str], tuple[str, ...]] = {
        (record.example_id, record.source_document_id): record.context for record in dataset.records
    }
    validate_evidence_pack(pack, contexts)
    ordered_cues = join_b1_inputs(dataset, pack.cues)

    predictions: list[B0Prediction] = []
    scores: list[B0ExampleScore] = []
    for record, cue in zip(dataset.records, ordered_cues, strict=True):
        prompt = build_b1_prompt(record, cue)
        prompt_sha256 = sha256_hexdigest(prompt)
        request = GenerationRequest(
            prompt=prompt, seed=config.seed, max_new_tokens=config.max_new_tokens
        )
        try:
            result = generator.generate(request)
        except BackendError:
            predictions.append(
                B0Prediction(
                    example_id=record.example_id,
                    row_ordinal=record.row_ordinal,
                    prompt_sha256=prompt_sha256,
                    raw_output=None,
                    raw_output_sha256=None,
                    predicted_decision=None,
                    parse_state="generation_failed",
                )
            )
            scores.append(
                B0ExampleScore(
                    example_id=record.example_id,
                    gold_decision=record.gold_decision,
                    predicted_decision=None,
                    parse_state="generation_failed",
                    correct=False,
                )
            )
            continue
        raw = result.text
        decision, state = parse_b0_output(raw)
        predictions.append(
            B0Prediction(
                example_id=record.example_id,
                row_ordinal=record.row_ordinal,
                prompt_sha256=prompt_sha256,
                raw_output=raw,
                raw_output_sha256=sha256_hexdigest(raw),
                predicted_decision=decision,
                parse_state=state,
            )
        )
        scores.append(
            B0ExampleScore(
                example_id=record.example_id,
                gold_decision=record.gold_decision,
                predicted_decision=decision,
                parse_state=state,
                correct=state == "parsed" and decision == record.gold_decision,
            )
        )
    aggregate = _aggregate(predictions, scores)
    canonical = _canonical_payload(
        config,
        manifest,
        dataset.input_sha256,
        dataset.input_size,
        pack.pack_sha256,
        pack.record_count,
        pack.subset_digest,
        predictions,
        aggregate,
    )
    run_digest = sha256_hexdigest(canonical)
    return B1Report(
        run_id=f"mesc-b1-run-{run_digest}",
        run_digest=run_digest,
        config=config,
        manifest=manifest,
        input_sha256=dataset.input_sha256,
        input_size=dataset.input_size,
        evidence_pack_sha256=pack.pack_sha256,
        evidence_pack_size=pack.record_count,
        subset_digest=pack.subset_digest,
        predictions=tuple(predictions),
        scores=tuple(scores),
        aggregate=aggregate,
    )


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_hex64(value: object) -> bool:
    return isinstance(value, str) and bool(_HEX_SHA256.match(value))


def _manifest_payload(manifest: B1RuntimeManifest) -> dict[str, object]:
    return {
        "code_commit": manifest.code_commit,
        "python_version": manifest.python_version,
        "medscale_version": manifest.medscale_version,
        "transformers_version": manifest.transformers_version,
        "torch_version": manifest.torch_version,
        "tokenizers_version": manifest.tokenizers_version,
        "huggingface_hub_version": manifest.huggingface_hub_version,
        "safetensors_version": manifest.safetensors_version,
        "model_revision": manifest.model_revision,
        "tokenizer_revision": manifest.tokenizer_revision,
        "device": manifest.device,
        "dtype": manifest.dtype,
        "quantization": manifest.quantization,
        "seed": manifest.seed,
        "prompt_template_version": manifest.prompt_template_version,
        "evidence_condition": manifest.evidence_condition,
        "evidence_pack_sha256": manifest.evidence_pack_sha256,
        "evidence_pack_size": manifest.evidence_pack_size,
        "evidence_schema_version": manifest.evidence_schema_version,
        "annotation_protocol_version": manifest.annotation_protocol_version,
        "subset_digest": manifest.subset_digest,
    }


def _canonical_payload(
    config: B1Config,
    manifest: B1RuntimeManifest,
    input_sha256: str,
    input_size: int,
    evidence_pack_sha256: str,
    evidence_pack_size: int,
    subset_digest: str,
    predictions: list[B0Prediction],
    aggregate: B0Aggregate,
) -> dict[str, object]:
    return {
        "experiment_id": config.experiment_id,
        "experiment_version": config.experiment_version,
        "model_id": config.model_id,
        "max_new_tokens": config.max_new_tokens,
        "input_sha256": input_sha256,
        "input_size": input_size,
        "evidence_pack_sha256": evidence_pack_sha256,
        "evidence_pack_size": evidence_pack_size,
        "subset_digest": subset_digest,
        "manifest": _manifest_payload(manifest),
        "predictions": [
            {
                "example_id": prediction.example_id,
                "row_ordinal": prediction.row_ordinal,
                "prompt_sha256": prediction.prompt_sha256,
                "raw_output_sha256": prediction.raw_output_sha256,
                "predicted_decision": prediction.predicted_decision,
                "parse_state": prediction.parse_state,
            }
            for prediction in sorted(predictions, key=lambda item: item.row_ordinal)
        ],
        "aggregate": {
            "total": aggregate.total,
            "parsed_count": aggregate.parsed_count,
            "unparseable_count": aggregate.unparseable_count,
            "ambiguous_count": aggregate.ambiguous_count,
            "generation_failed_count": aggregate.generation_failed_count,
            "correct_count": aggregate.correct_count,
            "predicted_distribution": dict(aggregate.predicted_distribution),
            "gold_distribution": dict(aggregate.gold_distribution),
        },
    }


def report_to_document(report: B1Report) -> dict[str, object]:
    """Full serializable B1 report: canonical result plus verbose per-example output.

    Raw prompts are never persisted; only prompt hashes are recorded.
    """
    canonical = _canonical_payload(
        report.config,
        report.manifest,
        report.input_sha256,
        report.input_size,
        report.evidence_pack_sha256,
        report.evidence_pack_size,
        report.subset_digest,
        list(report.predictions),
        report.aggregate,
    )
    return {
        "run_id": report.run_id,
        "run_digest": report.run_digest,
        "canonical": canonical,
        "predictions_verbose": [
            {
                "example_id": prediction.example_id,
                "row_ordinal": prediction.row_ordinal,
                "predicted_decision": prediction.predicted_decision,
                "parse_state": prediction.parse_state,
                "raw_output": prediction.raw_output,
            }
            for prediction in report.predictions
        ],
    }


def write_b1_report(report: B1Report, path: Path) -> None:
    """Atomically write the B1 report; never silently overwrite an existing file."""
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {path}")
    data = canonical_json_bytes(report_to_document(report)) + b"\n"
    tmp = path.with_name(path.name + ".partial")
    published = False
    try:
        with tmp.open("wb") as handle:
            handle.write(data)
            handle.flush()
        tmp.replace(path)
        published = True
    finally:
        if not published:
            with contextlib.suppress(FileNotFoundError):
                tmp.unlink()
