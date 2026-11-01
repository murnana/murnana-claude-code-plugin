---
name: comment
description: Write and clean up Rust comments, placing How/What/Why/Why not where each belongs and writing rustdoc doc comments for public items.
when_to_use: Rustのコメントを書いて / このモジュールにドキュメントコメントを付けて / 不要なコメントを整理して
argument-hint: "[file, module or item to comment]"
model: sonnet
allowed-tools: Read Grep Glob Edit LSP AskUserQuestion Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/rust_comments.py *) Bash(cargo doc:*) Bash(cargo test:*) Bash(cargo clippy:*) Bash(git log:*) Bash(git blame:*) Bash(git show:*) Bash(git diff:*) Bash(git status:*)
---

# Rust Comment

Write comments for Rust code following two sources:

- **Where information goes** — t_wada's principle: "コードには How、テストコードには What、コミットログには Why、コードコメントには Why not". Details, adjustments and Rust examples: [references/comment-placement.md](references/comment-placement.md).
- **How rustdoc comments are written** — *Rust by Example*, "Documentation", and RFC 1574: [references/rustdoc.md](references/rustdoc.md).

Read both references before editing. Ask the user questions in Japanese. Write comment text in the language the crate already uses for comments; if it has none, use English.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Change comments only.** Do not change code, not even formatting. Renames, extracted functions and new tests are proposals for the report, applied only if the user already agreed in this conversation.
2. **Never delete** `// SAFETY:` comments, license or copyright headers, the reason next to `#[allow]`/`#[expect]`, or an existing `TODO`/`FIXME`. You may reword them; a vague TODO goes to the user as a question.
3. **Never invent a reason.** Every Why or Why not you write needs evidence: a commit you read (`git show`), an issue reference already in the code, or the user's answer. Carry issue numbers (`#42`) from the evidence into the comment. No hedged reasons ("probably", "may be because") and no "confirm this" placeholders in the code.
4. **Document only what the code shows.** `# Panics` only for panic paths visible in the body or in a callee you read (`panic!`, `assert!`, `unwrap`, `expect`, indexing, `unreachable!`). `# Errors` only for error values you can trace.
5. **If you cannot ask** (no `AskUserQuestion` tool, or a non-interactive run), don't stop and don't guess: leave that spot as it is and list the question in the report.

## Working efficiently

- Use Bash only for the `rust_comments.py`, `cargo` and `git` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read; never `ls`, `cat`, `grep` or `find` in Bash.
- Send independent calls together in one message (all of Step 2's commands; Step 5's checks 1–3).
- Read each target file once. After an `Edit`, don't Read the file again to confirm; the tool reports failures.
- Code pasted into the conversation instead of a file: skip the snapshot and the script and `cargo` commands, apply every other step to the pasted code, and return the result in the reply.

## Step 1: Fix the scope and take a snapshot

