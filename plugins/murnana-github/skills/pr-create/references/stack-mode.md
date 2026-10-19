# Stack mode

Applies when `gh stack view --short` in the dynamic context block exited 0 and the current branch is one of the stack's layers (Stacked PRs managed by the `gh stack` extension).

A stacked branch must not get a plain PR: `gh pr create` would target the wrong base (or the trunk) and leave the PR outside the stack on GitHub. Use `gh stack` commands instead, as below. Everything not mentioned here (Steps 2, 3, 5's template discovery, 6's approval) works as in SKILL.md.

## Non-interactive rules

`gh stack` opens a TUI or prompt when arguments are missing, which blocks this session.

- `gh stack submit --auto` — never bare `gh stack submit` (opens the PR editor TUI).
- `gh stack view --json` for parsing — `--short` is only the detection signal; never bare `gh stack view` (full-screen TUI).
- Never `gh stack switch` / `gh stack modify` (menu/TUI only).

## S1: Read the stack

```bash
gh stack view --json
```

- `currentBranch` equals `trunk` (it isn't in `branches[].name`) → not a layer; leave stack mode and follow SKILL.md's normal steps.
- From `branches[]` (bottom to top), the **targets** are the unmerged branches without `pr` — `submit` creates a PR for every one of them, not just the current branch.
- Each layer's **parent branch** is the previous entry in `branches[]`, or `trunk` for the bottom one. `branches[].base` is the parent's tip **commit SHA**, not a branch name — use it for diffs, never show it as the base branch.
- If the current branch already has an open PR and there are no targets, there's nothing to create. Report the existing PR URL and stop; suggest `/murnana-github:stack-pr-message` if the user wants to rewrite messages.
- Any branch with `needsRebase: true` → stop and suggest `/murnana-github:stack-rebase` first. Submitting a stale stack pushes layers whose diffs include their parent's old commits.
- More than one remote in `git remote` and `git config remote.pushDefault` empty → pass `--remote <name>` to `submit` (ask which remote if unclear).

## S2: Pre-PR checks (Step 3)

Run them on the current branch as usual. If a target lies **below** the current branch, it will get a PR too: say so, and run the checks there as well when it could plausibly break on its own (`gh stack down` / `bottom` to check it out; come back with `gh stack up` / `top`). A broken lower layer blocks every layer above it from merging.

## S3: Push (Step 4) — skip

Don't run `git push`. `gh stack submit` pushes every branch in the stack with the right lease and base wiring; pushing yourself can desync gh-stack's metadata.

## S4: Messages (Step 5)

Draft a title and body for **each target**, bottom to top, following `${CLAUDE_PLUGIN_ROOT}/skills/stack-pr-message/references/stack-message.md`:

- Template / project rules / fallback format are discovered exactly as in Step 5 and apply to every layer.
- Each body describes only its own layer's diff (`git diff --stat <base>..<branch>`, then the full diff only if needed; `<base>` is the SHA from the JSON), plus the stack section from `stack-message.md` unless project rules forbid extra sections.
- The stack section links neighbor PRs as `#n`, but new PRs have no number until S6. Write `#<branch-name>` as a placeholder for each not-yet-created neighbor; S6 replaces them with real numbers.
- No position (`2/3`) in titles.
- End every body with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

## S5: Approval (Step 6)

Show the trunk, then for every target bottom to top: branch, parent branch, title, full body. Also list which branches `submit` will push, and note that `#<branch-name>` placeholders will be replaced with PR numbers after creation. **Wait for approval.**

## S6: Create (Step 7)

```bash
gh stack submit --auto [--remote <name>]
```

- This creates every target's PR as a **draft** with a placeholder title, and links the stack on GitHub. Don't add `--open`: it also flips *existing* draft PRs in the stack to ready.
- Exit 9 → stacked PRs aren't enabled for this repository. Stop and report; don't fall back to `gh pr create` without asking.
- Exit 8 (stack locked) → wait ~5 s and retry once, then report.

Then read the new PR numbers with `gh stack view --json`, replace every `#<branch-name>` placeholder with that branch's `#<pr.number>` (the only change allowed after approval), and apply the messages to each target:

```bash
gh pr edit <n> --title "<title>" --add-assignee @me --body-file - <<'EOF'
<body>
EOF
```

- Use `--body-file -` with a quoted heredoc, never a multi-line `--body` argument.
- Drop `--add-assignee @me` when the template or the user specified an assignee (assign them instead).
- Unless the user asked for drafts, mark each **new** PR ready: `gh pr ready <n>`. This matches plain pr-create's default (non-draft) without touching PRs that existed before.
- Report every new PR's URL from the JSON, bottom first. No extra re-fetch.
- If any PR existed before this run, its stack section (position, upper neighbor) is now stale. Say so and suggest `/murnana-github:stack-pr-message` to refresh it; don't edit those PRs here.
