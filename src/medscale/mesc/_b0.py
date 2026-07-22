"""Deterministic MESC B0 zero-shot orchestration (private).

B0 is the simplest baseline: one approved student model, zero-shot, no retrieved
evidence, no fine-tuning, no teacher, no Evidence Judge, no specialist board, no
reranker or embedding model, and no model-family combination. The runner is
dependency-injected with a generator, so the full pipeline is exercised with a
deterministic fake and never touches a real model, the network, or training.

The gold decision never enters a prompt and is never passed to the generator.
Canonical result bytes and the run digest exclude timestamps, elapsed time,
machine paths, hostnames, and any nondeterministic ordering.
"""

from __future__ import annotations

import platform
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from medscale.backends.common import BackendError
from medscale.backends.transformers.validation import APPROVED_B0_MODELS
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
    "PROMPT_TEMPLATE_VERSION",
    "B0Aggregate",
    "B0Config",
    "B0ConfigError",
    "B0Environment",
    "B0ExampleScore",
    "B0Generator",
    "B0Prediction",
    "B0Report",
    "build_b0_prompt",
    "parse_b0_output",
    "report_to_document",
    "run_b0",
    "validate_b0_config",
    "write_b0_report",
]

B0_EVIDENCE_CONDITION = "none"
PROMPT_TEMPLATE_VERSION = "mesc-b0-prompt/1"
B0_EXPERIMENT_ID = "mesc-b0"

_ParseState = str  # one of: "parsed", "unparseable", "ambiguous", "generation_failed"
_WORD = re.compile(r"[a-z]+")
_DECISION_KEYS: tuple[str, ...] = DECISIONS


class B0ConfigError(ValueError):
    """Raised when a B0 experiment configuration is invalid."""


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
class B0Environment:
    """Non-canonical reproducibility metadata; never part of the run digest."""

    python_version: str
    python_implementation: str
    code_commit: str | None = None

    @classmethod
    def capture(cls, *, code_commit: str | None = None) -> B0Environment:
        return cls(
            python_version=".".join(str(part) for part in sys.version_info[:3]),
            python_implementation=platform.python_implementation(),
            code_commit=code_commit,
        )


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
    input_sha256: str
    input_size: int
    predictions: tuple[B0Prediction, ...]
    scores: tuple[B0ExampleScore, ...]
    aggregate: B0Aggregate
    environment: B0Environment


def validate_b0_config(config: B0Config) -> None:
    """Fail closed on any unapproved or nondeterministic B0 configuration."""
    if not isinstance(config.model_id, str) or config.model_id not in APPROVED_B0_MODELS:
        raise B0ConfigError(
            f"model_id must be one of {sorted(APPROVED_B0_MODELS)}, got {config.model_id!r}"
        )
    for value, field in (
        (config.experiment_id, "experiment_id"),
        (config.experiment_version, "experiment_version"),
        (config.model_revision, "model_revision"),
        (config.tokenizer_revision, "tokenizer_revision"),
    ):
        if not isinstance(value, str) or not value.strip():
            raise B0ConfigError(f"{field} must be a non-blank string")
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
    environment: B0Environment | None = None,
) -> B0Report:
    """Execute B0 zero-shot over the dataset with an injected generator.

    Configuration is validated before the generator is ever invoked. A generation
    failure is represented deterministically and never scored as correct.
    """
    validate_b0_config(config)
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
        config, dataset.input_sha256, dataset.input_size, predictions, aggregate
    )
    run_digest = sha256_hexdigest(canonical)
    return B0Report(
        run_id=f"mesc-b0-run-{run_digest}",
        run_digest=run_digest,
        config=config,
        input_sha256=dataset.input_sha256,
        input_size=dataset.input_size,
        predictions=tuple(predictions),
        scores=tuple(scores),
        aggregate=aggregate,
        environment=environment if environment is not None else B0Environment.capture(),
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


def _canonical_payload(
    config: B0Config,
    input_sha256: str,
    input_size: int,
    predictions: list[B0Prediction],
    aggregate: B0Aggregate,
) -> dict[str, object]:
    return {
        "experiment_id": config.experiment_id,
        "experiment_version": config.experiment_version,
        "model_id": config.model_id,
        "model_revision": config.model_revision,
        "tokenizer_revision": config.tokenizer_revision,
        "prompt_template_version": config.prompt_template_version,
        "evidence_condition": config.evidence_condition,
        "max_new_tokens": config.max_new_tokens,
        "seed": config.seed,
        "input_sha256": input_sha256,
        "input_size": input_size,
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
    """Full serializable report: canonical result plus non-canonical environment."""
    canonical = _canonical_payload(
        report.config,
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
        "environment": {
            "python_version": report.environment.python_version,
            "python_implementation": report.environment.python_implementation,
            "code_commit": report.environment.code_commit,
        },
    }


def write_b0_report(report: B0Report, path: Path) -> None:
    """Write the report as canonical UTF-8 JSON. The caller controls the path."""
    document = report_to_document(report)
    path.write_bytes(canonical_json_bytes(document) + b"\n")
