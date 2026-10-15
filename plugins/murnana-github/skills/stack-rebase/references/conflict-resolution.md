# Conflict resolution for stacked branches

Condensed from <https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands> and the official gh-stack agent skill. When this file and `gh stack rebase --help` disagree, the CLI wins.

## How `gh stack rebase` works

- Fetches the remote (unless `--no-trunk`), then rebases each branch onto the tip of the layer below, from the trunk upward.
- For a layer whose PR is already merged, it switches to `--onto` mode so the merged commits aren't replayed again. This is why manual `git rebase` goes wrong after partial merges.
- `--committer-date-is-author-date` (`--preserve-dates`) keeps commit dates; the setting persists across `--continue`.

## Exit codes during rebase / sync

| Code | Meaning | What to do |
|---|---|---|
| 3 | Rebase conflict | Resolve → `git add` → `gh stack rebase --continue` |
| 3 from `sync` | Conflict; sync already restored every branch | `gh stack rebase` to reproduce, then resolve |
| 7 | A rebase is already in progress | Ask: `--continue` or `--abort` |
| 8 | Stack locked by another process (another worktree / terminal) | Wait ~5 s, retry once, then report |
| 2 | Not in a stack | Stop |
| 4 | GitHub API failure (sync) | Report; retry if transient |
| 10 | Interrupted `modify` | User runs `gh stack modify --abort` themselves |

`sync` divergence (local and remote stacks differ) in a non-interactive run: prints both chains, changes nothing, exits 0 with "Sync aborted". Show both chains to the user and ask which is the source of truth; resolving it needs an interactive `gh stack sync` in their own terminal.

## `--continue` and `--abort`

- Both act on the worktree recorded in gh-stack's journal (under the common `.git` directory), wherever you run them.
- `--abort` restores **every** branch in the stack to its pre-rebase state — not only the one that conflicted. It's the safe exit.
- Don't use `git rebase --continue` / `--abort`: gh-stack wouldn't advance to the next branch or record the outcome.

## rerere

`gh stack init` enables `git rerere`. When the same conflict appears again on a higher layer, git re-applies your earlier resolution automatically. Still verify the result: `git diff` on the "resolved" file before `git add`.

## Resolution principles

1. **The lower layer wins on its own concern.** The layer being rebased onto is what will land first; the upper layer adapts to it.
2. **Keep both intents when they are compatible.** Adjacent edits, import lists, and renamed-symbol call sites are mechanical: merge them.
3. **Ask when behavior differs.** Different logic for the same case, modify-vs-delete, or a schema disagreement → present the options with `AskUserQuestion`.
4. **Don't move code between layers during a rebase.** If the conflict shows a change belongs in a different layer, finish or abort the rebase first, then make that change in the right layer and rebase `--upstack`.
5. **No conflict markers left.** Before `git add`, grep the file for `<<<<<<<`, `=======`, `>>>>>>>`.
