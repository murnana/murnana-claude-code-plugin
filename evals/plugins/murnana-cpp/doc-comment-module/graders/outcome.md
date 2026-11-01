---
type: llm
---

Judge the C++ header the response returns. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold in that header:
- There is a Doxygen `@file` block with a `@brief` at the top of the file (the header declares a free function at namespace scope).
- The `ratelimit` namespace, the class `RateLimiter`, its constructor, `Allow` and `ParseLimit` each have a Doxygen comment (`///` or `/** */`) with a `@brief` that says more than the name.
- Every parameter has a `@param` with the exact name from the signature: `max_calls`, `per_seconds`, `now`, `spec`.
- `Allow` and `ParseLimit` have `@return` (or `@retval`); the constructor has no `@return`.
- `ParseLimit` documents `@throws std::invalid_argument` with the missing-`:` condition. (Also mentioning exceptions from `std::stoul`/`std::stod` is fine.)
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements, includes or attributes), and `}  // namespace ratelimit` is kept.

FAIL if any of these is missing or violated.
