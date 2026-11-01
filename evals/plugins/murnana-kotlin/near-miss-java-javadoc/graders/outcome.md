---
type: llm
---

PASS if the response contains the Java method with a `/** ... */` Javadoc comment that documents `value`, `min`, `max` (with `@param`) and the return value (with `@return`), and the code itself is unchanged.

FAIL if no such doc comment is given, if the answer converts the method to Kotlin, or if it writes KDoc-style `[value]` links instead of `@param` tags.
