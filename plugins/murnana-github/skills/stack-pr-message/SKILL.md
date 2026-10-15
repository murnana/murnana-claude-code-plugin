---
name: stack-pr-message
description: Write titles and bodies for every PR in a GitHub stack and apply them with gh pr edit
argument-hint: "[optional intent hint for the whole stack]"
disable-model-invocation: true
allowed-tools: Bash(git log *) Bash(git diff *) Bash(gh auth status *) Bash(gh repo view *) Bash(gh stack view *) Bash(gh pr view *) Bash(gh pr diff *) Bash(gh pr edit *) Read Grep Glob AskUserQuestion
---

# Stack PR Message

Write a title and body for each open PR in the current stack — each describing its own layer and where it sits in the stack — and apply them with `gh pr edit`.

## Current state

```bash
gh auth status 2>&1 || true
gh stack view --json 2>&1 || true
```

Treat `$ARGUMENTS` (if any) as a hint about the overall goal of the stack — it doesn't override the steps below.

## Output discipline

- Bound every query: `gh pr view <n> --json <fields>`, `gh pr diff <n> --name-only` first, the full diff only when the file list doesn't explain the layer.
- Never re-run a command whose output is already in this context.

Copy this checklist into your response and tick it off:

```
- [ ] 1 Read the stack
- [ ] 2 Read each layer
- [ ] 3 Project rules and template
- [ ] 4 Draft all layers
- [ ] 5 Approval
- [ ] 6 Apply
```

## Step 1: Read the stack

- `gh stack view --json` failed (exit 2) → the current branch isn't in a stack. Stop and say so.
- From `branches[]` (bottom to top), take the layers that have `pr.number` and `pr.state == "OPEN"`. Skip merged and queued PRs; they are not edited.
- Branches without a PR → tell the user to run `/murnana-github:stack-create` (or `gh stack submit --auto`) first; draft messages only for layers that have PRs.
- `gh auth status` failed → stop and ask, per `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/gh-fallback-mcp.md`.

## Step 2: Read each layer

For each open PR:

```bash
gh pr view <n> --json number,title,body,baseRefName,headRefName,isDraft,assignees,commits
gh pr diff <n> --name-only
```

`gh pr diff` shows only that layer's diff (base = the branch below), which is exactly what the message must describe. Read the commit subjects too; they often state the layer's intent.

## Step 3: Project rules and template

Apply the same discovery as pr-create, reading the shared references:

1. `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/project-rules.md` — project conventions are authoritative.
2. `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/pr-template-discovery.md` — if a template exists, use it for every layer.
3. Neither → `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/pr-message.md` (emoji title + なぜ / 影響範囲 / デバッグ方法).

In every case, add the stack section from [references/stack-message.md](references/stack-message.md) — unless the project's own rules forbid extra sections.

## Step 4: Draft all layers, bottom to top

Follow [references/stack-message.md](references/stack-message.md). Draft the bottom layer first: upper layers reference what lower ones provide.

- Each body describes **its own layer's diff**, framed by the stack's overall goal. Don't describe what other layers do beyond one line of context.
- If an existing body contains human-written content (not the `submit --auto` placeholder), keep it and merge your sections around it; never silently drop it.
- End every body with the attribution line: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

## Step 5: Present and get approval

Show, for every layer bottom to top: PR number, branch, new title, and the full new body exactly as it will be submitted. **Wait for approval.** Apply only the layers the user approves.

## Step 6: Apply

For each approved layer:

```bash
gh pr edit <n> --title "<title>" --body-file - <<'EOF'
<body>
EOF
```

- Use `--body-file -` with a quoted heredoc — never a multi-line `--body` argument, which mangles Japanese text and line breaks.
- If `assignees` was empty and the user didn't say otherwise, add `--add-assignee @me` in the same call.
- Don't change draft/ready state; that's the user's call (`gh pr ready` / `gh stack submit --open`).
- Report each PR URL (from the Step 1 JSON) when done. No re-fetch needed.

## Gotchas

- Don't put the position (`2/3`, `Part 2`) in the **title**: layers get inserted, folded and merged, and titles go stale. Keep the position in the body's stack section only.
- Don't hand-write a full list of links to every PR in the stack: GitHub already shows a stack map on each PR page. Link only the adjacent layers.
- The stack section is regenerated each run. If a layer was added or merged since the last run, re-run this skill so positions and neighbor links stay correct.
- `gh pr merge` can't merge a stack and is out of scope here anyway.

## References

- Stack section spec, title rules, examples:
  [references/stack-message.md](references/stack-message.md)
- Shared with pr-create (project rules, template discovery, fallback format, `gh` fallback):
  `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/`
