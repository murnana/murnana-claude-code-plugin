---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I added boundary tests for the C# `shipping fee` function (4999, 5000 and 5001 yen) because last week's off-by-one bug at exactly 5000 yen reached production without any test catching it. Write me a commit message for this change.
