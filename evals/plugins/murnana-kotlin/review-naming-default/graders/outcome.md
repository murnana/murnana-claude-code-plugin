---
type: llm
---

Don't require any particular report format, headings or language.

PASS if all of the following hold:
- The response says which naming convention it judged by, and that convention is JetBrains' Kotlin coding conventions (the convention of the language's developer), used because the project has no rule of its own.
- The response flags at least four of these, each with the name it should become or the rule it breaks: the package `com.Example.user_profile` (must be lowercase without underscores), `maxNameLength` (a `const val` must be SCREAMING_SNAKE_CASE), `user_Repository` (class must be UpperCamelCase), `Cache`, `Load_User`, the parameter `UserId` and the local `cached_name` (must be lowerCamelCase), `XMLHTTPParser` (acronyms longer than two letters capitalize only the first letter).
- The response does not claim to have edited or rewritten a file. Showing renamed code as a proposal is fine.

FAIL if the response judges by a different convention without saying why, flags fewer than four of the names above, or says the names are fine.
