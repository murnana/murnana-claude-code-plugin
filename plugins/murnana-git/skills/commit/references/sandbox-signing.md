# When commit signing fails under the sandbox

Claude Code's Bash sandbox can keep commands away from the signing keys and credentials stored on the user's computer: the SSH agent (including 1Password's and its `op-ssh-sign` signer), `gpg-agent` and its pinentry, and the OS keyring or keychain that holds a passphrase. A signed commit then fails inside the sandbox, even though the same command works in the user's own terminal.

## Recognize it

The `git commit` output mentions signing, a key or an agent, for example:

- `error: gpg failed to sign the data` / `fatal: failed to write commit object`
- `Couldn't get agent socket?`, `Could not open a connection to your authentication agent`, `communication with agent failed`, `agent refused operation`
- `gpg: signing failed: No pinentry` / `Inappropriate ioctl for device` / `No secret key`
- `error: 1Password: ...` or a message from `op-ssh-sign`

To confirm, read the signing settings (pre-approved): `git config --get commit.gpgsign`, `git config --get gpg.format`, `git config --get gpg.ssh.program`, `git config --get user.signingkey`. Signing enabled plus an error like the above is this case, whichever signer is configured.

## What to do

- Stop. Do not commit unsigned (`--no-gpg-sign`, `-c commit.gpgsign=false`), do not change the signing settings, do not retry with the sandbox disabled on your own, and do not edit the user's Claude Code settings.
- Report the `git commit` output as-is, then tell the user, in Japanese, that the sandbox likely blocks the signing key or credentials on their computer and that `git commit` has to be excluded from the sandbox. Show this setting, to add to `.claude/settings.local.json` (this project only) or `~/.claude/settings.json` (all projects):

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

`excludedCommands` matches the text of the whole Bash call: every command in it must match, and a call with `cd`, `&&`/`||` chains, a `$(...)` substitution or an output redirect to a file stays sandboxed. So run `git commit` as a call of its own and feed the message on stdin (`git commit -F - <<'EOF'`), not through `-m "$(cat <<'EOF' ...)"`.
