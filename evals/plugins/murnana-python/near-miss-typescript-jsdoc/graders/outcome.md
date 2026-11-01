---
type: llm
---

PASS if the response contains the TypeScript function with a `/** ... */` JSDoc comment that documents `value`, `min`, `max` (for example with `@param`) and the return value.

FAIL if no JSDoc comment is given, or if the answer is written as a Python docstring.
