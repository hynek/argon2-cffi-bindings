# SPDX-License-Identifier: MIT

import os
import platform
import sys
import sysconfig

from setuptools import setup


def _is_emscripten_build():
    return os.environ.get("PYODIDE")


cmdclass = {}

if platform.python_implementation() == "CPython":
    try:
        try:
            from setuptools.command.bdist_wheel import bdist_wheel
        except ImportError:
            from wheel.bdist_wheel import bdist_wheel

        class BDistWheel(bdist_wheel):
            def finalize_options(self):
                # Free-threaded CPython and Pyodide wheels are exact-ABI.
                if (
                    sysconfig.get_config_var("Py_GIL_DISABLED")
                    or _is_emscripten_build()
                ):
                    self.py_limited_api = False
                else:
                    self.py_limited_api = f"cp3{sys.version_info[1]}"

                super().finalize_options()

        cmdclass["bdist_wheel"] = BDistWheel
    except ImportError:
        pass


if __name__ == "__main__":
    setup(
        # Ensure limited API is set on CPython
        cmdclass=cmdclass,
        # CFFI
        zip_safe=False,
        ext_package="_argon2_cffi_bindings",
        cffi_modules=["src/_argon2_cffi_bindings/_ffi_build.py:ffi"],
    )
