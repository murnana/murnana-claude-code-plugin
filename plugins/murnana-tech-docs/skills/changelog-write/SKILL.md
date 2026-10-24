---
name: changelog-write
description: Create or update CHANGELOG.md following the latest Keep a Changelog, and cut a release section when asked.
argument-hint: "[changes to record, or \"release\" / a version to cut]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Edit Write AskUserQuestion WebFetch(domain:raw.githubusercontent.com) WebFetch(domain:keepachangelog.com) Bash(git status *) Bash(git log *) Bash(git diff *) Bash(git tag *) Bash(git describe *) Bash(git remote *) Bash(git show *) Bash(gh pr list *) Bash(gh pr view *) Bash(gh issue view *)
---

# Changelog Write

Write CHANGELOG.md entries that tell users what they can now do and what was fixed. Follow the project's own rules first and [Keep a Changelog](https://keepachangelog.com/) otherwise. Add entries to `[Unreleased]` by default. Cut a release section only when the user asks for one.

## Current state

Run these first. Each one is safe in an empty repository or one without tags:

```sh
git status --short --branch
git describe --tags --abbrev=0 2>/dev/null || true
git remote get-url origin 2>/dev/null || true
```

Treat `$ARGUMENTS` (if any) as a hint about which changes to record. Run Step 8 as well only when the argument is just a release request or a version ("release", "バージョンを切って", "1.2.0"). If it's ambiguous (e.g. "fixed release notes"), ask.

Copy this checklist into your response and update it as you go:

```
- [ ] 1 Locate the target changelog
- [ ] 2 Discover project rules
- [ ] 3 New file: pick format version, language, versioning
- [ ] 4 Existing file: read its conventions
- [ ] 5 Collect changes
- [ ] 6 Draft entries
- [ ] 7 Present and get approval → write
- [ ] 8 (Only if asked) Cut a release
```

## Step 1: Locate the target changelog

- Glob for `**/CHANGELOG.md`, and also `HISTORY*`, `NEWS*`, `RELEASES*`, skipping `node_modules/` and vendored trees.
- In a monorepo, each component may keep its own changelog. Pick the one that matches the changed paths. For example, changes under `plugins/<name>/` may belong to `docs/plugins/<name>/CHANGELOG.md`. Project rules from Step 2 can say where it lives.
- If several candidates still fit, or none exists and the location is unclear, ask with `AskUserQuestion`. A new top-level changelog goes at the repository root as `CHANGELOG.md`.

## Step 2: Discover project rules (highest priority)

Check the sources in [references/project-rules.md](references/project-rules.md). A project rule overrides anything in this skill and its references: language, categories, version scheme, link format, where entries go. Glob for a candidate file before reading it.

## Step 3: New file only — pick format version, language, versioning

1. **Format version**: always start a new changelog on the **latest** Keep a Changelog version. Check it each time with the procedure in [references/keep-a-changelog.md](references/keep-a-changelog.md). Don't rely on memory or on the upstream git tags.
2. **Language**: default to the language of the current conversation. Confirm it with `AskUserQuestion`: offer that language first, then English if the conversation isn't already in English; "Other" covers the rest. Skip the question only if a project rule fixes the language.
3. **Versioning**: follow the project's scheme if there is one. Otherwise use [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).
4. Write the header preamble from the reference for that version, translated into the chosen language, then an empty `## [Unreleased]`.

## Step 4: Existing file only — read its conventions

