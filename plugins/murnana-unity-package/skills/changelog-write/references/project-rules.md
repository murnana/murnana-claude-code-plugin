# Where to look for project-specific changelog rules

Check all of these. Whatever they say overrides this skill's defaults and Keep a Changelog. If two sources conflict, the explicit instruction (first rows) beats what is inferred from the file (last rows).

| Kind | Where to look | What to take from it |
|---|---|---|
| Instructions | `CLAUDE.md` (root, the Unity project, and the package folder), `.claude/rules/*.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.github/CONTRIBUTING.md`, release docs under `docs/` or the package's `Documentation~/` | Changelog location, language, categories, version policy, when to bump, required link format. Follow exactly as written |
| Release tooling | `.releaserc*` / `release` key in `package.json` (semantic-release, often with `semantic-release-upm` or `@semantic-release/changelog`), `.release-please-manifest.json` / `release-please-config.json`, `.changeset/`, `cliff.toml` (git-cliff), `.github/workflows/*.yml` that publish an `upm` branch, push to OpenUPM, or run `npm publish` to a scoped registry | The tool may own the file, the version, or the tags. Don't hand-edit generated sections, and don't bump `version` by hand if the tool does it. For per-change-file setups (`.changeset/`), write the change file the tool expects instead and say so |
| Unity validation | `com.unity.package-validation-suite` in `Packages/manifest.json` or CI | `[Unreleased]` handling at release time (see [unity-package.md](unity-package.md)) |
| Version source | The package's `package.json` (`version`, `unity`, `unityRelease`), existing tags (`v1.2.3`, `1.2.3`, `<name>/1.2.3`, `upm/1.2.3`) | The current version, the tag pattern for link references, and whether the Unity version fields changed |
| The changelog itself | Its preamble and existing entries | Keep a Changelog version, versioning scheme, language, heading/category order, link-reference format, entry style, whether an empty `[Unreleased]` is kept after releases |

Before reading a candidate, Glob for it. Read only the files that exist.
