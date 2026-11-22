---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response reports at least two of these leaks, each with the place in the code and the path or condition that triggers it:
  - The singleton `ThumbnailCache` stores the `Activity` as `context`, so the activity can never be collected.
  - `GlobalScope.launch` with `while (true)` is never cancelled and captures the activity (`filesDir`); it keeps running after the activity is gone.
- Each reported leak comes with a concrete fix.
- The response does not claim to have edited or rewritten a file. Showing a corrected snippet as a proposal is fine.

FAIL if fewer than two of the leaks above are reported, if the response only comments on style or naming, or if it says the code has no problems.
