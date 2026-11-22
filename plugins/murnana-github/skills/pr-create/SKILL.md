---
name: pr-create
description: Push the current branch and create a pull request (or stacked PRs) after approval.
argument-hint: "[optional scope or intent hint]"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git branch --show-current) Bash(git rev-parse *) Bash(git push) Bash(git push -u origin *) Bash(git config --get *) Bash(git remote -v) Bash(git remote get-url *) Bash(gh auth status *) Bash(gh --version *) Bash(gh repo view *) Bash(gh pr view *) Bash(gh pr list *) Bash(gh pr create *) Bash(gh pr edit *) Bash(gh pr ready *) Bash(gh stack view *) Bash(gh stack submit *) Bash(gh stack up *) Bash(gh stack up) Bash(gh stack down *) Bash(gh stack down) Bash(gh stack top) Bash(gh stack bottom) Read Grep Glob AskUserQuestion
---

# PR Create

Create a pull request for the current branch, following the target project's own conventions when they exist, or a sensible generated format otherwise.

## Current state

Run these first, each line as its own Bash call, exactly as written. Send the first five together in one message, then run the last one on its own (it exits non-zero outside a stack, which is expected):

```bash
gh auth status 2>&1 || true
git status --short --branch
git log --format='%s' --no-merges '@{u}..HEAD' 2>/dev/null || true
git log --format='%s' --no-merges -15 2>/dev/null || true
git remote get-url origin 2>/dev/null || true
gh stack view --short
```

They give, in order: whether `gh` is logged in, the branch with its upstream (`## <branch>...<remote>/<branch> [ahead N]`; no `...` part means no upstream) and uncommitted files, the unpushed commit subjects (empty when there are none or no upstream), recent subjects for inferring a title format, the remote URL, and the stack tree or an error.

Treat `$ARGUMENTS` (if any) as an additional hint about the PR's intent — it does not override the steps below.

## Output discipline

- Bound every `gh`/`git log` query; never fetch unbounded history or full PR lists.
- Prefer `gh pr view --json <fields>` over the default human-readable form when only specific fields are needed.
- Never re-run a command whose output is already in this context.

## Asking the user

- Every question to the user goes through the `AskUserQuestion` tool, never as a plain-text question at the end of a reply. This includes every "wait for approval" and every "ask how to proceed": show the plan or the failure in the reply, then call `AskUserQuestion` with options such as 「この内容で進める」 and 「修正する」. The dialog can hide the reply, so say in the question itself, in one line, what is being approved.
- Ask as few times as possible. Don't ask what `$ARGUMENTS`, the conversation, the files or command output already answer. Where a step gives a default, use it and state it in the plan instead of asking.
- Collect the open questions and send them in one call (up to 4 questions per call). A question that can wait goes into the approval call, not a call of its own.
- If `AskUserQuestion` is unavailable (a non-interactive run), don't guess: stop before changing anything and list the questions in the reply.

## Step 1: Confirm `gh` is usable

- If `gh auth status` reported no login or a keyring/token error while `gh` is installed, the sandbox may be blocking the credentials stored on the user's computer. **Stop** and follow [references/sandbox-credentials.md](references/sandbox-credentials.md): guide the user to exclude the `gh` commands from the sandbox, and offer the MCP fallback in the same question.
- If `gh` is missing (`command not found`), **stop and ask the user** (`AskUserQuestion`) whether to fall back to the GitHub MCP server.
  Do not install the `gh` CLI or configure an MCP server without explicit confirmation — both are environment-level changes.
- See [references/gh-fallback-mcp.md](references/gh-fallback-mcp.md) for the fallback procedure once the user agrees.

### Stack detection

Read the result of `gh stack view --short` from Current state:

