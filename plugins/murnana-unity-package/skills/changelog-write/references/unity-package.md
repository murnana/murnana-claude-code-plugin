# Unity Package Manager (UPM) packages

What a UPM package looks like, where its changelog goes, and which changes are breaking. Sources are listed at the end; the Unity Manual is the authority when it disagrees with this file.

## Contents

- Finding the package
- Package layout
- The changelog in the Package Manager
- `.meta` files
- Version rules
- Finding breaking changes in a UPM package
- Lifecycle and pre-release versions
- Package Validation Suite
- Sources

## Finding the package

A UPM package is a folder whose root holds a lowercase `package.json` with at least `name` and `version`. `name` uses reverse domain notation (`com.company.package-name`). Tell it apart from an npm `package.json` by that name and by Unity fields such as `unity`, `displayName` or `samples`.

Where packages live:

| Location | How to recognize it | Editable? |
|---|---|---|
| Embedded: `<project>/Packages/<name>/` | Folder under `Packages/`, no entry needed in `Packages/manifest.json`. Shown as "Custom" in the Package Manager | Yes |
| Local, outside the project | `Packages/manifest.json` has `"<name>": "file:../path"`. Shown as "Local" | Yes, at the referenced path |
| Standalone repository | `package.json` at the repository root, or in a subfolder for git URLs with `?path=` | Yes |
| Cache: `Library/PackageCache/`, registry or git installs | Inside `Library/` | **No.** Unity overwrites it. Never edit |

Glob for `**/package.json` and skip `node_modules/`, `Library/`, `Temp/`, `Logs/`, `obj/`. `Packages/manifest.json` is the project manifest, not a package.

## Package layout

From the Unity Manual (layout created by **Create package**):

```
<package-root>
  ├── package.json
  ├── README.md
  ├── CHANGELOG.md
  ├── LICENSE.md
  ├── Third Party Notices.md
  ├── Editor/
  ├── Runtime/
  ├── Tests/
  │   ├── Editor/
  │   └── Runtime/
  ├── Samples~/   (Samples/ before export)
  └── Documentation~/
```

- `CHANGELOG.md` sits at the package root, next to `package.json`. It lists changes in reverse chronological order. Never put it in `Documentation~/`.
- Folders ending in `~` are hidden from the Project window and get no `.meta` files.
- Unity recommends the Keep a Changelog format and asks for an update every time a new version is published. The changelog is optional for unshared packages and strongly recommended for shared ones.

## The changelog in the Package Manager

- The Package Manager window links to the changelog. If `package.json` has `changelogUrl`, it opens that URL. If the URL can't be reached, an installed package falls back to its cached `CHANGELOG.md`, and an uninstalled one shows a warning.
- If `changelogUrl` points somewhere other than this file (a docs site, GitHub Releases), ask whether `CHANGELOG.md` is still maintained before editing it, and remind the user that the external page needs the same update.
- If the package is packed with `npm pack` and `.npmignore` or the `files` key excludes `CHANGELOG.md`, mention it: the file won't ship.

## `.meta` files

Unity gives every file it imports a `.meta` file with a GUID. Files in an immutable package (git URL, registry, tarball) that lack a `.meta` produce a warning on import, and Unity can't generate one there.

- Create `CHANGELOG.md.meta` next to a new `CHANGELOG.md` when the package tracks `.meta` files, that is, when `package.json.meta` exists.
- Generate a fresh GUID with `uuidgen`. Write it as 32 lowercase hex digits without hyphens. Never copy a GUID from another file: duplicate GUIDs break asset references. If `uuidgen` isn't available (Windows), skip the `.meta` for an embedded package and tell the user that the Editor will create it on the next import; for any other location, ask the user.
- Write the `.meta` before `CHANGELOG.md`. Otherwise an open Editor may import the new file first and generate a `.meta` with a different GUID.
- Template:

  ```yaml
  fileFormatVersion: 2
  guid: 0123456789abcdef0123456789abcdef
  TextScriptImporter:
    externalObjects: {}
    userData: 
    assetBundleName: 
    assetBundleVariant: 
  ```

- Never change the GUID of an existing `.meta`. Editing `CHANGELOG.md` itself never needs a `.meta` change.

## Version rules

`version` in `package.json` must be SemVer `major.minor.patch`. Start new packages at `0.1.0` and stay on `0.y.z` until the package is production-ready. When bumping, reset the lower numbers to 0. Renaming a package isn't supported: publish under a new name instead.

