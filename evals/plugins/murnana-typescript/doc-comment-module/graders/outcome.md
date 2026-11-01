---
type: llm
---

Judge the TypeScript file the response returns. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold in that file:
- `RateLimiter`, its constructor, `allow` and `parseLimit` each have a `/** ... */` TSDoc comment whose summary says more than the name. The summaries of `allow` and `parseLimit` start with a third-person verb ("Returns ...", "Parses ...", "Records ..."), not an imperative ("Return ...").
- Every parameter is documented with the TSDoc form `@param name - description` (with the hyphen), using the exact names `maxCalls`, `perSeconds`, `now`, `spec`.
- `allow` and `parseLimit` have `@returns`; the constructor has none.
- `parseLimit` has `@throws` for `RangeError` with the non-integer call count condition.
- No tag carries a JSDoc type in braces (no `@param {number} now`, no `@returns {boolean}`). `{@link ...}` is fine.
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements, imports or decorators).

FAIL if any of these is missing or violated.
