---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This module has no doc comments at all and our API Extractor run is complaining. Can you write the TSDoc for it? Just reply with the full updated file.

```ts
export class RateLimiter {
  private calls: number[] = [];

  constructor(
    readonly maxCalls: number,
    readonly perSeconds: number,
  ) {}

  allow(now: number): boolean {
    this.calls = this.calls.filter((t) => now - t < this.perSeconds);
    if (this.calls.length >= this.maxCalls) {
      return false;
    }
    this.calls.push(now);
    return true;
  }
}

export function parseLimit(spec: string): RateLimiter {
  const [calls, seconds] = spec.split(":");
  const count = Number(calls);
  if (!Number.isInteger(count)) {
    throw new RangeError(`bad call count in "${spec}"`);
  }
  return new RateLimiter(count, Number(seconds));
}
```
