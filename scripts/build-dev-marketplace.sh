#!/bin/sh
# Generate the dev (early access) channel catalog from the stable one.
#   sh scripts/build-dev-marketplace.sh          write channels/dev/.claude-plugin/marketplace.json
#   sh scripts/build-dev-marketplace.sh --check  exit 1 if the committed file is out of date
# The dev catalog renames the marketplace, drops every version and release commit pin, and points
# this repository's plugins at the develop branch, so installs track develop by
# commit SHA.
# channels/dev/extra-plugins.json lists plugins published only on the dev channel (for example
# from other repositories); they are appended unchanged.
# See .claude/rules/release-channels.md for why.
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
stable="$root/.claude-plugin/marketplace.json"
dev="$root/channels/dev/.claude-plugin/marketplace.json"
extra="$root/channels/dev/extra-plugins.json"
self_url="https://github.com/murnana/murnana-claude-code-plugin.git"

generated=$(jq --arg url "$self_url" --slurpfile extra "$extra" '
  .name += "-dev"
  | .description += " (early access: follows the develop branch, without release versions)"
  | .plugins |= map(
      if (.source | type) == "object" and .source.url == $url
      then del(.version, .source.sha) | .source.ref = "develop"
      else .
      end)
  | .plugins += $extra[0]
' "$stable")

if [ "${1:-}" = "--check" ]; then
  if ! printf '%s\n' "$generated" | diff -u "$dev" - >&2; then
    echo "channels/dev/.claude-plugin/marketplace.json is out of date. Run: sh scripts/build-dev-marketplace.sh" >&2
    exit 1
  fi
  exit 0
fi

mkdir -p "$(dirname "$dev")"
printf '%s\n' "$generated" > "$dev"
