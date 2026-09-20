# When `gh` is unavailable

## Step 1: Confirm the diagnosis

Show the user exactly what failed — the output of `gh auth status` from the dynamic context block, and, if `gh` itself is missing, the shell's "command not found".

## Step 2: Ask, don't act

Use `AskUserQuestion` with options along the lines of:

- Install the `gh` CLI
- Configure the GitHub MCP server
- Abort

Never silently install a CLI tool or edit MCP configuration — both are environment-level changes that need explicit consent.

## Step 3a: If the user chooses to install `gh`

Point them to the official install instructions for their platform rather than guessing a package manager command; only run an install command they've explicitly approved:

- macOS (Homebrew): <https://github.com/cli/cli/blob/trunk/docs/install_macos.md#homebrew>
- Windows (WinGet): <https://github.com/cli/cli/blob/trunk/docs/install_windows.md#winget>
- Linux: <https://github.com/cli/cli/blob/trunk/docs/install_linux.md>

After install, re-run `gh auth status` and continue the skill from Step 1.

## Step 3b: If the user chooses the GitHub MCP server

Point to <https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md> for the setup procedure (a GitHub PAT or OAuth, then `claude mcp add` or an `.mcp.json` entry) — link only, don't inline the whole guide here.

Once the MCP server is configured:

- Re-map the skill's `gh pr create` / `gh pr view` / `gh repo view` calls to the equivalent MCP tool calls (e.g. `create_pull_request`, `get_pull_request`, `get_repository`). Tool names may differ by server version — check the available MCP tools at runtime rather than hardcoding them.
- This plugin's `allowed-tools` is scoped to `Bash(gh ...)` forms only, so MCP tool calls are **not** pre-authorized — the user will see a normal permission prompt for each one. This is expected; do not try to work around it.
