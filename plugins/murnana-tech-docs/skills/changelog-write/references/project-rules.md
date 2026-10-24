# Where to look for project-specific changelog rules

Check all of these. Whatever they say overrides this skill's defaults and Keep a Changelog. If two sources conflict, the explicit instruction (first rows) beats what is inferred from the file (last rows).

| Kind | Where to look | What to take from it |
|---|---|---|
| Instructions | `CLAUDE.md` (root and subdirectories), `.claude/rules/*.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.github/CONTRIBUTING.md`, release docs under `docs/` | Changelog location, language, categories, version policy, when to bump, required link format. Follow exactly as written |
| Release tooling | `.release-please-manifest.json` / `release-please-config.json`, `.changeset/`, `cliff.toml` (git-cliff), `.releaserc*` / `release` key in `package.json` (semantic-release), `changelog.d/` / towncrier config | The tool may own the file or part of it. Don't hand-edit generated sections; for per-change-file setups (`.changeset/`, `changelog.d/`), write the change file the tool expects instead and say so |
| Version source | `package.json`, `plugin.json`, `pyproject.toml`, `Cargo.toml`, `*.csproj`, existing tags | The current version and its scheme (SemVer, CalVer, …) when cutting a release |
| The changelog itself | Its preamble and existing entries | Keep a Changelog version, versioning scheme, language, heading/category order, link-reference format, entry style |

Before reading a candidate, Glob for it. Read only the files that exist.

Example from the murnana-claude-code-plugin marketplace repository: `.claude/rules/plugin-version-bump.md` says plugin changelogs live at `docs/plugins/<plugin-name>/CHANGELOG.md`. Entries go under `## [Unreleased]`, written in Japanese with the Keep a Changelog categories. The version in `plugin.json` and `marketplace.json` is bumped in the same PR.
