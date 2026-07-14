"""Optional llama.cpp backend package.

This package is import-safe without ``llama_cpp`` installed. When installed,
it provides optional CPU-friendly generation and span extraction with explicit
missing-dependency failures when unavailable.
"""

from __future__ import annotations

from medscale.backends.llamacpp.backend import (
    LlamaCppBackend,
    LlamaCppSpanExtractor,
    LlamaCppTextGenerator,
)
from medscale.backends.llamacpp.validation import validate_package_installed

__all__ = [
    "LlamaCppBackend",
    "LlamaCppSpanExtractor",
    "LlamaCppTextGenerator",
    "LlamaTextGenerator",
    "validate_package_installed",
]

LlamaTextGenerator = LlamaCppTextGenerator
LlamaSpanExtractor = LlamaCppSpanExtractor
