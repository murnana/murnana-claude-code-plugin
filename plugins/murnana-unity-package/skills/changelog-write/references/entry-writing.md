# Writing entries

How to word each changelog entry. These rules come from the plugin owner. Where they differ from Keep a Changelog (source links), they win. A project rule overrides both.

## Contents

- The rules
- Finding breaking changes
- Per-type guidance
- Examples
- When to ask instead of writing

## The rules

1. **Describe behavior, not code.** Say what users can now do, or which symptom no longer occurs. Leave out internal class, method and file names. The reader is a developer using the package, deciding whether to upgrade, not a reviewer reading the diff.
   - **Exception: names users touch themselves.** In a UPM package these are the user interface, so name them in backticks, because that's what users search for:
     - the package's public C# API that users call from their own scripts (types, members, attributes, events);
     - component names in **Add Component**, Inspector fields, menu paths (`Tools > Foo > Bake`), `Create` menu assets, Project Settings and Preferences entries;
     - sample names shown in the Package Manager, scripting define symbols, assembly names users reference from their asmdef.

     Still say what the change lets them do: "Added `FooSettings.Timeout` to stop waiting after the given number of seconds", not just "Added `FooSettings.Timeout`". `internal` and `private` types never appear.
2. **Use the past tense.** English: start with a past-tense verb ("Added…", "Changed…", "Fixed…", "Deprecated…"). Japanese: end with 「〜した」 or 「〜できるようにした」, not 「〜する」 or a bare noun phrase.
3. **Record small changes too.** A wording fix in a console message or a changed Inspector default counts if users can notice it. Changes to package dependencies, to the minimum Unity version (`unity` / `unityRelease`), and to supported platforms or render pipelines are user-visible as well: integrators need them. The only filter is "can this be described as behavior?" If it can't, see "When to ask instead of writing".
4. **Link the source.** If an issue, PR, ticket or discussion prompted the change, end the entry with its full URL as an inline Markdown link: `([#18](https://github.com/owner/repo/pull/18))`. Use the ticket key as the link text for non-GitHub trackers (`([PROJ-123](https://…))`). Link several sources with commas. If no source can be found, leave the link out and say so when presenting the draft. Never invent a URL.
   - Use only permanent URLs: issue, PR and ticket pages, tags, commit SHAs. Never link a branch (`tree/main/…`, `blob/feature-x/…`): its content changes or disappears. Broken links are one of the most common complaints about release notes.
5. **For bugs, state the trigger.** A Fixed entry says which steps or conditions produced the bug and what went wrong: Play Mode or Edit Mode, the platform or Unity version, the domain reload setting, the Inspector action. "Fixed a crash" isn't enough.
6. **Exception: Deprecated, Removed and `**Breaking:**` entries name the API.** Here readers need the exact name to find affected code. Write the API name in backticks, and the replacement if one exists. If there is no replacement, say so explicitly ("There is no replacement."), so readers don't go looking for one. Also say which version will remove a deprecated API, if it's known.
7. **Say what users must do.** When existing use stops working, a `**Breaking:**` entry ends with the action users must take ("Re-assign the field on existing prefabs.", "Upgrade to Unity 6000.0 before updating."). Link to a migration guide when the steps don't fit in a sentence.
8. **Lead with what the reader recognizes.** Readers scan the first words of each line. Start with the component, window, menu, API or area users know. Put the most important information first.
9. **Write plainly.** Many readers aren't native speakers or experts. Use one entry per change, merging commits that make up one change, and one or two sentences per entry. When a Fixed entry gets long, split it into two sentences: the trigger, then the symptom that no longer occurs.
10. **No generic entries.** "Bug fixes and improvements", "Improved performance", 「軽微な修正」 and 「改善した」 tell the reader nothing. Say what improved and where, or ask (see below).

## Finding breaking changes

Breaking changes are left out of release notes far more often than they are written wrong. Don't rely on commit messages or the version number to flag them: many breaking changes ship in minor and patch releases. Check the diff for:

- removed or renamed public APIs, components, menu items, settings or define symbols;
- changed defaults, or changed serialized data formats;
- changed file locations or sample paths;
- a raised or added package dependency that users' code or assets don't work with;
- behavior that existing users rely on, even if it was undocumented.

Then go through the Unity-specific checklist in [unity-package.md](unity-package.md) ("Finding breaking changes in a UPM package"): asmdef settings, `.meta` GUIDs, serialized field renames. A raised minimum Unity version is recorded under Changed without `**Breaking:**`; the reference explains why.

Mark each one `**Breaking:**` and add the action users must take (rule 7). If it's unclear whether the project treats an interface as stable, ask.

## Per-type guidance

Within each type, put the entries with the most user impact first.

| Type | What to write |
|---|---|
| Security | CVE ID first if there is one; what an attacker could do, in a few words; link to the advisory |
| Removed | The removed API/feature by name; what to use instead, or that there is no replacement; `**Breaking:**` and the required action if users relied on it |
| Changed | Old behavior → new behavior, from the user's view; `**Breaking:**` and the required action when existing use stops working |
| Deprecated | The API/feature by name (usually now `[Obsolete]`); its replacement, or that there is none; the planned removal version if known |
| Fixed | The steps or conditions that triggered it, and the wrong result that no longer occurs |
| Added | What users can now do, and where (component, window, menu, API) in user-facing terms |