| Change | Minimum bump |
|---|---|
| Removed or renamed public type/member; changed signature or visibility | MAJOR |
| Removed an `[Obsolete]` API | MAJOR |
| Removed an asset, or changed an asset's `.meta` GUID | MAJOR |
| Removed an assembly, or a supported platform | MAJOR |
| Added `defineConstraints` to an assembly | MAJOR |
| Turned a normal assembly into a test assembly | MAJOR |
| Added an assembly with **Auto Referenced** on, or turned Auto Referenced on (new types can clash with user code) | MAJOR (judge case by case) |
| Added a feature, public type, member or overload | MINOR |
| Added an assembly with Auto Referenced off; added a platform | MINOR |
| Marked an API `[Obsolete]` | MINOR |
| Changed `unity` or `unityRelease` | MINOR at least |
| Turned a test assembly into a normal one | MINOR |
| Bug fix, internal refactor, performance, documentation | PATCH |
| Asset fix that keeps its GUID | PATCH |
| Changed assembly references; toggled **Allow 'unsafe' Code** or **Override References** | PATCH |
| Changed `description`, `displayName`, `category`, `keywords` | Any |

A dependency change takes the bump of its effect: internal only → PATCH; new behavior → MINOR; breaks compatibility (for example a dependency's types exposed through an Auto Referenced assembly) → MAJOR.

While the version is `0.y.z`, a breaking change may go in a MINOR bump.

## Finding breaking changes in a UPM package

In addition to the general checklist in [entry-writing.md](entry-writing.md), check the diff for:

- `public` / `protected` C# members in `Runtime/` and `Editor/` assemblies that were removed, renamed, or changed in signature, return type, or visibility;
- `*.asmdef` changes: `name` (users reference it from their own asmdef), `autoReferenced`, `defineConstraints`, `includePlatforms` / `excludePlatforms`;
- deleted assets, or a `guid:` line that changed in any `*.meta` (references in user scenes and prefabs break);
- renamed or removed serialized fields (`[SerializeField]`, public fields) without `[FormerlySerializedAs]`: saved data in user assets is lost;
- `samples` paths or names changed: imported samples land in a different folder;
- menu paths (`[MenuItem]`), `[CreateAssetMenu]` entries, Project Settings / Preferences paths users know;
- `dependencies` added or raised: judge by effect (see "Version rules"). Breaking only when users' code or assets stop working with the new dependency version.

Not breaking, but always recorded and highlighted: `unity` or `unityRelease` raised in `package.json`. The Package Manager hides the new version from older Editors instead of breaking them. Record it under Changed without `**Breaking:**`, bump at least MINOR, and mention it in the release summary line.

## Lifecycle and pre-release versions

| State | Version form | Notes |
|---|---|---|
| Experimental | `0.y.z`, or `x.y.z-exp.N` | Unsupported, for testing and feedback |
| Pre-release | `x.y.z-pre.N` (Manual example: `1.3.0-pre`) | On the release track |
| Released | `x.y.z`, no suffix | Passed documentation, changelog and license checks |

Unity's own registry moves a changed package like this: breaking change `1.2.3` → `2.0.0-exp`; non-breaking change in usage `1.2.3` → `1.3.0-pre`; fix `1.2.3` → `1.2.4`. Third-party packages don't have to follow it. Use a suffix only if the project already does or the user asks for one. Changelog headings may carry the suffix: `## [1.3.0-pre.1] - 2026-10-24`.

## Package Validation Suite

Unity's Package Validation Suite (`com.unity.package-validation-suite`) reports a warning for an `[Unreleased]` section in `CHANGELOG.md` during CI and candidate publishing, and an error during promotion to the Unity registry. Only packages published through Unity's own pipeline go through promotion. If the project runs the Validation Suite, or its released files never keep an empty `[Unreleased]`, follow that: remove the empty section at release time and re-add it when the next change is recorded.

## Sources

- Package development: https://docs.unity3d.com/6000.6/Documentation/Manual/cus-pkg-development.html
- Package layout: https://docs.unity3d.com/6000.6/Documentation/Manual/cus-layout.html
- Update the package changelog: https://docs.unity3d.com/6000.6/Documentation/Manual/cus-changelog.html
- Package manifest reference: https://docs.unity3d.com/6000.6/Documentation/Manual/upm-manifestPkg.html
- Package versioning: https://docs.unity3d.com/6000.6/Documentation/Manual/upm-semver.html
- Package states and lifecycle: https://docs.unity3d.com/6000.6/Documentation/Manual/upm-lifecycle.html
- Package location (embedded or local): https://docs.unity3d.com/6000.6/Documentation/Manual/cus-location.html
- Package Validation Suite changelog (entries adding the UNRELEASED warning and error): https://docs.unity3d.com/Packages/com.unity.package-validation-suite@0.80/changelog/CHANGELOG.html
