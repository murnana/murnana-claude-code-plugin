---
type: llm
---

Judge the Rust file the response returns. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold in that file:
- The file starts with a `//!` module doc comment.
- `RateLimiter`, `RateLimiter::new`, `RateLimiter::allow` and `parse_limit` each have a `///` doc comment whose summary sentence is in the third person ("Creates ...", "Returns ...", "Parses ..."), ends with a period, and says more than the name.
- `new` has a `# Panics` section that says it panics when `max_calls` is 0.
- `parse_limit` has a `# Errors` section that describes when it returns `Err` (missing `:` or an unparsable count or seconds). (A `# Panics` section on `parse_limit` for a zero call count is also fine.)
- Sections, where present, come in the order `# Examples`, `# Panics`, `# Errors`. If any `# Examples` doctest is included, it refers to the crate as `throttle` (for example `use throttle::rate_limit::...`).
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements, attributes or `use` lines).

FAIL if any of these is missing or violated.