Changed or Fixed? If the old behavior was a bug, use Fixed. If it worked as designed and the design changed, use Changed.

## Examples

### Added

```markdown
<!-- Bad: names an internal class -->
- Added `CsvExporter` to `ReportBuilder`.

<!-- Good: says what users can do, and where -->
- Added CSV export to the `Window > Analysis > Report` window. ([#42](https://github.com/acme/report-tools/issues/42))
```

```markdown
<!-- Bad: present tense, only the API name -->
- `SaveSystem.SaveAsync()` を追加する

<!-- Good: the API is what users call, so name it, and say what it does -->
- `SaveSystem.SaveAsync()` を使うと、メインスレッドを止めずにセーブデータを書き込めるようにした ([#57](https://github.com/acme/save-system/pull/57))
```

```markdown
- Added the "URP Setup" sample. Import it from the Package Manager to see the effect working with the Universal Render Pipeline. ([#63](https://github.com/acme/fx/pull/63))
```

### Fixed

```markdown
<!-- Bad: no trigger, names the code -->
- Fixed null check in `PoolManager`.

<!-- Good -->
- Fixed `ObjectPool` returning destroyed objects after leaving Play Mode with domain reload disabled. ([#88](https://github.com/acme/pooling/issues/88))
```

```markdown
<!-- Bad -->
- Inspector 修正

<!-- Good: starts with what the user recognizes; trigger and symptom in two sentences -->
- `FootstepAudio` コンポーネント: Inspector で `Clips` を空にしたまま再生すると、コンソールに例外が出続けていた。この不具合を修正した ([#7](https://github.com/acme/audio-kit/issues/7))
```

### Changed

```markdown
- Changed `Tools > Atlas > Pack` to skip textures that haven't changed since the last pack. ([#120](https://github.com/acme/atlas/pull/120))
- Raised the minimum Unity version from 2022.3 to 6000.0. Projects on older Editors stay on 1.x. ([#140](https://github.com/acme/atlas/pull/140))
- **Breaking:** Renamed the serialized field `speed` to `moveSpeed` on `PlayerMover` without migrating saved values. Re-enter the value on existing scenes and prefabs after updating. ([#131](https://github.com/acme/movement/pull/131))
- **Breaking:** Turned off **Auto Referenced** on the `Acme.Movement` assembly. Reference `Acme.Movement` from your own asmdef; move scripts that have no asmdef into one first. ([#133](https://github.com/acme/movement/pull/133))
```

```markdown
<!-- Bad: generic -->
- パフォーマンスを改善した

<!-- Good -->
- 1,000 個を超えるオブジェクトを持つシーンで、`Tools > Atlas > Pack` が速く終わるようにした（約 30 秒から 3 秒） ([#145](https://github.com/acme/atlas/pull/145))
```

### Deprecated and Removed (API names required)

```markdown
### Deprecated

- Deprecated `SaveSystem.Save()`; it will be removed in 3.0.0. Use `SaveSystem.SaveAsync()` instead. ([#150](https://github.com/acme/save-system/issues/150))

### Removed

- **Breaking:** Removed the `ACME_LEGACY_INPUT` scripting define symbol. Use the Input System backend, which is now always on. ([#151](https://github.com/acme/input-kit/pull/151))
- **Breaking:** Removed the `Tools > Acme > Rebuild Cache` menu item. There is no replacement; the cache now rebuilds on domain reload. ([#152](https://github.com/acme/input-kit/pull/152))
```

```markdown
### Deprecated

- `SaveSlot.Load()` を非推奨にした（3.0.0 で削除予定）。代わりに `SaveSlot.LoadAsync()` を使う ([#160](https://github.com/acme/save-system/issues/160))
- `SaveSettings.LegacyFormat` を非推奨にした（3.0.0 で削除予定）。移行先はない ([#161](https://github.com/acme/save-system/issues/161))
```

### Security

```markdown
- CVE-2026-12345: Fixed save file loading that let a crafted file write outside `Application.persistentDataPath`. See the [advisory](https://github.com/acme/save-system/security/advisories/GHSA-xxxx-xxxx-xxxx).
```

## When to ask instead of writing

Some changes can't be described as behavior: an internal refactor, test-only changes (`Tests/`), CI configuration, code formatting, `.meta` churn from re-importing, a dependency bump with no visible effect. Don't make up a user-facing effect for them, and don't silently drop them either. List them separately when presenting the draft and ask with `AskUserQuestion` for each group:

- leave it out (the usual answer for refactors and tests), or
- record it, with wording the user supplies or approves (for example a dependency bump that raises the minimum Unity version, which is really a Changed entry).

Also ask when:

- the trigger of a fix can't be found in the issue, PR, commit or diff;
- a change could be either Changed or Fixed, and the issue doesn't say whether the old behavior was intended;
- a change might be breaking, but it's unclear which interface the project keeps stable (for example `public` types in an assembly the project treats as internal);
- the only wording available is generic ("improved performance"), and the diff doesn't show what improved or by how much.
