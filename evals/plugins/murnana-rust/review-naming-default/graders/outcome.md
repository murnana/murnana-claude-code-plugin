---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is the Rust API Guidelines (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: `maxConnections` (constants are SCREAMING_SNAKE_CASE), `HTTPClient` (acronyms are one word: `HttpClient`), the field `BaseUrl`, the method `SendRequest` and the parameter `Path` (must be snake_case), `get_base_url` (getters have no `get_` prefix), `to_bytes` (a cheap borrowed-to-borrowed conversion is `as_`).
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
