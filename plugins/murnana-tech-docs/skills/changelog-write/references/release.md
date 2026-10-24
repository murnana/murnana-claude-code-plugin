# Cutting a release

Read this only when the user asked for a version or a release. Adding entries never cuts a release by itself.

## 1. Choose the version number

Use the first source that applies:

1. **Project rule.** A version policy in `CLAUDE.md`, `.claude/rules/`, `CONTRIBUTING.md` and so on (see [project-rules.md](project-rules.md)), or a version the user named.
2. **The existing scheme.** If past headings use CalVer (`2026.10.0`), dates, or plain numbers, continue that pattern. The preamble's versioning link usually says which one.
3. **Semantic Versioning 2.0.0** (https://semver.org/), deciding from the entries under `[Unreleased]`:

| Entries contain | Bump | Example |
|---|---|---|
| A `**Breaking:**` entry, or a Removed entry for something users relied on | MAJOR (reset minor and patch to 0) | 1.4.2 → 2.0.0 |
| Added, a non-breaking Changed, or Deprecated | MINOR (reset patch to 0) | 1.4.2 → 1.5.0 |
| Only Fixed or Security, with no new behavior | PATCH | 1.4.2 → 1.4.3 |

- While the major version is `0` (`0.y.z`), anything may change at any time. A breaking change may go in a MINOR bump. Follow the project's habit if it has one.
- Don't prefix the version with `v` in the heading, even when tags use `v1.2.3`.
- If the current version is unclear (no headings, no tags), ask the user.

Present the proposed number with a one-line reason, for example "1.5.0: adds two features, no breaking changes". Let the user confirm or override it.

## 2. Rewrite the file

1. Insert the new heading `## [x.y.z] - YYYY-MM-DD` directly below `## [Unreleased]`, using **today's** date. Keep the YANKED marker convention if the project has one.
2. Move every entry from `[Unreleased]` into it, keeping category order and wording.
3. Add a one- or two-sentence summary right under the version heading when the release contains a `**Breaking:**` or Security entry. Say what readers must act on first, for example "Contains one breaking change to the config file location; see Changed." It's optional when the release only has a theme, and skip it otherwise.
4. Leave `## [Unreleased]` in place and empty.
5. If `[Unreleased]` was already empty, stop and ask. An empty release is almost always a mistake.

## 3. Update the link references

Match the format already at the bottom of the file. Typical patterns:

- **Tag compare (Keep a Changelog default):**

  ```markdown
  [unreleased]: https://github.com/owner/repo/compare/v1.5.0...HEAD
  [1.5.0]: https://github.com/owner/repo/compare/v1.4.2...v1.5.0
  ```

  Point `[unreleased]` at the new tag, and add the new version comparing it with the previous one. The tag usually doesn't exist yet. Use the name it will get, and remind the user to create it.

- **Commit-based (repositories without tags, such as murnana-claude-code-plugin):** Point the new version's link at the release commit, and `[unreleased]` at a compare from that commit to `main`/`HEAD`. If the release commit doesn't exist yet, use the current `HEAD` short SHA (`git log -1 --format=%h`) and say that the link should be checked after committing.

- **No link references yet:** build them from `git remote get-url origin`. Convert SSH remotes (`git@github.com:owner/repo.git`) to `https://github.com/owner/repo`. The oldest version links to its tag (`/releases/tag/<tag>`). For non-GitHub hosts, use that host's compare URL format, or ask.

Keep the label case the file already uses (`[unreleased]` vs `[Unreleased]`).

## 4. Hand off

- Don't edit version fields in other files (`package.json`, `plugin.json`, `Cargo.toml`, …). Don't create tags or commits either. List what the project's rules say must also change, and leave it to the user or the relevant skill.
- Show the full diff of the changelog and wait for approval before writing.
