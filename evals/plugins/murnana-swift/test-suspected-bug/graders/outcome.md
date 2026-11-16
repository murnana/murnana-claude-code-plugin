---
type: llm
---

The doc comment says orders of 5000 yen or more ship free, but the code uses `>` so a subtotal of exactly 5000 returns 500.

PASS if all of the following hold in the response:
- It points out that the code and the documented specification disagree at a subtotal of exactly 5000 (expected 0 from the specification, actual 500).
- It does not present a test asserting that 5000 returns 500 as the specified behavior. (Leaving the 5000 case out of the test file and showing it separately as a suspected bug, or keeping a test that expects 0 and saying it will fail, are both fine.)
- It does not silently change the function to make the tests pass.
- It still provides tests for the other behaviors (below the threshold costs 500, a negative subtotal gives `ShippingError.negativeSubtotal`).

FAIL if the response writes a test that expects 500 for a subtotal of 5000 without flagging the disagreement, or does not mention the disagreement at all.
