# Keep a Changelog

How to find the latest version of the format, and a snapshot of 2.0.0 to fall back on.

## Contents

- Checking the latest version
- Snapshot: 2.0.0
  - Header preamble
  - Types of changes and their order
  - Breaking changes
  - Naming the part a change touches
  - Structuring a release
  - Links
  - Yanked releases and rewriting
  - Monorepos and large files
  - What not to do

## Checking the latest version

Run this every time you start a new changelog, and when an existing file links an older version than the snapshot below (to tell the user whether it's behind). The format keeps changing, and the upstream git tags lag behind the spec: `v1.1.2` was still the newest tag after 2.0.0 shipped. Don't read the version from tags or from memory.

1. WebFetch `https://raw.githubusercontent.com/olivierlacan/keep-a-changelog/main/CHANGELOG.md`. That is the changelog of keepachangelog.com itself. The first `## [x.y.z] - YYYY-MM-DD` heading below `[Unreleased]` is the latest released spec version.
2. Read that version's spec from its source: `https://raw.githubusercontent.com/olivierlacan/keep-a-changelog/main/source/en/<x.y.z>/index.html.md`. The rendered page is `https://keepachangelog.com/en/<x.y.z>/`.
3. If the latest version is newer than the 2.0.0 snapshot below, read the spec and that version's changelog section first. Apply what changed, and tell the user which version you used.
4. If both fetches fail, use the snapshot below. Tell the user that the latest version couldn't be checked and that 2.0.0 was used.

## Snapshot: 2.0.0

Released 2026-06-07. It changed the guidance, not the format: the six types, `YYYY-MM-DD` dates, `Unreleased` and `[YANKED]` are the same as in 1.1.0, so 1.1.0 files stay valid.

### Header preamble

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

- Pin the Keep a Changelog link to the version you follow.
- The second link names the versioning scheme. Replace it if the project uses CalVer, a plain number, or dates.
- Translate the preamble when the changelog isn't in English. Keep both link URLs unchanged. A Japanese example from murnana-claude-code-plugin:

  ```markdown
  # 変更履歴

  このプラグインの注目すべき変更はすべてこのファイルに記録します。

  フォーマットは [Keep a Changelog](https://keepachangelog.com/en/2.0.0/) に基づいており、
  このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。
  ```

- Moving an existing file to a newer format version doesn't mean rewriting its history. Keep past entries. Apply the new conventions from the next release, update the version in the link, and say so in that release's summary line. Do this only when the user asks for it.

### Types of changes and their order

2.0.0 lists them in order of urgency, so readers notice what they must act on:

| Type | Use for |
|---|---|
| `Security` | Vulnerabilities |
| `Removed` | Features that are now removed |
| `Changed` | Existing behavior that worked as intended and now works differently |
| `Deprecated` | Features that will be removed soon |
| `Fixed` | Behavior that was wrong and is now correct |
| `Added` | New features |

- Keep the order consistent across releases, and omit empty sections. If a file already uses another order (for example 1.1.0's Added, Changed, Deprecated, Removed, Fixed, Security), keep that order.
- Changed or Fixed? Ask whether the old behavior was a bug. If yes, it's Fixed. If it was intentional and you're changing it, it's Changed.
- Security entries lead with the CVE ID when there is one, and link to the advisory: `- CVE-2024-12345: Fixed an out-of-bounds read when parsing malformed input. See the [advisory](https://…).`
- Keep to the six types. A performance gain goes under Changed. Internal or housekeeping changes are rarely notable.
- Dependencies aren't a type. Describe the effect under the right type, or leave it out if users aren't affected.
- Known issues go on the affected version or in the tracker. They move to Fixed once they're fixed.
- Deprecate before removing: mark a feature `Deprecated` in one release, and `Removed` only in a later one. Say which version will remove it.

### Breaking changes

- Keep them in their type (usually Changed or Removed) and prefix the entry with `**Breaking:**`. Don't collect them into a separate section.
- Say which interface breaks: CLI, library API, protocol, file format, or configuration schema.
- A short upgrade note can sit in the entry. Link to a migration guide when the steps are long.

```markdown
- **Breaking:** Changed `parse()` to return a result object instead of raising.
```

### Naming the part a change touches

This is optional. In a project with distinct parts, an entry can start with the area name (`- CLI: …`). When several entries share an area, nest them under a level-4 heading inside the type. Keep area names few and consistent.

### Structuring a release

- Keep `## [Unreleased]` at the top for upcoming changes.
- A version heading is `## [x.y.z] - YYYY-MM-DD`. The date follows ISO 8601.
- A version may open with a one- or two-sentence summary before its typed sections. This is optional.
- At release time, rename `Unreleased` to the new version in the heading and its link, then add a fresh empty `Unreleased`.
- On a project without a changelog, start by recording changes from now on. Reconstructing past releases is optional.
- For projects released continuously without version numbers, keep dated entries under `Unreleased`.

### Links

Version headings are reference links. They are resolved at the bottom of the file:

```markdown
[Unreleased]: https://github.com/your/project/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/your/project/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/your/project/releases/tag/v1.0.0
```

2.0.0 treats issue and PR links as optional and suggests reference-style links. **This skill instead requires the source URL, inline at the end of each entry.** See [entry-writing.md](entry-writing.md). A project rule overrides both.

### Yanked releases and rewriting

- Keep yanked releases in the file and mark them: `## [0.0.5] - 2014-12-13 [YANKED]`.
- Improving old entries after release (a forgotten entry, an unrecorded breaking change) is fine. Consider noting the date of the edit.

### Monorepos and large files

- Unrelated projects in one repository each keep their own changelog.
- One product made of several parts may keep a changelog per component, plus one central summary.
- One long file is fine. If you archive old versions, link the files both ways and never delete entries.
- If `[Unreleased]` causes frequent merge conflicts, use `merge=union` in `.gitattributes`. Very busy projects can use per-change files in `changelog.d/`. Use these only if the project already does.

### What not to do

- Don't use a commit list as a changelog.
- Don't skip deprecations, removals or breaking changes.
- Don't record only some notable changes. Readers treat the file as complete.
- Machines can draft, humans curate: a drafted changelog must be read and approved by a person before it's published.
