---
type: llm
---

PASS if the response contains the Kotlin function with a `/** ... */` KDoc comment that documents `value`, `min` and `max` (with `@param` or `[value]`-style mentions) and the return value, and the code itself is unchanged.

FAIL if no such doc comment is given, if the answer converts the function to Java, or if it uses Javadoc-only markup such as `{@code ...}` or `<p>`.
