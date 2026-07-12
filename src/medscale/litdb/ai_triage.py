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
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal, cast

from medscale._runtime import git_sha, utc_now
from medscale.litdb.records import LiteratureRecord
from medscale.reproducibility import canonical_json

__all__ = [
    "AI_TRIAGE_SIGNALS",
    "AIRecommendation",
    "DeterministicFlag",
    "OntologySignal",
    "TriageRecord",
    "_priority_label",
    "_recommendation_from_scores",
    "append_recommendations",
    "build_recommendation",
    "detect_deterministic_flags",
    "detect_ontology_signals",
    "load_triage_log",
    "pending_for_triage",
    "score_triage",
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
    """Informational pre-screen flag; never produces automatic exclusion."""

    rule: str
    severity: Literal["review_required", "monitor"]


@dataclass(frozen=True)
class OntologySignal:
    """Matched healthcare domain concept."""

    name: str
    matched_text: str


@dataclass(frozen=True)
class TriageRecord:
    record: LiteratureRecord
    deterministic_flags: tuple[DeterministicFlag, ...] = ()
    ontology_signals: tuple[str, ...] = ()
    priority_score: float = 0.0
    relevance_score: float = 0.0


@dataclass(frozen=True)
class AIRecommendation:
    record_id: str
    recommendation: Literal["review first", "review later", "low priority", "uncertain"]
    confidence: float
    reasoning: str
    reason_codes: tuple[str, ...] = ()
    matched_rules: tuple[str, ...] = ()
    timestamp: str = ""
    agent_version: str = ""
    git_sha: str = ""
    deterministic_flags: tuple[dict[str, str], ...] = ()
    ontology_signals: tuple[str, ...] = ()
    priority_score: float = 0.0
    relevance_score: float = 0.0
    model: str | None = None
    provider: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "format": 1,
            "record_id": self.record_id,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "reason_codes": list(self.reason_codes),
            "matched_rules": list(self.matched_rules),
            "timestamp": self.timestamp,
            "agent_version": self.agent_version,
            "git_sha": self.git_sha,
            "deterministic_flags": [dict(item) for item in self.deterministic_flags],
            "ontology_signals": list(self.ontology_signals),
            "priority_score": self.priority_score,
            "relevance_score": self.relevance_score,
            "model": self.model,
            "provider": self.provider,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> AIRecommendation:
        required = ("record_id", "recommendation", "confidence")
        missing = [key for key in required if key not in data]
        if missing:
            raise ValueError(f"AIRecommendation missing required fields: {missing}")

        record_id_raw = data["record_id"]
        if not isinstance(record_id_raw, str):
            raise TypeError("record_id must be a string")
        record_id = record_id_raw

        recommendation_raw = data["recommendation"]
        if not isinstance(recommendation_raw, str):
            raise TypeError("recommendation must be a string")
        allowed = {"review first", "review later", "low priority", "uncertain"}
        if recommendation_raw not in allowed:
            raise ValueError(f"Invalid recommendation: {recommendation_raw}")
        recommendation = cast(
            Literal["review first", "review later", "low priority", "uncertain"],
            recommendation_raw,
        )

        confidence_raw = data["confidence"]
        if not isinstance(confidence_raw, int | float):
            raise TypeError("confidence must be a number")
        confidence = float(confidence_raw)

        reasoning = str(data.get("reasoning", ""))

        raw_reason_codes = data.get("reason_codes", [])
        if not isinstance(raw_reason_codes, list):
            raise TypeError("reason_codes must be a list")
        reason_codes = tuple(str(code) for code in raw_reason_codes)

        raw_matched_rules = data.get("matched_rules", [])
        if not isinstance(raw_matched_rules, list):
            raise TypeError("matched_rules must be a list")
        matched_rules = tuple(str(rule) for rule in raw_matched_rules)

        timestamp = str(data.get("timestamp", ""))
        agent_version = str(data.get("agent_version", ""))
        git_sha = str(data.get("git_sha", ""))

        raw_deterministic_flags = data.get("deterministic_flags", [])
        if not isinstance(raw_deterministic_flags, list):
            raise TypeError("deterministic_flags must be a list")
        deterministic_flags = tuple(dict(item) for item in raw_deterministic_flags)

        raw_ontology_signals = data.get("ontology_signals", [])
        if not isinstance(raw_ontology_signals, list):
            raise TypeError("ontology_signals must be a list")
        ontology_signals = tuple(str(signal) for signal in raw_ontology_signals)

        priority_raw = data.get("priority_score", 0.0)
        if not isinstance(priority_raw, int | float):
            raise TypeError("priority_score must be a number")
        priority_score = float(priority_raw)

        relevance_raw = data.get("relevance_score", 0.0)
        if not isinstance(relevance_raw, int | float):
            raise TypeError("relevance_score must be a number")
        relevance_score = float(relevance_raw)

        model = str(data["model"]) if "model" in data else None
        provider = str(data["provider"]) if "provider" in data else None

        return cls(
            record_id=record_id,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            reason_codes=reason_codes,
            matched_rules=matched_rules,
            timestamp=timestamp,
            agent_version=agent_version,
            git_sha=git_sha,
            deterministic_flags=deterministic_flags,
            ontology_signals=ontology_signals,
            priority_score=priority_score,
            relevance_score=relevance_score,
            model=model,
            provider=provider,
        )


def _triaged_path(
    recommendations: dict[str, AIRecommendation],
    record_id: str,
) -> AIRecommendation | None:
    return recommendations.get(record_id)


def _insert_if_higher_confidence(
    recommendations: dict[str, AIRecommendation], candidate: AIRecommendation
) -> None:
    existing = _triaged_path(recommendations, candidate.record_id)
    if existing is None or candidate.confidence >= existing.confidence:
        recommendations[candidate.record_id] = candidate


def load_triage_log(log_path: Path) -> dict[str, AIRecommendation]:
    if not log_path.exists():
        return {}
    recommendations: dict[str, AIRecommendation] = {}
    for line in log_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        data = json.loads(stripped)
        recommendation = AIRecommendation.from_dict(data)
        _insert_if_higher_confidence(recommendations, recommendation)
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
    signals: list[str],
    flags: tuple[DeterministicFlag, ...],
    record: LiteratureRecord,
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


def pending_for_triage(
    corpus: Iterable[LiteratureRecord],
    reviews: dict[str, Any],
    query: str | None = None,
    limit: int | None = None,
) -> list[TriageRecord]:
    pending: list[TriageRecord] = []
    seen = 0
    for record in corpus:
        if limit is not None and seen >= limit:
            break
        if query is not None and query not in (record.tags or ()):
            continue
        if record.record_id in reviews:
            continue
        pending.append(TriageRecord(record=record))
        seen += 1
    return pending
