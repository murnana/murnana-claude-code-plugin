# Plugin Version Bump Rules

Applies when creating a pull request from `develop` into `main` (a release). See `.claude/rules/branch-workflow.md` for the overall flow.

Do not bump versions in `feature/*` or `bugfix/*` pull requests into `develop`. In those, only add entries under `## [Unreleased]` in `docs/plugins/<plugin-name>/CHANGELOG.md`.

- Find the plugins that changed since the last release: `git diff --name-only origin/main...origin/develop -- plugins/`.
  Bump `version` in `plugins/<plugin-name>/.claude-plugin/plugin.json` for each of them, in the release PR.
  Users keep their cached copy until the version string changes, so unbumped changes never reach them.
- Bump only the plugins whose files changed. Leave the others alone.
- Keep the same plugin's `version` in `.claude-plugin/marketplace.json` equal to `plugin.json`.
  When both are set, Claude Code silently uses `plugin.json`, and `claude plugin validate .` reports a mismatch.
- Follow Semantic Versioning (https://semver.org/): `MAJOR.MINOR.PATCH`, with no `v` prefix.
  - Patch: backward-compatible fixes and doc edits inside the plugin.
  - Minor: backward-compatible new or changed skills/commands/hooks.
  - Major: breaking changes (renamed or removed skills/commands, changed behavior users rely on). Reset lower numbers to 0.
  - While the version is `0.y.z`, anything may change at any time, so breaking changes may go in a minor bump.
  - Choose the level from the combined changes accumulated in `[Unreleased]`, using the largest one.
- Record changes in `docs/plugins/<plugin-name>/CHANGELOG.md` under `## [Unreleased]` as they are made (in the `feature/*` / `bugfix/*` PR), in Japanese, using the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) categories (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
- In the release PR, move the `[Unreleased]` entries to a new `## [x.y.z] - YYYY-MM-DD` section and update the link references at the bottom of the file.
- Run `claude plugin validate .` before opening the release PR.
- Do not bump versions for changes outside `plugins/` (README, `docs/`, CLAUDE.md, `.claude/`). Editing a CHANGELOG alone needs no bump.
