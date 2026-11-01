---
type: llm
---

Judge only the C# code block the response returns as the updated code. A report or table that quotes the old comments is fine and doesn't count as keeping them. Don't require any particular report format or headings (Japanese or otherwise).

PASS if, in that code block, there is a `//` comment directly above the `text.IndexOf(...)` line that names the `string.Contains(string, StringComparison)` overload as the rejected alternative and gives the reason that it isn't available in .NET Standard 2.0, which the project targets, AND the lines `// find the index ignoring case` and `// return true if found` no longer appear in the code block, AND apart from comments the code is the same as in the prompt (the alternative was not applied, nothing renamed or restructured).

FAIL if the comment only describes what the code does, gives no availability or version-based reason, invents a different or additional reason that the prompt doesn't give, if either `// find the index ignoring case` or `// return true if found` still appears in the code block, or if the code itself was changed.
