# SPDX-License-Identifier: MIT

import platform
import sys
import sysconfig

from setuptools import setup


cmdclass = {}

if platform.python_implementation() == "CPython":
    try:
        import wheel.bdist_wheel

        class BDistWheel(wheel.bdist_wheel.bdist_wheel):
            def finalize_options(self):
                # Free-threaded CPython doesn't support limited API.
                if sysconfig.get_config_var("Py_GIL_DISABLED"):
                    self.py_limited_api = False
                else:
                    self.py_limited_api = f"cp3{sys.version_info[1]}"

                wheel.bdist_wheel.bdist_wheel.finalize_options(self)

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
