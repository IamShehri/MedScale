"""Deterministic Pilot-01 split contracts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

_DECISION = Literal["yes", "no", "maybe", "abstain"]
_SPLIT = Literal["train", "validation", "test", "holdout"]


@dataclass(frozen=True)
class PilotSplitAssignment:
    example_id: str
    split: _SPLIT
    source_document_id: str
    partition_key: str = ""

    @property
    def is_train(self) -> bool:
        return self.split == "train"

    @property
    def is_validation(self) -> bool:
        return self.split == "validation"

    @property
    def is_test(self) -> bool:
        return self.split == "test"

    @property
    def is_holdout(self) -> bool:
        return self.split == "holdout"


@dataclass(frozen=True)
class PilotSplitManifest:
    split_assignments: tuple[PilotSplitAssignment, ...]
    split_hash: str = ""
    split_seed: str = "mesc-pilot-01"
    note: str | None = None

    @property
    def train_example_ids(self) -> tuple[str, ...]:
        return tuple(
            assignment.example_id for assignment in self.split_assignments if assignment.is_train
        )

    @property
    def validation_example_ids(self) -> tuple[str, ...]:
        return tuple(
            assignment.example_id
            for assignment in self.split_assignments
            if assignment.is_validation
        )

    @property
    def test_example_ids(self) -> tuple[str, ...]:
        return tuple(
            assignment.example_id for assignment in self.split_assignments if assignment.is_test
        )

    @property
    def holdout_example_ids(self) -> tuple[str, ...]:
        return tuple(
            assignment.example_id for assignment in self.split_assignments if assignment.is_holdout
        )

    @property
    def computed_split_hash(self) -> str:
        if self.split_hash:
            return self.split_hash
        canonical = self._canonical_payload()
        return hashlib.sha256(json.dumps(canonical, sort_keys=True).encode("utf-8")).hexdigest()[
            :16
        ]

    def _canonical_payload(self) -> object:
        return {
            "split_seed": self.split_seed,
            "assignments": [
                {
                    "example_id": assignment.example_id,
                    "split": assignment.split,
                    "source_document_id": assignment.source_document_id,
                    "partition_key": assignment.partition_key,
                }
                for assignment in self.split_assignments
            ],
        }


class PilotSplitNotAuthorizedError(NotImplementedError):
    """Raised when unimplemented Pilot-01 split allocation is invoked.

    The real source-document-grouped allocation algorithm is P01-04B scope and
    must not exist — even as a silent placeholder — before that stage is
    formally authorized.
    """


class SourceDocumentGroupedSplitter:
    """Placeholder for the P01-04B source-document-grouped split allocator.

    The data-model classes above (``PilotSplitAssignment``,
    ``PilotSplitManifest``) are stable contracts. Allocation itself is NOT
    implemented: an earlier stub silently assigned every example to ``train``,
    which is indistinguishable from a real split manifest downstream. Until
    P01-04B is authorized and the founder-ratified split policy is implemented,
    ``assign`` refuses to run.
    """

    def __init__(self, seed: str = "mesc-pilot-01") -> None:
        self.seed = seed

    def assign(
        self, example_ids: Sequence[str], source_document_ids: Sequence[str]
    ) -> PilotSplitManifest:
        raise PilotSplitNotAuthorizedError(
            "SourceDocumentGroupedSplitter.assign is not implemented: real split "
            "allocation is P01-04B scope and requires explicit authorization. "
            "Refusing to fabricate split assignments."
        )


@dataclass(frozen=True)
class PilotLeakageFinding:
    example_id: str
    duplicate_type: str
    match_example_id: str
    similarity: float
    shared_surface: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "example_id": self.example_id,
            "duplicate_type": self.duplicate_type,
            "match_example_id": self.match_example_id,
            "similarity": self.similarity,
            "shared_surface": list(self.shared_surface),
        }


@dataclass(frozen=True)
class PilotLeakageAuditReport:
    findings: tuple[PilotLeakageFinding, ...]
    leaked: bool = False

    @property
    def finding_count(self) -> int:
        return len(self.findings)

    def to_dict(self) -> dict[str, object]:
        return {
            "findings": [finding.to_dict() for finding in self.findings],
            "leaked": self.leaked,
            "finding_count": self.finding_count,
        }


PilotLeakageAudit = PilotLeakageAuditReport
