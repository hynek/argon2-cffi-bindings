# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Calendar Versioning](https://calver.org/).
The **first number** of the version is the year.
The **second number** is incremented with each release, starting at 1 for each year.
The **third number** is when we need to start branches for older releases (only for emergencies).

<!-- changelog follows -->

## [25.1.0](https://github.com/hynek/argon2-cffi-bindings/compare/21.2.0...25.1.0) - 2025-07-30


Vendoring Argon2 @ [**`f57e61e`**](https://github.com/P-H-C/phc-winner-argon2/commit/f57e61e19229e23c4445b85494dbf7c07de721cb).


### Added

- Official Python 3.12, 3.13, and 3.14 support.
  No code or packaging changes were necessary.

- Support for free-threading (aka nogil) on Python 3.14.
  [#93](https://github.com/hynek/argon2-cffi-bindings/pull/93)

- Wheels for Windows on ARM64.
  [#83](https://github.com/hynek/argon2-cffi-bindings/pull/83)


### Removed

- Python 3.6, 3.7, and 3.8 support.
  There is very little activity on the bindings repo, so it doesn't make sense to carry around the build complexity of those ancient Python versions.
  The [21.2.0 wheels on PyPI](https://pypi.org/project/argon2-cffi-bindings/21.2.0/) include support for Python 3.6 and are based on the same Argon2 version.


## [21.2.0](https://github.com/hynek/argon2-cffi-bindings/compare/21.1.0...21.2.0) - 2021-12-01

Vendoring Argon2 @ [**`f57e61e`**](https://github.com/P-H-C/phc-winner-argon2/commit/f57e61e19229e23c4445b85494dbf7c07de721cb).


### Added

- Native macOS wheels for Apple Silicon (`universal2`).
  [#2](https://github.com/hynek/argon2-cffi-bindings/pull/2)

### Changed

- The compilation of the vendored Argon2 C library is now left to CFFI.
  This prevents the accidental usage of a system-wide Argon2 installation.
  [#1](https://github.com/hynek/argon2-cffi-bindings/pull/1)


## [21.1.0](https://github.com/hynek/argon2-cffi-bindings/releases/tag/21.1.0) - 2021-11-28

Vendoring Argon2 @ [**`f57e61e`**](https://github.com/P-H-C/phc-winner-argon2/commit/f57e61e19229e23c4445b85494dbf7c07de721cb).

### Added

- Initial import from [*argon2-cffi*](https://github.com/hynek/argon2-cffi).
