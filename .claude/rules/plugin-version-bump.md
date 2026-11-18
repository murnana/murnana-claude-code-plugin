# Plugin Version Bump Rules

Applies when creating a pull request from `develop` into `main` (a release). See `.claude/rules/branch-workflow.md` for the overall flow.

Do not bump versions in `feature/*` or `bugfix/*` pull requests into `develop`. In those, only add entries under `## [Unreleased]` in `docs/plugins/<plugin-name>/CHANGELOG.md`.

- Find the plugins that changed since the last release: `git diff --name-only origin/main...origin/develop -- plugins/`.
  Bump each of them in the release PR with `sh scripts/set-plugin-version.sh <plugin-name> <x.y.z>`. It sets the entry's `version` and its `source.ref` (`<plugin-name>--v<x.y.z>`) in `.claude-plugin/marketplace.json`, and regenerates the dev channel catalog.
  Users keep their cached copy until the version string changes, so unbumped changes never reach them.
- Bump only the plugins whose files changed. Leave the others alone.
- The entry in `.claude-plugin/marketplace.json` is the only place a plugin's version is written.
  Never add `version` to `plugins/<plugin-name>/.claude-plugin/plugin.json`: Claude Code reads it before the entry, so it would also pin an install that tracks a branch and stop it from receiving new commits.
  `claude plugin validate plugins/<plugin-name>` warns `No version specified`; that warning is expected.
- Follow Semantic Versioning (https://semver.org/): `MAJOR.MINOR.PATCH`, with no `v` prefix.
  - Patch: backward-compatible fixes and doc edits inside the plugin.
  - Minor: backward-compatible new or changed skills/commands/hooks.
  - Major: breaking changes (renamed or removed skills/commands, changed behavior users rely on). Reset lower numbers to 0.
  - While the version is `0.y.z`, anything may change at any time, so breaking changes may go in a minor bump.
  - Choose the level from the combined changes accumulated in `[Unreleased]`, using the largest one.
- Record changes in `docs/plugins/<plugin-name>/CHANGELOG.md` under `## [Unreleased]` as they are made (in the `feature/*` / `bugfix/*` PR), in Japanese, using the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) categories (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
- In the release PR, move the `[Unreleased]` entries to a new `## [x.y.z] - YYYY-MM-DD` section and update the link references at the bottom of the file. Point new links at the release tag: `[x.y.z]: https://github.com/murnana/murnana-claude-code-plugin/tree/<plugin-name>--vx.y.z/plugins/<plugin-name>` and `[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/<plugin-name>--vx.y.z...main`. Leave the older commit-based links as they are.
- Do not create tags by hand. After the release PR is merged, the `Tag plugin releases` workflow (`.github/workflows/release-tags.yml`) tags `main` with `<plugin-name>--v<version>` for every entry whose tag is missing. Until it finishes (usually under a minute), stable installs of the new versions fail because the tag does not exist yet. Check the run succeeded. It also fails when a plugin's files on `main` differ from its existing tag, which means a change reached `main` without a version bump.
- The `Check plugin versions` workflow (`.github/workflows/version-check.yml`) checks only versions: no `plugin.json` may set `version`, every entry's `version` must be `MAJOR.MINOR.PATCH` with `source.ref` `<plugin-name>--v<version>`, the dev channel catalog must match its generator, a PR into `main` must raise the version of every changed plugin, and `feature/*` / `bugfix/*` PRs into `develop` must not change a version. It does not run `claude plugin validate`; run that locally.
- Run `claude plugin validate .` before opening the release PR.
- Do not bump versions for changes outside `plugins/` (README, `docs/`, CLAUDE.md, `.claude/`). Editing a CHANGELOG alone needs no bump.
