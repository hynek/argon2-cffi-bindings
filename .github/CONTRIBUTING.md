# How To Contribute

First off, thank you for considering contributing to *argon2-cffi-bindings*!
It's people like *you* who make it such a great tool for everyone.

This document intends to make contribution more accessible by codifying tribal knowledge and expectations.
Don't be afraid to open half-finished PRs, and ask questions if something is unclear!

Please note that this project is released with a Contributor [Code of Conduct](https://github.com/hynek/argon2-cffi-bindings/blob/main/.github/CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.
Please report any harm to [Hynek Schlawack] in any way you find appropriate.


## Workflow

- No contribution is too small!
  Please submit as many fixes for typos and grammar bloopers as you can!
- Try to limit each pull request to *one* change only.
- Since we squash on merge, it's up to you how you handle updates to the main branch.
  Whether you prefer to rebase on main or merge main into your branch, do whatever is more comfortable for you.
- *Always* add tests and docs for your code.
  This is a hard rule; patches with missing tests or documentation can't be merged.
- Make sure your changes pass our [CI].
  You won't get any feedback until it's green unless you ask for it.
- Once you've addressed review feedback, make sure to bump the pull request with a short note, so we know you're done.
- Don’t break backwards compatibility.


## Local Development Environment

You can (and should) run our test suite using [*tox*].
However, you’ll probably want a more traditional environment as well.

First, create a [virtual environment](https://virtualenv.pypa.io/) so you don't break your system-wide Python installation.
We recommend using the Python version from the `.python-version-default` file in project's root directory.

If you're using [*direnv*](https://direnv.net), you can automate the creation of a virtual environment with the correct Python version by adding the following `.envrc` to the project root after you've cloned it to your computer:

```bash
layout python python$(cat .python-version-default)
```

If you're using tools that understand `.python-version` files like [*pyenv*](https://github.com/pyenv/pyenv) does, you can make it a link to the `.python-version-default` file.

---

Next, fork the repository on GitHub and get an up-to-date checkout:

```console
$ git clone git@github.com:<your-username>/argon2-cffi-bindings.git
```

or if you want to use git via `https`:

```console
$ git clone https://github.com/<your-username>/argon2-cffi-bindings.git
```

Change into the newly created directory and **activate your virtual environment**

First you have to make sure that our *Argon2* *git* submodule is up-to-date:

```console
$ cd argon2-cffi-bindings
$ git submodule init     # initialize git submodule mechanics
$ git submodule update   # update the vendored Argon2 C library to the version we are packaging
```

Now an editable version of *argon2-cffi-bindings* along with its test requirements can be installed as usual:

```console
$ python -Im pip install --upgrade pip setuptools cffi  # PLEASE don't skip this step
$ python -Im pip install -e '.[dev]'
```

At this point,

```console
$ python -m pytest
```

should work and pass.

---

When working on `src/_argons_cffi_bindings/_ffi_build.py`, it makes sense to regularly delete the `build` directory along with the created binary in `src/_argons_cffi_bindings` (e.g. on macOS and Linux, it's called `_ffi.abi3.so`) to ensure it's built fresh.

---

To avoid committing code that violates our style guide, we strongly encourage you to install [*pre-commit*] [^dev] hooks:

```console
$ pre-commit install
```

You can also run them anytime (as our tox does) using:

```console
$ pre-commit run --all-files
```

[^dev]: *pre-commit* should have been installed into your virtualenv automatically when you ran `pip install -e '.[dev]'` above.
        If *pre-commit* is missing, your probably need to run `pip install -e '.[dev]'` again.


## Code

- Obey [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/).
  We use the `"""`-on-separate-lines style for docstrings:

  ```python
  def func(x):
      """
      Do something.

      :param str x: A very important parameter.

      :rtype: str
      """
  ```
- If you add or change public APIs, tag the docstring using `..  versionadded:: 16.0.0 WHAT` or `..  versionchanged:: 16.2.0 WHAT`.
- We use [*isort*](https://github.com/PyCQA/isort) to sort our imports, and we use [*Black*](https://github.com/psf/black) with line length of 79 characters to format our code.
  As long as you run our full [*tox*] suite before committing, or install our [*pre-commit*] hooks (ideally you'll do both – see [*Local Development Environment*](#local-development-environment) above), you won't have to spend any time on formatting your code at all.
  If you don't, [CI] will catch it for you – but that seems like a waste of your time!


## Tests

- Write your asserts as `expected == actual` to line them up nicely:

  ```python
  x = f()

  assert 42 == x.some_attribute
  assert "foo" == x._a_private_attribute
  ```

- To run the test suite, all you need is a recent [*tox*].
  It will ensure the test suite runs with all dependencies against all Python versions just as it will in our [CI].
  If you lack some Python versions, you can can always limit the environments like `tox -e py38,py39`, or make it a non-failure using `tox --skip-missing-interpreters`.

  In that case you should look into [*asdf*](https://asdf-vm.com) or [*pyenv*](https://github.com/pyenv/pyenv), which make it very easy to install many different Python versions in parallel.
- Write [good test docstrings](https://jml.io/pages/test-docstrings.html).


## Documentation

- Use [semantic newlines] in [Markdown*] files (files ending in `.md`):

  ```markdown
  This is a sentence.
  This is another sentence.
  ```


### Changelog

If your change is noteworthy, there needs to be a changelog entry in `CHANGELOG.md`.

- As with other docs, please use [semantic newlines] in the changelog.
- Wrap symbols like modules, functions, or classes into backticks so they are rendered in a `monospace font`.
- Wrap arguments into asterisks like in docstrings:
  `Added new argument *an_argument*.`
- If you mention functions or other callables, add parentheses at the end of their names:
  `_argon2_cffi_bindings.func()` or `_argon2_cffi_bindings.Class.method()`.
  This makes the changelog a lot more readable.
- Prefer simple past tense or constructions with "now".
  For example:

  + Added `_argon2_cffi_bindings.func()`.
  + `_argon2_cffi_bindings.func()` now doesn't crash the Large Hadron Collider anymore when passed the *foobar* argument.

Example entries:

```markdown
Added `_argon2_cffi_bindings.func()`.
The feature really *is* awesome.
```

or:

```markdown
`_argon2_cffi_bindings.func()` now doesn't crash the Large Hadron Collider anymore when passed the *foobar* argument.
The bug really *was* nasty.
```


[CI]: https://github.com/hynek/argon2-cffi-bindings/actions
[Hynek Schlawack]: https://hynek.me/about/
[*pre-commit*]: https://pre-commit.com/
[*tox*]: https://https://tox.wiki/
[semantic newlines]: https://rhodesmill.org/brandon/2012/one-sentence-per-line/
