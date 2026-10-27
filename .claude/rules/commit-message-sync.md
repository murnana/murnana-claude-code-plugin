---
paths:
  - "plugins/murnana-git/skills/commit/**"
---

# Commit Message Sync Rules

`.claude/rules/commit-message.md` mirrors the `murnana-git` `commit` skill. The skill is the source of truth.

- When changing `SKILL.md` or `references/*.md` of the `commit` skill (format, emoji table, splitting rules, safety rules), make the matching change to `.claude/rules/commit-message.md` and the commit-message section of `CONTRIBUTING.md` in the same PR.
- Mirror the intent, not the exact text. Keep the rule file short.
- The skill's project-rule lookup and pre-commit steps are skill behavior, not commit-message rules; do not copy them.
- If a change is deliberately not mirrored, say so and why in the PR description.
- Changing the skill is a change under `plugins/murnana-git/`; bump its version in the release PR (see `.claude/rules/plugin-version-bump.md`).
