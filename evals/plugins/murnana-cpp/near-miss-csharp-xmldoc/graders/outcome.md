---
type: llm
---

PASS if the response contains the C# method with a `///` XML documentation comment that has a `<summary>`, a `<param>` for `value`, `min` and `max`, and a `<returns>`, and the code itself is unchanged.

FAIL if no such doc comment is given, or if the answer is written as a Doxygen comment (`@brief`, `@param`) or as C++ code.
