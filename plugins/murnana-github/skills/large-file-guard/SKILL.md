---
name: large-file-guard
description: Install a hook that blocks git commit when a non-LFS file is too large for GitHub to accept on push.
disable-model-invocation: true
allowed-tools: Bash(git rev-parse --show-toplevel) Bash(command -v jq) Bash(mkdir -p .claude/hooks) Bash(cp ${CLAUDE_SKILL_DIR}/scripts/check-git-file-size.sh .claude/hooks/check-git-file-size.sh) Bash(chmod +x .claude/hooks/check-git-file-size.sh) Bash(jq empty *) Read Glob AskUserQuestion
---

# Large file guard

Set up a `PreToolUse` hook in the current repository. Before Claude runs `git commit`, the hook checks the size of every file that would be committed and stops the commit when GitHub would reject the push. Files tracked by Git LFS are not counted, because Git stores only a small pointer for them.

Limits the hook enforces (details and sources: [references/github-limits.md](references/github-limits.md)):

- 50 MiB or more: the commit goes ahead, but Claude is told to warn the user.
- 100 MiB or more: the commit is blocked (exit code 2) and Claude must ask the user how to proceed.

Treat `$ARGUMENTS` (if any) as the settings scope or limits the user wants. It does not skip the steps below.

## Steps

1. Run `git rev-parse --show-toplevel`. If it fails, stop and say this is not a git repository. Work from that directory in every step below (the paths are relative to it).
2. Run `command -v jq`. The hook reads the tool input with `jq`. If it prints nothing, stop and tell the user to install `jq` first.
3. `Glob` for `.claude/settings.json` and `.claude/settings.local.json`, and `Read` each one that exists. Note whether a `PreToolUse` entry whose command contains `check-git-file-size.sh` is already registered.
4. Ask the user with one `AskUserQuestion` call (skip a question that `$ARGUMENTS` already answers):
   - Where to register the hook: `.claude/settings.json` (committed, shared with the team; recommended) or `.claude/settings.local.json` (this checkout only). Show the file that already has the entry, if step 3 found one, and say the install will refresh the script only.
   - Whether to keep the default limits (warn at 50 MiB, block at 100 MiB; recommended) or set different ones. Different limits go into the hook command as environment variables (see step 7).
5. Run `mkdir -p .claude/hooks`, then `cp ${CLAUDE_SKILL_DIR}/scripts/check-git-file-size.sh .claude/hooks/check-git-file-size.sh`, then `chmod +x .claude/hooks/check-git-file-size.sh`. If `.claude/hooks/check-git-file-size.sh` already existed (step 3 `Glob` it too), say that it was overwritten with the bundled version.
6. If the entry from step 3 is already registered in the chosen file, skip to step 8.
7. Merge this entry into the chosen settings file with the `Edit` tool. Keep every existing key and hook as it is: add to an existing `hooks.PreToolUse` array instead of replacing it, and create the file with `Write` only if it does not exist.

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             {
               "type": "command",
               "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-git-file-size.sh"
             }
           ]
         }
       ]
     }
   }
   ```

   For custom limits, prefix the command: `GIT_FILE_SIZE_WARN_MIB=30 GIT_FILE_SIZE_BLOCK_MIB=80 "$CLAUDE_PROJECT_DIR"/.claude/hooks/check-git-file-size.sh`.
8. Run `jq empty <the settings file>`. If it reports an error, fix the JSON you wrote and run it again; do not leave an invalid settings file.
9. Report in Japanese: the files created or changed, the active limits, and what the hook cannot see:
   - Only the Bash tool's `git commit` is checked. Commits made from a terminal, an IDE or another tool are not.
   - A `git add <big file> && git commit` in one command is checked before the `git add` runs, so the file is not seen. Stage in a separate command first.
   - Only per-file sizes are checked, not the size of the whole push or the repository.
   - Settings are read at session start; tell the user to open `/hooks` or restart Claude Code if the hook does not show up.

## When the hook blocks a commit

The hook prints the file list and the options. Do not retry the same commit and do not bypass the hook. Ask the user with `AskUserQuestion` whether to track the files with Git LFS (`git lfs track '<pattern>'`, which needs `git-lfs` installed), leave them out of the commit and add them to `.gitignore`, or split or compress them.

## References

- GitHub's file size limits and how the hook measures size: [references/github-limits.md](references/github-limits.md)
