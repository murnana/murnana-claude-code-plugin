---
name: comment
description: Write, review or clean up Python code comments (PEP 257 docstrings for the API, Why-not comments in implementations). Not for commit messages or prose docs.
argument-hint: "[file, directory or function to comment]"
model: sonnet
allowed-tools: Read Grep Glob Edit LSP AskUserQuestion Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/py_comments.py *) Bash(ruff check *) Bash(git log *) Bash(git blame *) Bash(git show *) Bash(git diff *) Bash(git status *)
---

# Python Comment

Write comments for Python code following two sources:

- **Where information goes**: t_wada's principle 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」. The why-not shape, where reasons come from, and more examples (including Japanese): [references/why-not-comments.md](references/why-not-comments.md).
- **How docstrings are written**: PEP 257 and the project's docstring style (Google when none is set): [references/pep-257.md](references/pep-257.md) and [references/docstring-styles.md](references/docstring-styles.md).

Read [references/why-not-comments.md](references/why-not-comments.md) and the Google section of [references/docstring-styles.md](references/docstring-styles.md) before editing; read the other style sections and [references/pep-257.md](references/pep-257.md) when Step 1 or Step 4 says so. Ask the user questions in Japanese. Write comment text in the language the file already uses for comments and docstrings; if it has none, use English. Never translate existing comments.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Change comments and docstrings only.** Do not change code, not even formatting, imports, type hints or decorators. Renames, extracted functions and new tests are proposals for the report, applied only if the user already agreed in this conversation.
2. **Never delete** license or copyright headers, the shebang and coding lines, tool directives (`# noqa`, `# type: ignore`, `# pragma: no cover`, `# pylint:`, `# fmt: off/on`, `# isort:`, `# ruff:`), or an existing `TODO`/`FIXME`. You may reword a TODO; a vague one goes to the user as a question.
3. **Never invent a reason.** Every Why or Why not you write needs a source from Step 2's list. A reason inferred from the code alone is a guess, even when it is plausible. No hedged reasons ("probably", "may be because", "(confirm this)") and no `TODO: verify` placeholders in the code.
4. **Document only what the code shows.** `Raises:` only for a `raise` you can see in the body or a callee whose contract you read (or hovered), with the condition taken from that code. `None` results only for paths you can see. Write no units, ranges, side-effect or thread-safety claims you cannot point to in the code or an existing doc; a guess becomes a question.
5. **If you cannot ask** (no `AskUserQuestion` tool, a non-interactive run, or the user said they are away), don't stop and don't guess: leave that spot without a comment, and list it, your candidate reasons and the question to answer in the report.

## Working efficiently

- Use Bash only for the `py_comments.py`, `ruff check` and `git` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read; never `ls`, `cat`, `grep` or `find` in Bash.
- Send independent calls together in one message (all of Step 2's commands; Step 5's checks 1 and 2).
- Read each target file once. After an `Edit`, don't Read the file again to confirm; the tool reports failures.
- Code pasted into the conversation instead of a file: skip the snapshot and the script commands, apply every other step to the pasted code, and return the full updated code in the reply.

## Step 1: Fix the scope and take a snapshot

1. Target = `$ARGUMENTS` (a file, directory or function). If empty, use the `.py` files from `git status --short`. If that is empty too, ask.
2. Resolve the target to a list of files. Skip generated code (`*_pb2.py`, migrations, a "generated" header) and virtual environments unless named.
3. Find project settings, once. Project instructions (`CLAUDE.md`, `.claude/rules/`, `CONTRIBUTING.md`) override this skill.
   - **Docstring style**: Glob for `pyproject.toml`, `ruff.toml`, `.ruff.toml`, `setup.cfg`, `tox.ini`, `.pydocstyle`, `docs/conf.py`; read the ones that exist for a pydocstyle `convention` or Sphinx `napoleon_*` / `numpydoc` settings. If none decides it, follow the existing docstrings in the package; if those don't either, use **Google**. For NumPy, reST or plain PEP 257, read that section of [references/docstring-styles.md](references/docstring-styles.md).
   - **Python version**: note `requires-python`. It is often the reason for a why-not.
4. Snapshot the files before any edit, and remember the printed directory:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/py_comments.py snapshot <files...>
   ```

## Step 2: Inventory

Collect, without reading more than needed:

- **Existing comments and undocumented API**: `python3 ${CLAUDE_SKILL_DIR}/scripts/py_comments.py list <files...>`. It tags each `#` comment `DIRECTIVE`, `LICENSE`, `SHEBANG`, `TODO`, `FIXME` or `LINE`, then prints `UNDOCUMENTED` for the module and each public class and function (including `__init__` with arguments) without a docstring.
- **Reasons for odd code**, used in this order: the user's request and the conversation; the code and config (`requires-python`, pinned versions, nearby code and tests); who depends on the behavior (LSP `findReferences`, else Grep); history (`git log -L <start>,<end>:<file> --format=%h%n%s%n%b -n 3`, then `git show <sha>`).
- **Callers and tests**, only for functions whose contract is unclear from the body. Read two or three call sites, not all.

Then Read each target file once, in full.

## Step 3: Classify

Write a short worksheet in your reply before editing, one line per existing comment and per spot where you might add one:

```
<file>:<line> | <quote, ≤8 words> | How / What / Why / Why not / TODO / API doc / directive | delete / move to doc / keep / rewrite / write / ask | evidence (commit hash, issue, —)
```

For each `#` comment, take the **first** row that matches:

