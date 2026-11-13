# Subagent format reference

Spec for Claude Code subagent files, condensed from the official docs (`code.claude.com/docs/en/sub-agents.md`). When this file and the live docs disagree, the docs win.

## Contents

- Locations and precedence
- File format
- Frontmatter fields
- Plugin subagents
- Tools
- Model
- What a subagent receives
- Invocation
- Reloading
- Troubleshooting

## Locations and precedence

| Scope | Path | Loads in | Priority on a name clash |
|---|---|---|---|
| Project | `<project>/.claude/agents/**/*.md` | That project | Higher |
| Personal | `~/.claude/agents/**/*.md` | All your projects | Middle |
| Plugin | `<plugin>/agents/**/*.md` | Where the plugin is enabled | Lowest |

- Managed settings and the `--agents` CLI flag rank above all three.
- Directories are scanned recursively. In project and personal locations a subfolder is only for organizing: identity comes from `name`.
- In a plugin, a subfolder becomes part of the identifier: `agents/review/security.md` in plugin `my-plugin` is `my-plugin:review:security`.
- Two files with the same `name` in one tree: only one loads, and which one is not defined. Keep names unique.

## File format

Markdown with YAML frontmatter that starts on line 1. The body is the subagent's system prompt.

```markdown
---
name: code-reviewer
description: Reviews changed code for bugs and unclear naming. Use after code is written or modified.
tools: Read, Grep, Glob
model: inherit
---

You review code. You only read and report. Never edit files.
```

## Frontmatter fields

Only `name` and `description` are required. Multi-word fields are camelCase. An unknown or misspelled field is ignored without an error.

| Field | Meaning | Notes |
|---|---|---|
| `name` | Identifier | Lowercase letters, digits, hyphens. No `:`, no leading `-`. Keep it equal to the filename |
| `description` | When Claude should delegate to it | Always in context. Keep it short; "use proactively" encourages delegation |
| `tools` | Tools it may use: comma-separated string or YAML list | **Omitted = every tool available to subagents** |
| `disallowedTools` | Tools removed from the inherited or listed set | Wins over `tools` |
| `model` | `sonnet`, `opus`, `haiku`, a full model ID, or `inherit` | See Model |
| `maxTurns` | Maximum agentic turns | On reaching it, the output is marked partial |
| `skills` | Skills whose full text is injected at startup | Not a restriction. Skills with `disable-model-invocation: true` can't be preloaded |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max` | Overrides the session level |
| `memory` | Persistent memory: `user`, `project` or `local` | Turns on Read, Write and Edit for the memory directory |
| `background` | `true` keeps it in the background | Subagents Claude spawns already start in the background |
| `isolation` | `worktree` runs it in a temporary git worktree | Cleaned up if it makes no changes |
| `omitClaudeMd` | `true` skips user and project CLAUDE.md | |
| `color` | Display color | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `permissionMode` | Permission mode for the subagent | **Ignored in plugins** |
| `hooks` | Hooks scoped to the subagent | **Ignored in plugins** |
| `mcpServers` | MCP servers for the subagent | **Ignored in plugins** |

Use `name`, `description`, `tools` and `model` by default. Add another field only when a requirement calls for it.

## Plugin subagents

- `hooks`, `mcpServers` and `permissionMode` are ignored for security. Ship hooks in the plugin's `hooks/hooks.json` and MCP servers in its `.mcp.json`.
- The scoped name is `<plugin-name>:<name>`.

## Tools

- Write `tools` every time. Without it the subagent gets everything, including `Edit`, `Write`, `Bash` and `Agent`.
- Removed from every subagent, even when listed: `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode`, `ScheduleWakeup`, `Workflow`. A subagent cannot ask the user a question.
- Subagents can spawn subagents (up to three levels deep) only if `Agent` is in `tools`. Leave it out to prevent that.
- A background subagent keeps only: `Read`, `Grep`, `Glob`, `LSP`, `Bash`, `PowerShell`, `Edit`, `Write`, `NotebookEdit`, `WebFetch`, `WebSearch`, `TodoWrite`, `Skill`, `ToolSearch`, `Monitor`, `SendMessage` and a few session tools, plus every MCP tool. Don't design a subagent around any other built-in tool.
- MCP tools are listed by their full name.
- `tools` is a grant, not a sandbox for what a granted tool does. `Bash` can still change files. If a subagent needs `Bash` but must not write, say so in the body, and in a project or personal location add a `PreToolUse` hook as a backstop.

## Model

Resolved in this order: the per-call `model` argument, the frontmatter `model` (`inherit` = the main conversation's model), the `CLAUDE_CODE_SUBAGENT_MODEL` variable, then the main conversation's model.

| Work | `model` |
|---|---|
| Judgment, review, rating, anything where a wrong answer is costly | `inherit` |
| Running commands and reporting, mechanical search | `sonnet` |
| Simple lookups over many files | `haiku` |

## What a subagent receives

| It gets | It does not get |
|---|---|
| Its own body as the system prompt | The Claude Code system prompt |
| The delegation message Claude writes | The conversation history |
| CLAUDE.md files (unless `omitClaudeMd`) | Files Claude already read |
| A git status snapshot and the working directory | Skills already invoked |
| Skills listed in `skills` | The user's output style and auto memory |

Only its final message returns to the main conversation. Its tool calls and intermediate text stay out.

## Invocation

- Automatic: Claude matches the request against each `description`.
- By name in the prompt: `@agent-<name>`, or `@agent-<plugin-name>:<name>` for a plugin subagent. Typing `@` also lists them.
- Natural language: "Use the code-reviewer subagent to check the auth changes".
- Whole session: `claude --agent <name>`.

## Reloading

- Edits under an existing `.claude/agents/` or `~/.claude/agents/` are picked up within a few seconds.
- A restart is needed for the first file in a newly created `agents` directory, and for directories added with `--add-dir`.
- Plugin subagents need `/reload-plugins`.

## Troubleshooting

| Symptom | Check |
|---|---|
| Not listed under `@` | Frontmatter doesn't start on line 1 or doesn't parse; missing `name`; new directory needs a restart |
| Never delegated to | `description` lacks the words of the request, or another subagent's description is closer |
| Delegated to too often | `description` too broad: add "Not for X" |
| A field has no effect | Misspelled or wrong case (`claude --debug` logs unknown fields); plugin-ignored field |
| Edits files it shouldn't | `tools` omitted, or `Bash` granted |
| Stops to ask a question | The body tells it to ask; give it a default assumption instead |
| Frontmatter parse errors | `claude plugin validate <agents-directory or plugin-root>` |
