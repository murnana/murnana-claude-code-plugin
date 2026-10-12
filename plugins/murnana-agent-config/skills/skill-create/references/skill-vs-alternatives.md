# Is a skill the right tool?

Decide this **before** drafting. A skill is on-demand instructions: its description costs context every session (unless it's explicit-only), and its body loads only when invoked. If the request fits another mechanism better, propose that instead and let the user decide.

| The need is… | Use | Why not a skill |
|---|---|---|
| A repeatable multi-step workflow ("release", "fix an issue", "write a migration") | **Skill** | (the sweet spot) |
| Domain knowledge needed only for some tasks (an internal API, a file format, a schema) | **Skill** (auto-invocable, maybe `user-invocable: false`) | (the sweet spot) |
| A workflow with side effects the user wants to trigger themselves | **Skill** with `disable-model-invocation: true` | (the sweet spot) |
| A short fact or convention relevant to almost every session | **CLAUDE.md** | A skill may not load when needed; CLAUDE.md always does |
| A convention tied to certain files/directories | **Path-scoped rule** (`.claude/rules/`) | Rules load automatically on matching files; no trigger guesswork |
| "Every time X happens, do Y" with zero exceptions (format on edit, lint before commit) | **Hook** | A skill is advisory; Claude may skip it. A hook always runs |
| "Never do X" that must actually be prevented | **Permission deny rule** or **PreToolUse hook** | Instructions can be ignored; guardrails must be deterministic |
| Heavy research or review whose intermediate output shouldn't fill the main context | **Subagent** (`.claude/agents/`), or a skill with `context: fork` | A normal skill runs in the main context |
| Access to an external system Claude has no tool for | **MCP server** (a skill can then teach *how* to use it) | A skill can't create new tool capabilities, only instructions and scripts |
| Something Claude already does well without help | **Nothing** | Adds listing cost and noise. Confirm by trying the task without a skill |
| Information that changes frequently | **Nothing** / link to the source of truth | Goes stale and causes wrong behavior |

## Combinations that work

- **Skill + hook**: the skill teaches the workflow, and a hook in the skill's `hooks` frontmatter enforces the one step that must never be skipped.
- **Skill + script**: deterministic or fragile parts become `scripts/` that the skill runs; judgment stays in prose.
- **Skill + MCP**: MCP provides the tool; the skill provides the conventions, with tool names fully qualified as `server:tool`.

## Scope: one coherent unit

Scope a skill like a function: one coherent unit of work.

- **Too narrow**: several skills must load for one task, and they may conflict.
- **Too broad**: the description can't say precisely when to trigger.

Example: "query the DB and format results" is one skill. Adding "DB administration" to it makes it two.
