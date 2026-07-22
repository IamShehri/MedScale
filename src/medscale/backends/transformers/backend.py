"""Deterministic, dependency-injected Transformers generation boundary.

No model, tokenizer, ``torch``, or pipeline is imported or constructed at module
import time. Runtime construction is separated from generation and injected, so
tests exercise the whole boundary with fakes and never touch a real model, the
network, or the filesystem. Production generation never echoes the prompt: only
the newly generated tokens are decoded and returned.
"""

from __future__ import annotations

import importlib
from typing import Any, Protocol

from medscale.backends.common import BackendError
from medscale.backends.transformers.validation import (
    TransformersGenerationConfig,
    validate_generation_config,
    validate_package_installed,
)
from medscale.modelkit.interfaces import (
    FinishReason,
    GenerationRequest,
    GenerationResult,
    ModelRef,
    Span,
)

__all__ = [
    "TransformersBackend",
    "TransformersDecodeError",
    "TransformersGenerateError",
    "TransformersLoadError",
    "TransformersRuntime",
    "TransformersSpanExtractor",
    "TransformersTextGenerator",
    "TransformersTokenizeError",
    "build_transformers_runtime",
]


class TransformersLoadError(BackendError):
    """Runtime/model construction failed."""


class TransformersTokenizeError(BackendError):
    """Tokenization of the prompt failed."""


class TransformersGenerateError(BackendError):
    """Token generation failed or produced an inconsistent result."""


class TransformersDecodeError(BackendError):
    """Decoding of generated tokens failed."""


class TransformersRuntime(Protocol):
    """The injectable runtime boundary: encode, generate, decode, revision.

    ``generate`` must return the full token sequence (the exact prompt tokens
    followed by newly generated tokens), so the generator can strip the prompt
    prefix and never echo it.
    """

    @property
    def revision(self) -> str: ...

    def encode(self, text: str) -> tuple[int, ...]: ...

    def generate(self, input_ids: tuple[int, ...], *, max_new_tokens: int) -> tuple[int, ...]: ...

    def decode(self, token_ids: tuple[int, ...]) -> str: ...


class TransformersBackend:
    name = "transformers"
    version = "0.1.0"


class TransformersTextGenerator:
    """Deterministic generator over an injected :class:`TransformersRuntime`.

    Configuration is validated before anything else; a mismatched runtime
    revision is rejected. The returned completion contains only the generated
    tokens, never the prompt.
    """

    def __init__(
        self, config: TransformersGenerationConfig, *, runtime: TransformersRuntime
    ) -> None:
        validate_generation_config(config)
        if runtime.revision != config.revision:
            raise TransformersLoadError(
                f"runtime revision {runtime.revision!r} does not match "
                f"config revision {config.revision!r}"
            )
        self._config = config
        self._runtime = runtime
        self._ref = ModelRef(
            model_id=config.model_id, revision=config.revision, backend="transformers"
        )

    @property
    def model(self) -> ModelRef:
        return self._ref

    def generate(self, request: GenerationRequest) -> GenerationResult:
        input_ids = self._encode(request.prompt)
        output_ids = self._generate(input_ids)
        if output_ids[: len(input_ids)] != input_ids:
            raise TransformersGenerateError(
                "generation output does not begin with the exact prompt tokens"
            )
        new_ids = output_ids[len(input_ids) :]
        text = self._decode(new_ids)
        finish = (
            FinishReason.LENGTH
            if len(new_ids) >= self._config.max_new_tokens
            else FinishReason.STOP
        )
        return GenerationResult(text=text, model=self._ref, finish_reason=finish)

    def _encode(self, prompt: str) -> tuple[int, ...]:
        try:
            return tuple(int(token) for token in self._runtime.encode(prompt))
        except TransformersTokenizeError:
            raise
        except Exception as exc:  # normalize any tokenizer failure
            raise TransformersTokenizeError(f"tokenization failed: {exc}") from exc

    def _generate(self, input_ids: tuple[int, ...]) -> tuple[int, ...]:
        try:
            return tuple(
                int(token)
                for token in self._runtime.generate(
                    input_ids, max_new_tokens=self._config.max_new_tokens
                )
            )
        except TransformersGenerateError:
            raise
        except Exception as exc:  # normalize any generation failure
            raise TransformersGenerateError(f"generation failed: {exc}") from exc

    def _decode(self, token_ids: tuple[int, ...]) -> str:
        try:
            return self._runtime.decode(token_ids)
        except TransformersDecodeError:
            raise
        except Exception as exc:  # normalize any decode failure
            raise TransformersDecodeError(f"decoding failed: {exc}") from exc


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


class _RealTransformersRuntime:
    """The production runtime wrapper. Never exercised by the test suite.

    Uses ``importlib`` so mypy/tooling never statically follows the optional
    ``transformers`` dependency, and loads with ``local_files_only`` and
    ``trust_remote_code=False`` so no download or remote code path is possible.
    """

    def __init__(self, *, tokenizer: Any, model: Any, revision: str) -> None:
        self._tokenizer = tokenizer
        self._model = model
        self._revision = revision

    @property
    def revision(self) -> str:
        return self._revision

    def encode(self, text: str) -> tuple[int, ...]:
        encoded: Any = self._tokenizer(text)
        return tuple(int(token) for token in encoded["input_ids"])

    def generate(self, input_ids: tuple[int, ...], *, max_new_tokens: int) -> tuple[int, ...]:
        output: Any = self._model.generate(
            [list(input_ids)], max_new_tokens=max_new_tokens, do_sample=False, num_beams=1
        )
        return tuple(int(token) for token in output[0])

    def decode(self, token_ids: tuple[int, ...]) -> str:
        return str(self._tokenizer.decode(list(token_ids), skip_special_tokens=True))


def build_transformers_runtime(config: TransformersGenerationConfig) -> TransformersRuntime:
    """Construct the real runtime after validating config and dependency presence.

    Loads tokenizer and model at the same explicit revision, local-files-only,
    with remote code disabled. This is the production path and is not invoked by
    the deterministic test suite.
    """
    validate_generation_config(config)
    validate_package_installed()
    try:
        module: Any = importlib.import_module("transformers")
        tokenizer: Any = module.AutoTokenizer.from_pretrained(
            config.model_id,
            revision=config.revision,
            trust_remote_code=config.trust_remote_code,
            local_files_only=config.local_files_only,
        )
        model: Any = module.AutoModelForCausalLM.from_pretrained(
            config.model_id,
            revision=config.revision,
            trust_remote_code=config.trust_remote_code,
            local_files_only=config.local_files_only,
        )
    except Exception as exc:  # normalize any load failure to a typed error
        raise TransformersLoadError(
            f"failed to load {config.model_id}@{config.revision} locally: {exc}"
        ) from exc
    return _RealTransformersRuntime(tokenizer=tokenizer, model=model, revision=config.revision)
