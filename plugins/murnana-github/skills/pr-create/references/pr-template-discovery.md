# Where to look for a PR template

Search in this order (mirrors GitHub's own convention: <https://docs.github.com/articles/creating-a-pull-request-template-for-your-repository>). `Glob` case-insensitively, since GitHub itself matches these filenames without regard to case.

| Order | Location | Notes |
|---|---|---|
| 1 | `.github/PULL_REQUEST_TEMPLATE/*.md` | Multiple templates. GitHub shows the author a picker — treat this as "multiple candidates, pick or ask" (see SKILL.md Step 5). |
| 2 | `.github/pull_request_template.md` | Single template, case-insensitive (`PULL_REQUEST_TEMPLATE.md` etc. also match). |
| 3 | `docs/pull_request_template.md` | |
| 4 | `pull_request_template.md` (repo root) | |

## Handling the template content

- Templates may contain `<!-- HTML comments -->` instructing the author not to remove certain sections, or explaining what to write in a section. Preserve these verbatim; only fill in placeholders, don't strip instructional comments.
- If a template already has a required-sections structure, do not add the Why/影響範囲/デバッグ方法 sections from [pr-message.md](pr-message.md) on top of it — the template is authoritative once found.

## When multiple templates exist

- If a template's filename clearly matches the nature of the change (e.g. `bug_report.md`-style naming, `feature.md`, `hotfix.md`), pick it autonomously and say which one and why.
- If it's ambiguous, ask via `AskUserQuestion` listing the available templates by filename.
