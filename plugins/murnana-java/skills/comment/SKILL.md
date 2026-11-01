---
name: comment
description: Write and clean up Java comments, placing How/What/Why/Why not where each belongs and writing Javadoc doc comments for the API.
when_to_use: Javaのコメントを書いて / このクラスにJavadocを付けて / 不要なコメントを整理して
argument-hint: "[file, directory or declaration to comment]"
model: sonnet
allowed-tools: Read Grep Glob Edit LSP AskUserQuestion Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/java_comments.py *) Bash(git log:*) Bash(git blame:*) Bash(git show:*) Bash(git diff:*) Bash(git status:*)
---

# Java Comment

Write comments for Java code following two sources:

- **Where information goes**: t_wada's principle 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」. Details, the Why supplement and Java examples: [references/comment-routing.md](references/comment-routing.md).
- **How doc comments are written**: the `javadoc` tool reference (Java SE 8, with later additions marked): [references/javadoc.md](references/javadoc.md).

Read both references before editing. If an `LSP` tool is available, also read [references/lsp.md](references/lsp.md). Ask the user questions in Japanese. Write comment text in the language the file or package already uses for comments; if it has none, use English.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Change comments only.** Do not change code, not even formatting, imports or annotations (adding `@Deprecated` is a code change). Renames, extracted methods, explicit constructors and new tests are proposals for the report, applied only if the user already agreed in this conversation.
2. **Never delete** license or copyright headers, `//CHECKSTYLE:`, `// NOSONAR`, `//noinspection`, `// @formatter:` and similar tool directives, the reason next to `@SuppressWarnings`, or an existing `TODO`/`FIXME`. You may reword them; a vague TODO goes to the user as a question.
3. **Never invent a reason.** Every Why or Why not you write needs evidence: a commit you read (`git show`), an issue reference already in the code, or the user's answer. Carry issue IDs (`#42`, `PROJ-123`) from the evidence into the comment. No hedged reasons ("probably", "may be because") and no "confirm this" placeholders in the code.
4. **Document only what the code shows.** `@throws` only for exceptions in the `throws` clause, a `throw` you can see in the body, or a callee whose contract you read (or hovered). Its condition ("if ...") must come from a `throw` you can see or a callee's documented contract; for a `throws`-clause exception with neither, ask instead of writing a condition. `null` cases in `@return` only for `return null` paths you can see. Write no units, limits, complexity or thread-safety claims you cannot point to in the declaration, its body, or an existing doc; a guess becomes a question.
5. **If you cannot ask** (no `AskUserQuestion` tool, or a non-interactive run), don't stop and don't guess: leave that spot as it is and list the question in the report.

## Working efficiently

- Use Bash only for the `java_comments.py` and `git` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read; never `ls`, `cat`, `grep` or `find` in Bash.
- Send independent calls together in one message (all of Step 2's commands; Step 5's checks 1 and 2).
- Read each target file once. After an `Edit`, don't Read the file again to confirm; the tool reports failures.
- Code pasted into the conversation instead of a file: skip the snapshot and the script commands, apply every other step to the pasted code, and return the result in the reply.

## Step 1: Fix the scope and take a snapshot

1. Target = `$ARGUMENTS` (a file, directory or declaration name). If empty, use the `.java` files from `git status --short`. If that is empty too, ask.
2. Resolve the target to a list of `.java` files. Skip generated code (under `target/`, `build/`, `generated-sources/`, or with a `@Generated` annotation or "generated" header) and `module-info.java` unless named. For a declaration name, find its file with LSP `workspaceSymbol` if available, else Grep `(class|interface|enum|record) Name\b`.
3. Find project settings, once: Glob `**/pom.xml` and `**/build.gradle*`. If none exist, use the defaults below and move on. Otherwise Grep those files for `-tag`, `<tags>`, `doclint`, `<show>`/`-package`/`-private`, and the Java release (`maven.compiler.release`, `<release>`, `sourceCompatibility`, `toolchain`). Remember:
   - custom tags (`apiNote`, `implSpec`, `implNote` ...) → pass `--tags apiNote,implSpec,implNote` to `lint`;
   - package-private docs generated, or most package-private declarations already have `/** */` → pass `--package` to `list` and `lint`;
   - the release, to decide which newer tags (`{@return}`, `{@snippet}` ...) are allowed. Unknown release → Java 8 tags only.
