---
type: llm
---

Judge the C# file the response returns. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold in that file:
- `RateLimiter`, its constructor, `MaxCalls`, `PerSeconds`, `Allow` and `Parse` each have a `///` XML documentation comment with a `<summary>` that says more than the member's name.
- There is a `<param name="...">` for every parameter, with the exact name from the signature: `maxCalls`, `perSeconds`, `now`, `spec`.
- `Allow` and `Parse` have `<returns>`; the constructor and the properties have none.
- `Parse` has `<exception cref="ArgumentNullException">` (for a null `spec`) and `<exception cref="FormatException">` (for a malformed spec).
- The XML is well formed (every tag closed; parameter references inside text use `<paramref name="..."/>`).
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements, usings or attributes).

FAIL if any of these is missing or violated.
