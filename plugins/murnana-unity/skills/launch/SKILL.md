---
name: launch
description: Launches a Unity project in the Unity Editor on a chosen platform, and saves the first platform given as the project default.
disable-model-invocation: true
argument-hint: "[platform: android|ios|webgl|win64|osx|linux64|tvos|visionos|…] [project path]"
allowed-tools: Read Glob Grep Write AskUserQuestion Bash(unity *) Bash(UNITY_CLI_FTUE=1 unity auth status *) Bash(cat */ProjectSettings/ProjectVersion.txt) Bash(ls *) Bash(uname *) Bash(pgrep *) Bash(/Applications/Unity/Hub/Editor/*/Unity.app/Contents/MacOS/Unity *) Bash(/opt/Unity/Hub/Editor/*/Editor/Unity *)
---

# Launch Unity

Start with `UNITY_CLI_FTUE=1 unity auth status --json`

Open a Unity project in the right Editor version on the right platform, and remember the platform so the next launch needs no argument.

Treat `$ARGUMENTS` as an optional platform and an optional project path, in either order.

## Step 1: Find the project

The project root is the folder that has `Assets/`, `Packages/`, and `ProjectSettings/ProjectVersion.txt`.

1. If `$ARGUMENTS` has a path, use it.
2. Otherwise use the working directory, then look for the nearest folder below it that matches (`Glob` `**/ProjectSettings/ProjectVersion.txt`).
3. If several projects match, ask which one. If none, stop and say so.

## Step 2: Decide the platform

Resolve in this order and stop at the first hit:

1. A platform in `$ARGUMENTS` or the user's request.
2. `platform:` in `<project>/.claude/unity-launch.local.md` (see "Saved default").
3. Ask with `AskUserQuestion`. Offer the platforms the project's installed modules support, most likely first. Do not guess.

Map the user's wording to a `-buildTarget` value with [references/editor-cli.md](references/editor-cli.md) (for example "Windows" → `win64`, "Mac" → `osxuniversal`). If the wording matches no value, ask.

### Saved default

The default is per project. It lives in `<project>/.claude/unity-launch.local.md`:

```markdown
---
platform: android
---
```

- When the file is missing, the platform you resolved in Step 2 becomes the default: write the file after a successful launch and say so in one line. Create `<project>/.claude/` if needed.
- When the user names a platform that differs from the saved one, launch with it for this run only. Overwrite the default only if the user says to ("今後はこれをデフォルトに", "make this the default").
- Remind the user once, when you create the file, to git-ignore `*.local.md` if the project does not already.

## Step 3: Find the Editor

1. Read the version from `m_EditorVersion:` in `ProjectSettings/ProjectVersion.txt` (e.g. `6000.3.7f1`).
2. If the `unity` CLI exists (`unity version`), run `unity editors -i --json` (each entry has `version`, `location`, `moduleNames`) and look for that version. The CLI is documented at <https://docs.unity.com/en-us/unity-cli/unity-cli-reference>.
3. Without the CLI, look at the default Hub path in [references/editor-cli.md](references/editor-cli.md) for the current OS (`ls`).

Outcomes:

- **Found**: continue.
- **Not installed**: tell the user which version is missing and ask before installing. With the CLI, install with `unity install <version> -m <module>`; take `-c <changeset>` from `ProjectVersion.txt`'s `m_EditorVersionWithRevision` (the hash in parentheses) when the version is not in the release list. Without the CLI, tell the user to install it from Unity Hub and stop.
- **Platform module missing** (the chosen platform needs one, such as `android`, `ios`, `webgl`; see the table in the reference): list with `unity install-modules -e <version> -l`, then ask before running `unity install-modules -e <version> -m <module> --cm`. Without the CLI, tell the user to add the module in Unity Hub.

Installing downloads gigabytes and may need elevation. Never install without a yes.

## Step 4: Check the project is not already open

Unity allows one instance per project. If `<project>/Temp/UnityLockfile` exists and a Unity process is running (`pgrep -fl Unity`), the project is probably open. Tell the user and ask whether to continue. Do not close it: `unity close` discards unsaved work.

A stale lockfile with no process is fine to ignore.

## Step 5: Launch

With the `unity` CLI, which returns once the Editor is starting:

```sh
unity open "<project>" --build-target <target> [--editor-path "<editor .app>"]
```

`--build-target` is passed to the Editor as `-buildTarget`. Use the CLI's own spelling from [references/editor-cli.md](references/editor-cli.md) (for example `Android`, `StandaloneOSX`). Extra Editor arguments go in `--args "<string>"`. Add `--wait` only if the user wants to block.

Without the CLI, start the Editor executable directly with the Editor's lowercase target, in the background (`run_in_background: true`) because it stays running until the user quits it:

```sh
"<editor executable>" -projectPath "<project>" -buildTarget <target>
```

Add extra Editor arguments only when the user asked for them (`-logFile -`, `-force-vulkan`, `-disable-assembly-updater`, and so on; see the reference). Do not use `--batchmode`, `-batchmode`, `-quit`, or `-nographics`: they make the Editor non-interactive or exit it. Do not use `--accept-upgrades` unless the user asks: it upgrades the project and rewrites scripts without a prompt.

Switching a project to another platform reimports assets and can take many minutes the first time. Warn the user when the target differs from the platform in `ProjectSettings/EditorUserBuildSettings.asset` (`m_ActiveBuildTarget`) or the first launch.

## Step 6: Report

One or two lines: Editor version, platform, project, whether the default was saved. If the launch command exits immediately with an error, show the error and the command. Do not retry with different flags blindly.

## Gotchas

- `-projectPath` must be quoted when it has spaces. A relative path is resolved from the working directory.
- `-buildTarget` takes lowercase identifiers, not Hub labels. `win` is 32-bit; use `win64`.
- A project whose version is missing from the machine opens a Hub dialog if launched through the Hub. Check the version first.
- `-activeBuildProfile <path>` (Unity 6) applies a build profile's scripting defines before compilation. Offer it only if the user mentions build profiles; it is a separate choice from the platform.
- Documentation differs per version. Don't fetch Unity's documentation yourself: Unity's Terms of Service restrict automated access to its sites. When an argument is in doubt, run `unity open --help` when the CLI exists, or give the user the page for the project's version to check: `https://docs.unity3d.com/<major>000.<minor>/Documentation/Manual/EditorCommandLineArguments.html` for Unity 6 (for example `6000.3`), and `https://docs.unity3d.com/<year>.<minor>/Documentation/Manual/CommandLineArguments.html` for 2022.x and earlier.
