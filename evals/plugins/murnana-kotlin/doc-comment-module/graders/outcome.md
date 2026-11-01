---
type: llm
---

Judge the Kotlin file the response returns. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold in that file:
- `RateLimiter`, `allow` and `parseLimit` each have a `/** ... */` KDoc comment whose first sentence says more than the name. The summaries of `allow` and `parseLimit` start with a third-person verb ("Returns ...", "Parses ...", "Records ..."), not an imperative ("Return ...").
- The primary-constructor properties `maxCalls` and `perSeconds` are documented, either with `@property`/`@param` tags in the class KDoc or by `[maxCalls]` / `[perSeconds]` mentions in its text.
- The parameters `now` and `spec` are documented, either with `@param` or by `[now]` / `[spec]` mentions in the text.
- `parseLimit` documents that it throws `IllegalArgumentException` (with `@throws` or in the text) for a malformed spec or a non-numeric call count. (Mentioning `NumberFormatException` from `toDouble()` in addition is fine.)
- No KDoc uses Javadoc-only markup such as `<p>` or `{@code ...}`, and no tag repeats a type in braces.
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements, imports or annotations).

FAIL if any of these is missing or violated.
