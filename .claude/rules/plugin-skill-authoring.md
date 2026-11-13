---
paths:
  - "plugins/**/SKILL.md"
---

# Plugin Skill Authoring Rules

Format details live in `plugins/murnana-agent-config/skills/skill-create/references/skill-format.md` and `writing-guide.md`. Read them before writing a new skill. The rules below are the ones this repository has already been bitten by.

## Frontmatter

- Write `description` as one short English sentence (what it does, then "Not for X" if a near-miss exists). Do not add `when_to_use` or Japanese trigger phrases: descriptions of auto-invocable skills stay in context for as long as the plugin is enabled.
- Set `disable-model-invocation: true` on any skill with side effects (commit, push, create a PR, launch an app, write outside the target file).
- List in `allowed-tools` only the exact command shapes the body runs, as `Bash(git log *)`, space-separated. Never the old `Bash(git log:*)` form, and never a whole tool family such as `Bash(git config *)` when the body only reads (`Bash(git config --get *)`). A broad grant lets through the very operations the body says to confirm first.
- Leave out any tool the body says must be confirmed or must not run (`git push`, `git commit --amend`, `git reset`). The approval prompt is the safety valve.
- Remove a tool from `allowed-tools` when the body stops using it.
- Reference bundled scripts as `${CLAUDE_SKILL_DIR}/scripts/<name>`, in both `allowed-tools` and the body.

## Dynamic context injection

- An injected block is a fence whose info string is `!`. A fence marked `bash` is not injected; Claude only sees it as text.
- Keep the prose and the fence type consistent: say "these blocks were filled in when the skill loaded, do not re-run them" only above injected blocks, and say "run these first" above `bash` blocks.
- Write one command per injected line, covered by `allowed-tools`, optionally followed by `2>/dev/null || true`. A pipe into `head` or `grep`, an `echo`, or `a || b` with an unlisted `b` is refused, and the whole skill then fails to load.
- Do not inject a command whose exit code the steps depend on (for example `gh stack view`). `|| true` hides the code. Make it a numbered step that Claude runs instead.
- Never write the inline injection syntax (a bang followed by a backtick) anywhere in SKILL.md, even in prose. It is executed. Describe it in words.

## Body

- Write the body in English.
- Write procedures as numbered steps with the exact command, how to read its result, and where to go for each outcome. Skills also run on Sonnet (the `comment` skills set `model: sonnet`), which skips or reorders loosely described steps.
- Ask the user only through `AskUserQuestion`, with all open questions in one call. Do not end a reply with a question in prose. Do not ask for what has a sensible default (reply language, optional rounds).
- Do not tell the skill to add attribution lines or footers (`Co-Authored-By:`, "Generated with Claude Code"). That is the user's setting.

## Check before committing

- `.claude/hooks/check-plugin-authoring.sh` runs after every Edit or Write of a `SKILL.md` and rejects the mechanical mistakes above (`when_to_use`, a non-ASCII `description`, old or broad `allowed-tools` forms, inline injection syntax, compound commands in injected blocks). Fix what it reports; do not work around it. It cannot judge the rest of this file.
- Run `claude plugin validate plugins/<plugin-name>`.
- Invoke each changed skill once with `claude --plugin-dir plugins/<plugin-name>` and confirm it loads without `Shell command failed for pattern` or `This command requires approval`.
