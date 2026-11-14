# Is a subagent the right tool?

Decide this before designing. A subagent is a separate worker: it starts with an empty context, does one job, and returns one report. Find the row that matches the job. If the "Use" column is not **Subagent**, propose that tool instead and let the user decide.

| The job is… | Use | Why not a subagent |
|---|---|---|
| Reading many files or pages when the main conversation needs only the conclusion (review, audit, research) | **Subagent** | (the sweet spot) |
| A second opinion that must not be influenced by the conversation so far | **Subagent** | (the sweet spot) |
| A specialist that needs fewer tools than the main conversation (read-only reviewer) | **Subagent** | (the sweet spot) |
| Independent pieces of work that can run in parallel | **Subagent** | (the sweet spot) |
| Noisy work (test runs, log reading) whose output would fill the main context | **Subagent** | (the sweet spot) |
| A multi-step procedure Claude follows in the main conversation ("how to release") | **Skill** | The steps need the conversation and the user's replies |
| Work that asks the user questions or needs approval along the way | **Skill** | A subagent cannot ask the user anything |
| Work that needs most of what was said and read so far | **Fork** (`/subtask`), or do it in the main conversation | A subagent would need the whole background re-explained |
| Edits the user wants to watch and steer one by one | Main conversation | Only the final report comes back |
| A convention for certain files | **Path-scoped rule** | A subagent isn't loaded when those files are edited |
| "Every time X happens, do Y" with no exceptions | **Hook** | Delegation is Claude's choice; a hook always runs |
| A quick, small task | **Nothing** | Starting a subagent costs a fresh context and a restated task |
| A job an existing subagent already does | **Update that subagent** | Two similar descriptions compete for delegation |

## Combinations that work

- **Skill + subagent**: the skill runs the workflow in the main conversation and tells Claude when to hand one self-contained part (a review, a search) to the subagent.
- **Subagent + hook** (project or personal only): the body says what not to do, and a `PreToolUse` hook blocks it.

## Scope: one job

- **Too broad** ("helps with backend work"): the description can't say when to delegate, and the body can't fix a report format.
- **Too narrow** ("checks line 3 of config.yml"): a one-off task, not a role.
- Right: one role with one kind of result, such as "reviews a diff and reports problems by severity".
