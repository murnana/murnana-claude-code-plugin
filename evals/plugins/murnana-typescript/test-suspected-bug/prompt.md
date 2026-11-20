---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Please add tests for this TypeScript function so we can turn on the coverage gate. I can't run anything here, so reply with the full test file.

```ts
/**
 * Returns the shipping fee in yen for an order subtotal in yen.
 *
 * Orders of 5000 yen or more ship free. Anything below costs 500 yen.
 *
 * @throws RangeError if `subtotal` is negative.
 */
export function shippingFee(subtotal: number): number {
  if (subtotal < 0) {
    throw new RangeError("subtotal must not be negative");
  }
  if (subtotal > 5000) {
    return 0;
  }
  return 500;
}
```
