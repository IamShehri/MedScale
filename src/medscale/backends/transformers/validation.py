"""Transformers backend validation: dependency presence and fail-closed B0 config.

Everything here is import-safe without ``transformers`` installed. Configuration
validation is deterministic, typed, and must run *before* any runtime/model
construction so an unapproved or nondeterministic request never reaches a loader.
"""

from __future__ import annotations

from dataclasses import dataclass

from medscale.backends.common import (
    BackendError,
    BackendMissingDependencyError,
    BackendUnsupportedModelError,
)

__all__ = [
    "APPROVED_B0_MODELS",
    "SUPPORTED_DEVICES",
    "SUPPORTED_DTYPES",
    "TransformersConfigError",
    "TransformersGenerationConfig",
    "validate_generation_config",
    "validate_package_installed",
]

#: The only model identifiers B0 will serve. These are the two ratified student
#: candidates. No other model is accepted, and no Chinese model, embedding model,
#: reranker, or teacher may ever be added to this set.
APPROVED_B0_MODELS: frozenset[str] = frozenset(
    {"google/medgemma-1.5-4b-it", "meta-llama/Llama-3.2-3B-Instruct"}
)
SUPPORTED_DTYPES: frozenset[str] = frozenset({"float32", "float16", "bfloat16"})
SUPPORTED_DEVICES: frozenset[str] = frozenset({"cpu", "cuda"})


class TransformersConfigError(BackendError):
    """A Transformers generation configuration is invalid for the B0 phase."""


def validate_package_installed() -> None:
    """Fail closed with an actionable install hint when transformers is absent."""
    spec = __import__("importlib.util").util.find_spec("transformers")
    if spec is None:
        raise BackendMissingDependencyError(
            "Transformers backend unavailable.\n"
            "Install:\n"
            "  pip install medscale[backends-transformers]\n"
            "Missing dependency:\n"
            "  transformers>=4.44\n"
            "Required extra: backends-transformers"
        )


@dataclass(frozen=True, slots=True)
class TransformersGenerationConfig:
    """Explicit, deterministic B0 generation configuration.

    Values are validated by :func:`validate_generation_config`, never silently
    coerced. B0 permits only greedy, deterministic, local-files-only generation.
    """

    model_id: str
    revision: str
    max_new_tokens: int
    seed: int
    do_sample: bool = False
    trust_remote_code: bool = False
    local_files_only: bool = True
    dtype: str = "float32"
    device: str = "cpu"
    quantization: str = "none"


def _is_int(value: object) -> bool:
    """True only for a genuine built-in int (a ``bool`` is never accepted)."""
    return isinstance(value, int) and not isinstance(value, bool)


def validate_generation_config(config: TransformersGenerationConfig) -> None:
    """Reject any unapproved or nondeterministic B0 configuration, fail-closed.

    Raises before any runtime or model construction. No value is substituted.
    """
    if not isinstance(config.model_id, str) or config.model_id not in APPROVED_B0_MODELS:
        raise BackendUnsupportedModelError(
            f"model_id must be one of {sorted(APPROVED_B0_MODELS)}, got {config.model_id!r}"
        )
    if not isinstance(config.revision, str) or not config.revision.strip():
        raise TransformersConfigError("model revision must be an explicit non-blank string")
    if config.do_sample:
        raise TransformersConfigError(
            "B0 requires deterministic greedy generation: do_sample must be False"
        )
    if not _is_int(config.max_new_tokens) or config.max_new_tokens <= 0:
        raise TransformersConfigError(
            f"max_new_tokens must be a positive integer, got {config.max_new_tokens!r}"
        )
    if not _is_int(config.seed) or config.seed < 0:
        raise TransformersConfigError(f"seed must be a non-negative integer, got {config.seed!r}")
    if config.trust_remote_code:
        raise TransformersConfigError("trust_remote_code must be False for B0")
    if not config.local_files_only:
        raise TransformersConfigError(
            "local_files_only must be True for B0 (no network or model download)"
        )
    if config.dtype not in SUPPORTED_DTYPES:
        raise TransformersConfigError(
            f"dtype must be one of {sorted(SUPPORTED_DTYPES)}, got {config.dtype!r}"
        )
    if config.device not in SUPPORTED_DEVICES:
        raise TransformersConfigError(
            f"device must be one of {sorted(SUPPORTED_DEVICES)}, got {config.device!r}"
        )
    if config.quantization != "none":
        raise TransformersConfigError(
            f"unsupported quantization {config.quantization!r}; B0 permits only 'none'"
        )
