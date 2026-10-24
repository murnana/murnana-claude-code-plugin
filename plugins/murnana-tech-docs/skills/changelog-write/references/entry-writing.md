# Writing entries

How to word each changelog entry. These rules come from the plugin owner. Where they differ from Keep a Changelog (source links), they win. A project rule overrides both.

## Contents

- The rules
- Finding breaking changes
- Per-type guidance
- Examples
- When to ask instead of writing

## The rules

1. **Describe behavior, not code.** Say what users can now do, or which symptom no longer occurs. Leave out function, class, endpoint and file names. The reader is a user deciding whether to upgrade, not a reviewer reading the diff.
   - **Exception: names users type themselves.** CLI commands and flags, configuration keys, environment variables and slash commands are the user interface. Name them in backticks, because that's what users search for. Still say what the change lets them do: "Added `--dry-run` to preview the changes without applying them", not just "Added `--dry-run`".
2. **Use the past tense.** English: start with a past-tense verb ("Added…", "Changed…", "Fixed…", "Deprecated…"). Japanese: end with 「〜した」 or 「〜できるようにした」, not 「〜する」 or a bare noun phrase.
3. **Record small changes too.** A wording fix in an error message or a changed default counts if users can notice it. Changes to configuration, to dependencies that users install or configure, and to the minimum supported runtime or OS are user-visible as well: integrators need them. The only filter is "can this be described as behavior?" If it can't, see "When to ask instead of writing".
4. **Link the source.** If an issue, PR, ticket or discussion prompted the change, end the entry with its full URL as an inline Markdown link: `([#18](https://github.com/owner/repo/pull/18))`. Use the ticket key as the link text for non-GitHub trackers (`([PROJ-123](https://…))`). Link several sources with commas. If no source can be found, leave the link out and say so when presenting the draft. Never invent a URL.
   - Use only permanent URLs: issue, PR and ticket pages, tags, commit SHAs. Never link a branch (`tree/main/…`, `blob/feature-x/…`): its content changes or disappears. Broken links are one of the most common complaints about release notes.
5. **For bugs, state the trigger.** A Fixed entry says which steps or conditions produced the bug and what went wrong. "Fixed a crash" isn't enough.
6. **Exception: Deprecated, Removed and `**Breaking:**` entries name the API.** Here readers need the exact name to find affected code. Write the API name in backticks, and the replacement if one exists. If there is no replacement, say so explicitly ("There is no replacement."), so readers don't go looking for one. Also say which version will remove a deprecated API, if it's known.
7. **Say what users must do.** When existing use stops working, a `**Breaking:**` entry ends with the action users must take ("Move your file to the new location before upgrading."). Link to a migration guide when the steps don't fit in a sentence.
8. **Lead with what the reader recognizes.** Readers scan the first words of each line. Start with the feature, screen, command or area users know. Put the most important information first.
9. **Write plainly.** Many readers aren't native speakers or experts. Use one entry per change, merging commits that make up one change, and one or two sentences per entry. When a Fixed entry gets long, split it into two sentences: the trigger, then the symptom that no longer occurs.
10. **No generic entries.** "Bug fixes and improvements", "Improved performance", 「軽微な修正」 and 「改善した」 tell the reader nothing. Say what improved and where, or ask (see below).

## Finding breaking changes

Breaking changes are left out of release notes far more often than they are written wrong. Don't rely on commit messages or the version number to flag them: many breaking changes ship in minor and patch releases. Check the diff for:

- removed or renamed commands, options, flags, configuration keys, environment variables or public APIs;
- changed defaults, or changed output formats that scripts may parse;
- changed file locations, file formats or configuration schemas;
- a raised minimum version of a runtime, OS, or required dependency;
- behavior that existing users rely on, even if it was undocumented.

Mark each one `**Breaking:**` and add the action users must take (rule 7). If you can't tell whether the project treats an interface as stable, ask.

## Per-type guidance

Within each type, put the entries with the most user impact first.

| Type | What to write |
|---|---|
| Security | CVE ID first if there is one; what an attacker could do, in a few words; link to the advisory |
| Removed | The removed API/feature by name; what to use instead, or that there is no replacement; `**Breaking:**` and the required action if users relied on it |
| Changed | Old behavior → new behavior, from the user's view; `**Breaking:**` and the required action when existing use stops working |
| Deprecated | The API/feature by name; its replacement, or that there is none; the planned removal version if known |
| Fixed | The steps or conditions that triggered it, and the wrong result that no longer occurs |
| Added | What users can now do, and where (screen, command, option) in user-facing terms |

