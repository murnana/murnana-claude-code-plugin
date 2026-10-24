---
name: changelog-write
description: Creates or updates the CHANGELOG.md of a Unity Package Manager (UPM) package following Keep a Changelog and Unity's package versioning rules, and on request cuts a release that also bumps the version in the package's package.json.
when_to_use: Use when the user asks to record changes in a UPM package's changelog, write its release notes, or release a new version of it. A UPM package is a folder with a package.json whose name is reverse-domain (com.company.package) and that has Unity fields such as `unity`. Example requests - "Unity パッケージの CHANGELOG を更新して", "UPM パッケージの変更履歴に追記して", "このパッケージを 1.2.0 でリリースして", "update the UPM package changelog", "release com.acme.foo 1.2.0". Not for npm or other non-Unity packages, Claude Code plugins, a Unity project's own version (bundleVersion), or dependency updates in Packages/manifest.json.
argument-hint: "[changes to record, or \"release\" / a version to cut]"
allowed-tools: Read Grep Glob Edit Write AskUserQuestion WebFetch(domain:raw.githubusercontent.com) WebFetch(domain:keepachangelog.com) WebFetch(domain:docs.unity3d.com) Bash(git status *) Bash(git log *) Bash(git diff *) Bash(git tag -l *) Bash(git tag --list *) Bash(git describe *) Bash(git remote get-url *) Bash(git show *) Bash(gh pr list *) Bash(gh pr view *) Bash(gh issue view *) Bash(uuidgen)
---

# Changelog Write (UPM package)

Write a UPM package's `CHANGELOG.md` entries that tell package users what they can now do and what was fixed. Follow the project's own rules first, then Unity's package rules, then [Keep a Changelog](https://keepachangelog.com/). Add entries to `[Unreleased]` by default. Cut a release section, and update `version` in `package.json`, only when the user asks for one.

## Current state

Run these first. Each one is safe in an empty repository or one without tags:

```sh
git status --short --branch
git describe --tags --abbrev=0 2>/dev/null || true
git remote get-url origin 2>/dev/null || true
```

Treat `$ARGUMENTS` (if any) as a hint about which changes to record. Run Step 8 as well only when the argument or request is just a release request or a version ("release", "バージョンを切って", "1.2.0"). If it's ambiguous (e.g. "fixed release notes"), ask.

For a release request, run Steps 1, 2 and 4, then Step 5. If Step 5 finds changes not yet under `[Unreleased]`, draft and approve them (Steps 6–7) first. Then run Step 8.

Copy this checklist into the response and update it as work proceeds:

```
- [ ] 1 Locate the package and its changelog
- [ ] 2 Discover project rules
- [ ] 3 New file: pick format version, language, versioning; .meta
- [ ] 4 Existing file: read its conventions
- [ ] 5 Collect changes
- [ ] 6 Draft entries
- [ ] 7 Present and get approval → write
- [ ] 8 (Only if asked) Cut a release and update package.json
```

## Step 1: Locate the package and its changelog

- Find UPM packages with the procedure in [references/unity-package.md](references/unity-package.md) ("Finding the package"): a `package.json` with a reverse-domain `name`, outside the build and cache folders listed there.
- **If no UPM package is found, stop.** Tell the user that this skill only handles UPM packages, and edit nothing. Don't fall back to an npm `package.json` or a repository-root changelog.
- The changelog is `CHANGELOG.md` in the same folder as that `package.json`.
- If the repository holds several packages (several `Packages/<name>/`, or `file:` references in `Packages/manifest.json`), pick the one whose paths changed. If several still fit, ask with `AskUserQuestion`, listing each package's `name` and path.
- Read the package's `package.json`: `name`, `version`, `unity`, `unityRelease`, `changelogUrl`. If `changelogUrl` points elsewhere, follow [references/unity-package.md](references/unity-package.md) ("The changelog in the Package Manager") before editing.

## Step 2: Discover project rules (highest priority)

