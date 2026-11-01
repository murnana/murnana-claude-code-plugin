---
name: comment
description: Write and clean up Kotlin comments, placing How/What/Why/Why not where each belongs and writing KDoc for the API contract.
when_to_use: Kotlinのコメントを書いて / このクラスにKDocを付けて / 不要なコメントを整理して
argument-hint: "[file, directory or declaration to comment]"
model: sonnet
allowed-tools: Read Grep Glob Edit LSP AskUserQuestion Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/kt_comments.py *) Bash(git log *) Bash(git blame *) Bash(git show *) Bash(git diff *) Bash(git status *)
---

# Kotlin Comment

Write comments for Kotlin code following two sources:

- **Where information goes**: t_wada's principle 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」. Details, the Why supplement and Kotlin examples: [references/comment-roles.md](references/comment-roles.md).
- **How KDoc is written**: the kotlinlang.org KDoc page and coding conventions. Syntax, block tags, links, module/package docs: [references/kdoc.md](references/kdoc.md).

Read both references and [references/field-notes.md](references/field-notes.md) (Kotlin constructs worth documenting, phrasing) before editing. If an `LSP` tool is available, also read [references/lsp.md](references/lsp.md). Ask the user questions in Japanese. Write comment text in the language the file or module already uses for comments; if it has none, use English.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Change comments only.** Do not change code, not even formatting, imports or annotations (adding `@Deprecated` or `@Suppress` is a code change). Renames, extracted functions, named constants and new tests are proposals for the report, applied only if the user already agreed in this conversation.
2. **Never delete** license or copyright headers, tool directives (`// ktlint-disable`, `//noinspection`, `// @formatter:off/on`, `// language=`, `// region`/`// endregion`), the reason next to `@Suppress`/`@OptIn`, or an existing `TODO`/`FIXME`. You may reword them; a vague TODO goes to the user as a question.
3. **Never invent a reason.** Every Why or Why not you write needs evidence: a commit you read (`git show`), an issue reference already in the code, or the user's answer. Carry issue IDs (`#42`, `PROJ-123`) from the evidence into the comment. No hedged reasons ("probably", "may be because") and no "confirm this" placeholders in the code.
4. **Document only what the code shows.** `@throws` only for a `throw`, `require`, `check` or `error()` you can see in the body or a callee whose contract you read (or hovered). `null` meanings only for paths you can see. Write no units, ranges, threading, dispatcher or cancellation claims you cannot point to in the declaration, its body, or an existing doc; a guess becomes a question.
5. **If you cannot ask** (no `AskUserQuestion` tool, or a non-interactive run), don't stop and don't guess: leave that spot as it is and list the question in the report.

## Working efficiently

- Use Bash only for the `kt_comments.py` and `git` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read; never `ls`, `cat`, `grep` or `find` in Bash.
- Send independent calls together in one message (all of Step 2's commands; Step 5's checks 1 and 2).
- Read each target file once. After an `Edit`, don't Read the file again to confirm; the tool reports failures.
- Code pasted into the conversation instead of a file: skip the snapshot and the script commands, apply every other step to the pasted code, and return the result in the reply.

## Step 1: Fix the scope and take a snapshot

