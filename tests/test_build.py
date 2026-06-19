import sys

import pytest

from _argon2_cffi_bindings._ffi_build import (
    _get_target_platform,
    _is_emscripten_build,
)


@pytest.mark.parametrize(
    ("arch_flags", "expected"),
    [
        (" -arch arm64", "arm64"),
        ("abc -arch  arm64  xyz", "arm64"),
        ("abc -arch  aRm64  xyz", "arm64"),
        ("nonsense ", "FOO"),
        ("", "FOO"),
    ],
)
def test_arch(arch_flags, expected):
    """
    _get_target_platform parses ARCHFLAGS and returns the default value if
    it doesn't find anything.
    """
    assert expected == _get_target_platform(arch_flags, "FOO")


def test_is_emscripten_build_from_platform(monkeypatch):
    """
    emscripten as a platform is detected.
    """
    monkeypatch.setattr(sys, "platform", "emscripten")

    assert _is_emscripten_build()


def test_is_emscripten_build_from_pyodide_env(monkeypatch):
    """
    emscripten is detected via env var.
    """
    monkeypatch.setenv("PYODIDE", "1")

    assert _is_emscripten_build()
