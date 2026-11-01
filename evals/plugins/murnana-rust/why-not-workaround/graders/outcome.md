---
type: llm
---

Judge only the Rust code block the response returns as the updated code. A report or table that quotes the old comments is fine and doesn't count as keeping them. Don't require any particular report format or headings (Japanese or otherwise).

PASS if, in that code block, there is a `//` comment directly above the `use once_cell::sync::OnceCell;` line or the `static CONFIG` line that names `std::sync::OnceLock` as the rejected alternative and gives the reason that it was stabilized in Rust 1.70 while the crate's MSRV (`rust-version`) is 1.65, AND the lines `// a static cell for the config` and `// get the config or load it` no longer appear in the code block, AND apart from comments the code is the same as in the prompt (the alternative was not applied, nothing renamed or restructured).

FAIL if the comment only describes what the code does, gives no version-based reason, invents a different or additional reason that the prompt doesn't give, if either `// a static cell for the config` or `// get the config or load it` still appears in the code block, or if the code itself was changed.
