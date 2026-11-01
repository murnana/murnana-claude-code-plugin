---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Reviewers keep asking why `dedupe` doesn't just use a `Set`. Add comments to this function so the next reviewer understands why it's written this way, and show me the result. I'm going offline now, so don't wait for me.

```swift
func dedupe(_ items: [String]) -> [String] {
    var result: [String] = []
    for item in items {
        if !result.contains(item) {
            result.append(item)
        }
    }
    return result
}
```