Changed or Fixed? If the old behavior was a bug, use Fixed. If it worked as designed and the design changed, use Changed.

## Examples

### Added

```markdown
<!-- Bad: names the code, not the capability -->
- Added `exportCsv()` to `ReportService`.

<!-- Good -->
- Added CSV download to the report screen. ([#42](https://github.com/acme/app/issues/42))
```

```markdown
<!-- Bad: present tense, only the flag name -->
- `--dry-run` フラグを追加する

<!-- Good: the flag is something users type, so name it, and say what it does -->
- `--dry-run` を付けると、実際には実行せず、実行される内容だけを確認できるようにした ([#57](https://github.com/acme/cli/pull/57))
```

### Fixed

```markdown
<!-- Bad: no trigger, names the code -->
- Fixed null check in `SessionManager`.

<!-- Good -->
- Fixed the app signing users out when they reopened it after more than 24 hours in the background. ([#88](https://github.com/acme/app/issues/88))
```

```markdown
<!-- Bad -->
- 空リポジトリ対応

<!-- Good: starts with what the user recognizes; trigger and symptom in two sentences -->
- commit スキル: コミットが 1 件もないリポジトリで起動すると、エラーになって起動できなかった。この不具合を修正した ([#7](https://github.com/acme/tools/issues/7))
```

### Changed

```markdown
- Changed search results to sort by relevance instead of date. ([#120](https://github.com/acme/app/pull/120))
- **Breaking:** Moved the config file from `~/.acme/` to `~/.config/acme/`. Move your file to the new location before upgrading. ([#131](https://github.com/acme/app/pull/131))
- **Breaking:** Raised the minimum supported Node.js version from 18 to 20. Upgrade Node.js before updating. ([#140](https://github.com/acme/cli/pull/140))
```

```markdown
<!-- Bad: generic -->
- パフォーマンスを改善した

<!-- Good -->
- 1,000 件を超えるプロジェクトで、一覧画面の表示が速くなるようにした（約 5 秒から 1 秒未満） ([#145](https://github.com/acme/app/pull/145))
```

### Deprecated and Removed (API names required)

```markdown
### Deprecated

- Deprecated `client.fetchAll()`; it will be removed in 3.0.0. Use `client.list()` with pagination instead. ([#150](https://github.com/acme/sdk/issues/150))

### Removed

- **Breaking:** Removed the `--legacy-output` option. Use `--format=v1` for the old output format. ([#151](https://github.com/acme/sdk/pull/151))
- **Breaking:** Removed the `sync --watch` mode. There is no replacement; run `sync` from your own file watcher instead. ([#152](https://github.com/acme/sdk/pull/152))
```

```markdown
### Deprecated

- `Foo.load()` を非推奨にした（3.0.0 で削除予定）。移行先として `Foo.open()` を用意した ([#160](https://github.com/acme/sdk/issues/160))
- `Foo.legacyMode` を非推奨にした（3.0.0 で削除予定）。移行先はない ([#161](https://github.com/acme/sdk/issues/161))
```

### Security

```markdown
- CVE-2026-12345: Fixed a path traversal that let uploaded file names write outside the upload directory. See the [advisory](https://github.com/acme/app/security/advisories/GHSA-xxxx-xxxx-xxxx).
```

## When to ask instead of writing

Some changes can't be described as behavior: an internal refactor, test-only changes, CI configuration, code formatting, a dependency bump with no visible effect. Don't make up a user-facing effect for them, and don't silently drop them either. List them separately when presenting the draft and ask with `AskUserQuestion` for each group:

- leave it out (the usual answer for refactors and tests), or
- record it, with wording the user supplies or approves (for example a dependency bump that changes the minimum supported runtime, which is really a Changed entry).

Also ask when:

- the trigger of a fix can't be found in the issue, PR, commit or diff;
- a change could be either Changed or Fixed, and the issue doesn't say whether the old behavior was intended;
- a change might be breaking, but you can't tell which interface the project keeps stable;
- the only wording you can find is generic ("improved performance"), and the diff doesn't show what improved or by how much.
