"""FHIR boundary package.

This package is import-safe without optional validator dependencies.
All operations are local-only; no hidden network calls are made.
"""

from __future__ import annotations

from medscale.fhirkit.errors import (
    FhirBoundaryError,
    FhirMissingDependencyError,
    FhirStorageError,
    FhirValidationError,
    InvalidReportError,
    UnavailableValidatorError,
)
from medscale.fhirkit.report import (
    FORMAT_VERSION,
    ValidationReport,
    load_report_from_json,
    report_hash,
    report_to_json,
    validate_report_schema,
)
from medscale.fhirkit.storage import store_report
from medscale.fhirkit.validate import (
    FHIR_VALIDATOR_NAME,
    FHIR_VALIDATOR_VERSION,
    validate_fhir,
    validate_fhir_with_validator,
)

__all__ = [
    "FHIR_VALIDATOR_NAME",
    "FHIR_VALIDATOR_VERSION",
    "FORMAT_VERSION",
    "FhirBoundaryError",
    "FhirMissingDependencyError",
    "FhirStorageError",
    "FhirValidationError",
    "InvalidReportError",
    "UnavailableValidatorError",
    "ValidationReport",
    "load_report_from_json",
    "report_hash",
    "report_to_json",
    "store_report",
    "validate_fhir",
    "validate_fhir_with_validator",
    "validate_report_schema",
]
