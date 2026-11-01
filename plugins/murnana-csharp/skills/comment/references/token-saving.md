# Saving Tokens: Roslyn LSP First, Narrow Reads Second

The plugin registers Microsoft's Roslyn language server (`roslyn-language-server`, the server behind the VS Code C# extension) in `.lsp.json`. When it runs, Claude Code exposes the `LSP` tool and pushes diagnostics after each edit of a `.cs` file. Use it to fetch only the facts a comment needs instead of reading whole files.

## Is the LSP available?

- Call `LSP` `documentSymbol` on the first target file. A symbol list means the server is up.
- An error result means it is not: the binary is missing, the .NET 10 runtime is missing, or this is a cloud session (Claude Code does not start plugin language servers there). Do not retry; use the fallback below for the whole run, and mention it once in the report.
- Roslyn loads the solution on first use (a single `.sln`/`.slnx` at the root, otherwise every `.csproj`). The first call on a large solution can be slow; later calls are fast.

## What to ask the LSP for

| Need | LSP operation | Instead of |
|---|---|---|
| Members of a file and their line ranges | `documentSymbol` | Reading the whole file |
| Signature, parameter and return types, existing doc comment of a member | `hover` on the member name | Reading the declaration and its surroundings |
| Where a type or member is declared | `goToDefinition`, or `workspaceSymbol` by name | Grep plus reading every hit |
| Who calls it (for the contract and the Why) | `findReferences`, `incomingCalls` | Grep plus reading every caller file |
| Base member for `<inheritdoc/>` | `goToDefinition` on the base type / interface, `goToImplementation` from the interface | Reading the class hierarchy by hand |
| Which exceptions the member can let through | `outgoingCalls`, then `hover` on the callees | Reading every callee body |

Rules:

- Use `documentSymbol` to pick the members in scope, then `Read` only those line ranges (`offset`/`limit`) with a few lines of margin for existing comments and attributes.
- Ask `hover` before reading a callee: its signature and doc comment are usually all a caller's doc needs.
- Look at a small sample of references (two or three call sites) to infer the contract; do not read every reference.
- Positions are 1-based line and character as shown by `Read`; place the cursor on the identifier, not on a keyword or modifier.

## Diagnostics after edits

- After each `Edit`, Claude Code reports new diagnostics from the server. Fix doc-comment warnings as they appear (badly formed XML, `<param>` names that do not match, unresolved `cref`).
- Roslyn reports doc-comment warnings only when the project generates a documentation file. When the project does not, the diagnostics do not cover them; run the single filtered build below once at the end instead of after every edit.

## Fallback without the LSP

- Find declarations with `Grep` using `-n` and a tight pattern (`(class|record|struct|interface) Name\b`, `\bName\s*\(`), limited by `glob: "*.cs"` and `head_limit`.
- Read only the matched line ranges. Read a whole file only when it is the target and short.

## Other ways to keep context small

- Work file by file; finish and verify one file before opening the next.
- Limit history to the lines you comment on: `git log -L <start>,<end>:<file> --no-patch --format='%h %s%n%b'` or `git blame -L <start>,<end> <file>`, not the full `git log -p`.
- When the target is "the current change", start from `git diff -U0 --stat` and `git diff -U3 -- <file>` instead of reading whole files.
- Keep build output short with `dotnet build -p:GenerateDocumentationFile=true -v q -clp:NoSummary` (the exact command in SKILL.md Step 5; a pipe to `grep` would need a permission prompt). Read only the `CS1570`–`CS1734` lines for the files in scope.
- Do not re-read a file after `Edit` to check it; the diagnostics and the edit result are enough.
