---
name: stack-rebase
description: Cascade-rebase a GitHub stack with gh stack rebase / sync, resolve conflicts, and push
argument-hint: "[--upstack | --downstack | --no-trunk | sync]"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git add *) Bash(git rev-parse *) Bash(gh stack view *) Bash(gh stack rebase *) Bash(gh stack rebase) Bash(gh stack push *) Bash(gh stack push) Bash(gh stack sync *) Bash(gh stack sync) Read Edit Grep Glob AskUserQuestion
---

# Stack Rebase

Restore a linear history across a GitHub stack — every branch containing the tip of the layer below it — with `gh stack rebase` (or `gh stack sync`), resolve any conflicts, and push.

## Current state

```bash
git status --short --branch
gh stack view --json 2>&1 || true
```

Treat `$ARGUMENTS` as the requested mode (`--upstack`, `--downstack`, `--no-trunk`, or `sync`). With no argument, choose per Step 2.

## Ground rules (read first)

- Only `gh stack rebase` / `gh stack sync` move branches, and only `gh stack push` / `sync` push them. Never run `git rebase`, `git rebase --continue`, `git push --force`, or `git push` on stack branches yourself: gh-stack keeps its own journal and per-branch metadata, and bypassing it desyncs the stack (wrong `--onto` after merges, broken `--abort`).
- Never run `gh stack modify` or `gh stack switch` — TUI-only, they block this session.
- Pushing rewrites remote history and re-triggers CI on every PR, so **get approval before any push**.

Copy this checklist into your response and tick it off:

```
- [ ] 1 Preconditions
- [ ] 2 Choose mode
- [ ] 3 Rebase (conflict loop)
- [ ] 4 Verify
- [ ] 5 Approval → push
```

## Step 1: Preconditions

- `gh stack view --json` failed with exit 2 → the current branch isn't in a stack. Stop and say so (`/murnana-github:stack-create` builds one).
- Working tree dirty → stop. `rebase` and `sync` never stash. Ask the user to commit (to the layer that owns the change) or stash, then re-run.
- Exit 7 / a rebase already in progress → ask whether to `gh stack rebase --continue` (go to Step 3's loop) or `gh stack rebase --abort`.
- Exit 10 → a `modify` session was interrupted. The user must run `gh stack modify --abort` themselves; stop.
- From the JSON, note which branches have `needsRebase: true` and which are `isMerged`.

## Step 2: Choose the mode

| Situation | Command |
|---|---|
| User asked, or trunk moved and/or several layers need rebase (default) | `gh stack rebase` |
| A mid-stack layer just got new commits; only layers above it are stale | check out that layer, `gh stack rebase --upstack` |
| Only want trunk → current branch updated | `gh stack rebase --downstack` |
| Re-chain layers onto each other without pulling trunk | `gh stack rebase --no-trunk` |
| Lower PRs were merged on GitHub, or the remote stack changed (PRs added on the web) | `gh stack sync` — it fetches, reconciles, rebases, pushes, and refreshes PR state |

`sync` pushes as part of its run, so ask for approval (Step 5) **before** running it, not after. Add `--prune` (delete local branches of merged PRs) only if the user asked for it.

With multiple remotes and no `remote.pushDefault`, add `--remote <name>` to `rebase`/`push`/`sync`.

## Step 3: Rebase and the conflict loop

Run the chosen command. On exit 0, go to Step 4. On exit 3 (conflict):

1. The output lists conflicted files with line numbers. `git status --short` confirms them.
2. For each file, Read the conflict hunks and identify which side is the **lower layer** (the branch being rebased onto) and which is the layer being replayed. Explain both intents to the user in one or two lines.
3. Resolve:
   - Mechanical (both sides' intents compatible: adjacent edits, import order, renamed symbol) → Edit to keep both intents.
   - Semantic or ambiguous (two different behaviors, deleted-vs-modified) → `AskUserQuestion` with the concrete options. Don't guess.
4. `git add <resolved files>`, then `gh stack rebase --continue`.
5. Repeat until exit 0. `rerere` (enabled by `gh stack init`) replays a resolution you already made when the same conflict reappears higher up the stack.
6. If the user wants out at any point: `gh stack rebase --abort` restores every branch to its pre-rebase state.

If `sync` hit the conflict, it has already restored all branches. Run `gh stack rebase` to reproduce the conflict, then use this loop.

Details per exit code and resolution principles: [references/conflict-resolution.md](references/conflict-resolution.md).

## Step 4: Verify

- `gh stack view --json`: every unmerged branch must have `needsRebase: false`. If not, report which and why before going further.
- If conflicts were resolved by hand, run the project's relevant checks (same discovery as pr-create Step 3; each is a permission-prompted call) on the affected layers. A failure stops before push.

## Step 5: Approval, then push

- Show which branches will be force-pushed (with lease) and their PR numbers, and **wait for approval**.
- Run `gh stack push`. It uses per-branch `--force-with-lease` and is **not atomic**: if one branch is rejected (someone pushed to it), the others still update. Report the rejected branch; usually `gh stack sync` reconciles it, then push again.
- Merged and queued branches are skipped automatically.
- Report the result. Mention that a rebase which doesn't change a PR's diff keeps its existing approvals.

## Gotchas

- Fix a lower layer's problem in that layer (`gh stack down`/`checkout <branch>`, commit, `gh stack rebase --upstack`) — never patch around it on an upper branch to avoid a rebase.
- `rebase` and `sync` also update clean linked worktrees, and block if an affected worktree is dirty or busy. Report the blocking worktree path rather than touching it.
- `--continue` / `--abort` act on the worktree recorded in gh-stack's journal, not necessarily the current one.
- Exit 8 (stack locked): wait ~5 s and retry once.
- When no conflicts are expected, GitHub's **Rebase stack** button in the PR merge box does a server-side cascading rebase — a valid alternative the user can choose instead of this skill.
- Merging the bottom PR on GitHub auto-rebases the rest; run `sync`, not `rebase`, to pick that up locally.

## References

- Exit codes, `--continue`/`--abort` semantics, rerere, resolution principles:
  [references/conflict-resolution.md](references/conflict-resolution.md)
