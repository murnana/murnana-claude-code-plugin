---
type: llm
---

PASS if the response contains the C++ function with a Doxygen comment (`///` or `/** */`) that has a `@brief`, a `@param` for `value`, `min` and `max`, and a `@return`, and the code itself is unchanged.

FAIL if no such doc comment is given, or if the answer is written as a rustdoc comment with Markdown sections (`# Panics`, `# Examples`) or as Rust code.
