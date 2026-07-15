# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.15...4.3)

project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module
                                        ${SKBUILD_SABI_COMPONENT})

# The C source for the CFFI extension module (_ffi.c) is generated from the
# FFI definition (_ffi.cdef.txt) and the C source prelude (_ffi.csrc.c) with
# cffi-gen-src, and the result is committed to the repository.
#


# We compile that committed file directly instead of regenerating it during the
# build: cffi-gen-src ships with CFFI 2.1+, which older PyPy can't provide (it
# bundles an older CFFI that can't be upgraded), so regenerating at build time
# would break source builds on PyPy. The generated C is interpreter-independent,
# so the one committed file builds everywhere and the build needs no CFFI at
# all. Run `tox -e gen` to regenerate it after editing _ffi.cdef.txt or
# _ffi.csrc.c
set(FFI_C "${CMAKE_CURRENT_SOURCE_DIR}/src/_argon2_cffi_bindings/_ffi.c")
if(NOT EXISTS "${FFI_C}")
  message(
    FATAL_ERROR
      "${FFI_C} is missing. It is generated from _ffi.cdef.txt and "
      "_ffi.csrc.c with cffi-gen-src; run `tox -e gen` to create it.")
endif()

# cffi's generated code supports the limited API, so we build one abi3
# wheel per platform. SKBUILD_SABI_VERSION is only set when the target
# supports the stable ABI (e.g. not on PyPy or free-threaded CPython).
if(NOT "${SKBUILD_SABI_VERSION}" STREQUAL "")
  set(_sabi_args USE_SABI "${SKBUILD_SABI_VERSION}")
endif()
python_add_library(_ffi MODULE ${_sabi_args} WITH_SOABI "${FFI_C}")

if("${SKBUILD_SABI_VERSION}" STREQUAL "")
  # Not a stable-ABI (abi3) build -- e.g. free-threaded CPython or PyPy.
  # cffi's generated code otherwise turns the limited API on by itself, which
  # the free-threaded build's Python.h rejects ("The limited API is not
  # currently supported in the free-threaded build"). Tell cffi to emit a
  # regular extension instead. (In abi3 builds USE_SABI defines Py_LIMITED_API,
  # which takes precedence over this, so it is only needed when SABI is off.)
  target_compile_definitions(_ffi PRIVATE _CFFI_NO_LIMITED_API)
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Emscripten")
  set(ARGON2_EMSCRIPTEN TRUE)
else()
  set(ARGON2_EMSCRIPTEN FALSE)
endif()

if("$ENV{ARGON2_CFFI_USE_SYSTEM}" STREQUAL "1")
  if(ARGON2_EMSCRIPTEN)
    message(
      FATAL_ERROR
        "ARGON2_CFFI_USE_SYSTEM=1 is not supported for Emscripten builds.")
  endif()
  find_path(ARGON2_INCLUDE_DIR argon2.h)
  find_library(ARGON2_LIBRARY argon2)
  if(NOT ARGON2_INCLUDE_DIR OR NOT ARGON2_LIBRARY)
    message(
      FATAL_ERROR
        "ARGON2_CFFI_USE_SYSTEM is set to 1, but a system installation of "
        "Argon2 was not found (argon2.h: ${ARGON2_INCLUDE_DIR}, library: "
        "${ARGON2_LIBRARY}).")
  endif()
  target_include_directories(_ffi PRIVATE "${ARGON2_INCLUDE_DIR}")
  target_link_libraries(_ffi PRIVATE "${ARGON2_LIBRARY}")
else()
  set(ARGON2_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/extras/libargon2")
  if(NOT EXISTS "${ARGON2_ROOT}/include/argon2.h")
    message(
      FATAL_ERROR
        "The vendored copy of Argon2 was not found in ${ARGON2_ROOT}. "
        "If you are building from a git checkout, run "
        "`git submodule update --init` first. Alternatively, set "
        "ARGON2_CFFI_USE_SYSTEM=1 to build against a system installation "
        "of Argon2.")
  endif()

  # The optimized implementation requires SSE2 extensions. They have been
  # around since 2001, so we use it on every x86 target -- and on
  # Emscripten, which translates them to Wasm SIMD -- unless
  # ARGON2_CFFI_USE_SSE2 overrides the choice.
  if("$ENV{ARGON2_CFFI_USE_SSE2}" STREQUAL "0")
    set(ARGON2_USE_SSE2 FALSE)
  elseif("$ENV{ARGON2_CFFI_USE_SSE2}" STREQUAL "1" OR ARGON2_EMSCRIPTEN)
    set(ARGON2_USE_SSE2 TRUE)
  else()
    if(APPLE AND CMAKE_OSX_ARCHITECTURES)
      # May hold multiple architectures (universal2); SSE2 is only usable
      # if x86 is the only kind of target.
      set(_target_archs "${CMAKE_OSX_ARCHITECTURES}")
    elseif(CMAKE_GENERATOR_PLATFORM)
      set(_target_archs "${CMAKE_GENERATOR_PLATFORM}")
    else()
      set(_target_archs "${CMAKE_SYSTEM_PROCESSOR}")
    endif()
    set(ARGON2_USE_SSE2 TRUE)
    foreach(_arch IN LISTS _target_archs)
      string(TOLOWER "${_arch}" _arch)
      if(NOT _arch MATCHES "^(i686|x86|x86_64|amd64|x64|win32)$")
        set(ARGON2_USE_SSE2 FALSE)
      endif()
    endforeach()
  endif()

  if(ARGON2_USE_SSE2)
    set(ARGON2_IMPL opt.c)
  else()
    set(ARGON2_IMPL ref.c)
  endif()
  message(STATUS "Using Argon2 implementation: ${ARGON2_IMPL}")

  target_sources(
    _ffi
    PRIVATE "${ARGON2_ROOT}/src/argon2.c"
            "${ARGON2_ROOT}/src/blake2/blake2b.c"
            "${ARGON2_ROOT}/src/core.c"
            "${ARGON2_ROOT}/src/encoding.c"
            "${ARGON2_ROOT}/src/${ARGON2_IMPL}"
            "${ARGON2_ROOT}/src/thread.c")
  target_include_directories(_ffi PRIVATE "${ARGON2_ROOT}/include")

  if(ARGON2_USE_SSE2 AND ARGON2_EMSCRIPTEN)
    target_compile_options(_ffi PRIVATE -msimd128 -msse2)
  elseif(ARGON2_USE_SSE2 AND NOT MSVC)
    target_compile_options(_ffi PRIVATE -msse2)
  endif()

  # Argon2 uses pthreads everywhere but on Windows; Pyodide has no threads.
  if(ARGON2_EMSCRIPTEN)
    target_compile_definitions(_ffi PRIVATE ARGON2_NO_THREADS)
  elseif(NOT WIN32)
    set(THREADS_PREFER_PTHREAD_FLAG ON)
    find_package(Threads REQUIRED)
    target_link_libraries(_ffi PRIVATE Threads::Threads)
  endif()
endif()

install(TARGETS _ffi DESTINATION _argon2_cffi_bindings)
