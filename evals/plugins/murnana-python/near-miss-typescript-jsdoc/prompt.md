---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add a JSDoc comment to this TypeScript function and reply with the updated code.

```ts
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
```
