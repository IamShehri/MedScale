"""Transformers backend validation."""
from __future__ import annotations

from medscale.backends.common import BackendMissingDependencyError

__all__ = [
    "validate_package_installed",
]


def validate_package_installed() -> None:
    spec = __import__("importlib.util").util.find_spec("transformers")
    if spec is None:
        raise BackendMissingDependencyError(
            "Transformers backend unavailable.\n"
            "Install:\n"
            "  pip install medscale[backends-transformers]\n"
            "Missing dependency:\n"
            "  transformers>=4.44\n"
            "Required extra: backends-transformers"
        )
