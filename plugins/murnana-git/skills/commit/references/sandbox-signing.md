# When commit signing fails under the sandbox

Claude Code's Bash sandbox can block the 1Password SSH agent and the `op-ssh-sign` signer. A commit signed with a key kept in 1Password then fails inside the sandbox, even though the same command works in the user's own terminal.

## Recognize it

The `git commit` output mentions signing or the SSH agent, for example:

- `error: 1Password: ...` or a message from `op-ssh-sign`
- `error: gpg failed to sign the data` / `fatal: failed to write commit object`
- `Couldn't get agent socket?`, `Could not open a connection to your authentication agent`, `communication with agent failed`, `agent refused operation`

To confirm, read the signing settings (pre-approved): `git config --get commit.gpgsign`, `git config --get gpg.format`, `git config --get gpg.ssh.program`. A `gpg.ssh.program` that names `op-ssh-sign` or 1Password confirms the case. Other signers (GPG, plain `ssh-agent`) can fail the same way; give the same guidance.

## What to do

- Stop. Do not commit unsigned (`--no-gpg-sign`, `-c commit.gpgsign=false`), do not retry with the sandbox disabled on your own, and do not edit the user's settings.
- Report the `git commit` output as-is, then tell the user, in Japanese, that the sandbox blocks the 1Password key and that `git commit` has to be excluded from the sandbox. Show this setting, to add to `.claude/settings.local.json` (this project only) or `~/.claude/settings.json` (all projects):

  ```json
  {
    "sandbox": {
      "excludedCommands": ["git commit *"]
    }
  }
  ```

  Mention that an excluded command runs outside the sandbox with the user's full access, and link to https://code.claude.com/docs/en/sandboxing for details.
- Ask with `AskUserQuestion` whether to retry once the setting is in place (「設定したので再試行する」「中止する」). On retry, run the same `git add` and `git commit` again.

## Keep the call matchable

`excludedCommands` matches the text of the whole Bash call, and a call with `cd`, `&&` chains, a `$(...)` substitution or an output redirect to a file stays sandboxed. So run `git commit` as a call of its own and feed the message on stdin (`git commit -F - <<'EOF'`), not through `-m "$(cat <<'EOF' ...)"`.
