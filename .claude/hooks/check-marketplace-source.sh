#!/bin/sh
# PostToolUse hook: after Claude edits .claude-plugin/marketplace.json, fail if any
# plugin entry's source is not a git-subdir object with an https:// url. Exit 2 feeds stderr back to Claude.
# See .claude/rules/marketplace-manifest.md for why.

file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  */.claude-plugin/marketplace.json) ;;
  *) exit 0 ;;
esac

bad=$(jq -r '.plugins[] | select((.source | type) != "object" or .source.source != "git-subdir" or ((.source.url // "") | startswith("https://") | not)) | .name' "$file")
if [ -n "$bad" ]; then
  echo "marketplace.json: these entries must use a git-subdir source with an https:// url (see .claude/rules/marketplace-manifest.md):" >&2
  echo "$bad" >&2
  exit 2
fi
