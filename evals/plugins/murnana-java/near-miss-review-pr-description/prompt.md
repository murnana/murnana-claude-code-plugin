---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I finished a Java change that makes the retry logic use exponential backoff (1s, 2s, 4s) instead of a fixed 1 second delay, because the upstream API started rate-limiting us. A teammate will do the code review. Write the pull request description for it: why, what is affected, and how to verify.
