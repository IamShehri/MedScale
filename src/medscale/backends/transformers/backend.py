from __future__ import annotations

from medscale.backends.common import GenerationConfig
from medscale.backends.transformers.validation import validate_package_installed
from medscale.modelkit.interfaces import (
    FinishReason,
    GenerationRequest,
    GenerationResult,
    ModelRef,
    Span,
)

__all__ = [
    "TransformersBackend",
    "TransformersSpanExtractor",
    "TransformersTextGenerator",
]


class TransformersBackend:
    name = "transformers"
    version = "0.1.0"


class TransformersTextGenerator:
    def __init__(self, ref: ModelRef) -> None:
        validate_package_installed()
        self.model = ref
        self._config = GenerationConfig(
            backend_name="transformers",
            backend_version="0.1.0",
            do_sample=False,
            temperature=0.0,
            top_p=1.0,
            max_new_tokens=512,
            seed=42,
        )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            text=f"[transformers:{self.model.model_id}] {request.prompt}",
            model=self.model,
            finish_reason=FinishReason.STOP,
        )


class TransformersSpanExtractor:
    def __init__(self, ref: ModelRef) -> None:
        validate_package_installed()
        self.model = ref

    def extract(self, text: str) -> tuple[Span, ...]:
        return (
            Span(
                start=0,
                end=min(4, len(text)),
                label="TRANSFORMER",
                text=text[:4],
            ),
        )
