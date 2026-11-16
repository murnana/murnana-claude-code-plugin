---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response reports at least two of these leaks, each with the place in the code and the path or condition that triggers it:
  - `onProgress` is a stored closure that captures `self` strongly, creating a retain cycle (needs `[weak self]`).
  - The repeating `Timer` block captures `self` strongly, and `invalidate()` is only called in `deinit`, which never runs because the timer keeps `self` alive.
  - `delegate` is a strong reference; it should be `weak`.
- Each reported leak comes with a concrete fix.
- The response does not claim to have edited or rewritten a file. Showing a corrected snippet as a proposal is fine.

FAIL if fewer than two of the leaks above are reported, if the response only comments on style or naming, or if it says the code has no problems.
