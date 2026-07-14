"""Optional transformers backend package.

This package is import-safe without ``transformers`` installed. When installed,
it provides optional deterministic generation and span extraction with explicit
missing-dependency failures when unavailable.
"""

from __future__ import annotations

from medscale.backends.transformers.backend import (
    TransformersBackend,
    TransformersSpanExtractor,
    TransformersTextGenerator,
)
from medscale.backends.transformers.validation import validate_package_installed

__all__ = [
    "TransformersBackend",
    "TransformersSpanExtractor",
    "TransformersTextGenerator",
    "validate_package_installed",
]
