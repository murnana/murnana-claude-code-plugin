---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is the Swift API Design Guidelines (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: `MAX_RETRY_COUNT` (constants are lowerCamelCase), `data_loading` and `http_response` (types and protocols are UpperCamelCase), `LoadData`, the parameter `Url`, the property `StatusCode` and `sorted_headers` (must be lowerCamelCase), the enum cases `Idle` / `CONNECTED` (must be lowerCamelCase), `empty` (a Boolean should read as an assertion: `isEmpty`).
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
