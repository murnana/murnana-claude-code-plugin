---
paths:
  - ".claude-plugin/marketplace.json"
---

# Marketplace Manifest Rules

- Give every plugin entry a `git-subdir` source, never a relative path:
  `{"source": "git-subdir", "url": "https://github.com/murnana/murnana-claude-code-plugin.git", "path": "plugins/<plugin-name>"}`.
  Write `url` as the full HTTPS URL, not the `owner/repo` shorthand: the shorthand is cloned over SSH, which fails with `Permission denied (publickey)` for users without a GitHub SSH key.
  Users add this marketplace with `--sparse .claude-plugin`, so `plugins/` is absent from the marketplace checkout and a relative path fails at install with `Source path does not exist`.
- Pin each entry of this repository to the released commit with `source.sha` (the full 40-character SHA), and leave `ref` unset. Change `version` and `sha` together with `sh scripts/set-plugin-version.sh <plugin-name> <version>`, never one alone.
  The pin keeps stable installs on the released files even if `main` moves on. On a PR into `main`, `Check plugin versions` fails when `plugins/<plugin-name>/` differs from the files at `sha`, or when `sha` is not in the PR's history.
- Plugins installed through this (stable) marketplace come from GitHub `main`, so unpushed changes and anything still on `develop` or a `feature/*` / `bugfix/*` branch never show up there. `develop` reaches users only through the dev channel (`.claude/rules/release-channels.md`). Test local changes with `claude --plugin-dir plugins/<plugin-name>`.
- After editing this file, regenerate the dev channel catalog with `sh scripts/build-dev-marketplace.sh` and commit it too.
- After editing, run `claude plugin validate .` and `claude plugin validate channels/dev`. It does not read `plugin.json` of `git-subdir` plugins, so also run `claude plugin validate plugins/<plugin-name>` for each plugin whose files changed.
- `unity-ariadne` is the one entry whose plugin lives in another repository: its `source` is `git-subdir` with `url` `https://github.com/murnana/unity-ariadne.git` and `path` `claude-plugins`. Keep its `version` equal to `version` in that repository's `claude-plugins/.claude-plugin/plugin.json`; `Check plugin versions` does not cover it. See `docs/plugins/unity-ariadne/README.md`.
