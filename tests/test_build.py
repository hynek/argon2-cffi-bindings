import importlib.util
import sys
from pathlib import Path

import pytest

# Import _ffi_build directly to avoid triggering __init__.py, which requires
# the compiled _ffi extension to be present.
_ffi_build_spec = importlib.util.spec_from_file_location(
    "_ffi_build",
    Path(__file__).parent.parent / "src" / "_argon2_cffi_bindings" / "_ffi_build.py",
)
_ffi_build = importlib.util.module_from_spec(_ffi_build_spec)
sys.modules["_argon2_cffi_bindings"] = type(sys)("_argon2_cffi_bindings")
_ffi_build_spec.loader.exec_module(_ffi_build)

_get_target_platform = _ffi_build._get_target_platform
_use_system_lib = _ffi_build._use_system_lib


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


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        ("1", True),
        ("0", False),
        ("", False),
        ("yes", False),
        (None, False),
    ],
)
def test_use_system_lib(monkeypatch, env_value, expected):
    """
    _use_system_lib returns True only when ARGON2_CFFI_USE_SYSTEM is exactly
    "1".
    """
    if env_value is None:
        monkeypatch.delenv("ARGON2_CFFI_USE_SYSTEM", raising=False)
    else:
        monkeypatch.setenv("ARGON2_CFFI_USE_SYSTEM", env_value)

    assert expected == _use_system_lib()
