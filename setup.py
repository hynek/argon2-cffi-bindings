# SPDX-License-Identifier: MIT

import platform
import sys

from setuptools import setup


cmdclass = {}

if platform.python_implementation() == "CPython":
    try:
        try:
            from setuptools.command.bdist_wheel import bdist_wheel
        except ImportError:
            from wheel.bdist_wheel import bdist_wheel

        class BDistWheel(bdist_wheel):
            def finalize_options(self):
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
