"""MedScale AI Triage Assistant v0.1 tests."""

from __future__ import annotations

from pathlib import Path

from medscale._runtime import utc_now
from medscale.litdb.ai_triage import (
    AI_TRIAGE_SIGNALS,
    AIRecommendation,
    DeterministicFlag,
    TriageRecord,
    _priority_label,
    _recommendation_from_scores,
    append_recommendations,
    build_recommendation,
    detect_deterministic_flags,
    detect_ontology_signals,
    load_triage_log,
    pending_for_triage,
    score_triage,
)
from medscale.litdb.records import EvidenceTier, Identifiers, LiteratureRecord
from medscale.provenance import Provenance, RetrievalStatus, SourceAPI


def _make_record(
    title: str = "Test title",
    abstract: str | None = "Medical paper.",
    year: int | None = 2024,
    evidence_tier: str = "peer-reviewed",
    source_api: str = "openalex",
    *,
    tags: tuple[str, ...] = ("Q1",),
    doi: str | None = "10.1234/test",
) -> LiteratureRecord:
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi, pmid=None, arxiv_id=None, s2_corpus_id=None),
        title=title,
        evidence_tier=EvidenceTier(evidence_tier),
        provenance=Provenance(
            source_api=SourceAPI(source_api),
            identifier="test-identifier",
            verified_at=utc_now(),
            raw_response_sha256="0" * 64,
            status=RetrievalStatus.FOUND,
        ),
        year=year,
        venue="Test venue",
        authors=("Author A",),
        abstract=abstract,
        tags=tuple(tags),
    )


def test_ontology_signals_fhir() -> None:
    """Detect FHIR ontology signal."""
    signals = detect_ontology_signals("FHIR and healthcare interoperability.")
    assert "FHIR" in signals


def test_ontology_signals_multiple() -> None:
    """Detect multiple ontology signals."""
    text = (
        "A clinical NLP model for EHR data using OHDSI and HL7 FHIR standards,"
        " improving clinical decision support and biomedical AI workflows."
    )
    signals = detect_ontology_signals(text)
    assert "FHIR" in signals
    assert "HL7" in signals
    assert "OHDSI" in signals
    assert "EHR" in signals
    assert "CLINICAL_NLP" in signals
    assert "CLINICAL_DECISION_SUPPORT" in signals
    assert "BIOMEDICAL_AI" in signals


def test_ontology_no_false_positives() -> None:
    """No aggressive keyword false positives outside medical domain."""
    text = "Deep learning for autonomous driving with Python."
    signals = detect_ontology_signals(text)
    assert signals == []


def test_deterministic_flags_no_abstract() -> None:
    """Flag records without abstract."""
    record = _make_record(abstract=None)
    flags = detect_deterministic_flags(record)
    rule_names = [f.rule for f in flags]
    assert "HAS_ABSTRACT" in rule_names


def test_deterministic_flags_no_identifier() -> None:
    """Records with identifiers must not trigger HAS_IDENTIFIER; schema requires at least one."""
    record = _make_record(doi="10.1234/test")
    flags = detect_deterministic_flags(record)
    rule_names = [f.rule for f in flags]
    assert "HAS_IDENTIFIER" not in rule_names


def test_deterministic_flags_low_year() -> None:
    """Flag records older than threshold."""
    record = _make_record(year=2010)
    flags = detect_deterministic_flags(record)
    rule_names = [f.rule for f in flags]
    assert "YEAR_RANGE" in rule_names


def test_deterministic_flags_tier() -> None:
    """Flag evidence tiers outside known set."""
    record = _make_record(abstract=None)
    object.__setattr__(record, "evidence_tier", EvidenceTier.GREY)
    flags = detect_deterministic_flags(record)
    rule_names = [f.rule for f in flags]
    assert "EVIDENCE_TIER" in rule_names


def test_score_triage_high() -> None:
    """High priority for full-featured record with multiple ontology signals."""
    record = _make_record()
    triage = TriageRecord(
        record=record,
        ontology_signals=("FHIR", "HL7", "EHR", "CLINICAL_DECISION_SUPPORT"),
    )
    priority, relevance = score_triage(triage)
    assert priority >= 0.7
    assert relevance >= 0.55


def test_score_triage_low() -> None:
    """Low priority for record with many deterministic flags and no ontology coverage."""
    record = _make_record(abstract=None, year=2009)
    flags = detect_deterministic_flags(record)
    triage = TriageRecord(record=record, deterministic_flags=tuple(flags))
    priority, _relevance = score_triage(triage)
    assert priority < 0.45


def test_recommendation_first() -> None:
    """Review first for strong priority/relevance."""
    assert _recommendation_from_scores(priority_score=0.8, relevance_score=0.75) == "review first"


def test_recommendation_later() -> None:
    """Review later for moderate priority/relevance."""
    assert _recommendation_from_scores(priority_score=0.5, relevance_score=0.45) == "review later"


