"""M4 — ModelKit optional backend contracts and the B0 dependency-injected generator."""

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
from medscale.backends.transformers.backend import (
    TransformersDecodeError,
    TransformersGenerateError,
    TransformersLoadError,
    TransformersTokenizeError,
    build_transformers_runtime,
)
from medscale.backends.transformers.validation import (
    APPROVED_B0_MODELS,
    TransformersConfigError,
    TransformersGenerationConfig,
    validate_generation_config,
)
from medscale.modelkit.interfaces import (
    FinishReason,
    GenerationRequest,
    GenerationResult,
    ModelRef,
    Span,
)

_SRC = Path(__file__).resolve().parents[1] / "src" / "medscale"
_MODEL = "meta-llama/Llama-3.2-3B-Instruct"


def _ref() -> ModelRef:
    return ModelRef(model_id=_MODEL, revision="rev-1", backend="transformers")


def _config(**overrides: object) -> TransformersGenerationConfig:
    base: dict[str, object] = {
        "model_id": _MODEL,
        "revision": "rev-1",
        "max_new_tokens": 8,
        "seed": 0,
    }
    base.update(overrides)
    return TransformersGenerationConfig(**base)  # type: ignore[arg-type]


class _FakeRuntime:
    """A deterministic in-memory runtime; never touches a real model or network."""

    def __init__(
        self,
        *,
        revision: str = "rev-1",
        prompt_ids: tuple[int, ...] = (1, 2, 3),
        new_ids: tuple[int, ...] = (4, 5),
        fail: str | None = None,
        prefix_prompt: bool = True,
    ) -> None:
        self.revision = revision
        self._prompt_ids = prompt_ids
        self._new_ids = new_ids
        self._fail = fail
        self._prefix_prompt = prefix_prompt
        self.decoded: tuple[int, ...] | None = None

    def encode(self, text: str) -> tuple[int, ...]:
        if self._fail == "encode":
            raise RuntimeError("boom-encode")
        return self._prompt_ids

    def generate(self, input_ids: tuple[int, ...], *, max_new_tokens: int) -> tuple[int, ...]:
        if self._fail == "generate":
            raise RuntimeError("boom-generate")
        tail = self._new_ids[:max_new_tokens]
        return (input_ids + tail) if self._prefix_prompt else tail

    def decode(self, token_ids: tuple[int, ...]) -> str:
        if self._fail == "decode":
            raise RuntimeError("boom-decode")
        self.decoded = token_ids
        return f"decoded:{list(token_ids)}"


# --------------------------------------------------------------- package/dependency
def test_backends_package_imports_cleanly() -> None:
    import medscale.backends as backends

    assert hasattr(backends, "BackendMissingDependencyError")


