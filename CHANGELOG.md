# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Calendar Versioning](https://calver.org/).


## [Unreleased](https://github.com/hynek/argon2-cffi-bindings/compare/21.1.0...HEAD)

### Changed

- The compilation of the vendored *Argon2* C library is now left to *CFFI*.
  This prevents the accidental usage of a system-wide *Argon2* installation.
  [#1](https://github.com/hynek/argon2-cffi-bindings/pull/1)


## [21.1.0](https://github.com/hynek/argon2-cffi-bindings/releases/tag/21.1.0) – 2021-11-28

### Added

- Initial import from [*argon2-cffi*](https://github.com/hynek/argon2-cffi).


### Changed

- The currently vendored *Argon2* commit ID is [**`f57e61e`**](https://github.com/P-H-C/phc-winner-argon2/commit/f57e61e19229e23c4445b85494dbf7c07de721cb).
