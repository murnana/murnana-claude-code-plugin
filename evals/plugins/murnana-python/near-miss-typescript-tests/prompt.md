---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

Write Vitest tests for this TypeScript function. Just reply with the test file.

```typescript
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
```
