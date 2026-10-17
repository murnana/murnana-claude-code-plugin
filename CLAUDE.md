# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo is a **Claude Code plugin marketplace** owned by `murnana`. The marketplace manifest lives at `.claude-plugin/marketplace.json` and currently lists four published plugins (`murnana-unreal-engine`, `murnana-git`, `murnana-github`, `murnana-agent-config`). Work in this repo will typically mean **adding plugins to the marketplace** and/or **authoring plugin source** that the marketplace points to.

## Marketplace manifest

`.claude-plugin/marketplace.json` is the entry point. Its `plugins` array lists each published plugin. When adding a plugin, append an entry following the Claude Code plugin marketplace schema (`name`, `source`, `description`, `version`, etc.). Keep `name` and `owner.name` in sync with the repository identity (`murnana-claude-code-plugin` / `murnana`).

A user installs this marketplace with:

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
```

…then `claude plugin install <plugin-name>@murnana-claude-code-plugin`. `--sparse .claude-plugin` keeps the marketplace checkout to the manifest only; each plugin is fetched separately at install time because its `source` is `git-subdir`.

## Conventions

- Plugin sources should live in their own directories (e.g. `plugins/<plugin-name>/`) with a `.claude-plugin/plugin.json` and the relevant `commands/`, `agents/`, `hooks/`, `skills/`, or `mcp.json` subpaths as appropriate.
- Give every `marketplace.json` entry a `git-subdir` source (`url`: `murnana/murnana-claude-code-plugin`, `path`: `plugins/<plugin-name>`), not a relative path. A relative path needs `plugins/` in the marketplace checkout, which defeats `--sparse .claude-plugin`.
- Plugins installed through the marketplace come from GitHub `main`, so unpushed or unmerged changes do not show up. Test local changes with `claude --plugin-dir plugins/<plugin-name>`.
- After modifying `marketplace.json`, run `claude plugin validate .` before committing. It no longer checks each plugin's `plugin.json`, so validate those with `claude plugin validate plugins/<plugin-name>`.
- Per-plugin documentation (usage, design rationale) lives under `docs/plugins/<plugin-name>/`, separate from the plugin's own `skills/*/references/` (which holds the rules Claude reads at runtime).
