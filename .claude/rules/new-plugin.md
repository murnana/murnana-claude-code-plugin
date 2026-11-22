---
paths:
  - "plugins/*/.claude-plugin/plugin.json"
---

# New Plugin Rules

- Use one name, `murnana-<name>`, for `plugins/<name>/`, `plugin.json` `name`, the `marketplace.json` entry, `docs/plugins/<name>/` and `evals/plugins/<name>/`.
- Copy the field set of `plugins/murnana-git/.claude-plugin/plugin.json`: `$schema`, `name`, `description`, `license` (`0BSD`), `repository`, `keywords`, `defaultEnabled: false`, `author.name` (`murnana`).
- Do not put `version` in `plugin.json` on `develop` (`.claude/rules/plugin-version-bump.md`). Commit the plugin's files, then run `sh scripts/set-plugin-version.sh <plugin-name> 0.0.1`. It writes `version` `0.0.1` to `plugin.json` and exits; commit that, run the command again to set `version` and `source.sha` on its `marketplace.json` entry, and remove the `plugin.json` version with `sh scripts/strip-plugin-json-version.sh` before the PR into `develop`. This is the one case where a `feature/*` PR sets a version.
- Create these in the same PR as the plugin:
  - the `marketplace.json` entry (`.claude/rules/marketplace-manifest.md`)
  - `docs/plugins/<name>/README.md`, `CHANGELOG.md` (with `## [Unreleased]`) and one `<skill>.md` per skill, in Japanese
  - `plugins/<name>/THIRD_PARTY_NOTICES.md`, if the plugin bundles third-party material or names a trademark
  - `evals/plugins/<name>/` cases for every auto-invocable skill (`.claude/rules/plugin-evals.md`)
  - a row in the plugin table of `README.md`, and the plugin count and list in `CLAUDE.md` ("Repository purpose")
- Run `claude plugin validate .` and `claude plugin validate plugins/<name>`.
