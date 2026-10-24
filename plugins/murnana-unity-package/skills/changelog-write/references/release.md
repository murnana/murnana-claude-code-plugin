# Cutting a release

Read this only when the user asked for a version or a release. Adding entries never cuts a release by itself.

A release changes two files together: the package's `CHANGELOG.md` and the `version` in its `package.json`. They must name the same version.

## 1. Choose the version number

Use the first source that applies:

1. **Project rule.** A version policy in `CLAUDE.md`, `.claude/rules/`, `CONTRIBUTING.md` and so on (see [project-rules.md](project-rules.md)), or a version the user named.
2. **The existing scheme.** Continue the pattern of past headings and of `package.json`, including pre-release suffixes (`-exp.N`, `-pre.N`) if the package uses them.
3. **Unity's SemVer rules**, deciding from the entries under `[Unreleased]` and the diff. Use the table in [unity-package.md](unity-package.md) ("Version rules"). In short:

| Entries contain | Bump | Example |
|---|---|---|
| A `**Breaking:**` entry, or a Removed entry for something users relied on | MAJOR (reset minor and patch to 0) | 1.4.2 → 2.0.0 |
| Added; Deprecated; a Changed entry that adds or alters behavior users use; a changed `unity` / `unityRelease` | MINOR (reset patch to 0) | 1.4.2 → 1.5.0 |
| Only Fixed, Security, or behavior-preserving Changed (performance, message wording) | PATCH | 1.4.2 → 1.4.3 |

- Compare `unity` and `unityRelease` in `package.json` with the last release (`git diff <last-release>..HEAD -- <package>/package.json`). If either changed, the bump is at least MINOR, even when the entries are only fixes.
- While the major version is `0` (`0.y.z`), anything may change at any time. A breaking change may go in a MINOR bump. Follow the project's habit if it has one.
- Add a pre-release suffix only if the project already uses one or the user asks. When continuing a series, increment its number (`1.3.0-pre.1` → `1.3.0-pre.2`). The release after a pre-release drops the suffix (`1.3.0-pre.2` → `1.3.0`).
- Don't prefix the version with `v`, in the heading or in `package.json`, even when tags use `v1.2.3`.
- If the current version is unclear (`package.json` and the changelog disagree, no headings), ask the user.

Present the proposed number with a one-line reason, for example "1.5.0: adds two features and raises `unity` to 6000.0". Let the user confirm or override it.

## 2. Rewrite the changelog

1. Insert the new heading `## [x.y.z] - YYYY-MM-DD` directly below `## [Unreleased]`, using **today's** date. Keep the YANKED marker convention if the project has one.
2. Move every entry from `[Unreleased]` into it, keeping category order and wording.
3. Add a one- or two-sentence summary right under the version heading when the release contains a `**Breaking:**` or Security entry, or raises the minimum Unity version. Say what readers must act on first, for example "Requires Unity 6000.0 or later; see Changed." Skip it otherwise.
4. Leave `## [Unreleased]` in place and empty, unless the project removes it at release time (Package Validation Suite, or past releases that never kept an empty one; see [unity-package.md](unity-package.md)). In that case remove it and say so.
5. If `[Unreleased]` was already empty, stop and ask. An empty release is almost always a mistake.

## 3. Update the link references

Match the format already at the bottom of the file. Typical patterns:

- **Tag compare (Keep a Changelog default):**

  ```markdown
  [unreleased]: https://github.com/owner/repo/compare/v1.5.0...HEAD
  [1.5.0]: https://github.com/owner/repo/compare/v1.4.2...v1.5.0
  ```

  Point `[unreleased]` at the new tag, and add the new version comparing it with the previous one. Use the tag pattern the repository already uses (`v1.5.0`, `1.5.0`, `com.company.pkg/1.5.0`, `upm/1.5.0`). The tag usually doesn't exist yet. Use the name it will get, and remind the user to create it.

- **Commit-based (repositories without tags):** Point the new version's link at the release commit, and `[unreleased]` at a compare from that commit to the default branch. If the release commit doesn't exist yet, use the current `HEAD` short SHA (`git log -1 --format=%h`) and say that the link should be checked after committing.

- **No link references yet:** build them from `git remote get-url origin`. Convert SSH remotes (`git@github.com:owner/repo.git`) to `https://github.com/owner/repo`. The oldest version links to its tag (`/releases/tag/<tag>`). For non-GitHub hosts, use that host's compare URL format, or ask.

Keep the label case the file already uses (`[unreleased]` vs `[Unreleased]`).

## 4. Update `package.json`

- Change only the `version` value of the package's own `package.json`. Keep the file's formatting (indentation, key order, trailing newline); use Edit on that one line.
- Skip this step if release tooling owns the version (semantic-release, release-please, changesets). Say that the tool will set it.
- If `package.json` has an `_upm` object with a `changelog` field (some packages carry release notes there for the Package Manager), tell the user and propose replacing its text with the new release's entries, for approval with the rest.
- Don't touch `dependencies` of other packages, `Packages/manifest.json`, or `packages-lock.json`.

## 5. Hand off

- Show the full diff of both files and wait for approval before writing.
- Don't create tags or commits. List what else the release needs: the tag to create (with its name), the `changelogUrl` page if it points elsewhere, and any publish step the project's rules or CI describe.
