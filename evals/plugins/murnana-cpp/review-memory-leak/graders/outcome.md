---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response reports at least two of these leaks, each with the place in the code and the path or condition that triggers it:
  - On the `fgets` failure path the function throws without `fclose(fp)` and without freeing `buffer`, so the file handle and the buffer leak.
  - `buffer` is allocated with `new char[4096]` but released with `delete` instead of `delete[]`.
- Each reported leak comes with a concrete fix.
- The response does not claim to have edited or rewritten a file. Showing a corrected snippet as a proposal is fine.

FAIL if fewer than two of the leaks above are reported, if the response only comments on style or naming, or if it says the code has no problems.
