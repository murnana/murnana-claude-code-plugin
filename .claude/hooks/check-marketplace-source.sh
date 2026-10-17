#!/bin/sh
# PostToolUse hook: after Claude edits .claude-plugin/marketplace.json, fail if any
# plugin entry's source is not a git-subdir object. Exit 2 feeds stderr back to Claude.
# See .claude/rules/marketplace-manifest.md for why.

file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  */.claude-plugin/marketplace.json) ;;
  *) exit 0 ;;
esac

bad=$(jq -r '.plugins[] | select((.source | type) != "object" or .source.source != "git-subdir") | .name' "$file")
if [ -n "$bad" ]; then
  echo "marketplace.json: these entries must use a git-subdir source (see .claude/rules/marketplace-manifest.md):" >&2
  echo "$bad" >&2
  exit 2
fi
