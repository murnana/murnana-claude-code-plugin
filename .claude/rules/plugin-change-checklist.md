---
paths:
  - "plugins/**"
---

# Plugin Change Checklist

Applies to every change under `plugins/<plugin-name>/`. Do these in the same PR.

- Update `docs/plugins/<plugin-name>/<skill-or-agent>.md` (Japanese) when behavior, frontmatter or `allowed-tools` changes. Add the reason for the decision under its design section. Link to `references/` files instead of copying their content.
- Add an entry under `## [Unreleased]` in `docs/plugins/<plugin-name>/CHANGELOG.md`, in Japanese, written for the plugin's user (what changes for them), not as a description of the diff.
- Do not edit `version` in `plugin.json` or `marketplace.json`. Versions change only in the release PR (`.claude/rules/plugin-version-bump.md`).
- Update `README.md` when a skill is added, renamed or removed: its plugin table lists the slash commands.
- If the change touches `skills/changelog-write/`, `skills/commit/` or `skills/pr-create/`, follow the matching `*-sync.md` rule in `.claude/rules/`.
- If the change adds text, code or a template taken from another source, follow `.claude/rules/third-party-notices.md`.
- Keep everything the plugin needs inside `plugins/<plugin-name>/`. Each plugin is installed alone (`git-subdir`), so a link to `docs/`, `evals/` or another plugin's files is broken for the user.
