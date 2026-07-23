"""Deterministic MESC B0 zero-shot orchestration (private).

B0 is the simplest baseline: one approved student model, zero-shot, no retrieved
evidence, no fine-tuning, no teacher, no Evidence Judge, no specialist board, no
reranker or embedding model, and no model-family combination. The runner is
dependency-injected with a generator, so the full pipeline is exercised with a
deterministic fake and never touches a real model, the network, or training.

The gold decision never enters a prompt and is never passed to the generator. A
reproducible runtime manifest (code commit, immutable revisions, library and
runtime versions, device, dtype) is recorded and its reproducibility-relevant
fields are covered by the canonical run digest. The digest excludes hostnames,
absolute paths, and wall-clock/elapsed time.
"""

from __future__ import annotations

import contextlib
import re
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from medscale.backends.common import BackendError
from medscale.backends.transformers.validation import APPROVED_B0_MODELS, is_commit_sha
from medscale.mesc._pilot_loader import B0InputDataset, B0InputRecord
from medscale.mesc._split_v1 import (
    DECISIONS,
    Decision,
    canonical_json_bytes,
    sha256_hexdigest,
)
from medscale.modelkit.interfaces import GenerationRequest, GenerationResult

__all__ = [
    "B0_EVIDENCE_CONDITION",
    "MANIFEST_PACKAGES",
    "PROMPT_TEMPLATE_VERSION",
    "B0Aggregate",
    "B0Config",
    "B0ConfigError",
    "B0ExampleScore",
    "B0Generator",
    "B0Prediction",
    "B0Report",
    "B0RuntimeManifest",
    "VersionSource",
    "build_b0_prompt",
    "capture_runtime_manifest",
    "parse_b0_output",
    "report_to_document",
    "run_b0",
    "validate_b0_config",
    "write_b0_report",
]

B0_EVIDENCE_CONDITION = "none"
PROMPT_TEMPLATE_VERSION = "mesc-b0-prompt/1"
B0_EXPERIMENT_ID = "mesc-b0"
MANIFEST_PACKAGES: tuple[str, ...] = (
    "medscale",
    "transformers",
    "torch",
    "tokenizers",
    "huggingface-hub",
    "safetensors",
)

_ParseState = str  # one of: "parsed", "unparseable", "ambiguous", "generation_failed"
_WORD = re.compile(r"[a-z]+")
_DECISION_KEYS: tuple[str, ...] = DECISIONS

#: Resolve a distribution name to its installed version string.
VersionSource = Callable[[str], str]


class B0ConfigError(ValueError):
    """Raised when a B0 experiment configuration or manifest is invalid."""


class B0Generator(Protocol):
    """The injected generation contract (matches ``TextGenerator``)."""

    def generate(self, request: GenerationRequest) -> GenerationResult: ...


@dataclass(frozen=True, slots=True)
class B0Config:
    experiment_version: str
    model_id: str
    model_revision: str
    tokenizer_revision: str
    max_new_tokens: int
    seed: int
    experiment_id: str = B0_EXPERIMENT_ID
    prompt_template_version: str = PROMPT_TEMPLATE_VERSION
    evidence_condition: str = B0_EVIDENCE_CONDITION


@dataclass(frozen=True, slots=True)
class B0RuntimeManifest:
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


@dataclass(frozen=True, slots=True)
class B0Prediction:
    example_id: str
    row_ordinal: int
    prompt_sha256: str
    raw_output: str | None
    raw_output_sha256: str | None
    predicted_decision: Decision | None
    parse_state: _ParseState


@dataclass(frozen=True, slots=True)
class B0ExampleScore:
    example_id: str
    gold_decision: Decision
    predicted_decision: Decision | None
    parse_state: _ParseState
    correct: bool


