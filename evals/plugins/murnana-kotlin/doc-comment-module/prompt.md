---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This file has no KDoc at all and our Dokka build is complaining about undocumented public API. Can you write the KDoc for it? Just reply with the full updated file.

```kotlin
package com.example.ratelimit

class RateLimiter(val maxCalls: Int, val perSeconds: Double) {
    private val calls = ArrayDeque<Double>()

    fun allow(now: Double): Boolean {
        while (calls.isNotEmpty() && now - calls.first() >= perSeconds) {
            calls.removeFirst()
        }
        if (calls.size >= maxCalls) return false
        calls.addLast(now)
        return true
    }
}

fun parseLimit(spec: String): RateLimiter {
    val parts = spec.split(":")
    require(parts.size == 2) { "bad limit spec '$spec'" }
    val calls = parts[0].toIntOrNull() ?: throw IllegalArgumentException("bad call count in '$spec'")
    return RateLimiter(calls, parts[1].toDouble())
}
```
