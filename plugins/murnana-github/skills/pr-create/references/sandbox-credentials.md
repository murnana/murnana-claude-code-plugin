# When GitHub credentials are blocked by the sandbox

Claude Code's Bash sandbox can keep commands away from the credentials stored on the user's computer: the token `gh` keeps in the OS keyring (macOS Keychain, Windows Credential Manager, Secret Service), the git credential helper used for HTTPS remotes, and the SSH agent (including 1Password's) used for SSH remotes. The same command then works in the user's own terminal but fails inside the sandbox.

## Recognize it

- `gh auth status` reports no login, a failed keyring/keychain read, or an invalid token, while `gh` itself is installed. Ask yourself whether the user would plausibly be logged in (they ran this skill to create a PR); if so, suspect the sandbox before the MCP fallback.
- `gh pr create`, `gh repo view` or `gh stack submit` fails with an authentication error (`HTTP 401`, `authentication required`, `gh auth login`).
- `git push` fails on credentials:
  - HTTPS remote: `could not read Username`, `Authentication failed`, `terminal prompts disabled`
  - SSH remote: `Permission denied (publickey)`, `sign_and_send_pubkey: signing failed`, `communication with agent failed`, `Could not open a connection to your authentication agent`

## What to do

- Stop. Do not switch the remote between HTTPS and SSH, do not run `gh auth login`, do not retry with the sandbox disabled on your own, and do not edit the user's settings.
- Report the output as-is, then tell the user, in Japanese, that the sandbox likely blocks the GitHub credentials on their computer and that the commands have to be excluded from the sandbox. Show this setting, to add to `.claude/settings.local.json` (this project only) or `~/.claude/settings.json` (all projects):

  ```json
  {
    "sandbox": {
      "excludedCommands": ["gh auth status *", "gh repo view *", "gh pr *", "gh stack *", "git push *"]
    }
  }
  ```

  Mention that an excluded command runs outside the sandbox with the user's full access (they may trim the list to the commands that failed), and link to https://code.claude.com/docs/en/sandboxing for details.
- In the same `AskUserQuestion` call, offer: 「設定したので再試行する」, GitHub MCP server fallback ([gh-fallback-mcp.md](gh-fallback-mcp.md)), and 「中止する」. On retry, run `gh auth status` on its own (no `2>&1 || true`, so the exclusion matches) and resume from the step that failed.

## Keep the call matchable

`excludedCommands` matches the text of the whole Bash call: every command in it must match, and a call with `cd`, `&&`/`||` chains, a `$(...)` substitution or an output redirect to a file stays sandboxed. Run `git push` and each `gh` command as a call of its own, and feed a body on stdin (`--body-file - <<'EOF'`), not through `$(...)`.
