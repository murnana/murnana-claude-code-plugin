---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is PEP 8 (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: `maxRetries` (a module constant must be UPPER_CASE), `http_client` (class must be CapWords), `SendRequest` (method must be lowercase_with_underscores), the parameters or attributes `BaseUrl` / `Path` / `requestCount` and the local `fullUrl` (must be lowercase_with_underscores).
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
