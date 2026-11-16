---
type: llm
---

PASS if the response contains a commit message (a short subject line and a body) that mentions the added boundary tests and the reason (the off-by-one bug that was not caught).

FAIL if no commit message is given, or if the response instead writes or rewrites test code.
