---
name: comment
description: Write, review or clean up TypeScript code comments (TSDoc doc comments for the API, Why-not comments in implementations). Not for commit messages or prose docs.
argument-hint: "[file, directory or declaration to comment]"
model: sonnet
allowed-tools: Read Grep Glob Edit LSP AskUserQuestion Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/ts_comments.py *) Bash(git log *) Bash(git blame *) Bash(git show *) Bash(git diff *) Bash(git status *) Bash(npx --no-install eslint *)
---

# TypeScript Comment

Write comments for TypeScript code following three sources:

- **Where information goes**: t_wada's principle 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」. Details, the Why supplement and TypeScript examples: [references/comment-routing.md](references/comment-routing.md).
- **How doc comments are written**: TSDoc. Tags, layout and the JSDoc habits to drop: [references/tsdoc.md](references/tsdoc.md).
- **How links are written**: TSDoc declaration references (`{@link pkg!Foo#bar}`): [references/declaration-reference.md](references/declaration-reference.md). Read it before writing any `{@link}`, `{@inheritDoc}` or `@see`.

Read the first two references before editing. If an `LSP` tool is available, also read [references/lsp.md](references/lsp.md). Ask the user questions in Japanese. Write comment text in the language the file or package already uses for comments; if it has none, use English.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Change comments only.** Do not change code, not even formatting, imports, types, modifiers or decorators. Renames, extracted functions, narrower types and new tests are proposals for the report, applied only if the user already agreed in this conversation.
2. **Never delete, move or reword** `DIRECTIVE` comments (`// @ts-expect-error`, `// @ts-ignore`, `// eslint-disable-next-line`, `// prettier-ignore`, `/// <reference>`, `/* #__PURE__ */`, `/* webpackChunkName */` ...) or `LICENSE` comments. Do not touch an existing `TODO`/`FIXME` except to ask about a vague one. A reason for a directive goes on its own `//` line *above* the directive, never between the directive and its code.
3. **Never invent a reason.** Every Why or Why not you write needs evidence: a commit you read (`git show` / `git log -L`), an issue reference already in the code, or the user's answer. Carry issue IDs (`#42`, `PROJ-123`) from the evidence into the comment. No hedged reasons ("probably", "may be because") and no "confirm this" placeholders in the code.
4. **Document only what the code shows.** TypeScript has no checked exceptions: write `@throws` only for a `throw` you can see in the body or a callee whose contract you read (or hovered), with the condition taken from that code. Mention `undefined`/`null` results only for paths you can see. Write no units, ranges, defaults, complexity or side-effect claims you cannot point to in the declaration, its body, or an existing doc; a guess becomes a question.
5. **If you cannot ask** (no `AskUserQuestion` tool, or a non-interactive run), don't stop and don't guess: leave that spot as it is and list the question in the report.

## Working efficiently

- Use Bash only for the `ts_comments.py`, `git` and `npx --no-install eslint` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read; never `ls`, `cat`, `grep` or `find` in Bash.
- Send independent calls together in one message (all of Step 2's commands; Step 5's checks 1 and 2).
- Read each target file once. After an `Edit`, don't Read the file again to confirm; the tool reports failures.
- Code pasted into the conversation instead of a file: skip the snapshot and the script commands, apply every other step to the pasted code, and return the result in the reply.

## Step 1: Fix the scope and take a snapshot

