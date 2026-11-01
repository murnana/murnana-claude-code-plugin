---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our `pyproject.toml` has `requires-python = ">=3.10"`. A reviewer on my PR asked "why not just use `async with asyncio.timeout(5)` here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this function needs and show me the updated code.

```python
import asyncio


async def load_profile(client, user_id):
    # call the API
    result = await asyncio.wait_for(client.get(f"/users/{user_id}"), timeout=5)
    # return the json
    return result.json()
```
