# Third-Party Notices Rules

Applies whenever a change adds, updates or removes material that comes from someone else. `THIRD_PARTY_NOTICES.md` at the repository root is the record.

- Check rights before adding third-party material to `plugins/` or `docs/`. This covers text, code, templates and specs that are copied, translated, summarized or adapted, and trademarks.
  - Find the license from the source itself (its LICENSE file, terms page or site footer), not from memory. Read the license text when the license is unfamiliar.
  - Do not add material whose license forbids this use (for example a no-derivatives or non-commercial license for adapted text). Link to it, or write a summary in your own words instead.
- Update `THIRD_PARTY_NOTICES.md` in the same PR as the change:
  - Add or remove the entry (what, where in the repo, source URL, license, and the copyright line).
  - Include the full license text when the license requires keeping its notice (for example MIT).
  - List material that is only fetched at runtime, or only linked, in its own section, so it is not mistaken for bundled content.
  - Add new trademarks to the trademark list. Keep the non-affiliation statement in `README.md`.
- When bumping or re-snapshotting an included source (for example a new Keep a Changelog version), re-check that its license has not changed and update the entry.
- If the license can't be determined, say so in the PR and the notices file instead of guessing.
- A change that only edits `THIRD_PARTY_NOTICES.md` needs no plugin version bump (see `.claude/rules/plugin-version-bump.md`).
