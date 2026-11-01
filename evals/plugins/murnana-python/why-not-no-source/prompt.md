---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Reviewers keep asking why `dedupe` doesn't just use a set. Add comments to this function so the next reviewer understands why it's written this way, and show me the result. I'm going offline now, so don't wait for me.

```python
def dedupe(items):
    seen = []
    result = []
    for item in items:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result
```
