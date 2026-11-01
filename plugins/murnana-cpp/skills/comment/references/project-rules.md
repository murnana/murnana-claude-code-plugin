# Where to look for project comment conventions

Check these in order. A convention found here overrides the defaults in SKILL.md and the other references. If two sources disagree, an explicit written rule beats a config file, and both beat what the existing code happens to do.

| Kind | Where to look | What to take from it |
|---|---|---|
| Written rules | `CLAUDE.md` and `AGENTS.md` (root and the target's directories), `.claude/rules/`, `CONTRIBUTING.md`, a style guide under `docs/` (search for "comment", "Doxygen", "TODO") | Follow exactly: language, required tags, TODO format, what must or must not be commented |
| Doxygen config | `Doxyfile` (root, `docs/`, `doc/`), or `DOXYGEN_*` variables passed to `doxygen_add_docs()` in `CMakeLists.txt` | `JAVADOC_AUTOBRIEF`, `QT_AUTOBRIEF`, `MULTILINE_CPP_IS_BRIEF` (decide whether `@brief` is needed), `EXTRACT_ALL` / `EXTRACT_PRIVATE` (what is published), `INPUT` / `EXCLUDE` (which files are documented at all), `ALIASES` (project-specific commands), `OUTPUT_LANGUAGE` |
| Formatter | `.clang-format` | `ReflowComments` (long lines get rewrapped), `CommentPragmas` (comments it must not touch), `ColumnLimit` (wrap width), `FixNamespaceComments` (adds `// namespace foo`) |
| Linters | `.clang-tidy`, CI workflows under `.github/workflows/` | Checks that read comments (`google-readability-todo` expects `TODO(name)`), a CI job that runs Doxygen with `WARN_AS_ERROR` |
| Existing code | Other comments in the target file, then its neighbors in the same directory | Only when nothing above decides it: `///` vs `/** */` vs `//!`, `@` vs `\`, the language, whether directions (`[in]`) are used, whether private members are documented. Follow the target file's majority, and say in the report that the convention was inferred |

Notes:

- Doxygen config values can come from more than one place: a Doxyfile can `@INCLUDE` another, and CMake's `doxygen_add_docs()` generates one at build time. Read the one that is actually used.
- If the project has no Doxygen setup at all, still write doc comments in Doxygen syntax: IDEs (clangd, Visual Studio, CLion) render them on hover, and clang's `-Wdocumentation` checks them.
- If the project bans doc comments on some kinds of code (for example generated files, or tests), skip those files even when they're in the target list, and say so.
