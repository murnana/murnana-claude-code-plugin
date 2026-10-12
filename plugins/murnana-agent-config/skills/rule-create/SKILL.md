---
name: rule-create
description: Create or update a Claude Code rule file in .claude/rules/ (project) or ~/.claude/rules/ (user)
argument-hint: "[topic or intent, e.g. testing, api conventions]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Write Edit AskUserQuestion Bash(ls *) Bash(git ls-files *) Bash(git rev-parse *)
---

# Rule Create

Create (or update) one rule file that Claude Code loads from `.claude/rules/` or `~/.claude/rules/`, following the official format and best practices.

## Current state

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
ls -R .claude/rules 2>/dev/null || true
ls CLAUDE.md .claude/CLAUDE.md CLAUDE.local.md AGENTS.md 2>/dev/null || true
```

Treat `$ARGUMENTS` (if any) as a hint about the rule's topic — it does not skip the steps below.

## Ground rules

- The rule's **body is always written in English**, regardless of the conversation language.
- Format and loading semantics: [references/rule-format.md](references/rule-format.md). Never invent frontmatter fields — `paths` is the only one Claude Code reads.
- Never write a file before Step 7 approval.

## Step 1: Survey existing instructions

- List user rules with the Glob tool (`~/.claude/rules/**/*.md`) — not `ls`, which a sandboxed Bash may be denied outside the project.
- Read the existing project and user rule files, plus the project `CLAUDE.md` / `.claude/CLAUDE.md` (and `AGENTS.md` if there is no CLAUDE.md).
- Note any rule that already covers the requested topic (→ propose updating it instead of creating a new one) and any instruction the new rule could contradict.

## Step 2: Confirm a rule is the right tool

- Check the request against [references/rule-vs-alternatives.md](references/rule-vs-alternatives.md).
- If it is better served by a skill, hook, permission rule, `CLAUDE.local.md`, or nothing at all, say so with the reason and ask the user (`AskUserQuestion`) whether to proceed with a rule anyway or stop. Do not build the alternative in this skill.
- If a "never do X" must actually be prevented, still allow the rule but tell the user it is advisory and recommend a permission deny / PreToolUse hook as well.

## Step 3: Gather intent

Ask with `AskUserQuestion` only for what `$ARGUMENTS`, the conversation, and Step 1 haven't already answered:

- **Scope**: project (`<repo>/.claude/rules/`, committed) or user (`~/.claude/rules/`, all projects)
- **Purpose**: one of the categories in [references/rule-content-by-purpose.md](references/rule-content-by-purpose.md)
- **Target files**: which directories / file types the rule is about (or "everywhere")
- **Key instructions**: what Claude currently gets wrong, or the conventions that must hold

## Step 4: Decide filename and `paths`

- Filename: descriptive kebab-case topic, `.md`; use a subdirectory if the rules dir already groups by area.
- Default to a path-scoped rule. Omit `paths` only when the rule is relevant to almost every session.
- Glob the candidate patterns against the repo (for project scope). If a pattern matches **zero** files, warn and fix it before continuing — such a rule never loads.
- Quote every pattern; prefer the YAML list form.

## Step 5: Draft

- Use the purpose's checklist in [references/rule-content-by-purpose.md](references/rule-content-by-purpose.md).
- Pull real details from the repo: actual commands (package scripts, Makefile, CI workflows), actual paths, a real example file to imitate. Read files to confirm; don't guess.
- Write imperative, verifiable bullets; add the *why* where it isn't self-evident; keep examples short.

## Step 6: Self-review

Before showing the draft, check and fix:

- [ ] Frontmatter is valid YAML with only `paths` (or none); patterns quoted and matching real files
- [ ] Under 200 lines (aim for 5–30)
- [ ] No item Claude would do anyway, no item derivable from the code, no procedure that belongs in a skill
- [ ] Every instruction is concrete enough to check
- [ ] No contradiction with CLAUDE.md, other project rules, or user rules (from Step 1)
- [ ] At most one `IMPORTANT`

## Step 7: Present and get approval

- Show the target path, whether it is new or an update, and the full file content exactly as it will be written (for an update, show the diff of what changes).
- Mention any contradiction or overlap found in Step 1 and how the draft resolves it.
- **Wait for approval.** Then Write (new) or Edit (update) the file.

## Step 8: Tell the user how to verify

- Unconditional rule: start a new session and check `/context` → **Memory files** (or `/memory`).
- Path-scoped rule: in a new session, have Claude Read a matching file, then check `/context`.
- If it doesn't load: run `claude --debug` to look for a frontmatter parse error (a broken frontmatter silently turns the rule unconditional).
- For project scope, remind them to commit the rule so the team gets it.

## References

- Format, loading, globs, symlinks, verification:
  [references/rule-format.md](references/rule-format.md)
- Rule vs. CLAUDE.md / skill / hook / permission:
  [references/rule-vs-alternatives.md](references/rule-vs-alternatives.md)
- What to write, per purpose:
  [references/rule-content-by-purpose.md](references/rule-content-by-purpose.md)