@dataclass(frozen=True, slots=True)
class B0Aggregate:
    total: int
    parsed_count: int
    unparseable_count: int
    ambiguous_count: int
    generation_failed_count: int
    correct_count: int
    predicted_distribution: Mapping[str, int]
    gold_distribution: Mapping[str, int]

    @property
    def accuracy(self) -> float:
        return self.correct_count / self.total if self.total else 0.0

    @property
    def coverage(self) -> float:
        return self.parsed_count / self.total if self.total else 0.0


@dataclass(frozen=True, slots=True)
class B0Report:
    run_id: str
    run_digest: str
    config: B0Config
    manifest: B0RuntimeManifest
    input_sha256: str
    input_size: int
    predictions: tuple[B0Prediction, ...]
    scores: tuple[B0ExampleScore, ...]
    aggregate: B0Aggregate


def _default_package_version(package: str) -> str:
    import importlib.metadata

    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def capture_runtime_manifest(
    *,
    code_commit: str,
    config: B0Config,
    device: str,
    dtype: str,
    quantization: str,
    version_source: VersionSource | None = None,
) -> B0RuntimeManifest:
    """Build the reproducibility manifest, capturing library versions on demand.

    ``code_commit`` must be an explicit full lowercase 40-hex SHA (never inferred
    from a working directory). Library versions are read only when this function
    is called (after the execution boundary), via ``version_source`` so tests can
    inject them without real packages.
    """
    if not is_commit_sha(code_commit):
        raise B0ConfigError(
            f"code_commit must be an explicit full lowercase 40-hex SHA, got {code_commit!r}"
        )
    resolve = version_source if version_source is not None else _default_package_version
    return B0RuntimeManifest(
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
    )


def validate_b0_config(config: B0Config) -> None:
    """Fail closed on any unapproved or nondeterministic B0 configuration."""
    if not isinstance(config.model_id, str) or config.model_id not in APPROVED_B0_MODELS:
        raise B0ConfigError(
            f"model_id must be one of {sorted(APPROVED_B0_MODELS)}, got {config.model_id!r}"
        )
    for value, field in (
        (config.experiment_id, "experiment_id"),
        (config.experiment_version, "experiment_version"),
    ):
        if not isinstance(value, str) or not value.strip():
            raise B0ConfigError(f"{field} must be a non-blank string")
    for value, field in (
        (config.model_revision, "model_revision"),
        (config.tokenizer_revision, "tokenizer_revision"),
    ):
        if not is_commit_sha(value):
            raise B0ConfigError(
                f"{field} must be a full lowercase 40-hex commit SHA, got {value!r}"
            )
    if config.prompt_template_version != PROMPT_TEMPLATE_VERSION:
        raise B0ConfigError(
            f"prompt_template_version must be {PROMPT_TEMPLATE_VERSION!r}, "
            f"got {config.prompt_template_version!r}"
        )
    if config.evidence_condition != B0_EVIDENCE_CONDITION:
        raise B0ConfigError(
            f"B0 evidence_condition must be {B0_EVIDENCE_CONDITION!r}, "
            f"got {config.evidence_condition!r}"
        )
    if not _is_int(config.max_new_tokens) or config.max_new_tokens <= 0:
        raise B0ConfigError(
            f"max_new_tokens must be a positive integer, got {config.max_new_tokens!r}"
        )
    if not _is_int(config.seed) or config.seed < 0:
        raise B0ConfigError(f"seed must be a non-negative integer, got {config.seed!r}")


def _require_manifest_matches_config(config: B0Config, manifest: B0RuntimeManifest) -> None:
    if not is_commit_sha(manifest.code_commit):
        raise B0ConfigError(
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
    )
    for manifest_value, config_value, field in pairs:
        if manifest_value != config_value:
            raise B0ConfigError(
                f"manifest {field} {manifest_value!r} does not match config {config_value!r}"
            )
    if manifest.seed != config.seed:
        raise B0ConfigError(
            f"manifest seed {manifest.seed!r} does not match config {config.seed!r}"
        )


