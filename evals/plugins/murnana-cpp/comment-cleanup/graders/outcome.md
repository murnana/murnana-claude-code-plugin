---
type: llm
---

Judge the code by the C++ code block the response returns as the cleaned-up function. A report or table that quotes the old comments is fine and doesn't count as keeping them. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold:
- The code block no longer contains `// orders と refunds をループする`, `// refund の id が一致したら金額を引く` or `// int old = std::accumulate(orders.begin(), orders.end(), 0, SumAmount);`.
- The `#128` history (the date and "の修正") is gone from the code block, and the response suggests putting it in a commit message, or the code block replaces it with a comment that explains why the guard exists without the date or history narrative.
- Every comment and doc comment in the code block is in Japanese.
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements; the `refunds.empty()` guard is still there).
- The response says how each original comment was handled.

FAIL if any of the three comments above, or the `#128` history comment, still appears in the code block, if the code block's comments were translated to English, or if the code itself was changed.
