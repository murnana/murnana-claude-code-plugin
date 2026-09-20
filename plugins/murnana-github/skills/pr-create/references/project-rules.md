# Where to look for project-specific PR rules

Check these in order. The first rule found is the **only** rule that applies for tone/format — do not blend it with the generated fallback in [pr-message.md](pr-message.md). This file is deliberately separate from `murnana-git`'s commit `project-rules.md`: PR conventions (template, required reviewers, base branch) and commit-message conventions are orthogonal, and a project may have one without the other.

| Kind | Where to look | What to do if found |
|---|---|---|
| Instructions | `CONTRIBUTING.md`, `.github/CONTRIBUTING.md`, `CLAUDE.md` (repo root and subdirectories), any PR-related convention documented under `docs/` | Follow it exactly as written |
| Template | See [pr-template-discovery.md](pr-template-discovery.md) — don't duplicate the search order here | Use the discovered template as-is |
| Required checks | `.github/workflows/*.yml` (job names hint at what must pass), package manager scripts, `Makefile`, or equivalent project-specific tooling (not necessarily Node.js — could be Unity, Unreal Engine, Python, etc.) | Run the relevant ones before pushing (see SKILL.md Step 3) |
| Base branch | `gh repo view --json defaultBranchRef`, or an explicit convention documented in `CONTRIBUTING.md`/`CLAUDE.md` (e.g. PRs target `develop`, not `main`) | Use the discovered default unless the user specifies otherwise |
