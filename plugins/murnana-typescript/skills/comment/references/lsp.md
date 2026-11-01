# Using typescript-language-server (optional) and Keeping Context Small

When a TypeScript language server is running, use the `LSP` tool to fetch only the facts a comment needs instead of reading whole files. It is an aid, never a requirement: everything in this skill works with Read / Grep / Glob and `ts_comments.py`.

## Where the server comes from

- This plugin bundles no `.lsp.json`. The server comes from the official `typescript-lsp` plugin (`/plugin install typescript-lsp@claude-plugins-official`) plus a `typescript-language-server` command on the PATH (`npm install -g typescript-language-server typescript`). Bundling a second config would start a second server for the same files.
- Claude Code never starts plugin language servers in cloud sessions, so the `LSP` tool is inactive there.
- The server uses the nearest `tsconfig.json` / `jsconfig.json`. Files outside every project are treated as standalone: trust only single-file operations (`documentSymbol`, `hover` on symbols declared in the same file). In monorepos, imports across packages may show as unresolved until dependencies are installed and built.

## Step 0: Decide whether to use it

1. No `LSP` tool in this session → skip LSP for the whole run. Don't ask the user to install anything mid-task; mention it once in the report.
2. Otherwise make one probe call: `documentSymbol` on the first target file.
   - Symbols returned → use LSP for the rest of the run.
   - Error result → skip LSP for the rest of the run.
   - Empty result on a non-empty file, or a timeout → the project may still be loading. Continue with Read / Grep, and retry once later in the run, not in a loop.

## What to ask the server

| Need | Operation | Instead of |
|---|---|---|
| Declarations in a file, their kinds and line ranges | `documentSymbol` | Reading the whole file to find them |
| Resolved signature, inferred return type, generic constraints, existing or inherited doc | `hover` on the declaration's name | Reading the declaration, its imports and supertypes |
| The return type of a function without an annotation (for `@returns`) | `hover` on the function name | Reasoning it out from the body |
| A callee's contract (what it throws, when it returns `undefined`) | `hover` on the call, then `goToDefinition` only if hover is not enough | Reading the callee's file |
| How callers use an API (arguments passed, `undefined` checks, `catch` blocks) | `findReferences`, or `prepareCallHierarchy` + `incomingCalls` | Grep plus reading every caller |
| Which callees can throw, before writing `@throws` | `prepareCallHierarchy` + `outgoingCalls`, then `hover` on each callee | Reading every callee body |
| The parent doc an `override` inherits; implementations of an interface member | `goToDefinition` on the base member, `goToImplementation` from the interface member | Reading the class hierarchy by hand |
| Target of a `{@link}` / `@see` exists, and where (for `LINK_UNRESOLVED`) | `workspaceSymbol` | Grep across the project |
| How a `{@link}` renders | `hover` on the documented declaration: TypeScript resolves `{@link}` targets in hovers | Guessing |

Rules:

- Positions are 1-based line and character as shown by `Read`. Put the cursor on the identifier, not on `export`, a modifier, a decorator or the return type.
- Look at two or three references to infer a contract; do not read every reference.
- An empty `findReferences` result does not prove a member is unused (dynamic property access, string-keyed lookups, framework conventions, other packages). Confirm with Grep before relying on it.
- After an `Edit`, Claude Code shows the server's new diagnostics for the file. The TypeScript server does not check TSDoc syntax, so `ts_comments.py lint` stays the check of record. A new diagnostic after a comment-only edit usually means a directive moved (e.g. "Unused '@ts-expect-error' directive"): restore it. Ignore diagnostics about code you didn't touch.
- When LSP and the files disagree, trust the files and say in the report which source said what.

## Narrow reads without the LSP

- Get the declaration list with line numbers from `python3 ${CLAUDE_SKILL_DIR}/scripts/ts_comments.py list <files...>`, and use `Grep -n` with a tight pattern (`\bname\s*[(<]`, `(class|interface|type|enum) Name\b`) limited by `glob: "*.{ts,tsx,mts,cts}"`.
- Read a whole file only when it is a target. For other files, Read the matched line range (`offset`/`limit`) with a few lines of margin.

## Other ways to keep context small

- Work file by file. Finish and verify one file before opening the next.
- Limit history to the lines you comment on: `git log -L <start>,<end>:<file> --format=%h%n%s%n%b -n 3`, not `git log -p`.
- When the target is "the current change", start from `git diff --stat` and `git diff -U3 -- <file>`.
- Don't re-read a file after `Edit`; the tool reports failures, and `lint` / `check` verify the result.

## Report

Add one line to the report saying how code was read:

- LSP used: say so, and list any result that Grep had to correct.
- LSP not used: give the reason (no `LSP` tool, cloud session, server failed to start, project still loading). If the tool was missing, suggest installing `typescript-lsp@claude-plugins-official` and `typescript-language-server` for more accurate type and reference lookups.

## Sources

- Code intelligence plugins: https://code.claude.com/docs/en/plugins/code-intelligence.md
- LSP tool behavior: https://code.claude.com/docs/en/tools-reference.md#lsp-tool-behavior
- typescript-language-server: https://github.com/typescript-language-server/typescript-language-server
