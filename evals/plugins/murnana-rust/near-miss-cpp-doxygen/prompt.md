---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add a Doxygen comment to this C++ function and reply with the updated code.

```cpp
int Clamp(int value, int min, int max) {
    return std::min(std::max(value, min), max);
}
```
