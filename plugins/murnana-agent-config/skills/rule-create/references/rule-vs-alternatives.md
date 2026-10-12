# Is a rule the right tool?

Decide this **before** drafting. A rule is advisory context that loads every session (unconditional) or when matching files are touched (path-scoped). If the request fits another mechanism better, propose that instead and let the user decide.

| The instruction is… | Use | Why not a rule |
|---|---|---|
| A convention or constraint that applies to part of the codebase (some directories / file types) | **Path-scoped rule** | — (this is the sweet spot) |
| A cross-cutting concern touching many but not all corners of the repo (tests, migrations, handlers) | **Path-scoped rule** over a nested `CLAUDE.md` | A nested CLAUDE.md only covers one subtree |
| Broadly applicable to every session, short | Unconditional rule **or** `CLAUDE.md` | An unconditional rule is mechanically identical to CLAUDE.md content; split it into a rule only to keep CLAUDE.md under ~200 lines or to group by topic |
| A multi-step procedure / workflow ("how to release", "how to add an endpoint") | **Skill** | Procedures only matter sometimes; rules cost context every time they load |
| Domain knowledge needed only for some tasks, not tied to file paths | **Skill** | Skills load on demand by relevance |
| "Every time X happens, always do Y" (format after edit, lint before commit) | **Hook** | The model choosing to run a formatter is not the same as the formatter running automatically |
| "Never do X" that must actually be prevented (writing to `migrations/`, running `rm -rf`) | **Permission deny rule** or **PreToolUse hook** | A real guardrail must be deterministic; a rule can be ignored. A rule may still explain *why*, alongside the guardrail |
| Personal preference across all your projects | **User rule** (`~/.claude/rules/`) | Not a team convention; don't commit it |
| Personal preference for one project only | `CLAUDE.local.md` (gitignored) | Rules under `.claude/rules/` are normally committed |
| Something Claude already does by default, or can read from the code | **Nothing** | Adds noise and dilutes the rules that matter |
| Information that changes frequently (versions, current sprint, owners) | **Nothing** / link to a source of truth | Goes stale and causes wrong behavior |

## Unconditional vs. path-scoped

Default to **path-scoped**. Leave `paths` off only when the rule is genuinely relevant to almost every session in the project, for example:

- non-negotiable data-handling / compliance constraints
- repository etiquette (branch, commit, PR conventions)
- baseline language conventions in a single-language repo

Everything else — framework patterns, test conventions, migration rules, module-specific architecture — should carry `paths` so it stays out of unrelated sessions.
