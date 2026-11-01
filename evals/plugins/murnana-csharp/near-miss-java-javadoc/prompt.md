---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add a Javadoc comment to this Java method and reply with the updated code.

```java
public static int clamp(int value, int min, int max) {
    return Math.min(Math.max(value, min), max);
}
```
