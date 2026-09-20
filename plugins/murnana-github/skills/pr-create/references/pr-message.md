<!-- kept in sync with plugins/murnana-git/skills/commit/references/commit-message.md —
     this table is duplicated rather than shared because each plugin is independently
     installable and a skill's references/ links only resolve within its own plugin
     tree (${CLAUDE_PLUGIN_ROOT} is per-plugin). When editing one, check the other. -->

# Fallback PR format (no template found)

Apply this format **only when [pr-template-discovery.md](pr-template-discovery.md) finds no template.** If the project has an explicit PR convention documented in [project-rules.md](project-rules.md)'s sources, that takes priority over this file too.

## Format

```
:emoji: Short phrase summarizing the change (~50 chars)

## なぜ (Why)
The problem solved, the constraint satisfied, or the reasoning behind the change.

## 影響範囲 (Scope / Impact)
What this change affects — files, features, users, or systems that could be touched.

## デバッグ方法 (How to verify)
Concrete steps to check the change works: commands to run, screens to check, edge
cases to try.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

- The title starts with a GitHub emoji markup code (e.g. `:memo:`).
- All three body sections are required — do not omit one because it seems obvious.
- The attribution line is required and always goes last.

## Emoji table (gitmoji-based)

| Emoji | Use |
|---|---|
| `:sparkles:` | New feature |
| `:bug:` | Bug fix |
| `:recycle:` | Refactor |
| `:memo:` | Documentation |
| `:white_check_mark:` | Tests |
| `:art:` | New, edit texture, audio and other assets. |
| `:zap:` | Performance |
| `:fire:` | Removal |
| `:wrench:` | Configuration |
| `:arrow_up:` | Dependency update |
| `:bookmark:` | Version bump |
| `:construction:` | Work in progress |
| `:green_heart:` | CI fix |

## Good vs. bad examples

- Bad: a body that just re-describes the diff line by line — the diff is already visible on the PR page.
- Good: 影響範囲 that names the specific consumers/files affected instead of "全体に影響あり", and デバッグ方法 that gives an exact command or click-path, not "動作確認してください".
