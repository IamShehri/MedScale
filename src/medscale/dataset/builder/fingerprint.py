"""Deterministic fingerprint utilities for the dataset builder."""

from __future__ import annotations

from medscale.dataset.builder.contracts import PipelineContext, StageResult
from medscale.reproducibility import content_hash

__all__ = [
    "context_fingerprint",
    "pipeline_fingerprint",
]


def _stage_result_payload(result: StageResult) -> dict[str, object]:
    """Return the deterministic identity payload for a single pipeline stage result."""

    return {
        "stage_name": result.stage_name,
        "input_count": result.input_count,
        "accepted": result.accepted,
        "rejected": result.rejected,
        "artifacts": sorted(result.artifacts),
    }


def pipeline_fingerprint(results: tuple[StageResult, ...]) -> str:
    """Compute a deterministic fingerprint from pipeline stage results.

    Identity-bearing fields:
        stage_name, input_count, accepted, rejected, artifacts

    Non-identity fields are intentionally excluded:
        metadata
    """

    payload = [_stage_result_payload(result) for result in results]
    return content_hash(payload)


def context_fingerprint(context: PipelineContext) -> str:
    """Compute a deterministic fingerprint from a pipeline context.

    Identity-bearing fields:
        config, results, bundle_references, validation_statuses

    Non-identity fields are intentionally excluded:
        root, metadata
    """

    payload = {
        "config": dict(context.config),
        "results": [_stage_result_payload(result) for result in context.results],
        "bundle_references": sorted(context.bundle_references),
        "validation_statuses": dict(sorted(context.validation_statuses.items())),
    }
    return content_hash(payload)