- Exit 0 and the tree has a `» <branch> (current)` line → the current branch is a layer of a GitHub stack. **Stack mode**: follow [references/stack-mode.md](references/stack-mode.md), which replaces `git push` and `gh pr create` with `gh stack submit` + `gh pr edit` in Steps 4–7. Never create a plain PR for a stacked branch.
- Exit 0 but no `(current)` line → the current branch is the stack's trunk; normal mode. `gh stack view` also succeeds on a trunk that has stacks on top of it.
- Any non-zero exit (2 = not in a stack; `unknown command` = `gh stack` isn't installed) → normal mode, the steps below as written. Don't install gh-stack for this, and don't retry the command.
- The MCP fallback can't create stacks. If `gh` is unusable and the branch is stacked, say so when asking in Step 1.

## Step 2: Discover project rules for PRs (highest priority)

Check the sources in [references/project-rules.md](references/project-rules.md), in order. If found, it is the **only** rule that applies for tone/format/required sections — do not blend with the generated fallback in Step 5.

Glob for a candidate file before reading it.

## Step 3: Run pre-PR checks

- If the project defines lint/test/build steps (package manager scripts, a `Makefile`, `.github/workflows/`, or any other project-specific tooling — the project may not be Node.js at all, it could be Unity, Unreal Engine, Python, etc.), run the ones relevant to the changed branch. These commands are not pre-authorized in `allowed-tools`, so they run as ordinary Bash calls subject to the normal permission prompt — never widen `allowed-tools` to guess a runner in advance.
- If a check fails, **stop entirely** — do not push, do not create the PR. Report the failure output as-is and ask how to proceed.
- If no check is discoverable, say so and proceed.

## Step 4: Push local commits

Stack mode: skip this step (`gh stack submit` pushes). See [references/stack-mode.md](references/stack-mode.md).

- Use the status line and the unpushed subjects from Current state. No upstream → `git push -u origin <branch>`. Upstream with unpushed commits → `git push`. Nothing unpushed → skip the push.
- If the push fails for any reason (rejected, no remote, auth), **stop entirely** — do not attempt PR creation. Report the failure and ask how to proceed.
- If the push fails on credentials (HTTPS credential helper, or the SSH key/agent such as 1Password, which the sandbox can block), follow [references/sandbox-credentials.md](references/sandbox-credentials.md): guide the user to exclude the command from the sandbox, then retry after they confirm.
- Never force-push. Only plain `git push` and `git push -u origin <branch>` are pre-approved; any other form asks for permission.

## Step 5: Find or generate the PR template

- Search the locations in [references/pr-template-discovery.md](references/pr-template-discovery.md), in order.
- If exactly one template is found, use it.
- If multiple are found (e.g. multiple files under `.github/PULL_REQUEST_TEMPLATE/`), either pick the one whose name most closely matches the change (e.g. `bug_fix.md` for a fix) or, if ambiguous, ask the user via `AskUserQuestion`.
- If none is found, generate title and body per [references/pr-message.md](references/pr-message.md) — title prefixed with a GitHub emoji code, body with なぜ (why) / 影響範囲 (scope & impact) / デバッグ方法 (how to verify) sections.

## Step 6: Present the plan and get approval

- Show the target branch, base branch, title, and full body exactly as it will be submitted.
- **Wait for approval** before running `gh pr create` — never create the PR silently, even when a template made the content mostly mechanical.

## Step 7: Create the PR

Stack mode: use `gh stack submit --auto` + `gh pr edit` per [references/stack-mode.md](references/stack-mode.md) instead of `gh pr create`.

- Write the approved body to a temporary file first, then pass that file to `gh`. This keeps Japanese text and line breaks intact and keeps the `gh` call a single plain command:
  1. Run `git rev-parse --absolute-git-dir` and use `<that dir>/PR_BODY.md` as the path. It lives inside `.git/`, so it is never committed, and it is overwritten on the next run.
  2. Write the body there with the `Write` tool, exactly as approved.
  3. Run `gh pr create --title "<title>" --body-file <that path>` as a Bash call of its own.
- Never pass a multi-line body as a `--body` argument, through `$(...)`, or on stdin with a heredoc.
- Use `--draft` only if the user asked for a draft; do not ask by default.
- If no assignee is specified (neither by the template nor by the user), add `--assignee @me` so the skill's operator is assigned automatically.
- If `gh pr create` fails on authentication, treat it as the sandbox case in [references/sandbox-credentials.md](references/sandbox-credentials.md).
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
- Current branch is in a `gh stack` stack → Steps 4–7 replacements:
  [references/stack-mode.md](references/stack-mode.md)
- `gh` login or push fails because the sandbox blocks the computer's credentials → how to guide the user:
  [references/sandbox-credentials.md](references/sandbox-credentials.md)
