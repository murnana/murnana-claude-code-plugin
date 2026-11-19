#!/bin/sh
# Set a plugin's release version in the stable catalog and pin its source to the released commit.
#   sh scripts/set-plugin-version.sh <plugin-name> <MAJOR.MINOR.PATCH>
# Updates `version` and `source.sha` on the entry in .claude-plugin/marketplace.json, then
# regenerates the dev channel catalog. `source.sha` becomes the last commit on HEAD that changed
# plugins/<plugin-name>/, so commit the plugin's changes first and push that commit.
# See .claude/rules/plugin-version-bump.md.
set -eu

if [ $# -ne 2 ]; then
  echo "usage: sh scripts/set-plugin-version.sh <plugin-name> <MAJOR.MINOR.PATCH>" >&2
  exit 2
fi
name=$1
version=$2
if ! printf '%s' "$version" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; then
  echo "version must be MAJOR.MINOR.PATCH without a v prefix (got '$version')" >&2
  exit 2
fi

root=$(cd "$(dirname "$0")/.." && pwd)
stable="$root/.claude-plugin/marketplace.json"
self_url="https://github.com/murnana/murnana-claude-code-plugin.git"

if ! jq -e --arg n "$name" --arg url "$self_url" \
    'any(.plugins[]; .name == $n and .source.url == $url)' "$stable" >/dev/null; then
  echo "$name is not an entry of this repository in .claude-plugin/marketplace.json" >&2
  exit 1
fi
if [ -n "$(git -C "$root" status --porcelain -- "plugins/$name")" ]; then
  echo "plugins/$name has uncommitted changes; commit them first so the pinned commit contains them" >&2
  exit 1
fi
sha=$(git -C "$root" log -1 --format=%H HEAD -- "plugins/$name")
if [ -z "$sha" ]; then
  echo "no commit on HEAD touches plugins/$name" >&2
  exit 1
fi

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
jq --arg n "$name" --arg v "$version" --arg sha "$sha" \
  '.plugins |= map(if .name == $n then .version = $v | .source |= (del(.ref) | .sha = $sha) else . end)' \
  "$stable" > "$tmp"
cat "$tmp" > "$stable"

sh "$root/scripts/build-dev-marketplace.sh"
echo "$name: version $version, sha $sha"
