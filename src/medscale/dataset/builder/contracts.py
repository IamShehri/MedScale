"""Immutable contracts for the dataset builder pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class StageResult:
    """Deterministic result for a single pipeline stage execution."""

    stage_name: str
    input_count: int
    accepted: int
    rejected: int
    artifacts: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StageDefinition:
    """Declarative description of a pipeline stage."""

    name: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class PipelineContext:
    """Immutable execution context passed through the pilot slice."""

    root: str
    config: dict[str, Any] = field(default_factory=dict)
    results: tuple[StageResult, ...] = ()
    bundle_references: tuple[str, ...] = ()
    validation_statuses: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
