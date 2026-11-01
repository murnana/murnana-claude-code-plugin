---
type: llm
---

Judge the Swift file the response returns. Don't require any particular report format or headings (Japanese or otherwise).

PASS if all of the following hold in that file:
- `RateLimiter`, `maxCalls`, `perSeconds`, `init(maxCalls:perSeconds:)`, `allow(now:)`, `LimitParseError`, `malformed` and `parseLimit(_:)` each have a `///` documentation comment whose summary is one sentence or fragment ending with a period that says more than the name, with no symbol links or code voice in the summary.
- `init` has a `- Parameters:` section listing `maxCalls` and `perSeconds`, and no `- Returns:`.
- `allow(now:)` documents `now` (`- Parameter now:` or a `- Parameters:` section) and has `- Returns:`.
- `parseLimit(_:)` documents `spec`, has `- Returns:`, and has `- Throws:` naming `LimitParseError.malformed` (or `LimitParseError`) with the condition from the `guard`.
- The properties, the enum and its case have no `- Parameters:` or `- Returns:` items.
- Apart from comments, the code is the same as in the prompt (no renamed identifiers, no added or removed statements, imports or attributes).

FAIL if any of these is missing or violated.
