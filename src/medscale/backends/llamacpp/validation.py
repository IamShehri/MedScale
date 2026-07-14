"""llama.cpp backend validation."""

from __future__ import annotations

from medscale.backends.common import BackendMissingDependencyError

__all__ = [
    "validate_package_installed",
]


def validate_package_installed() -> None:
    spec = __import__("importlib.util").util.find_spec("llama_cpp")
    if spec is None:
        raise BackendMissingDependencyError(
            "llama.cpp backend unavailable.\n"
            "Install:\n"
            "  pip install medscale[backends-llamacpp]\n"
            "Missing dependency:\n"
            "  llama-cpp-python\n"
            "Required extra: backends-llamacpp"
        )
