---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add an XML documentation comment to this C# method and reply with the updated code.

```csharp
public static int Clamp(int value, int min, int max)
{
    return Math.Min(Math.Max(value, min), max);
}
```
