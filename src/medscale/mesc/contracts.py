"""Deterministic Pilot-01 scientific identity contracts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

SCHEMA_VERSION = "mesc-pilot-01/1"


def _sorted_json(payload: object) -> str:
    import json

    return json.dumps(payload, sort_keys=True, ensure_ascii=True)


@dataclass(frozen=True)
class PilotSourceIdentity:
    dataset_id: str
    dataset_revision: str
    configuration: str
    original_example_id: str
    source_document_id: str
    license_id: str


@dataclass(frozen=True)
class PilotEvidence:
    evidence_id: str
    sentence_index: int
    text: str
    source_document_id: str


@dataclass(frozen=True)
class PilotClaim:
    claim_id: str
    text: str
    evidence_ids: tuple[str, ...]
    annotation_status: str


@dataclass(frozen=True)
class PilotTarget:
    decision: str
    answer: str | None
    claims: tuple[PilotClaim, ...]
    evidence_sufficiency: str
    uncertainty: str
    abstain: bool = False
    abstention_reason: str | None = None


@dataclass(frozen=True)
class PilotProvenance:
    transformation_version: str
    annotation_method: str
    annotation_revision: str
    synthetic: bool = False


@dataclass(frozen=True)
class PilotRecord:
    schema_version: str
    example_id: str
    source: PilotSourceIdentity
    question: str
    evidence: tuple[PilotEvidence, ...]
    target: PilotTarget
    provenance: PilotProvenance

    def content_hash(self) -> str:
        payload = {
            "schema_version": self.schema_version,
            "example_id": self.example_id,
            "source": {
                "dataset_id": self.source.dataset_id,
                "dataset_revision": self.source.dataset_revision,
                "configuration": self.source.configuration,
                "original_example_id": self.source.original_example_id,
                "source_document_id": self.source.source_document_id,
                "license_id": self.source.license_id,
            },
            "question": self.question,
            "evidence": [
                {
                    "evidence_id": evidence.evidence_id,
                    "sentence_index": evidence.sentence_index,
                    "text": evidence.text,
                    "source_document_id": evidence.source_document_id,
                }
                for evidence in self.evidence
            ],
            "target": {
                "decision": self.target.decision,
                "answer": self.target.answer,
                "claims": [
                    {
                        "claim_id": claim.claim_id,
                        "text": claim.text,
                        "evidence_ids": list(claim.evidence_ids),
                        "annotation_status": claim.annotation_status,
                    }
                    for claim in self.target.claims
                ],
                "evidence_sufficiency": self.target.evidence_sufficiency,
                "uncertainty": self.target.uncertainty,
                "abstain": self.target.abstain,
                "abstention_reason": self.target.abstention_reason,
            },
            "provenance": {
                "transformation_version": self.provenance.transformation_version,
                "annotation_method": self.provenance.annotation_method,
                "annotation_revision": self.provenance.annotation_revision,
                "synthetic": self.provenance.synthetic,
            },
        }
        canonical = _sorted_json(payload)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
