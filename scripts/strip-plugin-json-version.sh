#!/bin/sh
# Remove `version` from every plugin.json so the early access channel (develop) tracks commits again.
#   sh scripts/strip-plugin-json-version.sh
# Run it on the branch that merges main back into develop, after the release (see CONTRIBUTING.md).
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
for f in "$root"/plugins/*/.claude-plugin/plugin.json; do
  [ -f "$f" ] || continue
  if jq -e 'has("version")' "$f" >/dev/null; then
    tmp=$(mktemp)
    jq 'del(.version)' "$f" > "$tmp"
    cat "$tmp" > "$f"
    rm -f "$tmp"
    echo "removed version: $f"
  fi
done