Check the sources in [references/project-rules.md](references/project-rules.md). A project rule overrides anything in this skill and its references: language, categories, version scheme, link format, tag pattern, who owns `version`. Glob for a candidate file before reading it.

## Step 3: New file only — pick format version, language, versioning

1. **Format version**: always start a new changelog on the **latest** Keep a Changelog version. Check it each time with the procedure in [references/keep-a-changelog.md](references/keep-a-changelog.md). Don't rely on memory or on the upstream git tags.
2. **Language**: default to the language of the current conversation. Confirm it with `AskUserQuestion`: offer that language first, then English if the conversation isn't already in English; "Other" covers the rest. Skip the question only if a project rule fixes the language.
3. **Versioning**: follow the project's scheme if there is one. Otherwise use Semantic Versioning 2.0.0 with Unity's package rules ([references/unity-package.md](references/unity-package.md), "Version rules"). The preamble links to `https://semver.org/spec/v2.0.0.html`.
4. Write the header preamble from the reference for that version, translated into the chosen language, then an empty `## [Unreleased]`.
5. **`.meta`**: if `package.json.meta` exists next to `package.json`, also create `CHANGELOG.md.meta` from the template in [references/unity-package.md](references/unity-package.md) ("`.meta` files"). Get the GUID from `uuidgen`, then remove the hyphens and lowercase it by hand. Write the `.meta` before `CHANGELOG.md`, so an open Editor doesn't generate its own first.

## Step 4: Existing file only — read its conventions

