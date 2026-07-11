"""Deterministic claim-verification: the rule-based slice of the verification engine.

Verification in MedScale is never a vibe — it is a named check with a pass/fail and a
reason. This module implements the two checks that are mechanically decidable today,
and uses them to advance evidence through the ADR-0009 state machine by RULE:

- **source reference check** — the object's ``source_record_id`` resolves to a live
  corpus record (no orphaned evidence, ever);
- **provenance anchor check** — the object's ``raw_response_sha256`` matches a payload
  hash actually recorded in a committed round manifest: the claim's provenance chain
  bottoms out in archived bytes, not in an assertion.

``rule_verify_source`` advances ``UNVERIFIED -> SOURCE_VERIFIED`` only when every check
passes. ``EXTRACTION_VERIFIED`` remains a human act (a model or rule re-reading its own
extraction is exactly what ADR-0009 forbids to shortcut).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import medscale._layout as _layout
from medscale.evidence import EvidenceObject, VerificationState

__all__ = [
    "CheckResult",
    "archived_payload_hashes",
    "provenance_anchor_check",
    "rule_verify_source",
    "source_reference_check",
]


@dataclass(frozen=True)
class CheckResult:
    """One named, deterministic verification check outcome."""

    check: str
    passed: bool
    reason: str


def source_reference_check(obj: EvidenceObject, corpus_ids: frozenset[str]) -> CheckResult:
    if obj.source_record_id is None:
        return CheckResult("source_reference", False, "evidence has no source_record_id")
    if obj.source_record_id not in corpus_ids:
        return CheckResult(
            "source_reference",
            False,
            f"source_record_id {obj.source_record_id[:12]}... not found in corpus",
        )
    return CheckResult("source_reference", True, "source record resolves in corpus")


def archived_payload_hashes(root: Path) -> frozenset[str]:
    """Every payload SHA-256 recorded by any committed round manifest under ``root``."""
    hashes: set[str] = set()
    manifests_dir = _layout.manifests_dir(root)
    if not manifests_dir.exists():
        return frozenset()
    for manifest_path in sorted(manifests_dir.glob("*.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest.get("entries", []):
            hashes.add(str(entry["payload_sha256"]))
    return frozenset(hashes)


def provenance_anchor_check(obj: EvidenceObject, known_hashes: frozenset[str]) -> CheckResult:
    if obj.provenance.raw_response_sha256 in known_hashes:
        return CheckResult(
            "provenance_anchor", True, "raw-response hash matches an archived payload"
        )
    return CheckResult(
        "provenance_anchor",
        False,
        "raw_response_sha256 matches no archived payload in any round manifest",
    )


def rule_verify_source(
    obj: EvidenceObject,
    corpus_ids: frozenset[str],
    known_hashes: frozenset[str],
) -> tuple[EvidenceObject, tuple[CheckResult, ...]]:
    """Run all source checks; advance to SOURCE_VERIFIED iff every one passes.

    Returns ``(possibly-advanced object, all check results)``. Never raises on a
    failed check — failure is a result, not an exception; callers decide what a
    failing object may do next. Objects already past UNVERIFIED are returned unchanged
    (re-verification is idempotent).
    """
    results = (
        source_reference_check(obj, corpus_ids),
        provenance_anchor_check(obj, known_hashes),
    )
    if obj.verification is not VerificationState.UNVERIFIED:
        return obj, results
    if all(result.passed for result in results):
        return obj.with_verification(VerificationState.SOURCE_VERIFIED), results
    return obj, results
