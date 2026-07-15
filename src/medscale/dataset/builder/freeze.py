"""Immutable deterministic dataset split-assignment freeze contract."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from medscale.dataset.builder.contracts import _validate_identifier
from medscale.dataset.split import SplitStrategy
from medscale.reproducibility import content_hash

__all__ = ["SplitAssignmentFreeze"]

_FREEZE_KIND = "medscale.dataset.split_assignment_freeze"
_SUPPORTED_VERSION = "split-freeze/v1"


def _require_sequence(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence):
        raise TypeError(
            f"{label} must be a sequence of strings, got {type(value).__name__}"
        )
    identifiers: list[str] = []
    for index, item in enumerate(value):
        _validate_identifier(item, f"{label}[{index}]")
        identifiers.append(str(item))
    return tuple(identifiers)


def _identity_payload(
    *,
    contract_version: str,
    source_dataset_fingerprint: str,
    strategy: SplitStrategy,
    seed: int,
    train: tuple[str, ...],
    validation: tuple[str, ...],
    test: tuple[str, ...],
) -> dict[str, object]:
    if contract_version != _SUPPORTED_VERSION:
        raise ValueError(
            f"unsupported contract_version {contract_version!r}; "
            f"expected {_SUPPORTED_VERSION!r}"
        )
    return {
        "contract_version": contract_version,
        "kind": _FREEZE_KIND,
        "seed": seed,
        "source_dataset_fingerprint": source_dataset_fingerprint,
        "strategy": strategy.value,
        "test": sorted(test),
        "train": sorted(train),
        "validation": sorted(validation),
    }


@dataclass(frozen=True)
class SplitAssignmentFreeze:
    """Immutable deterministic split-assignment freeze contract."""

    source_dataset_fingerprint: str
    strategy: SplitStrategy
    seed: int
    train: tuple[str, ...] = field(default_factory=tuple)
    validation: tuple[str, ...] = field(default_factory=tuple)
    test: tuple[str, ...] = field(default_factory=tuple)
    contract_version: str = _SUPPORTED_VERSION

    def __post_init__(self) -> None:
        if self.contract_version != _SUPPORTED_VERSION:
            raise ValueError(
                f"unsupported contract_version {self.contract_version!r}; "
                f"expected {_SUPPORTED_VERSION!r}"
            )
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise TypeError(
                f"seed must be an int, got {type(self.seed).__name__}: {self.seed!r}"
            )
        if not isinstance(self.strategy, SplitStrategy):
            raise TypeError(
                "strategy must be a SplitStrategy, got "
                f"{type(self.strategy).__name__}: {self.strategy!r}"
            )
        _validate_identifier(
            self.source_dataset_fingerprint, "source_dataset_fingerprint"
        )
        train = _require_sequence(self.train, "train")
        validation = _require_sequence(self.validation, "validation")
        test = _require_sequence(self.test, "test")
        seen: dict[str, str] = {}
        for split_name, identifiers in (
            ("train", train),
            ("validation", validation),
            ("test", test),
        ):
            for identifier in identifiers:
                if identifier in seen:
                    conflict_split = seen[identifier]
                    raise ValueError(
                        f"record identifier {identifier!r} appears in both "
                        f"{conflict_split} and {split_name}"
                    )
                seen[identifier] = split_name
        if not train and not validation and not test:
            raise ValueError(
                "assignment must include at least one record identifier across train, "
                "validation, and test"
            )
        object.__setattr__(self, "train", train)
        object.__setattr__(self, "validation", validation)
        object.__setattr__(self, "test", test)

    @property
    def assignment_count(self) -> int:
        return len(self.train) + len(self.validation) + len(self.test)

    @property
    def freeze_fingerprint(self) -> str:
        return content_hash(
            {
                "contract_version": self.contract_version,
                "kind": _FREEZE_KIND,
                "seed": self.seed,
                "source_dataset_fingerprint": self.source_dataset_fingerprint,
                "strategy": self.strategy.value,
                "test": sorted(self.test),
                "train": sorted(self.train),
                "validation": sorted(self.validation),
            }
        )
