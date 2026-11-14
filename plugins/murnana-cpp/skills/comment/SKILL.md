---
name: comment
description: Write, review or clean up C++ code comments (Doxygen doc comments for the API, Why-not comments in implementations). Not for commit messages or prose docs.
argument-hint: "[files, symbols, or \"review\"]"
model: sonnet
allowed-tools: Read Grep Glob Edit LSP AskUserQuestion Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/cpp_comments.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/check_comments.py *) Bash(git log *) Bash(git blame *) Bash(git show *) Bash(git diff *) Bash(git status *)
---

# C++ Comment

Write comments for C++ code following two sources:

- **Where information goes**: t_wada's principle 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」. Details, the Why supplement and C++ examples: [references/what-goes-where.md](references/what-goes-where.md).
- **How doc comments are written**: Doxygen. Commands, layout and pitfalls: [references/doxygen.md](references/doxygen.md).

Read both references, and [references/project-rules.md](references/project-rules.md) for where project conventions live, before editing. Ask the user questions in Japanese. Write comment text in the language the file or project already uses for comments; if it has none, use English. Keep Doxygen command names as they are.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Change comments only.** Do not change code, not even formatting, includes, attributes or `[[deprecated]]`. Renames, extracted functions and new tests are proposals for the report, applied only if the user already agreed in this conversation.
2. **Never delete** license or copyright headers, tool directives (`// NOLINT`, `// NOLINTNEXTLINE`, `// clang-format off/on`, `// IWYU pragma:`, `// cppcheck-suppress`), the reason next to a `#pragma` or a suppression, or an existing `TODO`/`FIXME`. You may reword them; a vague TODO goes to the user as a question. `}  // namespace foo` is conventional: keep it.
3. **Never invent a reason.** Every Why or Why not you write needs evidence: a commit you read (`git show`), an issue reference already in the code, or the user's answer. Carry issue IDs (`#42`, `PROJ-123`) from the evidence into the comment. No hedged reasons ("probably", "may be because") and no "confirm this" placeholders in the code.
4. **Document only what the code shows.** `@throws` only for a `throw` you can see in the body or a callee whose contract you read (or hovered). `@pre` only for a precondition the code checks or relies on visibly. Write no units, ranges, ownership, complexity or thread-safety claims you cannot point to in the declaration, its body, or an existing doc; a guess becomes a question.
5. **If you cannot ask** (no `AskUserQuestion` tool, or a non-interactive run), don't stop and don't guess: leave that spot as it is and list the question in the report.

## Working efficiently

- Use Bash only for the `cpp_comments.py`, `check_comments.py` and `git` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read; never `ls`, `cat`, `grep` or `find` in Bash.
- Send independent calls together in one message (all of Step 2's commands; Step 5's checks 1 and 2).
- Read each target file once. After an `Edit`, don't Read the file again to confirm; the tool reports failures.
- Code pasted into the conversation instead of a file: skip the snapshot and the script commands, apply every other step to the pasted code, and return the result in the reply.

## Step 1: Fix the scope and take a snapshot

