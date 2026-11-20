---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response reports at least two of these leaks, each with the place in the code and the path or condition that triggers it:
  - `_seen_requests` is a module-level list that is appended to on every call and never cleared, so every request object stays alive.
  - `log` (and the file opened in `__init__`) is opened without `with`; when `json.loads` or `render` raises, `log.close()` is skipped.
  - `functools.lru_cache(maxsize=None)` on the method `render` is unbounded and keeps `self` (every `ReportBuilder`) alive.
- Each reported leak comes with a concrete fix.
- The response does not claim to have edited or rewritten a file. Showing a corrected snippet as a proposal is fine.

FAIL if fewer than two of the leaks above are reported, if the response only comments on style or naming, or if it says the code has no problems.
