---
type: llm
---

PASS if the response returns the code with documentation comments (rustdoc comments) added to its public declarations, or asks only for information it needs to write them.

FAIL if the response is a code review instead (a list of findings about leaks, bugs or naming with severities) and writes no documentation comments.
