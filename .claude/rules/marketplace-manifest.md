---
paths:
  - ".claude-plugin/marketplace.json"
---

# Marketplace Manifest Rules

- Give every plugin entry a `git-subdir` source, never a relative path:
  `{"source": "git-subdir", "url": "https://github.com/murnana/murnana-claude-code-plugin.git", "path": "plugins/<plugin-name>"}`.
  Write `url` as the full HTTPS URL, not the `owner/repo` shorthand: the shorthand is cloned over SSH, which fails with `Permission denied (publickey)` for users without a GitHub SSH key.
  Users add this marketplace with `--sparse .claude-plugin`, so `plugins/` is absent from the marketplace checkout and a relative path fails at install with `Source path does not exist`.
- Leave `ref` unset on the source. Entries follow `main`; a pinned ref would keep users on the old copy even after a version bump.
- Plugins installed through the marketplace come from GitHub `main`, so unpushed changes and anything still on `develop` or a `feature/*` / `bugfix/*` branch never show up. Test local changes with `claude --plugin-dir plugins/<plugin-name>`.
- After editing, run `claude plugin validate .`. It does not read `plugin.json` of `git-subdir` plugins, so also run `claude plugin validate plugins/<plugin-name>` for each plugin whose files changed.
