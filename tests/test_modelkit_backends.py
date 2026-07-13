"""M4 — ModelKit optional backend contracts and integration tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from medscale.backends import (
    BackendError,
    BackendMissingDependencyError,
    BackendUnsupportedModelError,
    GenerationConfig,
)
from medscale.backends.llamacpp import (
    validate_package_installed as llamacpp_validate_package_installed,
)
from medscale.backends.transformers import (
    TransformersSpanExtractor,
    TransformersTextGenerator,
)
from medscale.modelkit.interfaces import (
    FinishReason,
    GenerationRequest,
    GenerationResult,
    ModelRef,
    Span,
)

_SRC = Path(__file__).resolve().parents[1] / "src" / "medscale"


def _ref() -> ModelRef:
    return ModelRef(model_id="qwen3-8b", revision="abc123", backend="transformers")


def test_backends_package_imports_cleanly() -> None:
    """Core install must import the backends package without crashing."""
    import medscale.backends as backends

    assert hasattr(backends, "BackendMissingDependencyError")


def test_transformers_missing_dependency_is_actionable() -> None:
    """When transformers is unavailable, construction fails with an install hint."""
    if importlib.util.find_spec("transformers") is not None:
        pytest.skip("transformers is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-transformers\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        TransformersTextGenerator(_ref())


def test_llamacpp_missing_dependency_is_actionable() -> None:
    """When llama-cpp-python is unavailable, validation fails with an install hint."""
    if importlib.util.find_spec("llama_cpp") is not None:
        pytest.skip("llama_cpp is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-llamacpp\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        llamacpp_validate_package_installed()


def test_transformers_generate_contract() -> None:
    if importlib.util.find_spec("transformers") is None:
        pytest.skip("transformers extra is not installed")
    request = GenerationRequest(prompt="test prompt", seed=0)
    result = TransformersTextGenerator(_ref()).generate(request)
    assert isinstance(result, GenerationResult)
    assert result.model.model_id == "qwen3-8b"
    assert result.text == f"[transformers:{_ref().model_id}] test prompt"
    assert result.finish_reason in {FinishReason.STOP, FinishReason.LENGTH, FinishReason.ERROR}


def test_transformers_span_extractor_contract() -> None:
    if importlib.util.find_spec("transformers") is None:
        pytest.skip("transformers extra is not installed")
    extractor = TransformersSpanExtractor(_ref())
    spans = extractor.extract("aspirin")
    assert isinstance(spans, tuple)
    assert all(isinstance(span, Span) for span in spans)


def test_backend_error_hierarchy() -> None:
    assert issubclass(BackendMissingDependencyError, BackendError)
    assert issubclass(BackendUnsupportedModelError, BackendError)


def test_generation_config_validates_bad_inputs() -> None:
    with pytest.raises(ValueError, match="backend_name must be non-empty"):
        GenerationConfig(backend_name="")
    with pytest.raises(ValueError, match="temperature must be >= 0"):
        GenerationConfig(backend_name="x", temperature=-1)
    with pytest.raises(ValueError, match="seed must be non-negative"):
        GenerationConfig(backend_name="x", seed=-1)


def test_backend_module_does_not_import_cli_or_research_or_dataset() -> None:
    """Backend boundaries must remain independent from application modules."""
    forbidden = {"cli", "research", "dataset"}
    offenders = []
    for py in (_SRC / "backends").rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        for token in forbidden:
            if f"medscale.{token}" in text:
                offenders.append(f"{py.relative_to(_SRC)}: imports medscale.{token}")
    assert not offenders, "\n  ".join(offenders)


def test_transformers_validation_import_is_actionable() -> None:
    if importlib.util.find_spec("transformers") is not None:
        pytest.skip("transformers is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-transformers\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        from medscale.backends.transformers.validation import validate_package_installed

        validate_package_installed()


def test_llamacpp_skip_when_unavailable() -> None:
    """Ensure llama backend validation can be imported without crashing."""
    import medscale.backends.llamacpp as llamacpp

    assert hasattr(llamacpp, "LlamaTextGenerator")


def test_llamacpp_validation_import_is_actionable() -> None:
    if importlib.util.find_spec("llama_cpp") is not None:
        pytest.skip("llama_cpp is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-llamacpp\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        llamacpp_validate_package_installed()
