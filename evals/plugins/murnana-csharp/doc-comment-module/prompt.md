---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This class has no XML documentation comments at all and the build with `GenerateDocumentationFile` is full of CS1591 warnings. Can you write the doc comments for it? Just reply with the full updated file.

```csharp
using System;
using System.Collections.Generic;
using System.Globalization;

namespace RateLimiting;

public sealed class RateLimiter
{
    private readonly Queue<double> _calls = new();

    public RateLimiter(int maxCalls, double perSeconds)
    {
        MaxCalls = maxCalls;
        PerSeconds = perSeconds;
    }

    public int MaxCalls { get; }

    public double PerSeconds { get; }

    public bool Allow(double now)
    {
        while (_calls.Count > 0 && now - _calls.Peek() >= PerSeconds)
        {
            _calls.Dequeue();
        }
        if (_calls.Count >= MaxCalls)
        {
            return false;
        }
        _calls.Enqueue(now);
        return true;
    }

    public static RateLimiter Parse(string spec)
    {
        ArgumentNullException.ThrowIfNull(spec);
        var parts = spec.Split(':');
        if (parts.Length != 2 || !int.TryParse(parts[0], out var calls))
        {
            throw new FormatException($"bad limit spec '{spec}'");
        }
        return new RateLimiter(calls, double.Parse(parts[1], CultureInfo.InvariantCulture));
    }
}
```
