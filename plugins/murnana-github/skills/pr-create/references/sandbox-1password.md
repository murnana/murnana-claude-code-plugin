# When the push fails under the sandbox

Claude Code's Bash sandbox can block the 1Password SSH agent. When the remote is reached over SSH with a key kept in 1Password, `git push` (or `gh stack submit`, which pushes) then fails inside the sandbox, even though the same command works in the user's own terminal.

## Recognize it

The remote URL in Current state is SSH (`git@...` or `ssh://...`), and the push output mentions the key or the agent, for example:

- `Permission denied (publickey)`
- `sign_and_send_pubkey: signing failed`, `communication with agent failed`, `agent refused operation`
- `Could not open a connection to your authentication agent`, or a message from 1Password

If `gh pr create` fails only with an authentication error after `gh auth status` succeeded, the sandbox may also be blocking the credential store `gh` uses. Give the same guidance for that command.

## What to do

- Stop, as Step 4 requires. Do not switch the remote to HTTPS, do not retry with the sandbox disabled on your own, and do not edit the user's settings.
- Report the output as-is, then tell the user, in Japanese, that the sandbox blocks the 1Password key and that the failing command has to be excluded from the sandbox. Show this setting, to add to `.claude/settings.local.json` (this project only) or `~/.claude/settings.json` (all projects), keeping only the entries for the commands that failed:

  ```json
  {
    "sandbox": {
      "excludedCommands": ["git push *", "gh stack submit *", "gh pr create *"]
    }
  }
  ```

  Mention that an excluded command runs outside the sandbox with the user's full access, and link to https://code.claude.com/docs/en/sandboxing for details.
- Ask with `AskUserQuestion` whether to retry once the setting is in place (「設定したので再試行する」「中止する」). On retry, resume from the step that failed.

## Keep the call matchable

`excludedCommands` matches the text of the whole Bash call, and a call with `cd`, `&&` chains, a `$(...)` substitution or an output redirect to a file stays sandboxed. Run `git push` and `gh pr create` as calls of their own, and feed the body on stdin (`--body-file - <<'EOF'`), not through `$(...)`.
