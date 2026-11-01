# Using Eclipse JDT LS (optional) and Keeping Context Small

When a Java language server is running, use the `LSP` tool to fetch only the facts a comment needs instead of reading whole files. It is an aid, never a requirement: everything in this skill works with Read / Grep / Glob and `java_comments.py`.

## Where the server comes from

- This plugin bundles no `.lsp.json`. The server comes from the official `jdtls-lsp` plugin (`/plugin install jdtls-lsp@claude-plugins-official`) plus a `jdtls` command on the PATH (Eclipse JDT Language Server; `brew install jdtls` on macOS, otherwise the archive from https://download.eclipse.org/jdtls/ with a wrapper script). It needs JDK 17+ to run, whatever release the project targets. Bundling a second config would start a second server for the same files.
- Claude Code never starts plugin language servers in cloud sessions, so the `LSP` tool is inactive there.
- JDT LS imports Maven and Gradle projects (and plain Eclipse projects). Without a build file it treats files as standalone: trust only single-file operations (`documentSymbol`, `hover` on symbols declared in the same file).
- The first start imports the project and downloads dependencies; on a large Gradle build this can take minutes.

## Step 0: Decide whether to use it

1. No `LSP` tool in this session → skip LSP for the whole run. Don't ask the user to install anything mid-task; mention it once in the report.
2. Otherwise make one probe call: `documentSymbol` on the first target file.
   - Symbols returned → use LSP for the rest of the run.
   - Error result → skip LSP for the rest of the run.
   - Empty result on a non-empty file, or a timeout → the project may still be importing. Continue with Read / Grep, and retry once later in the run, not in a loop.

## What to ask the server

| Need | Operation | Instead of |
|---|---|---|
| Declarations in a file, their kinds and line ranges | `documentSymbol` | Reading the whole file to find them |
| Resolved signature, generic bounds, `throws` clause, existing or inherited Javadoc | `hover` on the declaration's name | Reading the declaration and its supertypes |
| A callee's contract (what it throws, when it returns `null`) | `hover` on the call, then `goToDefinition` only if hover is not enough | Reading the callee's file |
| How callers use an API (arguments passed, `null` checks, `catch` blocks) | `findReferences`, or `prepareCallHierarchy` + `incomingCalls` | Grep plus reading every caller |
| Which callees can throw, before writing `@throws` | `prepareCallHierarchy` + `outgoingCalls`, then `hover` on each callee | Reading every callee body |
| The parent doc an override inherits; whether an override changes the contract | `goToDefinition` on the supertype method, `goToImplementation` from an interface method | Reading the type hierarchy by hand |
| Target of a `{@link}` / `@see` exists, and its qualified name | `workspaceSymbol` | Grep across the project |

Rules:

- Positions are 1-based line and character as shown by `Read`. Put the cursor on the identifier, not on a modifier, an annotation or the return type.
- Look at two or three references to infer a contract; do not read every reference.
- An empty `findReferences` result does not prove a member is unused (reflection, dependency injection, serialization, frameworks calling by name, other modules). Confirm with Grep before relying on it.
- After an `Edit`, Claude Code shows the server's new diagnostics for the file. JDT LS reports Javadoc problems only when the project enables them, so `java_comments.py lint` stays the check of record. Ignore diagnostics about code you didn't touch.
- When LSP and the files disagree, trust the files and say in the report which source said what.

## Narrow reads without the LSP

- Get the declaration list with line numbers from `python3 ${CLAUDE_SKILL_DIR}/scripts/java_comments.py list <files...>`, and use `Grep -n` with a tight pattern (`\bname\s*\(`, `(class|interface|enum|record) Name\b`) limited by `glob: "*.java"`.
- Read a whole file only when it is a target. For other files, Read the matched line range (`offset`/`limit`) with a few lines of margin.

## Other ways to keep context small

- Work file by file. Finish and verify one file before opening the next.
- Limit history to the lines you comment on: `git log -L <start>,<end>:<file> --format=%h%n%s%n%b -n 3`, not `git log -p`.
- When the target is "the current change", start from `git diff --stat` and `git diff -U3 -- <file>`.
- Don't re-read a file after `Edit`; the tool reports failures, and `lint` / `check` verify the result.

## Report

Add one line to the report saying how code was read:

- LSP used: say so, and list any result that Grep had to correct.
- LSP not used: give the reason (no `LSP` tool, cloud session, server failed to start, project still importing). If the tool was missing, suggest installing `jdtls-lsp@claude-plugins-official` and `jdtls` for more accurate type and reference lookups.

## Sources

- Code intelligence plugins: https://code.claude.com/docs/en/plugins/code-intelligence.md
- LSP tool behavior: https://code.claude.com/docs/en/tools-reference.md#lsp-tool-behavior
- Eclipse JDT LS: https://github.com/eclipse-jdtls/eclipse.jdt.ls
