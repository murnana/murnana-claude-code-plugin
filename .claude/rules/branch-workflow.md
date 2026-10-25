# Branch Workflow Rules

Applies to all development in this repository.

- Start every change from `develop`.
  Look for `develop` first (`git fetch origin develop`). If it does not exist on the remote, create it from the latest `main` and push it before branching off.
- Branch from `develop` with a prefix that matches the work:
  - `feature/<topic>`: new or changed functionality, docs, rules
  - `bugfix/<topic>`: bug fixes
- Open the pull request against `develop`, not `main`. Merge it into `develop` when the work is done.
  Do not bump plugin versions here. Record the change under `## [Unreleased]` in `docs/plugins/<plugin-name>/CHANGELOG.md` only.
- Release by merging `develop` into `main`. That pull request is where versions are bumped, following `.claude/rules/plugin-version-bump.md`.
- `main` is the published state: the marketplace entries follow `main`, so only merge to `main` what you want users to receive.
- Do not commit directly to `main` or `develop`. Do not branch `feature/*` or `bugfix/*` from `main`.
- After `develop` is merged into `main`, keep `develop` in sync (the release PR's version bump commits must also reach `develop`; merge `main` back into `develop` if needed).
