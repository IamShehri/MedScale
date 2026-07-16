"""Run manifest for Pilot-01 deterministic evaluation runs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PilotRunManifest:
    """Captures the inputs for one deterministic evaluation run."""

    schema_version: str
    run_id: str
    records: tuple[object, ...]
    model_family: str
    primary_model_id: str
    fallback_model_id: str | None = None
    dataset_id: str = "qiaojin/PubMedQA"
    configuration: str = "pqa_labeled"
    note: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "model_family": self.model_family,
            "primary_model_id": self.primary_model_id,
            "fallback_model_id": self.fallback_model_id,
            "dataset_id": self.dataset_id,
            "configuration": self.configuration,
            "record_count": len(self.records),
            "note": self.note,
        }
