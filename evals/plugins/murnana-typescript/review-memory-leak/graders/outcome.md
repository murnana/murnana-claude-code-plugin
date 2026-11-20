---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response reports at least two of these leaks, each with the place in the code and the path or condition that triggers it:
  - The effect has no cleanup function: the `WebSocket` is never closed and the `setInterval` is never cleared, so each `symbol` change or unmount leaves them running.
  - The `resize` listener on `window` is added on every effect run and never removed.
  - `responseCache` is a module-level `Map` that gets a new key on every message and is never pruned.
- Each reported leak comes with a concrete fix.
- The response does not claim to have edited or rewritten a file. Showing a corrected snippet as a proposal is fine.

FAIL if fewer than two of the leaks above are reported, if the response only comments on style or naming, or if it says the code has no problems.
