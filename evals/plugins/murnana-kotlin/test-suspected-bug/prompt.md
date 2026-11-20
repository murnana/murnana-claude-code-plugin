---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Please add tests for this Kotlin function so we can turn on the coverage gate. I can't run anything here, so reply with the full test file.

```kotlin
package shop

/**
 * Returns the shipping fee in yen for an order [subtotal] in yen.
 *
 * Orders of 5000 yen or more ship free. Anything below costs 500 yen.
 *
 * @throws IllegalArgumentException if [subtotal] is negative.
 */
fun shippingFee(subtotal: Int): Int {
    require(subtotal >= 0) { "subtotal must not be negative" }
    if (subtotal > 5000) {
        return 0
    }
    return 500
}
```
