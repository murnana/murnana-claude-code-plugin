# Writing guide

How to write a skill that triggers when it should and helps when it loads. Condensed from the platform "Skill authoring best practices" and "Prompting best practices" (with the per-model Haiku and Sonnet pages), agentskills.io "Best practices" and "Optimizing descriptions", and Anthropic's skill-creator.

## Contents

- What a good skill contains
- Writing the description and when_to_use
- Writing the body
- Writing for Haiku and Sonnet
- Keeping token use low
- Patterns
- Anti-patterns

## What a good skill contains

| Part | Required? | Purpose |
|---|---|---|
| Specific `name` | Yes | Says what it does at a glance; consistent with sibling skills |
| `description` (what it is) + `when_to_use` (triggers) | Yes (`when_to_use` for auto-invocable skills) | The *only* text Claude sees when deciding to load it |
| One-line purpose at the top of the body | Yes | Orients Claude immediately |
| Workflow steps (checklist if > ~4 steps) | For procedures | Keeps Claude from skipping steps |
| Real commands, paths, examples | Yes | Real expertise is the value; generic advice isn't |
| Gotchas | Usually | Concrete corrections to mistakes Claude makes without being told |
| Output template / input→output examples | When format matters | Claude pattern-matches concrete structures better than prose |
| Validation loop / success criteria | When output is checkable | Claude iterates until the check passes instead of stopping at "looks done" |
| Links to references with "read when…" | When > ~200 lines of detail | Progressive disclosure keeps SKILL.md lean |
| Bundled scripts | For deterministic / fragile / repeated work | More reliable and cheaper than generated code |
| Evals | Yes, unless purely subjective | Proof it beats no skill |

## Writing the description and when_to_use

Claude Code puts `description` and `when_to_use` of every auto-invocable skill into the skill listing, which is sent with every request of every session where the skill is enabled. Each word is a recurring cost, so keep the two fields small and give each one a single job.

- **`description` says what the skill is.** One short sentence in third person ("Analyzes…", "Creates…"), about 15 words or fewer. No trigger phrases, no example prompts, no "Use when…". Never "I can help…" or "You can use this…".
- **`when_to_use` says when to load it.** A YAML block scalar with 2–5 bullets. Each bullet is one kind of request or situation, described in English with the key words users actually use, including an implicit case where the user doesn't name the domain. Don't quote example prompts: Claude matches the meaning in any language, and quotes (in Japanese especially) cost more tokens. Add one `- Not for: …` bullet when a neighbor skill or a common near-miss exists.
- **Budget**: both fields together at most about 100 tokens, which is about 60 English words; fewer is better. Cut whatever Claude can infer from the skill name, and drop adjectives and examples first.
- **Explicit-only skills** (`disable-model-invocation: true`): the listing is not in Claude's context; the description is only shown to humans in the `/` menu. Write a short description and no `when_to_use`.
- No angle brackets (they display as `&lt;` and `&gt;`); write `[branch]` instead of `<branch>`.

```yaml
# Bad: triggers and examples packed into description, far over budget
description: >
  Analyze CSV and tabular data files: compute summary statistics, add derived
  columns, generate charts, and clean messy data. Use when the user has a CSV,
  TSV, or Excel file and wants to explore, transform, or visualize it, even if
  they don't say "CSV" or "analysis".

# Good: about 35 words in total
description: Analyzes CSV and Excel files and charts the results.
when_to_use: |
  - User shares a CSV, TSV or .xlsx file to explore or clean
  - User asks for summary stats or a chart of tabular data
  - Not for: loading data into a database
```

## Writing the body

