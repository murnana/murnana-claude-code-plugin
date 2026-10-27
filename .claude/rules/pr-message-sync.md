---
paths:
  - "plugins/murnana-github/skills/pr-create/**"
---

# Pull Request Message Sync Rules

`.claude/rules/pr-message.md` mirrors the `murnana-github` `pr-create` skill. The skill is the source of truth.

- When changing `SKILL.md` or `references/*.md` of the `pr-create` skill (message format, emoji table, approval flow, assignee, template handling), make the matching change to `.claude/rules/pr-message.md` and the PR section of `CONTRIBUTING.md` in the same PR.
- The same change goes to the private repository's `.claude/rules/pr-message.md` (`murnana-claude-code-plugin-private`), which cannot be updated by this rule automatically.
- Mirror the intent, not the exact text. Keep the rule file short.
- The skill's stack mode, `gh` fallback and project-rule discovery are skill behavior, not message rules; do not copy them.
- If a change is deliberately not mirrored, say so and why in the PR description.
- Changing the skill is a change under `plugins/murnana-github/`; bump its version in the release PR (see `.claude/rules/plugin-version-bump.md`).
