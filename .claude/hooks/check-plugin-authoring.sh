#!/bin/sh
# PostToolUse hook: after Claude edits a plugin skill (plugins/*/skills/*/SKILL.md) or a plugin
# subagent (plugins/*/agents/**/*.md), fail on the mistakes that a rule alone can't prevent.
# Exit 2 feeds stderr back to Claude.
# See .claude/rules/plugin-skill-authoring.md and .claude/rules/plugin-agent-authoring.md for why.

file=$(jq -r '.tool_input.file_path // empty' | tr '\\' '/')
case "$file" in
  */plugins/*/skills/*/SKILL.md) kind=skill ;;
  */plugins/*/agents/*.md) kind=agent ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

src=$(tr -d '\r' < "$file")
# Frontmatter: the lines between a "---" on line 1 and the next "---".
fm=$(printf '%s\n' "$src" | awk 'NR==1 { if ($0 != "---") exit; next } $0 == "---" { exit } { print }')
errors=""
add() { errors="${errors}- $1
"; }

if [ -z "$fm" ]; then
  add "No YAML frontmatter: the file must start with '---' on line 1."
fi

if [ "$kind" = skill ]; then
  # allowed-tools: the value on its own line plus any YAML list lines that follow.
  tools=$(printf '%s\n' "$fm" | awk '/^allowed-tools:/ { on=1; print; next } on && /^[A-Za-z_-]+:/ { on=0 } on { print }')

  # A frontmatter field: its own line plus any indented lines that follow (block scalars).
  field() { printf '%s\n' "$fm" | awk -v k="$1" '$0 ~ ("^" k ":") { on=1; print; next } on && /^[A-Za-z_-]+:/ { on=0 } on { print }'; }
  desc=$(field description)
  wtu=$(field when_to_use)

  if printf '%s\n%s\n' "$desc" "$wtu" | LC_ALL=C grep -q '[^ -~]'; then
    add "'description' or 'when_to_use' has non-ASCII characters: write both in English, without Japanese trigger phrases."
  fi
  if printf '%s\n' "$desc" | grep -qiE 'use (this skill |this |it )?when'; then
    add "'description' says when to use the skill: keep it to one sentence on what the skill is, and move triggers to 'when_to_use' bullets."
  fi
  if [ -n "$wtu" ]; then
    if printf '%s\n' "$fm" | grep -qiE '^disable-model-invocation:[[:space:]]*(true|yes|on|1)[[:space:]]*$'; then
      add "Remove 'when_to_use': an explicit-only skill's listing is not in Claude's context."
    fi
    if printf '%s\n' "$wtu" | head -n 1 | grep -qE '^when_to_use:[[:space:]]*(\[.*)?$'; then
      add "'when_to_use' is a YAML list or empty: it is a string, so write 'when_to_use: |' followed by indented '- ' bullets."
    fi
  fi
  # About 60 words (~100 tokens) is the target; reject clearly oversized listings.
  words=$(printf '%s\n%s\n' "$desc" "$wtu" | sed -E 's/^(description|when_to_use):[[:space:]]*[|>]?[-+]?//; s/^[[:space:]]*- //' | wc -w | tr -d ' ')
  if [ "${words:-0}" -gt 70 ]; then
    add "'description' + 'when_to_use' is ${words} words: keep it to about 60 words (about 100 tokens); fewer is better."
  fi
  old=$(printf '%s\n' "$tools" | grep -oE 'Bash\([^)]*:\*\)' | tr '\n' ' ')
  if [ -n "$old" ]; then
    add "Old ':*' form in allowed-tools: ${old}-> write 'Bash(cmd *)'."
  fi
  broad=$(printf '%s\n' "$tools" | grep -oE 'Bash\((\*|git \*|gh \*|git config \*)\)' | tr '\n' ' ')
  if [ -n "$broad" ]; then
    add "Too broad in allowed-tools: ${broad}-> list only the exact command shapes the body runs."
  fi
  if printf '%s\n' "$tools" | sed 's/Bash(/BASH_PAREN/g' | grep -qE '(^|[ ,:-])Bash([ ,]|$)'; then
    add "Bare 'Bash' in allowed-tools pre-approves every command: list 'Bash(cmd *)' shapes."
  fi
  denied=$(printf '%s\n' "$tools" | grep -oE 'Bash\(git (push (-f|--force)|reset|commit --amend)[^)]*\)' | tr '\n' ' ')
  if [ -n "$denied" ]; then
    add "allowed-tools pre-approves ${denied}: leave these out so the approval prompt stays."
  fi

  inline=$(printf '%s\n' "$src" | grep -nE '(^|[[:space:]])!`' | cut -d: -f1 | tr '\n' ' ')
  if [ -n "$inline" ]; then
    add "Inline injection syntax (a bang followed by a backtick) on line(s) ${inline}: it is executed when the skill loads. Describe it in words, or use a bang-fenced block."
  fi

  # Lines inside bang-fenced blocks: one command, optionally followed by a redirect and '|| true'.
  inj=$(printf '%s\n' "$src" | awk '
    /^[[:space:]]*```!/ { on=1; next }
    on && /^[[:space:]]*```/ { on=0; next }
    on && NF {
      l=$0
      sub(/[[:space:]]*\|\|[[:space:]]*true[[:space:]]*$/, "", l)
      sub(/[[:space:]]*2>(\/dev\/null|&1)[[:space:]]*$/, "", l)
      # Drop quoted strings first: a "|" inside a quoted regex is not a pipe.
      gsub(/\047[^\047]*\047/, "", l); gsub(/"[^"]*"/, "", l)
      if (l ~ /\|/ || l ~ /&&/ || l ~ /;/ || l ~ /^[[:space:]]*echo([[:space:]]|$)/) printf "%d ", NR
    }')
  if [ -n "$inj" ]; then
    add "Injected block line(s) ${inj}: a pipe, '&&', ';', 'a || b' or 'echo' is refused and the skill fails to load. Keep one allowed command per line, optionally with '2>/dev/null || true'."
  fi
fi

if [ "$kind" = agent ]; then
  base=$(basename "$file" .md)
  name=$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -n 1 | tr -d "\"'")
  if [ -z "$name" ]; then
    add "Missing 'name' in the frontmatter."
  elif [ "$name" != "$base" ]; then
    add "'name: ${name}' differs from the filename '${base}.md': keep them equal."
  fi
  if ! printf '%s\n' "$fm" | grep -q '^description:'; then
    add "Missing 'description' in the frontmatter."
  fi
  agent_tools=$(printf '%s\n' "$fm" | awk '/^tools:/ { on=1; print; next } on && /^[A-Za-z_-]+:/ { on=0 } on { print }')
  if [ -z "$agent_tools" ]; then
    add "Missing 'tools': without it the subagent gets every tool, including Edit, Bash and Agent."
  elif printf '%s\n' "$agent_tools" | grep -q 'AskUserQuestion'; then
    add "Remove 'AskUserQuestion' from 'tools': it is removed from every subagent."
  fi
  ignored=$(printf '%s\n' "$fm" | grep -oE '^(hooks|mcpServers|permissionMode):' | tr -d ':' | tr '\n' ' ')
  if [ -n "$ignored" ]; then
    add "Ignored in plugin subagents: ${ignored}-> ship hooks in hooks/hooks.json and MCP servers in .mcp.json."
  fi
fi

if [ -n "$errors" ]; then
  if [ "$kind" = skill ]; then rule=plugin-skill-authoring.md; else rule=plugin-agent-authoring.md; fi
  echo "${file}: fix these (see .claude/rules/${rule}):" >&2
  printf '%s' "$errors" >&2
  exit 2
fi
