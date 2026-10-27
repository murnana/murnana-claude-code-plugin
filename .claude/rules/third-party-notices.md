# Third-Party Notices Rules

Applies whenever a change adds, updates or removes material that comes from someone else. Each plugin keeps its own record at `plugins/<plugin-name>/THIRD_PARTY_NOTICES.md`, so the record is installed together with the plugin. There is no repository-root `THIRD_PARTY_NOTICES.md`.

- Check rights before adding third-party material to `plugins/` or `docs/`. This covers text, code, templates and specs that are copied, translated, summarized or adapted, and trademarks.
  - Find the license from the source itself (its LICENSE file, terms page or site footer), not from memory. Read the license text when the license is unfamiliar.
  - Do not add material whose license forbids this use (for example a no-derivatives or non-commercial license for adapted text). Link to it, or write a summary in your own words instead.
- Update the notices file of each plugin that uses the material, in the same PR as the change:
  - Add or remove the entry (what, where in the plugin, source URL, license, and the copyright line).
  - Include the full license text when the license requires keeping its notice (for example MIT).
  - Write only the source, the license and the trademarks. Do not list material that is only fetched at runtime or only linked, tools the user installs, or notes on reviewing terms of use.
  - Add new trademarks to that plugin's trademark list. Keep the non-affiliation statement in `README.md`.
  - When two plugins use the same source, each lists it; do not point one plugin's notices at another plugin's file, since each `git-subdir` plugin is installed alone.
- Create `plugins/<plugin-name>/THIRD_PARTY_NOTICES.md` when a plugin gains its first bundled third-party material or trademark mention.
- When bumping or re-snapshotting an included source (for example a new Keep a Changelog version), re-check that its license has not changed and update the entry.
- If the license can't be determined, say so in the PR and the notices file instead of guessing.
- Editing a notices file is a change under `plugins/<plugin-name>/`, so the plugin's version is bumped in the next release PR (see `.claude/rules/plugin-version-bump.md`).