1. Target = `$ARGUMENTS` (a file, directory or declaration name). If empty, use the `.ts`/`.tsx`/`.mts`/`.cts` files from `git status --short`. If that is empty too, ask.
2. Resolve the target to a list of files. Skip `node_modules/`, build output (`dist/`, `build/`, `lib/` or `out/` when `package.json` or `tsconfig.json` names it as output), generated files (`*.generated.ts`, `*.gen.ts`, a "generated" / "do not edit" header) and `.d.ts` files emitted by the build, unless named. For a declaration name, find its file with LSP `workspaceSymbol` if available, else Grep `(function|class|interface|type|enum|const) Name\b`.
3. Find project settings, once: Glob `**/tsdoc.json`, `**/typedoc.json`, `**/api-extractor.json` (exclude `node_modules`), and Grep the nearest `package.json` for `typedoc`, `@microsoft/api-extractor`, `eslint-plugin-tsdoc`, `eslint-plugin-jsdoc`. Remember:
   - **Link syntax**: `api-extractor.json` present → follow the link style already used in the codebase (API Extractor's parser accepts the older `{@link pkg#Foo.bar}` style); otherwise use declaration references per the reference file.
   - **Release tags** (`@public`, `@beta`, `@alpha`, `@internal`): add them only if the codebase already uses them.
   - **Doc scope**: if most non-exported top-level declarations already have `/** */`, pass `--internal` to `list` and `lint`.
   - **Custom tags**: `lint` reads `tsdoc.json` and allows TypeDoc's tags by itself. For any other tag the build registers, pass `--tags name1,name2`.
   - **ESLint**: `eslint-plugin-tsdoc` or `eslint-plugin-jsdoc` in `package.json` → run `npx --no-install eslint <files...>` in Step 5.
4. Snapshot the files before any edit, and remember the printed directory:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/ts_comments.py snapshot <files...>
   ```

## Step 2: Inventory

Collect, without reading more than needed:

- **Existing comments and undocumented API**: `python3 ${CLAUDE_SKILL_DIR}/scripts/ts_comments.py list <files...>`. It tags each comment `DOC`, `ORPHAN_DOC` (a `/** */` that documents nothing), `DIRECTIVE`, `LICENSE`, `TODO`, `FIXME`, `LINE` or `BLOCK`, then prints `UNDOCUMENTED` for each exported declaration and each non-private member of an exported class, interface or enum without a doc comment. `override` members and the later signatures of an overload are not listed: they inherit or share the doc.
- **Existing doc-comment problems**: `python3 ${CLAUDE_SKILL_DIR}/scripts/ts_comments.py lint <files...>` (plus the options from Step 1). It runs its own TSDoc checks, and the `@microsoft/tsdoc` parser when the project has it installed.
- **History of odd code**: for each `LINE`/`BLOCK` comment, and each spot that looks deliberate but strange, run `git log -L <start>,<end>:<file> --format=%h%n%s%n%b -n 3` and read the commit bodies. This is where Why and Why not usually are.
- **Callers and tests**, only for declarations whose contract is unclear from the body: LSP as in [references/lsp.md](references/lsp.md), else Grep for the name in `*.test.ts`, `*.spec.ts`, `__tests__/` and the sources. Read two or three call sites, not all.

Then Read each target file once, in full.

## Step 3: Classify

Write a short worksheet in your reply before editing, one line per existing comment and per spot where you might add one:

```
<file>:<line> | <quote, ≤8 words> | How / What / Why / Why not / TODO / API doc / directive | delete / move to doc / keep / rewrite / write / ask | evidence (commit hash, issue, —)
```

Decide each line with this table:

| Kind | Action |
|---|---|
| **How** (restates the code or the type) | Delete. If the code is unclear without it, add a rename or extract proposal to the report. |
| **What** on an exported declaration | Move it into the doc comment, then delete the `//` comment. |
| **What** elsewhere (spec of internal behavior) | Propose a test that pins it; keep the comment until the user agrees. |
| **Why** (reason for a change) | Draft it into a commit message for the report. If editing the line without knowing it would break something, also keep it as a `//` comment. |
| **Why not** (rejected alternative, workaround, deliberate non-optimization) | Keep or write a `//` comment above the line: the alternative, the reason, when the premise stops holding, the issue ID if any. |
| **TODO / FIXME** | Keep. If it has no owner, issue ID or condition, ask for one (rule 5 if you can't). |
| **API doc** (an `UNDOCUMENTED` line, or a `DOC` comment with lint findings) | Write or fix the doc comment in Step 4. |
| `DIRECTIVE` / `LICENSE` | Keep exactly (rule 2). A directive without a reason: if the evidence gives one, write it on a `//` line above; otherwise ask. |
| `ORPHAN_DOC` | Above a declaration but separated by another `/** */`: merge them into one doc comment (keep the text). Inside a function body or before a statement: turn `/**` into `//` (or `/*`), keeping the text, then classify the text like any other comment. Never delete it unread. |
| Commented-out code, change history, author/date notes | Delete; version control keeps them. Commented-out code with a reason for keeping it → ask. |

Batch every question for the user into one `AskUserQuestion` call (up to 4 questions; one per spot; offer 「理由はない / 分からない」 as an option). Apply the answers before Step 4.

## Step 4: Edit

- Apply the worksheet: one `Edit` per item, top of file to bottom.
- Write a doc comment for every `UNDOCUMENTED` line and fix every lint finding in comments, following [references/tsdoc.md](references/tsdoc.md). Use this shape, keeping only the parts that apply:

  ````ts
  /**
   * <Summary: one sentence a caller can act on; ends with "." (or 「。」).>
   *
   * @remarks
   * <What a caller can't see in the signature: side effects, I/O, mutation of arguments,
   * caching, ordering, accepted and default values, `undefined` handling.>
   *
   * @typeParam T - <type parameter meaning>
   * @param name - <meaning and accepted range>
   * @returns <what comes back; when it is `undefined` or empty>
   * @throws {@link SomeError} if <condition>
   *
   * @example
   * ```ts
   * <short, compilable usage>
   * ```
   */
  ````

- Summary: say what the element does or is, in the caller's terms; don't restate its name (`SUMMARY_RESTATES`). English functions start with a third-person verb ("Returns ...").
- One `@param name - ...` per named parameter in declaration order (destructured parameters: document the parameter by a name that reads well, e.g. `options`); `@typeParam` for each type parameter; `@returns` unless the return type is `void`, `Promise<void>` or `never`. No JSDoc types in braces: TypeScript has them.
- Overloads: document each overload signature; the implementation signature gets none. Members marked `override` that keep the parent's contract get no doc comment; one that changes behavior: `{@inheritDoc Base.member}` then `@remarks` with the difference.
- Code words in backticks; the first mention of another declaration in `{@link ...}` (declaration reference syntax; check the target exists first). Escape a literal `{`, `}` or `@` in text with a backslash, or put it in backticks.
- A `@deprecated` tag says what to use instead.
- Place the doc comment directly above the declaration, above its decorators, and above `export`.
- An `UNDOCUMENTED` element you can't describe from evidence (rule 4) → ask; don't write a summary that only restates the name.

## Step 5: Verify

Run each check, fix what your edits caused, and re-run until clean, at most 3 rounds:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/ts_comments.py check --base <snapshot dir> <files...>`: every file must print `OK`. A `CODE` line means you changed code or a string: undo it. A `DIRECTIVE` or `LICENSE` line means you broke rule 2: restore that comment exactly where it was.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/ts_comments.py lint <files...>` (same options as Step 2): no `ERROR` lines in comments you wrote or touched, and no `WARN` lines you caused. Leave pre-existing findings in comments you didn't touch for the report.
   - `LINK_UNRESOLVED` means the link target is not declared or imported in that file. Confirm it exists (LSP `workspaceSymbol` or Grep), then keep the link and say so in the report, or fix the reference.
   - `SKIP tsdoc-parser` means the project lacks `@microsoft/tsdoc`; the script's own checks still ran. Say so in the report.
3. If Step 1 found an ESLint TSDoc/JSDoc plugin: `npx --no-install eslint <files...>`. Fix comment findings you caused; ignore findings about code.
4. Re-run `list` and confirm every `UNDOCUMENTED` line in scope is gone, or listed in the report with the reason it was left.

If a command cannot run, say so in the report. Never report a check you did not run as passed.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## 変更したコメント
### 削除(How)
### TSDoc へ移動・追加(What)
### 残した・書いた Why not
### TODO / FIXME
## 提案(未適用)
## コミットメッセージ案(Why)
## 確認できなかった点(質問)
## 検証結果
```

Under コミットメッセージ案, write only a subject line and a body taken from the Why evidence: no trailers (`Co-Authored-By`, session links, model names). Under each 変更したコメント heading, list `file:line` and a one-line reason. Use line numbers from the Step 2 `list` output (before editing) for changed or deleted comments, and say 「(編集前の行番号)」 once. Under 検証結果, give each Step 5 command with its outcome (e.g. `check: OK 3 files`, `lint: ERROR 0 / WARN 2 (既存)`), plus the one line from [references/lsp.md](references/lsp.md) on how code was read. Do not commit unless the user asks.
