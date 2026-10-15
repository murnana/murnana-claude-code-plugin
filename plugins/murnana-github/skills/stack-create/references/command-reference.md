# gh stack command reference (creation)

Condensed from <https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands> (gh-stack v0.2.x). When this file and `gh stack <command> --help` disagree, the CLI wins.

## Contents

- init
- add
- submit
- link
- view --json
- Navigation
- Exit codes

## init

`gh stack init [-b|--base <trunk>] <branch>...`

- Branches are bottom to top. Existing branches are adopted; missing ones are created, each based on the previous one.
- `--base` sets the trunk (default: the repository's default branch). Use it for release or long-lived feature branches.
- Enables `git rerere`.
- Adopts branches checked out in other worktrees without switching them.

## add

`gh stack add [-m <msg>] [-A|-u] <branch>`

- Creates `<branch>` at HEAD on top of the stack and checks it out. You must be on the top branch.
- `-m` commits before creating the branch; with no branch name it generates one (date-slug). `-A` stages everything incl. untracked, `-u` tracked only; both require `-m`. This skill doesn't use them — stage explicitly with `git add <paths>`.

## submit

`gh stack submit --auto [--open] [--remote <name>]`

1. Pushes all branches.
2. Creates a PR for each branch without one.
3. Updates base branches of existing PRs.
4. Creates or updates the stack on GitHub.

- `--auto`: no editor, auto-generated titles, PRs created as **drafts** unless `--open`.
- `--open`: new PRs ready for review, and existing drafts marked ready.
- If every PR in the stack is merged, `submit` starts a new stack for the unmerged branches.

## link

`gh stack link [--base <trunk>] [--open] [--remote <name>] <branch-or-pr>...`

- For branches managed outside gh-stack (jj, Sapling, git-town, plain git). Creates no local tracking, so `rebase`/`sync`/navigation won't work on them afterwards.
- Arguments bottom to top: branch names, PR numbers or PR URLs. Branches are pushed; existing open PRs are reused; new PRs are drafts unless `--open`.
- Additive only — never removes PRs from a stack.
- Grow an existing stack: `gh stack link <stack-number> <new>...` (a numeric first argument is a stack number only if such a stack exists).

## view --json

`gh stack view --json` writes JSON to stdout; status messages go to stderr (don't parse them). Key fields:

| Field | Meaning |
|---|---|
| `trunk` | Stack base branch |
| `currentBranch` | Checked-out branch |
| `branches[]` | Bottom to top |
| `branches[].name`, `.head`, `.base` | Branch, tip SHA, parent branch |
| `branches[].isCurrent`, `.isMerged`, `.isQueued` | State flags |
| `branches[].needsRebase` | Parent's tip is no longer an ancestor |
| `branches[].pr.number`, `.url`, `.state` | PR info (`OPEN` / `MERGED` / `QUEUED`); `pr` absent if no PR yet |

## Navigation

`gh stack up [n]`, `down [n]`, `top`, `bottom`, `trunk`, `checkout <stack#|pr#|url|branch>`. Bottom is nearest the trunk. Never use `switch` (menu-only).

## Exit codes

| Code | Meaning | Action |
|---|---|---|
| 0 | Success | |
| 1 | Generic error | Report output |
| 2 | Not in a stack / stack not found | Check `gh stack view --json`; maybe `init` first |
| 3 | Rebase conflict | Hand off to `/murnana-github:stack-rebase` |
| 4 | GitHub API failure | Report; retry only if transient |
| 5 | Invalid arguments | Re-check `--help` |
| 6 | Branch in multiple stacks | Use a stack number |
| 7 | Rebase already in progress | Hand off to `/murnana-github:stack-rebase` |
| 8 | Stack locked by another process | Wait ~5 s, retry once |
| 9 | Stacked PRs not enabled for this repo | Tell the user and stop |
| 10 | Modify session interrupted | User must run `gh stack modify --abort` themselves (TUI) |