- Keep the Keep a Changelog version its preamble links to. Don't upgrade it on its own: the spec says to pin the version followed. If it's older than the latest (check it with the reference's procedure), mention that once and let the user decide.
- Keep its language, heading style, category order, pre-release suffixes and link-reference format, even where they differ from the reference. Note whether released files keep an empty `[Unreleased]`.
- Find the last release. Use the newest `## [x.y.z]` heading and its link reference at the bottom, which often names a tag or commit. Check that it matches `version` in `package.json`; if they disagree, say so. If there is no heading, use the tag from `git describe` above. If neither exists, use the whole history (drop the `<last-release>..` range) or ask. In a repository with no commits, rely on `$ARGUMENTS` and the conversation only.

## Step 5: Collect changes

- Start from `$ARGUMENTS` and the conversation. If the user described the changes, those come first.
- Then read what changed since the last release, scoped to the package folder:
  - `git log --oneline --no-merges <last-release>..HEAD -- <package-path>`
  - `git diff --numstat <last-release>..HEAD -- <package-path>`, then `git diff -U1` only for the files needed to understand a change. Skip `.meta`-only churn unless a `guid:` line changed.
- Find the issue, PR or ticket behind each change: commit trailers and bodies (`git show -s <sha>`), `gh pr list --state all --search <sha>`, `gh pr view <n>`, and any issue it closes. Record the full URL.
- Look for breaking changes directly in the diff, using both checklists: [references/entry-writing.md](references/entry-writing.md) ("Finding breaking changes") and [references/unity-package.md](references/unity-package.md) ("Finding breaking changes in a UPM package"). Commit messages and version numbers often don't mention them. Check `package.json` for changed `unity`, `unityRelease` and `dependencies`.
- Skip anything already listed under `[Unreleased]`.

## Step 6: Draft entries

Follow [references/entry-writing.md](references/entry-writing.md). The core rules:

- Describe what package users can now do, or which symptom was fixed. Don't name internal classes or files. Names users touch themselves are the exception: the public C# API they call, component names, menu paths, Inspector fields, Project Settings entries, sample names, define symbols.
- Write in the past tense.
- Record small changes too, including dependency, minimum Unity version and platform changes.
- End the entry with the URL of the issue, PR or ticket that prompted it, as an inline link. Use permanent URLs only, never a branch.
- For **Fixed**, state the steps that triggered the bug (Play Mode/Edit Mode, platform, Unity version, settings).
- For **Deprecated** and **Removed**, name the API explicitly, plus its replacement, or say there is none.
- For `**Breaking:**`, add the action users must take.
- Start each entry with what the reader recognizes (component, window, menu, API). Merge commits that make up one change. No generic entries ("改善した", "Bug fixes and improvements").
- If a change can't be described as behavior (internal refactor, test-only change, CI config, `.meta` churn), don't invent an entry. List those changes separately and ask with `AskUserQuestion` whether to record each one, and how.

## Step 7: Present and get approval

- Show the target path and the exact lines to add (or the full file, plus any `.meta`, for a new one). Group entries by category, in the file's existing order. If the file has no order yet, use the order its Keep a Changelog version recommends (2.0.0: Security, Removed, Changed, Deprecated, Fixed, Added). Omit empty categories. Within a category, put the entries with the most user impact first, `**Breaking:**` entries before the rest.
- Point out anything uncertain: a guessed category, a missing source URL, an unclear trigger for a fix, a possibly breaking change.
- **Wait for approval**, then Edit (existing file) or Write (new file). This holds even when the skill was started automatically. Don't commit.

## Step 8: Cut a release (only when asked)

Do this only when the user asks for a version or release ("release", "バージョンを切って", "1.2.0 にして"). Never do it as a side effect of adding entries. Follow [references/release.md](references/release.md):

1. Choose the version number: a project rule or the user's number first, then the existing scheme, then Unity's rules. A changed `unity` / `unityRelease` forces at least MINOR.
2. Move `[Unreleased]` into `## [x.y.z] - YYYY-MM-DD`, and keep (or, per project habit, remove) the empty `[Unreleased]`.
3. Update the link references, using the repository's tag pattern.
4. Set `version` in the package's `package.json` to the same number, unless release tooling owns it.

Present the diff of both files and get approval before writing. Don't create tags or commits; list the tag to create and any publish steps.

## Gotchas

- Never paste `git log` subjects as entries. One entry often spans several commits, and many commits don't matter to users.
- Don't read the Keep a Changelog version from the upstream repository's git tags. The tags lag behind the spec (`v1.1.2` was the newest tag when 2.0.0 was published).
- A Fixed entry without reproduction steps ("Fixed a crash") isn't finished. Ask the user if the steps can't be found in the issue, PR or diff.
- Don't infer compatibility from the version bump. Breaking changes often ship in minor and patch releases; judge from the diff. In Unity, a changed `.meta` GUID or an asmdef setting can break users without any C# change.
- A raised minimum Unity version isn't `**Breaking:**`: the Package Manager hides the new version from older Editors. Record it under Changed, bump at least MINOR, and mention it in the release summary.
- If a Unity rule in the references looks outdated, WebFetch the Unity Manual page listed under its Sources and follow the Manual.
- `CHANGELOG.md` belongs at the package root, never in `Documentation~/` or `Samples~/`. Never edit a package under `Library/PackageCache/`.
- Never reuse or change an existing `.meta` GUID. A new `CHANGELOG.md` in a package that tracks `.meta` files needs its own `.meta`, or immutable installs warn on import.
- Unity's Package Validation Suite flags an `[Unreleased]` section at publish and promotion time. Follow the project's habit for whether an empty one stays after a release.
- Dates are `YYYY-MM-DD`, using today's date at release time, not the date of the last commit.

## References

- UPM specifics — finding packages, layout, `changelogUrl`, `.meta` template, Unity version rules, Unity breaking-change checklist, lifecycle suffixes, Validation Suite:
  [references/unity-package.md](references/unity-package.md)
- Checking the latest Keep a Changelog version; snapshot of 2.0.0 (preamble, categories, breaking changes, links, yanked):
  [references/keep-a-changelog.md](references/keep-a-changelog.md)
- How to word each entry, with Unity examples in English and Japanese:
  [references/entry-writing.md](references/entry-writing.md)
- Choosing a version number, cutting a release section and updating `package.json`:
  [references/release.md](references/release.md)
- Where to look for project-specific changelog and release rules:
  [references/project-rules.md](references/project-rules.md)