- **Assume Claude is smart about the world, not about your procedure.** For each line ask: "Would Claude get this wrong without it?" If not, cut it. Don't explain what a PDF is or how git works. Do spell out the steps, commands, defaults and done-criteria of your task: that is where smaller models go wrong (next section).
- **Moderate detail beats exhaustive.** Concise, stepwise guidance with one working example outperforms covering every edge case. Instructions that don't apply to the current task still get followed and send Claude down wrong paths.
- **Match freedom to fragility.** Use prose heuristics where many approaches work (high freedom), a parameterized template where a preferred pattern exists (medium), and an exact command where the step is fragile ("Run exactly `scripts/migrate.py --verify --backup`. Do not add flags.") (low).
- **Defaults, not menus.** "Use pdfplumber. For scanned PDFs, use pdf2image + pytesseract instead." Don't write "you could use A, B, C or D".
- **Procedures over declarations.** Teach how to approach the class of problem, not the answer to one instance.
- **Explain why, briefly.** "Do X because Y causes Z" is followed more reliably, and generalizes better, than "ALWAYS do X". Keep the reason to a clause; the body stays in context for the whole session, so don't narrate. Treat a pile of capitalized MUSTs as a smell: newer models over-apply them. Emphasize at most one truly critical line.
- **Most important first.** After compaction only the top of a skill may survive.
- **Standing rules.** The skill is loaded once and not re-read, so word guidance to apply to the whole task ("after every edit, run the tests").
- **Consistent terminology.** Pick one term ("field", "endpoint") and never switch.
- **No time-sensitive info.** Move deprecated approaches to a collapsed "Old patterns" section.
- **Say whether to run or read** each bundled script.

## Writing for Haiku and Sonnet

A skill runs on whatever model the session uses: Haiku, Sonnet or Opus (or the one in its `model` field). Opus fills gaps in loose instructions; Haiku and Sonnet follow the text literally, skip or reorder loosely described steps, don't carry an instruction from one item over to the next, and, in long prompts at low effort, may stop before the work is done or skip a tool call. Unless the user names a single model, write so that Haiku succeeds; that costs Opus little.

| Do this | Because |
|---|---|
| Write each procedure as **numbered steps**, one action per step | Order and completeness hold only when they are explicit |
| In each step, name the **exact tool or command**, say **how to read the result**, and say **where to go for each outcome** ("empty → Step 4; error → stop and report") | A step that says only "check X" gets skipped or done differently each run |
| Make every required tool call its own step ("Call WebFetch on…", "Run `npm test`") | Smaller models skip searches and checks that are only implied |
| Give a **default for every decision**, as a "condition → action" table where there are several cases | "Use your judgment" yields different answers on each run |
| **State the scope**: "for every file", "in each section", "repeat for each finding" | A literal model applies the instruction to the first item only |
| Say **what to do**, not only what to avoid | "Write X" is followed more reliably than "Don't write Y" |
| Put the **template or 1–3 examples** right where the output is produced | Models match concrete structures better than prose descriptions |
| Say **when the work is done** (the checklist is all ticked, the validator passes) and add "keep going until then; stop only to ask or before a risky step" | Without a finish line, long tasks end early and hand the work back |
| Add a **verify step** after each change that can be checked (tests, build, validator, re-reading the file) | Smaller models report work as done without checking it |
| Link each reference **at the step that needs it** ("Read `references/x.md` now") | A link listed only at the end is often never opened |
| **Keep SKILL.md short**; move branch-specific detail to references | Long prompts raise early stopping and missed steps on smaller models |
| Use **one term** per concept, and the same step names everywhere ("Step 4", not "the interview" in one place and "Step 4" in another) | Literal models treat different words as different things |

Check: read the draft as a model that does exactly what the text says and nothing more. Wherever it would have to guess (which command, what counts as success, what to do on failure), add the missing line. Then test on each target model (`claude --model haiku`, `claude --model sonnet`) and read the transcripts.

## Keeping token use low

A skill costs tokens in three places: the listing (every request, every session), the body (every request after it loads, for the rest of the session), and what its steps pull in (tool results stay in context too). Explicit steps for Haiku and few tokens are not in conflict: cut background and narration, keep the steps.