def build_b0_prompt(record: B0InputRecord) -> str:
    """Build the deterministic B0 prompt from permitted fields only.

    Uses the question and context; the gold decision is never referenced.
    """
    context_block = "\n".join(record.context)
    return (
        "Answer the biomedical research question using only the provided context.\n"
        f"Question: {record.question}\n"
        "Context:\n"
        f"{context_block}\n"
        "Respond with exactly one word: yes, no, or maybe.\n"
        "Answer:"
    )


def parse_b0_output(text: str) -> tuple[Decision | None, _ParseState]:
    """Parse exactly one supported decision word; fail deterministically otherwise."""
    tokens = set(_WORD.findall(text.lower()))
    present = [decision for decision in DECISIONS if decision in tokens]
    if len(present) == 1:
        return present[0], "parsed"
    if not present:
        return None, "unparseable"
    return None, "ambiguous"


def run_b0(
    config: B0Config,
    dataset: B0InputDataset,
    generator: B0Generator,
    *,
    manifest: B0RuntimeManifest,
) -> B0Report:
    """Execute B0 zero-shot over the dataset with an injected generator.

    Configuration and manifest are validated before the generator is ever
    invoked. A generation failure is represented deterministically and never
    scored as correct.
    """
    validate_b0_config(config)
    _require_manifest_matches_config(config, manifest)
    predictions: list[B0Prediction] = []
    scores: list[B0ExampleScore] = []
    for record in dataset.records:
        prompt = build_b0_prompt(record)
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
        config, manifest, dataset.input_sha256, dataset.input_size, predictions, aggregate
    )
    run_digest = sha256_hexdigest(canonical)
    return B0Report(
        run_id=f"mesc-b0-run-{run_digest}",
        run_digest=run_digest,
        config=config,
        manifest=manifest,
        input_sha256=dataset.input_sha256,
        input_size=dataset.input_size,
        predictions=tuple(predictions),
        scores=tuple(scores),
        aggregate=aggregate,
    )


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _aggregate(
    predictions: list[B0Prediction],
    scores: list[B0ExampleScore],
) -> B0Aggregate:
    predicted_distribution: dict[str, int] = dict.fromkeys(_DECISION_KEYS, 0)
    for prediction in predictions:
        if prediction.predicted_decision is not None:
            predicted_distribution[prediction.predicted_decision] += 1
    gold_distribution: dict[str, int] = dict.fromkeys(_DECISION_KEYS, 0)
    for score in scores:
        gold_distribution[score.gold_decision] += 1
    return B0Aggregate(
        total=len(scores),
        parsed_count=sum(1 for score in scores if score.parse_state == "parsed"),
        unparseable_count=sum(1 for score in scores if score.parse_state == "unparseable"),
        ambiguous_count=sum(1 for score in scores if score.parse_state == "ambiguous"),
        generation_failed_count=sum(
            1 for score in scores if score.parse_state == "generation_failed"
        ),
        correct_count=sum(1 for score in scores if score.correct),
        predicted_distribution=predicted_distribution,
        gold_distribution=gold_distribution,
    )


def _manifest_payload(manifest: B0RuntimeManifest) -> dict[str, object]:
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
    }


def _canonical_payload(
    config: B0Config,
    manifest: B0RuntimeManifest,
    input_sha256: str,
    input_size: int,
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


def report_to_document(report: B0Report) -> dict[str, object]:
    """Full serializable report: canonical result plus verbose per-example output."""
    canonical = _canonical_payload(
        report.config,
        report.manifest,
        report.input_sha256,
        report.input_size,
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


def write_b0_report(report: B0Report, path: Path) -> None:
    """Atomically write the report; never silently overwrite an existing file.

    Bytes are written to a sibling temporary file, flushed and closed, then
    atomically published with ``Path.replace``. On any failure the temporary file
    is removed and no partial or completed artifact remains.
    """
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