| Kind | Action |
|---|---|
| Commented-out code | Delete; version control keeps it. With a reason for keeping it → ask. |
| **Why** told as history (a ticket with "fixed", a date, "used to", "changed") | Delete it from the code and draft its content into a commit message for the report. If the code still looks unnecessary without it, also write a why-not that states the reason without the history. |
| `DIRECTIVE` / `LICENSE` / `SHEBANG` | Keep exactly (rule 2). A directive without a reason: if a source gives one, write it on a `#` line above; otherwise ask. |
| **TODO / FIXME** | Keep. If it has no owner, issue link or condition, ask for one (rule 5 if you can't). |
| **What** a caller relies on ("returns None when missing") | Move it into the docstring, then delete the `#` comment. Propose a test for it in the report. |
| **Why not** (why written this way, or why not another way) | Keep, or rewrite it in the shape below if it doesn't name the alternative. |
| **How** (anything else: restates the code) | Delete. If the code is unclear without it, add a rename or extract proposal to the report. |

Write a new why-not only where a competent reviewer would suggest a different approach: a newer API that can't be used yet, a workaround for a library bug, deliberately simple or slow code, a narrow or broad `except` chosen on purpose, a copy, lock or ordering that looks unnecessary.

Batch every question for the user into one `AskUserQuestion` call (up to 4 questions; one per spot: show the line and the alternative; offer 「理由はない / 分からない」 as an option). Apply the answers before Step 4.

## Step 4: Edit

- Apply the worksheet: one `Edit` per item, top of file to bottom.
- **Why-not shape** (one or two lines, directly above the code it explains):

  ```python
  # asyncio.wait_for() instead of asyncio.timeout(): timeout() needs Python 3.11,
  # and requires-python is ">=3.10". Switch once 3.10 support is dropped.
  ```

- **Docstrings** for every `UNDOCUMENTED` line (skip private helpers unless their contract isn't obvious; skip test functions unless the project's tests already have docstrings):
  - Always `"""` (`r"""` with a backslash). Summary: one line ending with a period, imperative mood ("Return the user.", not "Returns ..."); a noun phrase is fine for a class or module. Never repeat the signature.
  - One-liner: quotes on the same line. Multi-line: summary, blank line, details or sections, closing `"""` on its own line.
  - Function: effect, each argument, return value, side effects, exceptions the caller should handle (rule 4), restrictions on when it may be called. Leave out empty sections. Class: behavior and public attributes; constructor arguments go in `__init__` (NumPy: in the class docstring). Module: summary, then exported names one line each.
  - Never in a docstring: types already in the annotations, implementation details, history, why-nots that don't change what callers see.
  - Google sections: `Args:`, `Returns:`, `Yields:`, `Raises:`, `Attributes:`; `Examples:` with doctest only if the project runs doctests. Read [references/pep-257.md](references/pep-257.md) for scripts, packages, and classes meant to be subclassed.
- An `UNDOCUMENTED` object you can't describe from evidence (rule 4) → ask; don't write a summary that only restates the name.

## Step 5: Verify

Run each check, fix what your edits caused, and re-run until clean, at most 3 rounds:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/py_comments.py check --base <snapshot dir> <files...>`: every file must print `OK`. A `CODE` line means you changed code: undo that change. A `DIRECTIVE` or `LICENSE` line means you broke rule 2: restore that comment exactly.
2. If Ruff is installed: with `D` rules or a pydocstyle convention in the project config, `ruff check <files...>`; otherwise `ruff check --isolated --select D --config 'lint.pydocstyle.convention = "<google|numpy|pep257>"' <files...>` (`pep257` for reST and plain). Fix findings on lines you wrote or changed; mention missing docstrings on untouched code at most once. If `ruff` isn't found, don't install it; say so.
3. Re-run `list` and confirm every `UNDOCUMENTED` line in scope is gone, or listed in the report with the reason it was left.
4. Re-read every comment and docstring you wrote or kept: does it say something the code can't, would it stay true if the body were rewritten without changing behavior, and is every why-not reason from a Step 2 source?

If a command cannot run, say so in the report. Never report a check you did not run as passed.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## 変更したコメント
### 削除(How)
### docstring へ移動・追加(What)
### 残した・書いた Why not
### TODO / FIXME
## 提案(未適用)
## コミットメッセージ案(Why)
## 確認できなかった点(質問)
## 検証結果
```

Under コミットメッセージ案, write only a subject line and a body taken from the Why evidence: no trailers (`Co-Authored-By`, session links, model names). Under each 変更したコメント heading, list `file:line` and a one-line reason, quoting the old comment for deletions. Use line numbers from the Step 2 `list` output (before editing) for changed or deleted comments, and say 「(編集前の行番号)」 once. Under 確認できなかった点, give each spot where a why-not seems needed but no source was found, with the question to answer. Under 検証結果, give each Step 5 command with its outcome (e.g. `check: OK 2 files`, `ruff: 0 errors`). Do not commit unless the user asks.

## Gotchas

- Update or delete the comments your edit makes wrong. A stale comment misleads more than a missing one.
- Ruff's `google` convention doesn't enforce the imperative mood. Still use it, unless the file already uses "Returns ..." consistently.
- PEP 257 puts a blank line after a class docstring; Ruff's `pep257` and `numpy` conventions require it (D204), `google` doesn't. Follow the project's formatter or linter.
- In running text, write argument names exactly (`timeout`), never in upper case. For a subclass method, "Override" means it replaces the parent's method without calling it, "Extend" means it calls `super()`.
