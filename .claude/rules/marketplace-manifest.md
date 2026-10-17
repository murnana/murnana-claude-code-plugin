---
paths:
  - ".claude-plugin/marketplace.json"
---

# Marketplace Manifest Rules

- Give every plugin entry a `git-subdir` source, never a relative path:
  `{"source": "git-subdir", "url": "murnana/murnana-claude-code-plugin", "path": "plugins/<plugin-name>"}`.
  Users add this marketplace with `--sparse .claude-plugin`, so `plugins/` is absent from the marketplace checkout and a relative path fails at install with `Source path does not exist`.
- Leave `ref` unset on the source. Entries follow `main`; a pinned ref would keep users on the old copy even after a version bump.
- Plugins installed through the marketplace come from GitHub `main`, so unpushed or unmerged changes never show up. Test local changes with `claude --plugin-dir plugins/<plugin-name>`.
- After editing, run `claude plugin validate .`. It does not read `plugin.json` of `git-subdir` plugins, so also run `claude plugin validate plugins/<plugin-name>` for each plugin whose files changed.
