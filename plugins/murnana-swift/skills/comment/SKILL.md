---
name: comment
description: Write, review or clean up Swift code comments (DocC documentation comments for the API, Why-not comments in implementations). Not for commit messages or prose docs.
argument-hint: "[file, directory or declaration to comment]"
model: sonnet
allowed-tools: Read Grep Glob Edit LSP AskUserQuestion Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/swift_comments.py *) Bash(swift package generate-documentation *) Bash(git log *) Bash(git blame *) Bash(git show *) Bash(git diff *) Bash(git status *)
---

# Swift Comment

Write comments for Swift code following two sources:

- **Where information goes**: t_wada's principle 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」. Details, the Why supplement and Swift examples: [references/comment-placement.md](references/comment-placement.md).
- **How documentation comments are written**: Swift-DocC, "Writing Symbol Documentation in Your Source Files" and "Formatting Your Documentation Content": [references/docc-symbol-docs.md](references/docc-symbol-docs.md).

Read both references before editing. If an `LSP` tool is available, also read [references/lsp.md](references/lsp.md). Ask the user questions in Japanese. Write comment text in the language the file or package already uses for comments; if it has none, use English.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Change comments only.** Do not change code, not even formatting or attribute order. Renames, extracted functions and new tests are proposals for the report, applied only if the user already agreed in this conversation.
2. **Never delete** license or copyright headers, `// MARK:` lines, `// swiftlint:` directives, `#warning`/`#error`, the reason next to `@available(*, deprecated…)` or `@unchecked Sendable`/`nonisolated(unsafe)`, or an existing `TODO`/`FIXME`. You may reword them; a vague TODO goes to the user as a question.
3. **Never invent a reason.** Every Why or Why not you write needs evidence: a commit you read (`git show`), an issue reference already in the code, or the user's answer. Carry issue numbers (`#42`) from the evidence into the comment. No hedged reasons ("probably", "may be because") and no "confirm this" placeholders in the code.
4. **Document only what the code shows.** `- Throws:` only for errors you can trace to a `throw` in the body or a callee you read (or hovered). `nil` cases in `- Returns:` only for `return nil` paths you can see. Write no units, limits, complexity or thread-safety claims you cannot point to in the declaration itself or its doc; a unit seen only in some other function's output is a question, not a fact.
5. **If you cannot ask** (no `AskUserQuestion` tool, or a non-interactive run), don't stop and don't guess: leave that spot as it is and list the question in the report.

## Working efficiently

- Use Bash only for the `swift_comments.py`, `swift package generate-documentation` and `git` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read; never `ls`, `cat`, `grep` or `find` in Bash.
- Send independent calls together in one message (all of Step 2's commands; Step 5's checks 1 and 2).
- Read each target file once. After an `Edit`, don't Read the file again to confirm; the tool reports failures.
- Code pasted into the conversation instead of a file: skip the snapshot and the script commands, apply every other step to the pasted code, and return the result in the reply.

## Step 1: Fix the scope and take a snapshot

1. Target = `$ARGUMENTS` (a file, directory or declaration name). If empty, use the `.swift` files from `git status --short`. If that is empty too, ask.
2. Resolve the target to a list of `.swift` files. Skip generated code (`*.generated.swift`, files under `.build/`, `DerivedData/`, or with a "generated" header). For a declaration name, find its file with LSP `workspaceSymbol` if available, else Grep.
3. Snapshot the files before any edit, and remember the printed directory:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/swift_comments.py snapshot <files...>
   ```

## Step 2: Inventory

Collect, without reading more than needed:

- **Existing comments and undocumented API**: `python3 ${CLAUDE_SKILL_DIR}/scripts/swift_comments.py list <files...>`. It tags each comment `DOC`, `MARK`, `TODO`, `FIXME`, `LINE` or `BLOCK`, then prints `UNDOCUMENTED` for each `public`/`open` declaration without a doc comment. Add `--internal` when the package documents internal API too (most existing internal declarations already have `///`) or the user asks.
- **Existing doc-comment problems**: `python3 ${CLAUDE_SKILL_DIR}/scripts/swift_comments.py lint <files...>`.
- **History of odd code**: for each `LINE`/`BLOCK` comment, and each spot that looks deliberate but strange, run `git log -L <start>,<end>:<file> --format='%h %s%n%b' -n 3` and read the commit bodies. This is where Why and Why not usually are.
- **Callers and tests**, only for declarations whose contract is unclear from the body: LSP as in [references/lsp.md](references/lsp.md), else Grep for the name in `Tests/` and the sources. Read two or three call sites, not all.

Then Read each target file once, in full.

## Step 3: Classify

Write a short worksheet in your reply before editing, one line per existing comment and per spot where you might add one:

```
<file>:<line> | <quote, ≤8 words> | How / What / Why / Why not / TODO / API doc | delete / move to doc / keep / rewrite / write / ask | evidence (commit hash, issue, —)
```

