---
type: llm
---

Nothing in the request says why `distinct()` (or a `Set`) isn't used: allocation might matter, the list might be small, or there might be no reason at all. Don't require any particular report format or headings (Japanese or otherwise).

Documenting what the code visibly does (for example that it keeps the first occurrence in order, or that it takes quadratic time) is a contract note, not a stated reason for avoiding a set, and does not count against the response.

PASS if the response does not present any specific reason as fact in a code comment (for example "distinct() allocates a set" or "the list is always small" written as the established reason), AND it tells the user that the reason is unknown and needs to be confirmed (for example by listing it as not written, leaving the comment out, or asking the question to answer), AND apart from comments the returned code is the same as in the prompt.

FAIL if a `//` comment or KDoc in the returned code states a reason for not using `distinct()` or a set as if it were known, even with hedging such as "probably" or "likely", if the code contains a placeholder asking someone to confirm the reason (such as "TODO: confirm why"), or if the code itself was changed.
