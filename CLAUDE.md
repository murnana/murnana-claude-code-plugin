# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo is a **Claude Code plugin marketplace** owned by `murnana`. The marketplace manifest lives at `.claude-plugin/marketplace.json` and currently lists seven published plugins (`murnana-unreal-engine`, `murnana-git`, `murnana-github`, `murnana-agent-config`, `murnana-tech-docs`, `murnana-unity-package`, `murnana-unity`). Work in this repo will typically mean **adding plugins to the marketplace** and/or **authoring plugin source** that the marketplace points to.

## Marketplace manifest

`.claude-plugin/marketplace.json` is the entry point. Its `plugins` array lists each published plugin. When adding a plugin, append an entry following the Claude Code plugin marketplace schema (`name`, `source`, `description`, `version`, etc.). Keep `name` and `owner.name` in sync with the repository identity (`murnana-claude-code-plugin` / `murnana`).

A user installs this marketplace with:

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
```

…then `claude plugin install <plugin-name>@murnana-claude-code-plugin`. `--sparse .claude-plugin` keeps the marketplace checkout to the manifest only; each plugin is fetched separately at install time because its `source` is `git-subdir`.

## Branch workflow

Development branches off `develop` (created from `main` if missing) as `feature/*` or `bugfix/*`, and merges back into `develop` without bumping plugin versions. Versions are bumped only in the `develop` → `main` release PR. Urgent fixes to released `main` use `hotfix/*` from `main`. Details live in `.claude/rules/branch-workflow.md` and `.claude/rules/plugin-version-bump.md`.

## Commit and PR messages

Follow the `murnana-github` `pr-create` skill for pull request titles and bodies (mirrored in `.claude/rules/pr-message.md`; update it whenever that skill changes, see `.claude/rules/pr-message-sync.md`).

Follow the `murnana-git` `commit` skill (gitmoji title, Why-driven body, one why per commit). The mirrored rules live in `.claude/rules/commit-message.md`; update them whenever that skill changes (`.claude/rules/commit-message-sync.md`).

## Third-party material

Before adding anything copied, summarized or adapted from another source, check its license and update that plugin's `plugins/<plugin-name>/THIRD_PARTY_NOTICES.md` in the same PR. There is no repository-root notices file. Details live in `.claude/rules/third-party-notices.md`.

## Conventions

- Plugin sources should live in their own directories (e.g. `plugins/<plugin-name>/`) with a `.claude-plugin/plugin.json` and the relevant `commands/`, `agents/`, `hooks/`, `skills/`, or `mcp.json` subpaths as appropriate.
- `marketplace.json` conventions (source type, local testing, validation) live in `.claude/rules/marketplace-manifest.md`.
- Per-plugin documentation (usage, design rationale) lives under `docs/plugins/<plugin-name>/`, separate from the plugin's own `skills/*/references/` (which holds the rules Claude reads at runtime).
