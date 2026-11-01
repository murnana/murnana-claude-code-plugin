# Using SourceKit-LSP (optional) and Keeping Context Small

When a Swift language server is running, use the `LSP` tool to fetch only the facts a comment needs instead of reading whole files. It is an aid, never a requirement: everything in this skill works with Read / Grep / Glob and `swift_comments.py`.

## Where the server comes from

- This plugin bundles no `.lsp.json`. The server comes from the official `swift-lsp` plugin (`/plugin install swift-lsp@claude-plugins-official`) plus `sourcekit-lsp`, which ships with the Swift toolchain (Xcode on macOS, the swift.org toolchain on Linux). Bundling a second config would start a second server for the same files.
- Claude Code never starts plugin language servers in cloud sessions, so the `LSP` tool is inactive there.
- Cross-file results (`findReferences`, `workspaceSymbol`, call hierarchy) need SourceKit-LSP's index:
  - SwiftPM packages: indexed in the background by default from Swift 6.1. The first run on a large package takes a while.
  - Xcode projects (`.xcodeproj` / `.xcworkspace` without `Package.swift`): SourceKit-LSP needs a build server (for example `xcode-build-server`) to know the build settings. Without one, trust only single-file operations (`documentSymbol`, `hover` on symbols declared in the same file).

## Step 0: Decide whether to use it

1. No `LSP` tool in this session → skip LSP for the whole run. Don't ask the user to install anything mid-task; mention it once in the report.
2. Otherwise make one probe call: `documentSymbol` on the first target file.
   - Symbols returned → use LSP for the rest of the run.
   - Error result → skip LSP for the rest of the run.
   - Empty result on a non-empty file, or a timeout → the index may still be building. Continue with Read / Grep, and retry once later in the run, not in a loop.

## What to ask the server

| Need | Operation | Instead of |
|---|---|---|
| Declarations in a file, their kinds and line ranges | `documentSymbol` | Reading the whole file to find them |
| Resolved signature, inferred types, `throws`/`async`, existing doc comment | `hover` on the declaration's name | Reading the declaration and its surroundings |
| A callee's contract (what it throws, when it returns `nil`) | `hover` on the call, then `goToDefinition` only if hover is not enough | Reading the callee's file |
| How callers use an API (arguments passed, `nil` handling, `try`/`catch`) | `findReferences`, or `prepareCallHierarchy` + `incomingCalls` | Grep plus reading every caller |
| Which callees can throw, before writing `- Throws:` | `prepareCallHierarchy` + `outgoingCalls`, then `hover` on each throwing callee | Reading every callee body |
| Protocol requirement an implementation satisfies | `goToDefinition` on the protocol, `goToImplementation` from the requirement | Reading the type hierarchy by hand |
| Target of a ` ``Symbol`` ` link exists | `workspaceSymbol` | Grep across the package |

Rules:

- Positions are 1-based line and character as shown by `Read`. Put the cursor on the identifier, not on `func`, a modifier or an attribute.
- Look at two or three references to infer a contract; do not read every reference.
- An empty `findReferences` result does not prove a symbol is unused (protocol witnesses, `@objc`, key paths, other modules). Confirm with Grep before relying on it.
- When LSP and the files disagree, trust the files and say in the report which source said what.

## Narrow reads without the LSP

- Get the declaration list from `python3 ${CLAUDE_SKILL_DIR}/scripts/swift_comments.py list <files...>` (it prints undocumented `public`/`open` declarations with line numbers), and `Grep -n` with a tight pattern (`func name\b`, `(struct|class|enum|actor|protocol) Name\b`) limited by `glob: "*.swift"`.
- Read a whole file only when it is a target. For other files, Read the matched line range (`offset`/`limit`) with a few lines of margin.

## Other ways to keep context small

- Work file by file. Finish and verify one file before opening the next.
- Limit history to the lines you comment on: `git log -L <start>,<end>:<file> --format='%h %s%n%b' -n 3`, not `git log -p`.
- When the target is "the current change", start from `git diff --stat` and `git diff -U3 -- <file>`.
- Don't re-read a file after `Edit`; the tool reports failures, and `lint` / `check` verify the result.

## Report

Add one line to the report saying how code was read:

- LSP used: say so, and list any result that Grep had to correct.
- LSP not used: give the reason (no `LSP` tool, cloud session, server failed to start, index not ready). If the tool was missing, suggest installing `swift-lsp@claude-plugins-official` for more accurate type and reference lookups.

## Sources

- Code intelligence plugins: https://code.claude.com/docs/en/plugins/code-intelligence.md
- LSP tool behavior: https://code.claude.com/docs/en/tools-reference.md#lsp-tool-behavior
- SourceKit-LSP: https://github.com/swiftlang/sourcekit-lsp
