---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add a KDoc comment to this Kotlin function and reply with the updated code.

```kotlin
fun clamp(value: Int, min: Int, max: Int): Int = maxOf(min, minOf(value, max))
```
