---
type: llm
---

Judge the Java file the response returns. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold in that file:
- The class `RateLimiter`, its constructor, `allow` and `parse` each have a `/** ... */` Javadoc comment whose first sentence ends with a period and says more than the name.
- The summaries of `allow` and `parse` start with a third-person verb ("Returns ...", "Parses ...", "Records ..."), not an imperative ("Return ...").
- There is an `@param` for every parameter with the exact name from the signature: `maxCalls`, `perSeconds`, `now`, `spec`.
- `allow` and `parse` have `@return`; the constructor has none.
- `parse` has `@throws IllegalArgumentException` (or `NumberFormatException`) with a condition starting with "if". (Mentioning `NumberFormatException` from `Integer.parseInt`/`Double.parseDouble` in addition is fine.)
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements, imports or annotations).

FAIL if any of these is missing or violated.
