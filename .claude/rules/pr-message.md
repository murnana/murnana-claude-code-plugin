# Pull Request Message Rules

Applies whenever you write a pull request title or body in this repository.

These rules mirror the `pr-create` skill of the `murnana-github` plugin (`plugins/murnana-github/skills/pr-create/SKILL.md` and `references/pr-message.md`). When that skill changes, update this file to match (see `.claude/rules/pr-message-sync.md`).

- Target the base branch the branch workflow prescribes: `develop` for `feature/*` and `bugfix/*`, `main` for the release PR (`develop` → `main`) and `hotfix/*` (see `.claude/rules/branch-workflow.md`).
- If the repository has a PR template (`.github/PULL_REQUEST_TEMPLATE/*.md`, `.github/pull_request_template.md`, `docs/pull_request_template.md`, `pull_request_template.md`), use it and keep its instructional comments; do not add the sections below on top of it.
- Otherwise use this format:

  ```
  :emoji: Short phrase summarizing the change (~50 chars)

  ## なぜ (Why)
  The problem solved, the constraint satisfied, or the reasoning behind the change.

  ## 影響範囲 (Scope / Impact)
  What this change affects: files, features, users, or systems that could be touched.

  ## デバッグ方法 (How to verify)
  Concrete steps to check the change works: commands to run, screens to check, edge cases to try.

  🤖 Generated with [Claude Code](https://claude.com/claude-code)
  ```

- The title starts with a GitHub emoji markup code (same table as `.claude/rules/commit-message.md`) and is written in Japanese. All three body sections are required, and the attribution line always goes last.
- Name the specific files or consumers under 影響範囲, and give an exact command or click-path under デバッグ方法. Do not re-describe the diff line by line.
- Run the relevant checks before pushing; if a check or the push fails, stop and report instead of creating the PR. Never force-push.
- Show the base branch, title and full body and wait for approval before creating the PR. Pass the body through stdin (`--body-file -`), not a multi-line `--body` argument.
- Add `--assignee @me` unless an assignee is specified. Use `--draft` only when asked.
