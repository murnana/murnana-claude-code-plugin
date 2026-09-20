---
name: commit
description: use `git commit` the working tree.
argument-hint: "[optional scope or intent hint]"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git add *) Bash(git restore --staged *) Bash(git commit *) Bash(git config *) Read Grep Glob AskUserQuestion
---

# Commit

Split the working tree into well-formed commits and create them, following the project's own commit rules when they exist, or a Why-driven convention otherwise.

## Current state

```sh
git status --short --branch
git diff --numstat
git diff --cached --numstat 2>/dev/null || true
git log --format='%s' --no-merges -15 2>/dev/null || true
```

Treat `$ARGUMENTS` (if any) as an additional hint about which changes to focus on or what the user's intent is — it does not override the steps below.

## Output discipline

Every command's output is spent tokens. Always choose the narrowest form that answers the question at hand:

- `git status --short --branch`, never bare `git status` — short format plus branch and tracking info in a single line.
- `--numstat` over `--stat` for diff summaries: no histogram bars, no padding, and pathnames are never abbreviated, so they stay usable as arguments.
- Locate changes with `--numstat` first; read hunks only for the paths you are actually grouping into a commit, and read them with `-U1`.
- Bound every history query: `git log --oneline -<n>`, never an unbounded `git log`.
- Never re-run a command whose output is already in this context.

## Step 1: Understand the diff

The state above already gives the branch, the staged and unstaged file lists, and recent history — do not re-run those commands.

Read the actual changes **path-scoped**, never as one bare `git diff`:

- `git diff -U1 -- <paths>` / `git diff --cached -U1 -- <paths>`, limited to the files you are about to group into a commit.
- For lock files, generated output, and vendored trees, the `--numstat` line above is enough — skip their hunks.
- Untracked files (`??` above) have no diff. `Read` them directly, and only the ones whose content actually affects how the work is split.

If some changes are already staged, treat that staging as intentional and respect it.

## Step 2: Discover project rules (highest priority)

Check the sources listed in [references/project-rules.md](references/project-rules.md), in order. If a rule is found there, it is the **only** rule that applies — do not mix in anything from the fallback convention below.
The history needed to infer a format is already injected above — do not re-run `git log`.
If you fall back to inferring a format from that history (weaker than an explicit rule), say so explicitly when presenting the plan in Step 4.

Before reading a candidate rule file, `Glob` for it first — only `Read` files that actually exist.

## Step 3: Run pre-commit checks

- If husky, lefthook, or pre-commit is configured, it will run automatically on `git commit` — do not run it manually as well.
- Otherwise, if the project defines lint/test/format/build tasks, run the ones relevant to the changed files.
- If a check fails, **stop without committing**, report the failure output as-is, and ask how to proceed.
- Never use `--no-verify` unless the user explicitly asks for it.

## Step 4: Split into "one commit = one why" units and get approval

- Group changes so each commit can be explained by a single "why" sentence. If a group of changes needs more than one such sentence, split it further.
- Order commits so the tree builds/passes at each step (foundational changes first).
- Present the split plan and each draft commit message, and **wait for approval** before committing anything — even when everything fits in a single commit.

## Step 5: Commit sequentially

- Stage explicit paths per commit with `git add <paths>` — never `git add -A` or `git add .`.
- If a file was already staged as part of a different "why" than the commit you're about to make, unstage it first with `git restore --staged <paths>`, then re-add only the paths for this commit.
- Pass the message via heredoc to avoid mangling Japanese text, line breaks, or punctuation.
- Never sweep in unrelated or unstaged changes that belong to a different why.
- Never run `git push`, `git commit --amend`, or `git reset` unless explicitly instructed.
- Append any attribution lines (e.g. `Co-Authored-By:`) required by the session or project.
- After all commits, report the result in Japanese using `git log --oneline -<N>`, where `<N>` is the number of commits just created.

## References

- Message format, emoji table, and Why examples:
  [references/commit-message.md](references/commit-message.md)
- Where to look for project-specific rules:
  [references/project-rules.md](references/project-rules.md)
