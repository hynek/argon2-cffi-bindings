# SPDX-License-Identifier: MIT

import pathlib
import platform
import sys

from setuptools import find_packages, setup


###############################################################################

NAME = "argon2-cffi-bindings"
DESCRIPTION = "Low-level CFFI bindings for Argon2"
URL = "https://github.com/hynek/argon2-cffi-bindings"
LICENSE = "MIT"
AUTHOR = "Hynek Schlawack"
EMAIL = "hs@ox.cx"

CFFI_MODULES = ["src/_argon2_cffi_bindings/_ffi_build.py:ffi"]
PYTHON_REQUIRES = ">=3.6"
SETUP_REQUIRES = ["cffi>=1.0.1", "setuptools_scm>=6.2"]
INSTALL_REQUIRES = ["cffi>=1.0.1"]
EXTRAS_REQUIRE = {"tests": ["pytest"]}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + [
    "cogapp",
    "pre-commit",
    "wheel",
]

KEYWORDS = ["password", "hash", "hashing", "security", "bindings", "cffi"]
PROJECT_URLS = {
    "Source Code": "https://github.com/hynek/argon2-cffi-bindings",
    "Funding": "https://github.com/sponsors/hynek",
    "Tidelift": "https://tidelift.com/subscription/pkg/pypi-argon2-cffi?"
    "utm_source=pypi-argon2-cffi&utm_medium=pypi",
    "Ko-fi": "https://ko-fi.com/the_hynek",
}
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Programming Language :: Python",
    "Topic :: Security :: Cryptography",
    "Topic :: Security",
    "Topic :: Software Development :: Libraries :: Python Modules",
]


###############################################################################


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
        name=NAME,
        use_scm_version=True,  # setuptools_scm
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        project_urls=PROJECT_URLS,
        author=AUTHOR,
        author_email=EMAIL,
        maintainer=AUTHOR,
        maintainer_email=EMAIL,
        long_description=pathlib.Path("README.md").read_text(),
        long_description_content_type="text/markdown",
        keywords=KEYWORDS,
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=CLASSIFIERS,
        python_requires=PYTHON_REQUIRES,
        setup_requires=SETUP_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        cmdclass=cmdclass,
        # CFFI
        zip_safe=False,
        ext_package="_argon2_cffi_bindings",
        cffi_modules=CFFI_MODULES,
    )
