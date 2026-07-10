"""Training recipes: typed, content-addressed LoRA/QLoRA configurations.

A recipe is a *schema object*, not a trainer — training execution remains gated at T5
(ADR-0006 acceptance note). Defining recipes now means every future training run is
reproducible by construction: the recipe's content hash is its identity, and identical
recipes are provably identical.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass

from medscale.modelkit.interfaces import ModelRef
from medscale.reproducibility import content_hash

__all__ = ["AdapterMethod", "DatasetRef", "TrainingRecipe"]


class AdapterMethod(enum.Enum):
    LORA = "lora"
    QLORA = "qlora"


@dataclass(frozen=True)
class DatasetRef:
    """The exact training data: name + version + content hash (contamination anchor)."""

    name: str
    version: str
    content_sha256: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.version.strip():
            raise ValueError("dataset name and version must be non-empty")
        if len(self.content_sha256) != 64:
            raise ValueError("content_sha256 must be a 64-hex content hash")


@dataclass(frozen=True)
class TrainingRecipe:
    """Everything that determines an adapter, hashed into a stable ``recipe_id``."""

    base: ModelRef
    method: AdapterMethod
    dataset: DatasetRef
    seed: int
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: tuple[str, ...] = ("q_proj", "k_proj", "v_proj", "o_proj")
    learning_rate: float = 2e-4
    max_steps: int = 1000

    def __post_init__(self) -> None:
        if self.seed < 0:
            raise ValueError("seed must be non-negative")
        if self.lora_r <= 0 or self.lora_alpha <= 0:
            raise ValueError("lora_r and lora_alpha must be positive")
        if not 0.0 <= self.lora_dropout < 1.0:
            raise ValueError("lora_dropout must be in [0, 1)")
        if not self.target_modules:
            raise ValueError("target_modules must be non-empty")
        if self.learning_rate <= 0 or self.max_steps <= 0:
            raise ValueError("learning_rate and max_steps must be positive")
        if self.method is AdapterMethod.QLORA and self.base.quantization == "none":
            raise ValueError(
                "QLoRA requires a quantized base (set ModelRef.quantization, e.g. 'nf4')"
            )

    @property
    def recipe_id(self) -> str:
        """Content-derived identity: equal recipes hash identically."""
        return content_hash(
            {
                "base": {
                    "model_id": self.base.model_id,
                    "revision": self.base.revision,
                    "quantization": self.base.quantization,
                    "backend": self.base.backend,
                },
                "method": self.method.value,
                "dataset": {
                    "name": self.dataset.name,
                    "version": self.dataset.version,
                    "content_sha256": self.dataset.content_sha256,
                },
                "seed": self.seed,
                "lora_r": self.lora_r,
                "lora_alpha": self.lora_alpha,
                "lora_dropout": self.lora_dropout,
                "target_modules": list(self.target_modules),
                "learning_rate": self.learning_rate,
                "max_steps": self.max_steps,
            }
        )
