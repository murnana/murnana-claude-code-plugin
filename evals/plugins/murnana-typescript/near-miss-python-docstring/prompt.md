---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add a docstring to this Python function and reply with the updated code.

```python
def clamp(value: int, min_value: int, max_value: int) -> int:
    return min(max(value, min_value), max_value)
```