1. Target = `$ARGUMENTS` (a file, directory or declaration name). If empty, use the `.kt`/`.kts` files from `git status --short`. If that is empty too, ask.
2. Resolve the target to a list of files. Skip generated code (under `build/`, `generated/`, or with a "generated" header) unless named. For a declaration name, find its file with LSP `workspaceSymbol` if available, else Grep `(class|interface|object|fun|val|var|typealias) Name\b`. Decide whether to use LSP at all (Step 0 in [references/lsp.md](references/lsp.md)).
3. Find project settings, once: `.editorconfig` (`max_line_length`), ktlint and detekt configs (`UndocumentedPublic*` rules), Dokka setup. Note whether the module is a library (KDoc on every public declaration) or an application (KDoc on the API other modules use). If most `internal` declarations already have KDoc, pass `--internal` to `list`.
4. Snapshot the files before any edit, and remember the printed directory:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/kt_comments.py snapshot <files...>
   ```

## Step 2: Inventory

Collect, without reading more than needed:

- **Existing comments and undocumented API**: `python3 ${CLAUDE_SKILL_DIR}/scripts/kt_comments.py list <files...>`. It tags each comment `DOC`, `LICENSE`, `DIRECTIVE`, `TODO`, `FIXME`, `LINE` or `BLOCK`, then prints `UNDOCUMENTED` for each public/protected declaration (in a public type, outside function bodies) without KDoc. `override` members are not listed: they inherit the parent's KDoc.
- **Existing KDoc problems**: `python3 ${CLAUDE_SKILL_DIR}/scripts/kt_comments.py lint <files...>`.
- **History of odd code**: for each `LINE`/`BLOCK` comment, and each spot that looks deliberate but strange, run `git log -L <start>,<end>:<file> --format=%h%n%s%n%b -n 3` and read the commit bodies. This is where Why and Why not usually are.
- **Callers and tests**, only for declarations whose contract is unclear from the body: LSP as in [references/lsp.md](references/lsp.md), else Grep for the name in `*Test.kt`, `*Spec.kt`, `src/test/`, `src/commonTest/` and the sources. Read two or three call sites, not all.

Then Read each target file once, in full.

## Step 3: Classify

Write a short worksheet in your reply before editing, one line per existing comment and per spot where you might add one:

```
<file>:<line> | <quote, ≤8 words> | How / What / Why / Why not / TODO / API doc / directive | delete / move to doc / keep / rewrite / write / ask | evidence (commit hash, issue, —)
```

Decide each line with this table:

| Kind | Action |
|---|---|
| **How** (restates the code) | Delete. If the code is unclear without it, add a rename, extract or named-constant proposal to the report. |
| **What** on a public declaration | Move it into the KDoc, then delete the `//` comment. |
| **What** elsewhere (spec of internal behavior) | Propose a test that pins it; keep the comment until the user agrees. |
| **Why** (reason for a change) | Draft it into a commit message for the report. If editing the line without knowing it would break something, also keep it as a `//` comment. |
| **Why not** (rejected alternative, workaround, abandoned refactoring, skipped optimization) | Keep or write a `//` comment above the line: the alternative, the reason, when the premise stops holding, the issue ID if any. |
| **TODO / FIXME** | Keep. If it has no owner, issue ID or condition, ask for one (rule 5 if you can't). |
| **API doc** (an `UNDOCUMENTED` line, or a `DOC` comment with lint findings) | Write or fix the KDoc in Step 4. |
| `DIRECTIVE` / `LICENSE` | Keep exactly (rule 2). A directive without a reason: if the evidence gives one, write it on a `//` line above; otherwise ask. |
| A comment that contradicts the code | Don't fix either side: list it in the report (the code may be the bug). |
| Commented-out code, change history, author/date notes | Delete; version control keeps them. Commented-out code with a reason for keeping it → ask. |

Batch every question for the user into one `AskUserQuestion` call (up to 4 questions; one per spot; offer 「理由はない / 分からない」 as an option). Apply the answers before Step 4.

## Step 4: Edit

- Apply the worksheet: one `Edit` per item, top of file to bottom.
- Write KDoc for every `UNDOCUMENTED` line and fix every lint finding, following [references/kdoc.md](references/kdoc.md). Use this shape, keeping only the parts that apply:

  ```kotlin
  /**
   * <Summary: one sentence; a third-person verb for functions ("Returns ..."),
   * a noun phrase for classes and properties. Mention parameters inline as [name].>
   *
   * <Detail a caller can't see in the signature: what null means, side effects,
   * suspension and cancellation, hot or cold flows, thread safety.>
   *
   * @param name <only when it needs more than an inline mention>
   * @return <only when it needs more than the summary>
   * @throws IllegalArgumentException if <condition from a visible require>
   */
  ```

- `@property` for properties declared in the primary constructor, `@constructor` when the primary constructor needs its own note, `@receiver` for extension receivers. `@sample` points at an existing sample or test function.
- KDoc has no `@deprecated` tag. For a deprecation, propose the `@Deprecated` annotation with a message and `ReplaceWith` in the report (rule 1).
- Overrides that keep the parent's contract get no KDoc. Private members get KDoc only when the project already does so.
- Every `[name]` link must resolve to a parameter, member or imported/qualified name in scope (LSP `workspaceSymbol` or Grep); qualified names use dots only.
- Place KDoc directly above the declaration, above its annotations. Write `//` comments with a space after `//`, next to the line they explain.
- An `UNDOCUMENTED` declaration you can't describe from evidence (rule 4) → ask; don't write a summary that only restates the name.

## Step 5: Verify

Run each check, fix what your edits caused, and re-run until clean, at most 3 rounds:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/kt_comments.py check --base <snapshot dir> <files...>`: every file must print `OK`. A `CODE` line means you changed code or a string literal: undo that change. A `DIRECTIVE` or `LICENSE` line means you broke rule 2: restore that comment exactly.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/kt_comments.py lint <files...>`: no `ERROR` lines in KDoc you wrote or touched, and no `WARN` lines you caused. Leave pre-existing findings in comments you didn't touch for the report.
3. Re-run `list` and confirm every `UNDOCUMENTED` line in scope is gone, or listed in the report with the reason it was left.

Don't run Gradle tasks unasked; suggest `detekt`, `ktlintCheck` or Dokka in the report when the project has them. If a command cannot run, say so in the report. Never report a check you did not run as passed.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## 変更したコメント
### 削除(How)
### KDoc へ移動・追加(What)
### 残した・書いた Why not
### TODO / FIXME
## 提案(未適用)
## コミットメッセージ案(Why)
## 確認できなかった点(質問)
## 検証結果
```

Under 提案, include tests to add for untested behavior (What), and comments that contradict the code. Under コミットメッセージ案, write only a subject line and a body taken from the Why evidence: no trailers (`Co-Authored-By`, session links, model names). Under each 変更したコメント heading, list `file:line` and a one-line reason. Use line numbers from the Step 2 `list` output (before editing) for changed or deleted comments, and say 「(編集前の行番号)」 once. Under 検証結果, give each Step 5 command with its outcome (e.g. `check: OK 3 files`, `lint: ERROR 0 / WARN 2 (既存)`), plus the one line from [references/lsp.md](references/lsp.md) on how code was read. Do not commit unless the user asks.
