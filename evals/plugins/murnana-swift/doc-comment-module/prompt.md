---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This file in our Swift package has no documentation comments at all and the DocC catalog shows nothing for it. Can you write the doc comments for it? Just reply with the full updated file.

```swift
import Foundation

public struct RateLimiter {
    public let maxCalls: Int
    public let perSeconds: TimeInterval
    private var calls: [TimeInterval] = []

    public init(maxCalls: Int, perSeconds: TimeInterval) {
        self.maxCalls = maxCalls
        self.perSeconds = perSeconds
    }

    public mutating func allow(now: TimeInterval) -> Bool {
        calls.removeAll { now - $0 >= perSeconds }
        if calls.count >= maxCalls {
            return false
        }
        calls.append(now)
        return true
    }
}

public enum LimitParseError: Error {
    case malformed(String)
}

public func parseLimit(_ spec: String) throws -> RateLimiter {
    let parts = spec.split(separator: ":")
    guard parts.count == 2, let calls = Int(parts[0]), let seconds = TimeInterval(parts[1]) else {
        throw LimitParseError.malformed(spec)
    }
    return RateLimiter(maxCalls: calls, perSeconds: seconds)
}
```
