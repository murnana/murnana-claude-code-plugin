---
paths:
  - "plugins/murnana-tech-docs/skills/changelog-write/**"
  - "plugins/murnana-unity-package/skills/changelog-write/**"
---

# changelog-write Sync Rules

`murnana-tech-docs` and `murnana-unity-package` each ship a `changelog-write` skill. The UPM copy started as a copy of the tech-docs one. They stay separate files because each `git-subdir` plugin is installed alone and can't link into another plugin's tree.

## Keep the shared parts in sync

- When changing `SKILL.md` or `references/*.md` in one copy, make the same change to the matching file in the other copy, in the same PR. Skip this only for the plugin-specific parts below.
- Mirror the intent, not the exact text. Keep each copy's own wording and examples (generic examples in tech-docs, Unity examples in the UPM copy).
- Shared, so mirror them:
  - the Keep a Changelog version check and the 2.0.0 snapshot (`keep-a-changelog.md`)
  - the entry rules, the general breaking-change checklist, per-type guidance and "When to ask" (`entry-writing.md`)
  - rewriting the changelog and its link references at release time (`release.md`)
  - the generic rows of the project-rules table (`project-rules.md`)
  - the SKILL.md checklist, the approval flow and the generic Gotchas
- If a change is deliberately not mirrored, say so and why in the PR description.

## Plugin-specific: never copy across

- UPM only: `references/unity-package.md`, the `package.json` version update, Unity's version rules, `-exp`/`-pre` suffixes, `.meta` handling, the Validation Suite and `[Unreleased]` removal, UPM tag patterns, the Unity-specific rows in `project-rules.md`, and the Unity names and examples in `entry-writing.md`.
- UPM only in SKILL.md: the frontmatter (`description`, `when_to_use`, `allowed-tools`, no `disable-model-invocation`) and the stop when no UPM package is found.
- tech-docs only: `disable-model-invocation: true`, the murnana-claude-code-plugin example in `project-rules.md`, and "don't edit version fields" in `release.md`.

## Versioning

- A mirrored change touches both plugins. Add an entry to both CHANGELOGs under `[Unreleased]` in the same `feature/*` / `bugfix/*` PR. Bump both versions in the `develop` → `main` release PR, following `.claude/rules/plugin-version-bump.md`.
