---
name: project-instructions-create
description: Create or revise the "Instructions" text of a claude.ai Project. Interviews the user, then produces paste-ready instructions
argument-hint: "[project purpose, or existing instructions to revise]"
disable-model-invocation: true
allowed-tools: AskUserQuestion Read
---

# Project Instructions Builder

Build the text for a claude.ai Project's "Instructions" field in five steps: check existing information -> interview -> draft -> self-check -> present. `$ARGUMENTS`, if given, is the project's purpose, or existing instructions (or a path to them) to revise.

This skill is for claude.ai Projects. If the user actually wants instructions for Claude Code, say so and point to `/murnana-agent-config:rule-create` (rules) or CLAUDE.md instead of continuing.

## Language

- Talk to the user (questions, issue lists, explanations) in the language the user writes in.
- Write the generated instructions in English.
- Every generated set of instructions includes a "Language" section stating the language for responses and for questions to the user. Default: "the language I write in during the conversation."

## Principles for writing instructions

- **Be specific.** Not "be clear" but "state the conclusion in the first sentence."
- **Give the reason.** "Do X, because Y." A reason lets Claude generalize to cases the rule didn't anticipate.
- **Say what to do, not what to avoid.** Rephrase prohibitions as the desired behavior.
- **New-colleague test.** Would a colleague with no background follow this without confusion?
- **Plain wording.** Overusing ALWAYS / NEVER / CRITICAL causes overreaction.
- **Examples.** To align format or tone, include 1-3 good ones.
- **Short.** Don't duplicate project files; name the file to refer to.

## Procedure

### 1. Check existing information

Read the conversation, uploaded files and any existing instructions (use Read if given a path). Don't ask about anything already known.

**Revision mode** (existing instructions supplied): before interviewing, list the problems found, each as location, type (vague / contradictory / duplicated / missing Language section) and proposed fix. Then interview only about gaps and points the user must decide.

### 2. Interview

Ask with AskUserQuestion, one call per round, options where possible (the user can always answer freely via "Other"). Without AskUserQuestion, send a numbered list. Go Round 1 -> 2 -> 3 and skip questions already answered. Fill anything the user leaves open with a sensible default, and report the defaults in step 5.

**Round 1: required**
1. **Goal and typical requests**: what the user wants to do here, what "done" looks like, 2-3 example prompts.
2. **Claude's role**: e.g. proofreader, sparring partner, code reviewer, tutor.
3. **About the user**: position, expertise, what needs no explaining.
4. **Response language**: recommend (first option) "the language I write in during the conversation". Ask about exceptions, e.g. code comments in English, quoted terms kept as-is.

**Round 2: important**
5. **Background**: subject overview, terminology, tools and versions, constraints.
6. **Project files**: which files are uploaded, which is the source of truth, priority on conflict, what to do for topics not in the files (infer / research / say unknown).
7. **Response style**: length, structure (e.g. conclusion first), headings / bullets / tables, tone, form of deliverables.
8. **Way of working**: for ambiguous requests, ask first or assume and state assumptions? Suggest only, or carry out?

**Round 3: optional**
9. **Things to avoid and repeated corrections**: unhelpful past responses, disliked phrasing, feedback the user keeps giving. For each, ask what to do instead and why. Top-priority candidates.
10. **Quality checks**: what to verify before answering.
11. **Examples of good output**: sample answers or writing to imitate.
12. **Maintenance**: shared with others (then keep context), and how it will be updated.

### 3. Draft

Compile into English instructions with the template below. Always keep "Language"; delete sections that don't apply; add a short reason to each rule.

```
# Goal
(What the project achieves. 1-3 sentences.)

# Your role
(Claude's role and expertise.)

# About me
(Position, knowledge level, how much to explain.)

# Language
- Respond and ask questions in the language I write in during the conversation.
  (Replace if the user chose otherwise, e.g. "Always respond in Japanese.")
- (Exceptions, if any.)

# Background
(Subject, terminology, environment and versions, constraints.)

# Project files
- Treat XX.md as the source of truth, because ...
- When something isn't covered in the files, ...

# How to respond
- Tone, structure, length, formatting

# Way of working
- When a request is ambiguous, ...
- Suggest only / carry it out

# Things to watch for
- Instead of ..., do ... (because ...)

# Before answering
- Check that ...

# Examples
<example>
Request: ...
Good response: ...
</example>
```

### 4. Self-check

- "Language" section present, covering both responses and questions
- Principles above satisfied: specific, reasons given, no bare prohibitions, new-colleague test passed, no overused strong words
- No contradictory rules
- No long text duplicating the project files

### 5. Present and finalize

- Show the instructions in a code block so they can be copied as-is. If they contain code fences, wrap them in a longer outer fence.
- In revision mode, add a short summary of what changed and why.
- List any defaults you filled in.
- Ask at most 3 confirmation questions (e.g. "Is this length guideline right?").
- Suggest 2-3 test prompts: a typical request, an edge case, and one that checks the language rule.
- Remind the user that a new chat in the project is the surest way to apply updated instructions.

## Gotchas

- Updated instructions affect only chats started afterwards; an old chat keeps the old ones.
- Paste-ready means no commentary inside the code block; put explanations outside it.
- Don't copy project-file contents into the instructions; name the file and the rule for using it.
