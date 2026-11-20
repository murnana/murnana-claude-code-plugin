---
paths:
  - ".claude-plugin/marketplace.json"
  - "channels/**"
  - "scripts/build-dev-marketplace.sh"
---

# Release Channel Rules

This repository publishes two marketplaces from the same plugin sources:

| Channel | Catalog | Marketplace `name` | Plugins come from | Version |
|---|---|---|---|---|
| stable | `.claude-plugin/marketplace.json` on `main` | `murnana-claude-code-plugin` | the released commit pinned by `source.sha` (see `.claude/rules/marketplace-manifest.md`) | the entry's `version` |
| dev (early access) | `channels/dev/.claude-plugin/marketplace.json` on `develop` | `murnana-claude-code-plugin-dev` | `ref: "develop"` | none: Claude Code uses the commit SHA |

- Users add the dev channel by the raw URL of the `develop` copy:
  `claude plugin marketplace add https://raw.githubusercontent.com/murnana/murnana-claude-code-plugin/develop/channels/dev/.claude-plugin/marketplace.json`.
  That makes it a `url` marketplace: Claude Code downloads only that file, so it needs no `--sparse`, and every entry must stay `git-subdir`.
  The copy of `channels/dev/` on `main` is never read by users.
- Generate the dev catalog; never edit it by hand. After any change to `.claude-plugin/marketplace.json`, run `sh scripts/build-dev-marketplace.sh` and commit both files. The `Check plugin versions` workflow fails when they differ (`--check`).
- The generator renames the marketplace with `-dev`, and for this repository's entries and for `unity-ariadne` (`murnana/unity-ariadne`) drops `version` and `source.sha` and sets `source.ref` to `develop`. Entries from any other repository would be copied unchanged.
- The dev channel tracks commits only because no `version` is set anywhere. Keep `version` out of `plugin.json` (`.claude/rules/plugin-version-bump.md`); with it, Claude Code would pin the dev install to that string. For `unity-ariadne` the same holds in its own repository: `claude-plugins/.claude-plugin/plugin.json` there must not set `version`, and its `release.yml` checks that. Releases before 0.3.0 still set it, so the dev channel is correct only from the `develop` commit that removed it.
- `unity-ariadne` on `develop` may need a newer `ariadne` command than the released one (new MCP tools). Early-access users of it should install `ariadne` from `develop` builds or accept missing tools.
- The dev version is the `develop` commit SHA, so every merge into `develop` offers an update for every dev plugin, even ones whose files did not change. This is expected.
- The two marketplaces have different names, so a user can add both. Tell users not to install the same plugin from both: the manifest names collide and the hooks of one copy do not run. To switch, `claude plugin uninstall <plugin>@<old-marketplace>` first, then install from the other.
- Keep the two channels' install commands in `README.md` and `CONTRIBUTING.md` in step with this file.