- Keep the Keep a Changelog version its preamble links to. Don't upgrade it on your own: the spec says to pin the version you follow. If it's older than the latest (check it with the reference's procedure), mention that once and let the user decide.
- Keep its language, heading style, category order and link-reference format, even where they differ from the reference.
- Find the last release. Use the newest `## [x.y.z]` heading and its link reference at the bottom, which often names a tag or commit. If there is none, use the tag from `git describe` above. If neither exists, use the whole history (drop the `<last-release>..` range) or ask. In a repository with no commits, rely on `$ARGUMENTS` and the conversation only.

## Step 5: Collect changes

- Start from `$ARGUMENTS` and the conversation. If the user described the changes, those come first.
- Then read what changed since the last release, scoped to the component's paths:
  - `git log --oneline --no-merges <last-release>..HEAD -- <paths>`
  - `git diff --numstat <last-release>..HEAD -- <paths>`, then `git diff -U1` only for the files you need to understand.
- Find the issue, PR or ticket behind each change: commit trailers and bodies (`git show -s <sha>`), `gh pr list --state all --search <sha>`, `gh pr view <n>`, and any issue it closes. Record the full URL.
- Look for breaking changes yourself, using the checklist in [references/entry-writing.md](references/entry-writing.md) ("Finding breaking changes"). Commit messages and version numbers often don't mention them.
- Skip anything already listed under `[Unreleased]`.

## Step 6: Draft entries

Follow [references/entry-writing.md](references/entry-writing.md). The core rules:

- Describe what users can now do, or which symptom was fixed. Don't describe API, function or file names. Names users type themselves (CLI flags, config keys, environment variables) are the exception.
- Write in the past tense.
- Record small changes too, including configuration, dependency and minimum-runtime changes users can notice.
- End the entry with the URL of the issue, PR or ticket that prompted it, as an inline link. Use permanent URLs only, never a branch.
- For **Fixed**, state the steps that triggered the bug.
- For **Deprecated** and **Removed**, name the API explicitly, plus its replacement, or say there is none.
- For `**Breaking:**`, add the action users must take.
- Start each entry with what the reader recognizes (feature, command, area). Merge commits that make up one change. No generic entries ("改善した", "Bug fixes and improvements").
- If a change can't be described as behavior (internal refactor, test-only change, CI config), don't invent an entry. List those changes separately and ask with `AskUserQuestion` whether to record each one, and how.

## Step 7: Present and get approval

- Show the target path and the exact lines to add (or the full file for a new one). Group entries by category, in the file's existing order. If the file has no order yet, use the order its Keep a Changelog version recommends (2.0.0: Security, Removed, Changed, Deprecated, Fixed, Added). Omit empty categories. Within a category, put the entries with the most user impact first, `**Breaking:**` entries before the rest.
- Point out anything uncertain: a guessed category, a missing source URL, an unclear trigger for a fix.
- **Wait for approval**, then Edit (existing file) or Write (new file). Don't commit.

## Step 8: Cut a release (only when asked)

Do this only when the user asks for a version or release ("release", "バージョンを切って", "1.2.0 にして"). Never do it as a side effect of adding entries. Follow [references/release.md](references/release.md): choose the version number, move `[Unreleased]` into `## [x.y.z] - YYYY-MM-DD`, keep a fresh empty `[Unreleased]`, and update the link references. Present the result and get approval before writing.

## Gotchas

- Never paste `git log` subjects as entries. One entry often spans several commits, and many commits don't matter to users.
- Don't read the Keep a Changelog version from the upstream repository's git tags. The tags lag behind the spec (`v1.1.2` was the newest tag when 2.0.0 was published).
- A Fixed entry without reproduction steps ("Fixed a crash") isn't finished. Ask the user if the steps can't be found in the issue, PR or diff.
- Code names belong only in Deprecated, Removed and `**Breaking:**` entries, where readers need them to find the affected code. Names users type themselves (flags, config keys) may appear anywhere, with what they do.
- Don't infer compatibility from the version bump. Breaking changes often ship in minor and patch releases; judge from the diff.
- Dates are `YYYY-MM-DD`, using today's date at release time, not the date of the last commit.

## References

- Checking the latest Keep a Changelog version; snapshot of 2.0.0 (preamble, categories, breaking changes, links, yanked):
  [references/keep-a-changelog.md](references/keep-a-changelog.md)
- How to word each entry, with good and bad examples in English and Japanese:
  [references/entry-writing.md](references/entry-writing.md)
- Choosing a version number and cutting a release section:
  [references/release.md](references/release.md)
- Where to look for project-specific changelog rules:
  [references/project-rules.md](references/project-rules.md)
