---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is the ISO C++ standard library style or the C++ Core Guidelines (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: `maxRetry` (a macro that is not ALL_CAPS), `HTTP_Client`, `SendRequest`, `Headers` (not snake_case), `strUrl` or `m_iTimeout` (type encoded in the name), `IDLE` / `CONNECTED` (ALL_CAPS enumerators).
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
