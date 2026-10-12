# Rule file format reference

Authoritative spec for `.claude/rules/` files, condensed from the official Claude Code docs (`memory.md` → "Organize rules with `.claude/rules/`", and `claude-directory.md`). When this file and the live docs disagree, the docs win.

## Locations

| Scope | Path | Applies to | Shared via git |
|---|---|---|---|
| Project | `<project>/.claude/rules/**/*.md` | That project | Yes (commit it) |
| User | `~/.claude/rules/**/*.md` | Every project on this machine | No |

- All `.md` files are discovered **recursively**: `.claude/rules/frontend/react.md` works.
- One topic per file. Use a descriptive kebab-case filename (`testing.md`, `api-design.md`, not `rules1.md`).
- Group related files in subdirectories (`frontend/`, `backend/`) once there are several.

## Loading behavior

| Rule kind | When it loads | After `/compact` |
|---|---|---|
| No `paths` (unconditional) | At session start, same priority as `.claude/CLAUDE.md` | Re-injected |
| With `paths` (path-scoped) | When Claude uses Read / Write / Edit on a matching file, or reads one with a single-file Bash read such as `cat` / `head` | Loads again on the next matching access |

- Order: user rules load **before** project rules, so project rules appear later in context. Neither overrides the other — if they conflict, Claude may follow either. Keep them consistent.
- Rules are **context, not enforcement**. Claude reads and tries to follow them; nothing guarantees compliance. For guaranteed behavior use hooks or permissions (see [rule-vs-alternatives.md](rule-vs-alternatives.md)).
- Project rules are skipped when `project` is excluded from `--setting-sources`.
- With **Project instructions** = `managed-only`, unconditional `.claude/rules/` files are left out; path-scoped rules still load on demand.

## Frontmatter

YAML between `---` markers at the very top of the file. `paths` is the **only** field Claude Code reads. Any other field is silently ignored. The frontmatter is stripped before the rule is injected into context.

| Field | Required | Value |
|---|---|---|
| `paths` | No | Glob patterns. A YAML list **or** a comma-separated string |

Preferred form (YAML list, each pattern quoted):

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "**/*.handler.ts"
---

# API Rules

- ...
```

Also valid: `paths: "src/**/*.ts, lib/**/*.ts"`.

- If the YAML fails to parse, the **whole frontmatter is ignored** and the rule loads as if it had no `paths` — i.e. it silently becomes unconditional. Run `claude --debug` to see the parse error.
- Do **not** use Cursor-style fields (`globs:`, `alwaysApply:`, `description:`). Claude Code ignores them, so a rule relying on them is effectively unconditional or mis-scoped.
- Always quote patterns: a pattern starting with `*` or containing `{` / `[` is otherwise interpreted by YAML (alias, flow mapping, flow sequence).

## Glob patterns

Patterns are relative to the project root.

| Pattern | Matches |
|---|---|
| `**/*.ts` | All `.ts` files in any directory |
| `src/**/*` | Everything under `src/` |
| `*.md` | Markdown files in the project root only |
| `src/components/*.tsx` | Direct children of `src/components/` only |
| `src/**/*.{ts,tsx}` | Brace expansion: `.ts` and `.tsx` under `src/` |

- **Brace expansion budget**: each brace group multiplies the pattern count. A rule's whole `paths` list shares a budget of 1,000 expanded patterns / 4 MiB. Patterns that would exceed it are used unexpanded, and their literal braces match nothing.
- `[` starts a bracket expression (`[abc]`). An unparseable one (e.g. `photos [2024/**`) makes that pattern match nothing; the rule's other patterns keep working. Escape a literal bracket as `\[`.
- A pattern that matches no existing file is not an error — the rule simply never loads. Verify patterns against real files.

## Symlinks

- `.claude/rules/` supports symlinked files and directories; circular links are handled.
- A link whose target is **outside the working directory** is treated as an external import: it needs a one-time per-project approval, and even then only rules **without** `paths` load from it. For cross-project sharing without approval, use `~/.claude/rules/` instead.
- Links to network paths (UNC `\\server\share`, `/net`, `/Network`) are not followed.

## Body

- Plain Markdown. Group under headers, use bullets. No required structure.
- `@path` imports are a CLAUDE.md feature; they help organize but never reduce context cost (imports load at launch). Don't rely on them inside rules.

## Size

- Target **under 200 lines** per file. Longer files consume more context and reduce adherence.
- Startup and `/status` warn when one instruction file exceeds the recommended length, or when many files add up past a combined limit. Each CLAUDE.md, rule file and import counts separately.
- Files over 4 MiB are skipped.

## Verifying a rule loads

- `/context` → **Memory files** lists what is loaded now. `/memory` lists and opens instruction files.
- For path-scoped rules: start a new session, have Claude Read a matching file, then check `/context` again.
- `InstructionsLoaded` hook: logs which CLAUDE.md / rule files load, when, and why (`load_reason` is `session_start` for unconditional files, `path_glob_match` for path-scoped rules).
- `/doctor prompt-audit [path]`: Claude reports outdated, broken or contradictory instructions across CLAUDE.md, rules, skills, etc.

## Historical note

GitHub issue anthropics/claude-code#17204 (2026-01) reported that quoted / YAML-list `paths` failed to load while Cursor-style `globs:` did. The current docs explicitly accept a YAML list or comma-separated string, and later releases fixed related `paths` parsing bugs (v2.1.207, v2.1.217). Verified on v2.1.296: a quoted YAML-list `paths` rule loads only when a matching file is read (`InstructionsLoaded` reports `load_reason: path_glob_match`) and stays out of context otherwise. Follow the documented format, but always verify loading after creating a rule.
