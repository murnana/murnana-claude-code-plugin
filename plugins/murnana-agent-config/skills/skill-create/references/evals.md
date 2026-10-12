# Evals

How to scaffold evals that show whether the skill (a) triggers on the right prompts and (b) produces better output than no skill. Condensed from agentskills.io "Evaluating skill output quality" and "Optimizing skill descriptions", and from the Claude Code `plugin-evals` docs.

**Cost:** every eval run and every LLM-judged grader is a real model call billed to the user's plan or API account. This skill writes eval files but never runs them. Give the user the commands.

## Contents

- Output test cases
- Assertions and grading
- Trigger queries
- Format A: plugin skills (`claude plugin eval`)
- Format B: project / personal skills (`evals/evals.json`)
- Iterating

## Output test cases

Each case has three parts: a **prompt** (what a real user would type), the **expected output** (a human-readable description of success), and optional **input files**.

- Start with **2–3** cases; expand after seeing results.
- Vary phrasing (casual / precise), detail and formality.
- Include at least one edge case: malformed input, an unusual request, or an ambiguous spot in the instructions.
- Be realistic: file paths, column names, personal context ("my manager wants…"). "Process this data" tests nothing.
- Phrase prompts the way a user would, **without naming the skill**.

## Assertions and grading

Add assertions only for things that are objectively checkable:

- Good: "The output file is valid JSON", "The chart has labeled axes", "At least 3 recommendations".
- Bad: "The output is good" (vague), or "Uses exactly the phrase 'Total: $X'" (brittle).
- Leave subjective qualities (style, tone, polish) to human review.
- Grade with concrete evidence. A label without substance is a FAIL.
- Drop assertions that pass both with and without the skill: they measure nothing.

Always compare against a baseline: the same prompt **without** the skill (for a new skill), or with the **previous version** (for an update). Value is the delta in pass rate, weighed against extra time and tokens.

## Trigger queries

Only for auto-invocable skills. Write about 20 realistic queries:

- **8–10 should-trigger**: vary phrasing, explicitness (some never name the domain), detail and complexity, and bury the task inside a larger request in some of them. The most valuable ones are those where the connection isn't obvious.
- **8–10 should-not-trigger near-misses**: they share keywords with the skill but need something else (e.g. for a CSV-analysis skill: "update the formulas in my Excel budget", "write a script that loads this CSV into Postgres"). Obviously unrelated queries test nothing.
- Simple one-step requests may not trigger any skill, because Claude handles them alone. Make positives substantive.

When optimizing the description:

1. Split the queries 60/40 into train and validation sets, keeping both proportional.
2. Run each query 3 times. A query passes when its trigger rate is on the right side of 0.5.
3. Revise the description using **train failures only**, generalizing to the category instead of pasting keywords from a failed query.
4. Pick the iteration with the best **validation** score; that is often not the last one.
5. About five iterations is usually enough.

## Format A: plugin skills (`claude plugin eval`)

The suite lives at `<plugin-root>/evals/`, one directory per case:

```text
<plugin>/
├── .claude-plugin/plugin.json
└── evals/
    └── <case-name>/
        ├── prompt.md          # the user message + run limits
        ├── graders/
        │   ├── outcome.md     # checks the result
        │   └── skill-fired.md # checks the skill was used
        └── case.yaml          # optional: workspace setup (context.*)
```

`prompt.md`:

```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

<realistic request, not naming the skill>
```

Outcome grader (LLM judge; use `type: regex` for long file output or anything mechanical):

```markdown
---
type: llm
---

PASS if <what a correct response contains>.
FAIL if <what a wrong or missing response looks like>.
```

Skill-fired grader:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill-name>"'
---
```

For a should-not-trigger case, use the same grader with `min: 0`, `max: 0` and `arm: both`.

Notes:

- Grader types: `regex`, `tool_used`, `tool_order` and `file_exists` are free; `llm` and `baseline` call a judge model. There are no custom-code graders.
- Give each case one outcome grader and one process grader.
- Runs are isolated: an empty workspace, and no user/project CLAUDE.md, settings, skills or MCP servers. Put everything the task needs into the prompt or `case.yaml`.
- An explicit-only skill (`disable-model-invocation: true`) can't be auto-triggered. Start its prompts with `/<plugin>:<skill> …`.

Commands to give the user (run from the plugin root):

```bash
claude plugin eval init          # interactive: Claude proposes cases and graders
claude plugin eval .             # run every case, 3× with and 3× without the plugin
claude plugin eval evals/<case>/prompt.md   # run one case
claude plugin eval . --ablation none        # one arm only (cheaper while tuning graders)
```

## Format B: project / personal skills (`evals/evals.json`)

Inside the skill directory:

```json
{
  "skill_name": "<skill-name>",
  "evals": [
    {
      "id": 1,
      "prompt": "<realistic user message>",
      "expected_output": "<what success looks like>",
      "files": ["evals/files/<fixture>"],
      "assertions": ["<objectively checkable statement>"]
    }
  ]
}
```

Store trigger queries in `evals/trigger-queries.json`:

```json
[
  { "query": "<realistic prompt>", "should_trigger": true },
  { "query": "<near-miss prompt>", "should_trigger": false }
]
```

How the user runs them:

- **skill-creator plugin** (automates runs, grading, benchmark, viewer and description tuning): `/plugin install skill-creator@claude-plugins-official`, then ask it to evaluate the skill.
- **Manually**: run each prompt in a fresh session with the skill, then again with it turned off (`"skillOverrides": { "<name>": "off" }` in settings). Compare the outputs against the assertions.
- **Trigger check from the shell**: `claude -p "<query>" --output-format json`, then inspect the result for a `Skill` tool call whose input names the skill.

Results go in a sibling workspace, not in the skill: `<skill-name>-workspace/iteration-N/eval-<id>/{with_skill,without_skill}/`.

## Iterating

- Use three signals: failed assertions (specific gaps), human feedback (broader problems) and **transcripts** (why it went wrong).
- **Generalize**: fix the underlying issue, not the one test prompt.
- **Keep it lean**: if transcripts show wasted work, remove the instruction causing it. If pass rates plateau, try removing rules.
- If every run re-wrote the same helper, bundle it in `scripts/`.
- Stop when feedback is consistently empty, or when iterations stop improving the results.
