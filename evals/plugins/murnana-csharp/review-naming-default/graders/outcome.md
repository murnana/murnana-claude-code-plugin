---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is Microsoft's C# / .NET naming conventions (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: `orderRepository` (interface without `I` and PascalCase), `load_order`, `order_service`, the parameter `OrderId` and local `Result` (should be camelCase), the private field `Repository` (should be `_repository`), `MAX_ITEMS` (constants are PascalCase), `GetOrder` or `load_order` missing the `Async` suffix.
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
