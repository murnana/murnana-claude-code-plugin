# Skill format reference

Authoritative spec for Claude Code skills, condensed from the official docs (`code.claude.com/docs/en/skills.md`) and the platform authoring guide. When this file and the live docs disagree, the docs win.

## Contents

- Locations and precedence
- Directory layout
- Frontmatter fields
- Portability subset
- Invocation control
- Arguments and variables
- Dynamic context injection
- Forked execution
- Lifecycle and listing budget
- Troubleshooting

## Locations and precedence

| Scope | Path | Loads in |
|---|---|---|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects (not cloud sessions) |
| Project | `.claude/skills/<name>/SKILL.md` | That repo (start dir and every parent up to the repo root) |
| Nested | `<subdir>/.claude/skills/<name>/SKILL.md` | On first file access in that subdirectory |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where the plugin is enabled, invoked as `/plugin-name:skill-name` |

- Conflicts: enterprise > personal > project. A skill beats a `.claude/commands/` file of the same name. Plugin skills are namespaced and never conflict.
- `.claude/commands/<name>.md` is the legacy format: it still works but doesn't support `name` or `paths`. Create skills, not commands.
- Reserved: `synced` and `anthropic-skills*` names don't load locally.
- Personal and project skill edits are picked up live. A brand-new top-level skills dir needs `/reload-skills`. Plugin changes need `/reload-plugins`.

## Directory layout

```text
my-skill/
├── SKILL.md          # required: frontmatter + instructions (keep < 500 lines)
├── references/       # docs Claude reads when SKILL.md tells it to
├── scripts/          # code Claude executes (output costs tokens, source doesn't)
├── assets/           # templates, fixtures used in output
└── evals/            # test cases (not loaded by Claude Code)
```

Link every supporting file from SKILL.md, one level deep, and say when to read it. Claude may only partially read (`head`) files reached through nested links.

## Frontmatter fields

Frontmatter must start on line 1. Every field is optional, and `description` is strongly recommended. Field names must match exactly, because unknown fields are silently ignored. Invalid YAML loads the skill with **no** metadata: `/name` still works, but auto-triggering doesn't.

| Field | Meaning / constraints |
|---|---|
| `name` | Command name; defaults to the directory name. Lowercase letters, digits, hyphens; ≤ 64 chars; no `claude` / `anthropic`. Keep it equal to the directory name |
| `description` | What it does + when to use it. Defaults to the first body line. `description` + `when_to_use` are truncated at 1,536 chars in the listing. Spec / API limit is 1,024 chars, no XML tags |
| `when_to_use` | Extra trigger phrases, appended to `description` (shares the 1,536 cap). Not portable |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` |
| `arguments` | Named positional args for `$name` substitution (space-separated string or YAML list) |
| `disable-model-invocation` | `true` = only the user can invoke; description is not in Claude's context; can't be preloaded into subagents |
| `user-invocable` | `false` = hidden from `/` menu; Claude can still load it (background knowledge) |
| `allowed-tools` | Tools pre-approved while the skill is active in the invoking turn. Grants only, doesn't restrict. Space/comma-separated or YAML list. Supports `Bash(cmd *)`, `${CLAUDE_SKILL_DIR}` |
| `disallowed-tools` | Tools removed while the skill is active (until next user message) |
| `model` | Model override for the turn (`inherit` keeps current); with `context: fork`, the subagent's model |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max` |
| `context` | `fork` = run in a forked subagent with no conversation history |
| `agent` | Subagent type with `context: fork`: `Explore`, `Plan`, `general-purpose` (default), or a custom agent |
| `background` | With `context: fork`: `false` waits for the result (default `true`) |
| `hooks` | Hooks registered when the skill is invoked, kept for the session |
| `paths` | Globs limiting *auto* loading to sessions touching matching files (same format as rules) |
| `shell` | `bash` (default) or `powershell` for injected commands |
| `metadata` | Free-form map for your tooling; ignored by Claude Code |
| `license`, `compatibility` | Agent Skills spec fields; accepted, not acted on |

## Portability subset

