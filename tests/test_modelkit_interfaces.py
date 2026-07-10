"""The model-agnostic contract: any model plugs in behind the same interface."""

from __future__ import annotations

import pytest

from medscale.modelkit import (
    FinishReason,
    GenerationRequest,
    GenerationResult,
    ModelRef,
    Span,
    SpanExtractor,
    TextGenerator,
)

_REF = ModelRef(model_id="qwen3-8b", revision="abc123", backend="stub")


class StubGenerator:
    """A dependency-free model stand-in: the replaceability proof."""

    @property
    def model(self) -> ModelRef:
        return _REF

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if request.grammar is not None:
            # The contract: backends that cannot enforce a grammar must raise.
            raise NotImplementedError("stub cannot enforce grammars")
        return GenerationResult(text=f"echo:{request.prompt}", model=self.model)


def run_through_interface(generator: TextGenerator, prompt: str) -> str:
    """Downstream code sees only the protocol — never a concrete backend."""
    return generator.generate(GenerationRequest(prompt=prompt, seed=0)).text


def test_stub_satisfies_text_generator_protocol() -> None:
    generator: TextGenerator = StubGenerator()
    assert run_through_interface(generator, "hello") == "echo:hello"
    assert generator.model.model_id == "qwen3-8b"


def test_grammar_incapable_backend_must_raise_not_ignore() -> None:
    request = GenerationRequest(prompt="p", seed=0, grammar='root ::= "x"')
    with pytest.raises(NotImplementedError):
        StubGenerator().generate(request)


def test_generation_request_validation() -> None:
    with pytest.raises(ValueError, match="prompt"):
        GenerationRequest(prompt="", seed=0)
    with pytest.raises(ValueError, match="seed"):
        GenerationRequest(prompt="p", seed=-1)
    with pytest.raises(ValueError, match="max_new_tokens"):
        GenerationRequest(prompt="p", seed=0, max_new_tokens=0)
    with pytest.raises(ValueError, match="grammar"):
        GenerationRequest(prompt="p", seed=0, grammar="   ")


def test_model_ref_validation() -> None:
    with pytest.raises(ValueError, match="model_id"):
        ModelRef(model_id="  ")
    ref = ModelRef(model_id="m", quantization="nf4", backend="llama.cpp")
    assert ref.quantization == "nf4"


def test_finish_reason_values() -> None:
    assert {r.value for r in FinishReason} == {"stop", "length", "error"}


class StubExtractor:
    @property
    def model(self) -> ModelRef:
        return _REF

    def extract(self, text: str) -> tuple[Span, ...]:
        return (Span(start=0, end=min(4, len(text)), label="TEST", text=text[:4]),)


def test_span_extractor_protocol_and_span_validation() -> None:
    extractor: SpanExtractor = StubExtractor()
    (span,) = extractor.extract("aspirin")
    assert span.label == "TEST"
    with pytest.raises(ValueError, match="offsets"):
        Span(start=5, end=5, label="X", text="")
    with pytest.raises(ValueError, match="label"):
        Span(start=0, end=1, label=" ", text="a")
