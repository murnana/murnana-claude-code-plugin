---
name: skill-create
description: Create or update a Claude Code skill (SKILL.md plus supporting files) in .claude/skills/ (project), ~/.claude/skills/ (personal), or a plugin's skills/ directory
argument-hint: "[what the skill should do]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Write Edit AskUserQuestion Bash(ls *) Bash(git ls-files *) Bash(git rev-parse *) Bash(claude plugin validate *)
---

# Skill Create

Create (or update) one Claude Code skill that follows the official format and authoring best practices, and scaffold the evals that prove it works.

## Current state

Run these first to see where skills already live:

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
ls -d .claude/skills/*/ 2>/dev/null || true
ls -d plugins/*/skills/*/ skills/*/ 2>/dev/null || true
ls .claude-plugin/plugin.json .claude-plugin/marketplace.json 2>/dev/null || true
```

Treat `$ARGUMENTS` (if any) as a hint about what the skill should do. It doesn't skip any of the steps below.

## Ground rules

- The generated skill (SKILL.md, references, eval prompts) is **always written in English**, whatever language the conversation uses. Interview the user in the conversation's language.
- Format, fields and loading semantics: [references/skill-format.md](references/skill-format.md). Never invent frontmatter fields, because unknown fields are silently ignored.
- A skill is only as good as the real expertise in it. Don't fill gaps with generic advice ("handle errors appropriately"). Ask the user, or read the repo.
- Never write a file before Step 8 approval.

Copy this checklist into your response and update it as you go:

```
- [ ] 1 Survey existing skills
- [ ] 2 Confirm a skill is the right tool
- [ ] 3 Gather intent
- [ ] 4 Design name, frontmatter, layout
- [ ] 5 Draft
- [ ] 6 Scaffold evals
- [ ] 7 Self-review
- [ ] 8 Present and get approval → write
- [ ] 9 Validate and hand off
```

## Step 1: Survey existing skills

- Glob `~/.claude/skills/*/SKILL.md` for personal skills. Use Glob, not `ls`: a sandboxed Bash may be denied outside the project. Also glob the project and plugin skills shown above.
- Read the frontmatter of any skill whose name or description is close to the request:
  - **Same name** → propose updating that skill instead of creating a new one.
  - **Overlapping description** → the two will compete for triggering. Plan a clear boundary, or merge them.
- Note the target location's conventions: naming pattern, `references/` layout, language. In a plugin marketplace repo, also note the per-plugin docs and the `plugin.json` / `marketplace.json` entries.

## Step 2: Confirm a skill is the right tool

- Check the request against [references/skill-vs-alternatives.md](references/skill-vs-alternatives.md).
- If a CLAUDE.md line, rule, hook, subagent, MCP server or permission fits better, or if Claude already does the task well without help, say so with the reason. Then ask (`AskUserQuestion`) whether to proceed with a skill anyway or stop. Do not build the alternative in this skill.

## Step 3: Gather intent

If the conversation already contains a worked example of the task, first extract its steps, the corrections the user made, the input/output formats and the project facts it used. Show them to the user to confirm.

Then ask with `AskUserQuestion`, but only for items that `$ARGUMENTS`, the conversation, Step 1 and the repo haven't answered. Batch up to 4 questions per call:

| Item | What to pin down |
|---|---|
| **Goal** | What Claude should be able to do, and what Claude gets wrong today without the skill (this is the skill's reason to exist) |
| **Triggers** | Phrases/contexts that should load it, and near-miss requests that must *not* |
| **Invocation** | Auto (default) / explicit `/name` only (anything with side effects: deploy, commit, send) / background knowledge only (`user-invocable: false`) |
| **Location** | Project `.claude/skills/`, personal `~/.claude/skills/`, or which plugin's `skills/` |
| **Inputs & output** | Arguments it takes; expected output format. For a strict format, get a template or a real example |
| **Source material** | Real steps, commands, paths, conventions, gotchas, docs/runbooks to read. If the user has none, ask them to point at examples in the repo |
| **Fragility** | Which parts must run exactly (low freedom: exact commands/scripts) vs. which are judgment calls (high freedom) |
| **Tools & deps** | Tools to pre-approve, CLIs/packages it assumes, MCP servers (fully qualified names), whether it should run isolated (`context: fork`) |
| **Success criteria** | How to tell the output is right. This drives Step 6 |

Don't ask what you can verify yourself (e.g. whether a command exists). Check it.

## Step 4: Design

- **Name**: kebab-case, ≤ 64 chars, no `claude` / `anthropic`. It should be specific (not `helper`, `utils`) and match its siblings' pattern (this repo uses verb-ish `noun-verb`, e.g. `rule-create`).
- **Frontmatter**: only the fields the skill needs (see [references/skill-format.md](references/skill-format.md)). Use minimal `allowed-tools`. `context: fork` only if the skill is a self-contained task, never for guideline-only content.
- **Layout**: keep SKILL.md under 500 lines; aim much lower.
  - Move detail into `references/` files linked **directly** from SKILL.md (one level deep). Each link says *when* to read the file.
  - Give any file over 100 lines a table of contents.
  - Put deterministic, repeated or fragile work in `scripts/` and say whether to *run* or *read* each script.
- **Freedom**: decide per section, from the fragility answers.

## Step 5: Draft

Follow [references/writing-guide.md](references/writing-guide.md). Key points:

- **Description**: what it does + when to use it, with the main use case first. Use the user's trigger words, and be slightly pushy about scope. Write in third person or "Use when…", never "I can…". Stay ≤ 1,024 chars for portability (Claude Code caps `description` + `when_to_use` at 1,536). Skip pushiness for explicit-only skills: their description is for humans in the `/` menu.
- **Body**:
  - Only what Claude wouldn't know. Give defaults, not menus, and procedures that generalize, not answers for one instance.
  - Include a **Gotchas** section with the concrete corrections.
  - Add a checklist for multi-step work, and a validate → fix → repeat loop wherever output can be checked.
  - Explain *why* instead of stacking ALL-CAPS MUSTs.
  - Put the most important instructions first: after compaction only the start of a skill may survive.
- **Specifics**: pull real commands, paths and examples from the repo, and read files to confirm them; don't guess. Use consistent terminology, nothing time-sensitive, and forward slashes in paths.

## Step 6: Scaffold evals

Follow [references/evals.md](references/evals.md). Write the files, but **never run them**: every eval run is a billed model call, so running is the user's decision.

- 2–3 realistic **output test cases** (prompt + expected output, optional input files), varied in phrasing and including one edge case. Add assertions only where they're objectively checkable.
- A **trigger query set** of about 20 queries: 8–10 that should trigger and 8–10 near-misses that shouldn't. Skip it for `disable-model-invocation: true` skills, since they never auto-trigger.
- **Format by location**:
  - **Plugin skill**: `claude plugin eval` cases under `<plugin>/evals/<case>/`. Each case has a `prompt.md`, an outcome grader, and a `tool_used: Skill` grader.
  - **Project or personal skill**: `evals/evals.json` (agentskills format) inside the skill directory, plus `evals/trigger-queries.json`.
- If the skill's output is purely subjective (style, tone), say so and keep evals to a human-review checklist instead.

## Step 7: Self-review

Check and fix before showing anything:

- [ ] Frontmatter starts on line 1, parses as YAML, uses only documented fields
- [ ] `name` valid and unique at its location; directory name matches
- [ ] Description says what + when, has the real trigger words, key use case first, ≤ 1,024 chars
- [ ] Invocation control matches side effects (side effects → `disable-model-invocation: true`)
- [ ] SKILL.md < 500 lines; nothing Claude would do anyway; no generic filler
- [ ] Every reference linked directly from SKILL.md with a "read when…"; TOC on files > 100 lines
- [ ] Every injected shell command (bang-backtick inline form or bang-fenced block) can't fail the load (`|| true` where needed), and every part of it (including `||` / `&&` / `|` segments) is allowed by `allowed-tools`. Never write a literal bang followed by a backtick in prose: it is executed too
- [ ] `allowed-tools` is minimal; scripts/CLIs it needs are listed with install hints
- [ ] Gotchas, checklist and validation loop present where the task warrants them
- [ ] Consistent terms; no time-sensitive info; no Windows paths; MCP tools fully qualified
- [ ] Evals: realistic prompts, near-miss negatives, checkable assertions

## Step 8: Present and get approval

- List every path to be written. For each one, say whether it's new or an update, and show the full content (a diff for updates).
- Mention any overlap found in Step 1 and how the draft resolves it.
- **Wait for approval**, then Write/Edit the files. In a plugin marketplace repo, also offer the manifest and docs updates its conventions call for.

## Step 9: Validate and hand off

- Run `claude plugin validate <skills-dir-or-plugin-dir>` and report the result. Fix any parse errors.
- Tell the user how to check it:
  - **Load**: `/name` runs it. For auto-invocable skills, "What skills are available?" lists it.
  - **Reload**: personal and project skills reload live; plugin skills need `/reload-plugins`. A plugin with `defaultEnabled: false` stays disabled even under `--plugin-dir`.
  - **Behavior**: test in a fresh session, on real tasks.
- Give the eval commands from [references/evals.md](references/evals.md) and remind them that runs cost usage.
- Iteration advice: when Claude has to be corrected while using the skill, add the correction to Gotchas. Read the transcripts, not just the outputs, and test on every model the skill will run on.
- For project or plugin skills, remind them to commit.

## References

- Format, fields, invocation, arguments, injection, lifecycle, troubleshooting:
  [references/skill-format.md](references/skill-format.md)
- Skill vs. CLAUDE.md / rule / hook / subagent / MCP / permission:
  [references/skill-vs-alternatives.md](references/skill-vs-alternatives.md)
- How to write the description and body; anti-patterns; quality checklist:
  [references/writing-guide.md](references/writing-guide.md)
- Output evals, trigger evals, `claude plugin eval` layout:
  [references/evals.md](references/evals.md)
