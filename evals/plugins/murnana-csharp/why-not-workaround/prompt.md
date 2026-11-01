---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our library's `.csproj` has `<TargetFramework>netstandard2.0</TargetFramework>`. A reviewer on my PR asked "why not just use `text.Contains(value, StringComparison.OrdinalIgnoreCase)` here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this method needs and show me the updated code.

```csharp
public static bool ContainsIgnoreCase(string text, string value)
{
    // find the index ignoring case
    int index = text.IndexOf(value, StringComparison.OrdinalIgnoreCase);
    // return true if found
    return index >= 0;
}
```
