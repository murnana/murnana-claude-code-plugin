---
paths:
  - "evals/plugins/**"
---

# Plugin Eval Rules

- Keep cases at `evals/plugins/<plugin-name>/<case>/`, never under `plugins/<plugin-name>/`, so they are not installed with the plugin.
- A case is `prompt.md` (frontmatter `max_turns`, `allowed_tools`, then the user prompt) plus `graders/*.md`. Imitate `evals/plugins/murnana-cpp/`.
- Give every case two graders: `outcome.md` (`type: llm`, explicit PASS and FAIL conditions) and a trigger grader (`type: tool_used`, `tool: Skill`).
  - Should fire: `skill-fired.md`.
  - Should not fire: `skill-not-fired.md` with `min: 0`, `max: 0`, `arm: both`.
- Match the skill name with and without the plugin prefix: `input_match: '"skill"\s*:\s*"(?:murnana-cpp:)?comment"'`.
- Include at least two `near-miss-*` cases per auto-invocable skill: prompts that share its vocabulary but belong to another skill or to no skill (a commit message, another language's doc comments).
- Write prompts the way a user would, without naming the skill.

## Running

- `claude plugin eval` only reads cases inside the plugin root (`--eval-dir` and `experimental.evals` reject `..`), so link them in temporarily: `ln -s ../../evals/plugins/<plugin-name> plugins/<plugin-name>/evals`. The link is git-ignored. Remove it afterwards and never commit it.
- Run `claude plugin eval plugins/<plugin-name> --output-dir <dir outside the plugin>`. Results cannot be written through the symlink.
- The plugins set `defaultEnabled: false` and the eval sandbox does not enable them. If the run prints "will run WITHOUT this plugin", the scores are meaningless.
