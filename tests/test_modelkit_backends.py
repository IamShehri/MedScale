"""M4 — ModelKit optional backend contracts and the B0 dependency-injected runtime."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

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
    EncodedInput,
    TransformersDecodeError,
    TransformersGenerateError,
    TransformersLoadError,
    TransformersTokenizeError,
    _RealTransformersRuntime,
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
_SHA = "a" * 40
_SHA2 = "b" * 40


def _ref() -> ModelRef:
    return ModelRef(model_id=_MODEL, revision=_SHA, backend="transformers")


def _config(**overrides: object) -> TransformersGenerationConfig:
    base: dict[str, object] = {
        "model_id": _MODEL,
        "model_revision": _SHA,
        "tokenizer_revision": _SHA,
        "max_new_tokens": 8,
        "seed": 0,
    }
    base.update(overrides)
    return TransformersGenerationConfig(**base)  # type: ignore[arg-type]


class _FakeRuntime:
    """Simple deterministic runtime for the high-level generator tests."""

    def __init__(
        self,
        *,
        model_revision: str = _SHA,
        tokenizer_revision: str = _SHA,
        prompt_ids: tuple[int, ...] = (1, 2, 3),
        new_ids: tuple[int, ...] = (4, 5),
        fail: str | None = None,
        prefix: bool = True,
    ) -> None:
        self.model_revision = model_revision
        self.tokenizer_revision = tokenizer_revision
        self._p = prompt_ids
        self._n = new_ids
        self._fail = fail
        self._prefix = prefix
        self.decoded: tuple[int, ...] | None = None
        self.touched = False

    def encode(self, text: str) -> EncodedInput:
        self.touched = True
        if self._fail == "encode":
            raise RuntimeError("boom-encode")
        return EncodedInput(input_ids=self._p, attention_mask=tuple(1 for _ in self._p))

    def generate(self, encoded: EncodedInput, *, max_new_tokens: int) -> tuple[int, ...]:
        if self._fail == "generate":
            raise RuntimeError("boom-generate")
        tail = self._n[:max_new_tokens]
        return (encoded.input_ids + tail) if self._prefix else tail

    def decode(self, token_ids: tuple[int, ...]) -> str:
        if self._fail == "decode":
            raise RuntimeError("boom-decode")
        self.decoded = token_ids
        return f"OUT{list(token_ids)}"


# ----- fakes for the real PyTorch adapter (no real torch/transformers) -----
class _FakeDtype:
    def __init__(self, name: str) -> None:
        self.name = name


class _FakeCuda:
    def __init__(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available


class _FakeInferenceCtx:
    def __init__(self, log: list[str]) -> None:
        self._log = log

    def __enter__(self) -> _FakeInferenceCtx:
        self._log.append("enter")
        return self

    def __exit__(self, *exc: object) -> None:
        self._log.append("exit")


class _FakeTorch:
    def __init__(self, *, cuda_available: bool = False) -> None:
        self.float32 = _FakeDtype("float32")
        self.float16 = _FakeDtype("float16")
        self.bfloat16 = _FakeDtype("bfloat16")
        self.cuda = _FakeCuda(cuda_available)
        self.inference_log: list[str] = []

    def inference_mode(self) -> _FakeInferenceCtx:
        return _FakeInferenceCtx(self.inference_log)


class _FakeTensor:
    def __init__(self, rows: list[list[int]], device: str | None = None) -> None:
        self.rows = rows
        self.device = device

    def to(self, device: str) -> _FakeTensor:
        return _FakeTensor(self.rows, device=device)

    def __getitem__(self, index: int) -> list[int]:
        return self.rows[index]


class _FakeTokenizer:
    def __init__(
        self,
        *,
        ids: tuple[int, ...] = (1, 2, 3),
        pad: int | None = 0,
        eos: int | None = 2,
    ) -> None:
        self._ids = ids
        self.pad_token_id = pad
        self.eos_token_id = eos
        self.calls: list[tuple[str, object]] = []
        self.decode_calls: list[tuple[int, ...]] = []

    def __call__(self, text: str, return_tensors: str | None = None) -> dict[str, _FakeTensor]:
        self.calls.append((text, return_tensors))
        return {
            "input_ids": _FakeTensor([list(self._ids)]),
            "attention_mask": _FakeTensor([[1 for _ in self._ids]]),
        }

    def decode(self, ids: list[int], skip_special_tokens: bool = False) -> str:
        self.decode_calls.append(tuple(ids))
        return "DEC:" + ",".join(str(i) for i in ids)


class _FakeModel:
    def __init__(self, *, new_ids: tuple[int, ...] = (4, 5), prefix: bool = True) -> None:
        self._new = new_ids
        self._prefix = prefix
        self.to_calls: list[str] = []
        self.eval_calls = 0
        self.generate_calls: list[dict[str, Any]] = []

    def to(self, device: str) -> _FakeModel:
        self.to_calls.append(device)
        return self

    def eval(self) -> _FakeModel:
        self.eval_calls += 1
        return self

    def generate(self, **kwargs: Any) -> _FakeTensor:
        self.generate_calls.append(kwargs)
        row = list(kwargs["input_ids"][0])
        out = (row + list(self._new)) if self._prefix else list(self._new)
        return _FakeTensor([out])


def _real_runtime(
    *,
    torch_module: _FakeTorch | None = None,
    tokenizer: _FakeTokenizer | None = None,
    model: _FakeModel | None = None,
    device: str = "cpu",
    dtype: str = "float32",
) -> _RealTransformersRuntime:
    return _RealTransformersRuntime(
        torch_module=torch_module if torch_module is not None else _FakeTorch(),
        tokenizer=tokenizer if tokenizer is not None else _FakeTokenizer(),
        model=model if model is not None else _FakeModel(),
        model_revision=_SHA,
        tokenizer_revision=_SHA,
        device=device,
        dtype=dtype,
    )


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
def test_models_outside_b0_allowlist_are_rejected(model_id: str) -> None:
    with pytest.raises(BackendUnsupportedModelError, match="model_id must be one of"):
        validate_generation_config(_config(model_id=model_id))


@pytest.mark.parametrize(
    "revision",
    ["main", "master", "v1.0", "abc123", "A" * 40, "", "   ", " " + "a" * 40, "a" * 39, "a" * 41],
)
def test_mutable_or_malformed_model_revision_rejected(revision: str) -> None:
    with pytest.raises(TransformersConfigError, match="model_revision"):
        validate_generation_config(_config(model_revision=revision))


@pytest.mark.parametrize("revision", ["main", "v1.0", "A" * 40, "", "a" * 39])
def test_mutable_or_malformed_tokenizer_revision_rejected(revision: str) -> None:
    with pytest.raises(TransformersConfigError, match="tokenizer_revision"):
        validate_generation_config(_config(tokenizer_revision=revision))


def test_sampling_and_nondeterministic_generation_fail() -> None:
    with pytest.raises(TransformersConfigError, match="do_sample"):
        validate_generation_config(_config(do_sample=True))
    with pytest.raises(TransformersConfigError, match="trust_remote_code"):
        validate_generation_config(_config(trust_remote_code=True))
    with pytest.raises(TransformersConfigError, match="local_files_only"):
        validate_generation_config(_config(local_files_only=False))
    with pytest.raises(TransformersConfigError, match="quantization"):
        validate_generation_config(_config(quantization="int8"))
    with pytest.raises(TransformersConfigError, match="dtype"):
        validate_generation_config(_config(dtype="int4"))
    with pytest.raises(TransformersConfigError, match="device"):
        validate_generation_config(_config(device="tpu"))


@pytest.mark.parametrize("bad_seed", [True, False, 0.5, 1.0, "1", None, -1])
def test_invalid_seed_values_fail(bad_seed: object) -> None:
    with pytest.raises(TransformersConfigError, match="seed"):
        validate_generation_config(_config(seed=bad_seed))


@pytest.mark.parametrize("bad_tokens", [True, False, 0.5, 1.0, "1", None, 0, -1])
def test_invalid_max_new_tokens_fail(bad_tokens: object) -> None:
    with pytest.raises(TransformersConfigError, match="max_new_tokens"):
        validate_generation_config(_config(max_new_tokens=bad_tokens))


# --------------------------------------------------------------- high-level generator
def test_generator_validates_config_before_touching_runtime() -> None:
    runtime = _FakeRuntime()
    with pytest.raises(BackendUnsupportedModelError):
        TransformersTextGenerator(_config(model_id="some/bad"), runtime=runtime)
    assert runtime.touched is False


def test_generator_rejects_revision_mismatch() -> None:
    with pytest.raises(TransformersLoadError, match="model_revision"):
        TransformersTextGenerator(_config(), runtime=_FakeRuntime(model_revision=_SHA2))
    with pytest.raises(TransformersLoadError, match="tokenizer_revision"):
        TransformersTextGenerator(_config(), runtime=_FakeRuntime(tokenizer_revision=_SHA2))


def test_generator_returns_only_new_tokens_never_echoes_prompt() -> None:
    runtime = _FakeRuntime(prompt_ids=(1, 2, 3), new_ids=(4, 5))
    generator = TransformersTextGenerator(_config(), runtime=runtime)
    prompt = "Question: does aspirin help?\nAnswer:"
    result = generator.generate(GenerationRequest(prompt=prompt, seed=0, max_new_tokens=8))
    assert isinstance(result, GenerationResult)
    assert runtime.decoded == (4, 5)
    assert result.text == "OUT[4, 5]"
    assert prompt not in result.text
    assert result.finish_reason is FinishReason.STOP
    assert result.model.revision == _SHA


def test_generator_reports_length_finish_reason() -> None:
    runtime = _FakeRuntime(prompt_ids=(1,), new_ids=(9, 9))
    generator = TransformersTextGenerator(_config(max_new_tokens=2), runtime=runtime)
    result = generator.generate(GenerationRequest(prompt="p", seed=0, max_new_tokens=2))
    assert result.finish_reason is FinishReason.LENGTH


def test_generator_is_deterministic_across_repeated_calls() -> None:
    generator = TransformersTextGenerator(_config(), runtime=_FakeRuntime())
    request = GenerationRequest(prompt="same prompt", seed=0, max_new_tokens=8)
    assert generator.generate(request) == generator.generate(request)


def test_generator_output_must_begin_with_prompt_tokens() -> None:
    runtime = _FakeRuntime(prefix=False, new_ids=(7, 8))
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


# --------------------------------------------------------------- real PyTorch adapter (fakes)
def test_real_runtime_passes_attention_mask_and_deterministic_flags() -> None:
    tok = _FakeTokenizer(ids=(1, 2, 3))
    model = _FakeModel(new_ids=(4, 5))
    runtime = _real_runtime(tokenizer=tok, model=model)
    encoded = runtime.encode("hi")
    assert encoded.input_ids == (1, 2, 3)
    assert encoded.attention_mask == (1, 1, 1)
    out = runtime.generate(encoded, max_new_tokens=8)
    assert out == (1, 2, 3, 4, 5)
    (call,) = model.generate_calls
    assert list(call["attention_mask"][0]) == [1, 1, 1]
    assert call["do_sample"] is False
    assert call["num_beams"] == 1
    assert call["pad_token_id"] == 0
    assert call["eos_token_id"] == 2


def test_real_runtime_moves_tensors_and_model_to_device() -> None:
    model = _FakeModel()
    runtime = _real_runtime(model=model, device="cpu")
    assert model.to_calls == ["cpu"]
    encoded = runtime.encode("hi")
    runtime.generate(encoded, max_new_tokens=8)
    (call,) = model.generate_calls
    assert call["input_ids"].device == "cpu"
    assert call["attention_mask"].device == "cpu"


def test_real_runtime_calls_eval_and_enters_inference_mode() -> None:
    torch_module = _FakeTorch()
    model = _FakeModel()
    runtime = _real_runtime(torch_module=torch_module, model=model)
    runtime.generate(runtime.encode("hi"), max_new_tokens=8)
    assert model.eval_calls == 1
    assert torch_module.inference_log == ["enter", "exit"]


def test_real_runtime_maps_dtype_exactly() -> None:
    torch_module = _FakeTorch()
    runtime = _real_runtime(torch_module=torch_module, dtype="bfloat16")
    assert runtime._dtype is torch_module.bfloat16


def test_real_runtime_rejects_unavailable_cuda() -> None:
    with pytest.raises(TransformersLoadError, match="CUDA"):
        _real_runtime(torch_module=_FakeTorch(cuda_available=False), device="cuda")


def test_real_runtime_rejects_unknown_dtype_and_device() -> None:
    with pytest.raises(TransformersLoadError, match="dtype"):
        _real_runtime(dtype="int4")
    with pytest.raises(TransformersLoadError, match="device"):
        _real_runtime(device="tpu")


def test_real_runtime_uses_eos_as_pad_when_pad_missing() -> None:
    runtime = _real_runtime(tokenizer=_FakeTokenizer(pad=None, eos=7))
    assert runtime._pad_id == 7
    assert runtime._eos_id == 7


def test_real_runtime_fails_closed_without_valid_eos() -> None:
    with pytest.raises(TransformersLoadError, match="eos_token_id"):
        _real_runtime(tokenizer=_FakeTokenizer(pad=None, eos=None))


def test_real_runtime_end_to_end_never_decodes_prompt_tokens() -> None:
    tok = _FakeTokenizer(ids=(1, 2, 3))
    model = _FakeModel(new_ids=(4, 5))
    runtime = _real_runtime(tokenizer=tok, model=model)
    generator = TransformersTextGenerator(_config(), runtime=runtime)
    result = generator.generate(GenerationRequest(prompt="prompt", seed=0, max_new_tokens=8))
    assert tok.decode_calls == [(4, 5)]  # only newly generated tokens decoded
    assert result.text == "DEC:4,5"


def test_real_runtime_prefix_mismatch_raises_typed_error() -> None:
    runtime = _real_runtime(model=_FakeModel(prefix=False, new_ids=(9, 9)))
    generator = TransformersTextGenerator(_config(), runtime=runtime)
    with pytest.raises(TransformersGenerateError, match="begin with the exact prompt tokens"):
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
