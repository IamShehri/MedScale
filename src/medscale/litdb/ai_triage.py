"""AI Triage Assistant v0.1 — advisory prioritization layer.

Stability: **audit-first advisory module**.

Responsibilities:
- Read pending records from the corpus.
- Apply deterministic flags (no automatic exclusion).
- Detect healthcare domain ontology signals.
- Compute priority and relevance scores.
- Produce structured reason codes and advisory recommendation.
- Write outputs to a separate AI audit log, never touching human review logs.

NOT a replacement for human screening. NOT an automatic include/exclude engine.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal

from medscale._runtime import git_sha, utc_now
from medscale.litdb.records import LiteratureRecord
from medscale.litdb.store import load_corpus
from medscale.litdb.review import current_reviews
from medscale.reproducibility import canonical_json

__all__ = [
    "AI_TRIAGE_SIGNALS",
    "DeterministicFlag",
    "OntologySignal",
    "TriageRecord",
    "AIRecommendation",
    "load_triage_log",
    "append_recommendations",
    "score_triage",
    "build_recommendation",
    "pending_for_triage",
    "_priority_label",
    "_recommendation_from_scores",
]


# Deterministic rule identifiers used in logs and prompts.
RULE_HAS_ABSTRACT: Final = "HAS_ABSTRACT"
RULE_HAS_IDENTIFIER: Final = "HAS_IDENTIFIER"
RULE_EVIDENCE_TIER: Final = "EVIDENCE_TIER"
RULE_YEAR_RANGE: Final = "YEAR_RANGE"

# Public signal vocabulary used as structured reason codes and CLI display labels.
AI_TRIAGE_SIGNALS: Final[tuple[str, ...]] = (
    "FHIR",
    "HL7",
    "OHDSI",
    "EHR",
    "CLINICAL_NLP",
    "MEDICAL_AI",
    "CLINICAL_DECISION_SUPPORT",
    "HEALTHCARE_INTEROPERABILITY",
    "BIOMEDICAL_AI",
)

# Default ontology matchers: case-insensitive regex fragments over title+abstract.
_ONTOLOGY_PATTERNS: Final[dict[str, str]] = {
    "FHIR": r"fhir|fast healthcare interoperability resources",
    "HL7": r"\bhl7\b|health level seven",
    "OHDSI": r"\bohdsi\b|observational health data sciences and informatics",
    "EHR": r"\behr\b|electronic health record",
    "CLINICAL_NLP": r"clinical nlp|clinical natural language processing",
    "MEDICAL_AI": r"medical ai|medical artificial intelligence",
    "CLINICAL_DECISION_SUPPORT": r"clinical decision support|\bcds\b",
    "HEALTHCARE_INTEROPERABILITY": r"healthcare interoperability",
    "BIOMEDICAL_AI": r"biomedical ai",
}

_DEFAULT_ONTOLOGY_RE: Final[re.Pattern[str]] = re.compile(
    "|".join(f"(?P<{key}>{pattern})" for key, pattern in _ONTOLOGY_PATTERNS.items()),
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class DeterministicFlag:
    """Deterministic pre-screening annotation.

    These are informational only. They never directly cause exclusion.
    """

    rule: str
    severity: Literal["review_required", "monitor"]


@dataclass(frozen=True)
class OntologySignal:
    """Detected healthcare domain ontology signal."""

    signal: str
    severity: Literal["monitor"] = "monitor"


@dataclass(frozen=True)
class TriageRecord:
    """A LiteratureRecord augmented with triage metadata."""

    record: LiteratureRecord
    deterministic_flags: tuple[DeterministicFlag, ...] = ()
    ontology_signals: tuple[str, ...] = ()
    priority_score: float = 0.0
    relevance_score: float = 0.0


@dataclass(frozen=True)
class AIRecommendation:
    """One AI triage recommendation written to the audit log."""

    record_id: str
    recommendation: Literal["review first", "review later", "low priority", "uncertain"]
    confidence: float
    reasoning: str
    reason_codes: tuple[str, ...]
    matched_rules: tuple[str, ...]
    model: str | None = None
    provider: str | None = None
    timestamp: str | None = None
    agent_version: str = "medscale-ai-triage-v0.1"
    git_sha: str | None = None
    deterministic_flags: tuple[dict[str, Any], ...] = ()
    ontology_signals: tuple[str, ...] = ()
    priority_score: float = 0.0
    relevance_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "record_id": self.record_id,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "reason_codes": list(self.reason_codes),
            "matched_rules": list(self.matched_rules),
            "model": self.model,
            "provider": self.provider,
            "timestamp": self.timestamp,
            "agent_version": self.agent_version,
            "git_sha": self.git_sha,
            "deterministic_flags": [
                {"rule": flag["rule"], "severity": flag["severity"]}
                for flag in self.deterministic_flags
            ],
            "ontology_signals": list(self.ontology_signals),
            "priority_score": self.priority_score,
            "relevance_score": self.relevance_score,
        }


def _dict_to_recommendation(payload: dict[str, Any]) -> AIRecommendation:
    return AIRecommendation(
        record_id=str(payload["record_id"]),
        recommendation=str(payload["recommendation"]),
        confidence=float(payload["confidence"]),
        reasoning=str(payload.get("reasoning", "")),
        reason_codes=tuple(payload.get("reason_codes", [])),
        matched_rules=tuple(payload.get("matched_rules", [])),
        model=payload.get("model"),
        provider=payload.get("provider"),
        timestamp=payload.get("timestamp"),
        agent_version=str(payload.get("agent_version", "medscale-ai-triage-v0.1")),
        git_sha=payload.get("git_sha"),
        deterministic_flags=tuple(payload.get("deterministic_flags", [])),
        ontology_signals=tuple(payload.get("ontology_signals", [])),
        priority_score=float(payload.get("priority_score", 0.0)),
        relevance_score=float(payload.get("relevance_score", 0.0)),
    )


def pending_for_triage(
    corpus: tuple[LiteratureRecord, ...],
    reviews: dict[str, Any],
    *,
    query: str | None = None,
    limit: int | None = None,
) -> list[TriageRecord]:
    """Return records still pending human review, preserving corpus order.

    Deterministic: same inputs -> same output.
    """

    queue: list[TriageRecord] = []
    for record in corpus:
        if query is not None and query not in record.tags:
            continue
        review = reviews.get(record.record_id)
        if review is not None and review.decision.value != "pending":
            continue
        queue.append(TriageRecord(record=record))
        if limit is not None and len(queue) >= limit:
            break
    return queue


def load_triage_log(path: Path) -> dict[str, AIRecommendation]:
    """Replay the triage log, latest entry per record wins."""

    if not path.exists():
        return {}
    recommendations: dict[str, AIRecommendation] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        payload = json.loads(stripped)
        recommendations[payload["record_id"]] = _dict_to_recommendation(payload)
    return recommendations


def append_recommendations(
    log_path: Path, recommendations: Iterable[AIRecommendation]
) -> None:
    """Append recommendations to the triage log in canonical JSONL form."""

    items = list(recommendations)
    if not items:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [canonical_json(item.to_dict()) for item in items]
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def _append_flag(
    flags: list[DeterministicFlag],
    rule: str,
    severity: Literal["review_required", "monitor"],
) -> None:
    flags.append(DeterministicFlag(rule=rule, severity=severity))


def _text(record: LiteratureRecord) -> str:
    parts = [record.title or "", " ", record.abstract or ""]
    return " ".join(parts)


def detect_deterministic_flags(record: LiteratureRecord) -> list[DeterministicFlag]:
    """Compute deterministic flags for a record.

    These are informational only. They never cause automatic exclusion.
    """

    flags: list[DeterministicFlag] = []
    text = _text(record)

    if not record.abstract or not record.abstract.strip():
        _append_flag(flags, RULE_HAS_ABSTRACT, "review_required")

    if not any(
        [
            record.identifiers.doi,
            record.identifiers.pmid,
            record.identifiers.arxiv_id,
            record.identifiers.s2_corpus_id,
        ]
    ):
        _append_flag(flags, RULE_HAS_IDENTIFIER, "review_required")

    tier = record.evidence_tier.value if record.evidence_tier else None
    if tier not in {"peer-reviewed", "preprint"}:
        _append_flag(flags, RULE_EVIDENCE_TIER, "monitor")

    year = record.year
    if year is None or year < 2015:
        _append_flag(flags, RULE_YEAR_RANGE, "monitor")

    return flags


def detect_ontology_signals(text: str) -> list[str]:
    """Detect healthcare domain ontology signals from free text."""

    signals: list[str] = []
    seen: set[str] = set()
    for match in _DEFAULT_ONTOLOGY_RE.finditer(text):
        name = match.lastgroup
        if name and name not in seen:
            seen.add(name)
            signals.append(name)
    return signals


def score_triage(record: TriageRecord) -> tuple[float, float]:
    """Heuristic scoring for priority and relevance.

    - priority_score: higher => review earlier.
    - relevance_score: higher => more aligned with MedScale themes.

    Stability: deterministic given the same record and deterministic pre-screen.
    """

    text = _text(record.record)
    lower_text = text.lower()
    tier = (record.record.evidence_tier.value or "").lower()

    # Base scores
    priority = 0.2
    relevance = 0.2

    # Evidence tier influence
    if tier == "peer-reviewed":
        priority += 0.2
        relevance += 0.1
    elif tier == "preprint":
        priority += 0.1
        relevance += 0.05

    # Completeness
    if record.record.abstract and len(record.record.abstract.strip()) > 200:
        priority += 0.1
        relevance += 0.05

    identifiers = [
        record.record.identifiers.doi,
        record.record.identifiers.pmid,
        record.record.identifiers.arxiv_id,
        record.record.identifiers.s2_corpus_id,
    ]
    if any(identifiers):
        priority += 0.05
        relevance += 0.05

    # Ontology signal coverage
    signals = record.ontology_signals
    signal_count = len(signals)
    priority += min(signal_count * 0.08, 0.4)
    relevance += min(signal_count * 0.1, 0.5)

    # Deterministic flags: issues slightly reduce priority for triage clarity.
    flag_count = len(record.deterministic_flags)
    priority -= min(flag_count * 0.05, 0.25)

    # Year recency
    year = record.record.year
    if year is not None and year >= 2023:
        priority += 0.1
        relevance += 0.05

    return max(0.0, min(1.0, priority)), max(0.0, min(1.0, relevance))


def _priority_label(priority_score: float) -> str:
    if priority_score >= 0.7:
        return "HIGH"
    if priority_score >= 0.45:
        return "MEDIUM"
    if priority_score >= 0.25:
        return "LOW"
    return "LOW"


def _recommendation_from_scores(
    priority_score: float, relevance_score: float
) -> Literal["review first", "review later", "low priority", "uncertain"]:
    if priority_score >= 0.7 and relevance_score >= 0.55:
        return "review first"
    if priority_score >= 0.45 and relevance_score >= 0.35:
        return "review later"
    if priority_score >= 0.25:
        return "low priority"
    return "uncertain"


def _confidence_from_scores(
    priority_score: float, relevance_score: float, signal_count: int
) -> float:
    raw = 0.35 + (priority_score * 0.35) + (relevance_score * 0.2) + (min(signal_count, 5) * 0.02)
    return max(0.0, min(1.0, raw))


def _recommendation_reasoning(
    record: LiteratureRecord,
    flags: list[DeterministicFlag],
    signals: list[str],
    priority_score: float,
    relevance_score: float,
    recommendation: str,
) -> str:
    parts: list[str] = []
    if signals:
        parts.append(
            f"Strong alignment with MedScale research themes: {', '.join(signals)}."
        )
    if flags:
        parts.append(
            f"Review attention needed for: {', '.join(flag.rule for flag in flags)}."
        )
    if recommendation == "review first":
        parts.append(
            "High priority: early human review is recommended."
        )
    elif recommendation == "review later":
        parts.append(
            "Suggested for standard queue review after higher-priority items."
        )
    elif recommendation == "low priority":
        parts.append(
            "Lower clinical/interoperability alignment; review after prioritized items."
        )
    else:
        parts.append(
            "Insufficient deterministic signal for confident prioritization."
        )
    return " ".join(parts)


def _derive_reason_codes(
    signals: list[str], flags: list[DeterministicFlag], record: LiteratureRecord
) -> list[str]:
    codes = list(signals)
    for flag in flags:
        if flag.rule == RULE_HAS_ABSTRACT and "PRIMARY_RESEARCH" not in codes:
            codes.append("PRIMARY_RESEARCH")
        if flag.rule == RULE_EVIDENCE_TIER and "PEER_REVIEWED" not in codes:
            tier = (record.evidence_tier.value or "").lower()
            if tier == "peer-reviewed":
                codes.append("PEER_REVIEWED")
    seen: set[str] = set()
    deduped: list[str] = []
    for code in codes:
        if code not in seen:
            seen.add(code)
            deduped.append(code)
    return deduped


def build_recommendation(
    record: TriageRecord,
    *,
    model: str | None = None,
    provider: str | None = None,
    agent_version: str = "medscale-ai-triage-v0.1",
) -> AIRecommendation:
    """Build an AIRecommendation for a single triage record.

    Deterministic path: no LLM is required for v0.1. An optional model/provider
    may be recorded for traceability and future model-as-judge expansion.
    """

    priority_score, relevance_score = score_triage(record)
    recommendation = _recommendation_from_scores(priority_score, relevance_score)
    confidence = _confidence_from_scores(
        priority_score, relevance_score, len(record.ontology_signals)
    )
    reasoning = _recommendation_reasoning(
        record.record,
        list(record.deterministic_flags),
        list(record.ontology_signals),
        priority_score,
        relevance_score,
        recommendation,
    )
    reason_codes = _derive_reason_codes(
        list(record.ontology_signals), record.deterministic_flags, record.record
    )
    matched_rules = list(
        dict.fromkeys(
            [flag.rule for flag in record.deterministic_flags] + list(record.ontology_signals)
        )
    )

    return AIRecommendation(
        record_id=record.record.record_id,
        recommendation=recommendation,
        confidence=round(confidence, 4),
        reasoning=reasoning,
        reason_codes=tuple(reason_codes),
        matched_rules=tuple(matched_rules),
        model=model,
        provider=provider,
        timestamp=utc_now(),
        agent_version=agent_version,
        git_sha=git_sha(),
        deterministic_flags=tuple(
            {"rule": flag.rule, "severity": flag.severity} for flag in record.deterministic_flags
        ),
        ontology_signals=tuple(record.ontology_signals),
        priority_score=round(priority_score, 4),
        relevance_score=round(relevance_score, 4),
    )