def test_transformers_missing_dependency_is_actionable() -> None:
    if importlib.util.find_spec("transformers") is not None:
        pytest.skip("transformers is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-transformers\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        build_transformers_runtime(_config())


def test_transformers_validation_import_is_actionable() -> None:
    if importlib.util.find_spec("transformers") is not None:
        pytest.skip("transformers is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-transformers\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        from medscale.backends.transformers.validation import validate_package_installed

        validate_package_installed()


def test_llamacpp_missing_dependency_is_actionable() -> None:
    if importlib.util.find_spec("llama_cpp") is not None:
        pytest.skip("llama_cpp is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-llamacpp\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        llamacpp_validate_package_installed()


def test_llamacpp_skip_when_unavailable() -> None:
    import medscale.backends.llamacpp as llamacpp

    assert hasattr(llamacpp, "LlamaTextGenerator")


def test_llamacpp_validation_import_is_actionable() -> None:
    if importlib.util.find_spec("llama_cpp") is not None:
        pytest.skip("llama_cpp is installed; cannot test missing-dependency path")
    pattern = r"pip install medscale\[backends-llamacpp\]"
    with pytest.raises(BackendMissingDependencyError, match=pattern):
        llamacpp_validate_package_installed()


# --------------------------------------------------------------- error hierarchy
def test_backend_error_hierarchy() -> None:
    assert issubclass(BackendMissingDependencyError, BackendError)
    assert issubclass(BackendUnsupportedModelError, BackendError)
    assert issubclass(TransformersConfigError, BackendError)
    for error in (
        TransformersLoadError,
        TransformersTokenizeError,
        TransformersGenerateError,
        TransformersDecodeError,
    ):
        assert issubclass(error, BackendError)


def test_generation_config_validates_bad_inputs() -> None:
    with pytest.raises(ValueError, match="backend_name must be non-empty"):
        GenerationConfig(backend_name="")
    with pytest.raises(ValueError, match="temperature must be >= 0"):
        GenerationConfig(backend_name="x", temperature=-1)
    with pytest.raises(ValueError, match="seed must be non-negative"):
        GenerationConfig(backend_name="x", seed=-1)


# --------------------------------------------------------------- config validation
def test_both_approved_models_validate() -> None:
    assert sorted(APPROVED_B0_MODELS) == [
        "google/medgemma-1.5-4b-it",
        "meta-llama/Llama-3.2-3B-Instruct",
    ]
    for model_id in sorted(APPROVED_B0_MODELS):
        validate_generation_config(_config(model_id=model_id))


@pytest.mark.parametrize(
    "model_id",
    [
        "Qwen/Qwen2.5-7B-Instruct",
        "deepseek-ai/DeepSeek-V2",
        "01-ai/Yi-1.5-9B",
        "THUDM/glm-4-9b",
        "internlm/internlm2-7b",
        "some/unapproved-model",
    ],
)
def test_unapproved_and_chinese_models_are_rejected(model_id: str) -> None:
    with pytest.raises(BackendUnsupportedModelError, match="model_id must be one of"):
        validate_generation_config(_config(model_id=model_id))


def test_blank_and_malformed_revisions_fail() -> None:
    with pytest.raises(TransformersConfigError, match="revision"):
        validate_generation_config(_config(revision=""))
    with pytest.raises(TransformersConfigError, match="revision"):
        validate_generation_config(_config(revision="   "))


def test_sampling_and_nondeterministic_generation_fail() -> None:
    with pytest.raises(TransformersConfigError, match="do_sample"):
        validate_generation_config(_config(do_sample=True))
    with pytest.raises(TransformersConfigError, match="trust_remote_code"):
        validate_generation_config(_config(trust_remote_code=True))
    with pytest.raises(TransformersConfigError, match="local_files_only"):
        validate_generation_config(_config(local_files_only=False))
    with pytest.raises(TransformersConfigError, match="quantization"):
        validate_generation_config(_config(quantization="int8"))


@pytest.mark.parametrize("bad_seed", [True, False, 0.5, 1.0, "1", None, -1])
def test_invalid_seed_values_fail(bad_seed: object) -> None:
    with pytest.raises(TransformersConfigError, match="seed"):
        validate_generation_config(_config(seed=bad_seed))


@pytest.mark.parametrize("bad_tokens", [True, False, 0.5, 1.0, "1", None, 0, -1])
def test_invalid_max_new_tokens_fail(bad_tokens: object) -> None:
    with pytest.raises(TransformersConfigError, match="max_new_tokens"):
        validate_generation_config(_config(max_new_tokens=bad_tokens))


# --------------------------------------------------------------- generator boundary
def test_generator_validates_config_before_touching_runtime() -> None:
    runtime = _FakeRuntime()
    with pytest.raises(BackendUnsupportedModelError):
        TransformersTextGenerator(_config(model_id="some/bad"), runtime=runtime)
    assert runtime.decoded is None  # runtime never exercised


def test_generator_rejects_revision_mismatch() -> None:
    with pytest.raises(TransformersLoadError, match="revision"):
        TransformersTextGenerator(_config(revision="rev-1"), runtime=_FakeRuntime(revision="other"))


def test_generator_returns_only_new_tokens_never_echoes_prompt() -> None:
    runtime = _FakeRuntime(prompt_ids=(1, 2, 3), new_ids=(4, 5))
    generator = TransformersTextGenerator(_config(), runtime=runtime)
    prompt = "Question: does aspirin help?\nAnswer:"
    result = generator.generate(GenerationRequest(prompt=prompt, seed=0, max_new_tokens=8))
    assert isinstance(result, GenerationResult)
    assert runtime.decoded == (4, 5)  # only the new tokens were decoded
    assert result.text == "decoded:[4, 5]"
    assert prompt not in result.text
    assert result.finish_reason is FinishReason.STOP


def test_generator_reports_length_finish_reason() -> None:
    runtime = _FakeRuntime(prompt_ids=(1,), new_ids=(9, 9))
    generator = TransformersTextGenerator(_config(max_new_tokens=2), runtime=runtime)
    result = generator.generate(GenerationRequest(prompt="p", seed=0, max_new_tokens=2))
    assert result.finish_reason is FinishReason.LENGTH


def test_generator_is_deterministic_across_repeated_calls() -> None:
    generator = TransformersTextGenerator(_config(), runtime=_FakeRuntime())
    request = GenerationRequest(prompt="same prompt", seed=0, max_new_tokens=8)
    first = generator.generate(request)
    second = generator.generate(request)
    assert first == second


def test_generator_output_must_begin_with_prompt_tokens() -> None:
    runtime = _FakeRuntime(prefix_prompt=False, new_ids=(7, 8))
    generator = TransformersTextGenerator(_config(), runtime=runtime)
    with pytest.raises(TransformersGenerateError, match="begin with the exact prompt tokens"):
        generator.generate(GenerationRequest(prompt="p", seed=0, max_new_tokens=8))


@pytest.mark.parametrize(
    ("stage", "error"),
    [
        ("encode", TransformersTokenizeError),
        ("generate", TransformersGenerateError),
        ("decode", TransformersDecodeError),
    ],
)
def test_generator_maps_each_stage_failure_to_typed_error(
    stage: str, error: type[BackendError]
) -> None:
    generator = TransformersTextGenerator(_config(), runtime=_FakeRuntime(fail=stage))
    with pytest.raises(error):
        generator.generate(GenerationRequest(prompt="p", seed=0, max_new_tokens=8))


def test_transformers_span_extractor_contract() -> None:
    if importlib.util.find_spec("transformers") is None:
        pytest.skip("transformers extra is not installed")
    extractor = TransformersSpanExtractor(_ref())
    spans = extractor.extract("aspirin")
    assert isinstance(spans, tuple)
    assert all(isinstance(span, Span) for span in spans)


# --------------------------------------------------------------- boundary hygiene
def test_backend_module_does_not_import_cli_or_research_or_dataset() -> None:
    forbidden = {"cli", "research", "dataset"}
    offenders = []
    for py in (_SRC / "backends").rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        for token in forbidden:
            if f"medscale.{token}" in text:
                offenders.append(f"{py.relative_to(_SRC)}: imports medscale.{token}")
    assert not offenders, "\n  ".join(offenders)
