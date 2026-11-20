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

Run evals on a throwaway copy of the plugin, never in `plugins/<plugin-name>/` itself. Two things make the repository layout unusable as it is (checked with Claude Code 2.1.325):

- `claude plugin eval` only reads cases inside the plugin root (`--eval-dir` and `experimental.evals` reject `..`), and it refuses a symlink: a linked `evals` fails every case with "is an eval-directory link that points outside the plugin".
- The plugins set `defaultEnabled: false` and the eval sandbox does not enable them. If the run prints "will run WITHOUT this plugin", the scores are meaningless.

Steps, with `<work>` a directory outside the repository (a temporary directory):

1. Copy the plugin and its cases: `cp -r plugins/<plugin-name> <work>/` then `cp -r evals/plugins/<plugin-name> <work>/<plugin-name>/evals`.
2. Enable the copy only: set `"defaultEnabled": true` in `<work>/<plugin-name>/.claude-plugin/plugin.json`. Never commit that value.
3. From `<work>`, run `claude plugin eval <plugin-name> --output-dir <work>/results/<plugin-name> --no-publish`. Add `--case "<glob>"` to run some cases, `--model sonnet` to test on Sonnet, `--runs 1` for a quick pass (the default is 3 runs per case, in two arms).
4. Check that the output has no "will run WITHOUT this plugin" line before reading the scores.
5. Read each case's `with` score and its `skill-fired` / `skill-not-fired` line. A `tool_used: Skill` grader is not part of the score in the default two-arm run, so a case can pass while its skill never fired.
6. A failed run leaves `/tmp/claude-eval-*` behind. Remove it as the message says, and copy again after every change to the plugin.

When `with` and `without` both pass, the case shows that the skill fires and does no harm, not that it improves the answer. Say so when reporting results.
