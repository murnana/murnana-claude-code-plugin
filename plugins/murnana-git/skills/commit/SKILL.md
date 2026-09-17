---
name: commit
description: >
  Commit the working tree, obeying the project's own commit rules when they exist
  and falling back to a Why-driven convention when they do not. Splits changes so
  that one commit carries exactly one "why", runs the project's pre-commit checks,
  and asks for approval before committing.
argument-hint: "[optional scope or intent hint]"
disable-model-invocation: true
allowed-tools: >
  Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git add *)
  Bash(git commit *) Bash(git branch *) Bash(git config *)
  Read Grep Glob AskUserQuestion
---

# Commit

Split the working tree into well-formed commits and create them, following the
project's own commit rules when they exist, or a Why-driven convention otherwise.

## Current state

```!
git status --short
git diff --stat HEAD
git log --format='%s' -20
```

Treat `$ARGUMENTS` (if any) as an additional hint about which changes to focus on
or what the user's intent is — it does not override the steps below.

## Step 1: Understand the diff

Using the injected state above as a starting point, run `git diff`,
`git diff --staged`, and `git branch --show-current` as needed to fully understand
the changes. If some changes are already staged, treat that staging as intentional
and respect it.

## Step 2: Discover project rules (highest priority)

Check the sources listed in [references/project-rules.md](references/project-rules.md),
in order. If a rule is found there, it is the **only** rule that applies — do not mix
in anything from the fallback convention below. If you fall back to inferring a
format from `git log` history (weaker than an explicit rule), say so explicitly when
presenting the plan in Step 4.

## Step 3: Run pre-commit checks

- If husky, lefthook, or pre-commit is configured, it will run automatically on
  `git commit` — do not run it manually as well.
- Otherwise, if the project defines lint/test/format/build tasks, run the ones
  relevant to the changed files.
- If a check fails, **stop without committing**, report the failure output as-is,
  and ask how to proceed.
- Never use `--no-verify` unless the user explicitly asks for it.

## Step 4: Split into "one commit = one why" units and get approval

- Group changes so each commit can be explained by a single "why" sentence. If a
  group of changes needs more than one such sentence, split it further.
- Order commits so the tree builds/passes at each step (foundational changes first).
- Present the split plan and each draft commit message, and **wait for approval**
  before committing anything — even when everything fits in a single commit.

## Step 5: Commit sequentially

- Stage explicit paths per commit with `git add <paths>` — never `git add -A` or
  `git add .`.
- Pass the message via heredoc to avoid mangling Japanese text, line breaks, or
  punctuation.
- Never sweep in unrelated or unstaged changes that belong to a different why.
- Never run `git push`, `git commit --amend`, or `git reset` unless explicitly
  instructed.
- Append any attribution lines (e.g. `Co-Authored-By:`) required by the session or
  project.
- After all commits, report the result in Japanese using `git log --oneline`.

## References

- Message format, emoji table, and Why examples:
  [references/commit-message.md](references/commit-message.md)
- Where to look for project-specific rules:
  [references/project-rules.md](references/project-rules.md)
