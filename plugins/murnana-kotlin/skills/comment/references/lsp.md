# Using the Kotlin language server (optional)

When a Kotlin language server is running, use the `LSP` tool to read code by symbol instead of by text. It is an aid for gathering facts, never a requirement: everything in this skill works with Read / Grep / Glob alone.

## Where the server comes from

- This plugin bundles no `.lsp.json`. The server is provided by the official `kotlin-lsp` plugin (`/plugin install kotlin-lsp@claude-plugins-official`) plus the `kotlin-lsp` binary from JetBrains (`brew install JetBrains/utils/kotlin-lsp`, or the standalone archive from https://github.com/Kotlin/kotlin-lsp/releases). Bundling a second config would start a second server for the same files.
- Claude Code never starts plugin language servers in cloud sessions, so the `LSP` tool is inactive there.
- JetBrains' Kotlin LSP is Alpha. It supports JVM projects built with Gradle or Maven; Android is experimental; Kotlin Multiplatform and Kotlin Toolchain (`module.yaml`) projects are not supported yet.

## Step 0: Decide whether to use it

1. If no `LSP` tool is available in this session, skip LSP for the whole run. Don't ask the user to install anything mid-task; mention it once in the report (see below).
2. If the project is Kotlin Multiplatform (a `kotlin("multiplatform")` / `org.jetbrains.kotlin.multiplatform` plugin, or `commonMain` source sets) or uses `module.yaml`, skip LSP: results would be incomplete.
3. Otherwise, make one probe call: `documentSymbol` on the first target file.
   - Symbols returned → use LSP for the rest of the run.
   - Error result (server can't start, binary not found) → skip LSP for the rest of the run.
   - Timeout or empty result on a non-empty file → the server may still be importing the project and building its index; the first start of a large Gradle project can take minutes. Continue with Read/Grep and retry LSP once later in the run, not in a loop.

## What to ask the server, per step of the skill

| Skill step | Operation | Use it to |
|---|---|---|
| Step 1 (scope) | `workspaceSymbol` | Find the file of a declaration named in the arguments. |
| Step 2 (inventory) | `documentSymbol` | Cross-check the script's `UNDOCUMENTED` list: classes, functions and properties in the file, and their visibility. |
| Step 2 | `hover` | Read the resolved signature, inferred types, nullability and any existing or inherited KDoc of a declaration. |
| Step 2 | `findReferences`, `incomingCalls` (after `prepareCallHierarchy`) | See how callers actually use a declaration: which arguments they pass, whether they handle `null` or catch exceptions. This shapes the contract in KDoc. References from other modules mean the declaration is API that needs KDoc. |
| Step 2 | `outgoingCalls` | Find what a function depends on, and which callees can throw, before writing `@throws`. |
| Step 3 (Why not) | `findReferences`, `goToImplementation` | Check a Why-not claim against the code, e.g. "plugins add cases at runtime": find the implementations that prove it. A claim the code contradicts is not written. |
| Step 4 (KDoc) | `goToDefinition` on an overridden member, `goToImplementation` on an interface member | Read the parent's documentation. An override that keeps the parent's contract needs no KDoc of its own. |
| Step 4 / Step 5 | `workspaceSymbol` | Confirm the target of a `[name]` link exists and find its qualified name when it is not imported. |

Positions given to the tool must point at the symbol's name, not at a keyword or a blank.

## Don't trust a result on its own

- An empty `findReferences` / `incomingCalls` result does not prove a declaration is unused. Confirm with Grep for the name (including reflection, DI, serialization and Java callers) before saying "unused" or dropping KDoc because "nobody calls it".
- If LSP and Grep disagree, trust what you can read in the files, and say in the report which source said what.
- Don't make edits based on diagnostics alone. After editing comments, read any diagnostics the server reports for the file. A warning about an unresolved KDoc link is a reason to fix the link. Other warnings that existed before your edit are not yours to fix; ignore them.

## Report

Add one line to the Japanese report saying how code was read:

- LSP used: say so, and list any results that Grep had to correct.
- LSP not available or skipped: say so with the reason (no `LSP` tool, cloud session, multiplatform project, server failed to start). If the reason was the missing tool, suggest installing the `kotlin-lsp` binary and `kotlin-lsp@claude-plugins-official` for more accurate reference and type lookups.

## Sources

- Code intelligence plugins: https://code.claude.com/docs/en/plugins/code-intelligence.md
- LSP tool behavior: https://code.claude.com/docs/en/tools-reference.md#lsp-tool-behavior
- Kotlin LSP: https://github.com/Kotlin/kotlin-lsp and https://kotlinlang.org/docs/kotlin-lsp.html
