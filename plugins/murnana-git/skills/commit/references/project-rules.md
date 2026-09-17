# Where to look for project-specific commit rules

Check these in order. The first rule found is the **only** rule that applies — do
not blend it with the fallback convention in
[commit-message.md](commit-message.md).

| Kind | Where to look | What to do if found |
|---|---|---|
| Instructions | `CLAUDE.md` (repo root and subdirectories), `CONTRIBUTING.md`, `.github/CONTRIBUTING.md`, any commit convention documented under `docs/` | Follow it exactly as written |
| Message template | The file pointed to by `git config commit.template`, `.gitmessage` | Use it as the message skeleton |
| Message linting | `commitlint.config.*`, `.commitlintrc*`, a `commitlint` key in `package.json` | Write messages that pass the configured rules (e.g. Conventional Commits) |
| Pre-commit checks | `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`, a `Makefile`, `scripts` in `package.json`, `.github/workflows/` | Let these run via `git commit` (see SKILL.md Step 3); don't duplicate them manually |
| Inferred from history | `git log --format='%s' -20` | Only when nothing above matched. Determine whether history follows Conventional Commits, gitmoji, or plain prose, and match it. Weaker than an explicit rule — say so when presenting the plan |
