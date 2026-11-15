---
type: llm
---

PASS if the response contains a pull request description that explains the backoff change, the rate-limiting reason, and how to verify it.

FAIL if no pull request description is given, or if the response instead performs a code review (findings with severities) or asks for the code in order to review it.
