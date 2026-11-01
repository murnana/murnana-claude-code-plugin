---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I changed `retry.cpp` so that `FetchWithRetry` waits with exponential backoff (1s, 2s, 4s) instead of a fixed 1 second, because the upstream API started rate-limiting us. Write me a commit message for this change.
