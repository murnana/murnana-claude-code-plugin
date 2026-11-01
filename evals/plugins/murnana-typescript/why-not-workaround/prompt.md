---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our `tsconfig.json` has `"target": "ES2021"` and `"lib": ["ES2021"]`. A reviewer on my PR asked "why not just use `items.at(-1)` here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this function needs and show me the updated code.

```ts
export function lastOrUndefined<T>(items: readonly T[]): T | undefined {
  // get the last index
  const index = items.length - 1;
  // return the item at that index
  return items[index];
}
```
