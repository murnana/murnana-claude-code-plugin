---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Reviewers keep asking why `Dedupe` doesn't just use a `std::unordered_set`. Add comments to this function so the next reviewer understands why it's written this way, and show me the result. I'm going offline now, so don't wait for me.

```cpp
std::vector<std::string> Dedupe(const std::vector<std::string>& items) {
    std::vector<std::string> result;
    for (const auto& item : items) {
        if (std::find(result.begin(), result.end(), item) == result.end()) {
            result.push_back(item);
        }
    }
    return result;
}
```
