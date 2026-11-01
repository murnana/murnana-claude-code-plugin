---
type: llm
---

PASS if the response contains the Java method with a `/** ... */` Javadoc comment that documents `value`, `min`, `max` (with `@param`) and the return value (with `@return`), and the code itself is unchanged.

FAIL if no such doc comment is given, or if the answer is written as a C# XML documentation comment (`<summary>`, `<param>`) or as C# code.
