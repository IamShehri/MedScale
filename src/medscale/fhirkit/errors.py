"""FHIR boundary error hierarchy."""

from __future__ import annotations


class FhirBoundaryError(Exception):
    """Base error for the FHIR boundary."""


class FhirValidationError(FhirBoundaryError):
    """Raised when FHIR input is structurally invalid."""


class UnavailableValidatorError(FhirBoundaryError):
    """Raised when an optional validator is requested but unavailable."""


class FhirMissingDependencyError(FhirBoundaryError):
    """Raised when an optional dependency is missing."""


class InvalidReportError(FhirBoundaryError):
    """Raised when a ValidationReport does not satisfy the schema contract."""


class FhirStorageError(FhirBoundaryError):
    """Raised when FHIR artifact storage fails."""
