---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This class has no Javadoc at all and `javadoc -Xdoclint:all` is complaining. Can you write the Javadoc for it? Just reply with the full updated file.

```java
package com.example.ratelimit;

import java.util.ArrayDeque;
import java.util.Deque;

public final class RateLimiter {
    private final int maxCalls;
    private final double perSeconds;
    private final Deque<Double> calls = new ArrayDeque<>();

    public RateLimiter(int maxCalls, double perSeconds) {
        this.maxCalls = maxCalls;
        this.perSeconds = perSeconds;
    }

    public boolean allow(double now) {
        while (!calls.isEmpty() && now - calls.peekFirst() >= perSeconds) {
            calls.pollFirst();
        }
        if (calls.size() >= maxCalls) {
            return false;
        }
        calls.addLast(now);
        return true;
    }

    public static RateLimiter parse(String spec) {
        String[] parts = spec.split(":");
        if (parts.length != 2) {
            throw new IllegalArgumentException("bad limit spec '" + spec + "'");
        }
        return new RateLimiter(Integer.parseInt(parts[0]), Double.parseDouble(parts[1]));
    }
}
```
