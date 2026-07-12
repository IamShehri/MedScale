"""Verification-state protocol for evidence systems.

Stability: internal. The protocol is consumed by the benchmark and research
modules; implementation details may change under the accepted layer boundary
policy, but the protocol surface is part of the public verification contract.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from medscale.evidence.models import VerificationState


@runtime_checkable
class EvidenceSystem(Protocol):
    """The model-agnostic verification contract (ADR-0015 pattern).

    A backend participates by implementing this protocol; nothing downstream
    (benchmark runners, experiment pipelines, training recipes) may depend on
    any concrete backend implementation.
    """

    def advance_verification(
        self,
        evidence_id: str,
        target: VerificationState,
        *,
        checked_by: str | None = None,
    ) -> tuple[bool, str]:
        """Attempt to advance ``evidence_id`` to ``target``.

        Returns ``(advanced, reason)``. ``advanced`` is ``True`` iff the state
        machine transition succeeded; ``reason`` is a human-readable audit note.
        """
        ...


__all__ = ["EvidenceSystem"]
