---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

Write pytest tests for this Python function. Just reply with the test file.

```python
def clamp(value: int, low: int, high: int) -> int:
    return min(max(value, low), high)
```
