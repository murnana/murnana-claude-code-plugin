---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Reviewers keep asking why `Dedupe` doesn't just use a `HashSet<string>`. Add comments to this method so the next reviewer understands why it's written this way, and show me the result. I'm going offline now, so don't wait for me.

```csharp
public static List<string> Dedupe(List<string> items)
{
    var result = new List<string>();
    foreach (var item in items)
    {
        if (!result.Contains(item))
        {
            result.Add(item);
        }
    }
    return result;
}
```
