---
name: pr-create
description: Create pull request
argument-hint: "[optional scope or intent hint]"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git branch *) Bash(git rev-parse *) Bash(git push *) Bash(git config *) Bash(gh auth status *) Bash(gh --version *) Bash(gh repo view *) Bash(gh pr view *) Bash(gh pr list *) Bash(gh pr create *) Read Grep Glob AskUserQuestion
---

# PR Create

Create a pull request for the current branch, following the target project's own conventions when they exist, or a sensible generated format otherwise.

## Current state

```bash
gh auth status 2>&1 || true
git status --short --branch
git branch --show-current 2>/dev/null || true
git log --format='%s' --no-merges @{u}..HEAD 2>/dev/null || true
git log --format='%s' --no-merges -15 2>/dev/null || true
git remote get-url origin 2>/dev/null || true
```

Treat `$ARGUMENTS` (if any) as an additional hint about the PR's intent — it does not override the steps below.

## Output discipline

- Bound every `gh`/`git log` query; never fetch unbounded history or full PR lists.
- Prefer `gh pr view --json <fields>` over the default human-readable form when only specific fields are needed.
- Never re-run a command whose output is already in this context.

## Step 1: Confirm `gh` is usable

- If `gh auth status` above failed or `gh` is missing, **stop and ask the user** (`AskUserQuestion`) whether to fall back to the GitHub MCP server. 
  Do not install the `gh` CLI or configure an MCP server without explicit confirmation — both are environment-level changes.
- See [references/gh-fallback-mcp.md](references/gh-fallback-mcp.md) for the fallback procedure once the user agrees.

## Step 2: Discover project rules for PRs (highest priority)

Check the sources in [references/project-rules.md](references/project-rules.md), in order. If found, it is the **only** rule that applies for tone/format/required sections — do not blend with the generated fallback in Step 5.

Glob for a candidate file before reading it.

## Step 3: Run pre-PR checks

- If the project defines lint/test/build steps (package manager scripts, a `Makefile`, `.github/workflows/`, or any other project-specific tooling — the project may not be Node.js at all, it could be Unity, Unreal Engine, Python, etc.), run the ones relevant to the changed branch. These commands are not pre-authorized in `allowed-tools`, so they run as ordinary Bash calls subject to the normal permission prompt — never widen `allowed-tools` to guess a runner in advance.
- If a check fails, **stop entirely** — do not push, do not create the PR. Report the failure output as-is and ask how to proceed.
- If no check is discoverable, say so and proceed.

## Step 4: Push local commits

- Compare local branch to its upstream (`@{u}..HEAD` above). If there are unpushed commits, run `git push` (set upstream with `-u` only if no upstream is configured).
- If the push fails for any reason (rejected, no remote, auth), **stop entirely** — do not attempt PR creation. Report the failure and ask how to proceed.
- Never force-push.

## Step 5: Find or generate the PR template

- Search the locations in [references/pr-template-discovery.md](references/pr-template-discovery.md), in order.
- If exactly one template is found, use it.
- If multiple are found (e.g. multiple files under `.github/PULL_REQUEST_TEMPLATE/`), either pick the one whose name most closely matches the change (e.g. `bug_fix.md` for a fix) or, if ambiguous, ask the user via `AskUserQuestion`.
- If none is found, generate title and body per [references/pr-message.md](references/pr-message.md) — title prefixed with a GitHub emoji code, body with 理由 (why) / 影響範囲 (scope & impact) / デバッグ方法 (how to verify) sections.
- Always append the required attribution line to the body: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

## Step 6: Present the plan and get approval

- Show the target branch, base branch, title, and full body exactly as it will be submitted.
- **Wait for approval** before running `gh pr create` — never create the PR silently, even when a template made the content mostly mechanical.

## Step 7: Create the PR

- Run `gh pr create --title <title> --body-file -` (heredoc/stdin) to avoid mangling Japanese text or line breaks — never pass a multi-line body as a `--body` shell arg.
- Use `--draft` only if the user asked for a draft; do not ask by default.
- If no assignee is specified (neither by the template nor by the user), add `--assignee @me` so the skill's operator is assigned automatically.
- After creation, report the PR URL from `gh pr create`'s output; do not re-fetch it with a separate `gh pr view` call.

## References

- Where to look for project-specific PR rules:
  [references/project-rules.md](references/project-rules.md)
- Template discovery order (GitHub's own convention):
  [references/pr-template-discovery.md](references/pr-template-discovery.md)
- Fallback title/body format and emoji table:
  [references/pr-message.md](references/pr-message.md)
- `gh` unavailable → MCP fallback procedure:
  [references/gh-fallback-mcp.md](references/gh-fallback-mcp.md)
