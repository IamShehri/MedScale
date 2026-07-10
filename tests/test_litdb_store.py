"""Corpus persistence: round-trip fidelity, dedupe-on-write, byte-stability."""

from __future__ import annotations

from pathlib import Path

from medscale.litdb import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.store import load_corpus, record_from_dict, record_to_dict, write_corpus
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _record(
    doi: str, title: str = "A paper", api: SourceAPI = SourceAPI.OPENALEX
) -> LiteratureRecord:
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi),
        title=title,
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(api, doi, _TS, "e" * 64),
        year=2026,
        authors=("A. Author",),
        abstract="An abstract with café unicode.",
    )


def test_roundtrip_preserves_record() -> None:
    original = _record("10.1/x")
    assert record_from_dict(record_to_dict(original)) == original


def test_write_dedupes_and_counts(tmp_path: Path) -> None:
    corpus = tmp_path / "records.jsonl"
    n = write_corpus(
        corpus,
        [
            _record("10.1/a"),
            _record("10.1/A", title="Same DOI, different metadata", api=SourceAPI.PUBMED),
            _record("10.1/b"),
        ],
    )
    assert n == 2  # 10.1/a == 10.1/A after normalization
    loaded = load_corpus(corpus)
    assert len(loaded) == 2
    assert {r.identifiers.doi for r in loaded} == {"10.1/a", "10.1/b"}


def test_corpus_bytes_are_order_independent_and_lf(tmp_path: Path) -> None:
    a, b = tmp_path / "a.jsonl", tmp_path / "b.jsonl"
    records = [_record("10.1/x"), _record("10.1/y"), _record("10.1/z")]
    write_corpus(a, records)
    write_corpus(b, list(reversed(records)))
    assert a.read_bytes() == b.read_bytes()
    assert b"\r\n" not in a.read_bytes()


def test_empty_corpus(tmp_path: Path) -> None:
    corpus = tmp_path / "empty.jsonl"
    assert write_corpus(corpus, []) == 0
    assert load_corpus(corpus) == ()


def test_loaded_records_revalidate(tmp_path: Path) -> None:
    corpus = tmp_path / "records.jsonl"
    write_corpus(corpus, [_record("10.1/q")])
    (loaded,) = load_corpus(corpus)
    assert loaded.record_id == _record("10.1/q").record_id