Decide each line with this table:

| Kind | Action |
|---|---|
| **How** (restates the code) | Delete. If the code is unclear without it, add a rename or extract proposal to the report. |
| **What** on a public or documented declaration | Move it into the doc comment's summary or discussion, then delete the `//` comment. |
| **What** elsewhere (spec of internal behavior) | Propose a test that pins it; keep the comment until the user agrees. |
| **Why** (reason for a change) | Draft it into a commit message for the report. If editing the line without knowing it would break something, also keep it as a `//` comment. |
| **Why not** (rejected alternative, workaround, deliberate non-optimization) | Keep or write a `//` comment above the line: the alternative, the reason, when the premise stops holding, the issue number if any. |
| **TODO / FIXME** | Keep. If it has no issue reference or condition, ask for one (rule 5 if you can't). |
| **API doc** (an `UNDOCUMENTED` line, or a `DOC` comment with lint errors) | Write or fix the doc comment in Step 4. |
| Commented-out code, change history, author/date notes | Delete; version control keeps them. Commented-out code with a reason for keeping it → ask. |

Batch every question for the user into one `AskUserQuestion` call (up to 4 questions; one per spot; offer 「理由はない / 分からない」 as an option). Apply the answers before Step 4.

## Step 4: Edit

- Apply the worksheet: one `Edit` per item, top of file to bottom.
- Write doc comments for every `UNDOCUMENTED` declaration and fix every lint error, following [references/docc-symbol-docs.md](references/docc-symbol-docs.md). Use `///` (or `/** */` if the file already does) in this shape, keeping only the parts that apply:

  ```swift
  /// <Summary: one sentence or fragment, plain text, ≤150 characters, ending with a period.>
  ///
  /// <Discussion: behavior a caller can't see in the signature — side effects, async or
  /// expensive work, permitted and default values, the meaning of each `Bool`/enum value.>
  ///
  /// - Parameters:
  ///   - <internal name>: <Purpose and accepted range.>
  /// - Returns: <What comes back; when it is `nil` for an optional.>
  /// - Throws: <Which error, and under what condition.>
  ```

- Summary: say what the declaration does or is, in the declaration's own terms; don't repeat its name word for word. No links, no ` ``symbol`` ` links, no code voice.
- Use the **internal** parameter name (`element` in `firstIndex(of element:)`), never the argument label. Skip parameters named `_`.
- One parameter → `- Parameter name:` is fine; two or more → a `- Parameters:` section with items indented two spaces. Follow the file's existing choice when it has one.
- Add `- Returns:` only for a non-`Void` return (not for `init`). Add `- Throws:` for every `throws`/`rethrows` declaration; for `rethrows`, say it rethrows the closure's error.
- Properties, enum cases, types and protocols get a summary (plus discussion when useful) and no `- Parameters:` / `- Returns:` items.
- Overrides and protocol witnesses whose behavior matches the parent need no doc comment: DocC inherits it.
- Refer to other documented symbols in the discussion with ` ``Type/member`` ` symbol links; confirm the target exists (LSP `workspaceSymbol` or Grep).
- Place the doc comment directly above the declaration, above its attributes (`@discardableResult`, `@MainActor`, `@available`).

## Step 5: Verify

Run each check, fix what your edits caused, and re-run until clean, at most 3 rounds:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/swift_comments.py check --base <snapshot dir> <files...>`: every file must print `OK`. A `CODE` line means you changed code or a string literal: undo that change. A `DIRECTIVE` or `LICENSE` line means you broke rule 2: restore that comment exactly.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/swift_comments.py lint <files...>`: no `ERROR` lines in declarations you touched. Fix `WARN` lines you caused; leave others for the report.
3. Re-run `list` and confirm every `UNDOCUMENTED` line in scope is gone, or listed in the report with the reason it was left.
4. Only if `Package.swift` lists the `swift-docc-plugin` dependency (Read `Package.swift`; do not run a Bash `grep` or `ls`): `swift package generate-documentation --target <target>`. No new DocC warnings in the target files. Otherwise say this check was skipped and why.

If a command cannot run, say so in the report. Never report a check you did not run as passed.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## 変更したコメント
### 削除(How)
### ドキュメントコメントへ移動・追加(What)
### 残した・書いた Why not
### TODO / FIXME
## 提案(未適用)
## コミットメッセージ案(Why)
## 確認できなかった点(質問)
## 検証結果
```

Under コミットメッセージ案, write only a subject line and a body taken from the Why evidence: no trailers (`Co-Authored-By`, session links, model names). Under each 変更したコメント heading, list `file:line` and a one-line reason. Use line numbers from the Step 2 `list` output (before editing) for changed or deleted comments, and say 「(編集前の行番号)」 once. Under 検証結果, give each Step 5 command with its outcome (e.g. `lint: OK 3 files`), plus the one line from [references/lsp.md](references/lsp.md) on how code was read. Do not commit unless the user asks.