4. Snapshot the files before any edit, and remember the printed directory:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/java_comments.py snapshot <files...>
   ```

## Step 2: Inventory

Collect, without reading more than needed:

- **Existing comments and undocumented API**: `python3 ${CLAUDE_SKILL_DIR}/scripts/java_comments.py list <files...>`. It tags each comment `DOC`, `ORPHAN_DOC` (a `/** */` javadoc ignores), `TODO`, `FIXME`, `LINE` or `BLOCK`, then prints `UNDOCUMENTED` for each public/protected declaration (and interface member) without a doc comment. `@Override` methods are not listed: they inherit their doc.
- **Existing doc-comment problems**: `python3 ${CLAUDE_SKILL_DIR}/scripts/java_comments.py lint <files...>` (plus the options from Step 1). It runs javac's doclint when `javac` is on the PATH and its own checks.
- **History of odd code**: for each `LINE`/`BLOCK` comment, and each spot that looks deliberate but strange, run `git log -L <start>,<end>:<file> --format=%h%n%s%n%b -n 3` and read the commit bodies. This is where Why and Why not usually are.
- **Callers and tests**, only for declarations whose contract is unclear from the body: LSP as in [references/lsp.md](references/lsp.md), else Grep for the name under `src/test/` and the sources. Read two or three call sites, not all.

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
| **What** on an API declaration | Move it into the doc comment, then delete the `//` comment. |
| **What** elsewhere (spec of internal behavior) | Propose a test that pins it; keep the comment until the user agrees. |
| **Why** (reason for a change) | Draft it into a commit message for the report. If editing the line without knowing it would break something, also keep it as a `//` comment. |
| **Why not** (rejected alternative, workaround, deliberate non-optimization) | Keep or write a `//` comment above the line: the alternative, the reason, when the premise stops holding, the issue ID if any. |
| **TODO / FIXME** | Keep. If it has no owner, issue ID or condition, ask for one (rule 5 if you can't). |
| **API doc** (an `UNDOCUMENTED` line, or a `DOC` comment with lint findings) | Write or fix the doc comment in Step 4. |
| `ORPHAN_DOC` | Between annotations and a declaration: move it, text unchanged, above the annotations (then fix it like any `DOC`); never delete it. Inside a method body: turn `/**` into `//` (or `/*`), keeping the text, then classify the text like any other comment. |
| Commented-out code, change history, author/date notes | Delete; version control keeps them. Commented-out code with a reason for keeping it → ask. |

Batch every question for the user into one `AskUserQuestion` call (up to 4 questions; one per spot; offer 「理由はない / 分からない」 as an option). Apply the answers before Step 4.

## Step 4: Edit

- Apply the worksheet: one `Edit` per item, top of file to bottom.
- Write a doc comment for every `UNDOCUMENTED` line and fix every lint finding in comments, following [references/javadoc.md](references/javadoc.md). Use this shape, keeping only the parts that apply:

  ```java
  /**
   * <Summary: one sentence that stands alone; ends with "." (or 「。」 then a line break).>
   * <p>
   * <Description: what a caller can't see in the signature — side effects, blocking or
   * expensive work, accepted and default values, {@code null} handling, thread safety.>
   *
   * @param <T> <type parameter meaning>
   * @param name <meaning and accepted range>
   * @return <what comes back; when it is {@code null} or empty>
   * @throws SomeException if <condition>
   */
  ```

- Summary: say what the element does or is, in the caller's terms; don't restate its name (`SUMMARY_RESTATES`). English methods start with a third-person verb ("Returns ...").
- One `@param` per parameter in declaration order, type parameters first as `@param <T>`; records document their components with `@param` on the record. `@return` only for non-`void` methods. `@throws` per rule 4, condition starting with "if".
- Overrides that keep the parent's contract get no doc comment. One that changes or adds behavior: `{@inheritDoc}` then a `<p>` with the difference.
- Code words in `{@code ...}`; the first mention of another API element in `{@link ...}`. Escape `<`, `>`, `&` outside `{@code}`. No `<p/>` or `<br/>`.
- A `@Deprecated` element gets a `@deprecated` tag: since when and what to use instead. A `@deprecated` tag without the annotation → propose adding the annotation (rule 1).
- Place the doc comment directly above the declaration, above its annotations. One documented field per declaration: for `int a, b;`, write the comment and propose splitting the declaration.
- An `UNDOCUMENTED` element you can't describe from evidence (rule 4) → ask; don't write a summary that only restates the name.

## Step 5: Verify

Run each check, fix what your edits caused, and re-run until clean, at most 3 rounds:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/java_comments.py check --base <snapshot dir> <files...>`: every file must print `OK`. A `CODE` line means you changed code or a string literal: undo that change. A `DIRECTIVE` or `LICENSE` line means you broke rule 2: restore that comment exactly.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/java_comments.py lint <files...>` (same options as Step 2): no `ERROR` lines in comments you wrote or touched, and no `WARN` lines you caused. Leave findings that need a code change (`use of default constructor`, `DEPRECATED_ANNOTATION`) and pre-existing ones in comments you didn't touch for the report.
   - `NOTE doclint: ... compiler diagnostic(s) ... ignored` is expected when dependencies aren't on the classpath. Then a `reference not found` for a dependency type is not your error: confirm the type exists (Grep the imports or LSP), keep the link, and say so in the report.
   - `SKIP doclint` means no JDK: `lint` still checks tag names, `@param`/`@return`/`@throws` coverage and the summary; say doclint was skipped.
3. Re-run `list` and confirm every `UNDOCUMENTED` line in scope is gone, or listed in the report with the reason it was left.

If a command cannot run, say so in the report. Never report a check you did not run as passed.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## 変更したコメント
### 削除(How)
### Javadoc へ移動・追加(What)
### 残した・書いた Why not
### TODO / FIXME
## 提案(未適用)
## コミットメッセージ案(Why)
## 確認できなかった点(質問)
## 検証結果
```

Under コミットメッセージ案, write only a subject line and a body taken from the Why evidence: no trailers (`Co-Authored-By`, session links, model names). Under each 変更したコメント heading, list `file:line` and a one-line reason. Use line numbers from the Step 2 `list` output (before editing) for changed or deleted comments, and say 「(編集前の行番号)」 once. Under 検証結果, give each Step 5 command with its outcome (e.g. `check: OK 3 files`, `lint: ERROR 0 / WARN 2 (既存)`), plus the one line from [references/lsp.md](references/lsp.md) on how code was read. Do not commit unless the user asks.
