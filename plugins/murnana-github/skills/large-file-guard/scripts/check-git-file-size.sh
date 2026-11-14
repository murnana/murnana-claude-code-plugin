#!/bin/bash
# PreToolUse hook (matcher: Bash). Before a `git commit`, check the size of every non-LFS file
# that would be committed. GitHub warns at 50 MiB and rejects pushes with a file over 100 MiB,
# so stop the commit before such a file lands in history.
# Exit 2 blocks the command and feeds stderr back to Claude. Exit 0 with no output allows it.
# Override the limits with GIT_FILE_SIZE_WARN_MIB / GIT_FILE_SIZE_BLOCK_MIB.
# Requires: bash, git, jq.

warn_mib=${GIT_FILE_SIZE_WARN_MIB:-50}
block_mib=${GIT_FILE_SIZE_BLOCK_MIB:-100}
warn_bytes=$((warn_mib * 1048576))
block_bytes=$((block_mib * 1048576))

cmd=$(jq -r '.tool_input.command // empty')

# Run only for `git commit`, not for other commands that merely mention it.
printf '%s\n' "$cmd" | grep -Eq '(^|[;&|(]|[[:space:]])git[[:space:]]+(-[Cc][[:space:]]+[^[:space:]]+[[:space:]]+)*commit([[:space:]]|$)' || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

blocked=""
warned=""

fmt_mib() { awk -v b="$1" 'BEGIN { printf "%.1f MiB", b / 1048576 }'; }

record() { # path, size in bytes
  if [ "$2" -ge "$block_bytes" ]; then
    blocked="${blocked}  - $1 ($(fmt_mib "$2"))
"
  elif [ "$2" -ge "$warn_bytes" ]; then
    warned="${warned}  - $1 ($(fmt_mib "$2"))
"
  fi
}

# 1. Staged files. The index blob of an LFS-tracked file is a small pointer, so LFS files pass
#    on their own. A file marked as LFS but not converted (git-lfs missing) is still large here.
while IFS= read -r -d '' path; do
  size=$(git cat-file -s ":$path" 2>/dev/null) || continue
  record "$path" "$size"
done < <(git diff --cached --name-only -z --diff-filter=ACMR 2>/dev/null)

# 2. `git commit -a` / `--all` also takes modified tracked files that are not staged yet.
#    Their working-tree content is not converted to a pointer yet, so skip LFS-tracked paths.
if printf '%s\n' "$cmd" | grep -Eq '(^|[[:space:]])(--all|-[A-Za-z]*a[A-Za-z]*)([[:space:]]|$)'; then
  while IFS= read -r -d '' path; do
    [ -f "$path" ] || continue
    filter=$(git check-attr filter -- "$path" 2>/dev/null | sed 's/.*: //')
    [ "$filter" = "lfs" ] && continue
    size=$(wc -c < "$path" | tr -d '[:space:]')
    record "$path" "$size"
  done < <(git diff --name-only -z --diff-filter=ACMR 2>/dev/null)
fi

if [ -n "$blocked" ]; then
  {
    echo "git commit blocked: these files are ${block_mib} MiB or larger and not stored in Git LFS."
    echo "GitHub rejects a push that contains a file over 100 MiB."
    printf '%s' "$blocked"
    echo "Do not commit them as they are. Ask the user whether to:"
    echo "  - track them with Git LFS: git lfs track '<pattern>' && git add .gitattributes <file>"
    echo "    (needs git-lfs installed; unstage first with git restore --staged <file>)"
    echo "  - leave them out of the commit and add them to .gitignore"
    echo "  - split or compress them"
    if [ -n "$warned" ]; then
      echo "Also over ${warn_mib} MiB (GitHub warns on push):"
      printf '%s' "$warned"
    fi
  } >&2
  exit 2
fi

if [ -n "$warned" ]; then
  msg="Large files in this commit (GitHub warns on push above ${warn_mib} MiB and rejects above ${block_mib} MiB). Tell the user before committing:
${warned}"
  jq -n --arg msg "$msg" '{hookSpecificOutput:{hookEventName:"PreToolUse",additionalContext:$msg}}'
fi
exit 0
