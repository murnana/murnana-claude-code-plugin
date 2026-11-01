---
type: llm
---

Judge only the Swift code block the response returns as the updated code. A report or table that quotes the old comments is fine and doesn't count as keeping them. Don't require any particular report format or headings (Japanese or otherwise).

PASS if, in that code block, there is a `//` comment directly above the `NavigationView {` line that names `NavigationStack` as the rejected alternative and gives the reason that it requires iOS 16 while the app's deployment target is iOS 15, AND the lines `// wrap the list in a navigation view` and `// show the settings list` no longer appear in the code block, AND apart from comments the code is the same as in the prompt (the alternative was not applied, nothing renamed or restructured).

FAIL if the comment only describes what the code does, gives no version-based reason, invents a different or additional reason that the prompt doesn't give, if either `// wrap the list in a navigation view` or `// show the settings list` still appears in the code block, or if the code itself was changed.
