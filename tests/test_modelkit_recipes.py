"""Training recipes: content-addressed identity and schema validation (no training)."""

from __future__ import annotations

import pytest

from medscale.modelkit import AdapterMethod, ModelRef, TrainingRecipe
from medscale.modelkit.recipes import DatasetRef

_DATA = DatasetRef(name="medscale-fhir-synthetic", version="v0.1", content_sha256="a" * 64)
_BASE = ModelRef(model_id="qwen3-8b", revision="abc123", quantization="nf4", backend="transformers")


def _recipe(**overrides: object) -> TrainingRecipe:
    base: dict[str, object] = {
        "base": _BASE,
        "method": AdapterMethod.QLORA,
        "dataset": _DATA,
        "seed": 0,
    }
    base.update(overrides)
    return TrainingRecipe(**base)  # type: ignore[arg-type]


def test_recipe_id_is_deterministic_and_content_sensitive() -> None:
    assert _recipe().recipe_id == _recipe().recipe_id
    assert _recipe().recipe_id != _recipe(seed=1).recipe_id
    assert _recipe().recipe_id != _recipe(lora_r=8).recipe_id


def test_qlora_requires_quantized_base() -> None:
    unquantized = ModelRef(model_id="qwen3-8b", backend="transformers")
    with pytest.raises(ValueError, match="quantized base"):
        _recipe(base=unquantized)


def test_lora_allows_unquantized_base() -> None:
    unquantized = ModelRef(model_id="qwen3-8b", backend="transformers")
    recipe = _recipe(base=unquantized, method=AdapterMethod.LORA)
    assert recipe.method is AdapterMethod.LORA


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("seed", -1, "non-negative"),
        ("lora_r", 0, "positive"),
        ("lora_dropout", 1.0, r"\[0, 1\)"),
        ("target_modules", (), "non-empty"),
        ("learning_rate", 0.0, "positive"),
        ("max_steps", 0, "positive"),
    ],
)
def test_invalid_hyperparameters_rejected(field: str, value: object, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _recipe(**{field: value})


def test_dataset_ref_validation() -> None:
    with pytest.raises(ValueError, match="64-hex"):
        DatasetRef(name="d", version="v1", content_sha256="short")
