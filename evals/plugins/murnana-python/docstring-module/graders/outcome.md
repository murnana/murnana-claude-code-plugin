---
type: llm
---

PASS if all of the following hold in the returned file:
- There is a module docstring, a docstring for `RateLimiter`, `RateLimiter.__init__`, `allow` and `parse_limits`, all using triple double quotes.
- Each summary line is a single line ending with a period. The summaries of `__init__`, `allow` and `parse_limits` are written as a command ("Initialize ...", "Return ...", "Parse ..."), not "Returns ..."; the class and module summaries may be noun phrases. None restates the signature (no "parse_limits(lines) -> dict").
- Arguments are documented in Google style (`Args:`, `Returns:`, `Raises:` sections), and `parse_limits` documents that it raises `ValueError`.
- The constructor arguments `max_calls` and `per_seconds` are documented in `__init__`'s docstring.
- No docstring repeats the type annotations as types (for example "max_calls (int):").

FAIL if any of these is missing or violated.
