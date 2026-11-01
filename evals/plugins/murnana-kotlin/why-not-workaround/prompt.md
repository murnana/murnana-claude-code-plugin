---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our `build.gradle.kts` pins `languageVersion` and `apiVersion` to `KotlinVersion.KOTLIN_1_8`. A reviewer on my PR asked "why not just use `LogLevel.entries` here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this function needs and show me the updated code.

```kotlin
fun parseLevel(name: String): LogLevel? {
    // loop over all levels
    for (level in LogLevel.values()) {
        // compare names ignoring case
        if (level.name.equals(name, ignoreCase = true)) return level
    }
    return null
}
```
