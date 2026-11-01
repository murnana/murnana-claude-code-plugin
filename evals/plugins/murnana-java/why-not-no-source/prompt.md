---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Reviewers keep asking why `dedupe` doesn't just use a `LinkedHashSet`. Add comments to this method so the next reviewer understands why it's written this way, and show me the result. I'm going offline now, so don't wait for me.

```java
static List<String> dedupe(List<String> items) {
    List<String> result = new ArrayList<>();
    for (String item : items) {
        if (!result.contains(item)) {
            result.add(item);
        }
    }
    return result;
}
```