1. Target = `$ARGUMENTS` (a file, directory, module path or item). If empty, use the `.rs` files from `git status --short`. If that is empty too, ask.
2. Resolve the target to a list of `.rs` files. For an item name, find its file with the LSP tool (`workspaceSymbol`) if available, else Grep.
3. Snapshot the files before any edit, and remember the printed directory:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/rust_comments.py snapshot <files...>
   ```

## Step 2: Inventory

Collect, without reading more than needed:

- **Existing comments**: `python3 ${CLAUDE_SKILL_DIR}/scripts/rust_comments.py list <files...>`. It tags each as `DOC_OUTER`, `DOC_INNER`, `SAFETY`, `TODO`, `FIXME`, `LINE` or `BLOCK`.
- **Public items missing docs**:

  ```
  cargo clippy --message-format=short -- -W missing_docs -W clippy::missing_errors_doc -W clippy::missing_panics_doc -W clippy::missing_safety_doc
  ```

  Keep only `warning`/`error` lines in the target files. For a binary-only crate, `missing_docs` reports nothing; use the LSP tool (`documentSymbol`) or Read to list `pub` items instead.
- **History of odd code**: for each `LINE`/`BLOCK` comment, and each spot that looks deliberate but strange, run `git log -L <start>,<end>:<file> --format='%h %s%n%b' -n 3` and read the commit bodies. This is where Why and Why not usually are.
- **Callers and tests**, only for items whose purpose is unclear from their body: LSP `findReferences` if available, else Grep for the name. Prefer LSP `hover` over reading another file to learn a type.

Then Read each target file once, in full.

## Step 3: Classify

Write a short worksheet in your reply before editing, one line per existing comment and per spot where you might add one:

```
<file>:<line> | <quote, ≤8 words> | How / What / Why / Why not / TODO / SAFETY | delete / move to doc / keep / rewrite / ask | evidence (commit hash, issue, —)
```

Decide each line with the decision table in [references/comment-placement.md](references/comment-placement.md). In short:

- **How** → delete. If the code is unclear without it, add a rename proposal to the report.
- **What** → for a public item, move it into the doc comment's contract (with a doctest when practical); otherwise propose a test. Delete the `//` comment only after the contract or test carries it.
- **Why** → draft it into a commit message for the report. If editing the line without knowing it would break something, also keep it as a `//` comment.
- **Why not** → keep or write a `//` comment next to the line: the alternative, the reason, when the premise stops holding, and the issue number if any.
- **TODO/FIXME** → keep. If it has no issue reference or condition, ask the user for one (rule 5 if you can't).
- **SAFETY** → keep; if it doesn't explain why the unsafe preconditions hold, ask.

Batch every question for the user into one `AskUserQuestion` call (up to 4 questions; one per spot; offer "理由はない / 分からない" as an option). Apply the answers before Step 4.

## Step 4: Edit

- Apply the worksheet: one `Edit` per item, top of file to bottom.
- Write doc comments for every public item the inventory flagged, following [references/rustdoc.md](references/rustdoc.md): summary sentence in third person ending with a period; a blank `///` line; details; then only the sections that apply, in the order `# Examples`, `# Panics`, `# Errors`, `# Safety`.
- Doctests: `use` the crate by its name from `Cargo.toml` (hyphens become underscores); keep them small; assert the behavior the summary claims.
- Add `//!` at the top of `lib.rs` and of public modules that lack it.
- Link items with intra-doc links (`` [`Cart`] ``); link only to public items.
- Private items get doc comments only if the crate already documents private items or the user asks.

## Step 5: Verify

Run each check, fix what your edits caused, and re-run until clean, at most 3 rounds:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/rust_comments.py check --base <snapshot dir> <files...>` — every file must print `OK`. A `CODE` line means you changed code: undo that change. A `LICENSE` or `SAFETY` line means you broke rule 2: restore that comment.
2. `cargo test --doc` — all doctests pass. Library crates only; for a binary-only crate, say doctests don't apply.
3. `cargo doc --no-deps` — no new rustdoc warnings in the target files.
4. Re-run the clippy command from Step 2 — no remaining doc lints in the items you touched.

If a command cannot run (missing dependencies offline, workspace too large), say so in the report. Never report a check you did not run as passed.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## 変更したコメント
### 削除(How)
### doc コメントへ移動・追加(What)
### 残した・書いた Why not
### TODO / SAFETY
## 提案(未適用)
## コミットメッセージ案(Why)
## 確認できなかった点(質問)
## 検証結果
```

Under コミットメッセージ案, write only a subject line and a body taken from the Why evidence: no trailers (`Co-Authored-By`, session links, model names). Under each 変更したコメント heading, list `file:line` and a one-line reason. Use line numbers from the Step 2 `list` output (before editing) for changed or deleted comments, and say 「(編集前の行番号)」 once. Under 検証結果, give each Step 5 command with its outcome (e.g. `check: OK 3 files`, `cargo test --doc: 7 passed`), and whether the `LSP` tool was used. Do not commit unless the user asks.
