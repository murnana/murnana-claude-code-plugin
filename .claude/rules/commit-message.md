# Commit Message Rules

Applies whenever you write a commit message in this repository.

These rules mirror the `commit` skill of the `murnana-git` plugin (`plugins/murnana-git/skills/commit/SKILL.md` and `references/commit-message.md`). When that skill changes, update this file to match (see `.claude/rules/commit-message-sync.md`).

- Write one commit per "why": if a change needs more than one sentence to explain why, split it. Order commits so the tree builds at each step.
- Format:

  ```
  :emoji: Short, concise title (~50 chars)

  Why this change was needed: the problem solved, the constraint satisfied, or the reasoning behind the decision. Do not restate the How; the diff shows it.

  Refs: #123
  ```

- The title starts with a GitHub emoji markup code. The body is optional, but required whenever the why is not obvious from the title or the diff.
- Write the message in Japanese, as the history does.
- Emoji (gitmoji-based): `:sparkles:` feature, `:bug:` bug fix, `:recycle:` refactor, `:memo:` documentation, `:white_check_mark:` tests, `:art:` assets, `:zap:` performance, `:fire:` removal, `:wrench:` configuration, `:arrow_up:` dependency update, `:bookmark:` version bump, `:construction:` work in progress, `:green_heart:` CI fix.
- Stage explicit paths (`git add <paths>`), never `git add -A` or `git add .`. Pass the message through a heredoc.
- Do not use `--no-verify`, `git push`, `git commit --amend` or `git reset` unless the user asks.
- Append the attribution lines the session requires (e.g. `Co-Authored-By:`).
