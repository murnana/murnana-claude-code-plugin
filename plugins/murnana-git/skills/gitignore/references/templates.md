# Choosing templates

Always confirm a path exists in the tree from SKILL.md Step 1 before using it. The table below is a starting point, not a list of what exists.

## Detecting from the project

`Glob` for these markers at the target directory, and only read files whose content decides between candidates.

| Marker | Template |
|---|---|
| `ProjectSettings/ProjectVersion.txt`, `Assets/` + `Packages/manifest.json` | `Unity.gitignore` |
| `*.uproject`, `*.uplugin` | `UnrealEngine.gitignore` |
| `project.godot` | `Godot.gitignore` |
| `*.sln`, `*.slnx`, `*.csproj`, `*.vcxproj` | `VisualStudio.gitignore` (not when Unity or Unreal already matched; their templates cover it) |
| `global.json`, `*.fsproj` without a `.sln` | `Dotnet.gitignore` |
| `package.json` | `Node.gitignore`; add `Nextjs.gitignore`, `Angular.gitignore`, `Nestjs.gitignore`, `community/JavaScript/Vue.gitignore` etc. when that framework is a dependency |
| `bun.lockb`, `bun.lock` | `bun.gitignore` |
| `deno.json`, `deno.jsonc` | `Deno.gitignore` |
| `pyproject.toml`, `requirements*.txt`, `setup.py` | `Python.gitignore` |
| `*.ipynb` | `community/Python/JupyterNotebooks.gitignore` |
| `Cargo.toml` | `Rust.gitignore` |
| `go.mod` | `Go.gitignore` |
| `pom.xml` | `Maven.gitignore` (+ `Java.gitignore`) |
| `build.gradle*`, `settings.gradle*` | `Gradle.gitignore` (+ `Java.gitignore` or `Kotlin.gitignore`) |
| `pubspec.yaml` | `Dart.gitignore`, or `Flutter.gitignore` if it depends on `flutter` |
| `Package.swift`, `*.xcodeproj` | `Swift.gitignore` |
| `Gemfile` | `Ruby.gitignore`, or `Rails.gitignore` if it depends on `rails` |
| `composer.json` | `Composer.gitignore`, plus the framework (`Laravel.gitignore`, `Symfony.gitignore`) |
| `CMakeLists.txt` | `CMake.gitignore` (+ `C.gitignore` or `C++.gitignore`) |
| `*.tf` | `Terraform.gitignore` |
| `*.tex` | `TeX.gitignore` |

If nothing matches, ask the user which templates to use. Offer at most four likely candidates.

## Global templates

`Global/` holds OS, editor and tool rules (`Global/macOS.gitignore`, `Global/Windows.gitignore`, `Global/JetBrains.gitignore`, `Global/VisualStudioCode.gitignore`, `Global/Agents.gitignore`, ...). Do not add them from project detection alone; they describe the developer's machine, not the project. Add them only when the user names them, or ask once whether to include any.

Some language templates say in a comment that editor rules are kept in a `Global/` template. Mention that comment when it appears, but do not add the Global template unasked.

## Several candidates

- A root template and a `community/` template with similar names: the root one is the current version, `community/` holds older or niche variants. Prefer the root one unless the user asks.
- Templates that overlap (e.g. `Node.gitignore` and `Nextjs.gitignore`) can both be added. Do not merge them into one block.
