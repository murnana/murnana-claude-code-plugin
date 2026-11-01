# Why-not comments

A why-not comment tells the next reader which obvious alternative was rejected, and why. Code can show what was done but never what was deliberately not done. Without the comment, a reader or reviewer assumes the author didn't know the alternative, and "fixes" the code back into the bug or the workaround's trigger.

## Contents

- Shape
- Where the reason comes from
- When to write one
- Placement
- Examples
- Moving other comments out

## Shape

```python
# <What the code does> instead of <the obvious alternative>: <reason>.
# <Optional: the condition that would lift the constraint, or the issue URL.>
```

- Name the alternative concretely (`asyncio.timeout()`, `list.sort()`, "a dict index"). "Not the usual way" tells the reader nothing.
- Give a reason that can be checked: a version, a measured size, a caller that depends on the behavior, a bug in a dependency.
- Write in the language of the surrounding comments.
- One or two lines. A longer story belongs in the commit message; link to it if needed.

## Where the reason comes from

Never invent a reason that sounds plausible. Look, in order:

1. The conversation: the user's request, the discussion that led to the code.
2. The code and config around it: `requires-python` in `pyproject.toml`, pinned versions, callers of the function, nearby comments and tests.
3. History: `git log -L <start>,<end>:<file>` (or `git blame -L <start>,<end> <file>`) to find the commit that introduced the lines, then `git show <sha>` for its message and the issue or PR it references.
4. The user, with `AskUserQuestion`: show the code and the alternative you think a reader would suggest, and ask why it wasn't used.

If none of these gives the reason, don't write the comment. List the spot in your reply so the user can fill it in.

## When to write one

Write one when a competent reader would reach for a different approach, or a reviewer would suggest one:

- A workaround for a bug or a missing feature in Python, a library or a platform.
- A newer or more idiomatic API that can't be used yet (supported Python version, pinned dependency).
- Code that looks inefficient, verbose or redundant on purpose (small input, run once, clarity over speed, thread safety).
- A broad or narrow `except` chosen on purpose.
- An ordering, copy, lock or retry that looks unnecessary but isn't.

Don't write one when nobody would consider the alternative. `# Use a for loop instead of recursion` above an ordinary loop is noise.

## Placement

- On the line(s) directly above the code it constrains, so whoever changes that code reads it, and updates or removes it along with the code.
- Not in the docstring, unless the choice changes what callers see (for example, returning a list instead of an iterator on purpose). The docstring is for callers, and why-nots are for maintainers.
- Above a directive (`# noqa`, `# type: ignore[...]`, `# pragma: no cover`), not after it, so the directive's syntax stays intact.

## Examples

**A newer API that can't be used yet**

```python
# asyncio.wait_for() instead of asyncio.timeout(): timeout() needs Python 3.11,
# and requires-python is ">=3.10". Switch once 3.10 support is dropped.
result = await asyncio.wait_for(fetch(), timeout=5)
```

**Deliberately simple code**

```python
# A plain O(n*m) scan instead of a dict index: both lists hold about 300 rows
# and this migration runs once, so the index isn't worth the extra code.
for user in users:
    for order in orders:
        ...
```

**Not mutating the input**

```python
# sorted() instead of list.sort(): callers keep using `items` in its original order.
ranked = sorted(items, key=score, reverse=True)
```

**A narrow except on purpose**

```python
# Catch OSError, not Exception: a bug in parse() must still stop the job.
try:
    raw = path.read_bytes()
except OSError:
    return None
```

**A directive**

```python
# Not wrapped: the URL must stay copy-pasteable from the source.
DOCS_URL = "https://example.com/a/very/long/path/that/exceeds/the/line/length/limit"  # noqa: E501
```

**Japanese, when the file's comments are in Japanese**

```python
# list.sort() ではなく sorted() を使う: 呼び出し元がこのあとも items を元の順序で使うため。
ranked = sorted(items, key=score, reverse=True)
```

```python
# datetime.utcnow() は使わない: naive な datetime を返し（3.12 で非推奨）、
# API から受け取る aware な時刻と比較できないため。
now = datetime.now(timezone.utc)
```

## Moving other comments out

| Comment found | Kind | Action |
|---|---|---|
| `# loop over users and sum their scores` | How | Delete. If the loop is unclear, propose a name or a helper (`total_score(users)`) |
| `# returns None if the user isn't found` | What | Put it in the docstring's Returns section, and propose a test for the missing-user case |
| `# Fixed #42 (2024-05): crashed on empty input` | Why (history) | Remove from the code, and offer the text for the commit message. If the guard still looks unnecessary, replace it with a why-not: `# Guard empty input: parse() raises on an empty list (#42).` |
| `# use wait_for` | Why-not without a reason | Find the reason (above) and complete it, or ask |
| `# old_value = compute_legacy(x)` | Commented-out code | Delete; version control keeps it |
| `# TODO: make faster` | Task without a trigger | Add the issue link or the condition, or delete it |
