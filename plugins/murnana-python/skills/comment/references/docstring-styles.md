# Docstring styles

PEP 257 doesn't fix how arguments, return values and exceptions are laid out. Projects pick a style for that. This file says how to detect it and gives a template for each.

## Contents

- Detecting the style
- Rules for every style
- Google (default)
- NumPy
- reST (Sphinx field lists)
- Plain PEP 257

## Detecting the style

Check in this order and stop at the first that decides it:

1. Project instructions (`CLAUDE.md`, `.claude/rules/`, `CONTRIBUTING.md`, a style guide).
2. Ruff: `convention` under `[tool.ruff.lint.pydocstyle]` in `pyproject.toml`, or `[lint.pydocstyle]` in `ruff.toml` / `.ruff.toml`.
3. pydocstyle: `convention` under `[tool.pydocstyle]` in `pyproject.toml`, or `[pydocstyle]` in `setup.cfg`, `tox.ini` or `.pydocstyle`.
4. Sphinx: `napoleon_google_docstring` / `napoleon_numpy_docstring` in `docs/conf.py` (or `doc/conf.py`), or `numpydoc` in its `extensions`.
5. The docstrings already in the same package: use the style most of them use. `Args:` means Google, an underlined `Parameters` header means NumPy, `:param` means reST.
6. None of the above → **Google**.

Ruff's convention `pep257` doesn't decide between reST and plain PEP 257. Fall through to step 5 for that.

## Rules for every style

- With type hints, leave types out of the docstring. Describe meaning, units, allowed values and defaults that aren't obvious.
- Sections appear only when they have content. A function returning `None` has no Returns section. A function that raises nothing on purpose has no Raises section.
- `Raises` lists the exceptions a caller is expected to handle, with the condition. Don't list every exception a bug could cause.
- Generators document what they yield (`Yields`), not that they return a generator.
- Examples are doctests (`>>>`). Add them only when they explain usage better than prose, and make sure they pass if the project runs `pytest --doctest-modules` or `doctest`.

## Google (default)

```python
def fetch_rows(table: Table, keys: Sequence[str], *, require_all: bool = False) -> dict[str, Row]:
    """Fetch the rows for the given keys from a table.

    Keys that aren't in the table are skipped.

    Args:
        table: The open table to read from.
        keys: Row keys to fetch. Duplicates are fetched once.
        require_all: Raise instead of skipping when a key is missing.
            Keyword-only.

    Returns:
        A mapping from each found key to its row. Empty when no key matched.

    Raises:
        KeyError: A key is missing and `require_all` is true.
        OSError: The table can't be read.
    """
```

```python
class SampleClass:
    """Summary of the class.

    Longer description of its behavior.

    Attributes:
        likes_spam: Whether the instance likes spam.
        eggs: Number of eggs laid so far.
    """

    def __init__(self, likes_spam: bool = False):
        """Initialize the instance with a spam preference.

        Args:
            likes_spam: Whether the instance likes spam.
        """
```

Other section names: `Yields:`, `Attributes:`, `Examples:`, `Note:`, `Warning:`, `See Also:`. Indent section bodies by 4 spaces, and continuation lines of an entry by 4 more.

## NumPy

```python
def fetch_rows(table, keys, *, require_all=False):
    """Fetch the rows for the given keys from a table.

    Keys that aren't in the table are skipped.

    Parameters
    ----------
    table : Table
        The open table to read from.
    keys : sequence of str
        Row keys to fetch. Duplicates are fetched once.
    require_all : bool, optional
        Raise instead of skipping when a key is missing. Default False.

    Returns
    -------
    dict of str to Row
        A mapping from each found key to its row.

    Raises
    ------
    KeyError
        A key is missing and `require_all` is true.
    """
```

- Section order: Parameters, Returns (or Yields), Raises, See Also, Notes, Examples.
- The type after the colon may be dropped when the signature has type hints. Follow what the package already does.
- Constructor parameters go in the **class** docstring's `Parameters` section, not in `__init__`.

## reST (Sphinx field lists)

```python
def fetch_rows(table: Table, keys: Sequence[str], *, require_all: bool = False) -> dict[str, Row]:
    """Fetch the rows for the given keys from a table.

    Keys that aren't in the table are skipped.

    :param table: The open table to read from.
    :param keys: Row keys to fetch. Duplicates are fetched once.
    :param require_all: Raise instead of skipping when a key is missing.
    :returns: A mapping from each found key to its row.
    :raises KeyError: A key is missing and ``require_all`` is true.
    """
```

- Inline code uses double backticks (``` ``name`` ```) in reST.
- Use `:type x:` / `:rtype:` only when there are no type hints.

## Plain PEP 257

When the project uses no markup, follow the example in PEP 257: one argument per line, `name -- description`.

```python
def complex(real=0.0, imag=0.0):
    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
```
