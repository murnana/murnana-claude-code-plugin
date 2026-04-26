# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo is a **Claude Code plugin marketplace** owned by `murnana`. The marketplace manifest lives at `claude-plugin/marketplace.json` and currently advertises an empty `plugins` array — i.e. no plugins have been published yet. Work in this repo will typically mean **adding plugins to the marketplace** and/or **authoring plugin source** that the marketplace points to.

## Marketplace manifest

`claude-plugin/marketplace.json` is the entry point. Its `plugins` array lists each published plugin. When adding a plugin, append an entry following the Claude Code plugin marketplace schema (`name`, `source`, `description`, `version`, etc.). Keep `name` and `owner.name` in sync with the repository identity (`murnana-claude-code-plugin` / `murnana`).

A user installs this marketplace with:

```
/plugin marketplace add murnana/murnana-claude-code-plugin
```

…then `/plugin install <plugin-name>@murnana-claude-code-plugin`.

## Conventions

- Plugin sources should live in their own directories (e.g. `claude-plugin/<plugin-name>/`) with a `.claude-plugin/plugin.json` and the relevant `commands/`, `agents/`, `hooks/`, `skills/`, or `mcp.json` subpaths as appropriate.
- After modifying `marketplace.json`, validate it parses as JSON before committing.
