---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is Oracle's Java code conventions (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: the package `com.Example.Billing` (must be lowercase), `invoice_printer` (class must be UpperCamelCase), `maxLines` (constant must be UPPER_SNAKE_CASE), `_customerName` (leading underscore), `Lines`, `Print_Invoice`, the parameter `CustomerName` and the local `line_count` (must be lowerCamelCase).
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
