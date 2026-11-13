# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo is a **Claude Code plugin marketplace** owned by `murnana`. The marketplace manifest lives at `.claude-plugin/marketplace.json` and currently lists sixteen published plugins (see the `plugins` array; the language comment plugins are `murnana-cpp`, `murnana-csharp`, `murnana-java`, `murnana-kotlin`, `murnana-python`, `murnana-rust`, `murnana-swift`, `murnana-typescript`; `unity-ariadne` is sourced from the separate `murnana/unity-ariadne` repository). Work in this repo will typically mean **adding plugins to the marketplace** and/or **authoring plugin source** that the marketplace points to.

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
- `unity-ariadne` is maintained in `murnana/unity-ariadne` (`claude-plugins/`); only its `marketplace.json` entry lives here. When that plugin is updated, update the entry's `version` to match (see `docs/plugins/unity-ariadne/README.md`).
- Name every plugin `murnana-<name>` (except `unity-ariadne`), and use the same name for `plugins/<name>/`, `docs/plugins/<name>/`, `evals/plugins/<name>/`, `plugin.json` `name` and the `marketplace.json` entry (skills are invoked as `/murnana-<name>:<skill>`).
- Keep each plugin's eval cases at the repository root under `evals/plugins/<plugin-name>/`, not inside `plugins/<plugin-name>/`, so they are not installed with the plugin. How to write and run them lives in `.claude/rules/plugin-evals.md`.
- Rules for writing skills and agents, for what to update with a plugin change, and for adding a plugin live in `.claude/rules/plugin-skill-authoring.md`, `.claude/rules/plugin-change-checklist.md` and `.claude/rules/new-plugin.md`.
- Per-plugin documentation (usage, design rationale) lives under `docs/plugins/<plugin-name>/`, separate from the plugin's own `skills/*/references/` (which holds the rules Claude reads at runtime).
