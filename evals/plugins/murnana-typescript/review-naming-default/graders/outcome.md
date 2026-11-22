---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is the TypeScript team's coding guidelines (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: `IUserRepository` (no `I` prefix on interfaces), `user_record`, `connectionState` and `userService` (types are PascalCase), `Find_User` (methods are camelCase), the parameters `UserId` / `Repository` and the property `DisplayName` (camelCase), the enum values `idle` / `CONNECTED` (PascalCase), `_repository` (no `_` prefix on private properties).
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
