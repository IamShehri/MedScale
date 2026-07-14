"""Dataset schema definitions.

Stability: **public-frozen by ADR-0030**. These JSON Schema documents define the
contract for dataset artifacts. Changing a schema requires a new dataset version
and a new ADR.
"""

from __future__ import annotations

LITERATURE_RECORD_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["id", "title", "identifiers", "provenance"],
    "properties": {
        "id": {"type": "string", "description": "Stable record_id from literature record."},
        "title": {"type": "string", "minLength": 1},
        "abstract": {"type": ["string", "null"]},
        "identifiers": {
            "type": "object",
            "required": ["doi", "pmid", "arxiv_id", "s2_corpus_id"],
            "properties": {
                "doi": {"type": ["string", "null"]},
                "pmid": {"type": ["string", "null"]},
                "arxiv_id": {"type": ["string", "null"]},
                "s2_corpus_id": {"type": ["string", "null"]},
            },
            "additionalProperties": False,
        },
        "provenance": {
            "type": "object",
            "required": [
                "source_api",
                "identifier",
                "verified_at",
                "raw_response_sha256",
                "status",
            ],
            "properties": {
                "source_api": {
                    "type": "string",
                    "enum": [
                        "semantic_scholar",
                        "openalex",
                        "pubmed",
                        "arxiv",
                    ],
                },
                "identifier": {"type": "string", "minLength": 1},
                "verified_at": {"type": "string", "format": "date-time"},
                "raw_response_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                "status": {"type": "string"},
            },
            "additionalProperties": False,
        },
        "license_spdx": {"type": ["string", "null"]},
        "year": {"type": ["integer", "null"]},
        "venue": {"type": ["string", "null"]},
        "authors": {"type": "array", "items": {"type": "string"}},
        "evidence_tier": {"type": ["string", "null"]},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "additionalProperties": False,
}

EVIDENCE_OBJECT_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": [
        "evidence_id",
        "claim",
        "study_type",
        "provenance",
        "verification",
        "schema_version",
    ],
    "properties": {
        "evidence_id": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "source_record_id": {"type": ["string", "null"]},
        "claim": {"type": "string", "minLength": 1},
        "study_type": {"type": "string"},
        "population": {"type": ["string", "null"]},
        "intervention": {"type": ["string", "null"]},
        "comparator": {"type": ["string", "null"]},
        "outcome": {"type": ["string", "null"]},
        "effect_measure": {"type": ["string", "null"]},
        "effect_value": {"type": ["string", "null"]},
        "provenance": {
            "type": "object",
            "required": [
                "source_api",
                "identifier",
                "verified_at",
                "raw_response_sha256",
            ],
            "properties": {
                "source_api": {
                    "type": "string",
                    "enum": [
                        "semantic_scholar",
                        "openalex",
                        "pubmed",
                        "arxiv",
                    ],
                },
                "identifier": {"type": "string", "minLength": 1},
                "verified_at": {"type": "string", "format": "date-time"},
                "raw_response_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                "status": {"type": "string"},
            },
            "additionalProperties": False,
        },
        "verification": {"type": "string"},
        "schema_version": {"type": "string"},
    },
    "additionalProperties": False,
}

BENCHMARK_ITEM_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["task_id", "input_reference"],
    "properties": {
        "task_id": {"type": "string", "minLength": 1},
        "input_reference": {"type": "string", "minLength": 1},
        "expected_output_reference": {"type": ["string", "null"]},
        "metadata": {"type": "object"},
    },
    "additionalProperties": False,
}


class DatasetSchema:
    """Top-level dataset schema bundle.

    This class does not execute schema validation; it documents the frozen
    contract and provides helper accessors for manifest generators and validators.
    """

    literature_record = LITERATURE_RECORD_SCHEMA
    evidence_object = EVIDENCE_OBJECT_SCHEMA
    benchmark_item = BENCHMARK_ITEM_SCHEMA
    version = "1"
