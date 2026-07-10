"""The package exposes a version string."""

from __future__ import annotations

import medscale


def test_version_is_exposed() -> None:
    assert isinstance(medscale.__version__, str)
    assert medscale.__version__.count(".") >= 2
