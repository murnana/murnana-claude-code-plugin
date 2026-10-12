# Writing guide

How to write a skill that triggers when it should and helps when it loads. Condensed from the platform "Skill authoring best practices", agentskills.io "Best practices" and "Optimizing descriptions", and Anthropic's skill-creator.

## Contents

- What a good skill contains
- Writing the description
- Writing the body
- Patterns
- Anti-patterns

## What a good skill contains

| Part | Required? | Purpose |
|---|---|---|
| Specific `name` | Yes | Says what it does at a glance; consistent with sibling skills |
| `description` (what + when) | Yes | The *only* thing Claude sees when deciding to load it |
| One-line purpose at the top of the body | Yes | Orients Claude immediately |
| Workflow steps (checklist if > ~4 steps) | For procedures | Keeps Claude from skipping steps |
| Real commands, paths, examples | Yes | Real expertise is the value; generic advice isn't |
| Gotchas | Usually | Concrete corrections to mistakes Claude makes without being told |
| Output template / input→output examples | When format matters | Claude pattern-matches concrete structures better than prose |
| Validation loop / success criteria | When output is checkable | Claude iterates until the check passes instead of stopping at "looks done" |
| Links to references with "read when…" | When > ~200 lines of detail | Progressive disclosure keeps SKILL.md lean |
| Bundled scripts | For deterministic / fragile / repeated work | More reliable and cheaper than generated code |
| Evals | Yes, unless purely subjective | Proof it beats no skill |

## Writing the description

The description carries the whole burden of triggering, and Claude tends to *under*-trigger skills.

- **What + when**, with the main use case first, because truncation cuts from the end.
- **Use the words users actually say**, plus the implicit cases: "…even if they don't mention X explicitly."
- **Focus on user intent**, not internal mechanics.
- **Point of view**: third person ("Analyzes…") or imperative ("Use when…"). Never "I can help…" or "You can use this…".
- **Mark the boundary** when a neighbor skill or a common near-miss exists: "Not for X; use Y."
- **Length**: a few sentences, ≤ 1,024 chars, no XML tags.
- **Explicit-only skills** (`disable-model-invocation: true`): the description is shown to humans in the `/` menu, not to Claude. Keep it a short, plain summary.

```yaml
# Bad
description: Helps with documents
description: I can process your CSV files

# Good
description: >
  Analyze CSV and tabular data files: compute summary statistics, add derived
  columns, generate charts, and clean messy data. Use when the user has a CSV,
  TSV, or Excel file and wants to explore, transform, or visualize it, even if
  they don't say "CSV" or "analysis".
```

## Writing the body

- **Assume Claude is smart.** For each line ask: "Would Claude get this wrong without it?" If not, cut it. Don't explain what a PDF is or how git works.
- **Moderate detail beats exhaustive.** Concise, stepwise guidance with one working example outperforms covering every edge case. Instructions that don't apply to the current task still get followed and send Claude down wrong paths.
- **Match freedom to fragility.** Use prose heuristics where many approaches work (high freedom), a parameterized template where a preferred pattern exists (medium), and an exact command where the step is fragile ("Run exactly `scripts/migrate.py --verify --backup`. Do not add flags.") (low).
- **Defaults, not menus.** "Use pdfplumber. For scanned PDFs, use pdf2image + pytesseract instead." Don't write "you could use A, B, C or D".
- **Procedures over declarations.** Teach how to approach the class of problem, not the answer to one instance.
- **Explain why.** "Do X because Y causes Z" is followed more reliably, and generalizes better, than "ALWAYS do X". Treat a pile of capitalized MUSTs as a smell. Emphasize at most one truly critical line.
- **Most important first.** After compaction only the top of a skill may survive.
- **Standing rules.** The skill is loaded once and not re-read, so word guidance to apply to the whole task ("after every edit, run the tests").
- **Consistent terminology.** Pick one term ("field", "endpoint") and never switch.
- **No time-sensitive info.** Move deprecated approaches to a collapsed "Old patterns" section.
- **Say whether to run or read** each bundled script.

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
