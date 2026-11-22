---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response reports at least two of these leaks, each with the place in the code and the path or condition that triggers it:
  - `attach` stores a strong `Rc` to the parent in the child and a strong `Rc` to the child in the parent, which is a reference cycle; the back reference should be `Weak`.
  - In `log`, the early `return Err(...)` skips `CString::from_raw(raw)`, so the string from `into_raw()` leaks on the error path.
- Each reported leak comes with a concrete fix.
- The response does not claim to have edited or rewritten a file. Showing a corrected snippet as a proposal is fine.

FAIL if fewer than two of the leaks above are reported, if the response only comments on style or naming, or if it says the code has no problems.
