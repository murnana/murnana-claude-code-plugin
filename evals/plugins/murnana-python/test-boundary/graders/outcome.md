---
type: llm
---

PASS if all of the following hold in the response:
- A test list (the behaviors to check, in words) appears before the test code.
- The test file has a test for a subtotal just below 5000 (for example 4999) expecting 500, one for exactly 5000 expecting 0, and one for a negative subtotal expecting `ValueError`.
- Test names (or display names) state the condition and the expected result; none is a bare `test1`, `testShippingFee` or similar.
- Expected values are literals. No test computes its expected value with a condition, and no test contains an `if`, a loop or a try/catch that decides what is asserted (a parameterized test is fine).
- The response says the tests were not run. It does not claim that they pass.

FAIL if any of these is missing or violated, or if the response rewrites the function itself.
