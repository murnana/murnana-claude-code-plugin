---
name: stack-create
description: Create a stack of pull requests (GitHub Stacked PRs) with gh stack
argument-hint: "[what to stack, or existing branch names bottom-to-top]"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git branch *) Bash(git rev-parse *) Bash(git remote *) Bash(git config *) Bash(git add *) Bash(git restore --staged *) Bash(git commit *) Bash(gh auth status *) Bash(gh extension list *) Bash(gh repo view *) Bash(gh stack view *) Bash(gh stack init *) Bash(gh stack add *) Bash(gh stack submit *) Bash(gh stack link *) Bash(gh stack up *) Bash(gh stack down *) Bash(gh stack top *) Bash(gh stack bottom *) Read Grep Glob AskUserQuestion
---

# Stack Create

Turn a change into a GitHub stack — an ordered chain of small PRs where each PR targets the branch below it and the bottom PR targets the trunk — using the `gh stack` CLI extension.

## Current state

```bash
gh auth status 2>&1 || true
gh extension list 2>&1 || true
git status --short --branch
git remote -v
gh stack view --json 2>/dev/null || true
```

Treat `$ARGUMENTS` (if any) as a hint about what to stack, or as existing branch names listed bottom to top. It doesn't skip any step below.

## Non-interactive rules (read first)

`gh stack` opens a TUI or prompt when arguments are missing, and that blocks this session. Always pass explicit arguments:

| Use | Never use | Why |
|---|---|---|
| `gh stack init <branch>...` | bare `gh stack init` | prompts for a branch name |
| `gh stack add <branch>` | bare `gh stack add` | prompts, fails even when piped |
| `gh stack submit --auto` | bare `gh stack submit` | opens the PR editor TUI |
| `gh stack view --json` | `gh stack view` | full-screen TUI; `--short` is for humans, not parsing |
| `gh stack up` / `down` / `top` / `bottom` | `gh stack switch`, `gh stack modify` | menu/TUI only — no non-interactive path |

Help is `gh stack <command> --help` (`gh stack help <command>` doesn't work). Flags and exit codes: [references/command-reference.md](references/command-reference.md).

Copy this checklist into your response and tick it off:

```
- [ ] 1 gh / gh-stack usable
- [ ] 2 Project rules
- [ ] 3 Pick the input pattern
- [ ] 4 Design layers → approval
- [ ] 5 Build the stack locally
- [ ] 6 Pre-PR checks
- [ ] 7 Submit
- [ ] 8 Verify and hand off
```

## Step 1: Confirm `gh` and `gh-stack` are usable

- `gh auth status` failed → stop and ask, following `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/gh-fallback-mcp.md`. Note that the MCP fallback cannot create stacks; it only helps for plain PRs.
- No `stack` line in `gh extension list` → ask (`AskUserQuestion`) before running `gh extension install github/gh-stack`. Never install silently. Requires Git 2.36+.
- More than one remote in `git remote -v` and `git config remote.pushDefault` empty → pass `--remote <name>` to every `init`/`submit`/`link` call (ask which remote if unclear).

## Step 2: Discover project rules

Read `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/project-rules.md` and apply it: project conventions decide the trunk (`--base`), branch naming, commit message format and required checks. Glob for a candidate file before reading it.

## Step 3: Pick the input pattern

| Situation | Path |
|---|---|
| **A.** Uncommitted (or not-yet-started) work to split into layers | Steps 4 → 5A |
| **B.** Branches that already exist and are already chained | `gh stack init <b1> <b2> ...` adopts them (bottom to top), then Step 6 |
| **C.** Branches managed by jj / Sapling / git-town, user doesn't want local tracking | `gh stack link [--base <trunk>] <b1> <b2> ...` (bottom to top) — pushes and creates PRs itself; skip Step 7 |
| Already-committed work on **one** branch that must be split | Out of scope: it needs a history rewrite. Stop, explain, and ask how to proceed |
| Current branch is already in a stack (`gh stack view --json` succeeded) | Extend it: `gh stack top`, then `gh stack add <branch>` per new layer |

## Step 4: Design the layers and get approval

Follow [references/layer-design.md](references/layer-design.md). Present the plan table it describes — trunk, then one row per layer bottom to top with branch name, files, and commit message — and **wait for approval** before touching git. Reordering layers after branches exist is expensive (and `gh stack modify` is unavailable to you), so settle the order now.

## Step 5A: Build the stack locally

For the bottom layer:

```bash
gh stack init [--base <trunk>] <branch-1>
git add <paths for layer 1>
git commit -m "<message>"
```

For each next layer, on the current top branch:

```bash
gh stack add <branch-n>
git add <paths for layer n>
git commit -m "<message>"
```

- Stage by explicit paths only — never `git add -A`, which would sweep later layers' files into this one.
- After the last layer, `git status --short` must be empty of planned files. Anything left over means a layer is missing a file: stop and ask.
- `gh stack add -Am` is **not** used: it auto-generates the branch name and stages everything.

## Step 6: Run pre-PR checks

Same rules as pr-create Step 3: discover the project's lint/test/build, run the relevant ones (each is an ordinary permission-prompted Bash call), and if one fails **stop** before pushing. Every layer is checked by CI against the stack base, so a broken lower layer blocks every layer above it from merging. Run checks on the top branch at minimum; when a lower layer could plausibly break on its own, check it out (`gh stack down`/`bottom`) and run them there too.

## Step 7: Submit

```bash
gh stack submit --auto [--remote <name>]
```

- `--auto` creates **draft** PRs with auto-generated titles. Add `--open` only if the user asked for ready-for-review PRs.
- `submit` pushes every branch, creates one PR per branch with chained bases, and links them as a stack on GitHub.
- Exit 9 → stacked PRs aren't enabled for this repository. Report it to the user and stop; don't fall back to plain chained PRs without asking.

## Step 8: Verify and hand off

- Run `gh stack view --json` and confirm every branch has `pr.number` and the bases chain trunk → bottom → … → top.
- Report each layer's PR URL from that JSON (bottom first).
- Tell the user the auto-generated titles/bodies are placeholders and that `/murnana-github:stack-pr-message` writes proper per-layer messages.

## Gotchas

- A stack is strictly linear: one parent, at most one child. Parallel independent work goes in separate stacks (or plain PRs).
- All branches must live in the same repository — cross-fork stacks are unsupported.
- `gh stack init` turns on `git rerere` automatically; don't fight it.
- Never `git push` the branches yourself; `submit`/`link` push with the right lease and base wiring.
- Don't set PR titles/bodies during submit — `gh pr edit` afterwards is the supported path (that is what stack-pr-message does).
- Exit 8 (stack locked by another process): wait ~5 s and retry once, then report.

## References

- Layer splitting rules and the approval table format:
  [references/layer-design.md](references/layer-design.md)
- `init` / `add` / `submit` / `link` / `view --json` flags, JSON fields, exit codes:
  [references/command-reference.md](references/command-reference.md)
- Project rules, PR template discovery, `gh` fallback (shared with pr-create):
  `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/`
