"""Model-agnostic interfaces: the contract every model must satisfy.

A model participates in MedScale by implementing one of these protocols behind a
:class:`ModelRef`. Nothing downstream (benchmark runners, experiment pipelines,
training recipes) may depend on any concrete backend — only on these types. That is
the replaceability guarantee: swapping models or backends changes a ``ModelRef``,
never MedScale.

Grammar-constrained generation is a first-class field of the *request*, not a backend
detail: a backend that cannot honor ``grammar`` must raise, never silently ignore it.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Protocol

__all__ = [
    "FinishReason",
    "GenerationRequest",
    "GenerationResult",
    "ModelRef",
    "Span",
    "SpanExtractor",
    "TextGenerator",
]


@dataclass(frozen=True)
class ModelRef:
    """An exact, reproducible reference to a model as used in a run.

    ``model_id`` is a registry id (see :mod:`medscale.modelkit.registry`);
    ``revision`` pins the exact weights; ``backend`` names the serving implementation
    (e.g. ``transformers``, ``llama.cpp``, ``api:<provider>``). ``quantization`` is
    part of identity because it changes outputs.
    """

    model_id: str
    revision: str | None = None
    quantization: str = "none"
    backend: str = "unspecified"

    def __post_init__(self) -> None:
        if not self.model_id.strip():
            raise ValueError("model_id must be non-empty")
        if not self.quantization.strip() or not self.backend.strip():
            raise ValueError("quantization and backend must be non-empty strings")


class FinishReason(enum.Enum):
    STOP = "stop"
    LENGTH = "length"
    ERROR = "error"


@dataclass(frozen=True)
class GenerationRequest:
    """One deterministic generation call: everything that determines the output."""

    prompt: str
    seed: int
    max_new_tokens: int = 512
    temperature: float = 0.0
    grammar: str | None = None
    stop: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.prompt:
            raise ValueError("prompt must be non-empty")
        if self.seed < 0:
            raise ValueError(f"seed must be non-negative, got {self.seed}")
        if self.max_new_tokens <= 0:
            raise ValueError("max_new_tokens must be positive")
        if self.temperature < 0:
            raise ValueError("temperature must be >= 0")
        if self.grammar is not None and not self.grammar.strip():
            raise ValueError("grammar, when given, must be non-empty (GBNF text)")


@dataclass(frozen=True)
class GenerationResult:
    """What came back, attributed to the exact model that produced it."""

    text: str
    model: ModelRef
    finish_reason: FinishReason = FinishReason.STOP


class TextGenerator(Protocol):
    """The generative contract (structural typing — backends need not import us).

    Implementations must be deterministic for a fixed ``(request, model)`` pair up to
    the disclosed hardware nondeterminism bounds, and must raise on a ``grammar`` they
    cannot enforce — degrading constrained decoding silently is prohibited.
    """

    @property
    def model(self) -> ModelRef: ...

    def generate(self, request: GenerationRequest) -> GenerationResult: ...


@dataclass(frozen=True)
class Span:
    """A labeled character span, for extraction baselines and RQ5 span tooling."""

    start: int
    end: int
    label: str
    text: str

    def __post_init__(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError(f"invalid span offsets [{self.start}, {self.end})")
        if not self.label.strip():
            raise ValueError("label must be non-empty")


class SpanExtractor(Protocol):
    """The extraction contract (formalizes the ADR-0007 adapter boundary)."""

    @property
    def model(self) -> ModelRef: ...

    def extract(self, text: str) -> tuple[Span, ...]: ...