claude.ai uploads, the Skills API and `package_skill.py` accept **only** `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Any other key is a hard upload error. If the user may share the skill outside Claude Code, stick to that subset and ≤ 1,024-char descriptions.

## Invocation control

| Setting | User can `/invoke` | Claude can auto-load | Description in context |
|---|---|---|---|
| (default) | Yes | Yes | Always |
| `disable-model-invocation: true` | Yes | No | No |
| `user-invocable: false` | No | Yes | Always |

Use `disable-model-invocation: true` for anything with side effects or that the user wants to time themselves: deploy, commit, push, send, create resources.

## Arguments and variables

| Placeholder | Expands to |
|---|---|
| `$ARGUMENTS` | Full argument string. If no placeholder is used, Claude Code appends `ARGUMENTS: <value>` |
| `$ARGUMENTS[N]` / `$N` | 0-based positional arg (shell-style quoting). Unmatched stays literal |
| `$name` | Named arg from `arguments`; missing → empty string |
| `${CLAUDE_SKILL_DIR}` | Directory containing SKILL.md, used to reference bundled scripts |
| `${CLAUDE_PROJECT_DIR}` | Project root |
| `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` | Plugin install dir / persistent data dir (plugin skills only) |
| `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}` | Session ID, effort level |

Escape a literal `$` as `\$`. Values are inserted literally and not re-expanded.

## Dynamic context injection

- `` !`command` `` (at line start or after whitespace) and fenced ` ```! ` blocks run **before** Claude sees the skill. Their output replaces them.
- **Any non-zero exit aborts the whole invocation** (except exit 1 from search/compare commands), so Claude never sees the skill. Append `|| true` to anything that can legitimately fail, e.g. listing a directory that may not exist.
- Commands are checked against permission rules without prompting. Anything not allowed aborts unless it's pre-approved in `allowed-tools`. **Every part of a compound command** must be allowed: `git rev-parse --show-toplevel || pwd` with only `Bash(git rev-parse *)` allowed fails with `This command requires approval` (verified on v2.1.296 in `-p` mode). Keep injected commands to single allowed commands, or use a plain ` ```bash ` block that Claude runs itself.
- They run in the session's cwd, with a 2-minute timeout. `disableSkillShellExecution` policy replaces them with a placeholder.
- The inline pattern is matched **anywhere in SKILL.md, including prose and inline code**. A checklist line that merely mentions it (a space, then a bang and a backtick) runs as a command and can abort the skill (verified on v2.1.296). When documenting the syntax inside SKILL.md, describe it in words. Reference files aren't rendered, so they're safe.
- A plain ` ```bash ` block is *not* injected. It's just text Claude may choose to run.

## Forked execution

- `context: fork` runs the body as a subagent prompt with **no conversation history**. Use it only for self-contained tasks that return a result. Guideline-only content produces nothing.
- It runs in the background by default with a narrower tool set. Set `background: false` when the user needs the result in the same turn, or when the skill needs more tools.
- Edits made by forked skills are not covered by `/rewind`.

## Lifecycle and listing budget

- When invoked, the rendered SKILL.md is added to the conversation **once** and is not re-read. Write standing instructions ("run tests after every edit"), not one-shot ones.
- After compaction, the most recent invocation of each skill is re-attached, up to 5,000 tokens each (25,000 total). Put the critical instructions at the top.
- Descriptions of all auto-invocable skills are always in context. The listing budget is about 1% of the context window, and when it overflows, the least-used skills lose their descriptions first. Shorter, front-loaded descriptions survive.

## Troubleshooting

| Symptom | Check |
|---|---|
| Never triggers | Description lacks the user's words; YAML broken (`claude --debug`); `disable-model-invocation: true`; task too simple to need a skill |
| Triggers too often | Description too broad: add what it does *not* cover, or make it explicit-only |
| Stops being followed mid-session | Rule must hold every time → move it to a hook (skill `hooks` frontmatter); compacted → re-invoke |
| `Shell command failed for pattern …` | An injected command exited non-zero or wasn't allowed: fix it, add `|| true`, or add to `allowed-tools` |
| Frontmatter parse errors | `claude plugin validate <skills-dir>` (also works on `.claude/skills`, `~/.claude/skills`) |
