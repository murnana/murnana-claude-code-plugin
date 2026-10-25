# Managed blocks

Each template lives in its own block so it can be refreshed or removed later without touching the user's own lines.

## Format

```gitignore
# --- BEGIN murnana/gitignore Unity.gitignore (e4410f4e4a88) ---
<template text, verbatim>
# --- END murnana/gitignore Unity.gitignore ---
```

- The name is the template's path in murnana/gitignore (`Unity.gitignore`, `Global/macOS.gitignore`, `community/JavaScript/Vue.gitignore`).
- The parenthesized value is the first 12 characters of the commit from `git -C <tmp> rev-parse HEAD`. Anyone can open `https://github.com/murnana/gitignore/blob/<commit>/<path>` to see the source.
- Copy the template text unchanged: no reformatting, no dropped comments, no merged duplicates. Changing it would make the next refresh show a diff the user never made.
- Make sure the file ends with a newline before a BEGIN line and after an END line, with one blank line between blocks.

## Where blocks go

Git applies the last matching pattern, so order decides which rule wins.

- New file: blocks in the order chosen, then nothing else.
- Existing file without blocks: insert blocks at the top, after any leading comment header, so the user's existing lines stay below and keep overriding the templates.
- Existing file with blocks: insert new blocks right after the last END line. Leave everything else where it is.

## Refreshing (`update`)

- Replace only the text between BEGIN and END, and the commit in the BEGIN line.
- If the template text is identical, keep the old commit and say "unchanged".
- If a template no longer exists in the tree (renamed or moved), say so and ask what to do. Do not delete the block on your own.

## Removing (`remove <name>`)

- Delete the BEGIN line, the END line and everything between them, plus one adjacent blank line.

## Lines outside blocks

- Never move, rewrite or delete them without approval.
- When a block adds a pattern that already appears outside blocks, list it in the plan as a duplicate. Removing the outside copy is the user's call.
- When the user has a negation (`!pattern`) above where a block would go, the block would override it. Point this out and propose placing the block above the negation.
- A file with hand-copied template content but no markers (for example, a file GitHub created at repo creation, which starts with the template's own header comment): offer to wrap that content in markers instead of adding a second copy. Do it only if the content matches the current template closely; otherwise ask.
