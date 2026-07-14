"""Deterministic fingerprint utilities for the dataset builder."""

from __future__ import annotations

from medscale.dataset.builder.contracts import PipelineContext, StageResult
from medscale.reproducibility import content_hash


def pipeline_fingerprint(results: tuple[StageResult, ...]) -> str:
    """Compute a deterministic fingerprint from pipeline stage results."""
    payload = [
        {
            "stage_name": result.stage_name,
            "accepted": result.accepted,
            "rejected": result.rejected,
            "artifacts": sorted(result.artifacts),
        }
        for result in results
    ]
    return content_hash(payload)


def context_fingerprint(context: PipelineContext) -> str:
    """Compute a deterministic fingerprint from a pipeline context."""
    payload = {
        "root": context.root,
        "config": dict(context.config),
        "result_count": len(context.results),
        "bundle_references": sorted(context.bundle_references),
        "validation_statuses": dict(sorted(context.validation_statuses.items())),
    }
    return content_hash(payload)
