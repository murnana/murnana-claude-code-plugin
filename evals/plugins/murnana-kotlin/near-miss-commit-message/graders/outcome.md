---
type: llm
---

PASS if the response contains a commit message (a short subject line and a body) that explains the backoff change and the rate-limiting reason.

FAIL if no commit message is given, or if the response instead rewrites Kotlin comments or KDoc.
