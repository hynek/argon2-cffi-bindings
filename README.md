# Python CFFI Bindings for Argon2

*argon2-cffi-bindings* provides low-level [*CFFI*](https://cffi.readthedocs.io/) bindings to the [*Argon2*] password hashing algorithm including a vendored version of them.

<!-- Extract commit ID; refresh using `tox -e cog`
[[[cog
import subprocess
cp = subprocess.run(["git", "submodule"], capture_output=True)
id = cp.stdout[1:].decode().split(" ", 1)[0]
link = f'[**`{id[:7]}`**](https://github.com/P-H-C/phc-winner-argon2/commit/{id})'
print(f"The currently vendored *Argon2* commit ID is {link}.")
]]] -->
The currently vendored *Argon2* commit ID is [**`f57e61e`**](https://github.com/P-H-C/phc-winner-argon2/commit/f57e61e19229e23c4445b85494dbf7c07de721cb).
<!-- [[[end]]] -->

> If you want to hash passwords in an application, this package is **not** for you.
> Have a look at [*argon2-cffi*] with its high-level abstractions!

These bindings have been extracted from [*argon2-cffi*] and it remains its main consumer.
However, they may be used by other packages that want to use *Argon2* library without dealing with C-related complexities.


## Usage

The provided *CFFI* bindings are compiled in API mode.
Best effort is given to provide binary wheels for as many platforms as possible.

---

A copy of [*Argon2*] is vendored and used by default, but can be disabled if *argon2-cffi-bindings* is installed using:

```console
$ env ARGON2_CFFI_USE_SYSTEM=1 \
  python -m pip install --no-binary=argon2-cffi-bindings argon2-cffi-bindings
```


### Python API

Since this package is intended to be an implementation detail, it uses a private module name.
Therefore you have to import the symbols from `_argon2_cffi_bindings`:

```python
from _argon2_cffi_bindings import ffi, lib
```

Please refer to [*cffi* documentation](https://cffi.readthedocs.io/en/latest/using.html) on how to use the `ffi` and `lib` objects.

The list of symbols that are provided can be found in the [`_ffi_build.py` file](https://github.com/hynek/argon2-cffi-bindings/blob/main/src/_argon2_cffi_bindings/_ffi_build.py).

[*Argon2*]: https://github.com/p-h-c/phc-winner-argon2
[*argon2-cffi*]: https://argon2-cffi.readthedocs.io/


## Project Information

*argon2-cffi-bindings* is available under the MIT license, available from [PyPI](https://pypi.org/project/argon2-cffi-bindings/), the source code and documentation can be found on [GitHub](https://github.com/hynek/argon2-cffi-bindings).

*argon2-cffi-bindings* targets Python 3.6 and later, including PyPy3.


### Credits & License

*argon2-cffi-bindings* is written and maintained by [Hynek Schlawack](https://hynek.me/about/).
It is released under the [MIT license](https://github.com/hynek/argon2-cffi/blob/main/LICENSE>).

The development is kindly supported by [Variomedia AG](https://www.variomedia.de/).

The authors of *Argon2* were very helpful to get the library to compile on ancient versions of Visual Studio for ancient versions of Python.

The documentation quotes frequently in verbatim from the *Argon2* [paper](https://www.password-hashing.net/argon2-specs.pdf) to avoid mistakes by rephrasing.


#### Vendored Code

The original *Argon2* repo can be found at <https://github.com/P-H-C/phc-winner-argon2/>.

Except for the components listed below, the *Argon2* code in this repository is copyright (c) 2015 Daniel Dinu, Dmitry Khovratovich (main authors), Jean-Philippe Aumasson and Samuel Neves, and under [CC0] license.

The string encoding routines in src/encoding.c are copyright (c) 2015 Thomas Pornin, and under [CC0] license.

The [*BLAKE2*](https://www.blake2.net) code in ``src/blake2/`` is copyright (c) Samuel Neves, 2013-2015, and under [CC0] license.

[CC0]: https://creativecommons.org/publicdomain/zero/1.0/
