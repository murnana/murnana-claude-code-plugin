# Designing the layers of a stack

Condensed from GitHub's stacked pull requests docs and community guidance. Use this when proposing how to split a change (SKILL.md Step 4).

## When not to stack

Propose plain PRs (`/murnana-github:pr-create`) instead when:

- The pieces are **independent**: each could target the trunk on its own. Stacks add rebases and CI runs for no benefit.
- The change spans **forks**: stacks only work within one repository.
- The whole change is small enough to review comfortably as one PR.

## Splitting rules

- **One concern per layer.** Each layer should pass the one-sentence test: "This PR adds ___ so that the next layer can ___." If the sentence needs several clauses, split further; if two layers share one sentence, merge them.
- **Dependencies point down.** Anything a layer uses must be in the same layer or below it. Natural bottom-to-top order: schema / migrations → shared types → core logic → API / delivery → UI → docs written after behavior settles.
- **Each layer builds and passes checks on its own.** CI runs every layer as if it targeted the trunk, and a layer can't merge until every layer below it passes.
- **Keep it shallow.** Every layer adds a CI run, a rebase step and a review hand-off. A few clear layers (typically 2–5) beat many tiny ones.
- **One effort per stack.** Unrelated fixes discovered along the way go in their own PR or stack.
- **Watch CODEOWNERS and protections.** Reviews and checks are evaluated against the stack base, and a `CODEOWNERS` change in a lower layer doesn't govern upper layers until it lands. Put such changes in their own bottom layer, or keep them out of the stack.

## Branch naming

- Follow the project's convention if one exists (CONTRIBUTING.md, CLAUDE.md).
- Otherwise use a shared prefix plus a per-layer slug so the stack is recognizable in branch lists, e.g. `feat/login-model`, `feat/login-api`, `feat/login-ui`.
- Always name branches explicitly; don't let `gh stack add -m` generate date-slug names.

## Commit messages

Follow the project's commit convention (same discovery as the murnana-git `commit` skill, if installed). Otherwise one commit per layer whose subject states the layer's concern is enough — the PR body explains the why.

## Approval table

Present exactly this before running any git command:

```
Trunk: main   (from gh repo view / project rules; --base if not default)

| # | Branch           | Files                                  | Commit message                 |
|---|------------------|----------------------------------------|--------------------------------|
| 1 | feat/login-model | src/models/user.ts, migrations/003.sql | Add user credential model      |
| 2 | feat/login-api   | src/api/login.ts, src/api/routes.ts    | Add login endpoint             |
| 3 | feat/login-ui    | src/ui/LoginForm.tsx                   | Add login form                 |

Layer 1 adds the credential model so that layer 2 can authenticate against it.
Layer 2 adds the endpoint so that layer 3 can call it.
Unassigned files: (none)   ← must be empty, or explain why each is left out
PRs will be created as: draft (default) | ready (--open)
```

Row 1 is the bottom of the stack (merges first).
