---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

We have no tests for this Java function yet. Can you write the test cases for it? I can't run anything here, so just reply with the full test file.

```java
package shop;

public final class Shipping {
    private Shipping() {}

    /**
     * Returns the shipping fee in yen for an order subtotal in yen.
     *
     * <p>Orders of 5000 yen or more ship free. Anything below costs 500 yen.
     *
     * @throws IllegalArgumentException if {@code subtotal} is negative
     */
    public static int shippingFee(int subtotal) {
        if (subtotal < 0) {
            throw new IllegalArgumentException("subtotal must not be negative");
        }
        if (subtotal >= 5000) {
            return 0;
        }
        return 500;
    }
}
```
