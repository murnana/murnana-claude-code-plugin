---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Reviewers keep asking why `dedupe` doesn't just use `distinct()`. Add comments to this function so the next reviewer understands why it's written this way, and show me the result. I'm going offline now, so don't wait for me.

```kotlin
fun dedupe(items: List<String>): List<String> {
    val result = mutableListOf<String>()
    for (item in items) {
        if (item !in result) {
            result.add(item)
        }
    }
    return result
}
```
