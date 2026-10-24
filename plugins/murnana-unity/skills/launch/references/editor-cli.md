# Unity launch reference

Sources: [Unity CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference) and the Editor command-line arguments page for Unity 6.3 (<https://docs.unity3d.com/6000.3/Documentation/Manual/EditorCommandLineArguments.html>). Values can change between Editor versions; when unsure, give the user the page for the project's version to check instead of fetching it.

## Editor executable (default Hub install path)

| OS | Path |
|---|---|
| macOS | `/Applications/Unity/Hub/Editor/<version>/Unity.app/Contents/MacOS/Unity` |
| Windows | `C:\Program Files\Unity\Hub\Editor\<version>\Editor\Unity.exe` |
| Linux | `/opt/Unity/Hub/Editor/<version>/Editor/Unity` |

The CLI's `unity editors -i --json` reports the real path, which may differ if the user changed the install location (`unity install-path`).

## `-buildTarget` values and modules

`unity open --build-target` is documented with the enum spelling (`StandaloneOSX`); the Editor's own argument list uses the lowercase names below. The table gives both. Use the CLI spelling with `unity open` and the lowercase one when calling the Editor directly.

| User says | `unity open --build-target` | Editor `-buildTarget` | Hub/CLI module id |
|---|---|---|---|
| Android | `Android` | `android` | `android` (child modules: SDK & NDK, OpenJDK) |
| iOS | `iOS` | `ios` | `ios` |
| WebGL | `WebGL` | `webgl` | `webgl` |
| Windows 64-bit (Windows/PC) | `StandaloneWindows64` | `win64` | `windows-il2cpp` / `windows-mono` (non-Windows hosts) |
| Windows 32-bit | `StandaloneWindows` | `win` | same as above |
| Mac | `StandaloneOSX` | `osxuniversal` | `mac-il2cpp` / `mac-mono` (non-Mac hosts) |
| Linux | `StandaloneLinux64` | `linux64` | `linux-il2cpp` / `linux-mono` (non-Linux hosts) |
| tvOS | `tvOS` | `tvos` | `appletv` |
| visionOS | `VisionOS` | `visionos` | `visionos` |
| Universal Windows Platform | `WSAPlayer` | `windowsstoreapps` | `universal-windows-platform` |
| Cloud Rendering | `CloudRendering` | `cloudrendering` | — |

Only `StandaloneOSX` comes from the CLI's own help; the other CLI spellings are Unity's `BuildTarget` enum names, assumed to be accepted the same way. If `unity open` rejects one, use the lowercase Editor value through `--args "-buildTarget <value>"` or launch the Editor directly.

Module ids vary by Editor version; confirm with `unity install-modules -e <version> -l`. Closed platforms (consoles) add their own values.

The host's own desktop platform needs no extra module.

## Unity CLI commands used

| Command | Use |
|---|---|
| `unity version` | Check the CLI is installed |
| `unity editors -i --json` | Installed Editors and paths |
| `unity install <version> [-c <changeset>] [-m <module>]... [--cm]` | Install an Editor |
| `unity install-modules -e <version> [-l] [-m <module>]... [--cm]` | List or add modules |
| `unity open [project] [--build-target <t>] [--editor-path <app>] [--editor-version <v>] [--args "<string>"] [--wait]` | Open a project in the Editor resolved from its version. `--build-target` is passed as `-buildTarget`; `--args` passes any other Editor arguments. Verified against 1.0.0-beta.14. Also has `--batchmode`, `--accept-upgrades`, `--until-ready`, which this skill does not use |
| `unity close` | Close the Editor that has the project open. Does not save. Never run it unasked |

Add `--non-interactive` when running the CLI without a terminal, so it errors instead of waiting for a prompt. Exit codes: `0` ok, `2` usage error, `6` primary operation failed, `7` service unreachable (safe to retry).

## Editor arguments for an interactive launch

| Argument | Purpose |
|---|---|
| `-projectPath <path>` | Project to open |
| `-buildTarget <name>` | Active platform on open (table above) |
| `-activeBuildProfile <path>` | Unity 6 build profile asset, relative to the project root |
| `-logFile <path>` | Editor log location; `-` prints to the console |
| `-force-vulkan`, `-force-d3d11`, `-force-d3d12`, `-force-metal`, `-force-glcore` | Force a graphics API (d3d is Windows-only, metal is macOS-only) |
| `-disable-assembly-updater` | Skip API Updater |
| `-rebuildLibrary` | Delete `Library/` and reimport everything (slow; only on request) |
| `-version` | Print the Editor version and exit |

Arguments that make the Editor non-interactive and are therefore not for this skill: `-batchmode`, `-quit`, `-nographics`, `-executeMethod`, `-runTests`, `-build*`.
