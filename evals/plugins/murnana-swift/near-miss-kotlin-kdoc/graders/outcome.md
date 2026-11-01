---
type: llm
---

PASS if the response contains the Kotlin function with a `/** ... */` KDoc comment that documents `value`, `min` and `max` (with `@param` or `[value]`-style mentions) and the return value, and the code itself is unchanged.

FAIL if no such doc comment is given, or if the answer is written with Swift DocC markup (`- Parameters:`, `- Returns:`) or as Swift code.