def test_recommendation_low() -> None:
    """Low priority only."""
    assert _recommendation_from_scores(priority_score=0.3, relevance_score=0.3) == "low priority"


def test_recommendation_uncertain() -> None:
    """Uncertain below threshold."""
    assert _recommendation_from_scores(priority_score=0.2, relevance_score=0.2) == "uncertain"


def test_priority_label() -> None:
    assert _priority_label(0.8) == "HIGH"
    assert _priority_label(0.6) == "MEDIUM"
    assert _priority_label(0.4) == "LOW"
    assert _priority_label(0.1) == "LOW"


def test_build_recommendation_has_fields() -> None:
    """Build recommendation includes required fields."""
    record = _make_record()
    triage = TriageRecord(record=record, ontology_signals=("FHIR",))
    recommendation = build_recommendation(triage)
    assert recommendation.record_id == record.record_id
    assert recommendation.recommendation in {
        "review first",
        "review later",
        "low priority",
        "uncertain",
    }
    assert 0.0 <= recommendation.confidence <= 1.0
    assert recommendation.git_sha
    assert recommendation.timestamp


def test_build_recommendation_flags_preserved() -> None:
    """Deterministic flags are preserved in log payload."""
    record = _make_record(abstract=None)
    flags = [DeterministicFlag(rule="HAS_ABSTRACT", severity="review_required")]
    triage = TriageRecord(record=record, deterministic_flags=tuple(flags))
    recommendation = build_recommendation(triage)
    assert recommendation.deterministic_flags == (
        {"rule": "HAS_ABSTRACT", "severity": "review_required"},
    )


def test_appended_recommendation_is_retrievable(tmp_path: Path) -> None:
    """Append and reload recommendation deterministically."""
    record = _make_record()
    triage = TriageRecord(record=record, ontology_signals=("FHIR",))
    recommendation = build_recommendation(triage)
    log = tmp_path / "ai_triage_log.jsonl"
    append_recommendations(log, [recommendation])
    reloaded = load_triage_log(log)
    assert recommendation.record_id in reloaded
    assert reloaded[recommendation.record_id].record_id == recommendation.record_id
    assert reloaded[recommendation.record_id].recommendation == recommendation.recommendation


def test_replay_latest_wins(tmp_path: Path) -> None:
    """Latest entry wins on replay for same record."""
    first = AIRecommendation(
        record_id="r1",
        recommendation="review later",
        confidence=0.5,
        reasoning="first",
        reason_codes=(),
        matched_rules=(),
        timestamp="2026-01-01T00:00:00+00:00",
        agent_version="test",
        git_sha="aaaaaaa",
        priority_score=0.3,
        relevance_score=0.3,
    )
    second = AIRecommendation(
        record_id="r1",
        recommendation="review first",
        confidence=0.9,
        reasoning="second",
        reason_codes=(),
        matched_rules=(),
        timestamp="2026-01-02T00:00:00+00:00",
        agent_version="test",
        git_sha="bbbbbbb",
        priority_score=0.8,
        relevance_score=0.8,
    )
    log = tmp_path / "ai_triage_log.jsonl"
    append_recommendations(log, [first, second])
    reloaded = load_triage_log(log)
    assert reloaded["r1"].recommendation == "review first"
    assert reloaded["r1"].confidence == 0.9


def test_pending_excludes_already_decided(tmp_path: Path) -> None:
    """pending_for_triage removes records with terminal decisions."""
    corpus = (_make_record(), _make_record(title="Second"))
    reviews = {}
    from medscale.litdb.review import RecordReview, ReviewDecision

    reviews[corpus[0].record_id] = RecordReview(ReviewDecision.INCLUDE, None)
    pending = pending_for_triage(corpus, reviews, query=None, limit=None)
    assert all(p.record.record_id == corpus[1].record_id for p in pending)


def test_pending_filters_query() -> None:
    """Only records tagged with query are returned."""
    corpus = (
        _make_record(title="A", tags=("Q1",)),
        _make_record(title="B", tags=("Q2",)),
    )
    pending = pending_for_triage(corpus, {}, query="Q2", limit=None)
    assert len(pending) == 1
    assert pending[0].record.tags == ("Q2",)


def test_no_human_log_mutation(tmp_path: Path) -> None:
    """AI triage log path must not collide with human review log."""
    from medscale._layout import DEFAULT_ROOT, review_log_path, triage_log_path

    assert review_log_path(DEFAULT_ROOT) != triage_log_path(DEFAULT_ROOT)


def test_ai_triage_signals_set() -> None:
    """Allowlist contains required healthcare concepts."""
    required = {
        "FHIR",
        "HL7",
        "OHDSI",
        "EHR",
        "CLINICAL_NLP",
        "MEDICAL_AI",
        "CLINICAL_DECISION_SUPPORT",
        "HEALTHCARE_INTEROPERABILITY",
        "BIOMEDICAL_AI",
    }
    assert required.issubset(set(AI_TRIAGE_SIGNALS))
