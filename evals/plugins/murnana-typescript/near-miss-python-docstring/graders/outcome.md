---
type: llm
---

PASS if the response contains the Python function with a triple-quoted docstring that documents `value`, `min_value`, `max_value` and the return value, and the code itself is unchanged.

FAIL if no docstring is given, or if the answer is written as a JSDoc/TSDoc `/** ... */` comment or as TypeScript code.