| Where | Technique |
|---|---|
| Listing | Keep `description` + `when_to_use` at about 100 tokens or less. Use `disable-model-invocation: true` for skills the user starts by name, and `paths` for skills tied to certain files, so the listing entry is absent when it can't help |
| Body | Every line is a recurring cost. Cut what Claude does right without being told. Move detail that only some runs need to a reference file read at the step that needs it. Put the essentials in the first 5,000 tokens, which is what survives compaction |
| Scripts | A bundled script is executed, not loaded: only its output costs tokens. Make the script print a short result (counts, failures, the lines that matter), not everything |
| Injected context | A bang-fenced block runs before Claude sees the skill and saves a tool round trip. Inject only short outputs (`git status -sb`, `git log --oneline -10`), never a full file or log |
| Commands | Ask for less output: `--oneline`, `--stat`, `--name-only`, `-q`, `--format`, a count or line limit, JSON with a field filter. Prefer a CLI (`gh`, `aws`) over an MCP server when both work |
| Reading | Grep or Glob first, then Read only what matches, with an offset and limit for large files. Never re-read a file that is already in context, including `CLAUDE.md` and rules loaded at session start |
| Verbose work | Send test runs, log scans, wide searches and doc fetching to a subagent (`model: haiku` or `sonnet` for mechanical work) so only its summary returns. WebFetch with a narrow prompt returns a short answer instead of the page |
| Turns | Each turn resends the whole context. Batch questions into one `AskUserQuestion` call, and batch independent tool calls into one message |
| Output to the user | Show diffs, not whole files, for updates. Report results in a few lines; don't repeat what the user already saw |

## Patterns

**Gotchas** (keep these in SKILL.md, so Claude reads them before hitting the situation):

```markdown
## Gotchas
- `users` uses soft deletes: always add `WHERE deleted_at IS NULL`.
- `/health` returns 200 even when the DB is down; use `/ready`.
```

**Checklist** (for multi-step workflows): a fenced `- [ ]` list Claude copies into its response and ticks off.

**Validation loop**: do the work → run a validator (script, linter, or a reference checklist) → fix → repeat → proceed only when it passes. Make validator errors specific ("Field 'x' not found. Available: a, b, c").

**Plan → validate → execute** (for batch or destructive work): write the plan to a structured file, validate it against the source of truth, then apply it.

**Template**: give the exact output skeleton. Say whether it is strict ("ALWAYS use this structure") or a sensible default ("adapt as needed").

**Examples**: 2–3 input → output pairs convey style better than a description.

**Conditional workflow**: "Creating new? → section A. Editing existing? → section B." Move a large branch to its own reference file.

**Domain split**: one reference file per domain or variant (`references/aws.md`, `references/gcp.md`) so only the relevant one loads.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Generic best-practice filler ("follow security best practices") | Replace with the concrete project fact, or delete |
| Vague names (`helper`, `utils`, `tools`) | Name the activity (`pdf-processing`, `release-notes`) |
| Offering many equal options | One default + one escape hatch |
| References linking to references | Link everything directly from SKILL.md |
| Long reference with no TOC | Add `## Contents` at the top |
| Windows paths (`scripts\run.py`) | Forward slashes |
| Magic numbers in scripts (`TIMEOUT = 47`) | Justify each constant in a comment |
| Scripts that crash and leave the fix to Claude | Handle the error in the script, with a clear message |
| Assuming a package/CLI is installed | State the dependency and the install command |
| Bare MCP tool names | Fully qualified `ServerName:tool_name` |
| `context: fork` on a guideline-only skill | Remove it; forks need an explicit task |
| Side-effecting skill left auto-invocable | `disable-model-invocation: true` |
| Content that would surprise the user given the description | The skill must do only what its description says |
| Steps like "check the config" or "handle failures" with no command or outcome | Name the command, how to read its result, and the next step for each outcome |
| A decision left to judgment with no default | Give the default, plus the condition for the alternative |
| Trigger phrases in `description`, or a description over a sentence | One sentence on what it is; triggers as bullets in `when_to_use` |
| A step that dumps a full log, file or command output into context | Limit the output, Grep for what matters, or hand the step to a subagent |
| Rules from your memory of a tool's behavior | Check the tool's current official docs and the version the project pins |
| Skill rules that contradict the project's CLAUDE.md or rules | Follow the project's instructions; the skill is the fallback |