1. Target = `$ARGUMENTS` (files, a directory, symbol names, or `review`). `review` means: judge existing comments only, and add new ones only where a public API has no contract. If empty, use the C++ files from `git status --short`. If that is empty too, ask.
2. Resolve the target to a list of files. For a symbol, find its declaration (usually a header) and its definition: with the `LSP` tool (`workspaceSymbol`, for example with the `clangd-lsp` plugin) if available, else Grep. Skip generated files and third-party directories (`third_party/`, `external/`, `vendor/`) unless named.
3. Find project settings, once, as listed in [references/project-rules.md](references/project-rules.md): `Doxyfile`, `.clang-format`, `.clang-tidy`, `CLAUDE.md`, `compile_commands.json`. Defaults when the project says nothing: `///` blocks with `@` commands; `///<` after enumerators and data members for one-line docs. With mixed styles, follow the target file's majority; don't convert existing comments.
4. Snapshot the files before any edit, and remember the printed directory:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/cpp_comments.py snapshot <files...>
   ```

## Step 2: Inventory

Collect, without reading more than needed:

- **Existing comments**: `python3 ${CLAUDE_SKILL_DIR}/scripts/cpp_comments.py list <files...>`. It tags each comment `DOC`, `LICENSE`, `DIRECTIVE`, `TODO`, `FIXME`, `LINE` or `BLOCK`.
- **Undocumented API and doc-comment problems**: `python3 ${CLAUDE_SKILL_DIR}/scripts/check_comments.py <files...>`. It runs Doxygen (and clang `-Wdocumentation` when a compilation database exists) with options that avoid false warnings, and prints `path:line: [check] message`.
- **History of odd code**: for each `LINE`/`BLOCK` comment, and each spot that looks deliberate but strange (an odd constant, a surprising container, a workaround), run `git log -L <start>,<end>:<file> --format=%h%n%s%n%b -n 3` and read the commit bodies. This is where Why and Why not usually are. Check the reason still matches the current code.
- **Callers and tests**, only for declarations whose contract is unclear from the body: LSP `findReferences` if available, else Grep for the name. Read two or three call sites, not all.

Then Read each target file once, in full.

## Step 3: Classify

Write a short worksheet in your reply before editing, one line per existing comment and per spot where you might add one:

```
<file>:<line> | <quote, ≤8 words> | How / What / Why / Why not / TODO / API doc / directive | delete / move to doc / keep / rewrite / write / ask | evidence (commit hash, issue, —)
```

Decide each line with this table:

| Kind | Action |
|---|---|
| **How** (restates the code) | Delete. If the code is unclear without it, add a rename or extract proposal to the report. A comment that compensates for a name (`int d; // days`) is the same: propose the rename. |
| **What** on a public declaration | Move it into the doc comment, then delete the `//` comment. |
| **What** elsewhere (spec of internal behavior) | Propose a test that pins it; keep the comment until the user agrees. |
| **Why** (reason for a change) | Draft it into a commit message for the report. If editing the line without knowing it would break something (an invariant, an ordering requirement, a spec quirk), also keep it as a `//` comment. |
| **Why not** (rejected alternative, workaround, deliberate non-optimization) | Keep or write a `//` comment above the line: the alternative, the reason, when the premise stops holding, the issue ID if any. |
| **TODO / FIXME** | Keep. If it has no owner, issue ID or condition, ask for one (rule 5 if you can't). |
| **API doc** (an undocumented-member finding, or a `DOC` comment with findings) | Write or fix the doc comment in Step 4. |
| `DIRECTIVE` / `LICENSE` | Keep exactly (rule 2). A directive without a reason: if the evidence gives one, write it on a `//` line above; otherwise ask. |
| Commented-out code, change history, author/date notes | Delete; version control keeps them. Commented-out code with a reason for keeping it → ask. |

Batch every question for the user into one `AskUserQuestion` call (up to 4 questions; one per spot; offer 「理由はない / 分からない」 as an option). Never ask about something the code shows. Apply the answers before Step 4.

## Step 4: Edit

- Apply the worksheet: one `Edit` per item, top of file to bottom.
- Write doc comments on the declaration in the header, once; never repeat them on the `.cpp` definition. Use this shape, keeping only the parts that apply:

  ```cpp
  /// @brief <One sentence, from the caller's view, that adds something beyond the name.>
  ///
  /// <Details a caller can't see in the signature: side effects, ownership, lifetime,
  /// thread safety, complexity, accepted and default values.>
  ///
  /// @tparam T <requirements the code imposes>
  /// @param name <what to pass: units, range, whether null or empty is allowed>
  /// @param[out] result <what is written>
  /// @return <what comes back>
  /// @throws std::invalid_argument <condition>
  ```

- `@param` for every parameter, names exactly as in the signature; mark outputs `[out]` or `[in,out]`. `@return` only for non-void functions, never on constructors; `@retval` for distinguished values. A one-line accessor may keep just a `@brief` that says what it returns.
- `@pre` / `@post` for conditions whose violation is undefined behavior or a crash; `@note` for ownership, lifetime, thread safety or complexity that matter to callers.
- Overrides with an unchanged contract get no block: Doxygen copies the base documentation.
- A header with free functions, enums or macros at file scope gets a `/// @file` + `/// @brief` block at the top. Each namespace with documented members gets a doc comment in its main header.
- Implementation comments use `//`, never `///`, inside a function body, directly above the line they explain.
- An undocumented declaration you can't describe from evidence (rule 4) → ask; don't write a `@brief` that only restates the name.

## Step 5: Verify

Run each check, fix what your edits caused, and re-run until clean, at most 3 rounds:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpp_comments.py check --base <snapshot dir> <files...>`: every file must print `OK`. A `CODE` line means you changed code or a string literal: undo that change. A `DIRECTIVE` or `LICENSE` line means you broke rule 2: restore that comment exactly.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/check_comments.py <files...>`: no `[doxygen]`, `[clang]` or `[structure]` finding in comments you wrote or touched. Add missing `@param`/`@return` for `[advisory]` lines unless the `@brief` of a one-line accessor already says everything. A missing contract you can't write without guessing (rule 3) stays; list it in the report.
   - `doxygen not found`: tell the user how to install it, check by eye against the Gotchas, and say the check was skipped.

If a command cannot run, say so in the report. Never report a check you did not run as passed.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## 変更したコメント
### 削除(How)
### Doxygen へ移動・追加(What)
### 残した・書いた Why not
### TODO / FIXME
## 提案(未適用)
## コミットメッセージ案(Why)
## 確認できなかった点(質問)
## 検証結果
```

Under コミットメッセージ案, write only a subject line and a body taken from the Why evidence: no trailers (`Co-Authored-By`, session links, model names). Under each 変更したコメント heading, list `file:line` and a one-line reason. Use line numbers from the Step 2 `list` output (before editing) for changed or deleted comments, and say 「(編集前の行番号)」 once. Under 検証結果, give each Step 5 command with its outcome (e.g. `check: OK 3 files`, `check_comments: 0 finding(s)`), and whether the `LSP` tool was used. Do not commit unless the user asks.

## Gotchas

- A multi-line `///` block without `@brief` has an empty brief by default, so member lists show nothing. `check_comments.py` reports it as `[structure]`.
- Free functions, enums and macros in a header without `@file`, and members of an undocumented namespace, are silently left out of the generated pages. Doxygen doesn't warn; the script does.
- A doc comment describing the algorithm (How) goes stale with the first refactor. Callers need the contract.
- Don't "improve" a correct comment just to change its wording. Every rewrite needs a worksheet line.
