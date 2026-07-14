"""Immutable contracts for the dataset builder pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "PipelineContext",
    "StageDefinition",
    "StageResult",
]


def _freeze(value: object) -> Any:
    if isinstance(value, dict):
        return _FrozenMapping({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        raise TypeError(f"sets are not JSON-compatible: {value!r}")
    return value


class _FrozenMapping(dict[str, Any]):
    """Immutable, JSON-compatible mapping."""

    def _raise(self) -> Any:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def __setitem__(self, key: object, value: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def __delitem__(self, key: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def pop(self, *args: object, **kwargs: object) -> Any:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def popitem(self, *args: object, **kwargs: object) -> tuple[Any, Any]:
        raise TypeError("FrozenMapping objects do not support item assignment")

    def setdefault(
        self,
        *args: object,
        **kwargs: object,
    ) -> Any:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def update(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def clear(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")


def _validate_identifier(name: str, label: str) -> None:
    if not isinstance(name, str):
        raise TypeError(f"{label} must be a non-empty string, got {type(name).__name__}: {name!r}")
    if not name.strip():
        raise ValueError(f"{label} must be a non-empty string, got {name!r}")


def _validate_counts(**kwargs: object) -> None:
    for name, value in kwargs.items():
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an int, got {type(value).__name__}")
        if value < 0:
            raise ValueError(f"{name} must be non-negative, got {value}")


def _validate_boolean(name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}: {value!r}")


def _validate_tuple_members(value: tuple[object, ...], expected_type: type, label: str) -> None:
    for entry in value:
        if not isinstance(entry, expected_type):
            raise TypeError(
                f"{label} members must be {expected_type.__name__}, "
                f"got {type(entry).__name__}: {entry!r}"
            )


def _validate_mapping(value: object, label: str) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a dict, got {type(value).__name__}")
    for key in value:
        if not isinstance(key, str):
            raise TypeError(f"{label} keys must be str, got {type(key).__name__}: {key!r}")


def _validate_json_compatible_mapping(value: object, label: str) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a dict, got {type(value).__name__}")
    for key, item in value.items():
        if not isinstance(key, str):
            raise TypeError(f"{label} keys must be str, got {type(key).__name__}: {key!r}")
        _validate_json_scalar(f"{label}[{key!r}]", item)


def _validate_json_scalar(label: str, value: object) -> None:
    if value is None or isinstance(value, (bool, int, str)):
        return
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError(f"{label} must be a finite scalar, got {value!r}")
        return
    if isinstance(value, (_FrozenMapping, dict)):
        _validate_json_compatible_mapping(value, label)
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _validate_json_scalar(f"{label}[{index}]", item)
        return
    raise TypeError(f"{label} must be JSON-compatible, got {type(value).__name__}: {value!r}")


def _validate_proportions(value: dict[str, float], label: str) -> None:
    for key, item in value.items():
        if not isinstance(item, (int, float)):
            raise TypeError(f"{label}[{key!r}] must be a float, got {type(item).__name__}")
        if float(item) < 0.0 or float(item) > 1.0:
            raise ValueError(f"{label}[{key!r}] must be within [0.0, 1.0], got {item}")


@dataclass(frozen=True)
class StageResult:
    """Deterministic result for a single pipeline stage execution."""

    stage_name: str
    input_count: int
    accepted: int
    rejected: int
    artifacts: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_identifier(self.stage_name, "stage_name")
        _validate_counts(
            input_count=self.input_count,
            accepted=self.accepted,
            rejected=self.rejected,
        )
        _validate_counts(rejection_count=self.rejected)
        _validate_tuple_members(self.artifacts, str, "artifacts")
        _validate_json_compatible_mapping(self.metadata, "metadata")
        object.__setattr__(self, "metadata", _freeze(self.metadata))


@dataclass(frozen=True)
class StageDefinition:
    """Declarative description of a pipeline stage."""

    name: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_identifier(self.name, "name")
        _validate_tuple_members(self.inputs, str, "inputs")
        _validate_tuple_members(self.outputs, str, "outputs")


@dataclass(frozen=True)
class PipelineContext:
    """Immutable execution context passed through the pilot slice."""

    root: str
    config: dict[str, Any] = field(default_factory=dict)
    results: tuple[StageResult, ...] = ()
    bundle_references: tuple[str, ...] = ()
    validation_statuses: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_json_compatible_mapping(self.config, "config")
        _validate_tuple_members(self.results, StageResult, "results")
        _validate_tuple_members(self.bundle_references, str, "bundle_references")
        _validate_mapping(self.validation_statuses, "validation_statuses")
        _validate_json_compatible_mapping(self.metadata, "metadata")
        object.__setattr__(self, "config", _freeze(self.config))
        object.__setattr__(self, "results", tuple(self.results))
        object.__setattr__(self, "bundle_references", tuple(self.bundle_references))
        object.__setattr__(self, "validation_statuses", _freeze(self.validation_statuses))
        object.__setattr__(self, "metadata", _freeze(self.metadata))
