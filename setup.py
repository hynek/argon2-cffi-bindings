# SPDX-License-Identifier: MIT

import platform
import sys

from setuptools import setup


if platform.python_implementation() == "CPython":
    try:
        import wheel.bdist_wheel
    except ImportError:
        BDistWheel = None
    else:

        class BDistWheel(wheel.bdist_wheel.bdist_wheel):
            def finalize_options(self):
                self.py_limited_api = f"cp3{sys.version_info[1]}"
                wheel.bdist_wheel.bdist_wheel.finalize_options(self)

else:
    BDistWheel = None


if __name__ == "__main__":
    cmdclass = {}
    if BDistWheel is not None:
        cmdclass["bdist_wheel"] = BDistWheel

    setup(
        # Ensure limited API is set on CPython
        cmdclass=cmdclass,
        # setuptools_scm
        use_scm_version=True,
        # CFFI
        ext_package="_argon2_cffi_bindings",
        cffi_modules=["src/_argon2_cffi_bindings/_ffi_build.py:ffi"],
    )
